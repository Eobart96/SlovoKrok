import re
import sys
from pathlib import Path

import pdfplumber
from pypdf import PdfReader


path = Path(sys.argv[1]).resolve()
expected_name = "Slovak_A2_Tema_8_6_Integrirovannaya_zadacha_reshaem_problemu.pdf"
if path.name != expected_name:
    raise SystemExit(f"Wrong output filename: {path.name}")
if not path.is_file() or path.stat().st_size < 40_000:
    raise SystemExit("PDF missing or unexpectedly small")

reader = PdfReader(str(path))
if len(reader.pages) != 7:
    raise SystemExit(f"Expected 7 pages, found {len(reader.pages)}")
metadata_title = (reader.metadata.title or "").strip()
expected_metadata = "Slovak A2 - Тема 8.6 - Интегрированная задача: решаем проблему"
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
    "A2 8.6", "Интегрированная задача: решаем проблему", "Ситуация и исходное сообщение",
    "Уточняем детали", "Предлагаем и подтверждаем решение", "Передаём решение третьему лицу",
    "Частые ошибки и упражнения", "Ответы и итоговая цепочка", "Упражнение 1", "Упражнение 6",
    "Финальная проверка",
]
missing = [item for item in required if item not in full_text]
if missing:
    raise SystemExit(f"Missing required sections: {missing}")

examples = [
    "Technik príde medzi deviatou a jedenástou", "Musí byť majiteľ bytu osobne doma",
    "Môže technikovi otvoriť suseda", "Dostaneme správu, keď bude oprava hotová",
    "Rozumiem správne, že technik príde doobeda", "Je možné, aby technikovi otvorila suseda",
    "Musím byť osobne doma", "Mohli by ste mi potvrdiť čas návštevy",
    "Komu mám odovzdať kľúč", "Čo mám urobiť, ak sa termín zmení",
    "To mi vyhovuje", "Potrebujem si to ešte overiť", "Navrhujem, aby technikovi otvorila Marta",
    "Ak to nebude možné, odovzdám kľúč správcovi", "Dohodnime sa teda, že správca zavolá Marte",
    "Platí, že technik príde najskôr o desiatej", "Správca pošle Marte správu o návšteve",
    "Včera som zavolal správcovi", "Marta otvorí technikovi dvere",
    "Ak sa čas zmení, správca mi zavolá", "Keď opravu dokončia, pošlú správu",
    "Mohli by ste zavolať aj susede", "Dohodli sme sa, že technik príde do bytu 14",
    "Správca povedal, že technik príde medzi desiatou a jedenástou",
    "Správca požiadal Martu, aby bola v byte o desiatej",
    "Správca sľúbil, že zavolá desať minút vopred", "V ozname sa píše, že",
    "Najdôležitejšie je, že", "Nie je však jasné, či", "Chcel by som sa opýtať, či",
    "Požiadal ma, aby som", "Zatiaľ neviem, či",
]
found = sum(example in full_text for example in examples)
if found < 28:
    raise SystemExit(f"Fewer than 28 expected Slovak examples were found: {found}")

if re.search(r"[\u4e00-\u9fff\u3040-\u30ff\u0600-\u06ff]", full_text):
    raise SystemExit("Unexpected script detected")
if re.search(r"[\u2010-\u2015]", full_text):
    raise SystemExit("Unexpected Unicode dash detected")

for forbidden in ["8.5", "образ жизни и спорт", "8.7", "мой опыт, планы и самостоятельность"]:
    if forbidden in full_text.lower():
        raise SystemExit(f"Neighboring topic leaked into the lesson: {forbidden}")

for bad in ["*Rozumiem dobre, technik príde?", "*Otvorí technik suseda.", "*Dohodli sme, že...", "*Povedal, aby príde.", "*Požiadal, že otvorím."]:
    if bad not in full_text:
        raise SystemExit(f"Expected labeled error missing: {bad}")

print("A2 PDF 8.6 identity verified")
print("A2 PDF 8.6 integrated-task content verified")
print(f"pages=7, slovak_examples={found}, text_chars={[len(text) for text in page_texts]}")
