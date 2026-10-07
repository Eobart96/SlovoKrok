import re
import sys
from pathlib import Path

import pdfplumber
from pypdf import PdfReader


path = Path(sys.argv[1]).resolve()
expected_name = "Slovak_A2_Tema_8_3_Samochuvstvie_i_razgovor_s_vrachom.pdf"
if path.name != expected_name:
    raise SystemExit(f"Wrong output filename: {path.name}")
if not path.is_file() or path.stat().st_size < 40_000:
    raise SystemExit("PDF missing or unexpectedly small")

reader = PdfReader(str(path))
if len(reader.pages) != 7:
    raise SystemExit(f"Expected 7 pages, found {len(reader.pages)}")
metadata_title = (reader.metadata.title or "").strip()
expected_metadata = "Slovak A2 - Тема 8.3 - Самочувствие и разговор с врачом"
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
    "A2 8.3", "Самочувствие и разговор с врачом", "Bolí ma...: что и у кого болит",
    "Je mi... и основные симптомы", "Когда началось и как менялось",
    "Понимаем врача: формальный императив", "Частые ошибки и упражнения",
    "Ответы и проверка мастерства", "Упражнение 1", "Упражнение 6", "Финальная проверка",
]
missing = [item for item in required if item not in full_text]
if missing:
    raise SystemExit(f"Missing required sections: {missing}")

examples = [
    "Bolí ma hlava", "Bolí ťa hrdlo", "Bolí ho brucho", "Bolí ju chrbát",
    "Bolia ma oči", "Bolia vás nohy", "Bolia ich kĺby", "Bolí ma pravé ucho",
    "Bolia ma oba členky", "Bolí ma to tu vpravo", "Bolesť ide do ľavej ruky",
    "Najviac ma to bolí pri pohybe", "Pri prehĺtaní ma bolí hrdlo", "Je mi zle",
    "Od rána mi je nevoľno", "Poobede mi bolo slabo", "Je vám chladno",
    "Dnes mi je trochu lepšie", "Mám suchý kašeľ", "Už tri dni mám nádchu",
    "Večer som mal zvýšenú teplotu", "Včera ma trápila zimnica",
    "Ráno sa mi zatočila hlava", "Začalo sa to včera večer",
    "Bolí ma to už tri dni", "Kašeľ mám od pondelka", "V noci sa to zhoršilo",
    "Sadnite si, prosím", "Otvorte ústa", "Zhlboka sa nadýchnite",
    "Pomaly vydýchnite", "Nehýbte sa", "Príďte na kontrolu o tri dni",
]
found = sum(example in full_text for example in examples)
if found < 28:
    raise SystemExit(f"Fewer than 28 expected Slovak examples were found: {found}")

if re.search(r"[\u4e00-\u9fff\u3040-\u30ff\u0600-\u06ff]", full_text):
    raise SystemExit("Unexpected script detected")
if re.search(r"[\u2010-\u2015]", full_text):
    raise SystemExit("Unexpected Unicode dash detected")

for forbidden in ["lekáreň", "dávkovanie", "tabletu každých", "zlomil", "zranil", "obväz"]:
    if forbidden in full_text.lower():
        raise SystemExit(f"Content reserved for topic 8.4 leaked into the lesson: {forbidden}")

for bad in ["*Mám bolí hlava.", "*Bolí mi hrdlo.", "*Bolí ma oči.", "*Som zle.", "*Otvoríte ústa!"]:
    if bad not in full_text:
        raise SystemExit(f"Expected labeled error missing: {bad}")

print("A2 PDF 8.3 identity verified")
print("A2 PDF 8.3 structure and learning content verified")
print(f"pages=7, slovak_examples={found}, text_chars={[len(text) for text in page_texts]}")
