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
    "Профессия, обязанности и опыт",
    "Нынешняя работа и обязанности",
    "Прошлый опыт и вид глагола",
    "Навыки: vedieť, poznať, môcť",
    "Банк фраз и модель рассказа",
    "Частые ошибки и упражнения",
    "Ответы и проверка мастерства",
    "Упражнение 1",
    "Упражнение 6",
    "Финальная проверка",
]
missing = [item for item in required if item not in full_text]
if missing:
    raise SystemExit(f"Missing required sections: {missing}")

slovak_examples = [
    "Pracujem ako účtovníčka", "Pracujem v malej firme", "Pracujem v oblasti IT",
    "Mám na starosti faktúry", "Zodpovedám za tím", "Starám sa o zákazníkov",
    "Venujem sa marketingu", "Komunikujem s dodávateľmi", "Pomáham novým kolegom",
    "Každý deň som kontroloval objednávky", "Včera som skontroloval veľkú objednávku",
    "Tri roky som pracovala v banke", "Zorganizovala som odbornú konferenciu",
    "Viem pracovať s Excelom", "Poznám tento program", "Môžem pracovať samostatne",
    "Mám skúsenosti s predajom", "Dobre ovládam slovenčinu",
    "Dokážem rýchlo vyriešiť problém", "Som zdravotná sestra",
    "Pracujem ako kuchár v hoteli", "Často pripravujem prezentácie",
    "Predtým som pracoval v obchode", "Viem používať účtovný program",
    "Táto práca je pokojnejšia ako predchádzajúca",
]
found = sum(example in full_text for example in slovak_examples)
if found < 20:
    raise SystemExit(f"Fewer than 20 expected Slovak examples were found: {found}")

if re.search(r"[\u4e00-\u9fff\u3040-\u30ff\u0600-\u06ff]", full_text):
    raise SystemExit("Unexpected non-Cyrillic/non-Latin script detected")

if "PDF 7.2" in full_text or "заполнить анкету" in full_text:
    raise SystemExit("Content reserved for the next topic leaked into the lesson")

print("A2 PDF 7.1 structure verified")
print("A2 PDF 7.1 learning content verified")
print(f"pages=7, slovak_examples={found}, text_chars={[len(text) for text in page_texts]}")
