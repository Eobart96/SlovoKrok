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
OUT = ROOT / "output" / "pdf" / "A2" / "Module_04" / "Slovak_A2_Tema_4_12_Otglagolnye_sushchestvitelnye_i_passivnye_prichastiya.pdf"
TITLE = "Slovak A2 - Тема 4.12 - Отглагольные существительные и пассивные причастия"

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
    "cover_title": ParagraphStyle("cover_title", fontName="SK-Bold", fontSize=20.5, leading=24.5, textColor=WHITE, alignment=TA_CENTER, spaceAfter=11),
    "cover_sub": ParagraphStyle("cover_sub", fontName="SK", fontSize=12.0, leading=16, textColor=WHITE, alignment=TA_CENTER),
    "h1": ParagraphStyle("h1", fontName="SK-Bold", fontSize=20, leading=24, textColor=PLUM, spaceAfter=8),
    "h2": ParagraphStyle("h2", fontName="SK-Bold", fontSize=13.5, leading=17, textColor=PLUM, spaceBefore=6, spaceAfter=5),
    "body": ParagraphStyle("body", fontName="SK", fontSize=9.35, leading=12.8, textColor=INK, spaceAfter=4),
    "small": ParagraphStyle("small", fontName="SK", fontSize=8.15, leading=11.0, textColor=MUTED, spaceAfter=2),
    "box": ParagraphStyle("box", fontName="SK", fontSize=8.9, leading=12.2, textColor=INK),
    "box_b": ParagraphStyle("box_b", fontName="SK-Bold", fontSize=9.25, leading=12.5, textColor=PLUM),
    "task": ParagraphStyle("task", fontName="SK", fontSize=8.25, leading=11.0, textColor=INK, spaceAfter=4),
    "answer": ParagraphStyle("answer", fontName="SK", fontSize=7.75, leading=10.15, textColor=INK, spaceAfter=3),
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
    canvas.setFont("SK-Bold", 10.2)
    canvas.drawCentredString(105 * mm, 57 * mm, "PLÁVANIE - LIEČENIE - ZATVORENÝ - ZLOMENÝ")
    canvas.setFont("SK", 9)
    canvas.drawCentredString(105 * mm, 47 * mm, "dej, proces a výsledný stav")
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
    canvas.drawString(20 * mm, 285 * mm, "SLOVOKROK  |  A2  |  ТЕМА 4.12  |  ПРОЦЕСС И РЕЗУЛЬТАТ")
    canvas.setFillColor(MUTED)
    canvas.setFont("SK", 7.5)
    canvas.drawCentredString(105 * mm, 10 * mm, f"стр. {doc.page} / 7")
    canvas.restoreState()


doc = SimpleDocTemplate(
    str(OUT), pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm,
    topMargin=26 * mm, bottomMargin=17 * mm, title=TITLE,
    author="SlovoKrok", subject="Slovak A2 self-study module 4.12",
)
story = []

# 1. Cover
story += [
    Spacer(1, 19 * mm), P("SLOVOKROK • СЛОВАЦКИЙ A2", "cover_kicker"),
    P("ТЕМА 4.12", "cover_kicker"),
    P("Отглагольные<br/>существительные<br/>и пассивные причастия", "cover_title"),
    P("Názov deja a výsledný stav", "cover_sub"), Spacer(1, 11 * mm),
    Table(
        [[P("После модуля вы сможете", "box_b")],
         [P("• узнавать названия действий на -anie, -enie и -tie;<br/>• понимать частотные формы в объявлениях и инструкциях;<br/>• согласовывать формы zatvorený, zlomený и подобные;<br/>• различать процесс и результативное состояние.", "box")]],
        colWidths=[145 * mm],
        style=TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#FFF7FB")),
            ("LEFTPADDING", (0, 0), (-1, -1), 10), ("RIGHTPADDING", (0, 0), (-1, -1), 10),
            ("TOPPADDING", (0, 0), (-1, -1), 7), ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ]),
    ), PageBreak(),
]

# 2. Verbal nouns
story += [
    P("1. Название действия: čo?", "h1"),
    callout("Главная идея", "Отглагольное существительное называет действие или процесс как предмет разговора: <i>plávať</i> - плавать, <i>plávanie</i> - плавание. Оно отвечает на <i>čo?</i>, имеет средний род и склоняется как существительное."),
    grid([
        ["Глагол", "Название действия", "Перевод"],
        ["čítať", "čítanie", "чтение"],
        ["písať", "písanie", "письмо, написание"],
        ["plávať", "plávanie", "плавание"],
        ["cestovať", "cestovanie", "путешествие как процесс"],
        ["liečiť", "liečenie", "лечение"],
        ["vyšetriť", "vyšetrenie", "обследование"],
        ["otvoriť", "otvorenie", "открытие"],
        ["vyplniť", "vyplnenie", "заполнение"],
    ], [39, 55, 75]),
    callout("Практический ориентир", "Часто видны окончания <b>-anie, -enie, -tie</b>: <i>čakanie, liečenie, umytie</i>. Но основу не всегда можно безопасно угадать. Для A2 запоминайте проверенные пары целиком: <i>vyšetriť - vyšetrenie</i>, <i>otvoriť - otvorenie</i>.", CREAM),
    P("Где это встречается", "h2"),
    grid([
        ["Модель", "Пример и перевод"],
        ["zákaz + родительный", "Zákaz fajčenia. - Курение запрещено."],
        ["na + винительный", "Miesto na parkovanie. - Место для парковки."],
        ["po + местный", "Po vyšetrení počkajte. - После обследования подождите."],
        ["počas + родительный", "Počas liečenia oddychujte. - Во время лечения отдыхайте."],
    ], [55, 114]),
    PageBreak(),
]

# 3. Passive participles
story += [
    P("2. Результат или состояние: aký?", "h1"),
    P("Пассивное причастие показывает, что с предметом что-то сделали или что он находится в результате действия. Оно ведёт себя как прилагательное и согласуется с существительным."),
    grid([
        ["Мужской род", "Женский род", "Средний род / мн. число"],
        ["zatvorený obchod", "zatvorená lekáreň", "zatvorené dvere"],
        ["zlomený prst", "zlomená ruka", "zlomené rebro"],
        ["vyplnený formulár", "podpísaná zmluva", "vyplnené údaje"],
        ["zrušený termín", "rezervovaná izba", "zrušené stretnutia"],
    ], [56, 56, 57]),
    callout("Частые окончания", "Наиболее заметны формы на <b>-aný, -ený, -tý</b>: <i>podpísaný, zatvorený, umytý</i>. Окончание меняется по роду, числу и падежу: <i>s vyplneným formulárom, o zrušenom termíne</i>.", BLUE),
    P("Не угадывайте форму механически", "h2"),
    grid([
        ["Глагол", "Проверенная форма", "Пример"],
        ["zatvoriť", "zatvorený", "Obchod je zatvorený. - Магазин закрыт."],
        ["zlomiť", "zlomený", "Má zlomenú ruku. - У него сломана рука."],
        ["zaplatiť", "zaplatený", "Účet je zaplatený. - Счёт оплачен."],
        ["poškodiť", "poškodený", "Balík je poškodený. - Посылка повреждена."],
        ["umyť", "umytý", "Jablká sú umyté. - Яблоки вымыты."],
    ], [37, 45, 87]),
    callout("Граница темы", "На A2 достаточно узнавать частотные формы и строить простые сочетания. Полную систему пассива и все способы образования здесь не выводим.", CREAM),
    PageBreak(),
]

# 4. Contrast and authentic contexts
story += [
    P("3. Процесс или готовый результат?", "h1"),
    grid([
        ["Процесс / событие", "Результат / признак"],
        ["zatvorenie obchodu - закрытие магазина", "zatvorený obchod - закрытый магазин"],
        ["vyplnenie formulára - заполнение бланка", "vyplnený formulár - заполненный бланк"],
        ["podpísanie zmluvy - подписание договора", "podpísaná zmluva - подписанный договор"],
        ["zrušenie termínu - отмена записи", "zrušený termín - отменённая запись"],
    ], [84.5, 84.5]),
    callout("Быстрая проверка", "Если нужно назвать <b>что происходит</b>, выбирайте существительное: <i>otvorenie, liečenie</i>. Если нужно описать <b>какой предмет или человек</b>, выбирайте согласованную форму: <i>otvorená lekáreň, liečený pacient</i>.", PALE),
    P("Объявления и инструкции", "h2"),
    callout("Na dverách a na recepcii", "<b>Lekáreň je zatvorená z dôvodu inventúry.</b> - Аптека закрыта из-за инвентаризации.<br/><b>Otvorenie je naplánované na pondelok.</b> - Открытие запланировано на понедельник.<br/><b>Vyplnený formulár odovzdajte na recepcii.</b> - Заполненный бланк сдайте на стойке регистрации.<br/><b>Parkovanie je povolené iba pre hostí.</b> - Парковка разрешена только гостям.", BLUE),
    P("В поликлинике", "h2"),
    callout("Pokyny pre pacienta", "<b>Pred vyšetrením nejedzte.</b> - Перед обследованием не ешьте.<br/><b>Po vyšetrení dostanete správu.</b> - После обследования вы получите заключение.<br/><b>Liečenie trvá približne dva týždne.</b> - Лечение длится примерно две недели.<br/><b>Zlomená ruka musí zostať znehybnená.</b> - Сломанная рука должна оставаться неподвижной.", GREEN),
    PageBreak(),
]

# 5. Phrase bank
story += [
    P("4. Частотные модели", "h1"),
    P("Читайте их как готовые блоки. Так легче сразу узнавать смысл в вывеске, письме или инструкции."),
    P("Процессы и события", "h2"),
    grid([
        ["Словацкий", "Русский"],
        ["Čakanie trvá desať minút.", "Ожидание длится десять минут."],
        ["Fajčenie je zakázané.", "Курение запрещено."],
        ["Upratovanie izby je v cene.", "Уборка номера включена в стоимость."],
        ["Objednanie na vyšetrenie je možné telefonicky.", "Записаться на обследование можно по телефону."],
        ["Podpísanie zmluvy je zajtra.", "Подписание договора состоится завтра."],
        ["Po zaplatení dostanete potvrdenie.", "После оплаты вы получите подтверждение."],
    ], [84, 85]),
    P("Результат и состояние", "h2"),
    grid([
        ["Словацкий", "Русский"],
        ["Izba je rezervovaná.", "Номер забронирован."],
        ["Dvere sú zamknuté.", "Дверь заперта."],
        ["Dokument je podpísaný.", "Документ подписан."],
        ["Stretnutie je zrušené.", "Встреча отменена."],
        ["Tovar je vypredaný.", "Товар распродан."],
        ["Pripravené lieky sú na recepcii.", "Подготовленные лекарства находятся на стойке регистрации."],
    ], [84, 85]),
    callout("Русский перевод помогает не всегда", "Слова на -ние часто соответствуют словацким формам на <i>-anie/-enie</i>, но совпадение не гарантирует правильную основу. Проверяйте словарную пару, а не переводите окончание отдельно.", CREAM),
    PageBreak(),
]

# 6. Exercises
story += [
    P("5. Ошибки и практика", "h1"),
    callout("Частые ошибки", "1) путать действие и признак; 2) не согласовывать причастие: *<i>zatvorený lekáreň</i>; 3) строить форму только по инфинитиву; 4) забывать падеж после предлога: *<i>po vyšetrenie</i>; 5) переводить любое русское -ние одинаково.", CREAM),
    P("<b>1. Что это: процесс (P) или результативный признак (R)?</b><br/>a) liečenie b) zatvorená c) vyplnenie d) podpísaný e) plávanie f) zlomené", "task"),
    P("<b>2. Соедините.</b><br/>1) fajčiť 2) vyšetriť 3) zatvoriť 4) umyť 5) podpísať<br/>a) podpísaný b) fajčenie c) umytý d) vyšetrenie e) zatvorený", "task"),
    P("<b>3. Согласуйте форму.</b><br/>a) zatvorený + lekáreň b) zlomený + rebro c) rezervovaný + izba d) vyplnený + údaje e) zrušený + stretnutia", "task"),
    P("<b>4. Выберите процесс или результат.</b><br/>a) ___ formulára trvá päť minút. (vyplnenie / vyplnený)<br/>b) Prineste ___ formulár. (vyplnenie / vyplnený)<br/>c) ___ je v pondelok. (otvorenie / otvorený)<br/>d) Obchod je ___. (zatvorenie / zatvorený)", "task"),
    P("<b>5. Переведите.</b><br/>a) Курение запрещено. b) Аптека закрыта. c) После обследования подождите. d) Договор подписан. e) Лечение длится две недели.", "task"),
    P("<b>6. Практическая задача.</b> Напишите объявление или инструкцию из 5-6 предложений для гостиницы, офиса или поликлиники. Используйте два названия процесса и три согласованные формы результата.", "task"),
    PageBreak(),
]

# 7. Answers
story += [
    P("6. Ответы и итог", "h1"),
    P("<b>1.</b> a) P; b) R; c) P; d) R; e) P; f) R.", "answer"),
    P("<b>2.</b> 1-b: fajčenie; 2-d: vyšetrenie; 3-e: zatvorený; 4-c: umytý; 5-a: podpísaný.", "answer"),
    P("<b>3.</b> a) zatvorená lekáreň; b) zlomené rebro; c) rezervovaná izba; d) vyplnené údaje; e) zrušené stretnutia.", "answer"),
    P("<b>4.</b> a) Vyplnenie formulára trvá päť minút. b) Prineste vyplnený formulár. c) Otvorenie je v pondelok. d) Obchod je zatvorený.", "answer"),
    P("<b>5.</b> a) Fajčenie je zakázané. b) Lekáreň je zatvorená. c) Po vyšetrení počkajte. d) Zmluva je podpísaná. e) Liečenie trvá dva týždne.", "answer"),
    P("Образец к заданию 6", "h2"),
    callout("Oznam v hoteli", "<b>Upratovanie izieb je od 9.00 do 12.00.</b><br/><b>Počas upratovania nechajte kľúč na recepcii.</b><br/><b>Raňajky sú pripravené od 7.00.</b><br/><b>Parkovanie je povolené iba pre ubytovaných hostí.</b><br/><b>Poškodený kľúč odovzdajte recepčnej.</b><br/><b>Hlavný vchod je po 22.00 zamknutý.</b><br/><br/><b>Перевод:</b> Уборка номеров проходит с 9 до 12. Во время уборки оставьте ключ на стойке регистрации. Завтрак готов с 7 часов. Парковка разрешена только проживающим гостям. Повреждённый ключ отдайте администратору. Главный вход после 22 часов заперт.", BLUE),
    P("Четыре опоры", "h2"),
    grid([
        ["1", "Формы на -anie, -enie и -tie называют действие, процесс или событие."],
        ["2", "Причастия на -aný, -ený и -tý описывают результат и согласуются как прилагательные."],
        ["3", "Сравнивайте: vyplnenie formulára - процесс; vyplnený formulár - результат."],
        ["4", "Для активной речи A2 используйте проверенные частотные пары, а не угадывайте основу."],
    ], [14, 155], header=False),
    callout("Проверка освоения", "Я могу:  □ узнать название процесса;  □ понять состояние предмета;  □ согласовать частую форму;  □ прочитать объявление или медицинскую инструкцию.", GREEN),
]

OUT.parent.mkdir(parents=True, exist_ok=True)
doc.build(story, onFirstPage=first_page, onLaterPages=later_page)
print(OUT)
