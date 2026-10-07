import re
import sys
from pathlib import Path

import pdfplumber
from pypdf import PdfReader


path = Path(sys.argv[1])
if not path.is_file() or path.stat().st_size < 40_000:
    raise SystemExit("PDF missing or unexpectedly small")

reader = PdfReader(str(path))
if len(reader.pages) != 7:
    raise SystemExit(f"Expected 7 pages, found {len(reader.pages)}")

for index, page in enumerate(reader.pages, 1):
    width = float(page.mediabox.width)
    height = float(page.mediabox.height)
    if abs(width - 595.28) > 2 or abs(height - 841.89) > 2:
        raise SystemExit(f"Page {index} is not A4: {width} x {height}")

with pdfplumber.open(path) as pdf:
    page_texts = [(page.extract_text() or "").strip() for page in pdf.pages]

if any(len(text) < 250 for text in page_texts):
    sparse = [index for index, text in enumerate(page_texts, 1) if len(text) < 250]
    raise SystemExit(f"Pages with too little extractable text: {sparse}")

full_text = "\n".join(page_texts)
required = [
    "Вакансия, анкета и условия работы",
    "Как читать вакансию",
    "Даты, Akuzatív и Lokál",
    "Анкета и личные местоимения",
    "Вежливые вопросы об условиях",
    "Банк фраз и упражнения",
    "Ответы и проверка мастерства",
    "Упражнение 1",
    "Упражнение 6",
    "Финальная проверка",
]
missing = [item for item in required if item not in full_text]
if missing:
    raise SystemExit(f"Missing required sections: {missing}")

slovak_examples = [
    "Hľadáme recepčnú", "komunikácia s hosťami", "Nástup od 15. októbra",
    "Hľadáme predavača", "Pošlite životopis a formulár", "Ovládam angličtinu",
    "Práca je v novom sklade", "Pracujem na recepcii", "Mám prax v administratíve",
    "Nástup je možný od 1. novembra 2026", "Pošlite žiadosť do 20. októbra",
    "Môžem nastúpiť ihneď", "Termín nástupu je dohodou", "Kontaktujte ma",
    "Pošlem vám formulár", "Pozvali nás", "Aký je, prosím, pracovný čas",
    "Pracuje sa aj cez víkend", "Kde presne je miesto výkonu práce",
    "Kedy je možný nástup", "Mohli by ste spresniť náplň práce",
    "Ponúkate zaškolenie", "Aká je ponúkaná mzda", "Ponuka ma zaujala",
    "Mám o túto pozíciu záujem", "Formulár som vyplnila elektronicky",
    "Životopis Vám posielam v prílohe", "Termín pohovoru mi vyhovuje",
]
found = sum(example in full_text for example in slovak_examples)
if found < 20:
    raise SystemExit(f"Fewer than 20 expected Slovak examples were found: {found}")

if re.search(r"[\u4e00-\u9fff\u3040-\u30ff\u0600-\u06ff]", full_text):
    raise SystemExit("Unexpected non-Cyrillic/non-Latin script detected")

for forbidden in ["pretože/preto", "kedy/keď", "preniesť stretnutie"]:
    if forbidden in full_text:
        raise SystemExit(f"Content reserved for topic 7.3 leaked into the lesson: {forbidden}")

print("A2 PDF 7.2 structure verified")
print("A2 PDF 7.2 learning content verified")
print(f"pages=7, slovak_examples={found}, text_chars={[len(text) for text in page_texts]}")
