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
    "Билет, маршрут и пересадка", "Как выбрать маршрут", "Kde, kam, odkiaľ",
    "Покупаем билет и говорим о времени", "Объявление и пересадка",
    "Частые ошибки и упражнения", "Ответы и проверка мастерства",
    "Упражнение 1", "Упражнение 6", "Финальная проверка",
]
missing = [item for item in required if item not in full_text]
if missing:
    raise SystemExit(f"Missing required sections: {missing}")

slovak_examples = [
    "Tento spoj ide do Žiliny", "Odchod je o 8.25", "Je to priamy spoj bez prestupu",
    "V Trnave máme jeden prestup", "Vlak odchádza z tretieho nástupišťa",
    "Prípojný vlak čaká desať minút", "Vlak má pätnásť minút meškanie",
    "Ideme vlakom do Košíc", "Nastúpime do autobusu", "Vystúpte na hlavnej stanici",
    "V Žiline prestúpime na rýchlik", "Cestujem z Bratislavy", "Idem do Košíc cez Žilinu",
    "Prestupujem v Žiline", "Idem na druhé nástupište", "Prosím si jeden lístok",
    "Prosím si spiatočný lístok", "Chcem jednosmerný lístok", "Kedy odchádza najbližší vlak",
    "Kde musím prestúpiť", "Z ktorého nástupišťa vlak odchádza",
    "Vlak odchádza o 8.25", "Autobus príde za desať minút", "Cesta trvá dve hodiny",
    "Vlak mešká dvadsať minút", "Rýchlik číslo 603 do Košíc", "prípojný vlak počká",
]
found = sum(example in full_text for example in slovak_examples)
if found < 22:
    raise SystemExit(f"Fewer than 22 expected Slovak examples were found: {found}")

if re.search(r"[\u4e00-\u9fff\u3040-\u30ff\u0600-\u06ff]", full_text):
    raise SystemExit("Unexpected non-Cyrillic/non-Latin script detected")

for forbidden in ["hotelová izba", "ubytovanie je lacnejšie", "dúfam, že cesta", "keby sme rezervovali"]:
    if forbidden in full_text.lower():
        raise SystemExit(f"Content reserved for topic 7.5 leaked into the lesson: {forbidden}")

print("A2 PDF 7.4 structure verified")
print("A2 PDF 7.4 learning content verified")
print(f"pages=7, slovak_examples={found}, text_chars={[len(text) for text in page_texts]}")
