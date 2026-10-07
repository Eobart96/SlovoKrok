import argparse
import re
import subprocess
from pathlib import Path

import pdfplumber
from PIL import Image
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "output" / "pdf" / "A2" / "Module_03" / "Slovak_A2_Tema_3_8_Neopredelennye_otricatelnye_i_obobshchayushchie_mestoimeniya.pdf"
RENDERS = ROOT / "tmp" / "pdfs" / "a2_3_8_final"
PDFINFO = Path(r"C:\Users\Eobar\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\poppler\Library\bin\pdfinfo.exe")


def verify_pdf():
    assert PDF.exists(), f"Missing PDF: {PDF}"
    assert PDF.stat().st_size > 50_000, "PDF is unexpectedly small"
    reader = PdfReader(str(PDF))
    assert len(reader.pages) == 7, f"Expected 7 pages, got {len(reader.pages)}"
    assert reader.metadata.title == "Slovak A2 - Тема 3.8 - Неопределённые, отрицательные и обобщающие местоимения"

    with pdfplumber.open(PDF) as document:
        texts = [(page.extract_text() or "") for page in document.pages]
        for index, page in enumerate(document.pages, start=1):
            assert abs(page.width - 595.276) < 1, f"Page {index}: wrong width"
            assert abs(page.height - 841.890) < 1, f"Page {index}: wrong height"
            assert len(texts[index - 1].strip()) > 250, f"Page {index}: too little extractable text"

    full_text = "\n".join(texts)
    required = [
        "Неопределённые, отрицательные", "Niekto, nikto, každý", "niekto / nikto",
        "niečo / nič", "niekde", "nikde", "nejaký", "žiadny", "každý / každá / každé",
        "všetci", "všetky", "všetko", "Двойное отрицание", "Nikto mi nič nepovedal",
        "Упражнение 1", "Упражнение 6", "Ответы", "Финальная проверка",
    ]
    for phrase in required:
        assert phrase in full_text, f"Missing phrase: {phrase}"

    examples = [
        "Niekto čaká pred domom", "Nikto nečaká pred domom", "Chcem niečo povedať",
        "Nechcem nič povedať", "Býva niekde blízko", "Nikde tu nebýva",
        "Hľadám nejaký hotel", "Nemáme žiadny voľný hotel", "Niekto neprišiel",
        "Nikto neprišiel", "s niekým", "od nikoho", "o ničom", "Musím niekomu zavolať",
        "Nikomu to nepoviem", "Nešiel som tam s nikým", "Máš nejakú otázku",
        "Nemám žiadnu otázku", "Potrebujeme nejaké riešenie", "Nenašli sme žiadne riešenie",
        "Každý dostal lístok", "Všetci dostali lístky", "Nie všetci prišli",
        "Všetky okná sú otvorené", "Všetko je otvorené", "Nikde som nikoho nevidel",
        "Nikomu som nikdy nič neposlal",
    ]
    assert sum(example in full_text for example in examples) >= 25, "Fewer than 25 expected Slovak examples were found"

    assert "Упражнен" not in texts[0]
    assert "Ответы" not in "\n".join(texts[:6])
    for page_number in range(1, 8):
        assert f"стр. {page_number} / 7" in texts[page_number - 1], f"Missing page number on page {page_number}"
    for bad in ["�", "□", "TODO", "PLACEHOLDER", "ne¬jaký"]:
        assert bad not in full_text, f"Forbidden or broken text found: {bad}"
    assert not re.search(r"[\u2010-\u2014]", full_text), "Non-ASCII dash found"
    assert "otcov" not in full_text.lower() and "matkin" not in full_text.lower(), "Previous possessive-adjective lesson was repeated"
    assert "koľko eur" not in full_text.lower(), "Later quantity lesson was pulled in"

    info = subprocess.run(
        [str(PDFINFO), str(PDF)], check=True, capture_output=True, text=True,
        encoding="utf-8", errors="replace",
    ).stdout
    assert "Pages:           7" in info
    assert "Page size:       595.276 x 841.89 pts (A4)" in info
    assert "PDF syntax error" not in info
    print("A2 PDF 3.8 verified")
    print(f"pages={len(reader.pages)} size={PDF.stat().st_size} chars={len(full_text)} examples>=25")


def verify_renders():
    images = sorted(RENDERS.glob("page-*.png"))
    assert len(images) == 7, f"Expected 7 rendered pages, got {len(images)}"
    for index, image_path in enumerate(images, start=1):
        assert image_path.stat().st_size > 30_000, f"Render {index} is unexpectedly small"
        with Image.open(image_path) as image:
            assert image.width >= 1200 and image.height >= 1700, f"Render {index} has low resolution"
            extrema = image.convert("L").getextrema()
            assert extrema[0] < 245 and extrema[1] > 250, f"Render {index} appears blank"
    print("A2 PDF 3.8 renders verified")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-renders", action="store_true")
    args = parser.parse_args()
    verify_pdf()
    if args.check_renders:
        verify_renders()
