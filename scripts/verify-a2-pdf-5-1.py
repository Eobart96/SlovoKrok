import argparse
import re
import subprocess
from pathlib import Path

import pdfplumber
from PIL import Image
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "output" / "pdf" / "A2" / "Module_05" / "Slovak_A2_Tema_5_1_Soedinyaem_mysli_a_ale_alebo.pdf"
RENDERS = ROOT / "tmp" / "pdfs" / "a2_5_1_final"
PDFINFO = Path(r"C:\Users\Eobar\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\poppler\Library\bin\pdfinfo.exe")


def verify_pdf():
    assert PDF.exists(), f"Missing PDF: {PDF}"
    assert PDF.stat().st_size > 50_000, "PDF is unexpectedly small"
    reader = PdfReader(str(PDF))
    assert len(reader.pages) == 7, f"Expected 7 pages, got {len(reader.pages)}"
    assert reader.metadata.title == "Slovak A2 - Тема 5.1 - Соединяем мысли: a, ale, alebo"

    with pdfplumber.open(PDF) as document:
        texts = [(page.extract_text() or "") for page in document.pages]
        for index, page in enumerate(document.pages, start=1):
            assert abs(page.width - 595.276) < 1, f"Page {index}: wrong width"
            assert abs(page.height - 841.890) < 1, f"Page {index}: wrong height"
            assert len(texts[index - 1].strip()) > 250, f"Page {index}: too little extractable text"

    full_text = "\n".join(texts)
    required = [
        "Соединяем мысли:", "Spájame myšlienky", "Союз a: добавляем и продолжаем",
        "Русское \"а\" не всегда означает ale", "Союз ale: поворачиваем мысль",
        "Главный сигнал: запятая", "Союз alebo: предлагаем выбор",
        "Короткая карта пунктуации", "Строим короткое связное высказывание",
        "Мини-диалог: план на вечер", "Упражнение 1", "Упражнение 6", "Ответы",
        "Финальная проверка", "aj - aj", "ani - ani",
    ]
    for phrase in required:
        assert phrase in full_text, f"Missing phrase: {phrase}"

    examples = [
        "Kúpim chlieb a mlieko", "Byt je malý a útulný", "Otvoril okno a zavolal Petrovi",
        "Ja pracujem doma a sestra pracuje v kancelárii", "Najprv sa najeme a potom pôjdeme von",
        "Ja bývam v Bratislave a brat býva v Nitre", "Ráno cvičím a večer čítam",
        "Kurz je praktický a učiteľ vysvetľuje jasne", "Sadli sme si a objednali sme si kávu",
        "Chcem ísť, ale nemám čas", "Hotel je pekný, ale drahý", "Je leto, ale dnes je chladno",
        "Veľa som sa učil, ale test bol ťažký", "Peter vstáva skoro, ale Jana spí dlho",
        "Rozumiem, ale nesúhlasím", "To je dobrý nápad, ale dnes to nestihnem",
        "Dáš si čaj alebo kávu", "Stretneme sa dnes alebo zajtra",
        "Môžeme ísť pešo alebo cestovať autobusom", "Zavolaj mi alebo mi napíš správu",
        "Ponáhľaj sa, alebo zmeškáme vlak", "Prídeš večer, alebo nie",
        "Pôjdeme pešo, alebo vezmeme taxík", "Koncert je zaujímavý, ale lístky sú drahé",
        "Kúpime lístky online alebo pri pokladni", "Môžeme sa stretnúť v centre alebo pri stanici",
    ]
    assert sum(example in full_text for example in examples) >= 24, "Fewer than 24 expected Slovak examples were found"

    assert "Упражнен" not in texts[0]
    assert "Ответы" not in "\n".join(texts[:6])
    for page_number in range(1, 8):
        assert f"стр. {page_number} / 7" in texts[page_number - 1], f"Missing page number on page {page_number}"
    for bad in ["�", "□", "TODO", "PLACEHOLDER"]:
        assert bad not in full_text, f"Forbidden or broken text found: {bad}"
    assert not re.search(r"[\u2010-\u2014]", full_text), "Non-ASCII dash found"
    assert "povedal, že" not in full_text.lower(), "Later topic 5.3 was pulled in"

    info = subprocess.run(
        [str(PDFINFO), str(PDF)], check=True, capture_output=True, text=True,
        encoding="utf-8", errors="replace",
    ).stdout
    assert "Pages:           7" in info
    assert "Page size:       595.276 x 841.89 pts (A4)" in info
    assert "PDF syntax error" not in info
    print("A2 PDF 5.1 verified")
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
    print("A2 PDF 5.1 renders verified")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-renders", action="store_true")
    args = parser.parse_args()
    verify_pdf()
    if args.check_renders:
        verify_renders()
