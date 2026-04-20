"""
Extractor views — wraps the docling_extract pipeline in a Django web interface.

Job lifecycle:
    POST /run/            → start background extraction, return {job_id}
    GET  /status/<id>/    → return {status, message, elapsed, filename}
    GET  /download/<id>/  → serve produced xlsx (or zip for multiple PDFs)
    GET  /history/        → return list of recent completed jobs
"""

# NOTE: Only one complete implementation lives here.  The file was previously
# corrupted by a duplicate (old SSE-based) copy appended below this section.

import shutil
import tempfile
import threading
import time
import uuid
import zipfile
from collections import deque
from pathlib import Path

from django.conf import settings
from django.http import FileResponse, Http404, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
MAX_FILE_SIZE  = 50 * 1024 * 1024   # 50 MB per file
JOB_TIMEOUT    = 600                 # seconds before a hung job is marked error
CLEANUP_DELAY  = 300                 # seconds after download before tmp cleanup
HISTORY_MAX    = 20                  # max entries kept in job history

# ---------------------------------------------------------------------------
# In-memory job registry and history
# ---------------------------------------------------------------------------
_JOBS: dict = {}
_JOBS_LOCK = threading.Lock()
_HISTORY: deque = deque(maxlen=HISTORY_MAX)
_HISTORY_LOCK = threading.Lock()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _set_message(job_id: str, msg: str):
    with _JOBS_LOCK:
        if job_id in _JOBS:
            _JOBS[job_id]["message"] = msg


# ---------------------------------------------------------------------------
# Views
# ---------------------------------------------------------------------------

def index(request):
    return render(request, "extractor/index.html")


@csrf_exempt
@require_POST
def run(request):
    pdf_files = request.FILES.getlist("pdfs")

    if not pdf_files:
        return JsonResponse({"error": "No PDF files uploaded."}, status=400)

    # Validate each file: size and PDF magic bytes
    for f in pdf_files:
        if f.size > MAX_FILE_SIZE:
            return JsonResponse(
                {"error": f"{f.name} exceeds the 50 MB size limit."}, status=400
            )
        header = f.read(5)
        f.seek(0)
        if header != b"%PDF-":
            return JsonResponse(
                {"error": f"{f.name} is not a valid PDF file."}, status=400
            )

    # Save all PDFs to a temp directory
    tmp_dir = Path(tempfile.mkdtemp())
    pdf_paths = []
    for f in pdf_files:
        dest = tmp_dir / f.name
        with open(dest, "wb") as fh:
            for chunk in f.chunks():
                fh.write(chunk)
        pdf_paths.append(dest)

    default = getattr(settings, "NRM_DB_DEFAULT", None)
    nrm_path = Path(default) if default and Path(default).exists() else None

    job_id = str(uuid.uuid4())
    now = time.time()

    with _JOBS_LOCK:
        _JOBS[job_id] = {
            "status": "running",
            "message": "Queued…",
            "started_at": now,
            "output_path": None,
            "filenames": [p.name for p in pdf_paths],
            "error": None,
            "tmp_dir": tmp_dir,
        }

    worker = threading.Thread(
        target=_run_extraction,
        args=(job_id, pdf_paths, nrm_path),
        daemon=True,
    )
    worker.start()

    # Watchdog: mark job as error if it exceeds JOB_TIMEOUT
    def _watchdog():
        worker.join(timeout=JOB_TIMEOUT)
        if worker.is_alive():
            with _JOBS_LOCK:
                job = _JOBS.get(job_id, {})
                if job.get("status") == "running":
                    job["status"] = "error"
                    job["error"] = (
                        f"Processing timed out after {JOB_TIMEOUT // 60} minutes."
                    )

    threading.Thread(target=_watchdog, daemon=True).start()

    return JsonResponse({"job_id": job_id})


@require_GET
def status(request, job_id):
    with _JOBS_LOCK:
        job = _JOBS.get(job_id)
    if not job:
        raise Http404
    elapsed = int(time.time() - job.get("started_at", time.time()))
    output_path = job.get("output_path")
    return JsonResponse({
        "status": job.get("status", "running"),
        "message": job.get("message", ""),
        "elapsed": elapsed,
        "filename": Path(output_path).name if output_path else "",
        "error": job.get("error") or "",
    })


@require_GET
def history(request):
    with _HISTORY_LOCK:
        entries = list(_HISTORY)
    return JsonResponse({"history": entries})


@require_GET
def download(request, job_id):
    with _JOBS_LOCK:
        job = _JOBS.get(job_id)
    if not job:
        raise Http404
    output_path = job.get("output_path")
    if not output_path or not Path(output_path).exists():
        raise Http404

    # Schedule temp directory cleanup after CLEANUP_DELAY seconds
    tmp_dir = job.get("tmp_dir")

    def _cleanup():
        if tmp_dir and Path(tmp_dir).exists():
            shutil.rmtree(tmp_dir, ignore_errors=True)
        with _JOBS_LOCK:
            _JOBS.pop(job_id, None)

    threading.Timer(CLEANUP_DELAY, _cleanup).start()

    return FileResponse(
        open(output_path, "rb"),
        as_attachment=True,
        filename=Path(output_path).name,
    )


# ---------------------------------------------------------------------------
# Background extraction worker
# ---------------------------------------------------------------------------

def _run_extraction(job_id: str, pdf_paths: list, nrm_path):
    """Run the full extraction pipeline in a background thread."""
    try:
        from docling_extract import (
            IcmsMatcher,
            NRMMatcher,
            UniclassMatcher,
            process_pdf,
        )
        from docling.document_converter import DocumentConverter

        _set_message(job_id, "Loading NRM database…")
        nrm_matcher = None
        if nrm_path and Path(nrm_path).exists():
            nrm_matcher = NRMMatcher(nrm_path)

        icms_matcher = None
        uniclass_matcher = None
        if nrm_matcher:
            _set_message(job_id, "Building ICMS & Uniclass matchers…")
            icms_matcher = IcmsMatcher(model=nrm_matcher.model)
            uniclass_matcher = UniclassMatcher(model=nrm_matcher.model)

        _set_message(job_id, "Initialising Docling AI models…")
        converter = DocumentConverter()

        output_paths = []
        total = len(pdf_paths)
        for idx, pdf_path in enumerate(pdf_paths, 1):
            _set_message(job_id, f"Processing {pdf_path.name} ({idx}/{total})…")
            out = process_pdf(
                converter, pdf_path, nrm_matcher, None,
                icms_matcher, uniclass_matcher,
            )
            output_paths.append(out)

        # Multiple PDFs → zip all xlsx outputs into one archive
        if len(output_paths) > 1:
            _set_message(job_id, "Creating ZIP archive…")
            with _JOBS_LOCK:
                tmp_dir = _JOBS[job_id]["tmp_dir"]
            zip_path = tmp_dir / "cost_plan_extracts.zip"
            with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
                for p in output_paths:
                    zf.write(p, p.name)
            final_output = zip_path
        else:
            final_output = output_paths[0]

        with _JOBS_LOCK:
            _JOBS[job_id]["output_path"] = final_output
            _JOBS[job_id]["status"] = "done"
            _JOBS[job_id]["message"] = "Complete"

        with _HISTORY_LOCK:
            _HISTORY.appendleft({
                "job_id": job_id,
                "filename": Path(final_output).name,
                "filenames_in": [p.name for p in pdf_paths],
                "completed_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            })

    except Exception as exc:
        with _JOBS_LOCK:
            _JOBS[job_id]["error"] = str(exc)
            _JOBS[job_id]["status"] = "error"
            _JOBS[job_id]["message"] = "Failed"
