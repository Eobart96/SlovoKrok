import argparse
import re
import subprocess
from pathlib import Path

import pdfplumber
from PIL import Image
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "output" / "pdf" / "A2" / "Module_02" / "Slovak_A2_Tema_2_11_Gde_kuda_i_otkuda_padezhnye_triady.pdf"
RENDERS = ROOT / "tmp" / "pdfs" / "a2_2_11_final"
PDFINFO = Path(r"C:\Users\Eobar\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\poppler\Library\bin\pdfinfo.exe")


def verify_pdf():
    assert PDF.exists(), f"Missing PDF: {PDF}"
    assert PDF.stat().st_size > 50_000, "PDF is unexpectedly small"
    reader = PdfReader(str(PDF))
    assert len(reader.pages) == 7, f"Expected 7 pages, got {len(reader.pages)}"
    assert reader.metadata.title == "Slovak A2 - Тема 2.11 - Где, куда и откуда: падежные триады"

    with pdfplumber.open(PDF) as document:
        texts = [(page.extract_text() or "") for page in document.pages]
        for index, page in enumerate(document.pages, start=1):
            assert abs(page.width - 595.276) < 1, f"Page {index}: wrong width"
            assert abs(page.height - 841.890) < 1, f"Page {index}: wrong height"
            assert len(texts[index - 1].strip()) > 250, f"Page {index}: too little extractable text"

    full_text = "\n".join(texts)
    required = [
        "Где, куда и откуда", "падежные триады", "Kde, kam a odkiaľ", "v/vo и na + L",
        "do + G, na + A, k + D", "z/zo + G", "kde? v/na + L", "kam? do + G или na + A",
        "odkiaľ? z/zo + G", "v škole", "do školy", "zo školy", "na pošte", "na poštu",
        "z pošty", "k lekárovi", "od lekára", "Som doma", "Idem domov", "Idem z domu",
        "Упражнение 1", "Упражнение 6", "Ответы", "Финальная проверка", "теме 2.12",
    ]
    for phrase in required:
        assert phrase in full_text, f"Missing phrase: {phrase}"

    examples = [
        "Som v kancelárii", "Čakám na námestí", "Bývame na Slovensku", "Idem do nemocnice",
        "Idem k lekárovi", "Vošla do domu", "Prišla k domu", "Ideme k susedovi",
        "Idem do práce", "Prišla na stretnutie", "Vošiel do izby", "Vrátime sa do hotela",
        "Vychádzam z obchodu", "Vrátili sa z Bratislavy", "Prišla zo Slovenska",
        "Ideme z koncertu", "Volám ti z pošty", "Sme v hoteli", "Ideme do hotela",
        "Odchádzame z hotela", "Je na letisku", "Ide na letisko", "Vracia sa z letiska",
        "Čaká u lekára", "Ide od lekára", "Dnes idem do práce", "Každý deň chodím do práce",
        "Prišli sme na stanicu", "Vošla do banky", "odchádzam z kancelárie", "vrátim domov",
    ]
    assert sum(example in full_text for example in examples) >= 27, "Fewer than 27 expected Slovak examples were found"

    assert "Упражнение" not in texts[0]
    assert "Ответы" not in "\n".join(texts[:6])
    for page_number in range(1, 8):
        assert f"стр. {page_number} / 7" in texts[page_number - 1], f"Missing page number on page {page_number}"
    for bad in ["�", "□", "TODO", "PLACEHOLDER"]:
        assert bad not in full_text, f"Forbidden or broken text found: {bad}"
    assert not re.search(r"[\u2010-\u2014]", full_text), "Non-ASCII dash found"
    assert "обращение" not in "\n".join(texts[:6]).lower(), "Topic 2.12 leaked into the lesson body"
    assert "средство, совместность" not in full_text.lower(), "Topic 2.10 leaked into this PDF"

    info = subprocess.run(
        [str(PDFINFO), str(PDF)], check=True, capture_output=True, text=True,
        encoding="utf-8", errors="replace",
    ).stdout
    assert "Pages:           7" in info
    assert "Page size:       595.276 x 841.89 pts (A4)" in info
    assert "PDF syntax error" not in info
    print("A2 PDF 2.11 verified")
    print(f"pages={len(reader.pages)} size={PDF.stat().st_size} chars={len(full_text)} examples>=27")


def verify_renders():
    images = sorted(RENDERS.glob("page-*.png"))
    assert len(images) == 7, f"Expected 7 rendered pages, got {len(images)}"
    for index, image_path in enumerate(images, start=1):
        assert image_path.stat().st_size > 30_000, f"Render {index} is unexpectedly small"
        with Image.open(image_path) as image:
            assert image.width >= 1200 and image.height >= 1700, f"Render {index} has low resolution"
            extrema = image.convert("L").getextrema()
            assert extrema[0] < 245 and extrema[1] > 250, f"Render {index} appears blank"
    print("A2 PDF 2.11 renders verified")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-renders", action="store_true")
    args = parser.parse_args()
    verify_pdf()
    if args.check_renders:
        verify_renders()
