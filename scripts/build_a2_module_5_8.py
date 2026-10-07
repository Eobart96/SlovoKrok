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
OUTPUT = ROOT / "output/pdf/A2/Module_05/Slovak_A2_Tema_5_8_Svyaznyi_rasskaz_i_aktualnoe_chlenenie.pdf"
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
        canvas.setStrokeColor(PINK); canvas.line(20*mm,h-16*mm,w-20*mm,h-16*mm); canvas.setFont("Arial",8); canvas.setFillColor(MUTED); canvas.drawString(20*mm,h-12*mm,"A2 5.8  |  Связный рассказ и актуальное членение")
    canvas.setFont("Arial",8); canvas.setFillColor(MUTED); canvas.drawString(20*mm,9*mm,"SlovoKrok | личный учебный модуль"); canvas.drawRightString(w-20*mm,9*mm,f"стр. {n} / 7"); canvas.restoreState()

doc=BaseDocTemplate(str(OUTPUT),pagesize=A4,leftMargin=20*mm,rightMargin=20*mm,topMargin=20*mm,bottomMargin=18*mm,title="Slovak A2 - Тема 5.8 - Связный рассказ и актуальное членение",author="SlovoKrok")
doc.addPageTemplates([PageTemplate(id="series",frames=[Frame(20*mm,18*mm,170*mm,257*mm,id="main",leftPadding=0,rightPadding=0)],onPage=draw)])

story=[
 p("МОДУЛЬ 5  •  СВЯЗНАЯ РЕЧЬ И СЛОЖНЫЕ ПРЕДЛОЖЕНИЯ",KICK),p("Связный рассказ и<br/>актуальное членение",TITLE),p("Najprv, potom, neskôr, nakoniec: ведём слушателя от известного к новому",SUBTITLE),Spacer(1,34*mm),
 p("Хороший короткий рассказ не просто перечисляет факты. Он показывает порядок событий, связывает каждую новую фразу с предыдущей и ставит смысловой акцент там, где он нужен."),p("После модуля вы сможете:",H2),
 table([["1","строить рассказ: начало, развитие, результат"],["2","связывать этапы словами najprv, potom, neskôr, nakoniec"],["3","вести фразу от известной информации к новой"],["4","менять порядок слов для ясного смыслового акцента"]],[12*mm,158*mm],7.2,False),Spacer(1,3*mm),
 box("<b>Формула рассказа:</b> <b>najprv</b> начинаем, <b>potom</b> продолжаем, <b>neskôr</b> переносимся вперёд, <b>nakoniec</b> даём результат."),PageBreak(),

 p("1. Каркас короткого рассказа",H1),p("Четыре связки помогают слушателю не потерять последовательность. Они не обязаны стоять в каждом предложении: используйте их в ключевых переходах."),
 table([["Связка","Роль","Пример","Перевод"],["najprv","первый шаг","Najprv sme si kúpili lístky.","Сначала мы купили билеты."],["potom","следующий шаг","Potom sme nastúpili do vlaku.","Потом мы сели в поезд."],["neskôr","спустя время","Neskôr sme sa zastavili v centre.","Позже мы остановились в центре."],["nakoniec","итог, последний шаг","Nakoniec sme sa vrátili domov.","В конце концов мы вернулись домой."]],[27*mm,35*mm,61*mm,47*mm],5.5),
 p("Начало - развитие - результат",H2),table([["Часть","Что сказать","Полезная модель"],["начало","когда, где, кто, цель","Minulú sobotu sme išli na výlet."],["развитие","2-4 последовательных события","Potom sme navštívili starý hrad."],["результат","чем всё закончилось, оценка","Nakoniec sme boli unavení, ale spokojní."]],[30*mm,58*mm,82*mm],6.0),
 box("<b>Potom или neskôr?</b> <b>Potom</b> просто даёт следующий шаг. <b>Neskôr</b> подчёркивает, что прошло некоторое время. Это смысловая разница, а не жёсткая грамматическая формула.",CREAM,colors.HexColor("#E7C76C"),SMALL),PageBreak(),

 p("2. Известное ведёт к новому",H1),p("Актуальное членение показывает, что в сообщении служит исходной точкой, а что является главным новым ядром. В спокойной нейтральной фразе известная опора обычно появляется раньше, а новая информация - ближе к концу."),
 table([["Контекст","Известная опора","Новое ядро"],["Kto prišiel?","ситуация: кто-то пришёл","Prišla <b>Zuzana</b>."],["Čo urobila Zuzana?","<b>Zuzana</b>","Zuzana priniesla <b>koláč</b>."],["Aký bol koláč?","<b>koláč</b>","Koláč bol <b>výborný</b>."],["Čo ste urobili potom?","предыдущая ситуация","Potom sme išli <b>na prechádzku</b>."]],[48*mm,50*mm,72*mm],6.0),
 p("Как возникает связность",H2),table([["Фраза","Связь"],["Na stanici čakala Lucia.","новое: Lucia"],["Lucia mala veľký kufor.","Lucia уже известна; новое: kufor"],["V kufri boli darčeky.","kufor уже известен; новое: darčeky"],["Darčeky dostali deti.","darčeky уже известны; новое: deti"]],[103*mm,67*mm],6.15),
 box("<b>Учебная опора:</b> спросите себя: «О чём уже знает слушатель?» и «Что я сообщаю сейчас?» Ответ часто подсказывает естественный порядок слов.",GREEN,colors.HexColor("#A8D5B3"),SMALL),PageBreak(),

 p("3. Нейтральный и выделенный порядок слов",H1),p("Словацкий порядок слов гибкий, но не случайный. Нейтральный вариант спокойно ведёт от опоры к новому. Выделенный вариант переносит элемент ради контраста и требует подходящего контекста или ударения."),
 table([["Вопрос или контекст","Естественный ответ","Где новое"],["Kto zavolal?","Zavolala <b>Lucia</b>.","Lucia"],["Komu zavolala Lucia?","Lucia zavolala <b>Martinovi</b>.","Martinovi"],["Kedy mu zavolala?","Zavolala mu <b>večer</b>.","večer"],["Čo kúpil Peter?","Peter kúpil <b>nové auto</b>.","nové auto"]],[49*mm,75*mm,46*mm],6.0),
 p("Когда нужен контраст",H2),table([["Фраза","Смысловой акцент"],["V SOBOTU sme išli na výlet, nie v nedeľu.","именно в субботу"],["Knihu som kúpil JA, nie Peter.","именно я"],["PETRA som stretol, nie Jána.","именно Петра"],["Na výlet sme išli VLAKOM, nie autom.","именно поездом"]],[108*mm,62*mm],6.1),
 box("<b>Важно:</b> заглавные буквы здесь только показывают логическое ударение. В обычном тексте пишите слова нормально. Не переставляйте слова ради эффекта без контекста: сначала выберите, что слушателю уже известно и что вы выделяете.",CREAM,colors.HexColor("#E7C76C"),SMALL),PageBreak(),

 p("4. Модель: поездка к озеру",H1),
 box("<b>Minulú sobotu sme išli k jazeru.</b> Najprv sme sa stretli na stanici. Na stanici už čakala Lucia. Lucia priniesla mapu a malé občerstvenie. Potom sme nastúpili do vlaku. Vo vlaku sme naplánovali trasu. Neskôr sme vystúpili v Žiline a pokračovali autobusom. Nakoniec sme prišli k jazeru. Najkrajší bol pokoj pri vode.",PALE,ROSE,SMALL),
 p("Перевод",H2),p("В прошлую субботу мы поехали к озеру. Сначала встретились на вокзале. На вокзале уже ждала Луция. Она принесла карту и небольшой перекус. Потом мы сели в поезд. В поезде спланировали маршрут. Позже вышли в Жилине и продолжили путь на автобусе. Наконец добрались до озера. Самым прекрасным был покой у воды.",SMALL),
 p("Почему текст связный",H2),table([["Приём","В модели"],["временной каркас","najprv -> potom -> neskôr -> nakoniec"],["цепочка известное -> новое","stanica -> Lucia -> mapa; vlak -> trasa"],["финальный результат","prišli k jazeru"],["смысловой итог","Najkrajší bol pokoj pri vode."]],[55*mm,115*mm],6.1),
 p("Банк полезных фраз",H2),table([["SK","RU"],["Všetko sa začalo ráno.","Всё началось утром."],["O chvíľu sme pokračovali ďalej.","Через некоторое время мы продолжили путь."],["Potom sa stalo niečo nečakané.","Потом случилось нечто неожиданное."],["Nakoniec všetko dobre dopadlo.","В конце концов всё закончилось хорошо."]],[88*mm,82*mm],6.0),PageBreak(),

 p("5. Частые ошибки и упражнения",H1),box("<b>Частые ошибки:</b> повторяют <b>potom</b> в каждом предложении; путают <b>neskôr</b> с простым следующим шагом; вводят нового героя без опоры; ставят главное новое в начало без контраста; заканчивают рассказ без результата.",CREAM,colors.HexColor("#E7C76C"),TINY),
 p("Упражнение 1. Выберите связку",H2),p("1) ___ sme si pripravili batohy. 2) ___ sme vyšli z domu. 3) O dve hodiny ___ sme si oddýchli. 4) ___ sme bezpečne prišli do cieľa. Используйте najprv, potom, neskôr, nakoniec.",TINY),
 p("Упражнение 2. Найдите известное и новое",H2),p("Контекст: Na stanici čakala žena. 1) Žena držala červený dáždnik. 2) Dáždnik bol veľmi starý. Назовите известную опору и новое ядро в каждом предложении.",TINY),
 p("Упражнение 3. Соберите нейтральный ответ",H2),p("1) Kto prišiel? (prišiel / Tomáš) 2) Čo kúpil Tomáš? (Tomáš / kúpil / lístky) 3) Kedy ich kúpil? (ich / kúpil / ráno)",TINY),
 p("Упражнение 4. Выделите контраст",H2),p("Ответьте с противопоставлением: 1) Išli ste v nedeľu? (v sobotu) 2) Knihu kúpil Peter? (ja) 3) Cestovali ste autom? (vlakom)",TINY),
 p("Упражнение 5. Соедините в рассказ",H2),p("Вставьте связки и при необходимости повторите известное слово: prišli sme do mesta; navštívili sme múzeum; dali sme si obed; vrátili sme sa domov.",TINY),
 p("Упражнение 6. Напишите свой рассказ",H2),p("Составьте 6-8 предложений о поездке, встрече или неожиданном дне. Дайте начало, 3-4 события и результат; используйте четыре связки и одну цепочку «известное -> новое».",TINY),PageBreak(),

 p("6. Ответы и проверка мастерства",H1),p("Ответы",H2),
 p("<b>1.</b> 1) Najprv; 2) Potom; 3) neskôr; 4) Nakoniec.",TINY),
 p("<b>2.</b> 1) известное: žena; новое: červený dáždnik. 2) известное: dáždnik; новое: veľmi starý.",TINY),
 p("<b>3.</b> 1) Prišiel Tomáš. 2) Tomáš kúpil lístky. 3) Kúpil ich ráno. Возможны варианты с естественным ударением.",TINY),
 p("<b>4.</b> 1) V SOBOTU sme išli, nie v nedeľu. 2) Knihu som kúpil JA, nie Peter. 3) Cestovali sme VLAKOM, nie autom.",TINY),
 p("<b>5.</b> Najprv sme prišli do mesta. Potom sme navštívili múzeum. Neskôr sme si dali obed. Nakoniec sme sa vrátili domov.",TINY),
 p("<b>6. Модель:</b> Minulú sobotu som išiel do Trnavy. Najprv som sa stretol s kamarátom na stanici. Kamarát priniesol mapu mesta. Potom sme navštívili starú vežu. Neskôr sme si dali obed v malej reštaurácii. Nakoniec sme sa vrátili vlakom domov. Najlepší bol spoločný čas. Возможны другие естественные варианты.",TINY),
 p("Итог в четырёх пунктах",H2),table([["OK","Строю рассказ с началом, развитием и результатом."],["OK","Различаю najprv, potom, neskôr и nakoniec."],["OK","Связываю известную опору с новым ядром."],["OK","Меняю порядок слов только ради понятного акцента."]],[12*mm,158*mm],6.25,False),Spacer(1,2*mm),
 box("<b>Финальная проверка:</b> расскажите за минуту о вчерашнем дне. Слушатель должен легко понять порядок событий, связь фраз и самый важный итог.",GREEN,colors.HexColor("#A8D5B3"),SMALL),p("Следующий шаг",H2),p("Модуль 5 завершён. Теперь применяйте связный рассказ в практических темах: поездки, работа, покупки и отношения.",SMALL)
]
doc.build(story); print(OUTPUT)
