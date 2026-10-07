import argparse
import re
import subprocess
from pathlib import Path

import pdfplumber
from PIL import Image
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "output" / "pdf" / "A2" / "Module_03" / "Slovak_A2_Tema_3_6_Prityazhatelnye_slova_i_svoj.pdf"
RENDERS = ROOT / "tmp" / "pdfs" / "a2_3_6_final"
PDFINFO = Path(r"C:\Users\Eobar\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\poppler\Library\bin\pdfinfo.exe")


def verify_pdf():
    assert PDF.exists(), f"Missing PDF: {PDF}"
    assert PDF.stat().st_size > 50_000, "PDF is unexpectedly small"
    reader = PdfReader(str(PDF))
    assert len(reader.pages) == 7, f"Expected 7 pages, got {len(reader.pages)}"
    assert reader.metadata.title == "Slovak A2 - Тема 3.6 - Притяжательные слова и местоимение svoj"

    with pdfplumber.open(PDF) as document:
        texts = [(page.extract_text() or "") for page in document.pages]
        for index, page in enumerate(document.pages, start=1):
            assert abs(page.width - 595.276) < 1, f"Page {index}: wrong width"
            assert abs(page.height - 841.890) < 1, f"Page {index}: wrong height"
            assert len(texts[index - 1].strip()) > 250, f"Page {index}: too little extractable text"

    full_text = "\n".join(texts)
    required = [
        "Притяжательные слова", "Privlastňovacie zámená a zámeno svoj",
        "môj/tvoj/jeho/jej/náš/váš/ich", "svoj", "čí? čia? čie?",
        "môj, tvoj, náš, váš, svoj", "jeho, jej, ich", "Svoj или jeho/jej/ich?",
        "Peter hľadá svoj telefón", "Peter hľadá jeho telefón",
        "svojho", "svojej", "svojím", "svojich", "svojimi",
        "Мини-диалог", "Упражнения 1-3", "Упражнения 4-6", "Ответы", "Финальная проверка",
    ]
    for phrase in required:
        assert phrase in full_text, f"Missing phrase: {phrase}"

    examples = [
        "Kontrolujem svoju rezerváciu", "Vezmi si svoj pas", "Peter hľadá svoj telefón",
        "Eva volá svojej sestre", "Chránime svoje údaje", "Skontrolujte svoju adresu",
        "Deti upratali svoju izbu", "Peter hľadá jeho telefón", "Anna číta svoj list",
        "Anna číta jej list", "Ukážem Eve jej izbu", "Mám tvoje kľúče", "To je môj byt",
        "Jeho brat pracuje doma", "Naša krajina je krásna", "Môj kolega pozná tvoju sestru",
        "Jej syn študuje v našom meste", "Ich deti sa hrajú s našimi deťmi",
        "Pošlem vám našu novú adresu", "Eva si zapisuje svoje heslo",
        "O svojom pláne zatiaľ nehovorím", "Peter cestuje so svojou dcérou",
        "Stretli sme sa s jeho kolegami", "Máš svoj pas", "svoje lístky",
        "tvojej taške", "Jana má moju tašku", "dala lístky do svojho kufra",
    ]
    assert sum(example in full_text for example in examples) >= 25, "Fewer than 25 expected Slovak examples were found"

    assert "Упражнен" not in texts[0]
    assert "Ответы" not in "\n".join(texts[:6])
    for page_number in range(1, 8):
        assert f"стр. {page_number} / 7" in texts[page_number - 1], f"Missing page number on page {page_number}"
    for bad in ["�", "□", "TODO", "PLACEHOLDER"]:
        assert bad not in full_text, f"Forbidden or broken text found: {bad}"
    assert not re.search(r"[\u2010-\u2014]", full_text), "Non-ASCII dash found"
    assert "otcov" not in full_text.lower() and "matkin" not in full_text.lower(), "Later adjective lesson was pulled into this PDF"

    info = subprocess.run(
        [str(PDFINFO), str(PDF)], check=True, capture_output=True, text=True,
        encoding="utf-8", errors="replace",
    ).stdout
    assert "Pages:           7" in info
    assert "Page size:       595.276 x 841.89 pts (A4)" in info
    assert "PDF syntax error" not in info
    print("A2 PDF 3.6 verified")
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
    print("A2 PDF 3.6 renders verified")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-renders", action="store_true")
    args = parser.parse_args()
    verify_pdf()
    if args.check_renders:
        verify_renders()
