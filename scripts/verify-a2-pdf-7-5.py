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
    "Бронирование и план поездки", "Сравниваем жильё и транспорт", "Условия и бронирование",
    "Предложение: кондиционал и будущее", "Согласовываем общий план",
    "Частые ошибки и упражнения", "Ответы и проверка мастерства",
    "Упражнение 1", "Упражнение 6", "Финальная проверка",
]
missing = [item for item in required if item not in full_text]
if missing:
    raise SystemExit(f"Missing required sections: {missing}")

slovak_examples = [
    "Penzión je lacnejší ako hotel", "Vlak je pohodlnejší ako autobus",
    "Lietadlo je rýchlejšie, ale drahšie", "Apartmán je bližšie k centru",
    "Hotel má lepšie raňajky", "Najvýhodnejší je nočný vlak",
    "Máte voľnú dvojlôžkovú izbu", "Chceli by sme zostať od 12. do 15. augusta",
    "Koľko stojí izba na noc", "Sú raňajky v cene", "Je možné rezerváciu bezplatne zrušiť",
    "Prosím, potvrďte nám rezerváciu e-mailom", "Mohli by sme ísť vlakom",
    "Radšej by som býval v penzióne", "Bolo by lepšie zostať tri noci",
    "Keby sme išli ráno, prišli by sme pred obedom", "V sobotu budeme cestovať do Tatier",
    "Večer sa ubytujeme", "Dúfam, že bude izba voľná", "Verím, že nám termín potvrdia",
    "Súhlasím, tento variant mi vyhovuje", "Navrhujem lacnejší penzión pri stanici",
    "Dohodnuté, dnes rezervujem izbu", "Dúfam, že ešte budú voľné miesta",
]
found = sum(example in full_text for example in slovak_examples)
if found < 20:
    raise SystemExit(f"Fewer than 20 expected Slovak examples were found: {found}")

if re.search(r"[\u4e00-\u9fff\u3040-\u30ff\u0600-\u06ff]", full_text):
    raise SystemExit("Unexpected non-Cyrillic/non-Latin script detected")

for forbidden in ["nečakane sa pokazilo", "keď sme sa vracali", "nakoniec sme dorazili", "príhoda z cesty"]:
    if forbidden in full_text.lower():
        raise SystemExit(f"Content reserved for topic 7.6 leaked into the lesson: {forbidden}")

print("A2 PDF 7.5 structure verified")
print("A2 PDF 7.5 learning content verified")
print(f"pages=7, slovak_examples={found}, text_chars={[len(text) for text in page_texts]}")
