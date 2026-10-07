import re
import sys
from pathlib import Path

import pdfplumber
from pypdf import PdfReader


path = Path(sys.argv[1]).resolve()
expected_name = "Slovak_A2_Tema_8_7_Itog_A2_moy_opyt_plany_i_samostoyatelnost.pdf"
if path.name != expected_name:
    raise SystemExit(f"Wrong output filename: {path.name}")
if not path.is_file() or path.stat().st_size < 45_000:
    raise SystemExit("PDF missing or unexpectedly small")

reader = PdfReader(str(path))
if len(reader.pages) != 8:
    raise SystemExit(f"Expected 8 pages, found {len(reader.pages)}")
metadata_title = (reader.metadata.title or "").strip()
expected_metadata = "Slovak A2 - Тема 8.7 - Итог A2: мой опыт, планы и самостоятельность"
if metadata_title != expected_metadata:
    raise SystemExit(f"Wrong metadata title: {metadata_title!r}")

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
    "A2 8.7", "Итог A2: мой опыт, планы и самостоятельность", "Четыре независимые части",
    "Задание 1. Чтение", "Задание 2. Короткое аудирование", "Задание 3. Устный рассказ",
    "Задание 4. Письмо организатору", "Задание 5. Решаем проблему по телефону",
    "Задание 6. Передаём изменения другу", "Ответы к рецепции", "Скрипт аудирования",
    "Модели и итоговая оценка", "Финальная проверка",
]
missing = [item for item in required if item not in full_text]
if missing:
    raise SystemExit(f"Missing required sections: {missing}")

examples = [
    "Zúčastnil som sa", "Teraz dokážem", "Najťažšie je pre mňa", "Počas víkendu budem",
    "Do troch mesiacov chcem", "Ak niečomu nerozumiem", "Rád by som potvrdil",
    "Rada by som potvrdila", "Prídem približne o", "Chcel by som sa opýtať",
    "Chcela by som sa opýtať", "Ďakujem za informáciu a teším sa na program",
    "Volám kvôli oneskoreniu vlaku", "Prídem asi o dvadsať minút neskôr",
    "Rozumiem správne, že mám ísť priamo na internát", "Mohli by ste mi zopakovať adresu",
    "Dohodnime sa teda, že", "Ďakujem za pomoc, dovidenia", "V správe sa píše, že",
    "Pôvodný čas sa zmenil", "Namiesto námestia pôjdeme do knižnice", "Treba si priniesť",
    "Najneskôr do piatku treba oznámiť", "Rozumiem zmene a potvrdzujem účasť",
    "VÍKENDOVÝ PROGRAM SLOVENČINA V PRAXI", "Účasť potvrďte do 10. októbra",
    "Pre opravu železničnej stanice", "na autobusovú stanicu k nástupišťu číslo šesť",
    "Prineste si občiansky preukaz alebo pas", "Ak budete meškať, zavolajte mi",
]
found = sum(example in full_text for example in examples)
if found < 26:
    raise SystemExit(f"Fewer than 26 expected Slovak examples were found: {found}")

if re.search(r"[\u4e00-\u9fff\u3040-\u30ff\u0600-\u06ff]", full_text):
    raise SystemExit("Unexpected script detected")
if re.search(r"[\u2010-\u2015]", full_text):
    raise SystemExit("Unexpected Unicode dash detected")

for forbidden in ["8.6", "интегрированная задача: решаем проблему", "8.8"]:
    if forbidden in full_text.lower():
        raise SystemExit(f"Neighboring topic leaked into the lesson: {forbidden}")

for page_no in range(1, 9):
    if f"стр. {page_no} / 8" not in page_texts[page_no - 1]:
        raise SystemExit(f"Missing page number on page {page_no}")

print("A2 PDF 8.7 identity verified")
print("A2 PDF 8.7 final-assessment content verified")
print(f"pages=8, slovak_examples={found}, text_chars={[len(text) for text in page_texts]}")
