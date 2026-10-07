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
OUTPUT = ROOT / "output" / "pdf" / "A2" / "Module_03" / "Slovak_A2_Tema_3_3_Stepeni_sravneniya_prilagatelnyh.pdf"
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
BODY = ParagraphStyle("Body", fontName="Arial", fontSize=8.9, leading=11.7, textColor=INK, spaceAfter=3.2 * mm)
SMALL = ParagraphStyle("Small", parent=BODY, fontSize=7.65, leading=9.6, spaceAfter=1.7 * mm)
TINY = ParagraphStyle("Tiny", parent=BODY, fontSize=6.95, leading=8.55, spaceAfter=1.0 * mm)
TITLE = ParagraphStyle("Title", fontName="Arial-Bold", fontSize=20, leading=24, textColor=colors.white, alignment=TA_LEFT, spaceAfter=5 * mm)
SUBTITLE = ParagraphStyle("Subtitle", fontName="Arial", fontSize=11.5, leading=15, textColor=colors.HexColor("#FFD8EB"), spaceAfter=5 * mm)
H1 = ParagraphStyle("H1", fontName="Arial-Bold", fontSize=15.5, leading=18.5, textColor=PLUM, spaceBefore=1 * mm, spaceAfter=3.2 * mm)
H2 = ParagraphStyle("H2", fontName="Arial-Bold", fontSize=10.8, leading=13.4, textColor=PINK, spaceBefore=1.5 * mm, spaceAfter=1.6 * mm)
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


def styled_table(data, widths, font_size=7.25, header=True):
    converted = []
    for row_index, row in enumerate(data):
        style = ParagraphStyle(
            f"Cell{row_index}_{font_size}_{len(data)}", parent=SMALL, fontSize=font_size, leading=font_size + 1.9,
            textColor=colors.white if header and row_index == 0 else INK,
            fontName="Arial-Bold" if header and row_index == 0 else "Arial", spaceAfter=0,
        )
        converted.append([p(str(cell), style) for cell in row])
    table = Table(converted, colWidths=widths, repeatRows=1 if header else 0)
    commands = [
        ("GRID", (0, 0), (-1, -1), 0.45, ROSE), ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4.2), ("RIGHTPADDING", (0, 0), (-1, -1), 4.2),
        ("TOPPADDING", (0, 0), (-1, -1), 3.2), ("BOTTOMPADDING", (0, 0), (-1, -1), 3.2),
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
        canvas.drawString(20 * mm, height - 12 * mm, "A2 3.3  |  Степени сравнения прилагательных")
    canvas.setFont("Arial", 8)
    canvas.setFillColor(MUTED)
    canvas.drawString(20 * mm, 9 * mm, "SlovoKrok | личный учебный модуль")
    canvas.drawRightString(width - 20 * mm, 9 * mm, f"стр. {page} / 7")
    canvas.restoreState()


doc = BaseDocTemplate(
    str(OUTPUT), pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=20 * mm, bottomMargin=18 * mm,
    title="Slovak A2 - Тема 3.3 - Степени сравнения прилагательных", author="SlovoKrok",
)
frame = Frame(20 * mm, 18 * mm, 170 * mm, 257 * mm, id="main", leftPadding=0, rightPadding=0)
doc.addPageTemplates([PageTemplate(id="series", frames=[frame], onPage=draw_page)])

story = [
    p("A2  •  ТЕМА 3.3  •  МОДУЛЬ 3  •  ПРИЛАГАТЕЛЬНЫЕ И СРАВНЕНИЕ", COVER_KICKER),
    p("Степени сравнения<br/>прилагательных", TITLE),
    p("Stupňovanie prídavných mien", SUBTITLE),
    Spacer(1, 34 * mm),
    p("Сравнение помогает выбрать человека, место, товар или вариант: не просто хороший, а лучше другого или лучший в группе.", BODY),
    p("После модуля вы сможете:", H2),
    styled_table([
        ["1", "образовывать частотные сравнительные формы на -ší и -ejší"],
        ["2", "использовать vyšší, lepší, horší и другие особые формы"],
        ["3", "строить превосходную степень с naj-"],
        ["4", "сравнивать через ako и выражать равенство через taký... ako"],
    ], [12 * mm, 158 * mm], font_size=7.35, header=False),
    Spacer(1, 3 * mm),
    box("<b>Главная формула:</b> nový - novší - najnovší; <b>A je + komparatív + ako B</b>.", PALE, PINK),
    PageBreak(),

    p("1. Три степени: признак, сравнение, максимум", H1),
    p("Качественное прилагательное имеет три степени. Вторая сравнивает два объекта, третья выбирает максимальный признак в группе.", BODY),
    styled_table([
        ["Степень", "Форма", "Что означает", "Пример"],
        ["1-я: pozitív", "nový", "обычный признак", "nový telefón"],
        ["2-я: komparatív", "novší", "больше признака", "novší telefón ako tento"],
        ["3-я: superlatív", "najnovší", "максимум в группе", "najnovší model v ponuke"],
    ], [32 * mm, 32 * mm, 46 * mm, 60 * mm], font_size=6.6),
    p("Частотные регулярные модели", H2),
    styled_table([
        ["1-я", "2-я", "3-я", "Перевод"],
        ["mladý", "mladší", "najmladší", "молодой - моложе - самый молодой"],
        ["starý", "starší", "najstarší", "старый - старше - самый старый"],
        ["dlhý", "dlhší", "najdlhší", "длинный - длиннее - самый длинный"],
        ["rýchly", "rýchlejší", "najrýchlejší", "быстрый - быстрее - самый быстрый"],
        ["lacný", "lacnejší", "najlacnejší", "дешёвый - дешевле - самый дешёвый"],
        ["moderný", "modernejší", "najmodernejší", "современный - современнее - самый современный"],
    ], [31 * mm, 38 * mm, 42 * mm, 59 * mm], font_size=6.15),
    box("<b>Надёжная стратегия:</b> окончания <b>-ší</b> и <b>-ejší</b> частотны, но форму не всегда можно предсказать по одному правилу. Учите ряд целиком: <b>lacný - lacnejší - najlacnejší</b>.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    PageBreak(),

    p("2. Особые и неправильные формы", H1),
    p("В частотных словах меняется основа. Эти ряды нужны целиком: они постоянно встречаются при выборе товара, места и варианта.", BODY),
    styled_table([
        ["1-я", "2-я", "3-я", "Перевод"],
        ["dobrý", "lepší", "najlepší", "хороший - лучше - лучший"],
        ["zlý", "horší", "najhorší", "плохой - хуже - худший"],
        ["veľký", "väčší", "najväčší", "большой - больше - самый большой"],
        ["malý", "menší", "najmenší", "маленький - меньше - самый маленький"],
        ["pekný", "krajší", "najkrajší", "красивый - красивее - самый красивый"],
        ["vysoký", "vyšší", "najvyšší", "высокий - выше - самый высокий"],
        ["nízky", "nižší", "najnižší", "низкий - ниже - самый низкий"],
        ["blízky", "bližší", "najbližší", "близкий - ближе - ближайший"],
    ], [31 * mm, 38 * mm, 42 * mm, 59 * mm], font_size=6.05),
    p("Не строим форму дважды", H2),
    styled_table([
        ["Неверно", "Правильно", "Почему"],
        ["*dobrejší", "lepší", "у dobrý меняется основа"],
        ["*zlejší", "horší", "у zlý меняется основа"],
        ["*najlepšejší", "najlepší", "naj- добавляется к lepší без нового суффикса"],
        ["*viac vysoký", "vyšší", "нейтральная форма синтетическая"],
    ], [42 * mm, 43 * mm, 85 * mm], font_size=6.55),
    box("<b>Орфография:</b> <b>vysoký - vyšší</b>, но <b>nízky - nižší</b>. Сочетание согласных и долгота меняются, поэтому проверяйте словарный ряд, а не угадывайте.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    PageBreak(),

    p("3. Ako и taký... ako", H1),
    p("Для неравного сравнения используйте <b>komparatív + ako</b>. Для равенства признака удобно использовать <b>taký/taká/také + прилагательное + ako</b>.", BODY),
    styled_table([
        ["Модель", "Пример", "Перевод"],
        ["A je vyšší ako B", "Peter je vyšší ako Martin.", "Петер выше Мартина."],
        ["A je lepší ako B", "Tento plán je lepší ako prvý.", "Этот план лучше первого."],
        ["A je lacnejší ako B", "Modrý kabát je lacnejší ako čierny.", "Синее пальто дешевле чёрного."],
        ["taký... ako", "Hotel je taký pohodlný ako apartmán.", "Отель такой же удобный, как апартаменты."],
        ["taká... ako", "Táto cesta je taká krátka ako druhá.", "Эта дорога такая же короткая, как вторая."],
        ["také... ako", "Mesto je také pokojné ako dedina.", "Город такой же спокойный, как деревня."],
    ], [38 * mm, 72 * mm, 60 * mm], font_size=6.25),
    p("Сравнительная форма согласуется", H2),
    styled_table([
        ["Род / число", "Пример"],
        ["мужской", "novší byt, lepší obchod, vyšší dom"],
        ["женский", "novšia izba, lepšia ponuka, vyššia cena"],
        ["средний", "novšie auto, lepšie miesto, vyššie poschodie"],
        ["множественное", "novšie byty, lepšie ponuky, vyššie domy"],
    ], [42 * mm, 128 * mm], font_size=6.65),
    box("<b>Опора на темы 3.1-3.2:</b> сравнительное прилагательное остаётся прилагательным и согласуется с существительным. Сравните: <b>lepší hotel, lepšia izba, lepšie miesto, lepšie hotely</b>.", PALE, ROSE, SMALL),
    PageBreak(),

    p("4. Превосходная степень и выбор варианта", H1),
    p("Превосходная степень образуется добавлением <b>naj-</b> к сравнительной форме: <b>vyšší - najvyšší, lepší - najlepší</b>. Часто после неё указывают группу через <b>z/zo + G</b> или область через <b>v/vo + L</b>.", BODY),
    styled_table([
        ["SK", "RU"],
        ["Toto je najlacnejší telefón v ponuke.", "Это самый дешёвый телефон в ассортименте."],
        ["Eva je najmladšia zo všetkých kolegýň.", "Ева самая молодая из всех коллег."],
        ["Ktorý hotel má najlepšiu polohu?", "У какого отеля лучшее расположение?"],
        ["Vybrali sme najväčšiu izbu.", "Мы выбрали самую большую комнату."],
        ["Je to najhorší variant pre rodinu.", "Это худший вариант для семьи."],
        ["Lomnický štít je vyšší ako Kriváň.", "Ломницкий Штит выше Криваня."],
        ["Táto zastávka je bližšia k centru.", "Эта остановка ближе к центру."],
        ["Nový model je menší, ale výkonnejší.", "Новая модель меньше, но мощнее."],
    ], [88 * mm, 82 * mm], font_size=6.1),
    p("Мини-диалог: выбираем жильё", H2),
    box("<b>A:</b> Ktorý byt je <b>lacnejší</b>? - Какая квартира дешевле?<br/><b>B:</b> Menší byt je lacnejší, ale je ďalej od centra. - Меньшая квартира дешевле, но дальше от центра.<br/><b>A:</b> Je veľký byt <b>taký svetlý ako</b> menší? - Большая квартира такая же светлая, как меньшая?<br/><b>B:</b> Áno, a má <b>lepšiu</b> polohu. - Да, и у неё лучше расположение.<br/><b>A:</b> Potom je to pre nás <b>najlepší</b> variant. - Тогда это лучший вариант для нас.", PALE, ROSE, TINY),
    box("<b>Смысл важнее формы:</b> superlatív требует группы или понятного контекста. <b>najlacnejší z troch</b> означает самый дешёвый из трёх, а не просто очень дешёвый.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    PageBreak(),

    p("5. Банк сравнений и упражнения", H1),
    p("Готовые модели для выбора", H2),
    styled_table([
        ["Ситуация", "Модель"],
        ["люди", "Anna je mladšia ako Eva. Peter je najstarší v tíme."],
        ["места", "Košice sú menšie ako Bratislava. Toto je najkrajšie námestie."],
        ["товары", "Tento notebook je výkonnejší. Tamten je najlacnejší."],
        ["варианты", "Prvý plán je lepší. Druhý je taký jednoduchý ako tretí."],
    ], [42 * mm, 128 * mm], font_size=6.45),
    p("Упражнение 1. Найдите степень", H2),
    p("Назовите pozitív, komparatív или superlatív: 1) nový; 2) vyšší; 3) najlepší; 4) lacnejšia; 5) najmenšie.", TINY),
    p("Упражнение 2. Образуйте 2-ю и 3-ю степень", H2),
    p("1) mladý; 2) rýchly; 3) lacný; 4) dobrý; 5) vysoký.", TINY),
    p("Упражнение 3. Согласуйте форму", H2),
    p("1) (lepší) ponuka; 2) (vyšší) poschodie; 3) (novší) byty; 4) (menší) izba; 5) (horší) výsledky.", TINY),
    p("Упражнение 4. Добавьте ako или форму taký", H2),
    p("1) Peter je vyšší ___ Martin. 2) Hotel je ___ pohodlný ako apartmán. 3) Táto izba je ___ svetlá ako prvá. 4) Modrý kabát je lacnejší ___ čierny.", TINY),
    p("Упражнение 5. Исправьте ошибки", H2),
    p("1) Tento plán je dobrejší. 2) Eva je najmladší kolegyňa. 3) Dom je viac vysoký ako hotel. 4) To je najlepšejší obchod. 5) Auto je lacnejšia ako vlak.", TINY),
    p("Упражнение 6. Выберите вариант", H2),
    p("Сравните в 5-7 предложениях два товара, места или варианта. Используйте три сравнительные формы, одно равенство с taký... ako и одну превосходную форму с ясной группой.", TINY),
    PageBreak(),

    p("6. Ответы и проверка мастерства", H1),
    p("Ответы", H2),
    p("<b>1.</b> nový - pozitív; vyšší - komparatív; najlepší - superlatív; lacnejšia - komparatív; najmenšie - superlatív.", TINY),
    p("<b>2.</b> mladší - najmladší; rýchlejší - najrýchlejší; lacnejší - najlacnejší; lepší - najlepší; vyšší - najvyšší.", TINY),
    p("<b>3.</b> lepšia ponuka; vyššie poschodie; novšie byty; menšia izba; horšie výsledky.", TINY),
    p("<b>4.</b> Peter je vyšší ako Martin. Hotel je taký pohodlný ako apartmán. Táto izba je taká svetlá ako prvá. Modrý kabát je lacnejší ako čierny.", TINY),
    p("<b>5.</b> Tento plán je lepší. Eva je najmladšia kolegyňa. Dom je vyšší ako hotel. To je najlepší obchod. Auto je lacnejšie ako vlak.", TINY),
    p("<b>6. Модель:</b> Prvý hotel je lacnejší ako druhý, ale je ďalej od centra. Druhý hotel má väčšiu izbu a lepšiu polohu. Je taký pokojný ako prvý. Prvý hotel je modernejší, no druhý má krajší výhľad. Pre našu rodinu je druhý hotel najlepší variant. Возможны другие естественные варианты.", TINY),
    p("Итог в четырёх пунктах", H2),
    styled_table([
        ["OK", "Строю частотные формы на -ší/-ejší и учу ряд целиком."],
        ["OK", "Знаю vyšší, lepší, horší, väčší, menší и krajší."],
        ["OK", "Добавляю naj- к сравнительной форме и согласую прилагательное."],
        ["OK", "Сравниваю через ako и выражаю равенство через taký... ako."],
    ], [12 * mm, 158 * mm], font_size=6.85, header=False),
    Spacer(1, 2.2 * mm),
    box("<b>Финальная проверка:</b> без таблицы сравните два телефона или два места: назовите три различия, одно сходство и лучший вариант в ясной группе.", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    p("Следующий шаг", H2),
    p("В теме 3.4 вы перенесёте логику сравнения на наречия: rýchlo - rýchlejšie - najrýchlejšie.", SMALL),
]

doc.build(story)
print(OUTPUT)
