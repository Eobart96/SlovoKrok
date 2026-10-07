import argparse
import re
import subprocess
from pathlib import Path

import pdfplumber
from PIL import Image
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "output" / "pdf" / "A2" / "Module_02" / "Slovak_A2_Tema_2_10_Instrumental_sredstvo_sovmestnost_i_harakteristika.pdf"
RENDERS = ROOT / "tmp" / "pdfs" / "a2_2_10_final"
PDFINFO = Path(r"C:\Users\Eobar\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\poppler\Library\bin\pdfinfo.exe")


def verify_pdf():
    assert PDF.exists(), f"Missing PDF: {PDF}"
    assert PDF.stat().st_size > 50_000, "PDF is unexpectedly small"

    reader = PdfReader(str(PDF))
    assert len(reader.pages) == 7, f"Expected 7 pages, got {len(reader.pages)}"
    assert reader.metadata.title == "Slovak A2 - Тема 2.10 - Inštrumentál: средство, совместность и характеристика"

    with pdfplumber.open(PDF) as document:
        texts = [(page.extract_text() or "") for page in document.pages]
        for index, page in enumerate(document.pages, start=1):
            assert abs(page.width - 595.276) < 1, f"Page {index}: wrong width"
            assert abs(page.height - 841.890) < 1, f"Page {index}: wrong height"
            assert len(texts[index - 1].strip()) > 250, f"Page {index}: too little extractable text"

    full_text = "\n".join(texts)
    required = [
        "Inštrumentál: средство, совместность", "prostriedok, sprievod a charakteristika",
        "Píšem perom", "Idem s kolegom", "Stal sa lekárom", "brat → bratom",
        "kolega → kolegom", "žena → ženou", "sestra → sestrou", "kolegyňa → kolegyňou",
        "mesto → mestom", "auto → autom", "námestie → námestím", "dieťa → dieťaťom", "s mojím dobrým kolegom",
        "s mojou dobrou kolegyňou", "Platím kartou", "Cestujem vlakom",
        "so sestrou", "so šéfom", "so mnou", "s tebou", "s ním", "s ňou",
        "s nami", "s vami", "s nimi", "pred", "za", "medzi", "nad", "pod",
        "Auto je pred domom", "Záhrada je za školou", "Kaviareň je medzi bankou a poštou",
        "Lampa je nad stolom", "Taška je pod stoličkou", "s dobrými kolegami",
        "s novými učiteľmi", "vlakmi / autami", "s ľuďmi / s deťmi",
        "Som lekár", "Je skúseným lekárom", "Stala sa učiteľkou",
        "Pracujem ako programátor", "Мини-диалог", "Упражнение 1", "Упражнение 6",
        "Ответы", "Финальная проверка", "теме 2.11",
    ]
    for phrase in required:
        assert phrase in full_text, f"Missing phrase: {phrase}"

    examples = [
        "Píšem perom", "Idem s kolegom", "Stal sa lekárom", "Platím kartou",
        "Cestujem vlakom", "Idem s kamarátom", "Otvorím to kľúčom", "Otvorím to s kolegom",
        "Pôjdeš so mnou", "Hovorím s ním a s ňou", "Zostanú s nami", "Stretávam sa s nimi",
        "Auto je pred domom", "Záhrada je za školou", "Kaviareň je medzi bankou a poštou",
        "Lampa je nad stolom", "Taška je pod stoličkou", "Pracujem s dobrými kolegami",
        "Rozprávam sa s novými učiteľmi", "Park je medzi starými domami",
        "Cestujeme vlakmi a autami", "Pracuje s ľuďmi a s deťmi", "Učiteľ stojí pred malými deťmi", "Som lekár",
        "Je skúseným lekárom", "Stala sa učiteľkou", "Pracujem ako programátor",
        "Väčšinou vlakom", "dnes s kolegyňou", "Pracujem ako technik",
    ]
    assert sum(example in full_text for example in examples) >= 25, "Fewer than 25 expected Slovak examples were found"

    for page_number in range(1, 8):
        assert f"стр. {page_number} / 7" in texts[page_number - 1], f"Missing page number on page {page_number}"

    for bad in ["�", "□", "–", "—", "TODO", "PLACEHOLDER"]:
        assert bad not in full_text, f"Forbidden or broken text found: {bad}"
    assert not re.search(r"[\u2010-\u2014]", full_text), "Non-ASCII dash found"
    assert "do/na + G/A" not in full_text, "Later case-triad lesson was pulled into this PDF"

    info = subprocess.run(
        [str(PDFINFO), str(PDF)], check=True, capture_output=True, text=True,
        encoding="utf-8", errors="replace",
    ).stdout
    assert "Pages:           7" in info
    assert "Page size:       595.276 x 841.89 pts (A4)" in info
    assert "PDF syntax error" not in info

    print("A2 PDF 2.10 verified")
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
    print("A2 PDF 2.10 renders verified")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-renders", action="store_true")
    args = parser.parse_args()
    verify_pdf()
    if args.check_renders:
        verify_renders()
