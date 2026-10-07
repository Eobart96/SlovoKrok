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
if abs(float(reader.pages[0].mediabox.width) - 595.28) > 2:
    raise SystemExit("First page is not A4 width")

with pdfplumber.open(path) as pdf:
    page_texts = [(page.extract_text() or "").strip() for page in pdf.pages]

if any(len(text) < 250 for text in page_texts):
    raise SystemExit("At least one page has too little extractable text")

full_text = "\n".join(page_texts)
required = [
    "Что нужно уметь",
    "Быстрая карта готовности",
    "Падежи и согласование",
    "Глаголы: время, вид и намерение",
    "Общение: от фразы к задаче",
    "Диагностические упражнения",
    "Ответы и личный маршрут",
    "Упражнение 1",
    "Упражнение 6",
    "Финальная проверка мастерства",
]
missing = [item for item in required if item not in full_text]
if missing:
    raise SystemExit(f"Missing required sections: {missing}")

slovak_examples = [
    "Volám sa Ari", "Kde bývate", "Môj byt je malý", "Včera som pracoval",
    "Zajtra budem študovať", "Mohli by ste mi pomôcť", "Stretneme sa o šiestej",
    "Peter povedal", "Nový kolega pracuje", "Hľadám nového kolegu",
    "Píšem novej kolegyni", "Hovoríme o novej práci", "Idem s dobrým kamarátom",
    "Vraciame sa z veľkého mesta", "Každý deň čítam", "Knihu som už prečítal",
    "Večer budem písať", "Večer napíšem", "Mohol by som dostať účet",
    "Môžete to povedať jednoduchšie", "Meškám, pretože autobus neprišiel",
    "To mi vyhovuje", "Anna povedala", "Bývame v malom meste",
]
if sum(example in full_text for example in slovak_examples) < 20:
    raise SystemExit("Fewer than 20 expected Slovak examples were found")

print("A2 PDF structure verified")
print("A2 PDF learning content verified")
