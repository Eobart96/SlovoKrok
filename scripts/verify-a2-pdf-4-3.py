import argparse
import hashlib
import re
from pathlib import Path

from PIL import Image, ImageStat
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
EXPECTED = ROOT / "output" / "pdf" / "A2" / "Module_04" / "Slovak_A2_Tema_4_3_Vidovye_pary_s_suffiksami_i_izmeneniem_osnovy.pdf"
TITLE = "Slovak A2 - Тема 4.3 - Видовые пары с суффиксами и изменением основы"


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
    w, h = float(page.mediabox.width), float(page.mediabox.height)
    if abs(w - 595.276) > 1.0 or abs(h - 841.89) > 1.0:
        fail(f"page {i} is not A4: {w} x {h}")
    text = page.extract_text() or ""
    if len(text.strip()) < 250:
        fail(f"page {i} has too little text")
    if f"стр. {i} / 7" not in text:
        fail(f"page {i} footer is missing")
    if i > 1 and "ТЕМА 4.3" not in text:
        fail(f"page {i} running header is missing")
    pages.append(text)

cover = pages[0]
for needle in ["A2", "ТЕМА 4.3", "Видовые пары", "с суффиксами", "и изменением основы"]:
    if needle not in cover:
        fail(f"cover identity missing: {needle}")

whole = "\n".join(pages)
required = [
    "dávať -> dať", "brať -> vziať", "hovoriť -> povedať",
    "vracať sa -> vrátiť sa", "Надёжная словарная строка",
    "dávať / dať komu čo", "brať / vziať koho, čo",
    "hovoriť s kým o čom", "povedať komu čo",
    "vracať sa / vrátiť sa", "Четыре готовые карточки",
    "Ошибки и практика", "Ответы и итог", "hovoriť / povedať",
]
for needle in required:
    if needle not in whole:
        fail(f"required content missing: {needle}")
if "Ошибки и практика" in pages[0] or any("Ответы и итог" in p for p in pages[:6]):
    fail("exercise/answer pagination is wrong")
if len(re.findall(r"\b(?:som|sme|sa|si|mi)\b", whole, flags=re.IGNORECASE)) < 40:
    fail("too few connected Slovak examples")
for bad in ["TODO", "TBD", "Lorem ipsum", "ТЕМА 4.2", "ТЕМА 4.4", "\ufffd"]:
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
            if ImageStat.Stat(im.convert("L")).stddev[0] < 8:
                fail(f"render appears blank: {p.name}")

print("A2 PDF 4.3 verified")
print(f"path={pdf}")
print(f"pages={len(reader.pages)}")
print(f"title={reader.metadata.title}")
print(f"sha256={hashlib.sha256(pdf.read_bytes()).hexdigest()}")
