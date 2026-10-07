import re
import sys
from pathlib import Path

import pdfplumber
from pypdf import PdfReader


path = Path(sys.argv[1]).resolve()
expected_name = "Slovak_A2_Tema_8_2_Emocii_nedorazumenie_i_podderzhka.pdf"
if path.name != expected_name:
    raise SystemExit(f"Wrong output filename: {path.name}")
if not path.is_file() or path.stat().st_size < 40_000:
    raise SystemExit("PDF missing or unexpectedly small")

reader = PdfReader(str(path))
if len(reader.pages) != 7:
    raise SystemExit(f"Expected 7 pages, found {len(reader.pages)}")
metadata_title = (reader.metadata.title or "").strip()
expected_metadata = "Slovak A2 - Тема 8.2 - Эмоции, недоразумение и поддержка"
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
    "A2 8.2", "Эмоции, недоразумение и поддержка", "Как назвать эмоцию",
    "Páčiť sa, Je mi ľúto и дательный", "Объясняем недоразумение и извиняемся",
    "Поддержка и мягкий совет", "Частые ошибки и упражнения",
    "Ответы и проверка мастерства", "Упражнение 1", "Упражнение 6", "Финальная проверка",
]
missing = [item for item in required if item not in full_text]
if missing:
    raise SystemExit(f"Missing required sections: {missing}")

examples = [
    "Som rád, že si prišiel", "Bola som sklamaná z výsledku", "Dnes sa cítim pokojne",
    "Po rozhovore sa cítim istejšia", "Mám radosť z tvojej správy", "Bojím sa jeho reakcie",
    "Teším sa na naše stretnutie", "Necítim sa dnes dobre", "Hnevám sa na Petra",
    "Asi som sa mýlil", "Teším sa z tvojho úspechu", "Páči sa mi tento nápad",
    "Páčia sa mi tvoje návrhy", "Páči sa ti táto hudba", "Jej sa páčia slovenské filmy",
    "Je mi ľúto, že sa to stalo", "To ma naozaj mrzí", "Chápem, že ťa to nahnevalo",
    "Neprišiel som, pretože som si pomýlil čas", "Pomýlil som si čas, preto som meškal",
    "Prepáč, že som ti nenapísal", "Nabudúce si čas hneď potvrdím",
    "Chápem, ako sa cítiš", "Som tu pre teba", "Môžem ti nejako pomôcť",
    "Mohla by si mu pokojne napísať", "Mal by si sa s ňou porozprávať",
    "Skús jej vysvetliť, čo sa stalo",
]
found = sum(example in full_text for example in examples)
if found < 24:
    raise SystemExit(f"Fewer than 24 expected Slovak examples were found: {found}")

if re.search(r"[\u4e00-\u9fff\u3040-\u30ff\u0600-\u06ff]", full_text):
    raise SystemExit("Unexpected script detected")
if re.search(r"[\u2010-\u2015]", full_text):
    raise SystemExit("Unexpected Unicode dash detected")

for forbidden in ["bolí ma", "bolieť +", "užívajte", "dávkovanie", "lekár", "lekáreň"]:
    if forbidden in full_text.lower():
        raise SystemExit(f"Content reserved for topic 8.3 or 8.4 leaked into the lesson: {forbidden}")

for bad in ["*Ja sa cítim nervózny dobre.", "*Ja páčim tento film.", "*Páči sa mi tie knihy.", "*Je ma ľúto.", "*Mal by si porozprávať s ňou."]:
    if bad not in full_text:
        raise SystemExit(f"Expected labeled error missing: {bad}")

print("A2 PDF 8.2 identity verified")
print("A2 PDF 8.2 structure and learning content verified")
print(f"pages=7, slovak_examples={found}, text_chars={[len(text) for text in page_texts]}")
