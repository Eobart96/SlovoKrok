import argparse
import hashlib
import re
from pathlib import Path

from PIL import Image, ImageStat
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
EXPECTED = ROOT / "output" / "pdf" / "A2" / "Module_04" / "Slovak_A2_Tema_4_1_Vid_v_svyaznom_rasskaze.pdf"
TITLE = "Slovak A2 - Тема 4.1 - Вид в связном рассказе: фон и цепочка событий"


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
    w = float(page.mediabox.width)
    h = float(page.mediabox.height)
    if abs(w - 595.276) > 1.0 or abs(h - 841.89) > 1.0:
        fail(f"page {i} is not A4: {w} x {h}")
    text = page.extract_text() or ""
    if len(text.strip()) < 250:
        fail(f"page {i} has too little text")
    if f"стр. {i} / 7" not in text:
        fail(f"page {i} footer is missing")
    pages.append(text)

cover = pages[0]
for needle in ["A2", "ТЕМА 4.1", "Вид в связном рассказе:", "фон и цепочка событий"]:
    if needle not in cover:
        fail(f"cover identity missing: {needle}")

whole = "\n".join(pages)
required = [
    "Три роли глагола в рассказе", "Одновременность и прерывание",
    "Как строится цепочка событий", "Образец связного рассказа",
    "Kým som varil večeru, deti sa hrali.",
    "Keď som varil večeru, zazvonil telefón.",
    "Keď som uvaril večeru, zavolal som deti.",
    "najprv", "potom", "keď", "kým", "nakoniec",
    "Sobotné raňajky", "Практика", "Ответы и итог", "Nečakané ráno",
]
for needle in required:
    if needle not in whole:
        fail(f"required content missing: {needle}")

if "Практика" in pages[0] or any("Ответы и итог" in p for p in pages[:6]):
    fail("exercise/answer pagination is wrong")
if len(re.findall(r"\b(?:som|sme|sa)\b", whole, flags=re.IGNORECASE)) < 35:
    fail("too few connected Slovak examples")

for bad in ["TODO", "TBD", "Lorem ipsum", "ТЕМА 4.12", "ТЕМА 5.1", "\ufffd"]:
    if bad in whole:
        fail(f"forbidden text found: {bad}")
if re.search(r"[\u2010-\u2014]", whole):
    fail("Unicode dash found; use ASCII hyphen")

if args.renders:
    pngs = sorted(args.renders.glob("*.png"))
    if len(pngs) != 7:
        fail(f"expected 7 rendered pages, got {len(pngs)}")
    for p in pngs:
        if p.stat().st_size < 30_000:
            fail(f"render is suspiciously small: {p.name}")
        with Image.open(p) as im:
            if im.width < 1200 or im.height < 1700:
                fail(f"render resolution too low: {p.name} {im.size}")
            stat = ImageStat.Stat(im.convert("L"))
            if stat.stddev[0] < 8:
                fail(f"render appears blank: {p.name}")

digest = hashlib.sha256(pdf.read_bytes()).hexdigest()
print("A2 PDF 4.1 verified")
print(f"path={pdf}")
print(f"pages={len(reader.pages)}")
print(f"title={reader.metadata.title}")
print(f"sha256={digest}")
