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
OUTPUT = ROOT / "output" / "pdf" / "A2" / "Module_02" / "Slovak_A2_Tema_2_7_Genitiv_mnozhestvennogo_chisla.pdf"
OUTPUT.parent.mkdir(parents=True, exist_ok=True)

PLUM = colors.HexColor("#7B245F")
PINK = colors.HexColor("#CE3C92")
PALE = colors.HexColor("#F8E7EF")
ROSE = colors.HexColor("#EACDD9")
ALT = colors.HexColor("#FFF8FA")
CREAM = colors.HexColor("#FFF5DA")
GREEN = colors.HexColor("#E8F5EC")
INK = colors.HexColor("#332A31")
MUTED = colors.HexColor("#6C5B66")

pdfmetrics.registerFont(TTFont("Arial", r"C:\Windows\Fonts\arial.ttf"))
pdfmetrics.registerFont(TTFont("Arial-Bold", r"C:\Windows\Fonts\arialbd.ttf"))

styles = getSampleStyleSheet()
BODY = ParagraphStyle("Body", fontName="Arial", fontSize=9.0, leading=12.0, textColor=INK, spaceAfter=4.0 * mm)
SMALL = ParagraphStyle("Small", parent=BODY, fontSize=7.8, leading=9.9, spaceAfter=2.0 * mm)
TINY = ParagraphStyle("Tiny", parent=BODY, fontSize=7.2, leading=9.0, spaceAfter=1.4 * mm)
TITLE = ParagraphStyle("Title", fontName="Arial-Bold", fontSize=23, leading=27, textColor=colors.white, alignment=TA_LEFT, spaceAfter=5 * mm)
SUBTITLE = ParagraphStyle("Subtitle", fontName="Arial", fontSize=12, leading=16, textColor=colors.HexColor("#FFD8EB"), spaceAfter=5 * mm)
H1 = ParagraphStyle("H1", fontName="Arial-Bold", fontSize=16, leading=19, textColor=PLUM, spaceBefore=1 * mm, spaceAfter=4 * mm)
H2 = ParagraphStyle("H2", fontName="Arial-Bold", fontSize=11.2, leading=14, textColor=PINK, spaceBefore=2 * mm, spaceAfter=2.2 * mm)
COVER_KICKER = ParagraphStyle("CoverKicker", fontName="Arial-Bold", fontSize=10, leading=12, textColor=colors.HexColor("#FFD8EB"), spaceAfter=4 * mm)


def p(text, style=BODY):
    return Paragraph(text, style)


def box(text, background=PALE, border=ROSE, style=BODY, padding=7):
    table = Table([[p(text, style)]], colWidths=[170 * mm])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), background), ("BOX", (0, 0), (-1, -1), 0.7, border),
        ("LEFTPADDING", (0, 0), (-1, -1), padding), ("RIGHTPADDING", (0, 0), (-1, -1), padding),
        ("TOPPADDING", (0, 0), (-1, -1), padding), ("BOTTOMPADDING", (0, 0), (-1, -1), padding),
    ]))
    return table


def styled_table(data, widths, font_size=7.6, header=True):
    converted = []
    for row_index, row in enumerate(data):
        style = ParagraphStyle(
            f"Cell{row_index}", parent=SMALL, fontSize=font_size, leading=font_size + 2,
            textColor=colors.white if header and row_index == 0 else INK,
            fontName="Arial-Bold" if header and row_index == 0 else "Arial", spaceAfter=0,
        )
        converted.append([p(str(cell), style) for cell in row])
    table = Table(converted, colWidths=widths, repeatRows=1 if header else 0)
    commands = [
        ("GRID", (0, 0), (-1, -1), 0.45, ROSE), ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]
    if header:
        commands.append(("BACKGROUND", (0, 0), (-1, 0), PLUM))
    start = 1 if header else 0
    for row_index in range(start, len(data)):
        if (row_index - start) % 2:
            commands.append(("BACKGROUND", (0, row_index), (-1, row_index), ALT))
    table.setStyle(TableStyle(commands))
    return table


def draw_page(canvas, doc):
    width, height = A4
    page = canvas.getPageNumber()
    canvas.saveState()
    if page == 1:
        canvas.setFillColor(PLUM)
        canvas.rect(0, height - 91 * mm, width, 91 * mm, fill=1, stroke=0)
        canvas.setFillColor(PINK)
        canvas.rect(0, height - 94 * mm, width, 3 * mm, fill=1, stroke=0)
    else:
        canvas.setStrokeColor(PINK)
        canvas.setLineWidth(0.8)
        canvas.line(20 * mm, height - 16 * mm, width - 20 * mm, height - 16 * mm)
        canvas.setFont("Arial", 8)
        canvas.setFillColor(MUTED)
        canvas.drawString(20 * mm, height - 12 * mm, "SLOVAK A2  |  ТЕМА 2.7")
        canvas.drawRightString(width - 20 * mm, height - 12 * mm, "Genitív множественного числа")
    canvas.setStrokeColor(PINK)
    canvas.setLineWidth(0.6)
    canvas.line(20 * mm, 14 * mm, width - 20 * mm, 14 * mm)
    canvas.setFont("Arial", 7.8)
    canvas.setFillColor(MUTED)
    canvas.drawString(20 * mm, 9 * mm, "SlovoKrok | личный учебный модуль")
    canvas.drawRightString(width - 20 * mm, 9 * mm, f"стр. {page} / 7")
    canvas.restoreState()


doc = BaseDocTemplate(
    str(OUTPUT), pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=20 * mm, bottomMargin=18 * mm,
    title="Slovak A2 - Тема 2.7 - Genitív множественного числа", author="SlovoKrok",
)
frame = Frame(20 * mm, 18 * mm, 170 * mm, 257 * mm, id="main", leftPadding=0, rightPadding=0)
doc.addPageTemplates([PageTemplate(id="series", frames=[frame], onPage=draw_page)])

story = [
    p("МОДУЛЬ 2  •  ПАДЕЖИ И УПРАВЛЕНИЕ A2", COVER_KICKER),
    p("Genitív<br/>множественного числа", TITLE),
    p("Genitív množného čísla", SUBTITLE),
    Spacer(1, 34 * mm),
    p("В теме 2.6 вы использовали готовые формы после количества. Теперь систематизируем их: где появляется -ov или -í, где окончания не слышно и почему меняется основа слова.", BODY),
    p("После модуля вы сможете:", H2),
    styled_table([
        ["1", "узнавать продуктивные окончания -ov, -í и частотное -at"],
        ["2", "понимать нулевое окончание и изменения основы"],
        ["3", "использовать частотные формы людей, предметов и единиц измерения"],
        ["4", "строить группы после количества и безопасное отрицание с niet"],
    ], [12 * mm, 158 * mm], font_size=8.0, header=False),
    Spacer(1, 3 * mm),
    box("<b>Главная формула:</b> päť + Genitív plural: päť kolegov • päť kníh • päť miest • päť eur.", PALE, PINK),
    PageBreak(),

    p("1. Продуктивные окончания", H1),
    p("Самый надёжный путь на A2 - сначала определить группу слова, затем проверить словарную пару. Ниже даны частые модели, а не правило без исключений.", BODY),
    styled_table([
        ["Модель", "Nominatív singular", "Genitív plural", "Пример"],
        ["мужской: -ov", "kolega", "kolegov", "päť kolegov"],
        ["мужской: -ov", "dom / stroj", "domov / strojov", "veľa domov"],
        ["женский: -í", "dlaň / kosť", "dlaní / kostí", "bez kostí"],
        ["средний: -í", "more", "morí", "päť morí"],
        ["средний: -í", "vysvedčenie", "vysvedčení", "bez vysvedčení"],
        ["тип dievča: -at", "dievča", "dievčat", "päť dievčat"],
    ], [34 * mm, 43 * mm, 44 * mm, 49 * mm], font_size=6.9),
    p("Согласование зависимых слов", H2),
    styled_table([
        ["Обычное прилагательное", "Мягкое прилагательное", "Притяжательное"],
        ["nových kolegov", "cudzích hostí", "mojich priateľov"],
        ["veľkých miest", "ďalších možností", "našich hotelov"],
    ], [57 * mm, 57 * mm, 56 * mm], font_size=7.0),
    box("<b>Короткий ориентир:</b> в Genitív plural род больше не меняет форму прилагательного: nových, cudzích, mojich, našich.", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    PageBreak(),

    p("2. Нулевое окончание и изменения основы", H1),
    p("У многих женских и средних существительных отдельного окончания нет. Но основа часто удлиняется или получает вставной звук. Поэтому форму нужно учить парой.", BODY),
    styled_table([
        ["Что меняется", "Словарная пара", "Готовое сочетание"],
        ["a → ie", "žena → žien", "osem žien"],
        ["i → í", "kniha → kníh", "veľa kníh"],
        ["вставка ie", "izba → izieb", "päť izieb"],
        ["o → ô", "škola → škôl", "niekoľko škôl"],
        ["e → ie", "mesto → miest", "desať miest"],
        ["вставка ie", "okno → okien", "bez okien"],
        ["l → ĺ", "jablko → jabĺk", "kilo jabĺk"],
        ["au → áu", "auto → áut", "veľa áut"],
        ["вставка e", "vajce → vajec", "šesť vajec"],
        ["без удлинения", "euro → eur", "dvadsať eur"],
    ], [36 * mm, 56 * mm, 78 * mm], font_size=6.75),
    Spacer(1, 3 * mm),
    box("<b>Важно:</b> это не механическая замена буквы. Ритмический закон и строение основы дают разные результаты: žien, kníh, izieb, škôl, miest, okien. Проверяйте новую форму в словаре.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    PageBreak(),

    p("3. Частотные формы: люди, предметы, меры", H1),
    styled_table([
        ["Люди", "Предметы", "Единицы и части"],
        ["ľudia → ľudí", "knihy → kníh", "kilá → kíl"],
        ["deti → detí", "izby → izieb", "litre → litrov"],
        ["ženy → žien", "mestá → miest", "gramy → gramov"],
        ["hostia → hostí", "vajcia → vajec", "kusy → kusov"],
        ["priatelia → priateľov", "autá → áut", "plátky → plátkov"],
        ["kolegovia → kolegov", "eurá → eur", "balenia → balení"],
    ], [57 * mm, 57 * mm, 56 * mm], font_size=7.0),
    p("После количества", H2),
    box("<b>Na kurze je päť nových kolegov.</b> - На курсе пять новых коллег.<br/><b>Potrebujeme viac voľných izieb.</b> - Нам нужно больше свободных номеров.<br/><b>Kúpime šesť čerstvých vajec.</b> - Купим шесть свежих яиц.<br/><b>Objednám päť balení čaju.</b> - Я закажу пять упаковок чая.", PALE, ROSE, SMALL),
    p("Отрицание: безопасная модель", H2),
    box("<b>V hoteli niet voľných izieb.</b> - В отеле нет свободных номеров.<br/><b>V obchode niet čerstvých rožkov.</b> - В магазине нет свежих рогаликов.<br/><b>Na stretnutí nebolo dosť stoličiek.</b> - На встрече не было достаточно стульев.", ALT, ROSE, SMALL),
    box("<b>Не копируйте русскую модель автоматически:</b> нейтрально <b>Nemám lístky</b> (Akuzatív). Genitív после обычного nemám возможен лишь в особых оттенках. Для A2 используйте <b>niet / nebolo + Genitív</b>.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    PageBreak(),

    p("4. Практика: подготовка мероприятия", H1),
    p("В связной речи Genitív plural объединяет количество, описание и отсутствие. Следите не только за существительным, но и за формой прилагательного.", BODY),
    p("Модель сообщения", H2),
    box("Na seminár príde <b>desať hostí</b> a <b>päť nových kolegov</b>. Potrebujeme <b>dvanásť stoličiek</b>, <b>osem pohárov</b> a <b>šesť fliaš vody</b>. Máme dosť <b>malých stolov</b>, ale v miestnosti niet <b>veľkých okien</b>. Objednáme <b>päť balení kávy</b>, <b>tri kilá jabĺk</b> a <b>dvesto gramov syra</b>.", PALE, ROSE, SMALL),
    p("На семинар придут десять гостей и пять новых коллег. Нам нужны двенадцать стульев, восемь стаканов и шесть бутылок воды. Маленьких столов достаточно, но в помещении нет больших окон. Закажем пять упаковок кофе, три килограмма яблок и двести граммов сыра.", SMALL),
    p("Мини-диалог", H2),
    box("<b>A:</b> Koľko ľudí príde?<br/><b>B:</b> Asi pätnásť ľudí.<br/><b>A:</b> Máme dosť stoličiek a pohárov?<br/><b>B:</b> Stoličiek áno, ale čistých pohárov je málo.<br/><b>A:</b> A čo izby pre hostí?<br/><b>B:</b> V hoteli niet voľných izieb, hľadám iný hotel.", ALT, ROSE, SMALL),
    p("Перевод: Сколько человек придёт? - Около пятнадцати. - Стульев и стаканов достаточно? - Стульев да, а чистых стаканов мало. - А номера для гостей? - В отеле нет свободных номеров, ищу другой отель.", SMALL),
    PageBreak(),

    p("5. Частые ошибки и упражнения", H1),
    box("<b>Алгоритм:</b> найдите слово количества или niet → поставьте всю группу в Genitív plural → проверьте окончание и изменение основы.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    p("Упражнение 1. Выберите форму", H2),
    p("1) päť (kolegov / kolegovia); 2) veľa (knihy / kníh); 3) desať (mestá / miest); 4) šesť (vajcia / vajec); 5) dvadsať (eurá / eur).", SMALL),
    p("Упражнение 2. Образуйте Genitív plural", H2),
    p("1) žena; 2) izba; 3) škola; 4) okno; 5) jablko; 6) auto; 7) dievča.", SMALL),
    p("Упражнение 3. Согласуйте всю группу", H2),
    p("1) päť (nový kolega); 2) veľa (dobrý človek); 3) desať (veľké mesto); 4) bez (čisté okno); 5) viac (voľná izba).", SMALL),
    p("Упражнение 4. Разделите по модели", H2),
    p("Распределите формы: kolegov, kostí, miest, dievčat, vysvedčení, áut. Группы: -ov; -í; -at; нулевое окончание с изменением основы.", SMALL),
    p("Упражнение 5. Исправьте ошибки", H2),
    p("1) Potrebujeme päť stoličky. 2) V hoteli niet voľné izby. 3) Kúpim veľa knihov. 4) Máme šesť vajcov. 5) V pokladni niet lístky na vlak.", SMALL),
    p("Упражнение 6. Подготовьте встречу", H2),
    p("Напишите 5-7 предложений: кто придёт, что нужно и чего нет. Используйте четыре разные формы Genitív plural и одну группу с прилагательным.", SMALL),
    PageBreak(),

    p("6. Ответы и проверка мастерства", H1),
    p("Ответы", H2),
    p("<b>1.</b> päť kolegov; veľa kníh; desať miest; šesť vajec; dvadsať eur.", TINY),
    p("<b>2.</b> žien; izieb; škôl; okien; jabĺk; áut; dievčat.", TINY),
    p("<b>3.</b> päť nových kolegov; veľa dobrých ľudí; desať veľkých miest; bez čistých okien; viac voľných izieb.", TINY),
    p("<b>4.</b> -ov: kolegov. -í: kostí, vysvedčení. -at: dievčat. Нулевое окончание с изменением основы: miest, áut.", TINY),
    p("<b>5.</b> 1) Potrebujeme päť stoličiek. 2) V hoteli niet voľných izieb. 3) Kúpim veľa kníh. 4) Máme šesť vajec. 5) V pokladni niet lístkov na vlak.", TINY),
    p("<b>6. Модель:</b> Na stretnutie príde desať hostí a päť nových kolegov. Potrebujeme dvanásť stoličiek a osem pohárov. V miestnosti niet veľkých okien. Máme málo fliaš vody, preto kúpime šesť fliaš. Objednáme aj päť balení kávy.", TINY),
    p("Итог в четырёх пунктах", H2),
    styled_table([
        ["OK", "Я узнаю частые окончания -ov, -í и -at."],
        ["OK", "Я понимаю нулевое окончание и учу формы žien, kníh, izieb, miest как пары."],
        ["OK", "Я согласую всю группу: päť nových kolegov / bez čistých okien."],
        ["OK", "Я различаю niet voľných izieb и нейтральное nemám lístky."],
    ], [12 * mm, 158 * mm], font_size=7.35, header=False),
    Spacer(1, 3 * mm),
    box("<b>Финальная проверка:</b> назовите по две формы людей, предметов и единиц измерения после päť или veľa, затем скажите, чего где-то нет.", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    p("Следующий шаг", H2),
    p("В теме 2.8 вы перейдёте к Datív: адресат, польза и причина, предлоги k/ku, vďaka, kvôli, oproti, proti и личные местоимения mi/mne, ti/tebe, mu/nemu, jej/nej, nám, vám, im/nim.", SMALL),
]

doc.build(story)
print(OUTPUT)
