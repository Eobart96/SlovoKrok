import re
from pathlib import Path

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
PDF_ROOT = ROOT / "output" / "pdf" / "A2"
files = sorted(PDF_ROOT.glob("Module_*/Slovak_A2_Tema_*.pdf"))
if len(files) != 72:
    raise SystemExit(f"Expected 72 PDFs, found {len(files)}")

seen = set()
total_pages = 0
total_text = 0
cover_identity_warnings = []
page_counts = {}
for path in files:
    match = re.match(r"Slovak_A2_Tema_(\d+)_(\d+)_.*\.pdf$", path.name)
    if not match:
        raise SystemExit(f"Unexpected filename: {path.name}")
    module, topic = int(match.group(1)), int(match.group(2))
    identity = f"{module}.{topic}"
    if identity in seen:
        raise SystemExit(f"Duplicate topic identity: {identity}")
    seen.add(identity)
    expected_folder = f"Module_{module:02d}"
    if path.parent.name != expected_folder:
        raise SystemExit(f"Wrong folder for {path.name}: {path.parent.name}")
    if path.stat().st_size < 40_000:
        raise SystemExit(f"Suspiciously small PDF: {path.name}")

    reader = PdfReader(str(path))
    if not 6 <= len(reader.pages) <= 8:
        raise SystemExit(f"{path.name}: expected 6-8 pages, got {len(reader.pages)}")
    page_counts[len(reader.pages)] = page_counts.get(len(reader.pages), 0) + 1
    title = (reader.metadata.title or "").strip()
    if identity not in title:
        raise SystemExit(f"{path.name}: metadata title misses {identity}: {title!r}")
    texts = []
    for page_index, page in enumerate(reader.pages, 1):
        width, height = float(page.mediabox.width), float(page.mediabox.height)
        if abs(width - 595.28) > 2 or abs(height - 841.89) > 2:
            raise SystemExit(f"{path.name}: page {page_index} is not A4: {width} x {height}")
        text = (page.extract_text() or "").strip()
        if len(text) < 100:
            raise SystemExit(f"{path.name}: page {page_index} has too little text")
        if re.search(r"[\u4e00-\u9fff\u3040-\u30ff\u0600-\u06ff]", text):
            raise SystemExit(f"{path.name}: unexpected script on page {page_index}")
        texts.append(text)
        total_text += len(text)
    cover = texts[0]
    if identity not in cover and f"{module}_{topic}" not in cover:
        cover_identity_warnings.append(identity)
    total_pages += len(reader.pages)

print(f"pdfs={len(files)}, pages={total_pages}, text_chars={total_text}")
print("page_counts=" + ",".join(f"{pages}:{count}" for pages, count in sorted(page_counts.items())))
print(f"cover_identity_warning_count={len(cover_identity_warnings)}")
print(f"cover_identity_warnings={','.join(cover_identity_warnings) if cover_identity_warnings else 'none'}")
print("A2 PDF collection integrity verified")
