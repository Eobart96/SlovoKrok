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
OUT = ROOT / "output" / "pdf" / "A2" / "Module_04" / "Slovak_A2_Tema_4_9_Imperativ_prosba_instruktsiya_i_zapret.pdf"
TITLE = "Slovak A2 - Тема 4.9 - Императив: просьба, инструкция и запрет"

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
    "cover_title": ParagraphStyle("cover_title", fontName="SK-Bold", fontSize=23, leading=28, textColor=WHITE, alignment=TA_CENTER, spaceAfter=11),
    "cover_sub": ParagraphStyle("cover_sub", fontName="SK", fontSize=12.2, leading=17, textColor=WHITE, alignment=TA_CENTER),
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
    canvas.setFont("SK-Bold", 11)
    canvas.drawCentredString(105 * mm, 57 * mm, "OTVOR - OTVORME - OTVORTE")
    canvas.setFont("SK", 9)
    canvas.drawCentredString(105 * mm, 47 * mm, "jasná výzva, zdvorilá prosba a zákaz")
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
    canvas.drawString(20 * mm, 285 * mm, "SLOVOKROK  |  A2  |  ТЕМА 4.9  |  ИМПЕРАТИВ")
    canvas.setFillColor(MUTED)
    canvas.setFont("SK", 7.5)
    canvas.drawCentredString(105 * mm, 10 * mm, f"стр. {doc.page} / 7")
    canvas.restoreState()


doc = SimpleDocTemplate(
    str(OUT), pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm,
    topMargin=26 * mm, bottomMargin=17 * mm, title=TITLE,
    author="SlovoKrok", subject="Slovak A2 self-study module 4.9",
)
story = []

# 1. Cover
story += [
    Spacer(1, 23 * mm), P("SLOVOKROK • СЛОВАЦКИЙ A2", "cover_kicker"),
    P("ТЕМА 4.9", "cover_kicker"),
    P("Императив: просьба,<br/>инструкция и запрет", "cover_title"),
    P("Rozkaz, návod, prosba a zákaz", "cover_sub"), Spacer(1, 14 * mm),
    Table(
        [[P("После модуля вы сможете", "box_b")],
         [P("• дать команду одному человеку, группе или включить себя;<br/>• употребить частотные неправильные формы;<br/>• выбрать вид и построить запрет с <i>ne-</i>;<br/>• превратить прямую команду в уместную просьбу или инструкцию.", "box")]],
        colWidths=[145 * mm],
        style=TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#FFF7FB")),
            ("LEFTPADDING", (0, 0), (-1, -1), 10), ("RIGHTPADDING", (0, 0), (-1, -1), 10),
            ("TOPPADDING", (0, 0), (-1, -1), 7), ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ]),
    ), PageBreak(),
]

# 2. Persons and productive patterns
story += [
    P("1. Кому адресована инструкция?", "h1"),
    callout("Три рабочие формы", "Словацкий императив имеет простые формы для <b>ty</b>, совместного <b>my</b> и <b>vy</b>. Форма <i>vy</i> обращена и к группе, и вежливо к одному человеку."),
    grid([
        ["Адресат", "читать", "открыть", "Смысл"],
        ["ty", "čítaj", "otvor", "читай / открой"],
        ["my", "čítajme", "otvorme", "давайте читать / откроем"],
        ["vy / Вы", "čítajte", "otvorte", "читайте / откройте"],
    ], [30, 43, 43, 53]),
    P("Частотные модели", "h2"),
    grid([
        ["Модель", "ty", "my", "vy / Вы"],
        ["čakať", "čakaj", "čakajme", "čakajte"],
        ["pracovať", "pracuj", "pracujme", "pracujte"],
        ["písať", "píš", "píšme", "píšte"],
        ["robiť", "rob", "robme", "robte"],
        ["zapnúť", "zapni", "zapnime", "zapnite"],
        ["zostať", "zostaň", "zostaňme", "zostaňte"],
    ], [43, 42, 42, 42]),
    callout("Как учить надёжно", "Форму <i>ty</i> нельзя всегда получить простым отрезанием <i>-ť</i>. Удобно учить тройку целиком: <i>píš - píšme - píšte</i>, <i>zapni - zapnime - zapnite</i>.", CREAM),
    P("Форма my приглашает к совместному действию", "h2"),
    P("<b>Začnime o deviatej.</b> - Давайте начнём в девять."),
    P("<b>Skontrolujme výsledky.</b> - Давайте проверим результаты."),
    P("<b>Poďme domov.</b> - Пойдёмте домой."),
    PageBreak(),
]

# 3. Irregular and reflexive forms
story += [
    P("2. Неправильные и частотные формы", "h1"),
    P("Эти формы встречаются постоянно, но плохо предсказываются по инфинитиву. Запоминайте их как готовые серии."),
    grid([
        ["Инфинитив", "ty", "my", "vy / Вы"],
        ["byť", "buď", "buďme", "buďte"],
        ["mať", "maj", "majme", "majte"],
        ["dať", "daj", "dajme", "dajte"],
        ["jesť", "jedz", "jedzme", "jedzte"],
        ["vedieť", "vedz", "vedzme", "vedzte"],
        ["vziať", "vezmi", "vezmime", "vezmite"],
        ["povedať", "povedz", "povedzme", "povedzte"],
        ["prísť", "príď", "príďme", "príďte"],
        ["ísť", "choď / poď", "choďme / poďme", "choďte / poďte"],
    ], [43, 42, 42, 42]),
    callout("Choď или poď?", "<i>Choď</i> обычно направляет адресата прочь или к цели: <i>Choď domov.</i> <i>Poď</i> приглашает двигаться к говорящему или вместе с ним: <i>Poď sem. Poďme spolu.</i>", BLUE),
    P("Готовые реплики", "h2"),
    grid([
        ["Фраза", "Перевод"],
        ["Buď opatrný!", "Будь осторожен!"],
        ["Majte sa pekne!", "Всего доброго!"],
        ["Dajte mi, prosím, účet.", "Дайте мне, пожалуйста, счёт."],
        ["Povedzte mi svoje meno.", "Скажите мне своё имя."],
        ["Vezmite si jednu tabletu.", "Примите одну таблетку."],
        ["Príďte o desať minút.", "Придите через десять минут."],
    ], [86, 83]),
    P("Sa/si сохраняет естественное место", "h2"),
    P("<b>Posaď sa. Posaďte sa. Daj si čaj. Vezmite si formulár. Neboj sa.</b> Короткая форма идёт после императива; отрицание присоединяется к глаголу."),
    PageBreak(),
]

# 4. Aspect and negation
story += [
    P("3. Вид в команде и запрет с ne-", "h1"),
    P("В положительной инструкции вид помогает выбрать между результатом и процессом. Это смысловой выбор, а не механическое правило."),
    grid([
        ["Нужен результат / граница", "Нужен процесс / способ"],
        ["<b>Napíš adresu.</b><br/>Напиши адрес.", "<b>Píš čitateľne.</b><br/>Пиши разборчиво."],
        ["<b>Prečítajte celý text.</b><br/>Прочитайте весь текст.", "<b>Čítajte potichu.</b><br/>Читайте тихо."],
        ["<b>Zavolajte mi večer.</b><br/>Позвоните мне вечером.", "<b>Čakajte tu.</b><br/>Ждите здесь."],
        ["<b>Skontroluj odpoveď.</b><br/>Проверь ответ.", "<b>Kontroluj údaje priebežne.</b><br/>Проверяй данные регулярно."],
    ], [84.5, 84.5]),
    callout("Положительная команда", "Для одного ожидаемого результата часто естественен совершенный глагол: <i>otvor, napíš, prečítaj</i>. Для длительности, повторения и способа действия - несовершенный: <i>čakaj, píš pomaly, čítaj nahlas</i>.", BLUE),
    P("Запрет: ne- пишется слитно", "h2"),
    grid([
        ["Тип запрета", "Пример", "Перевод"],
        ["общий / процесс", "Nehovorte nahlas.", "Не говорите громко."],
        ["общий / повтор", "Neotvárajte tieto dvere.", "Не открывайте эту дверь."],
        ["один нежелательный результат", "Nezabudnite si lístok.", "Не забудьте билет."],
        ["предупреждение", "Dávaj pozor, nespadni!", "Осторожно, не упади!"],
        ["частотная готовая форма", "Nechoď tam sám.", "Не ходи туда один."],
    ], [47, 65, 57]),
    callout("Тенденция, не запрет на вид", "В общих запретах часто встречается несовершенный вид: <i>nefajčite, nehovorte, neotvárajte</i>. Совершенный вид возможен, когда предотвращается один результат: <i>nezabudni, nespadni</i>.", CREAM),
    P("С sa/si", "h2"),
    P("<b>Neboj sa. Neponáhľajte sa. Nezabudnite si doklady.</b> - Не бойся. Не спешите. Не забудьте документы."),
    PageBreak(),
]

# 5. Politeness and instructions
story += [
    P("4. От приказа к уместной просьбе", "h1"),
    P("Одна и та же форма императива может звучать как приказ или просьба. Вежливость создают форма <i>vy</i>, <i>prosím</i>, обращение и спокойный контекст."),
    grid([
        ["Прямо", "Мягче и уместнее"],
        ["Zopakujte to.", "Zopakujte to, prosím."],
        ["Počkajte.", "Počkajte chvíľu, prosím."],
        ["Povedzte mi adresu.", "Prepáčte, povedzte mi, prosím, adresu."],
        ["Sadnite si.", "Nech sa páči, sadnite si."],
        ["Ukážte mi pas.", "Môžete mi ukázať pas?"],
    ], [68, 101]),
    callout("Vy: группа и вежливое Вы", "<i>Otvorte knihy.</i> может быть обращением к группе. <i>Otvorte dvere, prosím.</i> может быть вежливой просьбой одному незнакомому человеку. Ситуация и обращение снимают двусмысленность.", BLUE),
    P("Инструкция в аптеке", "h2"),
    callout("Ako užívať liek", "Najprv si prečítajte návod. Vezmite si jednu tabletu po jedle a zapite ju vodou. Neužívajte viac ako dve tablety denne. Ak sa necítite lepšie, zavolajte lekárovi.<br/><br/><b>Перевод:</b> Сначала прочитайте инструкцию. Примите одну таблетку после еды и запейте её водой. Не принимайте больше двух таблеток в день. Если вам не лучше, позвоните врачу.", PALE),
    P("Мини-диалог в офисе", "h2"),
    callout("Nová úloha", "<b>Vedúca:</b> Prosím, otvorte tento súbor a skontrolujte údaje.<br/><b>Peter:</b> Mám opraviť aj adresy?<br/><b>Vedúca:</b> Áno, opravte ich a potom mi pošlite novú verziu. Nezabudnite pridať dátum.<br/><b>Peter:</b> Dobre. Počkajte chvíľu, prosím. Hneď to urobím.<br/><br/><b>Перевод:</b> Руководительница: Пожалуйста, откройте файл и проверьте данные. Петер: Исправить и адреса? Руководительница: Да, исправьте их, затем пришлите мне новую версию. Не забудьте добавить дату. Петер: Хорошо. Подождите минуту, пожалуйста. Сейчас сделаю.", BLUE),
    callout("Граница следующей темы", "Вопрос <i>Môžete mi ukázať pas?</i> дан как готовая мягкая альтернатива. Формы с <i>by som</i> и система условной вежливости разбираются в следующем модуле.", CREAM),
    PageBreak(),
]

# 6. Exercises
story += [
    P("5 - Ошибки и практика", "h1"),
    callout("Частые ошибки", "1) строить императив от инфинитива: *písať -> písa; 2) путать адресата ty и vy; 3) забывать -me/-te; 4) отделять ne: *ne hovorte; 5) всегда выбирать один вид; 6) обращаться к незнакомому человеку резкой формой ty без prosím.", CREAM),
    P("<b>1. Определите адресата.</b><br/>a) Otvor okno. b) Otvorme okno. c) Otvorte okno. d) Poďme spolu. e) Prečítajte si návod.", "task"),
    P("<b>2. Образуйте формы ty / my / vy.</b><br/>a) čakať b) písať c) robiť d) zapnúť e) zostať f) prísť.", "task"),
    P("<b>3. Выберите вид.</b><br/>a) ___ adresu. (písať / napísať) b) ___ pomaly. (písať / napísať) c) ___ celý text. (čítať / prečítať) d) ___ tu päť minút. (čakať / počkať) e) ___ mi večer. (volať / zavolať)", "task"),
    P("<b>4. Сделайте запрет.</b><br/>a) Hovorte nahlas. b) Otvárajte tieto dvere. c) Zabudnite si lístok. d) Choď tam sám. e) Ponáhľajte sa.", "task"),
    P("<b>5. Смягчите просьбу и переведите.</b><br/>a) Повторите это. b) Подождите минуту. c) Скажите мне адрес. d) Садитесь. e) Покажите мне паспорт.", "task"),
    P("<b>6. Практическая инструкция.</b> Напишите 6-8 шагов: как пользоваться аппаратом, приготовить простое блюдо или выполнить офисную задачу. Используйте формы <i>vy</i>, один запрет, <i>prosím</i> и минимум два вида.", "task"),
    PageBreak(),
]

# 7. Answers
story += [
    P("6. Ответы и итог", "h1"),
    P("<b>1.</b> a) ty; b) my, совместное действие; c) vy / вежливое Вы; d) my; e) vy / вежливое Вы.", "answer"),
    P("<b>2.</b> a) čakaj / čakajme / čakajte; b) píš / píšme / píšte; c) rob / robme / robte; d) zapni / zapnime / zapnite; e) zostaň / zostaňme / zostaňte; f) príď / príďme / príďte.", "answer"),
    P("<b>3.</b> a) <b>Napíš</b> adresu. b) <b>Píš</b> pomaly. c) <b>Prečítaj</b> celý text. d) <b>Čakaj</b> tu päť minút. e) <b>Zavolaj</b> mi večer.", "answer"),
    P("<b>4.</b> a) <b>Nehovorte</b> nahlas. b) <b>Neotvárajte</b> tieto dvere. c) <b>Nezabudnite</b> si lístok. d) <b>Nechoď</b> tam sám. e) <b>Neponáhľajte sa.</b>", "answer"),
    P("<b>5.</b> Возможные ответы: a) Zopakujte to, prosím. b) Počkajte chvíľu, prosím. c) Povedzte mi, prosím, adresu. d) Nech sa páči, sadnite si. e) Môžete mi ukázať pas?", "answer"),
    P("Образец к заданию 6", "h2"),
    callout("Kopírovanie dokumentu", "Najprv zapnite kopírku. Položte dokument na sklo a zatvorte kryt. Potom vyberte počet kópií. Skontrolujte nastavenie papiera a stlačte zelené tlačidlo. Počkajte, kým sa kopírovanie skončí. Neotvárajte kryt počas kopírovania. Nakoniec si vezmite dokument aj kópie. Ak potrebujete pomoc, zavolajte ma, prosím.<br/><br/>Сначала включите копир. Положите документ на стекло и закройте крышку. Затем выберите число копий. Проверьте настройку бумаги и нажмите зелёную кнопку. Подождите до окончания копирования. Не открывайте крышку во время работы. В конце заберите документ и копии. Если нужна помощь, позовите меня, пожалуйста.", BLUE),
    P("Четыре опоры", "h2"),
    grid([
        ["1", "Ty: základ; my: +me; vy / Вы: +te. Частотные формы учатся готовой тройкой."],
        ["2", "Неправильные: buď, daj, jedz, vedz, vezmi, povedz, príď, choď/poď."],
        ["3", "Вид различает результат и процесс; ne- присоединяется к глаголу слитно."],
        ["4", "Вежливость создают vy, prosím, prepáčte, nech sa páči и вопрос с môžete."],
    ], [14, 155], header=False),
    callout("Проверка освоения", "Я могу:  □ выбрать форму ty/my/vy;  □ употребить неправильный императив;  □ построить запрет;  □ дать ясную и вежливую инструкцию.", GREEN),
]

OUT.parent.mkdir(parents=True, exist_ok=True)
doc.build(story, onFirstPage=first_page, onLaterPages=later_page)
print(OUT)
