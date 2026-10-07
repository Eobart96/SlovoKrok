import argparse
import re
import subprocess
from pathlib import Path

import pdfplumber
from PIL import Image
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "output" / "pdf" / "A2" / "Module_03" / "Slovak_A2_Tema_3_7_Prityazhatelnye_prilagatelnye.pdf"
RENDERS = ROOT / "tmp" / "pdfs" / "a2_3_7_final"
PDFINFO = Path(r"C:\Users\Eobar\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\poppler\Library\bin\pdfinfo.exe")


def verify_pdf():
    assert PDF.exists(), f"Missing PDF: {PDF}"
    assert PDF.stat().st_size > 50_000, "PDF is unexpectedly small"
    reader = PdfReader(str(PDF))
    assert len(reader.pages) == 7, f"Expected 7 pages, got {len(reader.pages)}"
    assert reader.metadata.title == "Slovak A2 - Тема 3.7 - Притяжательные прилагательные"

    with pdfplumber.open(PDF) as document:
        texts = [(page.extract_text() or "") for page in document.pages]
        for index, page in enumerate(document.pages, start=1):
            assert abs(page.width - 595.276) < 1, f"Page {index}: wrong width"
            assert abs(page.height - 841.890) < 1, f"Page {index}: wrong height"
            assert len(texts[index - 1].strip()) > 250, f"Page {index}: too little extractable text"

    full_text = "\n".join(texts)
    required = [
        "Притяжательные прилагательные", "Privlastňovacie prídavné mená",
        "otcov a matkin", "-ov", "-in", "čí? čia? čie?",
        "otcovho / matkinho", "otcovej / matkinej", "otcovým / matkiným",
        "otcových / matkiných", "otcovými / matkinými", "Где форма естественна",
        "Genitív", "Мини-диалог", "Упражнение 1", "Упражнение 6", "Ответы", "Финальная проверка",
    ]
    for phrase in required:
        assert phrase in full_text, f"Missing phrase: {phrase}"

    examples = [
        "otcov kabát", "otcova kniha", "otcovo auto", "bratov bicykel", "bratova izba",
        "Petrov kľúč", "Petrova taška", "Petrovo číslo", "Jánov plán", "Jánova práca",
        "matkin kabát", "matkina kniha", "matkino auto", "mamin hlas", "mamina kabelka",
        "sestrin syn", "sestrina izba", "Janin zošit", "Janina správa", "Janino miesto",
        "Bez otcovho súhlasu", "k maminmu autu", "Poznám Petrovho brata", "Mám Petrov telefón",
        "o matkinej práci", "s otcovým kolegom", "Prišli Petrovi bratia",
        "Vidím Petrových bratov", "Janine knihy", "o Janiných knihách",
    ]
    assert sum(example in full_text for example in examples) >= 27, "Fewer than 27 expected Slovak examples were found"

    assert "Упражнен" not in texts[0]
    assert "Ответы" not in "\n".join(texts[:6])
    for page_number in range(1, 8):
        assert f"стр. {page_number} / 7" in texts[page_number - 1], f"Missing page number on page {page_number}"
    for bad in ["�", "□", "TODO", "PLACEHOLDER"]:
        assert bad not in full_text, f"Forbidden or broken text found: {bad}"
    assert not re.search(r"[\u2010-\u2014]", full_text), "Non-ASCII dash found"
    assert "niekto" not in full_text.lower() and "nikto" not in full_text.lower(), "Later indefinite-pronoun lesson was pulled in"

    info = subprocess.run(
        [str(PDFINFO), str(PDF)], check=True, capture_output=True, text=True,
        encoding="utf-8", errors="replace",
    ).stdout
    assert "Pages:           7" in info
    assert "Page size:       595.276 x 841.89 pts (A4)" in info
    assert "PDF syntax error" not in info
    print("A2 PDF 3.7 verified")
    print(f"pages={len(reader.pages)} size={PDF.stat().st_size} chars={len(full_text)} examples>=27")


def verify_renders():
    images = sorted(RENDERS.glob("page-*.png"))
    assert len(images) == 7, f"Expected 7 rendered pages, got {len(images)}"
    for index, image_path in enumerate(images, start=1):
        assert image_path.stat().st_size > 30_000, f"Render {index} is unexpectedly small"
        with Image.open(image_path) as image:
            assert image.width >= 1200 and image.height >= 1700, f"Render {index} has low resolution"
            extrema = image.convert("L").getextrema()
            assert extrema[0] < 245 and extrema[1] > 250, f"Render {index} appears blank"
    print("A2 PDF 3.7 renders verified")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-renders", action="store_true")
    args = parser.parse_args()
    verify_pdf()
    if args.check_renders:
        verify_renders()
