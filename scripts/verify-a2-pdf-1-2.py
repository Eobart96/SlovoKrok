import sys
from pathlib import Path

import pdfplumber
from pypdf import PdfReader


path = Path(sys.argv[1])
reader = PdfReader(path)
assert len(reader.pages) == 7, f"expected 7 pages, got {len(reader.pages)}"
assert not reader.is_encrypted
assert "/AcroForm" not in reader.trailer["/Root"]

with pdfplumber.open(path) as pdf:
    assert all(abs(page.width - 595.276) < 1 and abs(page.height - 841.89) < 1 for page in pdf.pages)
    page_texts = [(page.extract_text() or "").strip() for page in pdf.pages]
    assert all(len(text) > 250 for text in page_texts), [len(text) for text in page_texts]

text = "\n".join(page_texts)
required = [
    "Вид глагола", "Вид - это не время", "Как учить видовые пары",
    "Вид в прошедшем и будущем", "Банк примеров", "Частые ошибки",
    "Упражнение 6", "Ответы", "Финальная проверка",
    "nedokonavý vid", "dokonavý vid", "budem + infinitív",
]
for item in required:
    assert item in text, item

pairs = [
    "robiť", "urobiť", "písať", "napísať", "čítať", "prečítať",
    "variť", "uvariť", "volať", "zavolať", "jesť", "zjesť",
    "piť", "vypiť", "kupovať", "kúpiť", "otvárať", "otvoriť",
    "dávať", "dať", "brať", "vziať",
]
assert all(form in text for form in pairs)
assert text.count("Упражнение ") >= 6
for a1_heading in ["Шесть личных форм", "Частые особые глаголы", "Когда используется настоящее время"]:
    assert a1_heading not in text

print("corrected A2 PDF 1.2 structure verified")
print("corrected A2 PDF 1.2 learning content verified")
