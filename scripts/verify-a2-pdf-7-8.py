import re
import sys
from pathlib import Path

import pdfplumber
from pypdf import PdfReader


path = Path(sys.argv[1])
expected_name = "Slovak_A2_Tema_7_8_Moya_strana_i_Slovakiya_informatsiya_dlya_gostya.pdf"
expected_title = "Slovak A2 - Тема 7.8 - Моя страна и Словакия: информация для гостя"

if path.name != expected_name:
    raise SystemExit(f"Unexpected output filename: {path.name}")
if not path.is_file() or path.stat().st_size < 40_000:
    raise SystemExit("PDF missing or unexpectedly small")

reader = PdfReader(str(path))
if len(reader.pages) != 7:
    raise SystemExit(f"Expected 7 pages, found {len(reader.pages)}")
if reader.metadata.title != expected_title:
    raise SystemExit(f"Unexpected metadata title: {reader.metadata.title}")

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
    "A2 7.8", "Моя страна и Словакия: информация для гостя",
    "Не переводим всё: выбираем главное", "Даты, время и место",
    "Упрощаем с неопределёнными местоимениями", "Четыре источника и культурное уточнение",
    "Частые ошибки и упражнения", "Ответы и проверка мастерства",
    "Упражнение 1", "Упражнение 6", "Финальная проверка",
]
missing = [item for item in required if item not in full_text]
if missing:
    raise SystemExit(f"Missing required sections: {missing}")

slovak_examples = [
    "Podujatie organizuje mesto", "Je to večerný koncert", "Koná sa na Hlavnom námestí",
    "Začína sa v sobotu o šiestej", "Je to vhodné aj pre rodiny", "Treba si kúpiť lístok vopred",
    "Nie som si istý/istá, radšej to overíme", "Podujatie bude piateho mája",
    "Koncert je dvadsiateho prvého júna", "Trvá od pol desiatej do dvanástej",
    "Niekto z organizátorov vám poradí", "Môžete tam ochutnať niečo miestne",
    "Autobus zastavuje niekde pri stanici", "V horách sa počasie niekedy rýchlo mení",
    "Budete potrebovať nejakú nepremokavú bundu", "Program ponúka niekoľko krátkych prehliadok",
    "Do centra ide električka číslo štyri", "V Tatrách bude chladno",
    "V nedeľu je vstup do múzea zdarma", "Ak si nie ste istý, opýtajte sa",
    "V domácnosti sa hostia často vyzúvajú", "Čas obeda sa môže líšiť",
]
found = sum(example in full_text for example in slovak_examples)
if found < 18:
    raise SystemExit(f"Fewer than 18 expected Slovak examples were found: {found}")

for token in ["kto", "čo", "kde", "kedy", "niekto", "niečo", "niekde", "niekoľko"]:
    if token not in full_text.lower():
        raise SystemExit(f"Required mediation token missing: {token}")

if re.search(r"[\u4e00-\u9fff\u3040-\u30ff\u0600-\u06ff]", full_text):
    raise SystemExit("Unexpected non-Cyrillic/non-Latin script detected")

for forbidden in ["восемь краёв и природа", "instrumentál", "susedí s piatimi štátmi", "описать положение страны и города"]:
    if forbidden in full_text.lower():
        raise SystemExit(f"Core content from topic 7.7 leaked into 7.8: {forbidden}")

cover = page_texts[0]
if "A2 7.8" not in cover or "Моя страна и Словакия: информация для гостя" not in cover:
    raise SystemExit("Cover identity does not match requested topic")

print("A2 PDF 7.8 identity verified")
print("A2 PDF 7.8 structure verified")
print("A2 PDF 7.8 mediation content verified")
print(f"pages=7, slovak_examples={found}, text_chars={[len(text) for text in page_texts]}")
