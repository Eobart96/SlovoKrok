import re
import subprocess
from pathlib import Path

import pdfplumber
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "output" / "pdf" / "A2" / "Module_01" / "Slovak_A2_Tema_1_7_Proiznoshenie_svyaznaya_rech.pdf"
PDFINFO = Path(r"C:\Users\Eobar\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\poppler\Library\bin\pdfinfo.exe")

assert PDF.exists(), f"Missing PDF: {PDF}"
assert PDF.stat().st_size > 50_000, "PDF is unexpectedly small"

reader = PdfReader(str(PDF))
assert len(reader.pages) == 7, f"Expected 7 pages, got {len(reader.pages)}"
assert reader.metadata.title == "Slovak A2 - Тема 1.7 - Произношение A2: связная речь"

with pdfplumber.open(PDF) as document:
    texts = [(page.extract_text() or "") for page in document.pages]
    for index, page in enumerate(document.pages, start=1):
        assert abs(page.width - 595.276) < 1, f"Page {index}: wrong width"
        assert abs(page.height - 841.890) < 1, f"Page {index}: wrong height"
        assert len(texts[index - 1].strip()) > 250, f"Page {index}: too little extractable text"

full_text = "\n".join(texts)
required = [
    "Произношение A2", "Výslovnosť A2: súvislá reč", "Оглушение и озвончение",
    "pod stolom", "s bratom", "Группы согласных", "štvrtok", "Долгота, ударение и ритм",
    "rad - rád", "Ритмический закон", "Интонация длинной фразы", "Prídeš zajtra?",
    "Упражнение 6", "Ответы", "модулю 2.1",
]
for phrase in required:
    assert phrase in full_text, f"Missing phrase: {phrase}"

for page_number in range(1, 8):
    assert f"стр. {page_number} / 7" in texts[page_number - 1], f"Missing page number on page {page_number}"

for bad in ["�", "□", "*inform", "–", "—"]:
    assert bad not in full_text, f"Forbidden or broken character found: {bad}"

assert not re.search(r"[\u2010-\u2014]", full_text), "Non-ASCII dash found"

info = subprocess.run([str(PDFINFO), str(PDF)], check=True, capture_output=True, text=True, encoding="utf-8", errors="replace").stdout
assert "Pages:           7" in info
assert "Page size:       595.276 x 841.89 pts (A4)" in info
assert "PDF syntax error" not in info

print(f"OK: {PDF}")
print(f"pages={len(reader.pages)} size={PDF.stat().st_size} chars={len(full_text)}")
