import argparse
from pathlib import Path

import pdfplumber
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "output" / "pdf" / "A2" / "Module_01" / "Slovak_A2_Tema_1_4_Semji_slov.pdf"


def extract():
    reader = PdfReader(PDF)
    with pdfplumber.open(PDF) as pdf:
        page_texts = [(page.extract_text() or "").strip() for page in pdf.pages]
        sizes = [(page.width, page.height) for page in pdf.pages]
    return reader, page_texts, sizes


def verify_structure(reader, page_texts, sizes):
    assert len(reader.pages) == 7, f"expected 7 pages, got {len(reader.pages)}"
    assert not reader.is_encrypted
    assert "/AcroForm" not in reader.trailer["/Root"]
    assert all(abs(width - 595.276) < 1 and abs(height - 841.89) < 1 for width, height in sizes)
    assert all(len(text) > 250 for text in page_texts), [len(text) for text in page_texts]
    print("A2 PDF 1.4 structure verified")


def verify_content(page_texts):
    text = "\n".join(page_texts)
    required = [
        "Семьи слов", "Что такое семья слов", "Названия людей и женские формы",
        "Действие, качество и признак", "Прозрачные семьи и предел догадки",
        "-anie / -enie", "-osť", "-ný", "-ový", "ne-",
        "Упражнение 6", "Ответы", "Финальная проверка",
    ]
    assert all(item in text for item in required), [item for item in required if item not in text]
    examples = [
        "pracovať", "pracovník", "pracovný", "učiteľka", "kolegyňa",
        "cestovanie", "cestovateľ", "zdravotný", "bezpečnosť", "nespokojnosť",
        "informovať", "informačný", "organizovať", "organizačný", "komunikovať",
        "rezervovať", "rezervačný", "kontrolovať", "kontrolný", "rýchlosť",
    ]
    assert all(example in text for example in examples)
    assert text.count("Упражнение ") >= 6
    rejected = ["род, число и модели основ", "TODO", "PLACEHOLDER"]
    assert not any(item.lower() in text.lower() for item in rejected)
    print("A2 PDF 1.4 learning content verified")


def main():
    parser = argparse.ArgumentParser()
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--structure", action="store_true")
    modes.add_argument("--content", action="store_true")
    args = parser.parse_args()
    reader, page_texts, sizes = extract()
    if args.structure:
        verify_structure(reader, page_texts, sizes)
    else:
        verify_content(page_texts)


if __name__ == "__main__":
    main()
