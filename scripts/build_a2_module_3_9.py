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
OUTPUT = ROOT / "output" / "pdf" / "A2" / "Module_03" / "Slovak_A2_Tema_3_9_Chislitelnye_daty_i_kolichestvo.pdf"
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
BODY = ParagraphStyle("Body", fontName="Arial", fontSize=8.75, leading=11.5, textColor=INK, spaceAfter=3 * mm)
SMALL = ParagraphStyle("Small", parent=BODY, fontSize=7.6, leading=9.5, spaceAfter=1.65 * mm)
TINY = ParagraphStyle("Tiny", parent=BODY, fontSize=6.85, leading=8.45, spaceAfter=1.0 * mm)
TITLE = ParagraphStyle("Title", fontName="Arial-Bold", fontSize=20, leading=24, textColor=colors.white, alignment=TA_LEFT, spaceAfter=5 * mm)
SUBTITLE = ParagraphStyle("Subtitle", fontName="Arial", fontSize=11.5, leading=15, textColor=colors.HexColor("#FFD8EB"), spaceAfter=5 * mm)
H1 = ParagraphStyle("H1", fontName="Arial-Bold", fontSize=15.5, leading=18.5, textColor=PLUM, spaceBefore=1 * mm, spaceAfter=3 * mm)
H2 = ParagraphStyle("H2", fontName="Arial-Bold", fontSize=10.7, leading=13.2, textColor=PINK, spaceBefore=1.3 * mm, spaceAfter=1.5 * mm)
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


def styled_table(data, widths, font_size=7.1, header=True):
    converted = []
    for row_index, row in enumerate(data):
        style = ParagraphStyle(
            f"Cell{row_index}_{font_size}_{len(data)}", parent=SMALL, fontSize=font_size,
            leading=font_size + 1.8, textColor=colors.white if header and row_index == 0 else INK,
            fontName="Arial-Bold" if header and row_index == 0 else "Arial", spaceAfter=0,
        )
        converted.append([p(str(cell), style) for cell in row])
    table = Table(converted, colWidths=widths, repeatRows=1 if header else 0)
    commands = [
        ("GRID", (0, 0), (-1, -1), 0.45, ROSE), ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4.0), ("RIGHTPADDING", (0, 0), (-1, -1), 4.0),
        ("TOPPADDING", (0, 0), (-1, -1), 3.0), ("BOTTOMPADDING", (0, 0), (-1, -1), 3.0),
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
        canvas.drawString(20 * mm, height - 12 * mm, "A2 3.9  |  Числительные, даты и количество")
    canvas.setFont("Arial", 8)
    canvas.setFillColor(MUTED)
    canvas.drawString(20 * mm, 9 * mm, "SlovoKrok | личный учебный модуль")
    canvas.drawRightString(width - 20 * mm, 9 * mm, f"стр. {page} / 7")
    canvas.restoreState()


doc = BaseDocTemplate(
    str(OUTPUT), pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=20 * mm, bottomMargin=18 * mm,
    title="Slovak A2 - Тема 3.9 - Числительные, даты и количество", author="SlovoKrok",
)
frame = Frame(20 * mm, 18 * mm, 170 * mm, 257 * mm, id="main", leftPadding=0, rightPadding=0)
doc.addPageTemplates([PageTemplate(id="series", frames=[frame], onPage=draw_page)])

story = [
    p("МОДУЛЬ 3  •  ПРИЛАГАТЕЛЬНЫЕ, МЕСТОИМЕНИЯ И ЧИСЛИТЕЛЬНЫЕ", COVER_KICKER),
    p("Числительные, даты<br/>и количество", TITLE),
    p("Číslovky, dátumy a množstvo: от одного до приблизительного", SUBTITLE),
    Spacer(1, 35 * mm),
    p("Словацкое число меняет форму существительного: <b>dve ženy</b>, но <b>päť žien</b>. Для мужчин-людей появляются особые формы <b>dvaja, traja, štyria</b>, а дата требует порядкового числительного и Genitív месяца."),
    p("После модуля вы сможете:", H2),
    styled_table([
        ["1", "выбирать jeden/jedna/jedno, dva/dve и dvaja/traja/štyria"],
        ["2", "строить количество 3-4 и 5+ с правильной формой существительного"],
        ["3", "спрашивать и называть дату: Koľkého je dnes?"],
        ["4", "говорить приблизительно: asi, okolo, niekoľko, päť až sedem"],
    ], [12 * mm, 158 * mm], font_size=7.2, header=False),
    Spacer(1, 3 * mm),
    box("<b>Маршрут:</b> 1 согласуется с родом; 2-4 выбирают форму по типу существительного; после 5+ существительное обычно стоит в Genitív množného čísla.", PALE, PINK),
    PageBreak(),

    p("1. Один, два, три, четыре", H1),
    p("Числительное <b>jeden</b> согласуется в роде. Для 2 различайте <b>dva</b> и <b>dve</b>. С группой мужчин или смешанной группой людей употребляются личные формы <b>dvaja, traja, štyria</b>."),
    styled_table([
        ["Число", "Мужчины-люди", "Муж. предмет", "Жен. род", "Сред. род"],
        ["1", "jeden muž", "jeden dom", "jedna žena", "jedno dieťa"],
        ["2", "dvaja muži", "dva domy", "dve ženy", "dve deti"],
        ["3", "traja muži", "tri domy", "tri ženy", "tri deti"],
        ["4", "štyria muži", "štyri domy", "štyri ženy", "štyri deti"],
    ], [17 * mm, 39 * mm, 38 * mm, 38 * mm, 38 * mm], font_size=6.2),
    p("В живой речи", H2),
    styled_table([
        ["SK", "RU"],
        ["Prišiel jeden kolega.", "Пришёл один коллега."],
        ["Prišli dvaja kolegovia.", "Пришли два коллеги."],
        ["Máme dva voľné stoly.", "У нас есть два свободных стола."],
        ["Čakajú tu dve zákazníčky.", "Здесь ждут две клиентки."],
        ["V izbe sú tri okná.", "В комнате три окна."],
        ["Štyria študenti píšu test.", "Четыре студента пишут тест."],
    ], [84 * mm, 86 * mm], font_size=6.4),
    box("<b>Типичная ошибка:</b> не *dva ženy и не *dve muži. Сравните: <b>dva stoly, dve ženy, dvaja muži</b>.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    PageBreak(),

    p("2. Пять и больше", H1),
    p("В прямой конструкции после 5 и выше существительное получает <b>Genitív množného čísla</b>. Это практическое продолжение темы 2.6, а не новая таблица падежей."),
    styled_table([
        ["Количество", "Люди", "Предметы / время"],
        ["5", "päť mužov, päť žien", "päť domov, päť minút"],
        ["6", "šesť kolegov", "šesť otázok, šesť hodín"],
        ["10", "desať hostí", "desať lístkov, desať eur"],
        ["21", "dvadsaťjeden študentov", "dvadsaťjeden dní"],
        ["100", "sto ľudí", "sto strán"],
    ], [27 * mm, 65 * mm, 78 * mm], font_size=6.45),
    p("Сказуемое с количеством", H2),
    p("Нейтральная и безопасная модель с 5+ использует сказуемое в единственном числе; в прошедшем времени - форму среднего рода."),
    styled_table([
        ["SK", "RU"],
        ["Päť ľudí čaká pred kinom.", "Пять человек ждут перед кинотеатром."],
        ["Prišlo päť hostí.", "Пришли пять гостей."],
        ["Desať študentov písalo test.", "Десять студентов писали тест."],
        ["Na stole leží šesť kníh.", "На столе лежат шесть книг."],
        ["Cesta trvá dvadsať minút.", "Дорога длится двадцать минут."],
    ], [84 * mm, 86 * mm], font_size=6.45),
    box("<b>Сравните:</b> <b>štyri knihy sú</b>, но <b>päť kníh je</b>. Число 5 меняет и форму существительного, и нейтральное согласование сказуемого.", PALE, ROSE, SMALL),
    PageBreak(),

    p("3. Порядковые числительные и дата", H1),
    p("Порядковые числительные отвечают на вопрос <b>koľký?</b> и согласуются как прилагательные: <b>prvý deň, druhá lekcia, tretie miesto</b>. В записи даты после числа ставится точка."),
    styled_table([
        ["Цифра", "Базовая форма", "В дате: Genitív муж. рода"],
        ["1.", "prvý / prvá / prvé", "prvého"],
        ["2.", "druhý / druhá / druhé", "druhého"],
        ["3.", "tretí / tretia / tretie", "tretieho"],
        ["4.", "štvrtý / štvrtá / štvrté", "štvrtého"],
        ["5.", "piaty / piata / piate", "piateho"],
        ["22.", "dvadsiaty druhý", "dvadsiateho druhého"],
    ], [24 * mm, 72 * mm, 74 * mm], font_size=6.3),
    p("Месяцы в дате", H2),
    styled_table([
        ["Nominatív", "Genitív", "Nominatív", "Genitív"],
        ["január", "januára", "júl", "júla"],
        ["február", "februára", "august", "augusta"],
        ["marec", "marca", "september", "septembra"],
        ["apríl", "apríla", "október", "októbra"],
        ["máj", "mája", "november", "novembra"],
        ["jún", "júna", "december", "decembra"],
    ], [42 * mm, 43 * mm, 42 * mm, 43 * mm], font_size=6.25),
    box("<b>Главная модель:</b> <b>Koľkého je dnes? Dnes je piateho mája.</b> Запись: <b>5. mája 2026</b>. Произношение: <b>piateho mája dvetisícdvadsaťšesť</b>.", PALE, PINK, SMALL),
    PageBreak(),

    p("4. Точные и приблизительные количества", H1),
    p("Приблизительность можно выразить без сложного вычисления. Выбор конструкции определяет падеж числительного или существительного."),
    styled_table([
        ["Модель", "Пример", "Смысл"],
        ["asi + число", "asi desať ľudí", "примерно десять человек"],
        ["približne + число", "približne dvadsať minút", "приблизительно двадцать минут"],
        ["okolo + G", "okolo desiatich eur", "около десяти евро"],
        ["от - до", "päť až sedem dní", "от пяти до семи дней"],
        ["niekoľko + G pl.", "niekoľko otázok", "несколько вопросов"],
        ["veľa / málo + G", "veľa práce; málo času", "много работы; мало времени"],
        ["takmer + число", "takmer sto strán", "почти сто страниц"],
    ], [37 * mm, 66 * mm, 67 * mm], font_size=6.25),
    p("Мини-диалог: встреча и дата", H2),
    box("<b>A:</b> Koľko ľudí príde na stretnutie? - Сколько человек придёт на встречу?<br/><b>B:</b> Asi desať. Zatiaľ sa prihlásilo osem ľudí. - Примерно десять. Пока записались восемь человек.<br/><b>A:</b> Kedy sa stretneme? - Когда встретимся?<br/><b>B:</b> Dvadsiateho druhého októbra o šiestej. - Двадцать второго октября в шесть.<br/><b>A:</b> Ako dlho to potrvá? - Как долго это продлится?<br/><b>B:</b> Približne deväťdesiat minút. - Около девяноста минут.", PALE, ROSE, TINY),
    box("<b>Не смешивайте:</b> <b>desiaty</b> = десятый по порядку; <b>desať</b> = десять; <b>okolo desiatich</b> = около десяти.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    PageBreak(),

    p("5. Частые ошибки и упражнения", H1),
    box("<b>Частые ошибки:</b> *dva ženy -> <b>dve ženy</b>; *tri muži -> <b>traja muži</b>; *päť ženy -> <b>päť žien</b>; *5 mája -> <b>5. mája</b>; *piaty mája в ответе на Koľkého? -> <b>piateho mája</b>.", CREAM, colors.HexColor("#E7C76C"), TINY),
    p("Упражнение 1. Выберите форму", H2),
    p("1) jeden/jedna kniha; 2) dva/dve autá; 3) dva/dvaja kolegovia; 4) tri/traja muži; 5) štyri/štyria okná.", TINY),
    p("Упражнение 2. Поставьте существительное после числа", H2),
    p("1) päť (žena); 2) sedem (deň); 3) desať (otázka); 4) dvadsať (minúta); 5) sto (strana).", TINY),
    p("Упражнение 3. Исправьте ошибки", H2),
    p("1) Prišli dve kolegovia. 2) Mám päť knihy. 3) Štyri ľudia čakajú. 4) Dnes je piaty mája. 5) Stretneme sa 12 júna.", TINY),
    p("Упражнение 4. Запишите дату словами", H2),
    p("1) 1. 1.; 2) 3. 4.; 3) 11. 5.; 4) 22. 10.; 5) 31. 12. Используйте ответ на вопрос Koľkého?", TINY),
    p("Упражнение 5. Выразите приблизительность", H2),
    p("Переведите: 1) примерно десять человек; 2) около двадцати евро; 3) пять-семь дней; 4) несколько вопросов; 5) почти сто страниц.", TINY),
    p("Упражнение 6. Своя встреча", H2),
    p("Напишите 5-7 предложений: дата, время, точное и приблизительное число участников, длительность и количество нужных предметов.", TINY),
    PageBreak(),

    p("6. Ответы и проверка мастерства", H1),
    p("Ответы", H2),
    p("<b>1.</b> jedna kniha; dve autá; dvaja kolegovia; traja muži; štyri okná.", TINY),
    p("<b>2.</b> päť žien; sedem dní; desať otázok; dvadsať minút; sto strán.", TINY),
    p("<b>3.</b> Prišli dvaja kolegovia. Mám päť kníh. Štyria ľudia čakajú. Dnes je piateho mája. Stretneme sa 12. júna.", TINY),
    p("<b>4.</b> prvého januára; tretieho apríla; jedenásteho mája; dvadsiateho druhého októbra; tridsiateho prvého decembra.", TINY),
    p("<b>5.</b> asi desať ľudí; okolo dvadsiatich eur; päť až sedem dní; niekoľko otázok; takmer sto strán.", TINY),
    p("<b>6. Модель:</b> Stretnutie bude dvadsiateho druhého októbra o šiestej. Príde asi desať ľudí. Zatiaľ sa prihlásili štyria kolegovia a dve kolegyne. Program bude trvať približne deväťdesiat minút. Potrebujeme dvanásť stoličiek a niekoľko fliaš vody. Возможны другие естественные варианты.", TINY),
    p("Итог в четырёх пунктах", H2),
    styled_table([
        ["OK", "Различаю dva domy, dve ženy и dvaja muži."],
        ["OK", "После 5+ ставлю существительное в Genitív množného čísla."],
        ["OK", "Называю дату: piateho mája; 5. mája 2026."],
        ["OK", "Использую asi, okolo, niekoľko и päť až sedem."],
    ], [12 * mm, 158 * mm], font_size=6.55, header=False),
    Spacer(1, 2 * mm),
    box("<b>Финальная проверка:</b> без таблицы скажите «двое коллег», «две книги», «пять женщин», сегодняшнюю дату и «около двадцати минут».", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    p("Следующий шаг", H2),
    p("В теме 4.1 вы будете чередовать фон, незавершённый процесс и цепочку завершённых событий в связном рассказе.", SMALL),
]

doc.build(story)
print(OUTPUT)
