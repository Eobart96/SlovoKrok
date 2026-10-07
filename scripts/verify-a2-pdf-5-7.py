import argparse,re,subprocess
from pathlib import Path
import pdfplumber
from PIL import Image
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parents[1]
PDF=ROOT/"output/pdf/A2/Module_05/Slovak_A2_Tema_5_7_Vremya_i_realnoe_uslovie.pdf"
RENDERS=ROOT/"tmp/pdfs/a2_5_7_final"
PDFINFO=Path(r"C:\Users\Eobar\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\poppler\Library\bin\pdfinfo.exe")
def verify_pdf():
 assert PDF.exists() and PDF.stat().st_size>50000
 reader=PdfReader(str(PDF)); assert len(reader.pages)==7; assert reader.metadata.title=="Slovak A2 - Тема 5.7 - Время и реальное условие"
 with pdfplumber.open(PDF) as d:
  texts=[p.extract_text() or "" for p in d.pages]
  for i,p in enumerate(d.pages,1): assert abs(p.width-595.276)<1 and abs(p.height-841.890)<1 and len(texts[i-1].strip())>250
 full="\n".join(texts)
 for s in ["Время и","Kedy спрашивает, keď связывает","Главный контраст","Ak вводит реальное условие","Ak или keď?","Настоящее и будущее в условии","Порядок частей и запятая","Модель общения: план на выходные","Упражнение 1","Упражнение 6","Ответы","Финальная проверка","najprv, potom, neskôr, nakoniec"]: assert s in full,s
 examples=["Kedy prídeš","Neviem, kedy prídeš","Keď som prišiel, Eva už čakala","Keď prší, zostávam doma","Keď prídem domov, zavolám ti","Kedy sa začína kurz","Keď sa kurz začne, pošlem ti správu","Povedz mi, kedy odchádza vlak","Keď vlak odíde, zavolám taxík","Ak budem mať čas, prídem","Ak skončíš skôr, zavolaj mi","Ak bude pršať, zostaneme doma","Ak je obchod otvorený, kúpime chlieb","Ak nerozumieš, opýtaj sa","Ak príde Peter, začneme","Keď príde Peter, začneme","Keď mám čas, chodím plávať","Ak mám čas, cvičím","Ak budem mať čas, budem cvičiť","Ak skončím, zavolám ti","Keď prídem, napíšem ti","Keď som prišiel, zavolal som","Ak bude pekne, pôjdeme na výlet","Keď skončím prácu, oddýchnem si","Neviem, kedy sa vráti","Keď sa vráti, porozprávame sa","Ak sa vráti skoro, pôjdeme spolu","Ak budeš potrebovať pomoc, zavolaj","Keď budem doma, pošlem ti adresu"]
 assert sum(x in full for x in examples)>=27
 assert "Ответы" not in "\n".join(texts[:6])
 for n in range(1,8): assert f"стр. {n} / 7" in texts[n-1]
 for bad in ["�","□","TODO","PLACEHOLDER"]: assert bad not in full
 assert not re.search(r"[\u2010-\u2014]",full); assert "Keby" not in full and "keby" not in full
 info=subprocess.run([str(PDFINFO),str(PDF)],check=True,capture_output=True,text=True,encoding="utf-8",errors="replace").stdout
 assert "Pages:           7" in info and "Page size:       595.276 x 841.89 pts (A4)" in info
 print("A2 PDF 5.7 verified"); print(f"pages=7 size={PDF.stat().st_size} chars={len(full)} examples>=27")
def verify_renders():
 imgs=sorted(RENDERS.glob("page-*.png")); assert len(imgs)==7
 for f in imgs:
  assert f.stat().st_size>30000
  with Image.open(f) as im: assert im.width>=1200 and im.height>=1700 and im.convert("L").getextrema()[0]<245
 print("A2 PDF 5.7 renders verified")
if __name__=="__main__":
 a=argparse.ArgumentParser(); a.add_argument("--check-renders",action="store_true"); x=a.parse_args(); verify_pdf(); verify_renders() if x.check_renders else None
