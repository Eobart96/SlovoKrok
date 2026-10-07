import argparse
import re
import subprocess
from pathlib import Path

import pdfplumber
from PIL import Image
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "output" / "pdf" / "A2" / "Module_05" / "Slovak_A2_Tema_5_5_Pridatochnye_s_kto_co_i_kde.pdf"
RENDERS = ROOT / "tmp" / "pdfs" / "a2_5_5_final"
PDFINFO = Path(r"C:\Users\Eobar\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\poppler\Library\bin\pdfinfo.exe")


def verify_pdf():
    assert PDF.exists(), f"Missing PDF: {PDF}"
    assert PDF.stat().st_size > 50_000, "PDF is unexpectedly small"
    reader = PdfReader(str(PDF))
    assert len(reader.pages) == 7, f"Expected 7 pages, got {len(reader.pages)}"
    assert reader.metadata.title == "Slovak A2 - Тема 5.5 - Придаточные с kto, čo и kde"

    with pdfplumber.open(PDF) as document:
        texts = [(page.extract_text() or "") for page in document.pages]
        for index, page in enumerate(document.pages, start=1):
            assert abs(page.width - 595.276) < 1, f"Page {index}: wrong width"
            assert abs(page.height - 841.890) < 1, f"Page {index}: wrong height"
            assert len(texts[index - 1].strip()) > 250, f"Page {index}: too little extractable text"

    full_text = "\n".join(texts)
    required = [
        "Придаточные с", "Nepriame otázky", "Прямой вопрос и придаточная часть",
        "Знак в конце выбираем по главной части", "Kto и čo: человек или информация",
        "Kto или ktorý?", "Kde: неизвестное место", "Порядок слов",
        "Модель общения: первый день на курсе", "Упражнение 1", "Упражнение 6",
        "Ответы", "Финальная проверка", "lebo, pretože", "preto",
    ]
    for phrase in required:
        assert phrase in full_text, f"Missing phrase: {phrase}"

    examples = [
        "Viem, kto tam pracuje", "Povedz mi, kto volal", "Neviem, čo potrebuješ",
        "Vysvetli, čo sa stalo", "Ukáž mi, kde je vchod", "Vieš, kde býva Eva",
        "Viem, kde býva", "Vieš, kde býva", "Neviem, kto otvoril okno",
        "Zistíme, kto príde", "Povedz, čo sa stalo", "Vidím, čo robíš",
        "Napíš, čo potrebuješ", "Vysvetli, čo je to", "Neviem, kto tam pracuje",
        "Poznám človeka, ktorý tam pracuje", "Neviem, kde sú moje kľúče",
        "Ukáž mi, kde je recepcia", "Povedz mi, kde máme čakať",
        "Pamätám si, kde sme sa stretli", "Zistím, kde sa koná kurz",
        "Vieš, kde je najbližšia lekáreň", "Vieš, kde je stanica",
        "Povedz, kde býva Peter", "Ukáž mi, kde sa začína cesta",
        "Neviem, kto má zoznam", "Povedz mi, čo máme priniesť",
        "Ukáž mi, kde si môžem sadnúť", "Vieš, kto nám môže pomôcť",
        "Pamätáš si, čo povedal lektor", "Zistíme, kde bude stretnutie",
    ]
    assert sum(example in full_text for example in examples) >= 28, "Fewer than 28 expected Slovak examples were found"

    assert "Упражнен" not in texts[0]
    assert "Ответы" not in "\n".join(texts[:6])
    for page_number in range(1, 8):
        assert f"стр. {page_number} / 7" in texts[page_number - 1], f"Missing page number on page {page_number}"
    for bad in ["�", "□", "TODO", "PLACEHOLDER"]:
        assert bad not in full_text, f"Forbidden or broken text found: {bad}"
    assert not re.search(r"[\u2010-\u2014]", full_text), "Non-ASCII dash found"
    assert "потому что" not in full_text.lower(), "Topic 5.6 cause explanation was pulled in"
    assert "следовательно" not in full_text.lower(), "Topic 5.6 consequence explanation was pulled in"

    info = subprocess.run(
        [str(PDFINFO), str(PDF)], check=True, capture_output=True, text=True,
        encoding="utf-8", errors="replace",
    ).stdout
    assert "Pages:           7" in info
    assert "Page size:       595.276 x 841.89 pts (A4)" in info
    assert "PDF syntax error" not in info
    print("A2 PDF 5.5 verified")
    print(f"pages={len(reader.pages)} size={PDF.stat().st_size} chars={len(full_text)} examples>=28")


def verify_renders():
    images = sorted(RENDERS.glob("page-*.png"))
    assert len(images) == 7, f"Expected 7 rendered pages, got {len(images)}"
    for index, image_path in enumerate(images, start=1):
        assert image_path.stat().st_size > 30_000, f"Render {index} is unexpectedly small"
        with Image.open(image_path) as image:
            assert image.width >= 1200 and image.height >= 1700, f"Render {index} has low resolution"
            extrema = image.convert("L").getextrema()
            assert extrema[0] < 245 and extrema[1] > 250, f"Render {index} appears blank"
    print("A2 PDF 5.5 renders verified")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-renders", action="store_true")
    args = parser.parse_args()
    verify_pdf()
    if args.check_renders:
        verify_renders()
