"""
Cost Plan PDF Table Extractor (Docling AI)
==========================================
Uses IBM Docling's TableFormer AI model to extract complex tables from
cost plan PDFs and write them into Excel workbooks.

Handles both text-based and scanned PDFs automatically.

Usage:
    python docling_extract.py <pdf_file_or_folder>

Dependencies:
    pip install docling openpyxl
"""

import sys
import logging
from pathlib import Path

from docling.document_converter import DocumentConverter
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill
from openpyxl.utils import get_column_letter

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)

# Suppress noisy third-party loggers
for noisy in ("docling", "transformers", "PIL", "urllib3", "huggingface_hub"):
    logging.getLogger(noisy).setLevel(logging.WARNING)


# ═══════════════════════════════════════════════════════════════════════════
#  STYLING CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════
HEADER_FONT = Font(name="Calibri", bold=True, size=11, color="FFFFFF")
HEADER_FILL = PatternFill(start_color="2F5496", end_color="2F5496", fill_type="solid")
HEADER_ALIGNMENT = Alignment(horizontal="center", vertical="center", wrap_text=True)
CELL_FONT = Font(name="Calibri", size=11)
CELL_ALIGNMENT = Alignment(vertical="top", wrap_text=True)
THIN_BORDER = Border(
    left=Side(style="thin"),
    right=Side(style="thin"),
    top=Side(style="thin"),
    bottom=Side(style="thin"),
)


# ═══════════════════════════════════════════════════════════════════════════
#  EXCEL WRITER
# ═══════════════════════════════════════════════════════════════════════════

def write_tables_to_excel(tables_data, output_path):
    """
    Write all extracted tables continuously onto a single Excel sheet.

    Tables are stacked vertically with a label row and a blank-row gap
    between each table.

    Parameters
    ----------
    tables_data : list of dict
        Each dict has keys: "sheet_name" (str), "dataframe" (pd.DataFrame).
    output_path : str | Path
        Destination .xlsx path.
    """
    LABEL_FONT = Font(name="Calibri", bold=True, size=12, color="1F3864")
    GAP_ROWS = 2  # blank rows between tables

    wb = Workbook()
    ws = wb.active
    ws.title = "Extracted Tables"

    if not tables_data:
        ws.cell(row=1, column=1, value="No tables were detected in this PDF.")
        ws.cell(row=1, column=1).font = Font(name="Calibri", size=12, italic=True)
        wb.save(output_path)
        log.info("Saved  %s  (no tables)", output_path)
        return

    current_row = 1

    for t_idx, entry in enumerate(tables_data):
        label = entry["sheet_name"]
        df = entry["dataframe"]

        # -- Table label row --
        label_cell = ws.cell(
            row=current_row, column=1,
            value=f"Table {t_idx + 1} -- {label}",
        )
        label_cell.font = LABEL_FONT
        current_row += 1

        # -- Header row --
        for c_idx, col_name in enumerate(df.columns, start=1):
            cell = ws.cell(row=current_row, column=c_idx, value=str(col_name))
            cell.font = HEADER_FONT
            cell.fill = HEADER_FILL
            cell.alignment = HEADER_ALIGNMENT
            cell.border = THIN_BORDER
        current_row += 1

        # -- Data rows --
        for row_tuple in df.itertuples(index=False):
            for c_idx, value in enumerate(row_tuple, start=1):
                cell = ws.cell(row=current_row, column=c_idx, value=value)
                cell.font = CELL_FONT
                cell.alignment = CELL_ALIGNMENT
                cell.border = THIN_BORDER
            current_row += 1

        # -- Gap before next table --
        current_row += GAP_ROWS

    # -- Auto-size columns across all data --
    for col_idx in range(1, ws.max_column + 1):
        max_len = 0
        col_letter = get_column_letter(col_idx)
        for row in ws.iter_rows(min_col=col_idx, max_col=col_idx):
            for cell in row:
                if cell.value:
                    max_len = max(max_len, len(str(cell.value)))
        ws.column_dimensions[col_letter].width = min(max_len + 4, 60)

    # -- Footer note --
    note_cell = ws.cell(
        row=current_row, column=1,
        value="[Extracted via Docling AI (TableFormer)]",
    )
    note_cell.font = Font(name="Calibri", size=9, italic=True, color="888888")

    wb.save(output_path)
    log.info("Saved  %s  (%d table(s) on 1 sheet)", output_path, len(tables_data))


# ═══════════════════════════════════════════════════════════════════════════
#  MAIN PIPELINE
# ═══════════════════════════════════════════════════════════════════════════

def process_pdf(converter, pdf_path):
    """
    Extract every table from a PDF using Docling and write to Excel.

    Returns the output Excel path.
    """
    pdf_path = Path(pdf_path)
    output_path = pdf_path.with_name(pdf_path.stem + "_docling_tables.xlsx")

    log.info("Processing  %s", pdf_path.name)

    result = converter.convert(str(pdf_path))
    doc = result.document

    tables = list(doc.tables)
    log.info("  Found %d table(s)", len(tables))

    tables_data = []
    for t_idx, table in enumerate(tables):
        try:
            df = table.export_to_dataframe(doc=doc)

            # Build a meaningful sheet name
            # Try to get the page number from the table's provenance
            page_label = ""
            if hasattr(table, "prov") and table.prov:
                try:
                    page_no = table.prov[0].page_no
                    page_label = f"P{page_no}"
                except (IndexError, AttributeError):
                    pass

            if page_label:
                sheet_name = f"{page_label}_Table_{t_idx + 1}"
            else:
                sheet_name = f"Table_{t_idx + 1}"

            log.info(
                "  Table %d: %d rows x %d cols %s",
                t_idx + 1, len(df), len(df.columns),
                f"(page {page_label})" if page_label else "",
            )

            tables_data.append({
                "sheet_name": sheet_name,
                "dataframe": df,
            })
        except Exception as exc:
            log.warning("  Table %d: export failed - %s", t_idx + 1, exc)

    write_tables_to_excel(tables_data, output_path)
    return output_path


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        print("Error: please provide a PDF file or folder path.")
        sys.exit(1)

    target = Path(sys.argv[1])

    if target.is_file() and target.suffix.lower() == ".pdf":
        pdf_files = [target]
    elif target.is_dir():
        pdf_files = sorted(target.glob("*.pdf"))
        if not pdf_files:
            log.error("No PDF files found in %s", target)
            sys.exit(1)
        log.info("Found %d PDF(s) in %s", len(pdf_files), target)
    else:
        log.error("Path is not a valid PDF file or directory: %s", target)
        sys.exit(1)

    # Initialise Docling converter once (loads models into memory)
    log.info("Initialising Docling AI models (this may take a moment on first run)...")
    converter = DocumentConverter()
    log.info("Models loaded.")

    results = []
    for pdf_file in pdf_files:
        try:
            out = process_pdf(converter, pdf_file)
            results.append((pdf_file.name, out, None))
        except Exception as exc:
            log.error("FAILED  %s : %s", pdf_file.name, exc)
            results.append((pdf_file.name, None, str(exc)))

    # Print summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    for name, out, err in results:
        if err:
            print(f"  [FAIL]  {name}  ->  ERROR: {err}")
        else:
            print(f"  [OK]    {name}  ->  {out.name}")
    print("=" * 60)


if __name__ == "__main__":
    main()
