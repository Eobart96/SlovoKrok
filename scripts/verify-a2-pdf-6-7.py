import argparse
import re
import subprocess
from pathlib import Path

import pdfplumber
from PIL import Image
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "output/pdf/A2/Module_06/Slovak_A2_Tema_6_7_Kolichestvo_upakovka_i_informatsiya_o_tovare.pdf"
RENDERS = ROOT / "tmp/pdfs/a2_6_7_final"
PDFINFO = Path(r"C:\Users\Eobar\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\poppler\Library\bin\pdfinfo.exe")


def verify_pdf():
    assert PDF.exists() and PDF.stat().st_size > 50000
    reader = PdfReader(str(PDF))
    assert len(reader.pages) == 7
    assert reader.metadata.title == "Slovak A2 - Тема 6.7 - Количество, упаковка и информация о товаре"
    with pdfplumber.open(PDF) as document:
        texts = [page.extract_text() or "" for page in document.pages]
        for page_number, page in enumerate(document.pages, 1):
            assert abs(page.width - 595.276) < 1
            assert abs(page.height - 841.890) < 1
            assert len(texts[page_number - 1].strip()) > 250
    full = "\n".join(texts)
    required = [
        "Количество, упаковка",
        "Мера или упаковка + Genitív",
        "Неопределённое количество",
        "Два, три, четыре или пять и больше",
        "Как попросить товар",
        "Что искать на этикетке",
        "Материал и происхождение",
        "Цена, срок и короткая инструкция",
        "Две разные даты",
        "Модель покупки и упражнения",
        "Упражнение 1",
        "Упражнение 6",
        "Ответы и итоговая проверка",
        "выбирать одежду",
    ]
    for item in required:
        assert item in full, item
    examples = [
        "kilo jabĺk",
        "pol kila paradajok",
        "liter mlieka",
        "dvesto gramov syra",
        "fľaša minerálnej vody",
        "balenie ryže",
        "téglik bieleho jogurtu",
        "veľa cukru",
        "málo soli",
        "trochu oleja",
        "Koľko syra chcete",
        "dve fľaše vody",
        "päť fliaš vody",
        "tri balenia cestovín",
        "šesť balení cestovín",
        "Prosím si dvesto gramov šunky",
        "Máte aj menšie balenie",
        "Predáva sa to aj po kusoch",
        "Čisté množstvo: 500 g",
        "Môže obsahovať orechy",
        "Krajina pôvodu: Slovensko",
        "Obal je z papiera",
        "Vyrobené na Slovensku",
        "spotrebujte do",
        "minimálna trvanlivosť do",
    ]
    assert sum(example in full for example in examples) >= 23
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
    print("A2 PDF 6.7 verified")
    print(f"pages=7 size={PDF.stat().st_size} chars={len(full)} examples>=23")


def verify_renders():
    images = sorted(RENDERS.glob("page-*.png"))
    assert len(images) == 7
    for image_path in images:
        assert image_path.stat().st_size > 30000
        with Image.open(image_path) as image:
            assert image.width >= 1200 and image.height >= 1700
            assert image.convert("L").getextrema()[0] < 245
    print("A2 PDF 6.7 renders verified")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-renders", action="store_true")
    args = parser.parse_args()
    verify_pdf()
    if args.check_renders:
        verify_renders()
