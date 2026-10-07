import argparse
import re
import subprocess
from pathlib import Path

import pdfplumber
from PIL import Image
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "output/pdf/A2/Module_06/Slovak_A2_Tema_6_1_Zhile_i_rayon.pdf"
RENDERS = ROOT / "tmp/pdfs/a2_6_1_final"
PDFINFO = Path(r"C:\Users\Eobar\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\poppler\Library\bin\pdfinfo.exe")


def verify_pdf():
    assert PDF.exists() and PDF.stat().st_size > 50000
    reader = PdfReader(str(PDF))
    assert len(reader.pages) == 7
    assert reader.metadata.title == "Slovak A2 - Тема 6.1 - Жильё и район"
    with pdfplumber.open(PDF) as document:
        texts = [page.extract_text() or "" for page in document.pages]
        for page_number, page in enumerate(document.pages, 1):
            assert abs(page.width - 595.276) < 1
            assert abs(page.height - 841.890) < 1
            assert len(texts[page_number - 1].strip()) > 250
    full = "\n".join(texts)
    required = [
        "Жильё и район",
        "Пространство: от жилья к комнате",
        "V или na + Lokál",
        "Мебель, техника и расположение",
        "Bývať, žiť и личные предпочтения",
        "Мини-диалог",
        "Банк фраз и связный профиль",
        "Модель письменного профиля",
        "Упражнение 1",
        "Упражнение 6",
        "Ответы",
        "Финальная проверка",
        "читать объявления, сравнивать условия и писать владельцу жилья",
    ]
    for item in required:
        assert item in full, item
    examples = [
        "Bývam v dvojizbovom byte",
        "V dome je nový výťah",
        "Byt má svetlú obývačku",
        "Kúpeľňa je vedľa spálne",
        "Bývam v byte v centre",
        "V kuchyni máme stôl",
        "Na stole je lampa",
        "Na sídlisku je park",
        "Bývame na treťom poschodí",
        "V obývačke je pohovka a televízor",
        "Vedľa postele stojí nočný stolík",
        "V kuchyni máme novú umývačku",
        "Na stole mám počítač",
        "Práčka je v kúpeľni",
        "Skrinka je vedľa okna",
        "Pohovka je oproti televízoru",
        "Stôl je medzi oknom a dverami",
        "Pri dome je malé ihrisko",
        "Bývam v prenajatom byte",
        "Bývam s kamarátkou",
        "Chcem žiť pokojnejšie",
        "Žije sa mi tu dobre",
        "Radšej bývam bližšie k centru",
        "Náš byt je tichší ako starý byt",
        "Pre mňa je dôležité dobré spojenie",
        "Páči sa mi zeleň",
    ]
    assert sum(example in full for example in examples) >= 24
    assert "Ответы" not in "\n".join(texts[:6])
    for page_number in range(1, 8):
        assert f"стр. {page_number} / 7" in texts[page_number - 1]
    for bad in ["�", "□", "TODO", "PLACEHOLDER"]:
        assert bad not in full
    assert not re.search(r"[\u2010-\u2014]", full)
    info = subprocess.run(
        [str(PDFINFO), str(PDF)],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    ).stdout
    assert "Pages:           7" in info
    assert "Page size:       595.276 x 841.89 pts (A4)" in info
    print("A2 PDF 6.1 verified")
    print(f"pages=7 size={PDF.stat().st_size} chars={len(full)} examples>=24")


def verify_renders():
    images = sorted(RENDERS.glob("page-*.png"))
    assert len(images) == 7
    for image_path in images:
        assert image_path.stat().st_size > 30000
        with Image.open(image_path) as image:
            assert image.width >= 1200 and image.height >= 1700
            assert image.convert("L").getextrema()[0] < 245
    print("A2 PDF 6.1 renders verified")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-renders", action="store_true")
    args = parser.parse_args()
    verify_pdf()
    if args.check_renders:
        verify_renders()
