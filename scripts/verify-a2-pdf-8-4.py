import re
import sys
from pathlib import Path

import pdfplumber
from pypdf import PdfReader


path = Path(sys.argv[1]).resolve()
expected_name = "Slovak_A2_Tema_8_4_Apteka_travma_i_pervaya_pomoshch.pdf"
if path.name != expected_name:
    raise SystemExit(f"Wrong output filename: {path.name}")
if not path.is_file() or path.stat().st_size < 40_000:
    raise SystemExit("PDF missing or unexpectedly small")

reader = PdfReader(str(path))
if len(reader.pages) != 7:
    raise SystemExit(f"Expected 7 pages, found {len(reader.pages)}")
metadata_title = (reader.metadata.title or "").strip()
expected_metadata = "Slovak A2 - Тема 8.4 - Аптека, травма и первая помощь"
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
    "A2 8.4", "Аптека, травма и первая помощь", "В аптеке: вежливая просьба",
    "Как понять дозировку и применение", "Объясняем травму: zraniť si / zlomiť si",
    "Первая помощь и две конструкции с D + A", "Частые ошибки и упражнения",
    "Ответы и проверка мастерства", "Упражнение 1", "Упражнение 6", "Финальная проверка",
]
missing = [item for item in required if item not in full_text]
if missing:
    raise SystemExit(f"Missing required sections: {missing}")

examples = [
    "Mohli by ste mi odporučiť", "Prosil by som si jedno balenie náplastí",
    "Prosila by som si dezinfekciu", "Potrebovala by som elastický obväz",
    "Máte niečo na štípance", "Je tento prípravok bez receptu",
    "Ako často to mám užívať", "Koľko tabliet mám užiť",
    "Mám to užívať pred jedlom alebo po jedle", "Ako dlho to mám používať",
    "Mám to zapiť vodou", "Môžem to používať spolu s iným liekom",
    "Zranil som si zápästie", "Zlomila si ruku", "Porezal som si prst",
    "Popálila som si dlaň", "Vyvrtol si členok", "Udrel som si koleno",
    "Spadol som z bicykla", "Stalo sa to pred hodinou", "Bolí ma pravý členok",
    "Prst je porezaný", "Ruka je opuchnutá", "Koleno je poranené",
    "Zavolajte 155 alebo 112", "Prineste lekárničku", "Nehýbte sa",
    "Pritlačte čistú látku na ranu", "Počkajte na pomoc", "Prineste mi lekárničku",
    "Priniesol som jej čistý obväz", "Zobral som mu tašku",
]
found = sum(example in full_text for example in examples)
if found < 28:
    raise SystemExit(f"Fewer than 28 expected Slovak examples were found: {found}")

if re.search(r"[\u4e00-\u9fff\u3040-\u30ff\u0600-\u06ff]", full_text):
    raise SystemExit("Unexpected script detected")
if re.search(r"[\u2010-\u2015]", full_text):
    raise SystemExit("Unexpected Unicode dash detected")

for forbidden in ["8.3", "Самочувствие и разговор с врачом", "образ жизни и спорт", "8.5"]:
    if forbidden in full_text.lower():
        raise SystemExit(f"Neighboring topic leaked into the lesson: {forbidden}")

for bad in ["*Ja by chcem obväz.", "*jedna balenie", "*Zranil som ruku.", "*Ruka je opuchnutý.", "*Prineste ja lekárničku."]:
    if bad not in full_text:
        raise SystemExit(f"Expected labeled error missing: {bad}")

print("A2 PDF 8.4 identity verified")
print("A2 PDF 8.4 structure and learning content verified")
print(f"pages=7, slovak_examples={found}, text_chars={[len(text) for text in page_texts]}")
