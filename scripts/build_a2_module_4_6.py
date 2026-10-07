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
OUT = ROOT / "output" / "pdf" / "A2" / "Module_04" / "Slovak_A2_Tema_4_6_Sinteticheskoe_budushchee_sovershennyh_glagolov.pdf"
TITLE = "Slovak A2 - Тема 4.6 - Синтетическое будущее совершенных глаголов"

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
    "body": ParagraphStyle("body", fontName="SK", fontSize=9.5, leading=13.1, textColor=INK, spaceAfter=4),
    "small": ParagraphStyle("small", fontName="SK", fontSize=8.4, leading=11.5, textColor=MUTED, spaceAfter=2),
    "box": ParagraphStyle("box", fontName="SK", fontSize=9.1, leading=12.6, textColor=INK),
    "box_b": ParagraphStyle("box_b", fontName="SK-Bold", fontSize=9.4, leading=12.8, textColor=PLUM),
    "ex": ParagraphStyle("ex", fontName="SK", fontSize=9.05, leading=12.35, textColor=INK, leftIndent=6, spaceAfter=3),
    "task": ParagraphStyle("task", fontName="SK", fontSize=8.55, leading=11.55, textColor=INK, spaceAfter=4),
    "answer": ParagraphStyle("answer", fontName="SK", fontSize=8.15, leading=10.85, textColor=INK, spaceAfter=3),
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
    canvas.drawCentredString(105 * mm, 57 * mm, "NAPÍŠEM = НАПИШУ И ПОЛУЧУ РЕЗУЛЬТАТ")
    canvas.setFont("SK", 9)
    canvas.drawCentredString(105 * mm, 47 * mm, "dokonavý tvar = budúca hranica alebo výsledok")
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
    canvas.drawString(20 * mm, 285 * mm, "SLOVOKROK  |  A2  |  ТЕМА 4.6  |  СОВЕРШЕННОЕ БУДУЩЕЕ")
    canvas.setFillColor(MUTED)
    canvas.setFont("SK", 7.5)
    canvas.drawCentredString(105 * mm, 10 * mm, f"стр. {doc.page} / 7")
    canvas.restoreState()


doc = SimpleDocTemplate(
    str(OUT), pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm,
    topMargin=26 * mm, bottomMargin=17 * mm, title=TITLE,
    author="SlovoKrok", subject="Slovak A2 self-study module 4.6",
)
story = []

# 1. Cover
story += [
    Spacer(1, 23 * mm), P("SLOVOKROK • СЛОВАЦКИЙ A2", "cover_kicker"),
    P("ТЕМА 4.6", "cover_kicker"),
    P("Синтетическое будущее<br/>совершенных глаголов", "cover_title"),
    P("Jednoduché futúrum dokonavých slovies", "cover_sub"), Spacer(1, 14 * mm),
    Table(
        [[P("После модуля вы сможете", "box_b")],
         [P("• узнавать будущее значение у форм совершенного глагола;<br/>• выражать одно завершённое действие и полученный результат;<br/>• строить отрицание, вопрос и формы с <i>sa</i>;<br/>• выбирать между <i>budem písať</i> и <i>napíšem</i> по смыслу.", "box")]],
        colWidths=[145 * mm],
        style=TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#FFF7FB")),
            ("LEFTPADDING", (0, 0), (-1, -1), 10), ("RIGHTPADDING", (0, 0), (-1, -1), 10),
            ("TOPPADDING", (0, 0), (-1, -1), 7), ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ]),
    ), PageBreak(),
]

# 2. Core rule and forms
story += [
    P("1. Форма настоящая, значение будущее", "h1"),
    P("У совершенного глагола личные формы выглядят как настоящее время, но обычно обозначают будущую границу или результат. Вспомогательный глагол <i>budem</i> не нужен."),
    grid([
        ["Лицо", "napísať", "Пример"],
        ["ja", "napíšem", "Zajtra napíšem e-mail.<br/>Завтра я напишу письмо."],
        ["ty", "napíšeš", "Večer napíšeš odpoveď.<br/>Вечером ты напишешь ответ."],
        ["on / ona / ono", "napíše", "Mária napíše správu.<br/>Мария напишет сообщение."],
        ["my", "napíšeme", "Napíšeme krátky plán.<br/>Мы напишем короткий план."],
        ["vy", "napíšete", "Napíšete svoje meno.<br/>Вы напишете своё имя."],
        ["oni / ony", "napíšu", "Napíšu všetky údaje.<br/>Они запишут все данные."],
    ], [39, 45, 85]),
    callout("Главная формула", "<b>Совершенный инфинитив -> личная форма без budem -> будущий результат.</b> Например: <i>zavolať -> zavolám</i>, <i>urobiť -> urobím</i>, <i>stretnúť sa -> stretneme sa</i>.", GREEN),
    callout("Не называйте это настоящим действием", "<i>Teraz napíšem e-mail.</i> означает «Сейчас я напишу письмо», то есть действие начнётся и завершится. «Сейчас я пишу письмо» будет <i>Teraz píšem e-mail.</i>", CREAM),
    P("Частотные модели", "h2"),
    P("<b>Zavolám ti po práci.</b> - Я позвоню тебе после работы.", "ex"),
    P("<b>Urobíme to zajtra.</b> - Мы сделаем это завтра.", "ex"),
    PageBreak(),
]

# 3. Three models, negation and question
story += [
    P("2. napíšem, zavolám, stretneme sa", "h1"),
    P("Окончания зависят от модели глагола, поэтому новую пару и её форму 1-го лица полезно хранить вместе. Ниже три частотных образца из дорожной карты."),
    grid([
        ["Лицо", "napísať", "zavolať", "stretnúť sa"],
        ["ja", "napíšem", "zavolám", "stretnem sa"],
        ["ty", "napíšeš", "zavoláš", "stretneš sa"],
        ["on / ona", "napíše", "zavolá", "stretne sa"],
        ["my", "napíšeme", "zavoláme", "stretneme sa"],
        ["vy", "napíšete", "zavoláte", "stretnete sa"],
        ["oni / ony", "napíšu", "zavolajú", "stretnú sa"],
    ], [30, 43, 43, 53]),
    P("Отрицание", "h2"),
    P("<b>Dnes mu nenapíšem.</b> - Я не напишу ему сегодня.", "ex"),
    P("<b>Eva večer nezavolá.</b> - Эва вечером не позвонит.", "ex"),
    P("<b>Zajtra sa nestretneme.</b> - Завтра мы не встретимся.", "ex"),
    P("В отрицании <b>ne-</b> присоединяется к самому глаголу. Формы *<i>nebudem napísať</i> и *<i>budem nenapísať</i> неверны."),
    P("Вопрос", "h2"),
    P("<b>Kedy mi zavoláš?</b> - Когда ты мне позвонишь?", "ex"),
    P("<b>Napíšete nám adresu?</b> - Вы напишете нам адрес?", "ex"),
    P("<b>Stretneme sa v stredu?</b> - Мы встретимся в среду?", "ex"),
    callout("Положение sa", "Если форма первая, говорим <i>Stretneme sa o šiestej.</i> После начального обстоятельства: <i>Zajtra sa stretneme o šiestej.</i> Подробные значения <i>sa/si</i> будут в теме 4.8.", BLUE),
    PageBreak(),
]

# 4. Aspect contrast
story += [
    P("3. Процесс или результат", "h1"),
    P("Выбор между аналитическим и синтетическим будущим зависит не от длины действия, а от точки зрения: будущая деятельность или достигнутая граница."),
    grid([
        ["Будущий процесс", "Будущий результат"],
        ["Budem písať správu.<br/>Я буду писать отчёт.", "Napíšem správu.<br/>Я напишу отчёт."],
        ["Bude telefonovať klientom.<br/>Он будет звонить клиентам.", "Zavolá jednému klientovi.<br/>Он позвонит одному клиенту."],
        ["Budeme robiť večeru.<br/>Мы будем готовить ужин.", "Urobíme večeru.<br/>Мы приготовим ужин."],
        ["Budeme sa stretávať každý týždeň.<br/>Мы будем встречаться каждую неделю.", "Stretneme sa v stredu.<br/>Мы встретимся в среду."],
        ["Budem čítať článok.<br/>Я буду читать статью.", "Prečítam článok.<br/>Я прочитаю статью."],
    ], [84.5, 84.5]),
    P("Длительность и предел", "h2"),
    P("<b>Dve hodiny budem písať správu.</b> - Я буду писать отчёт два часа: важен процесс.", "ex"),
    P("<b>Správu napíšem do dvoch hodín.</b> - Я напишу отчёт в течение двух часов: важен готовый результат.", "ex"),
    callout("Повтор тоже может иметь границу", "<i>Každý deň prečítam jednu kapitolu.</i> - Каждый день я прочитаю по одной главе. Повторяется не бесконечный процесс, а отдельный законченный результат. Маркер повторяемости сам по себе не выбирает вид.", GREEN),
    callout("Надёжный вопрос", "Если важно <b>что будет происходить?</b>, выбирайте несовершенный процесс. Если важно <b>что будет сделано?</b>, выбирайте совершенный результат.", PALE),
    PageBreak(),
]

# 5. Connected plan
story += [
    P("4. Цепочка будущих результатов", "h1"),
    P("Совершенные формы хорошо организуют план как последовательность законченных шагов. Связки <i>najprv, potom, nakoniec</i> делают границы видимыми."),
    callout(
        "Zajtrajší plán",
        "Zajtra vybavím niekoľko vecí. Ráno zavolám lekárovi a objednám sa na kontrolu. Potom napíšem e-mail vedúcej a pošlem jej dokumenty. O dvanástej sa stretnem s kolegom. Po práci kúpim potraviny a uvarím večeru. Nakoniec si pripravím plán na ďalší deň.<br/><br/><b>Перевод:</b> Завтра я решу несколько дел. Утром позвоню врачу и запишусь на осмотр. Потом напишу письмо руководительнице и отправлю ей документы. В двенадцать встречусь с коллегой. После работы куплю продукты и приготовлю ужин. Наконец подготовлю план на следующий день.",
        BLUE,
    ),
    P("Мини-диалог", "h2"),
    callout("Po práci", "<b>Anna:</b> Kedy mi zavoláš?<br/><b>Peter:</b> Zavolám ti po práci. Najprv dokončím správu a pošlem ju vedúcej.<br/><b>Anna:</b> Stretneme sa potom v centre?<br/><b>Peter:</b> Áno, stretneme sa o šiestej.<br/><b>Anna:</b> Dobre. Napíšem ti, kde budem čakať.<br/><br/><b>Перевод:</b> Анна: Когда ты мне позвонишь? Петер: После работы. Сначала закончу отчёт и отправлю его руководительнице. Анна: Потом встретимся в центре? Петер: Да, в шесть. Анна: Хорошо. Я напишу тебе, где буду ждать.", PALE),
    P("Результат и будущий фон", "h2"),
    P("В одном плане виды могут сочетаться: <b>Kým budeš čakať, zavolám lekárovi.</b> - Пока ты будешь ждать, я позвоню врачу.", "ex"),
    P("<b>Večer budem oddychovať, ale najprv upracem kuchyňu.</b> - Вечером буду отдыхать, но сначала уберу кухню.", "ex"),
    callout("Граница с темой 4.7", "Формы движения <i>pôjdem, prídem, odídem</i> имеют собственные важные противопоставления. Здесь они не систематизируются: следующий модуль отдельно разбирает <i>ísť/chodiť</i> и направление движения.", CREAM),
    PageBreak(),
]

# 6. Exercises
story += [
    P("5. Ошибки и практика", "h1"),
    callout("Частые ошибки", "1) добавлять budem к совершенному инфинитиву: *budem napísať; 2) понимать napíšem как действие прямо сейчас; 3) выбирать вид только по слову zajtra; 4) терять ne- в отрицании; 5) ставить sa в конец; 6) путать будущую деятельность и обещанный результат.", CREAM),
    P("<b>1. Процесс или результат?</b><br/>a) Budem písať správu. b) Napíšem správu. c) Budeme sa stretávať každý týždeň. d) Stretneme sa v piatok. e) Prečítam dve kapitoly.", "task"),
    P("<b>2. Дополните форму.</b><br/>a) ja: napísať -> ___ b) ty: zavolať -> ___ c) Eva: urobiť -> ___ d) my: stretnúť sa -> ___ e) vy: prečítať -> ___ f) deti: upratať -> ___", "task"),
    P("<b>3. Выберите форму.</b><br/>a) Zajtra dve hodiny <i>(budem písať / napíšem)</i> správu.<br/>b) Správu <i>(budem písať / napíšem)</i> do obeda.<br/>c) Každý deň <i>(budem čítať / prečítam)</i> jednu kapitolu do konca.<br/>d) V stredu sa <i>(budeme stretávať / stretneme)</i> o šiestej.", "task"),
    P("<b>4. Сделайте отрицание или вопрос.</b><br/>a) Zavolám Petrovi. -> отрицание.<br/>b) Napíšete odpoveď. -> вопрос.<br/>c) Zajtra sa stretneme. -> отрицание.<br/>d) Urobíš to večer. -> вопрос с <i>kedy</i>.", "task"),
    P("<b>5. Переведите.</b><br/>a) Завтра я напишу письмо.<br/>b) Мы встретимся в среду в шесть.<br/>c) Эва не позвонит клиенту.<br/>d) Сначала я закончу отчёт, потом отправлю его.<br/>e) Я буду читать статью два часа, но закончу её вечером.", "task"),
    P("<b>6. План результатов.</b> Напишите 6-8 предложений о завтрашнем дне: четыре завершённых шага, одно отрицание, один вопрос и один контраст процесса с результатом.", "task"),
    PageBreak(),
]

# 7. Answers
story += [
    P("6. Ответы и итог", "h1"),
    P("<b>1.</b> a) процесс; b) результат; c) повторяющийся процесс; d) одно завершённое событие; e) измеримый результат.", "answer"),
    P("<b>2.</b> a) <b>napíšem</b>; b) <b>zavoláš</b>; c) <b>urobí</b>; d) <b>stretneme sa</b>; e) <b>prečítate</b>; f) <b>upracú</b>.", "answer"),
    P("<b>3.</b> a) <b>budem písať</b> - длительность процесса; b) <b>napíšem</b> - результат к сроку; c) <b>prečítam</b> - по одной законченной главе; d) <b>stretneme</b> - одна встреча.", "answer"),
    P("<b>4.</b> a) Petrovi <b>nezavolám</b>. b) <b>Napíšete odpoveď?</b> c) Zajtra sa <b>nestretneme</b>. d) <b>Kedy to urobíš?</b>", "answer"),
    P("<b>5.</b> a) Zajtra napíšem list. b) Stretneme sa v stredu o šiestej. c) Eva nezavolá klientovi. d) Najprv dokončím správu, potom ju pošlem. e) Dve hodiny budem čítať článok, ale večer ho prečítam do konca.", "answer"),
    P("Образец к заданию 6", "h2"),
    callout("Zajtra", "Zajtra ráno napíšem dôležitý e-mail. Potom zavolám lekárovi a objednám sa na kontrolu. Petrovi nezavolám, pretože je na dovolenke. O dvanástej sa stretnem s kolegyňou. Popoludní budem pripravovať prezentáciu a večer ju dokončím. Nakoniec pošlem všetky dokumenty. Kedy mi odpovie vedúca?<br/><br/>Завтра утром я напишу важное письмо. Потом позвоню врачу и запишусь на осмотр. Петеру звонить не буду, потому что он в отпуске. В двенадцать встречусь с коллегой. После обеда буду готовить презентацию, а вечером закончу её. Наконец отправлю все документы. Когда мне ответит руководительница?", BLUE),
    P("Четыре опоры", "h2"),
    grid([
        ["1", "У совершенного глагола форма настоящего типа обычно имеет будущее значение."],
        ["2", "Budem не добавляется: napíšem, zavolám, urobíme, stretneme sa."],
        ["3", "Отрицание присоединяется к глаголу: nenapíšem, nezavolá, nestretneme sa."],
        ["4", "Budem písať показывает процесс; napíšem показывает будущую границу и результат."],
    ], [14, 155], header=False),
    callout("Проверка освоения", "Я могу:  □ узнать будущее значение совершенной формы;  □ построить отрицание и вопрос;  □ выбрать процесс или результат;  □ рассказать о завтрашнем дне как о цепочке законченных шагов.", GREEN),
]

OUT.parent.mkdir(parents=True, exist_ok=True)
doc.build(story, onFirstPage=first_page, onLaterPages=later_page)
print(OUT)
