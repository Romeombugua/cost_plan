import sys
import logging
import threading
from pathlib import Path

# torch must be imported before PyQt6 on Windows to avoid DLL initialization failure (WinError 1114)
import torch  # noqa: F401

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QCheckBox, QTextEdit, QFileDialog, QMessageBox
)
from PyQt6.QtCore import pyqtSignal, QObject, Qt, QTimer

from docling_extract import process_pdf, NRMMatcher, OllamaLLMVerifier, _find_nrm_db, IcmsMatcher, UniclassMatcher
from docling.document_converter import DocumentConverter

class LogEmitter(QObject):
    log_signal = pyqtSignal(str)
    done_signal = pyqtSignal()

    def write(self, msg):
        self.log_signal.emit(msg)

    def flush(self):
        pass

class RedirectText(logging.Handler):
    def __init__(self, emitter):
        super().__init__()
        self.emitter = emitter

    def emit(self, record):
        msg = self.format(record)
        self.emitter.write(msg)

class DoclingGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cost Plan PDF Extractor")
        self.resize(700, 500)
        self.emitter = LogEmitter()
        self.emitter.log_signal.connect(self.append_log)
        self.emitter.done_signal.connect(self.on_processing_done)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QVBoxLayout(central_widget)

        self.setup_ui()
        self.setup_logging()

    def setup_ui(self):
        # PDF Target Selection
        target_layout = QHBoxLayout()
        target_layout.addWidget(QLabel("PDF File/Folder:"))
        self.target_input = QLineEdit()
        target_layout.addWidget(self.target_input)
        
        btn_br_file = QPushButton("Browse File")
        btn_br_file.clicked.connect(self.browse_file)
        target_layout.addWidget(btn_br_file)
        
        btn_br_folder = QPushButton("Browse Folder")
        btn_br_folder.clicked.connect(self.browse_folder)
        target_layout.addWidget(btn_br_folder)
        self.main_layout.addLayout(target_layout)

        # Options
        options_layout = QHBoxLayout()
        self.chk_use_llm = QCheckBox("Use LLM for Verification (Ollama)")
        self.chk_use_llm.setChecked(True)
        options_layout.addWidget(self.chk_use_llm)
        options_layout.addStretch()
        self.main_layout.addLayout(options_layout)

        # Run Button
        self.btn_run = QPushButton("Run Extraction")
        self.btn_run.setStyleSheet("background-color: green; color: white; padding: 10px; font-weight: bold;")
        self.btn_run.clicked.connect(self.start_processing)
        self.main_layout.addWidget(self.btn_run)

        # Logging View
        self.main_layout.addWidget(QLabel("Logs:"))
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.main_layout.addWidget(self.log_text)

    def setup_logging(self):
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        for h in logger.handlers[:]:
            logger.removeHandler(h)
            
        handler = RedirectText(self.emitter)
        handler.setFormatter(logging.Formatter("%(asctime)s  %(levelname)-8s  %(message)s", "%H:%M:%S"))
        logger.addHandler(handler)

    def append_log(self, text):
        self.log_text.append(text)
        # Scroll to bottom
        scrollbar = self.log_text.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
        
    def on_processing_done(self):
        self.btn_run.setEnabled(True)
        self.btn_run.setText("Run Extraction")
        self.append_log("--- Finished ---")

    def browse_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select PDF File", "", "PDF Files (*.pdf)")
        if path:
            self.target_input.setText(path)

    def browse_folder(self):
        path = QFileDialog.getExistingDirectory(self, "Select Folder")
        if path:
            self.target_input.setText(path)

    def start_processing(self):
        target = self.target_input.text()
        if not target:
            QMessageBox.critical(self, "Error", "Please select a PDF file or folder.")
            return

        self.btn_run.setEnabled(False)
        self.btn_run.setText("Processing...")

        use_llm = self.chk_use_llm.isChecked()

        threading.Thread(target=self.process, args=(target, use_llm), daemon=True).start()

    def process(self, target_path_str, use_llm):
        log = logging.getLogger(__name__)
        target = Path(target_path_str)

        try:
            if target.is_file() and target.suffix.lower() == ".pdf":
                pdf_files = [target]
            elif target.is_dir():
                pdf_files = sorted(target.glob("*.pdf"))
                if not pdf_files:
                    log.error(f"No PDF files found in {target}")
                    return
            else:
                log.error(f"Invalid path: {target}")
                return

            nrm_db_path = _find_nrm_db(target)

            nrm_matcher = None
            if nrm_db_path and nrm_db_path.exists():
                log.info(f"NRM database found: {nrm_db_path}")
                nrm_matcher = NRMMatcher(nrm_db_path)
            else:
                log.warning("NRM database not found — skipping NRM enrichment.")

            icms_matcher = None
            uniclass_matcher = None
            if nrm_matcher:
                log.info("Building ICMS matcher ...")
                icms_matcher = IcmsMatcher(model=nrm_matcher.model)
                log.info("Building Uniclass matcher ...")
                uniclass_matcher = UniclassMatcher(model=nrm_matcher.model)

            llm_verifier = None
            if nrm_matcher and use_llm:
                verifier = OllamaLLMVerifier()
                if verifier.ping():
                    llm_verifier = verifier
                    log.info(f"Ollama LLM verifier ready (model: {verifier.model})")
                else:
                    log.warning("Ollama not available — LLM verification disabled.")

            log.info("Initialising Docling AI models...")
            converter = DocumentConverter()
            log.info("Models loaded.")

            for pdf_file in pdf_files:
                try:
                    process_pdf(
                        converter, pdf_file, nrm_matcher, llm_verifier,
                        icms_matcher, uniclass_matcher,
                    )
                except Exception as exc:
                    log.error(f"FAILED {pdf_file.name}: {exc}")

            log.info("Processing complete.")
        except Exception as e:
            log.error(f"An error occurred: {e}")
        finally:
            self.emitter.done_signal.emit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DoclingGUI()
    window.show()
    sys.exit(app.exec())
