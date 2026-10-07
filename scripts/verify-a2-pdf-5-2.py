import argparse
import re
import subprocess
from pathlib import Path

import pdfplumber
from PIL import Image
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "output" / "pdf" / "A2" / "Module_05" / "Slovak_A2_Tema_5_2_Parnye_soyuzy_aj_aj_i_ani_ani.pdf"
RENDERS = ROOT / "tmp" / "pdfs" / "a2_5_2_final"
PDFINFO = Path(r"C:\Users\Eobar\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\poppler\Library\bin\pdfinfo.exe")


def verify_pdf():
    assert PDF.exists(), f"Missing PDF: {PDF}"
    assert PDF.stat().st_size > 50_000, "PDF is unexpectedly small"
    reader = PdfReader(str(PDF))
    assert len(reader.pages) == 7, f"Expected 7 pages, got {len(reader.pages)}"
    assert reader.metadata.title == "Slovak A2 - Тема 5.2 - Парные союзы aj - aj и ani - ani"

    with pdfplumber.open(PDF) as document:
        texts = [(page.extract_text() or "") for page in document.pages]
        for index, page in enumerate(document.pages, start=1):
            assert abs(page.width - 595.276) < 1, f"Page {index}: wrong width"
            assert abs(page.height - 841.890) < 1, f"Page {index}: wrong height"
            assert len(texts[index - 1].strip()) > 250, f"Page {index}: too little extractable text"

    full_text = "\n".join(texts)
    required = [
        "Парные союзы", "aj - aj и ani - ani", "Aj - aj: включаем оба элемента",
        "Сильнее, чем простое a", "Ani - ani: исключаем оба элемента",
        "Отрицание видно в сказуемом", "Симметрия, падеж и согласование",
        "Два подлежащих - множественное число", "Запятая перед второй частью",
        "Мини-диалог: выбираем курс", "Упражнение 1", "Упражнение 6", "Ответы",
        "Финальная проверка", "передаче сообщения с союзом že",
    ]
    for phrase in required:
        assert phrase in full_text, f"Missing phrase: {phrase}"

    examples = [
        "Aj Anna, aj Peter pracujú doma", "Kúpila som aj chlieb, aj mlieko",
        "Kurz je aj praktický, aj zaujímavý", "Aj čítam knihy, aj počúvam podcasty",
        "Stretli sme sa aj v pondelok, aj v stredu", "Anna a Peter prišli",
        "Aj Anna, aj Peter prišli", "Kúpim aj ovocie, aj zeleninu",
        "Hovoríme aj o práci, aj o škole", "Ani Anna, ani Peter dnes nepracujú",
        "Nechcem ani čaj, ani kávu", "Nemám ani čas, ani energiu",
        "Neboli sme ani v múzeu, ani v galérii", "Ani mi nezavolal, ani mi nenapísal",
        "Ani Peter, ani Jana neprišli", "Ani neprší, ani nesneží",
        "Ani nevarím, ani nepečiem", "Pomáham aj bratovi, aj sestre",
        "Hovorím aj s kolegom, aj s kolegyňou", "Čítam aj o meste, aj o jeho histórii",
        "Ideme aj do banky, aj do obchodu", "Nemám čas ani na šport, ani na oddych",
        "Aj mama, aj otec prišli", "Pozná aj Bratislavu, aj Košice",
        "Kúpil aj chlieb, aj syr, aj ovocie", "Na výlet môžu ísť aj dospelí, aj deti",
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
    print("A2 PDF 5.2 verified")
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
    print("A2 PDF 5.2 renders verified")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-renders", action="store_true")
    args = parser.parse_args()
    verify_pdf()
    if args.check_renders:
        verify_renders()
