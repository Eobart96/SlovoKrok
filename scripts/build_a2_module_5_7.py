from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import BaseDocTemplate, Frame, PageBreak, PageTemplate, Paragraph, Spacer, Table, TableStyle

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output/pdf/A2/Module_05/Slovak_A2_Tema_5_7_Vremya_i_realnoe_uslovie.pdf"
OUTPUT.parent.mkdir(parents=True, exist_ok=True)
PLUM, PINK = colors.HexColor("#7B245F"), colors.HexColor("#CE3C92")
PALE, ROSE, ALT = colors.HexColor("#F8E7EF"), colors.HexColor("#EACDD9"), colors.HexColor("#FFF8FA")
CREAM, GREEN, INK, MUTED = colors.HexColor("#FFF5DA"), colors.HexColor("#E8F5EC"), colors.HexColor("#332A31"), colors.HexColor("#6C5B66")
pdfmetrics.registerFont(TTFont("Arial", r"C:\Windows\Fonts\arial.ttf"))
pdfmetrics.registerFont(TTFont("Arial-Bold", r"C:\Windows\Fonts\arialbd.ttf"))
styles = getSampleStyleSheet()
BODY = ParagraphStyle("Body", fontName="Arial", fontSize=8.75, leading=11.5, textColor=INK, spaceAfter=3*mm)
SMALL = ParagraphStyle("Small", parent=BODY, fontSize=7.55, leading=9.45, spaceAfter=1.6*mm)
TINY = ParagraphStyle("Tiny", parent=BODY, fontSize=6.8, leading=8.35, spaceAfter=1*mm)
TITLE = ParagraphStyle("Title", fontName="Arial-Bold", fontSize=20, leading=24, textColor=colors.white, alignment=TA_LEFT, spaceAfter=5*mm)
SUBTITLE = ParagraphStyle("Subtitle", fontName="Arial", fontSize=11.5, leading=15, textColor=colors.HexColor("#FFD8EB"), spaceAfter=5*mm)
H1 = ParagraphStyle("H1", fontName="Arial-Bold", fontSize=15.5, leading=18.5, textColor=PLUM, spaceBefore=1*mm, spaceAfter=3*mm)
H2 = ParagraphStyle("H2", fontName="Arial-Bold", fontSize=10.7, leading=13.2, textColor=PINK, spaceBefore=1.3*mm, spaceAfter=1.5*mm)
KICK = ParagraphStyle("Kicker", fontName="Arial-Bold", fontSize=10, leading=12, textColor=colors.HexColor("#FFD8EB"), spaceAfter=4*mm)

def p(text, style=BODY): return Paragraph(text, style)
def box(text, bg=PALE, border=ROSE, style=BODY, pad=7):
    t = Table([[p(text, style)]], colWidths=[170*mm])
    t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),bg),("BOX",(0,0),(-1,-1),.7,border),("LEFTPADDING",(0,0),(-1,-1),pad),("RIGHTPADDING",(0,0),(-1,-1),pad),("TOPPADDING",(0,0),(-1,-1),pad),("BOTTOMPADDING",(0,0),(-1,-1),pad)])); return t
def table(data, widths, size=7.1, header=True):
    rows=[]
    for i,row in enumerate(data):
        st=ParagraphStyle(f"c{i}_{size}_{len(data)}",parent=SMALL,fontSize=size,leading=size+1.8,textColor=colors.white if header and i==0 else INK,fontName="Arial-Bold" if header and i==0 else "Arial",spaceAfter=0)
        rows.append([p(str(x),st) for x in row])
    t=Table(rows,colWidths=widths,repeatRows=1 if header else 0)
    cmds=[("GRID",(0,0),(-1,-1),.45,ROSE),("VALIGN",(0,0),(-1,-1),"TOP"),("LEFTPADDING",(0,0),(-1,-1),4),("RIGHTPADDING",(0,0),(-1,-1),4),("TOPPADDING",(0,0),(-1,-1),3),("BOTTOMPADDING",(0,0),(-1,-1),3)]
    if header: cmds.append(("BACKGROUND",(0,0),(-1,0),PLUM))
    start=1 if header else 0
    for i in range(start,len(data)):
        if (i-start)%2: cmds.append(("BACKGROUND",(0,i),(-1,i),ALT))
    t.setStyle(TableStyle(cmds)); return t
def draw(canvas, doc):
    w,h=A4; n=canvas.getPageNumber(); canvas.saveState()
    if n==1:
        canvas.setFillColor(PLUM); canvas.rect(0,h-91*mm,w,91*mm,fill=1,stroke=0); canvas.setFillColor(PINK); canvas.rect(0,h-94*mm,w,3*mm,fill=1,stroke=0)
    else:
        canvas.setStrokeColor(PINK); canvas.line(20*mm,h-16*mm,w-20*mm,h-16*mm); canvas.setFont("Arial",8); canvas.setFillColor(MUTED); canvas.drawString(20*mm,h-12*mm,"A2 5.7  |  Время и реальное условие")
    canvas.setFont("Arial",8); canvas.setFillColor(MUTED); canvas.drawString(20*mm,9*mm,"SlovoKrok | личный учебный модуль"); canvas.drawRightString(w-20*mm,9*mm,f"стр. {n} / 7"); canvas.restoreState()

doc=BaseDocTemplate(str(OUTPUT),pagesize=A4,leftMargin=20*mm,rightMargin=20*mm,topMargin=20*mm,bottomMargin=18*mm,title="Slovak A2 - Тема 5.7 - Время и реальное условие",author="SlovoKrok")
doc.addPageTemplates([PageTemplate(id="series",frames=[Frame(20*mm,18*mm,170*mm,257*mm,id="main",leftPadding=0,rightPadding=0)],onPage=draw)])

story=[
 p("МОДУЛЬ 5  •  СВЯЗНАЯ РЕЧЬ И СЛОЖНЫЕ ПРЕДЛОЖЕНИЯ",KICK),p("Время и<br/>реальное условие",TITLE),p("Kedy, keď, ak: спрашиваем о времени и говорим о реальной возможности",SUBTITLE),Spacer(1,34*mm),
 p("<b>Kedy</b> спрашивает, когда произойдёт событие. <b>Keď</b> связывает событие со временем. <b>Ak</b> вводит реальное условие: результат возможен, если условие выполнится."),p("После модуля вы сможете:",H2),
 table([["1","различать вопрос kedy и временную связь keď"],["2","выбирать ak для открытого реального условия"],["3","использовать ak/keď с настоящим и будущим индикатива"],["4","ставить запятую и менять порядок частей"]],[12*mm,158*mm],7.2,False),Spacer(1,3*mm),
 box("<b>Три опоры:</b> <b>Kedy?</b> - вопрос. <b>Keď</b> - когда событие наступает. <b>Ak</b> - если событие возможно."),PageBreak(),

 p("1. Kedy спрашивает, keď связывает",H1),p("<b>Kedy</b> - вопросительное слово. Оно начинает прямой или косвенный вопрос о времени. <b>Keď</b> - союз: он соединяет событие с моментом или периодом времени."),
 table([["Функция","Пример","Перевод"],["прямой вопрос","Kedy prídeš?","Когда ты придёшь?"],["косвенный вопрос","Neviem, kedy prídeš.","Я не знаю, когда ты придёшь."],["время в прошлом","Keď som prišiel, Eva už čakala.","Когда я пришёл, Ева уже ждала."],["время сейчас","Keď prší, zostávam doma.","Когда идёт дождь, я остаюсь дома."],["время в будущем","Keď prídem domov, zavolám ti.","Когда я приду домой, позвоню тебе."]],[39*mm,65*mm,66*mm],5.9),
 p("Главный контраст",H2),table([["Kedy?","Keď"],["Kedy sa začína kurz?","Keď sa kurz začne, pošlem ti správu."],["Когда начинается курс?","Когда курс начнётся, я пришлю тебе сообщение."],["Povedz mi, kedy odchádza vlak.","Keď vlak odíde, zavolám taxík."],["Скажи, когда отправляется поезд.","Когда поезд отправится, я вызову такси."]],[85*mm,85*mm],6.05),
 box("<b>Ошибка:</b> *Kedy prídem domov, zavolám ti.* Здесь нет вопроса. Нужен союз: <b>Keď prídem domov, zavolám ti.</b>",CREAM,colors.HexColor("#E7C76C"),SMALL),PageBreak(),

 p("2. Ak вводит реальное условие",H1),p("Используйте <b>ak</b>, когда условие реально и его выполнение не гарантировано. Обе части стоят в <b>indikatív</b>: мы говорим о факте, плане или возможном результате, а не о нереальном предположении."),
 table([["Условие","Результат","Готовая фраза"],["будет время","приду","Ak budem mať čas, prídem."],["закончишь раньше","позвони","Ak skončíš skôr, zavolaj mi."],["будет дождь","останемся дома","Ak bude pršať, zostaneme doma."],["магазин открыт","купим хлеб","Ak je obchod otvorený, kúpime chlieb."],["не понимаешь","спроси","Ak nerozumieš, opýtaj sa."]],[43*mm,43*mm,84*mm],5.9),
 p("Ak или keď?",H2),table([["Форма","Смысл","Пример"],["ak","если; условие открыто","Ak príde Peter, začneme."],["keď","когда; событие ожидается как момент","Keď príde Peter, začneme."],["keď","когда/если; обычная повторяемая ситуация","Keď mám čas, chodím plávať."]],[27*mm,64*mm,79*mm],6.05),
 box("<b>Учебная опора:</b> если по-русски важна развилка <i>если случится</i>, выбирайте <b>ak</b>. Если говорящий ожидает событие и называет момент <i>когда случится</i>, выбирайте <b>keď</b>.",GREEN,colors.HexColor("#A8D5B3"),SMALL),PageBreak(),

 p("3. Настоящее и будущее в условии",H1),p("После <b>ak</b> и временного <b>keď</b> употребляется изъявительное наклонение. Форма зависит от вида и смысла глагола: аналитическое будущее у несовершенного глагола или форма совершенного глагола с будущим значением."),
 table([["Модель","Пример","Перевод"],["ak + настоящее, настоящее","Ak mám čas, cvičím.","Если у меня есть время, я тренируюсь."],["ak + будущее, будущее","Ak budem mať čas, budem cvičiť.","Если будет время, я буду тренироваться."],["ak + совершенный глагол","Ak skončím, zavolám ti.","Если закончу, позвоню тебе."],["keď + совершенный глагол","Keď prídem, napíšem ti.","Когда приду, напишу тебе."],["keď + прошлое, прошлое","Keď som prišiel, zavolal som.","Когда я пришёл, я позвонил."]],[49*mm,61*mm,60*mm],5.8),
 p("Порядок частей и запятая",H2),table([["Условие или время сначала","Главная часть сначала"],["Ak bude pekne, pôjdeme na výlet.","Pôjdeme na výlet, ak bude pekne."],["Keď skončím prácu, oddýchnem si.","Oddýchnem si, keď skončím prácu."]],[85*mm,85*mm],6.1),
 box("<b>Граница темы:</b> здесь только реальная ситуация с <b>indikatív</b>. Условное наклонение выражает другой, нереальный или гипотетический тип условия и в этот модуль не входит.",PALE,PINK,SMALL),PageBreak(),

 p("4. Модель общения: план на выходные",H1),
 box("<b>Mária:</b> Kedy pôjdeme na výlet?<br/><b>Ivan:</b> V sobotu, ak bude pekne.<br/><b>Mária:</b> A čo urobíme, ak bude pršať?<br/><b>Ivan:</b> Ak bude pršať, zostaneme v meste.<br/><b>Mária:</b> Dobre. Keď skončím prácu, pozriem si predpoveď.<br/><b>Ivan:</b> Ak nájdeš lepší plán, napíš mi.",PALE,ROSE,SMALL),
 p("Перевод",H2),p("Когда мы поедем на экскурсию? В субботу, если будет хорошая погода. А что мы сделаем, если будет дождь? Если будет дождь, останемся в городе. Хорошо. Когда я закончу работу, посмотрю прогноз. Если найдёшь план получше, напиши мне.",SMALL),
 p("Банк полезных моделей",H2),table([["SK","RU"],["Kedy máš voľno?","Когда ты свободен?"],["Neviem, kedy sa vráti.","Не знаю, когда он вернётся."],["Keď sa vráti, porozprávame sa.","Когда он вернётся, поговорим."],["Ak sa vráti skoro, pôjdeme spolu.","Если он вернётся рано, пойдём вместе."],["Ak budeš potrebovať pomoc, zavolaj.","Если понадобится помощь, позвони."],["Keď budem doma, pošlem ti adresu.","Когда буду дома, пришлю тебе адрес."]],[86*mm,84*mm],6.0),
 box("<b>Смысл решает:</b> <b>Kedy?</b> просит время; <b>keď</b> помещает действие во времени; <b>ak</b> оставляет реальную возможность открытой.",GREEN,colors.HexColor("#A8D5B3"),SMALL),PageBreak(),

 p("5. Частые ошибки и упражнения",H1),box("<b>Частые ошибки:</b> ставят <b>kedy</b> вместо союза <b>keď</b>; смешивают время и условие; забывают запятую; используют гипотетическое <i>by</i> в реальном условии; неверно строят будущее.",CREAM,colors.HexColor("#E7C76C"),TINY),
 p("Упражнение 1. Выберите kedy, keď или ak",H2),p("1) ___ prídeš? 2) ___ prídem domov, zavolám. 3) ___ bude pršať, zostaneme doma. 4) Neviem, ___ odchádza vlak.",TINY),
 p("Упражнение 2. Определите: время или условие",H2),p("1) Keď som prišiel, spala. 2) Ak budeš mať čas, príď. 3) Keď skončím, oddýchnem si. 4) Ak nerozumieš, opýtaj sa.",TINY),
 p("Упражнение 3. Вставьте глагол",H2),p("1) Ak ___ (mať) čas zajtra, prídem. 2) Keď ___ (prísť) domov, napíšem. 3) Ak ___ (pršať), nepôjdeme von. 4) Keď som ___ (skončiť), zavolal som.",TINY),
 p("Упражнение 4. Поставьте запятые и исправьте",H2),p("1) Kedy prídem zavolám ti. 2) Ak bude pekne pôjdeme von. 3) Neviem keď sa vráti. 4) Ak budem mať čas prišiel by som.",TINY),
 p("Упражнение 5. Переведите",H2),p("1) Когда ты придёшь? 2) Когда приду домой, позвоню. 3) Если будет дождь, останемся дома. 4) Если закончишь раньше, напиши мне.",TINY),
 p("Упражнение 6. Составьте реальный план",H2),p("Напишите 5-7 предложений о выходных или рабочем дне. Используйте вопрос с <b>kedy</b>, временную связь с <b>keď</b> и два реальных условия с <b>ak</b>.",TINY),PageBreak(),

 p("6. Ответы и проверка мастерства",H1),p("Ответы",H2),
 p("<b>1.</b> 1) Kedy; 2) Keď; 3) Ak; 4) kedy.",TINY),p("<b>2.</b> 1) время в прошлом; 2) реальное условие; 3) ожидаемый момент в будущем; 4) реальное условие.",TINY),
 p("<b>3.</b> 1) Ak budem mať čas zajtra, prídem. 2) Keď prídem domov, napíšem. 3) Ak bude pršať, nepôjdeme von. 4) Keď som skončil, zavolal som.",TINY),
 p("<b>4.</b> 1) Keď prídem, zavolám ti. 2) Ak bude pekne, pôjdeme von. 3) Neviem, kedy sa vráti. 4) Ak budem mať čas, prídem.",TINY),
 p("<b>5.</b> Kedy prídeš? Keď prídem domov, zavolám. Ak bude pršať, zostaneme doma. Ak skončíš skôr, napíš mi.",TINY),
 p("<b>6. Модель:</b> Kedy budeme mať voľno? Keď skončím prácu, pozriem si počasie. Ak bude pekne, pôjdeme na výlet. Ak bude pršať, zostaneme v meste. Keď sa rozhodneme, napíšem kamarátom. Возможны другие естественные варианты.",TINY),
 p("Итог в четырёх пунктах",H2),table([["OK","Kedy задаёт прямой или косвенный вопрос о времени."],["OK","Keď связывает действие с моментом или ожидаемым событием."],["OK","Ak вводит открытое реальное условие."],["OK","Использую indikatív и отделяю части запятой."]],[12*mm,158*mm],6.3,False),Spacer(1,2*mm),
 box("<b>Финальная проверка:</b> скажите по-словацки: <b>Когда ты придёшь?</b>; <b>Когда придёшь, позвони</b>; <b>Если будет время, приходи</b>.",GREEN,colors.HexColor("#A8D5B3"),SMALL),p("Следующий шаг",H2),p("В теме 5.8 вы построите связный рассказ с <b>najprv, potom, neskôr, nakoniec</b>.",SMALL)
]
doc.build(story); print(OUTPUT)
