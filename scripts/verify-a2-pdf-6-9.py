import argparse
import re
import subprocess
from pathlib import Path

import pdfplumber
from PIL import Image
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "output/pdf/A2/Module_06/Slovak_A2_Tema_6_9_Onlayn_zakaz_dostavka_i_vozvrat.pdf"
RENDERS = ROOT / "tmp/pdfs/a2_6_9_final"
PDFINFO = Path(r"C:\Users\Eobar\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\poppler\Library\bin\pdfinfo.exe")


def verify_pdf():
    assert PDF.exists() and PDF.stat().st_size > 50000
    reader = PdfReader(str(PDF))
    assert not reader.is_encrypted
    assert len(reader.pages) == 7
    assert reader.metadata.title == "Slovak A2 - Тема 6.9 - Онлайн-заказ, доставка и возврат"
    root = reader.trailer["/Root"]
    assert "/AcroForm" not in root
    assert "/OpenAction" not in root
    names = root.get("/Names")
    if names:
        assert "/JavaScript" not in names
    with pdfplumber.open(PDF) as document:
        texts = [page.extract_text() or "" for page in document.pages]
        for page_number, page in enumerate(document.pages, 1):
            assert abs(page.width - 595.276) < 1
            assert abs(page.height - 841.890) < 1
            assert len(texts[page_number - 1].strip()) > 250
    full = "\n".join(texts)
    required = [
        "Онлайн-заказ, доставка и возврат",
        "Статус заказа и прошедшее время",
        "Что будет дальше: два будущих времени",
        "Vziať или priniesť",
        "Адрес и пункт выдачи",
        "Причина, следствие и передача условий",
        "Передаём сообщение другому человеку",
        "Мини-диалог с поддержкой",
        "Условия возврата из письма",
        "Упражнение 1",
        "Упражнение 6",
        "Ответы и итоговая проверка",
        "Модуль 6 завершён",
    ]
    for item in required:
        assert item in full, item
    examples = [
        "Objednávka bola prijatá",
        "Platba bola prijatá",
        "Tovar bol odoslaný",
        "Zásielka je na ceste",
        "Zásielka mešká",
        "Zásielka je pripravená na vyzdvihnutie",
        "Zásielka bola doručená",
        "V pondelok som si objednal bundu",
        "Hneď som zaplatil kartou",
        "Obchod v utorok balík odoslal",
        "Kuriér mi včera volal",
        "Balík však neprišiel",
        "Budem čakať na kuriéra",
        "Balík si vyzdvihnem zajtra ráno",
        "Kuriér balík doručí popoludní",
        "Vezmem si občiansky preukaz",
        "Kuriér prinesie balík domov",
        "Potrebujem zmeniť doručovaciu adresu",
        "Balík je uložený na výdajnom mieste",
        "Na vyzdvihnutie potrebujete kód z SMS",
        "Kontaktoval som podporu, pretože zásielka mešká",
        "Balík neprišiel, preto som napísal predajcovi",
        "Tovar je poškodený, takže ho vrátim",
        "Formulár na vrátenie je v balíku",
    ]
    assert sum(example in full for example in examples) >= 22
    assert "Ответы" not in "\n".join(texts[:6])
    for page_number in range(1, 8):
        assert f"стр. {page_number} / 7" in texts[page_number - 1]
    for bad in ["�", "□", "TODO", "PLACEHOLDER"]:
        assert bad not in full
    assert not re.search(r"[\u2010-\u2014]", full)
    info = subprocess.run([str(PDFINFO), str(PDF)], capture_output=True, text=True, encoding="utf-8", errors="replace", check=True).stdout
    assert "Pages:           7" in info
    assert "Page size:       595.276 x 841.89 pts (A4)" in info
    print("A2 PDF 6.9 verified")
    print(f"pages=7 size={PDF.stat().st_size} chars={len(full)} examples>=22")


def verify_renders():
    images = sorted(RENDERS.glob("page-*.png"))
    assert len(images) == 7
    for image_path in images:
        assert image_path.stat().st_size > 25000
        with Image.open(image_path) as image:
            assert image.width >= 1400 and image.height >= 2000
    print("A2 PDF 6.9 renders verified")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-renders", action="store_true")
    args = parser.parse_args()
    verify_pdf()
    if args.check_renders:
        verify_renders()
