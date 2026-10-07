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
OUT = ROOT / "output" / "pdf" / "A2" / "Module_04" / "Slovak_A2_Tema_4_11_Modalnye_glagoly_v_uslovnykh_prosbakh_i_sovetakh.pdf"
TITLE = "Slovak A2 - Тема 4.11 - Модальные глаголы в условных просьбах и советах"

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
    "cover_title": ParagraphStyle("cover_title", fontName="SK-Bold", fontSize=21.5, leading=26, textColor=WHITE, alignment=TA_CENTER, spaceAfter=11),
    "cover_sub": ParagraphStyle("cover_sub", fontName="SK", fontSize=12.0, leading=16, textColor=WHITE, alignment=TA_CENTER),
    "h1": ParagraphStyle("h1", fontName="SK-Bold", fontSize=20, leading=24, textColor=PLUM, spaceAfter=8),
    "h2": ParagraphStyle("h2", fontName="SK-Bold", fontSize=13.5, leading=17, textColor=PLUM, spaceBefore=6, spaceAfter=5),
    "body": ParagraphStyle("body", fontName="SK", fontSize=9.45, leading=13.0, textColor=INK, spaceAfter=4),
    "small": ParagraphStyle("small", fontName="SK", fontSize=8.25, leading=11.25, textColor=MUTED, spaceAfter=2),
    "box": ParagraphStyle("box", fontName="SK", fontSize=9.0, leading=12.4, textColor=INK),
    "box_b": ParagraphStyle("box_b", fontName="SK-Bold", fontSize=9.35, leading=12.7, textColor=PLUM),
    "task": ParagraphStyle("task", fontName="SK", fontSize=8.4, leading=11.25, textColor=INK, spaceAfter=4),
    "answer": ParagraphStyle("answer", fontName="SK", fontSize=7.95, leading=10.45, textColor=INK, spaceAfter=3),
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
    canvas.setFont("SK-Bold", 10.5)
    canvas.drawCentredString(105 * mm, 57 * mm, "CHCEL BY SOM - MOHOL BY SOM - MAL BY SOM")
    canvas.setFont("SK", 9)
    canvas.drawCentredString(105 * mm, 47 * mm, "prosba, možnosť a jemná rada")
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
    canvas.drawString(20 * mm, 285 * mm, "SLOVOKROK  |  A2  |  ТЕМА 4.11  |  МОДАЛЬНЫЕ ГЛАГОЛЫ")
    canvas.setFillColor(MUTED)
    canvas.setFont("SK", 7.5)
    canvas.drawCentredString(105 * mm, 10 * mm, f"стр. {doc.page} / 7")
    canvas.restoreState()


doc = SimpleDocTemplate(
    str(OUT), pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm,
    topMargin=26 * mm, bottomMargin=17 * mm, title=TITLE,
    author="SlovoKrok", subject="Slovak A2 self-study module 4.11",
)
story = []

# 1. Cover
story += [
    Spacer(1, 21 * mm), P("SLOVOKROK • СЛОВАЦКИЙ A2", "cover_kicker"),
    P("ТЕМА 4.11", "cover_kicker"),
    P("Модальные глаголы<br/>в условных просьбах<br/>и советах", "cover_title"),
    P("Zdvorilá prosba, možnosť a jemná rada", "cover_sub"), Spacer(1, 12 * mm),
    Table(
        [[P("После модуля вы сможете", "box_b")],
         [P("• вежливо сообщить о желании или запросе;<br/>• попросить о действии и уточнить возможность;<br/>• дать мягкий совет без приказного тона;<br/>• выбрать между chcieť, môcť и mať в вопросе и отрицании.", "box")]],
        colWidths=[145 * mm],
        style=TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#FFF7FB")),
            ("LEFTPADDING", (0, 0), (-1, -1), 10), ("RIGHTPADDING", (0, 0), (-1, -1), 10),
            ("TOPPADDING", (0, 0), (-1, -1), 7), ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ]),
    ), PageBreak(),
]

# 2. Core contrast
story += [
    P("1. Три глагола - три намерения", "h1"),
    callout("Опора на тему 4.10", "Форма уже знакома: l-форма модального глагола + <b>by som/si/sme/ste</b> + инфинитив. Теперь главное не образование, а выбор значения: <i>chcel</i> - хочу, <i>mohol</i> - могу / возможно, <i>mal</i> - стоит / следует."),
    grid([
        ["Модель", "Главный смысл", "Типичный пример"],
        ["chcel by som", "желание, намерение, запрос", "Chcel by som si rezervovať izbu. - Я хотел бы забронировать номер."],
        ["mohol by som", "возможность или разрешение", "Mohol by som zaplatiť kartou? - Можно мне заплатить картой?"],
        ["mohli by ste", "вежливая просьба к адресату", "Mohli by ste mi pomôcť? - Вы не могли бы мне помочь?"],
        ["mal by som", "совет самому себе", "Mal by som viac oddychovať. - Мне стоило бы больше отдыхать."],
        ["mal by si / ste", "мягкий совет другому", "Mali by ste navštíviť lekára. - Вам стоило бы обратиться к врачу."],
    ], [39, 53, 77]),
    P("Chcieť: сообщить о своём намерении", "h2"),
    grid([
        ["Фраза", "Перевод"],
        ["Chcela by som zmeniť termín.", "Я хотела бы изменить дату."],
        ["Chceli by sme objednať stôl pre štyroch.", "Мы хотели бы заказать столик на четверых."],
        ["Chcel by som sa opýtať na cenu.", "Я хотел бы спросить о цене."],
    ], [82, 87]),
    callout("Не один русский перевод", "Русское «хотел бы» обычно ведёт к <i>chcel by som</i>. Но русское «не могли бы вы...» - это словацкое <i>mohli by ste / nemohli by ste</i>, а совет «вам бы...» - <i>mali by ste</i>.", CREAM),
    PageBreak(),
]

# 3. Questions and negation
story += [
    P("2. Вопрос и отрицание меняют тон", "h1"),
    P("Вопрос превращает модальную форму в предложение, просьбу или запрос совета. Отрицание присоединяется к l-форме: <i>nechcel, nemohol, nemal</i>."),
    grid([
        ["Форма", "Что делает", "Пример"],
        ["Chceli by ste...?", "предлагает / приглашает", "Chceli by ste kávu? - Хотите кофе?"],
        ["Mohol by som...?", "просит разрешение", "Mohol by som tu počkať? - Можно мне здесь подождать?"],
        ["Mohli by ste...?", "просит адресата", "Mohli by ste hovoriť pomalšie? - Не могли бы вы говорить медленнее?"],
        ["Mal by som...?", "просит совета", "Mal by som zavolať lekárovi? - Мне стоит позвонить врачу?"],
        ["Nemohli by ste...?", "делает просьбу особенно мягкой", "Nemohli by ste to zopakovať? - Не могли бы вы это повторить?"],
        ["Nemal by si...?", "мягко подталкивает к совету", "Nemal by si si oddýchnuť? - Может, тебе стоит отдохнуть?"],
    ], [43, 54, 72]),
    callout("Отрицательный вопрос не равен отказу", "В просьбе <i>Nemohli by ste mi pomôcť?</i> говорящий не утверждает, что собеседник не может. Такая форма снижает давление. Но <i>Nemohol by som prísť</i> без вопроса обычно значит «я не смог бы прийти».", BLUE),
    P("Согласование сохраняется", "h2"),
    grid([
        ["Мужчина", "Женщина", "Перевод"],
        ["Chcel by som odísť.", "Chcela by som odísť.", "Я хотел / хотела бы уйти."],
        ["Mohol by som prísť.", "Mohla by som prísť.", "Я мог / могла бы прийти."],
        ["Mal by som zavolať.", "Mala by som zavolať.", "Мне стоило бы позвонить."],
    ], [57, 57, 55]),
    PageBreak(),
]

# 4. Meaning contrasts
story += [
    P("3. Просьба, возможность или совет?", "h1"),
    grid([
        ["Ситуация", "Естественная фраза", "Почему"],
        ["вы сообщаете о запросе", "Chcel by som potvrdenie.", "ваше желание / потребность"],
        ["вы просите действие", "Mohli by ste mi poslať potvrdenie?", "возможность адресата = вежливая просьба"],
        ["вы уточняете разрешение", "Mohol by som odísť skôr?", "возможность для говорящего"],
        ["вы советуете", "Mali by ste si uložiť kópiu.", "рекомендация, не приказ"],
        ["вы предлагаете вместе", "Mohli by sme sa stretnúť zajtra.", "реальная возможность / предложение"],
    ], [44, 72, 53]),
    callout("Сравните силу", "<i>Pošlite mi potvrdenie.</i> - прямая инструкция.<br/><i>Mohli by ste mi poslať potvrdenie?</i> - вежливая просьба.<br/><i>Mali by ste mi poslať potvrdenie.</i> - совет или ожидание; для обычной просьбы звучит неуместно.", CREAM),
    P("Мини-диалог: перенос записи", "h2"),
    callout("Telefonát do ambulancie", "<b>Pacientka:</b> Dobrý deň. Chcela by som zmeniť termín.<br/><b>Sestra:</b> Mohli by ste prísť v piatok o desiatej?<br/><b>Pacientka:</b> Mohla by som prísť až poobede?<br/><b>Sestra:</b> Áno. Mali by ste však prísť aspoň desať minút skôr.<br/><b>Pacientka:</b> Dobre. Mohli by ste mi, prosím, poslať potvrdenie?<br/><br/><b>Перевод:</b> Пациентка: Добрый день. Я хотела бы изменить время. Медсестра: Вы могли бы прийти в пятницу в десять? Пациентка: Я могла бы прийти только после обеда? Медсестра: Да. Но вам стоит прийти хотя бы на десять минут раньше. Пациентка: Хорошо. Не могли бы вы прислать мне подтверждение?", PALE),
    P("Короткие формы держатся группой", "h2"),
    grid([
        ["Модель", "Пример"],
        ["by som + sa", "Chcel by som sa objednať."],
        ["by ste + mi + to", "Mohli by ste mi to poslať?"],
        ["by si + si", "Mal by si si oddýchnuť."],
        ["by sme + sa", "Mohli by sme sa porozprávať."],
    ], [57, 112]),
    PageBreak(),
]

# 5. Phrase bank
story += [
    P("4. Готовые модели для реальных ситуаций", "h1"),
    P("Запоминайте не отдельный глагол, а готовую рамку с инфинитивом и нужными короткими формами."),
    P("Сервис и бронирование", "h2"),
    grid([
        ["Словацкий", "Русский"],
        ["Chcel by som rezervovať dvojlôžkovú izbu.", "Я хотел бы забронировать двухместный номер."],
        ["Chcela by som si zmeniť rezerváciu.", "Я хотела бы изменить своё бронирование."],
        ["Mohli by ste mi poslať faktúru?", "Не могли бы вы прислать мне счёт?"],
        ["Nemohli by ste skontrolovať číslo izby?", "Не могли бы вы проверить номер комнаты?"],
    ], [84, 85]),
    P("Работа и договорённости", "h2"),
    grid([
        ["Словацкий", "Русский"],
        ["Chceli by sme sa dohodnúť na termíne.", "Мы хотели бы договориться о сроке."],
        ["Mohli by sme začať o deviatej.", "Мы могли бы начать в девять."],
        ["Mohli by ste mi ukázať nový súbor?", "Не могли бы вы показать мне новый файл?"],
        ["Mali by sme najprv skontrolovať údaje.", "Нам стоит сначала проверить данные."],
    ], [84, 85]),
    P("Советы и забота", "h2"),
    grid([
        ["Словацкий", "Русский"],
        ["Mal by si viac spať.", "Тебе стоит больше спать."],
        ["Mala by si piť viac vody.", "Тебе стоит пить больше воды. (к женщине)"],
        ["Mali by ste sa poradiť s lekárom.", "Вам стоит посоветоваться с врачом."],
        ["Nemali by sme už odísť?", "Может, нам уже стоит уйти?"],
    ], [84, 85]),
    callout("Одна форма - разная функция", "<i>Mohli by ste prísť zajtra?</i> может быть вопросом о возможности или вежливой просьбой прийти. Решает ситуация. <i>Prosím</i> и причина делают намерение яснее: <i>Mohli by ste prísť zajtra, prosím? Potrebujeme podpísať zmluvu.</i>", BLUE),
    PageBreak(),
]

# 6. Exercises
story += [
    P("5 - Ошибки и практика", "h1"),
    callout("Частые ошибки", "1) путать просьбу и совет; 2) *<i>môžem by</i> вместо <i>mohol by som</i>; 3) забывать инфинитив; 4) терять род: *<i>chcel by som</i> от женщины; 5) ставить <i>ne</i> отдельно; 6) разрывать <i>by ste mi</i> тяжёлыми словами.", CREAM),
    P("<b>1. Определите функцию: желание, возможность, просьба или совет.</b><br/>a) Chcela by som zmeniť termín. b) Mohli by ste mi pomôcť? c) Mal by si viac spať. d) Mohol by som tu počkať? e) Mali by sme skontrolovať údaje.", "task"),
    P("<b>2. Выберите chcel, mohol или mal и согласуйте.</b><br/>a) Ja, žena: ___ by som sa objednať. b) Vy: ___ by ste mi to poslať? c) Ty, muž: ___ by si viac oddychovať. d) My: ___ by sme začať skôr.", "task"),
    P("<b>3. Сделайте вопрос или отрицательный вопрос.</b><br/>a) Vy mi pošlete faktúru. b) Ty mi pomôžeš. c) Ja tu počkám. d) My už odídeme.", "task"),
    P("<b>4. Исправьте.</b><br/>a) *Môžem by som zaplatiť kartou? b) *Ne mohli by ste to zopakovať? c) *Mali by ste mi poslať účet? - нужна просьба. d) *Chcel by som zmeniť termín. - говорит женщина. e) *Mal by si oddýchol.", "task"),
    P("<b>5. Переведите.</b><br/>a) Я хотела бы изменить бронирование. b) Не могли бы вы говорить медленнее? c) Мне стоит позвонить врачу? d) Нам стоит сначала проверить данные. e) Может, нам встретиться завтра?", "task"),
    P("<b>6. Мини-диалог.</b> Напишите 6-8 реплик для гостиницы, офиса или врача. Используйте <i>chcel by som</i>, просьбу с <i>mohli by ste</i>, один отрицательный вопрос и совет с <i>mal by</i>.", "task"),
    PageBreak(),
]

# 7. Answers
story += [
    P("6. Ответы и итог", "h1"),
    P("<b>1.</b> a) желание / запрос; b) просьба; c) совет; d) возможность / разрешение; e) совет или предложение совместного действия.", "answer"),
    P("<b>2.</b> a) Chcela by som sa objednať. b) Mohli by ste mi to poslať? c) Mal by si viac oddychovať. d) Mohli by sme začať skôr.", "answer"),
    P("<b>3.</b> Возможные ответы: a) Mohli by ste mi poslať faktúru? / Nemohli by ste mi poslať faktúru? b) Mohol by si mi pomôcť? c) Mohol by som tu počkať? d) Nemali by sme už odísť?", "answer"),
    P("<b>4.</b> a) Mohol by som zaplatiť kartou? b) Nemohli by ste to zopakovať? c) Mohli by ste mi poslať účet? d) Chcela by som zmeniť termín. e) Mal by si oddychovať.", "answer"),
    P("<b>5.</b> a) Chcela by som si zmeniť rezerváciu. b) Nemohli by ste hovoriť pomalšie? c) Mal by som zavolať lekárovi? d) Mali by sme najprv skontrolovať údaje. e) Mohli by sme sa stretnúť zajtra?", "answer"),
    P("Образец к заданию 6", "h2"),
    callout("V hoteli", "<b>Hosť:</b> Dobrý deň. Chcel by som si rezervovať izbu na dve noci.<br/><b>Recepčná:</b> Samozrejme. Chceli by ste izbu s raňajkami?<br/><b>Hosť:</b> Áno. Mohli by ste mi, prosím, povedať cenu?<br/><b>Recepčná:</b> Je to 90 eur za noc.<br/><b>Hosť:</b> Nemohli by ste mi poslať potvrdenie e-mailom?<br/><b>Recepčná:</b> Iste. Mali by ste ho dostať do desiatich minút.<br/><br/><b>Перевод:</b> Гость: Добрый день. Я хотел бы забронировать номер на две ночи. Администратор: Конечно. Хотите номер с завтраком? Гость: Да. Не могли бы вы сказать цену? Администратор: 90 евро за ночь. Гость: Не могли бы вы прислать подтверждение по электронной почте? Администратор: Конечно. Подтверждение должно прийти в течение десяти минут.", BLUE),
    P("Четыре опоры", "h2"),
    grid([
        ["1", "Chcel by som сообщает о желании, намерении или запросе."],
        ["2", "Mohol by som спрашивает о возможности; mohli by ste часто оформляет просьбу."],
        ["3", "Mal by som / si / ste даёт мягкий совет или запрашивает рекомендацию."],
        ["4", "Отрицание пишется слитно: nechcel, nemohol, nemal; вопрос определяет функцию."],
    ], [14, 155], header=False),
    callout("Проверка освоения", "Я могу:  □ сообщить о желании;  □ попросить о действии;  □ уточнить возможность;  □ дать мягкий совет и выбрать уместное отрицание.", GREEN),
]

OUT.parent.mkdir(parents=True, exist_ok=True)
doc.build(story, onFirstPage=first_page, onLaterPages=later_page)
print(OUT)
