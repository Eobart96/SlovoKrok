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
    "A2 7.6", "История путешествия", "Каркас рассказа: фон и события",
    "Вид и неожиданное событие", "Возвратные глаголы в истории",
    "Последовательность и итог рассказа", "Частые ошибки и упражнения",
    "Ответы и проверка мастерства", "Упражнение 1", "Упражнение 6", "Финальная проверка",
]
missing = [item for item in required if item not in full_text]
if missing:
    raise SystemExit(f"Missing required sections: {missing}")

slovak_examples = [
    "Minulé leto sme cestovali po Slovensku", "Bývali sme v malom penzióne pri lese",
    "Celé dopoludnie sme chodili po meste", "Navštívili sme hrad a odfotili starý most",
    "Zrazu sa pokazil náš autobus", "Zavolali sme do penziónu a dočkali sme sa pomoci",
    "Nakoniec sme bezpečne dorazili do cieľa", "Bolo teplo a svietilo slnko",
    "Keď sme išli do Popradu, pokazil sa autobus", "Kým sme čakali, pili sme čaj",
    "Zrazu začalo silno pršať", "Zmeškali sme vlak, preto sme išli autobusom",
    "Našťastie nám pomohol miestny vodič", "Tešili sme sa na výlet do hôr",
    "Večer sme sa ubytovali v penzióne", "V centre sme sa na chvíľu stratili",
    "Rozhodli sme sa pokračovať pešo", "Po ceste sme si trochu oddýchli",
    "Všimli sme si nesprávne číslo autobusu", "Najprv sme si pozreli historické centrum",
    "Medzitým sa počasie zhoršilo", "Preto sme museli zmeniť plán",
    "Výlet sa nám veľmi páčil", "Poučili sme sa, že treba mať plán B",
]
found = sum(example in full_text for example in slovak_examples)
if found < 20:
    raise SystemExit(f"Fewer than 20 expected Slovak examples were found: {found}")

if re.search(r"[\u4e00-\u9fff\u3040-\u30ff\u0600-\u06ff]", full_text):
    raise SystemExit("Unexpected non-Cyrillic/non-Latin script detected")

for forbidden in ["susedí s rakúskom", "nachádza sa na západe", "najvyššie pohorie", "slovensko má osem krajov"]:
    if forbidden in full_text.lower():
        raise SystemExit(f"Content reserved for topic 7.7 leaked into the lesson: {forbidden}")

print("A2 PDF 7.6 structure verified")
print("A2 PDF 7.6 learning content verified")
print(f"pages=7, slovak_examples={found}, text_chars={[len(text) for text in page_texts]}")
