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
    "A2 7.7", "География, регионы и погода Словакии", "Где находится и с чем граничит",
    "Восемь краёв и природа", "Погода: безличные конструкции",
    "Описываем Словакию и сравниваем", "Частые ошибки и упражнения",
    "Ответы и проверка мастерства", "Упражнение 1", "Упражнение 6", "Финальная проверка",
]
missing = [item for item in required if item not in full_text]
if missing:
    raise SystemExit(f"Missing required sections: {missing}")

slovak_examples = [
    "Slovensko leží v strednej Európe", "Bratislava sa nachádza na juhozápade krajiny",
    "Vysoké Tatry sa nachádzajú na severe", "Slovensko susedí s piatimi štátmi",
    "Tento syr pochádza zo severného Slovenska", "Dunaj preteká cez Bratislavu",
    "Bratislavský kraj susedí s Rakúskom", "Slovensko susedí s Českom na západe",
    "Na severe Slovensko susedí s Poľskom", "Na východe susedí s Ukrajinou",
    "Na juhu susedí s Maďarskom", "Bratislava leží pri Dunaji",
    "Cez región preteká rieka Váh", "Na severe hraničí s Poľskom",
    "Na východe hraničí s Ukrajinou", "Na juhu sa rozprestiera Podunajská nížina",
    "V horských oblastiach je veľa lesov", "Dnes je slnečno a teplo",
    "Ráno bude zamračené a hmlisto", "V horách bude v noci snežiť",
    "Teplota vystúpi na dvadsať stupňov", "Na juhu je teplejšie ako na severe",
    "V horách býva chladnejšie", "Vo vyšších polohách sneží častejšie",
]
found = sum(example in full_text for example in slovak_examples)
if found < 20:
    raise SystemExit(f"Fewer than 20 expected Slovak examples were found: {found}")

if re.search(r"[\u4e00-\u9fff\u3040-\u30ff\u0600-\u06ff]", full_text):
    raise SystemExit("Unexpected non-Cyrillic/non-Latin script detected")

for forbidden in ["podľa mapy", "z programu podujatia", "turistovi vysvetlite", "kultúrny text hovorí"]:
    if forbidden in full_text.lower():
        raise SystemExit(f"Content reserved for topic 7.8 leaked into the lesson: {forbidden}")

print("A2 PDF 7.7 structure verified")
print("A2 PDF 7.7 learning content verified")
print(f"pages=7, slovak_examples={found}, text_chars={[len(text) for text in page_texts]}")
