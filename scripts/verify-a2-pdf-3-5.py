import argparse
import re
import subprocess
from pathlib import Path

import pdfplumber
from PIL import Image
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "output" / "pdf" / "A2" / "Module_03" / "Slovak_A2_Tema_3_5_Lichnye_mestoimeniya_v_kosvennyh_padezhah.pdf"
RENDERS = ROOT / "tmp" / "pdfs" / "a2_3_5_final"
PDFINFO = Path(r"C:\Users\Eobar\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\poppler\Library\bin\pdfinfo.exe")


def verify_pdf():
    assert PDF.exists(), f"Missing PDF: {PDF}"
    assert PDF.stat().st_size > 50_000, "PDF is unexpectedly small"
    reader = PdfReader(str(PDF))
    assert len(reader.pages) == 7, f"Expected 7 pages, got {len(reader.pages)}"
    assert reader.metadata.title == "Slovak A2 - Тема 3.5 - Личные местоимения в косвенных падежах"

    with pdfplumber.open(PDF) as document:
        texts = [(page.extract_text() or "") for page in document.pages]
        for index, page in enumerate(document.pages, start=1):
            assert abs(page.width - 595.276) < 1, f"Page {index}: wrong width"
            assert abs(page.height - 841.890) < 1, f"Page {index}: wrong height"
            assert len(texts[index - 1].strip()) > 250, f"Page {index}: too little extractable text"

    full_text = "\n".join(texts)
    required = [
        "Личные местоимения в косвенных падежах", "Osobné zámená v nepriamych pádoch",
        "G genitív", "D datív", "A akuzatív", "L lokál", "I inštrumentál",
        "mňa / ma", "mne / mi", "teba / ťa", "tebe / ti", "jeho / ho",
        "jemu / mu", "pre ňu", "k nemu", "o nich", "s nimi",
        "дательный + винительный", "by - som/si/sme/ste - sa/si - D - A",
        "Мини-диалог", "Упражнение 1", "Упражнение 6", "Ответы", "Финальная проверка",
    ]
    for phrase in required:
        assert phrase in full_text, f"Missing phrase: {phrase}"

    examples = [
        "Bojím sa ho", "Pomôžem jej", "Poznáš ma", "Hovoríme o nich", "Idem s ním",
        "Vidím ho každý deň", "Pozvali mňa, nie jeho", "Jemu to nepoviem", "Bez nej nepôjdem",
        "Bez nich nezačneme", "Mám správu od nej", "Prídem k nemu večer", "Je to pre ňu",
        "Často o ňom hovorí", "Pracujem s nimi", "Dám mu kľúč", "Idem k nemu",
        "Dnes mu zavolám", "Dám ti ho zajtra", "Včera som mu ju poslal",
        "Ukázal by som vám ho", "ráno mi ju poslala", "O chvíľu ti ju prepošlem",
        "Potom jej odpoviem", "s ňou stretneme zajtra",
    ]
    assert sum(example in full_text for example in examples) >= 23, "Fewer than 23 expected Slovak examples were found"

    assert "Упражнение" not in texts[0]
    assert "Ответы" not in "\n".join(texts[:6])
    for page_number in range(1, 8):
        assert f"стр. {page_number} / 7" in texts[page_number - 1], f"Missing page number on page {page_number}"
    for bad in ["�", "□", "TODO", "PLACEHOLDER"]:
        assert bad not in full_text, f"Forbidden or broken text found: {bad}"
    assert not re.search(r"[\u2010-\u2014]", full_text), "Non-ASCII dash found"
    assert "местоимение svoj" not in full_text.lower(), "Later possessive lesson was pulled into this PDF"

    info = subprocess.run(
        [str(PDFINFO), str(PDF)], check=True, capture_output=True, text=True,
        encoding="utf-8", errors="replace",
    ).stdout
    assert "Pages:           7" in info
    assert "Page size:       595.276 x 841.89 pts (A4)" in info
    assert "PDF syntax error" not in info
    print("A2 PDF 3.5 verified")
    print(f"pages={len(reader.pages)} size={PDF.stat().st_size} chars={len(full_text)} examples>=23")


def verify_renders():
    images = sorted(RENDERS.glob("page-*.png"))
    assert len(images) == 7, f"Expected 7 rendered pages, got {len(images)}"
    for index, image_path in enumerate(images, start=1):
        assert image_path.stat().st_size > 30_000, f"Render {index} is unexpectedly small"
        with Image.open(image_path) as image:
            assert image.width >= 1200 and image.height >= 1700, f"Render {index} has low resolution"
            extrema = image.convert("L").getextrema()
            assert extrema[0] < 245 and extrema[1] > 250, f"Render {index} appears blank"
    print("A2 PDF 3.5 renders verified")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-renders", action="store_true")
    args = parser.parse_args()
    verify_pdf()
    if args.check_renders:
        verify_renders()
