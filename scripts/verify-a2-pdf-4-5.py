import argparse
import hashlib
import re
from pathlib import Path

from PIL import Image, ImageStat
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
EXPECTED = ROOT / "output" / "pdf" / "A2" / "Module_04" / "Slovak_A2_Tema_4_5_Analiticheskoe_budushchee_nesovershennyh_glagolov.pdf"
TITLE = "Slovak A2 - Тема 4.5 - Аналитическое будущее несовершенных глаголов"


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
    if i > 1 and "ТЕМА 4.5" not in content:
        fail(f"page {i} running header is missing")
    pages.append(content)

cover = pages[0]
for needle in ["A2", "ТЕМА 4.5", "Аналитическое будущее", "несовершенных глаголов"]:
    if needle not in cover:
        fail(f"cover identity missing: {needle}")

whole = "\n".join(pages)
required = [
    "Формула: budem + infinitív",
    "Отрицание и вопрос",
    "sa/si и порядок слов",
    "Длительность и повторяемость",
    "Môj budúci týždeň",
    "Budem pracovať doma",
    "Zajtra nebudem pracovať",
    "Čo budete zajtra robiť",
    "Zajtra sa budem učiť doma",
    "Dve hodiny budem písať správu",
    "Každý utorok budeme trénovať",
    "Zajtra bude pršať",
    "Budeme musieť čakať",
    "Ошибки и практика",
    "Ответы и итог",
    "Проверка освоения",
    "теме 4.7",
    "темой 4.6",
]
for needle in required:
    if needle not in whole:
        fail(f"required content missing: {needle}")
if "Ошибки и практика" in pages[0] or any("Ответы и итог" in page for page in pages[:6]):
    fail("exercise/answer pagination is wrong")
if len(re.findall(r"\b(?:budem|budeš|bude|budeme|budete|budú|nebudem|sa|si)\b", whole, flags=re.IGNORECASE)) < 75:
    fail("too few target Slovak forms and examples")
for bad in ["TODO", "TBD", "Lorem ipsum", "ТЕМА 4.4", "ТЕМА 4.6", "ТЕМА 4.7", "\ufffd"]:
    if bad in whole:
        fail(f"forbidden text found: {bad}")
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

print("A2 PDF 4.5 verified")
print(f"path={pdf}")
print(f"pages={len(reader.pages)}")
print(f"title={reader.metadata.title}")
print(f"sha256={hashlib.sha256(pdf.read_bytes()).hexdigest()}")
