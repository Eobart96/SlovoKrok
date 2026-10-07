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
OUT = ROOT / "output" / "pdf" / "A2" / "Module_04" / "Slovak_A2_Tema_4_8_Vozvratnye_glagoly_sa_i_si.pdf"
TITLE = "Slovak A2 - Тема 4.8 - Возвратные глаголы sa и si"

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
    canvas.drawCentredString(105 * mm, 57 * mm, "UMÝVAM SA - UMÝVAM SI RUKY")
    canvas.setFont("SK", 9)
    canvas.drawCentredString(105 * mm, 47 * mm, "funkcia, význam a prirodzený slovosled")
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
    canvas.drawString(20 * mm, 285 * mm, "SLOVOKROK  |  A2  |  ТЕМА 4.8  |  ВОЗВРАТНЫЕ ГЛАГОЛЫ SA И SI")
    canvas.setFillColor(MUTED)
    canvas.setFont("SK", 7.5)
    canvas.drawCentredString(105 * mm, 10 * mm, f"стр. {doc.page} / 7")
    canvas.restoreState()


doc = SimpleDocTemplate(
    str(OUT), pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm,
    topMargin=26 * mm, bottomMargin=17 * mm, title=TITLE,
    author="SlovoKrok", subject="Slovak A2 self-study module 4.8",
)
story = []

# 1. Cover
story += [
    Spacer(1, 23 * mm), P("SLOVOKROK • СЛОВАЦКИЙ A2", "cover_kicker"),
    P("ТЕМА 4.8", "cover_kicker"),
    P("Возвратные глаголы<br/>sa и si", "cover_title"),
    P("Zvratnosť, vzájomnosť a zmena významu", "cover_sub"), Spacer(1, 14 * mm),
    Table(
        [[P("После модуля вы сможете", "box_b")],
         [P("• узнавать <i>sa/si</i> как обязательную часть словарного глагола;<br/>• различать действие на себя и на часть своего тела;<br/>• выражать взаимность между людьми;<br/>• понимать пары, где <i>sa/si</i> меняет значение глагола.", "box")]],
        colWidths=[145 * mm],
        style=TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#FFF7FB")),
            ("LEFTPADDING", (0, 0), (-1, -1), 10), ("RIGHTPADDING", (0, 0), (-1, -1), 10),
            ("TOPPADDING", (0, 0), (-1, -1), 7), ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ]),
    ), PageBreak(),
]

# 2. Four functions
story += [
    P("1. Одна форма - четыре функции", "h1"),
    callout("Рабочая стратегия", "Не переводите <i>sa/si</i> одним русским «-ся». Сначала определите функцию всей конструкции, а словарные глаголы запоминайте вместе с частицей."),
    grid([
        ["Функция", "Как узнать", "Пример"],
        ["обязательная часть", "без частицы такого значения нет", "<b>Páči sa mi film.</b><br/>Мне нравится фильм."],
        ["действие на себя", "действующий и объект совпадают", "<b>Ráno sa umývam.</b><br/>Утром я умываюсь."],
        ["взаимность", "несколько участников действуют друг на друга", "<b>Často si píšeme.</b><br/>Мы часто переписываемся."],
        ["изменение значения", "без частицы смысл или управление иные", "<b>Vrátim knihu. Vrátim sa domov.</b><br/>Верну книгу. Вернусь домой."],
    ], [39, 57, 73]),
    P("Sa и si как короткие формы", "h2"),
    grid([
        ["Форма", "Полезная учебная подсказка", "Пример"],
        ["<b>sa</b>", "часто соответствует Acc.: кого? что? - себя", "Umývam <b>sa</b>. - Я умываюсь."],
        ["<b>si</b>", "часто соответствует Dat.: кому? - себе", "Umývam <b>si</b> ruky. - Я мою себе руки."],
    ], [24, 72, 73]),
    callout("Это подсказка, а не универсальный перевод", "В <i>páčiť sa, ozvať sa, báť sa, myslieť si</i> короткая форма входит в словарную конструкцию. Нельзя каждый раз заменять её русским «себя / себе».", CREAM),
    P("Позиция в нейтральной фразе", "h2"),
    P("Короткие <i>sa/si</i> безударны и обычно стоят после первого ударного компонента: <b>Ráno sa umývam. Zajtra si dám čaj. Kedy sa vrátiš?</b> Не начинайте ими нейтральную фразу и не оставляйте автоматически в самом конце."),
    PageBreak(),
]

# 3. Obligatory verbs
story += [
    P("2. Обязательная частица: учим целиком", "h1"),
    P("Если частица является частью словарного глагола, она сохраняется во всех лицах и временах: <i>páčiť sa, ozvať sa, báť sa, tešiť sa</i>. Меняется личная форма глагола, но не <i>sa</i>."),
    P("Páčiť sa: нравится кому?", "h2"),
    grid([
        ["Что нравится", "Кому", "Пример"],
        ["один предмет", "mi / ti / mu / jej / nám / vám / im", "<b>Páči sa mi tento byt.</b><br/>Мне нравится эта квартира."],
        ["несколько предметов", "та же форма Dat.", "<b>Páčia sa nám tie fotografie.</b><br/>Нам нравятся те фотографии."],
        ["вопрос", "komu?", "<b>Páči sa ti Bratislava?</b><br/>Тебе нравится Братислава?"],
        ["отрицание", "nepáči sa", "<b>Ten návrh sa jej nepáči.</b><br/>Ей не нравится это предложение."],
    ], [42, 48, 79]),
    callout("Согласование", "Подлежащее - то, что нравится. Поэтому <i>film sa páči</i>, но <i>filmy sa páčia</i>. Человек выражается дательным: <i>mi, ti, mu, jej, nám, vám, im</i>.", BLUE),
    P("Ozvať sa: дать о себе знать", "h2"),
    P("<b>Ozvem sa ti zajtra.</b> - Я свяжусь с тобой завтра."),
    P("<b>Prečo si sa neozval?</b> - Почему ты не дал о себе знать?"),
    P("<b>Keď prídeš domov, ozvi sa.</b> - Когда придёшь домой, дай знать."),
    P("Ещё готовые словарные единицы", "h2"),
    grid([
        ["Глагол", "Пример", "Перевод"],
        ["báť sa", "Bojím sa skúšky.", "Я боюсь экзамена."],
        ["tešiť sa na", "Tešíme sa na víkend.", "Мы с нетерпением ждём выходных."],
        ["sťažovať sa na", "Sťažuje sa na hluk.", "Он жалуется на шум."],
    ], [38, 65, 66]),
    PageBreak(),
]

# 4. Reflexive and meaning change
story += [
    P("3. Себя, себе и новое значение", "h1"),
    P("Umývať sa или umývať si?", "h2"),
    grid([
        ["Конструкция", "Что означает", "Пример"],
        ["umývať <b>sa</b>", "ухаживать за собой / мыться в целом", "Dieťa sa už umýva samo.<br/>Ребёнок уже моется сам."],
        ["umývať <b>si</b> + часть тела", "мыть себе что-то", "Pred jedlom si umývam ruky.<br/>Перед едой я мою руки."],
        ["česať <b>sa</b>", "причёсываться", "Ráno sa rýchlo češem.<br/>Утром я быстро причёсываюсь."],
        ["čistiť <b>si</b> + предмет", "чистить себе что-то", "Večer si čistím zuby.<br/>Вечером я чищу зубы."],
    ], [47, 56, 66]),
    callout("Часть тела без svoj", "В обычной фразе принадлежность уже показывает <i>si</i>: <i>Umývam si ruky.</i> Русское «свои руки» не требует *svoje ruky, если нет особого противопоставления.", CREAM),
    P("Частица меняет участника или значение", "h2"),
    grid([
        ["Без sa/si", "С sa/si"],
        ["<b>Vrátim knihu.</b><br/>Я верну книгу.", "<b>Vrátim sa domov.</b><br/>Я вернусь домой."],
        ["<b>Dám ti kľúč.</b><br/>Я дам тебе ключ.", "<b>Dám si kávu.</b><br/>Я возьму / закажу себе кофе."],
        ["<b>Učím deti slovenčinu.</b><br/>Я учу детей словацкому.", "<b>Učím sa po slovensky.</b><br/>Я учу словацкий."],
        ["<b>Myslím na prácu.</b><br/>Я думаю о работе.", "<b>Myslím si, že má pravdu.</b><br/>Я считаю, что он прав."],
        ["<b>Rozprávam príbeh.</b><br/>Я рассказываю историю.", "<b>Rozprávam sa s kolegom.</b><br/>Я разговариваю с коллегой."],
    ], [84.5, 84.5]),
    callout("Лексическая дисциплина", "Не выводите новое значение механически. Записывайте в словарь целую модель: <i>vrátiť niečo</i>, <i>vrátiť sa niekam</i>, <i>dať niekomu niečo</i>, <i>dať si niečo</i>, <i>rozprávať sa s niekým o niečom</i>.", BLUE),
    PageBreak(),
]

# 5. Reciprocity, word order and dialogue
story += [
    P("4. Взаимность и естественная фраза", "h1"),
    P("При взаимности участники действуют друг на друга. По-русски перевод часто не содержит «себя / себе», поэтому значение узнаётся по контексту."),
    grid([
        ["Модель", "Пример", "Перевод"],
        ["rozprávať sa", "Večer sa rozprávame o práci.", "Вечером мы разговариваем о работе."],
        ["písať si", "S Martinom si často píšeme.", "Мы с Мартином часто переписываемся."],
        ["pomáhať si", "Susedia si navzájom pomáhajú.", "Соседи помогают друг другу."],
        ["stretnúť sa", "Stretneme sa pred kinom.", "Мы встретимся перед кинотеатром."],
        ["objímať sa", "Priatelia sa objali.", "Друзья обнялись."],
    ], [42, 67, 60]),
    callout("Как сделать взаимность явной", "Добавьте <i>navzájom</i> - «друг другу»: <i>Pomáhajú si navzájom.</i> С одним участником укажите партнёра: <i>Rozprávam sa s Evou.</i>", BLUE),
    P("Порядок коротких форм", "h2"),
    grid([
        ["Начало", "Естественная фраза"],
        ["время", "<b>Ráno sa vrátim.</b> - Утром я вернусь."],
        ["вопросительное слово", "<b>Kedy sa ozveš?</b> - Когда ты дашь знать?"],
        ["союз", "<b>Keď sa vrátim, zavolám ti.</b> - Когда вернусь, позвоню тебе."],
        ["подлежащее", "<b>Peter si dá polievku.</b> - Петер возьмёт суп."],
        ["отрицание", "<b>Ten film sa mi nepáči.</b> - Мне не нравится этот фильм."],
    ], [52, 117]),
    P("Мини-диалог", "h2"),
    callout("Po práci", "<b>Eva:</b> Ozveš sa mi po práci?<br/><b>Martin:</b> Áno. Keď sa vrátim domov, zavolám ti.<br/><b>Eva:</b> Dobre. Stretneme sa potom v centre?<br/><b>Martin:</b> Môžeme. Dám si kávu a porozprávame sa o výlete.<br/><b>Eva:</b> Výborne, ten nápad sa mi páči.<br/><br/><b>Перевод:</b> Ева: Дашь мне знать после работы? Мартин: Да. Когда вернусь домой, позвоню тебе. Ева: Хорошо. Потом встретимся в центре? Мартин: Можно. Я возьму кофе, и поговорим о поездке. Ева: Отлично, мне нравится эта идея.", PALE),
    callout("Граница следующей темы", "Форму <i>ozvi sa</i> здесь можно запомнить как готовую реплику. Полная система приказов, запретов и вежливых инструкций разбирается отдельно в следующем модуле.", CREAM),
    PageBreak(),
]

# 6. Exercises
story += [
    P("5. Ошибки и практика", "h1"),
    callout("Частые ошибки", "1) терять обязательное <i>sa</i>: *páči mi; 2) ставить <i>sa/si</i> в конец; 3) говорить *umývam sa ruky вместо <i>umývam si ruky</i>; 4) путать <i>vrátiť</i> и <i>vrátiť sa</i>; 5) согласовывать <i>páčiť sa</i> с человеком; 6) переводить каждое <i>si</i> словом «себе».", CREAM),
    P("<b>1. Определите функцию sa/si.</b><br/>a) Páči sa mi hudba. b) Ráno sa umývam. c) Často si píšeme. d) Vrátim sa večer. e) Dám si čaj.", "task"),
    P("<b>2. Вставьте sa или si.</b><br/>a) Eva ___ umýva ruky. b) Deti ___ umývajú. c) Zajtra ___ ozvem. d) S kolegom ___ rozprávame. e) Peter ___ dá polievku. f) Kedy ___ vrátiš?", "task"),
    P("<b>3. Выберите форму.</b><br/>a) Páči / Páčia sa mi tento obraz. b) Páči / Páčia sa nám tie knihy. c) Ráno umývam sa / sa umývam. d) Zajtra dám si / si dám kávu. e) Večer si čistím / sa čistím zuby.", "task"),
    P("<b>4. Исправьте ошибки.</b><br/>a) Tento film páči sa mi. b) Umývam sa ruky. c) Zajtra vrátim domov. d) Eva dá kávu si. e) Rozprávame o tom sa. f) Páči sa mi tie fotografie.", "task"),
    P("<b>5. Переведите.</b><br/>a) Мне нравится эта квартира. b) Завтра я дам тебе знать. c) Я верну книгу и вернусь домой. d) Мы разговариваем друг с другом. e) Перед едой дети моют руки. f) Я думаю, что это хорошая идея.", "task"),
    P("<b>6. Диалог после работы.</b> Напишите 6-8 реплик. Используйте <i>ozvať sa, vrátiť sa, stretnúť sa, dať si</i> и одну конструкцию с <i>páčiť sa</i>.", "task"),
    PageBreak(),
]

# 7. Answers
story += [
    P("6. Ответы и итог", "h1"),
    P("<b>1.</b> a) обязательная часть; b) действие на себя; c) взаимность; d) изменение участника / значения; e) значение «взять или заказать себе».", "answer"),
    P("<b>2.</b> a) <b>si</b>; b) <b>sa</b>; c) <b>sa</b>; d) <b>sa</b>; e) <b>si</b>; f) <b>sa</b>.", "answer"),
    P("<b>3.</b> a) <b>Páči sa mi tento obraz.</b> b) <b>Páčia sa nám tie knihy.</b> c) <b>Ráno sa umývam.</b> d) <b>Zajtra si dám kávu.</b> e) <b>Večer si čistím zuby.</b>", "answer"),
    P("<b>4.</b> a) <b>Tento film sa mi páči.</b> b) <b>Umývam si ruky.</b> c) <b>Zajtra sa vrátim domov.</b> d) <b>Eva si dá kávu.</b> e) <b>Rozprávame sa o tom.</b> f) <b>Páčia sa mi tie fotografie.</b>", "answer"),
    P("<b>5.</b> a) Páči sa mi tento byt. b) Zajtra sa ti ozvem. c) Vrátim knihu a vrátim sa domov. d) Rozprávame sa spolu / navzájom. e) Pred jedlom si deti umývajú ruky. f) Myslím si, že je to dobrý nápad.", "answer"),
    P("Образец к заданию 6", "h2"),
    callout("Stretnutie", "<b>Eva:</b> Ozveš sa mi po práci?<br/><b>Peter:</b> Áno, ozvem sa ti o piatej.<br/><b>Eva:</b> Kedy sa vrátiš do centra?<br/><b>Peter:</b> Vrátim sa asi o šiestej. Stretneme sa pri stanici?<br/><b>Eva:</b> Dobre. Dáme si kávu a porozprávame sa.<br/><b>Peter:</b> Výborne, ten plán sa mi páči.<br/><br/>Ева: Дашь мне знать после работы? Петер: Да, в пять. Ева: Когда вернёшься в центр? Петер: Примерно в шесть. Встретимся у вокзала? Ева: Хорошо. Выпьем кофе и поговорим. Петер: Отлично, мне нравится этот план.", BLUE),
    P("Четыре опоры", "h2"),
    grid([
        ["1", "Словарные глаголы запоминаются целиком: páčiť sa, ozvať sa, báť sa."],
        ["2", "Sa часто указывает на себя целиком; si - на действие для себя или с частью тела."],
        ["3", "При взаимности участники действуют друг на друга: rozprávať sa, písať si."],
        ["4", "Sa/si может менять значение: vrátiť/vrátiť sa, dať/dať si, učiť/učiť sa."],
    ], [14, 155], header=False),
    callout("Проверка освоения", "Я могу:  □ назвать функцию <i>sa/si</i>;  □ выбрать <i>umývať sa/si</i>;  □ выразить взаимность;  □ поставить короткую форму в естественное место.", GREEN),
]

OUT.parent.mkdir(parents=True, exist_ok=True)
doc.build(story, onFirstPage=first_page, onLaterPages=later_page)
print(OUT)
