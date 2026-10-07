import re
import sys
from pathlib import Path

import pdfplumber
from pypdf import PdfReader


path = Path(sys.argv[1]).resolve()
expected_name = "Slovak_A2_Tema_8_1_Semya_druzya_vneshnost_i_harakter.pdf"
if path.name != expected_name:
    raise SystemExit(f"Wrong output filename: {path.name}")
if not path.is_file() or path.stat().st_size < 40_000:
    raise SystemExit("PDF missing or unexpectedly small")

reader = PdfReader(str(path))
if len(reader.pages) != 7:
    raise SystemExit(f"Expected 7 pages, found {len(reader.pages)}")
metadata_title = (reader.metadata.title or "").strip()
expected_metadata = "Slovak A2 - Тема 8.1 - Семья, друзья, внешность и характер"
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
    "A2 8.1", "Семья, друзья, внешность и характер",
    "Родство и винительный множественного числа", "Внешность и характер",
    "Svoj, jeho, jej и притяжательные прилагательные", "Связный рассказ и банк живых фраз",
    "Частые ошибки и упражнения", "Ответы и проверка мастерства",
    "Упражнение 1", "Упражнение 6", "Финальная проверка",
]
missing = [item for item in required if item not in full_text]
if missing:
    raise SystemExit(f"Missing required sections: {missing}")

examples = [
    "navštevujem starých rodičov", "Majú dvoch vnukov", "stretávam bratrancov a sesternice",
    "Pozývame svokrovcov", "poznám svojich švagrov", "majú radi zaťov aj nevesty",
    "Mám dvoch nevlastných bratov", "pozvali svojich partnerov", "vidím bratov, synov, kamarátov",
    "poznám malé deti", "má modré oči a krátke vlasy", "Môj brat je vysoký a štíhly",
    "Má krátke tmavé vlasy", "Náš strýko nosí okuliare", "Je tichá, ale veľmi priateľská",
    "Môžem sa naňho spoľahnúť", "Eva je mladšia a otvorenejšia ako Jana",
    "Dcéra sa podobá na svoju mamu", "S bratom si rozumiem lepšie ako so sesternicou",
    "Anna má rada svojho brata", "Peter predstavil svoju sestru",
    "Deti navštívili svojich starých rodičov", "Poznám Petra a jeho sestru",
    "Otcov brat je môj strýko", "Matkina sestra býva v Nitre",
    "Poznáme sa už desať rokov", "Máme veľa spoločného", "Dobre sa dopĺňame",
]
found = sum(example in full_text for example in examples)
if found < 24:
    raise SystemExit(f"Fewer than 24 expected Slovak examples were found: {found}")

if re.search(r"[\u4e00-\u9fff\u3040-\u30ff\u0600-\u06ff]", full_text):
    raise SystemExit("Unexpected script detected")

for forbidden in ["cítiť sa", "je mi ľúto", "mal by som", "nedorozumenie", "ospravedlniť"]:
    if forbidden in full_text.lower():
        raise SystemExit(f"Content reserved for topic 8.2 leaked into the lesson: {forbidden}")

for bad in ["*Vidím moji kamaráti.", "*Anna má rada jej brata.", "*Poznám Peterovu sestru.", "*Má hnedé vlasov.", "*Je viac mladá ako ja."]:
    if bad not in full_text:
        raise SystemExit(f"Expected labeled error missing: {bad}")

print("A2 PDF 8.1 identity verified")
print("A2 PDF 8.1 structure and learning content verified")
print(f"pages=7, slovak_examples={found}, text_chars={[len(text) for text in page_texts]}")
