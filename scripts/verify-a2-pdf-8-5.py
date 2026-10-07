import re
import sys
from pathlib import Path

import pdfplumber
from pypdf import PdfReader


path = Path(sys.argv[1]).resolve()
expected_name = "Slovak_A2_Tema_8_5_Obraz_zhizni_i_sport.pdf"
if path.name != expected_name:
    raise SystemExit(f"Wrong output filename: {path.name}")
if not path.is_file() or path.stat().st_size < 40_000:
    raise SystemExit("PDF missing or unexpectedly small")

reader = PdfReader(str(path))
if len(reader.pages) != 7:
    raise SystemExit(f"Expected 7 pages, found {len(reader.pages)}")
metadata_title = (reader.metadata.title or "").strip()
expected_metadata = "Slovak A2 - Тема 8.5 - Образ жизни и спорт"
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
    "A2 8.5", "Образ жизни и спорт", "Называем активности", "Сравниваем через наречия",
    "Привычка и один результат: вид", "Совет и реальный план", "Частые ошибки и упражнения",
    "Ответы и проверка мастерства", "Упражнение 1", "Упражнение 6", "Финальная проверка",
]
missing = [item for item in required if item not in full_text]
if missing:
    raise SystemExit(f"Missing required sections: {missing}")

examples = [
    "Pravidelné cvičenie mi pomáha", "Počas behania sa rýchlo unavím",
    "Na plávanie chodím dvakrát týždenne", "Posilňovanie striedam s chôdzou",
    "Zdravé stravovanie nie je len diéta", "Rýchla chôdza je môj obľúbený pohyb",
    "Jazda na bicykli ma baví", "Dobrý spánok je pre mňa dôležitý",
    "Večer mám čas na cvičenie", "Počas plávania pokojne dýcham",
    "Pred spaním nepoužívam telefón", "Po behaní sa vždy ponaťahujem",
    "Teraz cvičím pravidelnejšie ako vlani", "Pri plávaní dýcham pokojnejšie než pri behu",
    "Na bicykli sa pohybujem rýchlejšie ako pešo", "Po večernej prechádzke zaspím ľahšie",
    "Cez víkend spím dlhšie", "Tento mesiac sedím menej a chodím viac",
    "Každý deň cvičím", "Dnes si zacvičím dvadsať minút", "Po práci sa prejdem",
    "V sobotu si zaplávam", "Po tréningu vypijem pohár vody",
    "Budúci týždeň budem cvičiť doma", "Zajtra si zacvičím po práci",
    "Mal by som sa viac hýbať", "Mala by som chodiť spať skôr",
    "Mali by sme častejšie chodiť pešo", "Nemal by si trénovať bez oddychu",
    "Ak bude pršať, budem cvičiť doma", "Keď prídem z práce, pôjdem sa prejsť",
    "Keď mám voľno, chodím plávať",
]
found = sum(example in full_text for example in examples)
if found < 28:
    raise SystemExit(f"Fewer than 28 expected Slovak examples were found: {found}")

if re.search(r"[\u4e00-\u9fff\u3040-\u30ff\u0600-\u06ff]", full_text):
    raise SystemExit("Unexpected script detected")
if re.search(r"[\u2010-\u2015]", full_text):
    raise SystemExit("Unexpected Unicode dash detected")

for forbidden in ["8.4", "аптека, травма и первая помощь", "8.6", "интегрированная задача"]:
    if forbidden in full_text.lower():
        raise SystemExit(f"Neighboring topic leaked into the lesson: {forbidden}")

for bad in ["*rýchlejší bežím", "*viac lepšie", "*mal som by cvičiť", "*mal by som viac sa hýbať", "*ak pršalo zajtra"]:
    if bad not in full_text:
        raise SystemExit(f"Expected labeled error missing: {bad}")

print("A2 PDF 8.5 identity verified")
print("A2 PDF 8.5 structure and learning content verified")
print(f"pages=7, slovak_examples={found}, text_chars={[len(text) for text in page_texts]}")
