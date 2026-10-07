import argparse
import re
import subprocess
from pathlib import Path

import pdfplumber
from PIL import Image
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "output/pdf/A2/Module_06/Slovak_A2_Tema_6_8_Odezhda_primerka_oplata_i_obmen.pdf"
RENDERS = ROOT / "tmp/pdfs/a2_6_8_final"
PDFINFO = Path(r"C:\Users\Eobar\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\poppler\Library\bin\pdfinfo.exe")


def verify_pdf():
    assert PDF.exists() and PDF.stat().st_size > 50000
    reader = PdfReader(str(PDF))
    assert len(reader.pages) == 7
    assert reader.metadata.title == "Slovak A2 - Тема 6.8 - Одежда, примерка, оплата и обмен"
    with pdfplumber.open(PDF) as document:
        texts = [page.extract_text() or "" for page in document.pages]
        for page_number, page in enumerate(document.pages, 1):
            assert abs(page.width - 595.276) < 1
            assert abs(page.height - 841.890) < 1
            assert len(texts[page_number - 1].strip()) > 250
    full = "\n".join(texts)
    required = [
        "Одежда, примерка",
        "Выбираем вещь: Akuzatív",
        "Полезные сочетания",
        "Примерка и сравнение",
        "Как сидит одежда",
        "Оплата и вид глагола",
        "Процесс или завершённый результат",
        "Обмен: причина и вежливая просьба",
        "Как объяснить проблему",
        "Мини-диалог об обмене",
        "Упражнение 1",
        "Упражнение 6",
        "Ответы и итоговая проверка",
        "статус онлайн-заказа",
    ]
    for item in required:
        assert item in full, item
    examples = [
        "Hľadám čierny kabát",
        "Chcem modrú bundu",
        "Potrebujem biele tričko",
        "Skúšam pohodlné topánky",
        "bavlnenú košeľu",
        "Potrebujem väčšiu veľkosť",
        "Máte menšiu bundu",
        "Chcem kratšie nohavice",
        "Tieto topánky sú pohodlnejšie",
        "Sedí mi dobre",
        "Je mi malá",
        "Tlačí ma v páse",
        "Môžem si to vyskúšať",
        "Môžem zaplatiť kartou",
        "Zaplatím mobilom",
        "Zaplatím v hotovosti",
        "Chcem si vyskúšať túto bundu",
        "Potrebujem vymeniť veľkosť",
        "Chcel by som túto košeľu vymeniť",
        "Mohli by ste mi priniesť väčšiu veľkosť",
        "Dalo by sa ju vymeniť za inú farbu",
        "Zips nefunguje",
        "Na košeli chýba gombík",
        "Šev sa pára",
    ]
    assert sum(example in full for example in examples) >= 22
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
    print("A2 PDF 6.8 verified")
    print(f"pages=7 size={PDF.stat().st_size} chars={len(full)} examples>=22")


def verify_renders():
    images = sorted(RENDERS.glob("page-*.png"))
    assert len(images) == 7
    for image_path in images:
        assert image_path.stat().st_size > 30000
        with Image.open(image_path) as image:
            assert image.width >= 1200 and image.height >= 1700
            assert image.convert("L").getextrema()[0] < 245
    print("A2 PDF 6.8 renders verified")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-renders", action="store_true")
    args = parser.parse_args()
    verify_pdf()
    if args.check_renders:
        verify_renders()
