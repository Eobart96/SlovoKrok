import re
import subprocess
from pathlib import Path

import pdfplumber
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "output" / "pdf" / "A2" / "Module_02" / "Slovak_A2_Tema_2_2_Nominativ_mnozhestvennogo_chisla_lyudi.pdf"
PDFINFO = Path(r"C:\Users\Eobar\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\poppler\Library\bin\pdfinfo.exe")

assert PDF.exists(), f"Missing PDF: {PDF}"
assert PDF.stat().st_size > 50_000, "PDF is unexpectedly small"

reader = PdfReader(str(PDF))
assert len(reader.pages) == 7, f"Expected 7 pages, got {len(reader.pages)}"
assert reader.metadata.title == "Slovak A2 - Тема 2.2 - Nominatív множественного числа: люди"

with pdfplumber.open(PDF) as document:
    texts = [(page.extract_text() or "") for page in document.pages]
    for index, page in enumerate(document.pages, start=1):
        assert abs(page.width - 595.276) < 1, f"Page {index}: wrong width"
        assert abs(page.height - 841.890) < 1, f"Page {index}: wrong height"
        assert len(texts[index - 1].strip()) > 250, f"Page {index}: too little extractable text"

full_text = "\n".join(texts)
required = [
    "Nominatív множественного числа", "Nominatív množného čísla: ľudia",
    "Три частотных окончания", "chlap -> chlapi", "učiteľ -> učitelia",
    "kolega -> kolegovia", "človek -> ľudia", "Профессии, национальности",
    "Полная цепочка согласования", "tí noví kolegovia", "moji dobrí priatelia",
    "dvaja muži", "traja učitelia", "štyria študenti", "Упражнение 6",
    "Ответы", "модуле 2.3",
]
for phrase in required:
    assert phrase in full_text, f"Missing phrase: {phrase}"

for page_number in range(1, 8):
    assert f"стр. {page_number} / 7" in texts[page_number - 1], f"Missing page number on page {page_number}"

for bad in ["�", "□", "–", "—", "*kolega"]:
    assert bad not in full_text, f"Forbidden or broken character found: {bad}"

assert not re.search(r"[\u2010-\u2014]", full_text), "Non-ASCII dash found"
assert "toho nového kolegu" in full_text, "Bridge to module 2.3 is missing"
assert "Akuzatív множественного числа" not in full_text, "Module 2.4 content leaked into 2.2"

info = subprocess.run([str(PDFINFO), str(PDF)], check=True, capture_output=True, text=True, encoding="utf-8", errors="replace").stdout
assert "Pages:           7" in info
assert "Page size:       595.276 x 841.89 pts (A4)" in info
assert "PDF syntax error" not in info

print(f"OK: {PDF}")
print(f"pages={len(reader.pages)} size={PDF.stat().st_size} chars={len(full_text)}")
