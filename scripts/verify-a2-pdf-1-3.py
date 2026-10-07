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
    "Клитики и", "Что такое вторая позиция", "Порядок внутри группы",
    "Прошедшее, условие и придаточные", "Короткая или ударная форма",
    "Частые ошибки", "Упражнение 6", "Ответы", "Финальная проверка",
    "by - som - sa/si - datív - akuzatív",
]
for item in required:
    assert item in text, item

examples = [
    "Včera som mu zavolal", "Po práci som mu zavolal", "Včera som sa vrátil",
    "Ráno som ti ho poslal", "Určite by som sa ti ospravedlnil",
    "Tento nápad sa mi páči", "Viem, že sa ti to páči",
    "Keď som sa vrátil", "Prosím ho, aby mi zavolal",
    "Mne dal knihu", "Videl práve jeho", "Idem k nemu",
]
assert all(example in text for example in examples)
assert text.count("Упражнение ") >= 6
for rejected in ["-l-формы", "настоящее время: расширенная система спряжения"]:
    assert rejected not in text.lower()

print("A2 PDF 1.3 structure verified")
print("A2 PDF 1.3 learning content verified")
