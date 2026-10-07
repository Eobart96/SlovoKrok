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
OUTPUT = ROOT / "output" / "pdf" / "A2" / "Module_02" / "Slovak_A2_Tema_2_6_Genitiv_kolichestva_i_mery.pdf"
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
        canvas.drawString(20 * mm, height - 12 * mm, "SLOVAK A2  |  ТЕМА 2.6")
        canvas.drawRightString(width - 20 * mm, height - 12 * mm, "Genitív количества и меры")
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
    title="Slovak A2 - Тема 2.6 - Genitív количества и меры", author="SlovoKrok",
)
frame = Frame(20 * mm, 18 * mm, 170 * mm, 257 * mm, id="main", leftPadding=0, rightPadding=0)
doc.addPageTemplates([PageTemplate(id="series", frames=[frame], onPage=draw_page)])

story = [
    p("МОДУЛЬ 2  •  ПАДЕЖИ И УПРАВЛЕНИЕ A2", COVER_KICKER),
    p("Genitív<br/>количества и меры", TITLE),
    p("Genitív množstva a miery", SUBTITLE),
    Spacer(1, 34 * mm),
    p("В теме 2.5 Genitív стоял после предлогов. Теперь он отвечает на вопрос koľko? и связывает количество с тем, что мы считаем, взвешиваем, наливаем или сравниваем.", BODY),
    p("После модуля вы сможете:", H2),
    styled_table([
        ["1", "заказывать kilo, liter, kus, kúsok или plátok продукта"],
        ["2", "говорить о приблизительном количестве с trochu, veľa и málo"],
        ["3", "сравнивать количество с viac и menej"],
        ["4", "строить сочетания с числительными от пяти"],
    ], [12 * mm, 158 * mm], font_size=8.0, header=False),
    Spacer(1, 3 * mm),
    box("<b>Главная формула:</b> количество + Genitív: kilo jabĺk • liter mlieka • trochu vody • päť rožkov.", PALE, PINK),
    PageBreak(),

    p("1. Точное количество: единица + продукт", H1),
    p("Сначала называем меру или часть, затем продукт в Genitív. Форма продукта не зависит от того, одну или две меры мы покупаем.", BODY),
    styled_table([
        ["Мера", "Готовое сочетание", "Перевод"],
        ["kilo", "kilo jabĺk", "килограмм яблок"],
        ["liter", "liter mlieka", "литр молока"],
        ["kus", "kus torty", "кусок торта"],
        ["kúsok", "kúsok chleba", "кусочек хлеба"],
        ["plátok", "plátok syra", "ломтик сыра"],
        ["gram", "dvesto gramov šunky", "двести граммов ветчины"],
    ], [30 * mm, 67 * mm, 73 * mm], font_size=7.1),
    p("Меняется мера, продукт сохраняет Genitív", H2),
    styled_table([
        ["1", "2-4", "5 и больше"],
        ["jedno kilo jabĺk", "dve kilá jabĺk", "päť kíl jabĺk"],
        ["jeden liter vody", "dva litre vody", "päť litrov vody"],
        ["jeden kus torty", "dva kusy torty", "päť kusov torty"],
        ["jeden plátok syra", "dva plátky syra", "päť plátkov syra"],
    ], [55 * mm, 55 * mm, 60 * mm], font_size=7.0),
    box("<b>Не путайте:</b> dve kilá, но päť kíl; dva litre, но päť litrov. После меры продукт остаётся: jabĺk, vody, torty, syra.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    PageBreak(),

    p("2. Точный счёт: от пяти", H1),
    p("После päť и последующих числительных предмет стоит в Genitív plural. В этой теме используйте частотные формы как готовые блоки; способы образования системно разбираются в 2.7.", BODY),
    styled_table([
        ["Число", "Люди", "Предметы", "Еда"],
        ["5", "päť ľudí", "päť lístkov", "päť jabĺk"],
        ["6", "šesť kolegov", "šesť stolov", "šesť rožkov"],
        ["7", "sedem detí", "sedem dní", "sedem vajec"],
        ["8", "osem žien", "osem izieb", "osem paradajok"],
        ["10", "desať hostí", "desať eur", "desať banánov"],
    ], [24 * mm, 46 * mm, 48 * mm, 52 * mm], font_size=7.0),
    p("Полезные модели", H2),
    box("<b>Potrebujem päť lístkov.</b> - Мне нужно пять билетов.<br/><b>Kúpime šesť rožkov.</b> - Мы купим шесть рогаликов.<br/><b>Na stretnutí je desať ľudí.</b> - На встрече десять человек.<br/><b>Hotel má osem izieb.</b> - В отеле восемь номеров.", PALE, ROSE, SMALL),
    box("<b>Граница темы:</b> сейчас важно связать число с готовой формой. Почему появляются ľudí, detí, žien, vajec или izieb, подробно объяснит тема 2.7.", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    PageBreak(),

    p("3. Приблизительно: trochu, veľa, málo", H1),
    p("Эти слова не называют точную цифру. После них тоже нужен Genitív: единственное число у вещества или абстрактного понятия, множественное у считаемых предметов и людей.", BODY),
    styled_table([
        ["Слово", "С веществом / понятием", "Со считаемым", "Смысл"],
        ["trochu", "trochu vody", "trochu jabĺk", "немного"],
        ["veľa", "veľa práce", "veľa ľudí", "много"],
        ["málo", "málo času", "málo obchodov", "мало"],
    ], [28 * mm, 50 * mm, 48 * mm, 44 * mm], font_size=7.0),
    p("Сравнение: viac и menej", H2),
    styled_table([
        ["Больше", "Меньше", "Перевод"],
        ["viac vody", "menej vody", "больше / меньше воды"],
        ["viac času", "menej času", "больше / меньше времени"],
        ["viac zeleniny", "menej cukru", "больше овощей / меньше сахара"],
        ["viac ľudí", "menej áut", "больше людей / меньше машин"],
    ], [53 * mm, 53 * mm, 64 * mm], font_size=7.05),
    Spacer(1, 3 * mm),
    box("<b>Русскоязычная ловушка:</b> не добавляйте предлог z: правильно <b>trochu vody</b>, <b>veľa ľudí</b>, <b>viac času</b>.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    PageBreak(),

    p("4. В магазине и кафе", H1),
    p("Модель просьбы: <b>Prosím si + количество + Genitív.</b> Для уточнения используйте Koľko? или Ešte niečo?", BODY),
    p("Мини-диалог", H2),
    box("<b>Predavačka:</b> Nech sa páči. Čo si prosíte?<br/><b>Zákazník:</b> Prosím si kilo jabĺk, dva litre mlieka a päť rožkov.<br/><b>Predavačka:</b> Ešte niečo?<br/><b>Zákazník:</b> Áno, dvesto gramov šunky a štyri plátky syra.<br/><b>Predavačka:</b> Je to všetko?<br/><b>Zákazník:</b> Ešte trochu zeleniny, ale menej paradajok. Ďakujem.", PALE, ROSE, SMALL),
    p("Продавец: Пожалуйста. Что желаете? - Покупатель: Килограмм яблок, два литра молока и пять рогаликов. - Ещё что-нибудь? - Да, двести граммов ветчины и четыре ломтика сыра. - Это всё? - Ещё немного овощей, но поменьше помидоров. Спасибо.", SMALL),
    p("Готовые реплики", H2),
    styled_table([
        ["Словацкий", "Русский"],
        ["Prosím si liter minerálky.", "Литр минеральной воды, пожалуйста."],
        ["Dám si kúsok torty.", "Я возьму кусочек торта."],
        ["Potrebujem viac ryže.", "Мне нужно больше риса."],
        ["Dajte mi menej cukru, prosím.", "Положите мне меньше сахара, пожалуйста."],
        ["Koľko kusov potrebujete?", "Сколько штук вам нужно?"],
    ], [85 * mm, 85 * mm], font_size=7.05),
    PageBreak(),

    p("5. Частые ошибки и упражнения", H1),
    box("<b>Алгоритм:</b> точное или приблизительное количество → мера / число → готовая форма продукта в Genitív.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    p("Упражнение 1. Выберите подходящее слово", H2),
    p("1) ___ vody (немного); 2) ___ času (мало); 3) ___ zeleniny (больше); 4) ___ cukru (меньше); 5) ___ ľudí (много).", SMALL),
    p("Упражнение 2. Соберите точное количество", H2),
    p("1) kilo + jablká; 2) liter + mlieko; 3) kúsok + torta; 4) plátok + syr; 5) dvesto gramov + šunka.", SMALL),
    p("Упражнение 3. Выберите форму меры", H2),
    p("1) dve (kilo / kilá / kíl) jabĺk; 2) päť (liter / litre / litrov) vody; 3) tri (kus / kusy / kusov) torty; 4) šesť (plátok / plátky / plátkov) syra.", SMALL),
    p("Упражнение 4. Вставьте форму после числа", H2),
    p("1) päť (lístok); 2) šesť (rožok); 3) sedem (dieťa); 4) osem (žena); 5) desať (euro).", SMALL),
    p("Упражнение 5. Исправьте ошибки", H2),
    p("1) Prosím si kilo jablká. 2) Potrebujem veľa čas. 3) Dajte mi dve kíl zemiakov. 4) Kúpime päť rožky. 5) Chcem viac cukor.", SMALL),
    p("Упражнение 6. Сделайте заказ", H2),
    p("Напишите 5-7 реплик покупателя: две точные меры, одно число от пяти, trochu или veľa и сравнение с viac / menej.", SMALL),
    PageBreak(),

    p("6. Ответы и проверка мастерства", H1),
    p("Ответы", H2),
    p("<b>1.</b> trochu vody; málo času; viac zeleniny; menej cukru; veľa ľudí.", TINY),
    p("<b>2.</b> kilo jabĺk; liter mlieka; kúsok torty; plátok syra; dvesto gramov šunky.", TINY),
    p("<b>3.</b> dve kilá jabĺk; päť litrov vody; tri kusy torty; šesť plátkov syra.", TINY),
    p("<b>4.</b> päť lístkov; šesť rožkov; sedem detí; osem žien; desať eur.", TINY),
    p("<b>5.</b> 1) Prosím si kilo jabĺk. 2) Potrebujem veľa času. 3) Dajte mi dve kilá zemiakov. 4) Kúpime päť rožkov. 5) Chcem viac cukru.", TINY),
    p("<b>6. Модель:</b> Prosím si kilo jabĺk a dva litre mlieka. Potrebujem aj šesť rožkov. Dajte mi dvesto gramov šunky a trochu syra. Prosím si viac zeleniny, ale menej paradajok. To je všetko, ďakujem.", TINY),
    p("Итог в четырёх пунктах", H2),
    styled_table([
        ["OK", "Я строю сочетания kilo jabĺk, liter mlieka, kus torty и plátok syra."],
        ["OK", "Я говорю trochu, veľa, málo, viac или menej + Genitív."],
        ["OK", "Я различаю dve kilá и päť kíl, dva litre и päť litrov."],
        ["OK", "Я использую готовые формы после числительных от пяти."],
    ], [12 * mm, 158 * mm], font_size=7.4, header=False),
    Spacer(1, 3 * mm),
    box("<b>Финальная проверка:</b> закажите продукты для завтрака, назвав две меры, одно число от пяти и одно приблизительное количество.", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    p("Следующий шаг", H2),
    p("В теме 2.7 вы систематизируете Genitív plural: продуктивные окончания, нулевое окончание, изменения основы и частотные формы людей, предметов и единиц измерения.", SMALL),
]

doc.build(story)
print(OUTPUT)
