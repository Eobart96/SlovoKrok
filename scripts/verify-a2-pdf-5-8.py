import argparse,re,subprocess
from pathlib import Path
import pdfplumber
from PIL import Image
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parents[1]
PDF=ROOT/"output/pdf/A2/Module_05/Slovak_A2_Tema_5_8_Svyaznyi_rasskaz_i_aktualnoe_chlenenie.pdf"
RENDERS=ROOT/"tmp/pdfs/a2_5_8_final"
PDFINFO=Path(r"C:\Users\Eobar\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\poppler\Library\bin\pdfinfo.exe")
def verify_pdf():
 assert PDF.exists() and PDF.stat().st_size>50000
 reader=PdfReader(str(PDF)); assert len(reader.pages)==7; assert reader.metadata.title=="Slovak A2 - Тема 5.8 - Связный рассказ и актуальное членение"
 with pdfplumber.open(PDF) as d:
  texts=[p.extract_text() or "" for p in d.pages]
  for i,page in enumerate(d.pages,1): assert abs(page.width-595.276)<1 and abs(page.height-841.890)<1 and len(texts[i-1].strip())>250
 full="\n".join(texts)
 for s in ["Связный рассказ и", "Каркас короткого рассказа", "Известное ведёт к новому", "Нейтральный и выделенный порядок слов", "Модель: поездка к озеру", "Почему текст связный", "Упражнение 1", "Упражнение 6", "Ответы", "Финальная проверка", "Модуль 5 завершён"]: assert s in full,s
 examples=["Najprv sme si kúpili lístky","Potom sme nastúpili do vlaku","Neskôr sme sa zastavili v centre","Nakoniec sme sa vrátili domov","Minulú sobotu sme išli na výlet","Potom sme navštívili starý hrad","Nakoniec sme boli unavení, ale spokojní","Prišla Zuzana","Zuzana priniesla koláč","Koláč bol výborný","Na stanici čakala Lucia","Lucia mala veľký kufor","V kufri boli darčeky","Darčeky dostali deti","Zavolala Lucia","Lucia zavolala Martinovi","Zavolala mu večer","Peter kúpil nové auto","V SOBOTU sme išli na výlet","Knihu som kúpil JA","PETRA som stretol","Na výlet sme išli VLAKOM","Minulú sobotu sme išli k jazeru","Lucia priniesla mapu a malé občerstvenie","Vo vlaku sme naplánovali trasu","Nakoniec sme prišli k jazeru","Najkrajší bol pokoj pri vode","Všetko sa začalo ráno","O chvíľu sme pokračovali ďalej","Potom sa stalo niečo nečakané","Nakoniec všetko dobre dopadlo"]
 assert sum(x in full for x in examples)>=29
 assert "Ответы" not in "\n".join(texts[:6])
 for n in range(1,8): assert f"стр. {n} / 7" in texts[n-1]
 for bad in ["�","□","TODO","PLACEHOLDER"]: assert bad not in full
 assert not re.search(r"[\u2010-\u2014]",full)
 for required in ["najprv","potom","neskôr","nakoniec"]: assert full.lower().count(required)>=6
 info=subprocess.run([str(PDFINFO),str(PDF)],check=True,capture_output=True,text=True,encoding="utf-8",errors="replace").stdout
 assert "Pages:           7" in info and "Page size:       595.276 x 841.89 pts (A4)" in info
 print("A2 PDF 5.8 verified"); print(f"pages=7 size={PDF.stat().st_size} chars={len(full)} examples>=29")
def verify_renders():
 imgs=sorted(RENDERS.glob("page-*.png")); assert len(imgs)==7
 for f in imgs:
  assert f.stat().st_size>30000
  with Image.open(f) as im: assert im.width>=1200 and im.height>=1700 and im.convert("L").getextrema()[0]<245
 print("A2 PDF 5.8 renders verified")
if __name__=="__main__":
 a=argparse.ArgumentParser(); a.add_argument("--check-renders",action="store_true"); x=a.parse_args(); verify_pdf(); verify_renders() if x.check_renders else None
