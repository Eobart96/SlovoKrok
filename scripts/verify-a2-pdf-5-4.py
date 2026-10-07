import argparse
import re
import subprocess
from pathlib import Path

import pdfplumber
from PIL import Image
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "output" / "pdf" / "A2" / "Module_05" / "Slovak_A2_Tema_5_4_Otnositelnye_predlozheniya_s_ktory.pdf"
RENDERS = ROOT / "tmp" / "pdfs" / "a2_5_4_final"
PDFINFO = Path(r"C:\Users\Eobar\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\poppler\Library\bin\pdfinfo.exe")


def verify_pdf():
    assert PDF.exists(), f"Missing PDF: {PDF}"
    assert PDF.stat().st_size > 50_000, "PDF is unexpectedly small"
    reader = PdfReader(str(PDF))
    assert len(reader.pages) == 7, f"Expected 7 pages, got {len(reader.pages)}"
    assert reader.metadata.title == "Slovak A2 - Тема 5.4 - Относительные предложения с ktorý"

    with pdfplumber.open(PDF) as document:
        texts = [(page.extract_text() or "") for page in document.pages]
        for index, page in enumerate(document.pages, start=1):
            assert abs(page.width - 595.276) < 1, f"Page {index}: wrong width"
            assert abs(page.height - 841.890) < 1, f"Page {index}: wrong height"
            assert len(texts[index - 1].strip()) > 250, f"Page {index}: too little extractable text"

    full_text = "\n".join(texts)
    required = [
        "Относительные предложения", "Vzťažné vety", "Nominatív: ktorý сам выполняет действие",
        "Из двух фраз в одну", "Падеж зависит от роли внутри придаточного",
        "Главный контраст", "Частотные формы: женщина и множественное число",
        "Позиция и запятые", "Мини-диалог: выбираем квартиру",
        "Упражнение 1", "Упражнение 6", "Ответы", "Финальная проверка",
        "kto, čo", "kde",
    ]
    for phrase in required:
        assert phrase in full_text, f"Missing phrase: {phrase}"

    examples = [
        "To je kolega, ktorý pracuje doma", "Poznám firmu, ktorá hľadá ľudí",
        "To je auto, ktoré stojí pred domom", "To sú študenti, ktorí bývajú vedľa",
        "To sú knihy, ktoré ležia na stole", "Hľadám lekára, ktorý hovorí po rusky",
        "Máme izbu, ktorá má balkón", "Vybral som si tričko, ktoré je lacnejšie",
        "Poznám muža, ktorý tu pracuje", "Poznám muža, ktorého hľadáš",
        "To je kolega, ktorému píšem", "To je projekt, o ktorom hovoríme",
        "To je kolega, s ktorým pracujem", "To je mesto, do ktorého cestujeme",
        "Poznám muža, ktorý spieva", "Poznám muža, ktorého počúvaš",
        "Poznám muža, o ktorom hovoríš", "To je žena, ktorú som včera stretol",
        "To je kolegyňa, ktorej často pomáham", "To je téma, o ktorej sa učíme",
        "To je kamarátka, s ktorou cestujem", "To sú ľudia, ktorým dôverujem",
        "To sú problémy, o ktorých hovoríme", "To sú kolegovia, s ktorými pracujem",
        "Hľadám byt, ktorý má balkón", "Muž, ktorý tam čaká, je môj sused",
        "Kniha, ktorú si mi požičal, je výborná",
    ]
    assert sum(example in full_text for example in examples) >= 25, "Fewer than 25 expected Slovak examples were found"

    assert "Упражнен" not in texts[0]
    assert "Ответы" not in "\n".join(texts[:6])
    for page_number in range(1, 8):
        assert f"стр. {page_number} / 7" in texts[page_number - 1], f"Missing page number on page {page_number}"
    for bad in ["�", "□", "TODO", "PLACEHOLDER"]:
        assert bad not in full_text, f"Forbidden or broken text found: {bad}"
    assert not re.search(r"[\u2010-\u2014]", full_text), "Non-ASCII dash found"
    assert "viem, kto" not in full_text.lower(), "Later topic 5.5 was pulled in"
    assert "povedz, čo" not in full_text.lower(), "Later topic 5.5 was pulled in"
    assert "ukáž, kde" not in full_text.lower(), "Later topic 5.5 was pulled in"

    info = subprocess.run(
        [str(PDFINFO), str(PDF)], check=True, capture_output=True, text=True,
        encoding="utf-8", errors="replace",
    ).stdout
    assert "Pages:           7" in info
    assert "Page size:       595.276 x 841.89 pts (A4)" in info
    assert "PDF syntax error" not in info
    print("A2 PDF 5.4 verified")
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
    print("A2 PDF 5.4 renders verified")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-renders", action="store_true")
    args = parser.parse_args()
    verify_pdf()
    if args.check_renders:
        verify_renders()
