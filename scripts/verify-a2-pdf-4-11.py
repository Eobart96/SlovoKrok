import argparse
import hashlib
import re
from pathlib import Path

from PIL import Image, ImageStat
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
EXPECTED = ROOT / "output" / "pdf" / "A2" / "Module_04" / "Slovak_A2_Tema_4_11_Modalnye_glagoly_v_uslovnykh_prosbakh_i_sovetakh.pdf"
TITLE = "Slovak A2 - Тема 4.11 - Модальные глаголы в условных просьбах и советах"


def fail(message):
    raise SystemExit(f"ERROR: {message}")


parser = argparse.ArgumentParser()
parser.add_argument("--pdf", type=Path, default=EXPECTED)
parser.add_argument("--renders", type=Path)
args = parser.parse_args()
pdf = args.pdf.resolve()

if pdf != EXPECTED.resolve():
    fail(f"wrong artifact path: {pdf}")
if not pdf.exists() or pdf.stat().st_size < 80_000:
    fail("PDF is missing or suspiciously small")
reader = PdfReader(str(pdf))
if len(reader.pages) != 7:
    fail(f"expected 7 pages, got {len(reader.pages)}")
if (reader.metadata.title or "") != TITLE:
    fail(f"metadata title mismatch: {reader.metadata.title!r}")

pages = []
for i, page in enumerate(reader.pages, 1):
    width, height = float(page.mediabox.width), float(page.mediabox.height)
    if abs(width - 595.276) > 1.0 or abs(height - 841.89) > 1.0:
        fail(f"page {i} is not A4: {width} x {height}")
    content = page.extract_text() or ""
    if len(content.strip()) < 250:
        fail(f"page {i} has too little text")
    if f"стр. {i} / 7" not in content:
        fail(f"page {i} footer is missing")
    if i > 1 and "ТЕМА 4.11" not in content:
        fail(f"page {i} running header is missing")
    pages.append(content)

cover = pages[0]
for needle in ["A2", "ТЕМА 4.11", "Модальные глаголы", "условных просьбах", "и советах"]:
    if needle not in cover:
        fail(f"cover identity missing: {needle}")

whole = "\n".join(pages)
whole_flat = re.sub(r"\s+", " ", whole)
required = [
    "Три глагола - три намерения", "chcel by som", "mohol by som", "mohli by ste", "mal by som",
    "mal by si / ste", "Chcel by som si rezervovať izbu", "Mohol by som zaplatiť kartou",
    "Mohli by ste mi pomôcť", "Mali by ste navštíviť lekára", "Chcela by som zmeniť termín",
    "Chceli by sme objednať stôl", "Chcel by som sa opýtať", "Chceli by ste kávu",
    "Mohol by som tu počkať", "Mohli by ste hovoriť pomalšie", "Mal by som zavolať lekárovi",
    "Nemohli by ste to zopakovať", "Nemal by si si oddýchnuť", "Chcela by som odísť",
    "Mohla by som prísť", "Mala by som zavolať", "Mohli by sme sa stretnúť zajtra",
    "Telefonát do ambulancie", "Mal by si si oddýchnuť", "Готовые модели для реальных ситуаций",
    "Nemohli by ste skontrolovať číslo izby", "Mali by sme najprv skontrolovať údaje",
    "Mali by ste sa poradiť s lekárom", "Ошибки и практика", "Ответы и итог", "V hoteli", "Проверка освоения",
]
for needle in required:
    if needle not in whole_flat:
        fail(f"required content missing: {needle}")
if "Ошибки и практика" in pages[0] or any("Ответы и итог" in page for page in pages[:6]):
    fail("exercise/answer pagination is wrong")
if len(re.findall(r"\b(?:chcel\w*|mohol\w*|mohli|mal\w*|nemohol\w*|nemal\w*|by|som|si|sme|ste)\b", whole, flags=re.IGNORECASE)) < 140:
    fail("too few target Slovak forms and examples")
for bad in ["TODO", "TBD", "Lorem ipsum", "ТЕМА 4.10", "ТЕМА 4.12", "\ufffd"]:
    if bad in whole_flat:
        fail(f"forbidden text found: {bad}")
outside_exercises = re.sub(r"\s+", " ", "\n".join(pages[:5] + pages[6:]))
for bad in ["môžem by", "ne mohli"]:
    if bad in outside_exercises.lower():
        fail(f"unintended incorrect form found outside exercises: {bad}")
if re.search(r"[\u2010-\u2014]", whole):
    fail("Unicode dash found; use ASCII hyphen")

if args.renders:
    pngs = sorted(args.renders.glob("*.png"))
    if len(pngs) != 7:
        fail(f"expected 7 rendered pages, got {len(pngs)}")
    for render in pngs:
        if render.stat().st_size < 30_000:
            fail(f"render is suspiciously small: {render.name}")
        with Image.open(render) as image:
            if image.width < 1200 or image.height < 1700:
                fail(f"render resolution too low: {render.name} {image.size}")
            if ImageStat.Stat(image.convert("L")).stddev[0] < 8:
                fail(f"render appears blank: {render.name}")

print("A2 PDF 4.11 verified")
print(f"path={pdf}")
print(f"pages={len(reader.pages)}")
print(f"title={reader.metadata.title!a}")
print(f"sha256={hashlib.sha256(pdf.read_bytes()).hexdigest()}")
