import argparse
import hashlib
import re
from pathlib import Path

from PIL import Image, ImageStat
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
EXPECTED = ROOT / "output" / "pdf" / "A2" / "Module_04" / "Slovak_A2_Tema_4_12_Otglagolnye_sushchestvitelnye_i_passivnye_prichastiya.pdf"
TITLE = "Slovak A2 - Тема 4.12 - Отглагольные существительные и пассивные причастия"


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
    if i > 1 and "ТЕМА 4.12" not in content:
        fail(f"page {i} running header is missing")
    pages.append(content)

cover = pages[0]
for needle in ["A2", "ТЕМА 4.12", "Отглагольные", "существительные", "пассивные причастия"]:
    if needle not in cover:
        fail(f"cover identity missing: {needle}")

whole = "\n".join(pages)
whole_flat = re.sub(r"\s+", " ", whole)
required = [
    "Название действия: čo?", "plávanie", "liečenie", "vyšetrenie", "otvorenie", "vyplnenie",
    "Zákaz fajčenia", "Miesto na parkovanie", "Po vyšetrení", "Počas liečenia",
    "Результат или состояние: aký?", "zatvorený obchod", "zatvorená lekáreň", "zatvorené dvere",
    "zlomený prst", "zlomená ruka", "zlomené rebro", "vyplnený formulár", "podpísaná zmluva",
    "zaplatený", "poškodený", "umytý", "Процесс или готовый результат", "zatvorenie obchodu",
    "Lekáreň je zatvorená", "Otvorenie je naplánované", "Parkovanie je povolené",
    "Pred vyšetrením nejedzte", "Liečenie trvá približne dva týždne",
    "Čakanie trvá desať minút", "Upratovanie izby je v cene", "Objednanie na vyšetrenie je možné telefonicky", "Izba je rezervovaná",
    "Dvere sú zamknuté", "Stretnutie je zrušené", "Ошибки и практика", "Ответы и итог",
    "Oznam v hoteli", "Проверка освоения",
]
for needle in required:
    if needle not in whole_flat:
        fail(f"required content missing: {needle}")
if "Ошибки и практика" in pages[0] or any("Ответы и итог" in page for page in pages[:6]):
    fail("exercise/answer pagination is wrong")
if len(re.findall(r"\b\w+(?:anie|enie|tie|aný|aná|ané|ení|ený|ená|ené|tý|tá|té)\b", whole, flags=re.IGNORECASE)) < 55:
    fail("too few target Slovak forms and examples")
for bad in ["TODO", "TBD", "Lorem ipsum", "ТЕМА 4.11", "ТЕМА 5.1", "\ufffd"]:
    if bad in whole_flat:
        fail(f"forbidden text found: {bad}")
outside_exercises = re.sub(r"\s+", " ", "\n".join(pages[:5] + pages[6:]))
for bad in ["zatvorený lekáreň", "po vyšetrenie"]:
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

print("A2 PDF 4.12 verified")
print(f"path={pdf}")
print(f"pages={len(reader.pages)}")
print(f"title={reader.metadata.title!a}")
print(f"sha256={hashlib.sha256(pdf.read_bytes()).hexdigest()}")
