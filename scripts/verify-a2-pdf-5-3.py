import argparse
import re
import subprocess
from pathlib import Path

import pdfplumber
from PIL import Image
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "output" / "pdf" / "A2" / "Module_05" / "Slovak_A2_Tema_5_3_Peredaem_soobshchenie_s_ze.pdf"
RENDERS = ROOT / "tmp" / "pdfs" / "a2_5_3_final"
PDFINFO = Path(r"C:\Users\Eobar\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\poppler\Library\bin\pdfinfo.exe")


def verify_pdf():
    assert PDF.exists(), f"Missing PDF: {PDF}"
    assert PDF.stat().st_size > 50_000, "PDF is unexpectedly small"
    reader = PdfReader(str(PDF))
    assert len(reader.pages) == 7, f"Expected 7 pages, got {len(reader.pages)}"
    assert reader.metadata.title == "Slovak A2 - Тема 5.3 - Передаём сообщение с že"

    with pdfplumber.open(PDF) as document:
        texts = [(page.extract_text() or "") for page in document.pages]
        for index, page in enumerate(document.pages, start=1):
            assert abs(page.width - 595.276) < 1, f"Page {index}: wrong width"
            assert abs(page.height - 841.890) < 1, f"Page {index}: wrong height"
            assert len(texts[index - 1].strip()) > 250, f"Page {index}: too little extractable text"

    full_text = "\n".join(texts)
    required = [
        "Передаём сообщение", "Nepriama správa", "Базовая модель: кто сообщает и что",
        "Запятая ставится перед že", "Меняем лицо и точку зрения",
        "Короткие местоимения после že", "Время выбираем по смыслу",
        "Слова времени и места", "Мнение, надежда и простая просьба",
        "Мини-диалог: передаём сообщение коллеге", "Медиация в одном сообщении",
        "Упражнение 1", "Упражнение 6", "Ответы", "Финальная проверка", "ktorý",
    ]
    for phrase in required:
        assert phrase in full_text, f"Missing phrase: {phrase}"

    examples = [
        "Peter povedal, že príde večer", "Anna napísala, že je doma",
        "Oznámili, že vlak mešká", "Viem, že obchod je zatvorený",
        "Počul som, že susedia sa sťahujú", "Mária povedala, že nemá čas",
        "Dúfam, že sa čoskoro uvidíme", "Verím, že to zvládneš",
        "Mária povedala, že je unavená", "Peter povedal, že má čas",
        "Povedali sme, že prídeme o šiestej", "Jana povedala Petrovi, že mu zavolá",
        "Marek povedal, že jeho sestra býva v Nitre", "Povedala, že mi zavolá",
        "Napísal, že sa vráti neskôr", "Oznámili, že nám pošlú nový termín",
        "Povedal, že pracuje doma", "Povedal, že včera pracoval doma",
        "Povedal, že zajtra bude pracovať doma", "Učiteľ povedal, že voda vrie pri 100 °C",
        "Mária napísala, že príde v piatok", "Myslím si, že tento plán je dobrý",
        "Dúfam, že zajtra nebude pršať", "Verím, že skúšku zvládneš",
        "Nemyslím si, že je to pravda", "Mama povedala, že mám kúpiť chlieb",
        "Povedala, že jej máme poslať adresu", "Myslí si, že stretnutie potrvá asi hodinu",
    ]
    assert sum(example in full_text for example in examples) >= 26, "Fewer than 26 expected Slovak examples were found"

    assert "Упражнен" not in texts[0]
    assert "Ответы" not in "\n".join(texts[:6])
    for page_number in range(1, 8):
        assert f"стр. {page_number} / 7" in texts[page_number - 1], f"Missing page number on page {page_number}"
    for bad in ["�", "□", "TODO", "PLACEHOLDER"]:
        assert bad not in full_text, f"Forbidden or broken text found: {bad}"
    assert not re.search(r"[\u2010-\u2014]", full_text), "Non-ASCII dash found"
    assert "ktorého" not in full_text.lower(), "Later relative-pronoun lesson was pulled in"

    info = subprocess.run(
        [str(PDFINFO), str(PDF)], check=True, capture_output=True, text=True,
        encoding="utf-8", errors="replace",
    ).stdout
    assert "Pages:           7" in info
    assert "Page size:       595.276 x 841.89 pts (A4)" in info
    assert "PDF syntax error" not in info
    print("A2 PDF 5.3 verified")
    print(f"pages={len(reader.pages)} size={PDF.stat().st_size} chars={len(full_text)} examples>=26")


def verify_renders():
    images = sorted(RENDERS.glob("page-*.png"))
    assert len(images) == 7, f"Expected 7 rendered pages, got {len(images)}"
    for index, image_path in enumerate(images, start=1):
        assert image_path.stat().st_size > 30_000, f"Render {index} is unexpectedly small"
        with Image.open(image_path) as image:
            assert image.width >= 1200 and image.height >= 1700, f"Render {index} has low resolution"
            extrema = image.convert("L").getextrema()
            assert extrema[0] < 245 and extrema[1] > 250, f"Render {index} appears blank"
    print("A2 PDF 5.3 renders verified")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-renders", action="store_true")
    args = parser.parse_args()
    verify_pdf()
    if args.check_renders:
        verify_renders()
