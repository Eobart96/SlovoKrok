import argparse
import re
import subprocess
from pathlib import Path

import pdfplumber
from PIL import Image
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "output" / "pdf" / "A2" / "Module_03" / "Slovak_A2_Tema_3_3_Stepeni_sravneniya_prilagatelnyh.pdf"
RENDERS = ROOT / "tmp" / "pdfs" / "a2_3_3_final"
PDFINFO = Path(r"C:\Users\Eobar\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\poppler\Library\bin\pdfinfo.exe")


def verify_pdf():
    assert PDF.exists(), f"Missing PDF: {PDF}"
    assert PDF.stat().st_size > 50_000, "PDF is unexpectedly small"
    reader = PdfReader(str(PDF))
    assert len(reader.pages) == 7, f"Expected 7 pages, got {len(reader.pages)}"
    assert reader.metadata.title == "Slovak A2 - Тема 3.3 - Степени сравнения прилагательных"

    with pdfplumber.open(PDF) as document:
        texts = [(page.extract_text() or "") for page in document.pages]
        for index, page in enumerate(document.pages, start=1):
            assert abs(page.width - 595.276) < 1, f"Page {index}: wrong width"
            assert abs(page.height - 841.890) < 1, f"Page {index}: wrong height"
            assert len(texts[index - 1].strip()) > 250, f"Page {index}: too little extractable text"

    full_text = "\n".join(texts)
    required = [
        "A2", "ТЕМА 3.3", "Степени сравнения прилагательных", "Stupňovanie prídavných mien", "pozitív", "komparatív",
        "superlatív", "-ší", "-ejší", "vyšší", "lepší", "horší", "najvyšší", "najlepší",
        "najhorší", "ako", "taký... ako", "dobrý", "zlý", "veľký", "malý", "pekný",
        "vysoký", "nízky", "blízky", "Мини-диалог", "Упражнение 1", "Упражнение 6",
        "Ответы", "Финальная проверка", "теме 3.4",
    ]
    for phrase in required:
        assert phrase in full_text, f"Missing phrase: {phrase}"

    examples = [
        "Peter je vyšší ako Martin", "Tento plán je lepší ako prvý",
        "Modrý kabát je lacnejší ako čierny", "Hotel je taký pohodlný ako apartmán",
        "Táto cesta je taká krátka ako druhá", "Mesto je také pokojné ako dedina",
        "Toto je najlacnejší telefón v ponuke", "Eva je najmladšia zo všetkých kolegýň",
        "Ktorý hotel má najlepšiu polohu", "Vybrali sme najväčšiu izbu",
        "Je to najhorší variant pre rodinu", "Lomnický štít je vyšší ako Kriváň",
        "Táto zastávka je bližšia k centru", "Nový model je menší, ale výkonnejší",
        "Anna je mladšia ako Eva", "Peter je najstarší v tíme",
        "Košice sú menšie ako Bratislava", "Toto je najkrajšie námestie",
        "Tento notebook je výkonnejší", "Tamten je najlacnejší",
        "Prvý plán je lepší", "Druhý je taký jednoduchý ako tretí",
    ]
    assert sum(example in full_text for example in examples) >= 20, "Fewer than 20 expected Slovak examples were found"

    assert "Упражнение" not in texts[0]
    assert "Ответы" not in "\n".join(texts[:6])
    for page_number in range(1, 8):
        assert f"стр. {page_number} / 7" in texts[page_number - 1], f"Missing page number on page {page_number}"
    for bad in ["�", "□", "TODO", "PLACEHOLDER"]:
        assert bad not in full_text, f"Forbidden or broken text found: {bad}"
    assert not re.search(r"[\u2010-\u2014]", full_text), "Non-ASCII dash found"
    assert "trochu, dosť, veľmi" not in full_text, "Topic 3.4 leaked into this PDF"
    assert "косвенных падежах" not in full_text.lower(), "Later pronoun lesson leaked into this PDF"

    info = subprocess.run(
        [str(PDFINFO), str(PDF)], check=True, capture_output=True, text=True,
        encoding="utf-8", errors="replace",
    ).stdout
    assert "Pages:           7" in info
    assert "Page size:       595.276 x 841.89 pts (A4)" in info
    assert "PDF syntax error" not in info
    print("A2 PDF 3.3 verified")
    print(f"pages={len(reader.pages)} size={PDF.stat().st_size} chars={len(full_text)} examples>=20")


def verify_renders():
    images = sorted(RENDERS.glob("page-*.png"))
    assert len(images) == 7, f"Expected 7 rendered pages, got {len(images)}"
    for index, image_path in enumerate(images, start=1):
        assert image_path.stat().st_size > 30_000, f"Render {index} is unexpectedly small"
        with Image.open(image_path) as image:
            assert image.width >= 1200 and image.height >= 1700, f"Render {index} has low resolution"
            extrema = image.convert("L").getextrema()
            assert extrema[0] < 245 and extrema[1] > 250, f"Render {index} appears blank"
    print("A2 PDF 3.3 renders verified")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-renders", action="store_true")
    args = parser.parse_args()
    verify_pdf()
    if args.check_renders:
        verify_renders()
