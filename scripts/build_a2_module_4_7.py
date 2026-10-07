from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output" / "pdf" / "A2" / "Module_04" / "Slovak_A2_Tema_4_7_Glagoly_dvizheniya_ist_i_chodit.pdf"
TITLE = "Slovak A2 - Тема 4.7 - Глаголы движения ísť и chodiť"

PLUM = colors.HexColor("#7B245F")
PALE = colors.HexColor("#FFF0F7")
ROSE = colors.HexColor("#EACDD9")
ALT = colors.HexColor("#FFF8FA")
BLUE = colors.HexColor("#EAF2FA")
GREEN = colors.HexColor("#E2F3E8")
CREAM = colors.HexColor("#FFF5E5")
INK = colors.HexColor("#30272E")
MUTED = colors.HexColor("#705E68")
WHITE = colors.white


def register_fonts():
    regular = next(p for p in [Path("C:/Windows/Fonts/arial.ttf"), Path("C:/Windows/Fonts/calibri.ttf")] if p.exists())
    bold = next(p for p in [Path("C:/Windows/Fonts/arialbd.ttf"), Path("C:/Windows/Fonts/calibrib.ttf")] if p.exists())
    pdfmetrics.registerFont(TTFont("SK", str(regular)))
    pdfmetrics.registerFont(TTFont("SK-Bold", str(bold)))


register_fonts()
ST = {
    "cover_kicker": ParagraphStyle("cover_kicker", fontName="SK-Bold", fontSize=14, leading=18, textColor=colors.HexColor("#F8D8E9"), alignment=TA_CENTER, spaceAfter=8),
    "cover_title": ParagraphStyle("cover_title", fontName="SK-Bold", fontSize=24, leading=29, textColor=WHITE, alignment=TA_CENTER, spaceAfter=11),
    "cover_sub": ParagraphStyle("cover_sub", fontName="SK", fontSize=12.2, leading=17, textColor=WHITE, alignment=TA_CENTER),
    "h1": ParagraphStyle("h1", fontName="SK-Bold", fontSize=20, leading=24, textColor=PLUM, spaceAfter=8),
    "h2": ParagraphStyle("h2", fontName="SK-Bold", fontSize=13.5, leading=17, textColor=PLUM, spaceBefore=6, spaceAfter=5),
    "body": ParagraphStyle("body", fontName="SK", fontSize=9.45, leading=13.0, textColor=INK, spaceAfter=4),
    "small": ParagraphStyle("small", fontName="SK", fontSize=8.25, leading=11.3, textColor=MUTED, spaceAfter=2),
    "box": ParagraphStyle("box", fontName="SK", fontSize=9.0, leading=12.4, textColor=INK),
    "box_b": ParagraphStyle("box_b", fontName="SK-Bold", fontSize=9.35, leading=12.7, textColor=PLUM),
    "task": ParagraphStyle("task", fontName="SK", fontSize=8.45, leading=11.35, textColor=INK, spaceAfter=4),
    "answer": ParagraphStyle("answer", fontName="SK", fontSize=8.0, leading=10.55, textColor=INK, spaceAfter=3),
}


def P(text, style="body"):
    return Paragraph(text, ST[style])


def callout(title, text, color=PALE, width=169):
    table = Table([[P(title, "box_b")], [P(text, "box")]], colWidths=[width * mm])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), color), ("BOX", (0, 0), (-1, -1), 0.7, ROSE),
        ("LINEBELOW", (0, 0), (-1, 0), 0.45, ROSE),
        ("LEFTPADDING", (0, 0), (-1, -1), 8), ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    return table


def grid(rows, widths, header=True, font="small"):
    data = [[P(cell, "box_b" if header and i == 0 else font) for cell in row] for i, row in enumerate(rows)]
    table = Table(data, colWidths=[w * mm for w in widths], repeatRows=1 if header else 0)
    rules = [
        ("GRID", (0, 0), (-1, -1), 0.45, ROSE), ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6), ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]
    if header:
        rules.append(("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#F5D4E5")))
    for row in range(1 if header else 0, len(data)):
        if row % 2 == 0:
            rules.append(("BACKGROUND", (0, row), (-1, row), ALT))
    table.setStyle(TableStyle(rules))
    return table


def first_page(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(PLUM)
    canvas.rect(0, 0, A4[0], A4[1], fill=1, stroke=0)
    canvas.setFillColor(colors.HexColor("#9E2F74"))
    canvas.circle(18 * mm, 266 * mm, 37 * mm, fill=1, stroke=0)
    canvas.circle(194 * mm, 28 * mm, 49 * mm, fill=1, stroke=0)
    canvas.setFillColor(colors.HexColor("#F8D8E9"))
    canvas.roundRect(27 * mm, 34 * mm, 156 * mm, 38 * mm, 5 * mm, fill=1, stroke=0)
    canvas.setFillColor(PLUM)
    canvas.setFont("SK-Bold", 11)
    canvas.drawCentredString(105 * mm, 57 * mm, "IDEM TERAZ - CHODÍM PRAVIDELNE")
    canvas.setFont("SK", 9)
    canvas.drawCentredString(105 * mm, 47 * mm, "smer, opakovanie a celý cestovný krok")
    canvas.setFillColor(colors.HexColor("#F8D8E9"))
    canvas.setFont("SK", 7.5)
    canvas.drawCentredString(105 * mm, 13 * mm, "стр. 1 / 7")
    canvas.restoreState()


def later_page(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(ROSE)
    canvas.setLineWidth(0.7)
    canvas.line(20 * mm, 281 * mm, 190 * mm, 281 * mm)
    canvas.setFillColor(PLUM)
    canvas.setFont("SK-Bold", 8)
    canvas.drawString(20 * mm, 285 * mm, "SLOVOKROK  |  A2  |  ТЕМА 4.7  |  ГЛАГОЛЫ ДВИЖЕНИЯ")
    canvas.setFillColor(MUTED)
    canvas.setFont("SK", 7.5)
    canvas.drawCentredString(105 * mm, 10 * mm, f"стр. {doc.page} / 7")
    canvas.restoreState()


doc = SimpleDocTemplate(
    str(OUT), pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm,
    topMargin=26 * mm, bottomMargin=17 * mm, title=TITLE,
    author="SlovoKrok", subject="Slovak A2 self-study module 4.7",
)
story = []

# 1. Cover
story += [
    Spacer(1, 23 * mm), P("SLOVOKROK • СЛОВАЦКИЙ A2", "cover_kicker"),
    P("ТЕМА 4.7", "cover_kicker"),
    P("Глаголы движения<br/>ísť и chodiť", "cover_title"),
    P("Smer, opakovanie a cestovanie", "cover_sub"), Spacer(1, 14 * mm),
    Table(
        [[P("После модуля вы сможете", "box_b")],
         [P("• выбирать <i>ísť</i> для одного направленного движения и <i>chodiť</i> для регулярного;<br/>• уточнять движение пешком, на транспорте и поездку в целом;<br/>• описывать прибытие, отправление и пересадку;<br/>• соединять глагол с естественным предлогом места и направления.", "box")]],
        colWidths=[145 * mm],
        style=TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#FFF7FB")),
            ("LEFTPADDING", (0, 0), (-1, -1), 10), ("RIGHTPADDING", (0, 0), (-1, -1), 10),
            ("TOPPADDING", (0, 0), (-1, -1), 7), ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ]),
    ), PageBreak(),
]

# 2. ist vs chodit
story += [
    P("1. Одно направление или привычный маршрут?", "h1"),
    callout("Главная опора", "<b>ísť</b> показывает одно актуальное или конкретное направленное перемещение. <b>chodiť</b> показывает повторяемость, привычку, движение туда и обратно или способность ходить."),
    P("Сравните смысл", "h2"),
    grid([
        ["Конкретно сейчас / один раз", "Регулярно / вообще"],
        ["<b>Teraz idem do práce.</b><br/>Сейчас я иду / еду на работу.", "<b>Každý deň chodím do práce.</b><br/>Я каждый день хожу / езжу на работу."],
        ["<b>Kam ideš?</b><br/>Куда ты сейчас идёшь / едешь?", "<b>Kam chodíš cez víkend?</b><br/>Куда ты обычно ходишь по выходным?"],
        ["<b>Ideme do kina.</b><br/>Мы идём в кино.", "<b>Radi chodíme do kina.</b><br/>Мы любим ходить в кино."],
        ["<b>Včera som išla pešo.</b><br/>Вчера я пошла пешком.", "<b>V detstve som chodila pešo.</b><br/>В детстве я обычно ходила пешком."],
    ], [84.5, 84.5]),
    P("Настоящее время", "h2"),
    grid([
        ["лицо", "ísť", "chodiť"],
        ["ja", "idem", "chodím"], ["ty", "ideš", "chodíš"], ["on / ona", "ide", "chodí"],
        ["my", "ideme", "chodíme"], ["vy", "idete", "chodíte"], ["oni / ony", "idú", "chodia"],
    ], [31, 68, 70]),
    callout("Не переводите механически", "Русское «ходить» не всегда требует <i>chodiť</i>. В вопросе «Куда ты идёшь сейчас?» нужен <i>Kam ideš?</i>; привычка «Я хожу в бассейн по вторникам» - <i>V utorok chodím do bazéna.</i>", CREAM),
    PageBreak(),
]

# 3. Walking, transport, travel
story += [
    P("2. Пешком, транспортом или в поездке", "h1"),
    P("Сам глагол <i>ísť</i> не сообщает способ передвижения. Его уточняет обстоятельство. <i>Chodiť</i> тоже может означать регулярные поездки на транспорте."),
    grid([
        ["Модель", "Пример", "Перевод"],
        ["ísť / chodiť <b>pešo</b>", "Idem domov pešo.", "Я иду домой пешком."],
        ["ísť / chodiť <b>autobusom</b>", "Do práce chodím autobusom.", "На работу я езжу автобусом."],
        ["ísť <b>na bicykli</b>", "Dnes idem na bicykli.", "Сегодня я еду на велосипеде."],
        ["cestovať <b>vlakom</b>", "Radi cestujeme vlakom.", "Мы любим путешествовать поездом."],
        ["cestovať <b>do zahraničia</b>", "Často cestuje do zahraničia.", "Он часто ездит за границу."],
    ], [45, 63, 61]),
    callout("ísť или cestovať?", "<i>Ísť</i> фокусируется на конкретном движении к цели: <i>Zajtra idem do Košíc.</i> <i>Cestovať</i> называет сам процесс поездки или путешествия: <i>Rád cestujem po Slovensku.</i>", BLUE),
    P("Прошедшее и будущее", "h2"),
    grid([
        ["Значение", "ísť", "chodiť"],
        ["прошедшее", "išiel / išla / išli", "chodil / chodila / chodili"],
        ["будущее", "pôjdem, pôjdeš, pôjde...", "budem chodiť..."],
        ["пример", "Zajtra pôjdem k lekárovi.<br/>Завтра пойду к врачу.", "V zime budem chodiť autobusom.<br/>Зимой буду ездить автобусом."],
    ], [40, 64.5, 64.5]),
    callout("Важная форма", "Для одного будущего перемещения употребляйте <b>pôjdem</b>, а не *budem ísť: <i>Večer pôjdeme do divadla.</i> Для регулярности удобно <i>budem chodiť</i>: <i>Budem chodiť na kurz dvakrát týždenne.</i>", CREAM),
    P("Ещё три естественных примера", "h2"),
    P("<b>Vlak ide o siedmej.</b> - Поезд отправляется в семь."),
    P("<b>Tento autobus chodí každú hodinu.</b> - Этот автобус ходит каждый час."),
    P("<b>Minulý rok sme cestovali po Európe.</b> - В прошлом году мы путешествовали по Европе."),
    PageBreak(),
]

# 4. Route verbs and prepositions
story += [
    P("3. Маршрут: от отправления до пересадки", "h1"),
    grid([
        ["Шаг", "Совершенный глагол", "Процесс / повтор"],
        ["прибыть", "prísť", "prichádzať"], ["уйти / уехать", "odísť", "odchádzať"],
        ["сесть в транспорт", "nastúpiť", "nastupovať"], ["выйти", "vystúpiť", "vystupovať"],
        ["пересесть", "prestúpiť", "prestupovať"],
    ], [39, 64, 66]),
    P("Готовые модели управления", "h2"),
    grid([
        ["Куда / откуда", "Пример"],
        ["<b>do + Gen.</b>", "Prídeme do Bratislavy o deviatej. - Приедем в Братиславу в девять."],
        ["<b>na + Acc.</b>", "Idem na stanicu. - Я иду на вокзал."],
        ["<b>k + Dat.</b>", "Pôjdem k lekárovi. - Я пойду к врачу."],
        ["<b>z / zo + Gen.</b>", "Odišla z kancelárie. - Она ушла из офиса."],
        ["<b>od + Gen.</b>", "Vraciame sa od rodičov. - Мы возвращаемся от родителей."],
        ["<b>do / z + транспорта</b>", "Nastúpte do autobusu. Vystúpte z električky. - Сядьте в автобус. Выйдите из трамвая."],
        ["<b>na + Acc.</b> при пересадке", "V Trnave prestúpime na vlak. - В Трнаве пересядем на поезд."],
    ], [54, 115]),
    callout("Вид показывает структуру маршрута", "<i>Keď autobus prichádzal, ľudia už čakali.</i> - фон, прибытие в процессе. <i>Autobus prišiel o šiestej.</i> - завершённый факт. <i>Každý deň prestupujem v centre.</i> - повтор. <i>Dnes prestúpim na vlak.</i> - один завершённый шаг.", BLUE),
    PageBreak(),
]

# 5. Connected route
story += [
    P("4. Связный маршрут и мини-диалог", "h1"),
    callout("Cesta do práce", "Každý pracovný deň chodím do práce vlakom. Z domu odchádzam o pol siedmej a na stanicu idem pešo. Nastúpim do vlaku do Bratislavy. V Trnave niekedy prestúpim na rýchlik. Keď prídem do Bratislavy, vystúpim z vlaku a idem električkou do centra. Do kancelárie prídem pred ôsmou.<br/><br/><b>Перевод:</b> Каждый рабочий день я езжу на работу поездом. Из дома выхожу в половине седьмого и иду на вокзал пешком. Сажусь в поезд до Братиславы. В Трнаве иногда пересаживаюсь на скорый поезд. Когда приезжаю в Братиславу, выхожу из поезда и еду трамваем в центр. В офис приезжаю до восьми.", BLUE),
    P("Как читать этот текст", "h2"),
    grid([
        ["Сигнал", "Выбор"],
        ["každý pracovný deň", "chodiť и формы процесса: регулярный маршрут"],
        ["na stanicu idem pešo", "одно направленное движение внутри маршрута"],
        ["nastúpim, prestúpim, prídem, vystúpim", "границы и завершённые шаги"],
    ], [53, 116]),
    P("Мини-диалог на вокзале", "h2"),
    callout("Ktorým vlakom?", "<b>Eva:</b> Ako chodíš do Nitry?<br/><b>Martin:</b> Zvyčajne cestujem vlakom, ale dnes idem autobusom.<br/><b>Eva:</b> Kde nastúpiš?<br/><b>Martin:</b> Na hlavnej stanici. V Trnave vystúpim a prestúpim na autobus do Nitry.<br/><b>Eva:</b> Kedy prídeš?<br/><b>Martin:</b> Prídem asi o tretej.<br/><br/><b>Перевод:</b> Ева: Как ты обычно добираешься до Нитры? Мартин: Обычно поездом, но сегодня еду автобусом. Ева: Где сядешь? Мартин: На главном вокзале. В Трнаве выйду и пересяду на автобус до Нитры. Ева: Когда приедешь? Мартин: Примерно в три.", PALE),
    callout("Граница с темой 4.8", "Форма <i>vraciame sa</i> здесь дана как готовый элемент маршрута. Значения и порядок <i>sa/si</i> систематизируются отдельно в следующем модуле.", CREAM),
    PageBreak(),
]

# 6. Exercises
story += [
    P("5. Ошибки и практика", "h1"),
    callout("Частые ошибки", "1) *Každý deň idem do práce вместо <i>chodím</i>; 2) *budem ísť вместо <i>pôjdem</i>; 3) считать <i>ísť</i> только ходьбой; 4) путать <i>do / na / k</i>; 5) говорить *nastúpiť na autobus вместо <i>nastúpiť do autobusu</i>; 6) терять приставку в шагах маршрута.", CREAM),
    P("<b>1. Выберите ísť или chodiť.</b><br/>a) Teraz ___ do obchodu. b) Každú sobotu ___ na trh. c) Kam ___ dnes večer? d) Deti ___ do školy pešo. e) Včera sme ___ do centra.", "task"),
    P("<b>2. Дополните форму.</b><br/>a) ja: ísť -> ___ b) oni: chodiť -> ___ c) ona, прошедшее: ísť -> ___ d) my, будущее один раз: ísť -> ___ e) ja, будущее регулярно: chodiť -> ___", "task"),
    P("<b>3. Вставьте предлог и форму.</b><br/>a) Idem ___ Bratislav___. b) Pôjdeme ___ lekár___. c) Odišiel ___ kancelári___. d) Nastúpili sme ___ autobus___. e) Vystúpte ___ električk___. f) Prestúpim ___ vlak.", "task"),
    P("<b>4. Соберите маршрут.</b> Поставьте глаголы в нужной форме: <i>odísť, ísť, nastúpiť, prestúpiť, vystúpiť, prísť</i>.<br/>Zajtra ___ z domu o šiestej. Na stanicu ___ pešo. Potom ___ do vlaku. V Trnave ___ na autobus. V Nitre ___ pri univerzite a ___ tam pred deviatou.", "task"),
    P("<b>5. Переведите.</b><br/>a) Я каждый день езжу на работу поездом. b) Сегодня я иду домой пешком. c) Завтра мы поедем в Кошице. d) В Братиславе пересядем на трамвай. e) Когда прибудет автобус?", "task"),
    P("<b>6. Мой маршрут.</b> Напишите 6-8 предложений: как вы обычно добираетесь до работы или учёбы и как поедете туда завтра. Используйте <i>chodiť</i>, форму <i>ísť</i>, вид транспорта и не менее трёх шагов маршрута.", "task"),
    PageBreak(),
]

# 7. Answers
story += [
    P("6. Ответы и итог", "h1"),
    P("<b>1.</b> a) <b>idem</b>; b) <b>chodím</b>; c) <b>ideš</b>; d) <b>chodia</b>; e) <b>išli</b>.", "answer"),
    P("<b>2.</b> a) <b>idem</b>; b) <b>chodia</b>; c) <b>išla</b>; d) <b>pôjdeme</b>; e) <b>budem chodiť</b>.", "answer"),
    P("<b>3.</b> a) <b>do Bratislavy</b>; b) <b>k lekárovi</b>; c) <b>z kancelárie</b>; d) <b>do autobusu</b>; e) <b>z električky</b>; f) <b>na vlak</b>.", "answer"),
    P("<b>4.</b> Zajtra <b>odídem</b> z domu o šiestej. Na stanicu <b>pôjdem</b> pešo. Potom <b>nastúpim</b> do vlaku. V Trnave <b>prestúpim</b> na autobus. V Nitre <b>vystúpim</b> pri univerzite a <b>prídem</b> tam pred deviatou.", "answer"),
    P("<b>5.</b> a) Každý deň chodím do práce vlakom. b) Dnes idem domov pešo. c) Zajtra pôjdeme do Košíc. d) V Bratislave prestúpime na električku. e) Kedy príde autobus?", "answer"),
    P("Образец к заданию 6", "h2"),
    callout("Moja cesta", "Každý deň chodím do práce autobusom. Z domu odchádzam o siedmej a na zastávku idem pešo. Nastúpim do autobusu číslo 50. V centre vystúpim a prestúpim na električku. Do kancelárie prídem o pol ôsmej. Zajtra však pôjdem autom, pretože po práci cestujem do Trnavy.<br/><br/>Каждый день я езжу на работу автобусом. Из дома выхожу в семь и иду на остановку пешком. Сажусь в автобус номер 50. В центре выхожу и пересаживаюсь на трамвай. В офис приезжаю в половине восьмого. Но завтра поеду на машине, потому что после работы еду в Трнаву.", BLUE),
    P("Четыре опоры", "h2"),
    grid([
        ["1", "ísť: одно конкретное направленное движение; chodiť: привычка, повтор или движение вообще."],
        ["2", "Способ задают pešo, autobusom, vlakom, na bicykli; cestovať называет поездку шире."],
        ["3", "pôjdem выражает одно будущее перемещение; budem chodiť - регулярное."],
        ["4", "Маршрут строят prísť/odísť, nastúpiť/vystúpiť/prestúpiť и точные предлоги."],
    ], [14, 155], header=False),
    callout("Проверка освоения", "Я могу:  □ выбрать <i>ísť</i> или <i>chodiť</i>;  □ назвать способ передвижения;  □ описать пересадку;  □ рассказать привычный и завтрашний маршрут.", GREEN),
]

OUT.parent.mkdir(parents=True, exist_ok=True)
doc.build(story, onFirstPage=first_page, onLaterPages=later_page)
print(OUT)
