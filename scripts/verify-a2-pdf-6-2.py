import argparse
import re
import subprocess
from pathlib import Path

import pdfplumber
from PIL import Image
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "output/pdf/A2/Module_06/Slovak_A2_Tema_6_2_Obyavlenie_i_poisk_zhilya.pdf"
RENDERS = ROOT / "tmp/pdfs/a2_6_2_final"
PDFINFO = Path(r"C:\Users\Eobar\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\poppler\Library\bin\pdfinfo.exe")


def verify_pdf():
    assert PDF.exists() and PDF.stat().st_size > 50000
    reader = PdfReader(str(PDF))
    assert len(reader.pages) == 7
    assert reader.metadata.title == "Slovak A2 - Тема 6.2 - Объявление и поиск жилья"
    with pdfplumber.open(PDF) as document:
        texts = [page.extract_text() or "" for page in document.pages]
        for page_number, page in enumerate(document.pages, 1):
            assert abs(page.width - 595.276) < 1
            assert abs(page.height - 841.890) < 1
            assert len(texts[page_number - 1].strip()) > 250
    full = "\n".join(texts)
    required = [
        "Объявление и",
        "Как читать объявление",
        "Образец объявления",
        "Genitív в объявлениях и ценах",
        "Что входит в цену",
        "Сравнение и вежливые вопросы",
        "Короткое сообщение",
        "Два варианта: читаем и выбираем",
        "Упражнение 1",
        "Упражнение 6",
        "Ответы",
        "Финальная проверка",
        "бытовой проблеме и договариваться о решении",
    ]
    for item in required:
        assert item in full, item
    examples = [
        "Prenajmem svetlý 2-izbový byt",
        "Nájom je 650 € mesačne",
        "Internet nie je v cene",
        "Byt je voľný od 1. októbra",
        "byt bez balkóna",
        "v blízkosti centra",
        "do desiatich minút",
        "voľný od prvého októbra",
        "depozit vo výške nájmu",
        "cena vrátane energií",
        "Energie sú v cene",
        "Cena je bez energií",
        "Internet je zahrnutý v cene",
        "Províziu neplatíte",
        "Platí sa nájom a depozit",
        "Byt A je lacnejší ako byt B",
        "Byt B je väčší o 12 m²",
        "Byt A je bližšie k zastávke",
        "Byt A mi vyhovuje viac",
        "Chcel/a by som sa opýtať",
        "Sú, prosím, energie zahrnuté v cene",
        "Aká je, prosím, výška depozitu",
        "Kedy by bolo možné prísť na obhliadku",
        "Byt A je menší, ale je bližšie k centru",
        "Byt B je väčší a má balkón",
        "Mesačné náklady na byt A sú 750 €",
    ]
    assert sum(example in full for example in examples) >= 24
    assert "Ответы" not in "\n".join(texts[:6])
    for page_number in range(1, 8):
        assert f"стр. {page_number} / 7" in texts[page_number - 1]
    for bad in ["�", "□", "TODO", "PLACEHOLDER"]:
        assert bad not in full
    assert not re.search(r"[\u2010-\u2014]", full)
    info = subprocess.run(
        [str(PDFINFO), str(PDF)], check=True, capture_output=True,
        text=True, encoding="utf-8", errors="replace",
    ).stdout
    assert "Pages:           7" in info
    assert "Page size:       595.276 x 841.89 pts (A4)" in info
    print("A2 PDF 6.2 verified")
    print(f"pages=7 size={PDF.stat().st_size} chars={len(full)} examples>=24")


def verify_renders():
    images = sorted(RENDERS.glob("page-*.png"))
    assert len(images) == 7
    for image_path in images:
        assert image_path.stat().st_size > 30000
        with Image.open(image_path) as image:
            assert image.width >= 1200 and image.height >= 1700
            assert image.convert("L").getextrema()[0] < 245
    print("A2 PDF 6.2 renders verified")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-renders", action="store_true")
    args = parser.parse_args()
    verify_pdf()
    if args.check_renders:
        verify_renders()
