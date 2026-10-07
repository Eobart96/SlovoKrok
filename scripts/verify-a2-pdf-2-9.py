import argparse
import re
import subprocess
from pathlib import Path

import pdfplumber
from PIL import Image
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "output" / "pdf" / "A2" / "Module_02" / "Slovak_A2_Tema_2_9_Lokal_mesto_i_tema_razgovora.pdf"
RENDERS = ROOT / "tmp" / "pdfs" / "a2_2_9_final"
PDFINFO = Path(r"C:\Users\Eobar\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\poppler\Library\bin\pdfinfo.exe")


def verify_pdf():
    assert PDF.exists(), f"Missing PDF: {PDF}"
    assert PDF.stat().st_size > 50_000, "PDF is unexpectedly small"

    reader = PdfReader(str(PDF))
    assert len(reader.pages) == 7, f"Expected 7 pages, got {len(reader.pages)}"
    assert reader.metadata.title == "Slovak A2 - Тема 2.9 - Lokál: место и тема разговора"

    with pdfplumber.open(PDF) as document:
        texts = [(page.extract_text() or "") for page in document.pages]
        for index, page in enumerate(document.pages, start=1):
            assert abs(page.width - 595.276) < 1, f"Page {index}: wrong width"
            assert abs(page.height - 841.890) < 1, f"Page {index}: wrong height"
            assert len(texts[index - 1].strip()) > 250, f"Page {index}: too little extractable text"

    full_text = "\n".join(texts)
    required = [
        "Lokál: место и тема разговора", "Lokál: miesto a téma rozhovoru",
        "v / vo", "na", "pri", "o + Lokál", "Bývam v Bratislave",
        "Som na pošte", "Čakám pri škole", "Hovoríme o práci",
        "byt → byte", "park → parku", "hotel → hoteli", "škola → škole",
        "ulica → ulici", "práca → práci", "mesto → meste", "auto → aute",
        "námestie → námestí", "múzeum → múzeu", "v tom novom byte",
        "na tej hlavnej ulici", "v tomto malom meste", "-ých", "vo vlaku",
        "v škole", "na univerzite", "o mne", "o tebe", "o ňom", "o nej",
        "o nás", "o vás", "o nich", "o sebe", "o novom projekte",
        "o dobrej kolegyni", "o malom meste", "o nových pravidlách",
        "Мини-диалог", "Упражнение 1", "Упражнение 6", "Ответы",
        "Финальная проверка", "теме 2.10", "теме 2.11",
    ]
    for phrase in required:
        assert phrase in full_text, f"Missing phrase: {phrase}"

    examples = [
        "Bývam v Bratislave", "Som na pošte", "Čakám pri škole", "Hovoríme o práci",
        "Bývame v tom novom byte", "Stretneme sa na tej hlavnej ulici",
        "Pracujem v tomto malom meste", "V tých moderných bytoch je ticho",
        "Hovoríme o nových pracoviskách", "Hovorili o mne", "Často premýšľam o tebe",
        "Čítal som o ňom", "Rozprávame sa o nej", "Napísali článok o nás",
        "Čo povedal o vás", "Neviem veľa o nich", "Hovoríme o novom projekte",
        "Píšem o dobrej kolegyni", "Čítame o malom meste", "Diskutujeme o nových pravidlách",
        "Som v kancelárii pri okne", "Čakáme na hlavnej stanici", "Deti sú v mestskom parku",
        "Kniha je na malom stole", "Býva vo veľkom meste", "Rozprávame sa o novej práci",
        "Premýšľam o našom pláne", "Čítam článok o moderných mestách",
    ]
    assert sum(example in full_text for example in examples) >= 24, "Fewer than 24 expected Slovak examples were found"

    for page_number in range(1, 8):
        assert f"стр. {page_number} / 7" in texts[page_number - 1], f"Missing page number on page {page_number}"

    for bad in ["�", "□", "–", "—", "TODO", "PLACEHOLDER"]:
        assert bad not in full_text, f"Forbidden or broken text found: {bad}"
    assert not re.search(r"[\u2010-\u2014]", full_text), "Non-ASCII dash found"
    assert "s/so, pred, za, medzi, nad, pod" not in full_text, "Later lesson content was pulled into this PDF"

    info = subprocess.run(
        [str(PDFINFO), str(PDF)], check=True, capture_output=True, text=True,
        encoding="utf-8", errors="replace",
    ).stdout
    assert "Pages:           7" in info
    assert "Page size:       595.276 x 841.89 pts (A4)" in info
    assert "PDF syntax error" not in info

    print("A2 PDF 2.9 verified")
    print(f"pages={len(reader.pages)} size={PDF.stat().st_size} chars={len(full_text)} examples>=24")


def verify_renders():
    images = sorted(RENDERS.glob("page-*.png"))
    assert len(images) == 7, f"Expected 7 rendered pages, got {len(images)}"
    for index, image_path in enumerate(images, start=1):
        assert image_path.stat().st_size > 30_000, f"Render {index} is unexpectedly small"
        with Image.open(image_path) as image:
            assert image.width >= 1200 and image.height >= 1700, f"Render {index} has low resolution"
            extrema = image.convert("L").getextrema()
            assert extrema[0] < 245 and extrema[1] > 250, f"Render {index} appears blank"
    print("A2 PDF 2.9 renders verified")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-renders", action="store_true")
    args = parser.parse_args()
    verify_pdf()
    if args.check_renders:
        verify_renders()
