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
OUT = ROOT / "output" / "pdf" / "A2" / "Module_04" / "Slovak_A2_Tema_4_5_Analiticheskoe_budushchee_nesovershennyh_glagolov.pdf"
TITLE = "Slovak A2 - Тема 4.5 - Аналитическое будущее несовершенных глаголов"

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
    canvas.drawCentredString(105 * mm, 57 * mm, "BUDEM + ИНФИНИТИВ = БУДУ ЗАНИМАТЬСЯ")
    canvas.setFont("SK", 9)
    canvas.drawCentredString(105 * mm, 47 * mm, "budem + infinitív = budúci priebeh alebo opakovanie")
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
    canvas.drawString(20 * mm, 285 * mm, "SLOVOKROK  |  A2  |  ТЕМА 4.5  |  АНАЛИТИЧЕСКОЕ БУДУЩЕЕ")
    canvas.setFillColor(MUTED)
    canvas.setFont("SK", 7.5)
    canvas.drawCentredString(105 * mm, 10 * mm, f"стр. {doc.page} / 7")
    canvas.restoreState()


doc = SimpleDocTemplate(
    str(OUT), pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm,
    topMargin=26 * mm, bottomMargin=17 * mm, title=TITLE,
    author="SlovoKrok", subject="Slovak A2 self-study module 4.5",
)
story = []

# 1. Cover
story += [
    Spacer(1, 23 * mm), P("SLOVOKROK • СЛОВАЦКИЙ A2", "cover_kicker"),
    P("ТЕМА 4.5", "cover_kicker"),
    P("Аналитическое будущее<br/>несовершенных глаголов", "cover_title"),
    P("Opisné futúrum nedokonavých slovies", "cover_sub"), Spacer(1, 14 * mm),
    Table(
        [[P("После модуля вы сможете", "box_b")],
         [P("• строить формы <i>budem + infinitív</i> для всех лиц;<br/>• говорить, чем будете заниматься и что будет происходить;<br/>• образовывать отрицание и вопросы;<br/>• ставить <i>sa/si</i> в естественное место и описывать длительность или повтор.", "box")]],
        colWidths=[145 * mm],
        style=TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#FFF7FB")),
            ("LEFTPADDING", (0, 0), (-1, -1), 10), ("RIGHTPADDING", (0, 0), (-1, -1), 10),
            ("TOPPADDING", (0, 0), (-1, -1), 7), ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ]),
    ), PageBreak(),
]

# 2. Formation
story += [
    P("1. Формула: budem + infinitív", "h1"),
    P("Будущее несовершенного глагола состоит из личной формы <b>budem</b> и неизменяемого инфинитива. Лицо выражает только вспомогательный глагол."),
    grid([
        ["Лицо", "Форма", "Пример"],
        ["ja", "budem + robiť", "Budem pracovať doma.<br/>Я буду работать дома."],
        ["ty", "budeš + robiť", "Budeš čítať tú knihu.<br/>Ты будешь читать эту книгу."],
        ["on / ona / ono", "bude + robiť", "Večer bude variť.<br/>Вечером он / она будет готовить."],
        ["my", "budeme + robiť", "Budeme čakať pred školou.<br/>Мы будем ждать перед школой."],
        ["vy", "budete + robiť", "Budete bývať v centre.<br/>Вы будете жить в центре."],
        ["oni / ony", "budú + robiť", "Budú telefonovať klientom.<br/>Они будут звонить клиентам."],
    ], [38, 50, 81]),
    callout("Что выражает эта форма", "Она называет будущий процесс, состояние, длительное или повторяющееся занятие: <i>Zajtra budem písať správu.</i> - Завтра я буду писать отчёт. Завершённый результат не заявлен.", GREEN),
    callout("Две важные границы", "У глагола <b>byť</b> будущее уже выражено формами <i>budem, budeš...</i>: не *budem byť. У глагола <b>ísť</b> используется <i>pôjdem</i>, а не *budem ísť. Глаголы движения подробно разбираются в теме 4.7.", CREAM),
    P("Не меняйте инфинитив", "h2"),
    P("<b>Budeme študovať.</b> - Мы будем учиться. Не *budeme študujeme и не *budeme študovali.", "ex"),
    PageBreak(),
]

# 3. Negation and questions
story += [
    P("2. Отрицание и вопрос", "h1"),
    P("В отрицании <b>ne-</b> присоединяется к форме <i>budem</i>. Инфинитив остаётся без изменения. В вопросе особой вопросительной формы нет: помогает интонация или вопросительное слово."),
    grid([
        ["Модель", "Пример", "Перевод"],
        ["nebudem + infinitív", "Zajtra nebudem pracovať.", "Завтра я не буду работать."],
        ["nebudeš + infinitív", "Nebudeš dlho čakať.", "Ты не будешь долго ждать."],
        ["áno / nie вопрос", "Budeš večer variť?", "Ты будешь готовить вечером?"],
        ["вопросительное слово", "Čo budete zajtra robiť?", "Что вы будете делать завтра?"],
        ["вопрос о времени", "Kedy budú cestovať?", "Когда они будут путешествовать?"],
    ], [41, 67, 61]),
    P("Нейтральный порядок слов", "h2"),
    P("<b>Zajtra budem pracovať doma.</b> - Завтра я буду работать дома.", "ex"),
    P("<b>Budem pracovať doma celý deň.</b> - Я буду работать дома весь день.", "ex"),
    P("<b>Kde budeš bývať?</b> - Где ты будешь жить?", "ex"),
    P("<b>Prečo nebudete cestovať?</b> - Почему вы не будете путешествовать?", "ex"),
    callout("Не разрывайте форму случайно", "Обычное место инфинитива - после формы <i>budem</i>, но обстоятельство может стоять перед всей конструкцией: <i>V lete budeme často cestovať.</i> Главное: личную форму и инфинитив легко узнать как одну грамматическую конструкцию.", BLUE),
    callout("Проверка", "Найдите две части: <b>Kedy</b> <i>budeš</i> <b>zajtra</b> <i>pracovať</i>? Лицо находится в <i>budeš</i>, значение действия - в <i>pracovať</i>.", PALE),
    PageBreak(),
]

# 4. Clitics and scope
story += [
    P("3. sa/si и порядок слов", "h1"),
    P("Краткие формы <b>sa/si</b> стремятся к ранней позиции. Если предложение начинается с <i>budem</i>, они стоят сразу после него. Если впереди есть отдельный ударный элемент, <i>sa/si</i> обычно следует за ним."),
    grid([
        ["Начало предложения", "Естественная модель", "Перевод"],
        ["budem...", "Budem sa učiť po slovensky.", "Я буду учить словацкий."],
        ["nebudem...", "Nebudem sa ponáhľať.", "Я не буду торопиться."],
        ["время + sa", "Zajtra sa budem učiť doma.", "Завтра я буду заниматься дома."],
        ["время + si", "Večer si budem čítať.", "Вечером я буду читать для удовольствия."],
        ["вопрос", "Budeš sa cez víkend učiť?", "Ты будешь заниматься на выходных?"],
    ], [43, 69, 57]),
    callout("Типичная ошибка", "Не ставьте *<i>Zajtra budem sa učiť</i>. После начального <i>zajtra</i> естественно: <b>Zajtra sa budem učiť.</b> Если первой стоит личная форма, говорим: <b>Budem sa učiť.</b>", CREAM),
    P("Длительность и повторяемость", "h2"),
    grid([
        ["Смысл", "Маркер", "Пример"],
        ["длительный процесс", "dve hodiny, celý deň", "Dve hodiny budem písať správu.<br/>Я буду писать отчёт два часа."],
        ["границы процесса", "od... do...", "Budeme pracovať od deviatej do piatej.<br/>Мы будем работать с девяти до пяти."],
        ["повтор", "každý týždeň, často", "Každý utorok budeme trénovať.<br/>Каждый вторник мы будем тренироваться."],
    ], [41, 48, 80]),
    callout("Граница с темой 4.6", "<i>Budem písať</i> называет будущее занятие. <i>Napíšem</i> называет будущий завершённый результат. Здесь тренируем только аналитическую форму несовершенных глаголов; совершенное будущее будет в следующем модуле.", BLUE),
    PageBreak(),
]

# 5. Connected use
story += [
    P("4. План и прогноз", "h1"),
    P("Аналитическое будущее удобно для расписания процессов, повторяющихся планов и явлений, которые будут продолжаться."),
    callout(
        "Môj budúci týždeň",
        "Budúci týždeň budem pracovať z domu. Každé ráno budem začínať o ôsmej. Dopoludnia budem odpovedať na e-maily a telefonovať klientom. Po obede budem pripravovať prezentáciu. V utorok a vo štvrtok budeme mať online poradu. Večer sa budem učiť po slovensky. Ak bude pekne, budem chodiť na prechádzku.<br/><br/><b>Перевод:</b> На следующей неделе я буду работать из дома. Каждое утро буду начинать в восемь. До обеда буду отвечать на письма и звонить клиентам. После обеда буду готовить презентацию. Во вторник и четверг у нас будут онлайн-совещания. Вечером я буду заниматься словацким. Если будет хорошая погода, буду ходить гулять.",
        BLUE,
    ),
    P("Мини-диалог", "h2"),
    callout("Cez víkend", "<b>Anna:</b> Čo budeš robiť cez víkend?<br/><b>Peter:</b> V sobotu budem upratovať byt a večer budem oddychovať.<br/><b>Anna:</b> Budeš sa aj učiť?<br/><b>Peter:</b> Áno. V nedeľu sa budem učiť po slovensky.<br/><b>Anna:</b> Ako dlho sa budeš učiť?<br/><b>Peter:</b> Asi dve hodiny. Potom budem variť večeru.<br/><br/><b>Перевод:</b> Анна: Что ты будешь делать на выходных? Петер: В субботу буду убирать квартиру, а вечером отдыхать. Анна: Ты будешь ещё и заниматься? Петер: Да. В воскресенье буду заниматься словацким. Анна: Как долго? Петер: Около двух часов. Потом буду готовить ужин.", PALE),
    P("Погода и необходимость", "h2"),
    P("<b>Zajtra bude pršať.</b> - Завтра будет идти дождь.", "ex"),
    P("<b>Budeme musieť čakať.</b> - Нам придётся ждать.", "ex"),
    P("<b>Budem môcť prísť neskôr.</b> - Я смогу прийти позже.", "ex"),
    callout("Один план - несколько процессов", "Повторяйте <i>budem</i>, когда это делает структуру яснее: <i>Budem pracovať a budem študovať.</i> В коротком однородном ряду вспомогательный глагол можно не дублировать: <i>Budem čítať a počúvať hudbu.</i>", GREEN),
    PageBreak(),
]

# 6. Exercises
story += [
    P("5. Ошибки и практика", "h1"),
    callout("Частые ошибки", "1) ставить личную форму вместо инфинитива: *budem pracujem; 2) образовывать отрицание у инфинитива: *budem nepracovať; 3) говорить *budem byť или *budem ísť; 4) ставить sa после всей конструкции; 5) использовать аналитическую форму, когда нужен явный завершённый результат.", CREAM),
    P("<b>1. Выберите правильную форму.</b><br/>a) Zajtra <i>(budem pracovať / budem pracujem)</i> doma.<br/>b) Večer <i>(bude čítať / bude číta)</i> knihu.<br/>c) V lete <i>(budeme cestovať / cestujeme budeme)</i> často.<br/>d) Oni <i>(budú bývať / budú bývajú)</i> v centre.", "task"),
    P("<b>2. Поставьте budem в нужное лицо.</b><br/>a) Ja ___ študovať. b) Ty ___ čakať. c) Eva ___ variť. d) My ___ pracovať. e) Vy ___ cestovať. f) Deti ___ spať.", "task"),
    P("<b>3. Сделайте отрицание и вопрос.</b><br/>Образец: Budem telefonovať. -> Nebudem telefonovať. / Budeš telefonovať?<br/>a) Budeme bývať v Bratislave. b) Bude čakať pred domom. c) Budú pracovať cez víkend.", "task"),
    P("<b>4. Исправьте порядок слов.</b><br/>a) Zajtra budem sa učiť doma. b) Večer budem si čítať. c) Budeš zajtra učiť sa? d) Nebudem ponáhľať sa.", "task"),
    P("<b>5. Переведите.</b><br/>a) Завтра я буду работать весь день.<br/>b) Что вы будете делать вечером?<br/>c) Мы не будем долго ждать.<br/>d) Каждую среду они будут тренироваться.<br/>e) В воскресенье я буду заниматься словацким два часа.", "task"),
    P("<b>6. План.</b> Напишите 6-8 предложений о следующей неделе: работа или учёба, один повторяющийся план, одно отрицание, один вопрос и одна фраза с <i>sa/si</i>.", "task"),
    PageBreak(),
]

# 7. Answers
story += [
    P("6. Ответы и итог", "h1"),
    P("<b>1.</b> a) <b>budem pracovať</b>; b) <b>bude čítať</b>; c) <b>budeme cestovať</b>; d) <b>budú bývať</b>.", "answer"),
    P("<b>2.</b> a) <b>budem</b>; b) <b>budeš</b>; c) <b>bude</b>; d) <b>budeme</b>; e) <b>budete</b>; f) <b>budú</b>.", "answer"),
    P("<b>3.</b> Возможные ответы: a) Nebudeme bývať v Bratislave. / Budete bývať v Bratislave? b) Nebude čakať pred domom. / Bude čakať pred domom? c) Nebudú pracovať cez víkend. / Budú pracovať cez víkend?", "answer"),
    P("<b>4.</b> a) Zajtra <b>sa budem učiť</b> doma. b) Večer <b>si budem čítať</b>. c) <b>Budeš sa zajtra učiť?</b> d) <b>Nebudem sa ponáhľať.</b>", "answer"),
    P("<b>5.</b> a) Zajtra budem pracovať celý deň. b) Čo budete robiť večer? c) Nebudeme dlho čakať. d) Každú stredu budú trénovať. e) V nedeľu sa budem dve hodiny učiť po slovensky.", "answer"),
    P("Образец к заданию 6", "h2"),
    callout("Budúci týždeň", "Budúci týždeň budem pracovať z domu. Každé ráno budem začínať o ôsmej. V pondelok nebudem cestovať do kancelárie. Večer sa budem učiť po slovensky. V stredu budem dve hodiny pripravovať prezentáciu. Cez víkend budem oddychovať a čítať. A čo budeš robiť ty?<br/><br/>На следующей неделе я буду работать из дома. Каждое утро буду начинать в восемь. В понедельник не поеду в офис. Вечером буду заниматься словацким. В среду два часа буду готовить презентацию. На выходных буду отдыхать и читать. А что будешь делать ты?", BLUE),
    P("Четыре опоры", "h2"),
    grid([
        ["1", "Несовершенное будущее: личная форма budem + неизменяемый инфинитив."],
        ["2", "Отрицание: nebudem + infinitív; вопрос строится интонацией или вопросительным словом."],
        ["3", "Sa/si стоит рано: Budem sa učiť. Zajtra sa budem učiť."],
        ["4", "Форма выражает будущий процесс, длительность или повтор, а не обещанный результат."],
    ], [14, 155], header=False),
    callout("Проверка освоения", "Я могу:  □ проспрягать <i>budem</i>;  □ построить отрицание и вопрос;  □ правильно поставить <i>sa/si</i>;  □ описать будущую неделю как последовательность процессов и повторов.", GREEN),
]

OUT.parent.mkdir(parents=True, exist_ok=True)
doc.build(story, onFirstPage=first_page, onLaterPages=later_page)
print(OUT)
