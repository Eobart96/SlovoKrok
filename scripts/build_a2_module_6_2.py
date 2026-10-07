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
OUTPUT = ROOT / "output/pdf/A2/Module_06/Slovak_A2_Tema_6_2_Obyavlenie_i_poisk_zhilya.pdf"
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
BODY = ParagraphStyle("Body", fontName="Arial", fontSize=8.65, leading=11.3, textColor=INK, spaceAfter=2.7 * mm)
SMALL = ParagraphStyle("Small", parent=BODY, fontSize=7.45, leading=9.2, spaceAfter=1.4 * mm)
TINY = ParagraphStyle("Tiny", parent=BODY, fontSize=6.65, leading=8.1, spaceAfter=0.9 * mm)
TITLE = ParagraphStyle("Title", fontName="Arial-Bold", fontSize=20, leading=24, textColor=colors.white, alignment=TA_LEFT, spaceAfter=5 * mm)
SUBTITLE = ParagraphStyle("Subtitle", fontName="Arial", fontSize=11.5, leading=15, textColor=colors.HexColor("#FFD8EB"), spaceAfter=5 * mm)
H1 = ParagraphStyle("H1", fontName="Arial-Bold", fontSize=15.5, leading=18.5, textColor=PLUM, spaceBefore=1 * mm, spaceAfter=3 * mm)
H2 = ParagraphStyle("H2", fontName="Arial-Bold", fontSize=10.7, leading=13.2, textColor=PINK, spaceBefore=1.1 * mm, spaceAfter=1.4 * mm)
KICK = ParagraphStyle("Kicker", fontName="Arial-Bold", fontSize=10, leading=12, textColor=colors.HexColor("#FFD8EB"), spaceAfter=4 * mm)


def p(text, style=BODY):
    return Paragraph(text, style)


def box(text, bg=PALE, border=ROSE, style=BODY, pad=7):
    item = Table([[p(text, style)]], colWidths=[170 * mm])
    item.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("BOX", (0, 0), (-1, -1), 0.7, border),
        ("LEFTPADDING", (0, 0), (-1, -1), pad),
        ("RIGHTPADDING", (0, 0), (-1, -1), pad),
        ("TOPPADDING", (0, 0), (-1, -1), pad),
        ("BOTTOMPADDING", (0, 0), (-1, -1), pad),
    ]))
    return item


def table(data, widths, size=7.0, header=True):
    rows = []
    for row_index, row in enumerate(data):
        style = ParagraphStyle(
            f"cell_{row_index}_{size}_{len(data)}",
            parent=SMALL,
            fontSize=size,
            leading=size + 1.75,
            textColor=colors.white if header and row_index == 0 else INK,
            fontName="Arial-Bold" if header and row_index == 0 else "Arial",
            spaceAfter=0,
        )
        rows.append([p(str(value), style) for value in row])
    item = Table(rows, colWidths=widths, repeatRows=1 if header else 0)
    commands = [
        ("GRID", (0, 0), (-1, -1), 0.45, ROSE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]
    if header:
        commands.append(("BACKGROUND", (0, 0), (-1, 0), PLUM))
    start = 1 if header else 0
    for row_index in range(start, len(data)):
        if (row_index - start) % 2:
            commands.append(("BACKGROUND", (0, row_index), (-1, row_index), ALT))
    item.setStyle(TableStyle(commands))
    return item


def draw_page(canvas, doc):
    width, height = A4
    page_number = canvas.getPageNumber()
    canvas.saveState()
    if page_number == 1:
        canvas.setFillColor(PLUM)
        canvas.rect(0, height - 91 * mm, width, 91 * mm, fill=1, stroke=0)
        canvas.setFillColor(PINK)
        canvas.rect(0, height - 94 * mm, width, 3 * mm, fill=1, stroke=0)
    else:
        canvas.setStrokeColor(PINK)
        canvas.line(20 * mm, height - 16 * mm, width - 20 * mm, height - 16 * mm)
        canvas.setFont("Arial", 8)
        canvas.setFillColor(MUTED)
        canvas.drawString(20 * mm, height - 12 * mm, "A2 6.2  |  Объявление и поиск жилья")
    canvas.setFont("Arial", 8)
    canvas.setFillColor(MUTED)
    canvas.drawString(20 * mm, 9 * mm, "SlovoKrok | личный учебный модуль")
    canvas.drawRightString(width - 20 * mm, 9 * mm, f"стр. {page_number} / 7")
    canvas.restoreState()


doc = BaseDocTemplate(
    str(OUTPUT), pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm,
    topMargin=20 * mm, bottomMargin=18 * mm,
    title="Slovak A2 - Тема 6.2 - Объявление и поиск жилья",
    author="SlovoKrok",
)
doc.addPageTemplates([
    PageTemplate(id="series", frames=[Frame(20 * mm, 18 * mm, 170 * mm, 257 * mm, id="main", leftPadding=0, rightPadding=0)], onPage=draw_page)
])


story = [
    p("МОДУЛЬ 6  •  ДОМ, ИНТЕРНЕТ И ПОКУПКИ", KICK),
    p("Объявление и<br/>поиск жилья", TITLE),
    p("Inzerát a hľadanie bývania: читаем условия, сравниваем и пишем владельцу", SUBTITLE),
    Spacer(1, 41 * mm),
    p("Объявление о жилье сжимает много информации в несколько строк. На уровне A2 нужно увидеть цену и дополнительные платежи, понять ограничения, сравнить варианты и задать вежливые уточняющие вопросы."),
    p("После модуля вы сможете:", H2),
    table([
        ["1", "извлечь из объявления площадь, цену и условия"],
        ["2", "понимать Genitív в типичных формулировках"],
        ["3", "сравнить два варианта по важным критериям"],
        ["4", "написать владельцу короткое вежливое сообщение"],
    ], [12 * mm, 158 * mm], 7.2, False),
    Spacer(1, 3 * mm),
    box("<b>Формула поиска:</b> прочитайте факты + отметьте неизвестное + сравните по своим критериям + задайте владельцу 3-4 точных вопроса."),
    PageBreak(),

    p("1. Как читать объявление", H1),
    p("Сначала найдите факты, которые можно сравнить. Не делайте вывод по одному слову <i>pekný</i>: площадь, полная цена и условия важнее рекламных оценок."),
    table([
        ["Параметр", "Типичная запись", "Что это значит"],
        ["тип", "2-izbový byt", "двухкомнатная квартира"],
        ["площадь", "48 m²", "48 квадратных метров"],
        ["цена", "nájom 650 € mesačne", "аренда 650 евро в месяц"],
        ["энергия", "energie 120 €", "коммунальные платежи 120 евро"],
        ["залог", "depozit vo výške nájmu", "залог в размере месячной аренды"],
        ["срок", "voľný od 1. októbra", "свободен с 1 октября"],
    ], [30 * mm, 65 * mm, 75 * mm], 5.75),
    p("Образец объявления", H2),
    box("<b>Prenajmem svetlý 2-izbový byt v Ružinove, 48 m², 3. poschodie s výťahom.</b> Byt je zariadený, bez balkóna. Nájom je 650 € mesačne, energie 120 €. Internet nie je v cene. Depozit je vo výške jedného nájmu. Byt je voľný od 1. októbra, nefajčiari, bez domácich zvierat.", PALE, ROSE, SMALL),
    p("Ключевые факты: район Ružinov; 48 m²; третий этаж и лифт; меблирован; без балкона; общая известная сумма 770 € без интернета; залог 650 €; ограничения для курящих и животных.", SMALL),
    box("<b>Важно:</b> <i>nájom</i> может обозначать арендную плату, а <i>energie</i> - коммунальные расходы. Всегда уточняйте, что именно включено в итоговую сумму.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    PageBreak(),

    p("2. Genitív в объявлениях и ценах", H1),
    p("В объявлениях Genitív часто появляется после предлогов и слов количества. Полезнее узнавать готовые модели, чем переводить каждую форму отдельно."),
    table([
        ["Модель", "Пример", "Перевод"],
        ["bez + G", "byt bez balkóna", "квартира без балкона"],
        ["v blízkosti + G", "v blízkosti centra", "вблизи центра"],
        ["do + G", "do desiatich minút", "до десяти минут"],
        ["od + G", "voľný od prvého októbra", "свободен с первого октября"],
        ["vo výške + G", "depozit vo výške nájmu", "залог в размере аренды"],
        ["vrátane + G", "cena vrátane energií", "цена, включая коммунальные платежи"],
    ], [42 * mm, 68 * mm, 60 * mm], 5.65),
    p("Что входит в цену", H2),
    table([
        ["Фраза", "Смысл"],
        ["Energie sú v cene.", "Коммунальные платежи включены."],
        ["Cena je bez energií.", "Цена указана без коммунальных платежей."],
        ["Internet je zahrnutý v cene.", "Интернет включён в цену."],
        ["Províziu neplatíte.", "Комиссию вы не платите."],
        ["Platí sa nájom a depozit.", "Оплачиваются аренда и залог."],
    ], [79 * mm, 91 * mm], 6.0),
    box("<b>Проверка полной суммы:</b> <i>nájom 650 € + energie 120 € = spolu 770 € mesačne</i>. Отдельно уточните интернет, парковку, депозит и комиссию агентству.", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    PageBreak(),

    p("3. Сравнение и вежливые вопросы", H1),
    p("Сравнивайте только сопоставимые параметры. <b>lacnejší/drahší</b> описывают цену, <b>väčší/menší</b> - размер, <b>bližšie/ďalej</b> - расстояние, <b>lepšie/horšie</b> - общую оценку."),
    table([
        ["Критерий", "Сравнение", "Перевод"],
        ["цена", "Byt A je lacnejší ako byt B.", "Квартира A дешевле квартиры B."],
        ["площадь", "Byt B je väčší o 12 m².", "Квартира B больше на 12 м²."],
        ["транспорт", "Byt A je bližšie k zastávke.", "Квартира A ближе к остановке."],
        ["условия", "V byte B sú energie zahrnuté.", "В квартире B коммунальные включены."],
        ["выбор", "Byt A mi vyhovuje viac.", "Квартира A подходит мне больше."],
    ], [30 * mm, 73 * mm, 67 * mm], 5.75),
    p("Вежливые вопросы владельцу", H2),
    table([
        ["Прямо", "Вежливо и естественно"],
        ["Je byt voľný?", "Chcel/a by som sa opýtať, či je byt ešte voľný."],
        ["Sú energie v cene?", "Sú, prosím, energie zahrnuté v cene?"],
        ["Koľko je depozit?", "Aká je, prosím, výška depozitu?"],
        ["Kedy môžem prísť?", "Kedy by bolo možné prísť na obhliadku?"],
    ], [55 * mm, 115 * mm], 5.8),
    p("Короткое сообщение", H2),
    box("<b>Dobrý deň, mám záujem o váš 2-izbový byt v Ružinove.</b> Chcel by som sa opýtať, či je ešte voľný a či sú energie zahrnuté v uvedenej cene. Je možné bývať v byte s mačkou? Kedy by bolo možné prísť na obhliadku? Ďakujem za odpoveď. S pozdravom, Ari Frost", PALE, ROSE, SMALL),
    PageBreak(),

    p("4. Два варианта: читаем и выбираем", H1),
    table([
        ["Параметр", "Byt A", "Byt B"],
        ["место", "Nové Mesto, pri električke", "Petržalka, pri jazere"],
        ["площадь", "42 m²", "54 m²"],
        ["аренда", "620 €", "690 €"],
        ["энергия", "130 €, internet v cene", "energie v cene, bez internetu"],
        ["условия", "zariadený, bez balkóna", "čiastočne zariadený, balkón"],
        ["срок", "voľný ihneď", "voľný od novembra"],
    ], [32 * mm, 69 * mm, 69 * mm], 5.7),
    p("Сравнение полными фразами", H2),
    table([
        ["SK", "RU"],
        ["Byt A je menší, ale je bližšie k centru.", "Квартира A меньше, но ближе к центру."],
        ["Byt B je väčší a má balkón.", "Квартира B больше, и у неё есть балкон."],
        ["Mesačné náklady na byt A sú 750 €.", "Ежемесячные расходы на A составляют 750 евро."],
        ["Pri byte B nepoznáme cenu internetu.", "Для B мы не знаем стоимость интернета."],
        ["Byt A je vhodnejší pre človeka bez auta.", "A больше подходит человеку без машины."],
        ["Byt B mi vyhovuje viac, lebo potrebujem viac miesta.", "B подходит мне больше, потому что мне нужно больше места."],
    ], [88 * mm, 82 * mm], 5.55),
    p("Решение", H2),
    box("<b>Vybral/a by som si byt A.</b> Je síce menší a nemá balkón, ale je lacnejší a bližšie k centru. Poznám aj celkové mesačné náklady. Pred obhliadkou by som sa opýtal/a na depozit, možnosť parkovania a minimálnu dĺžku nájmu.", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    p("Хороший выбор опирается на факты и личный приоритет. Другой вариант тоже может быть правильным, если объяснение логично.", SMALL),
    PageBreak(),

    p("5. Частые ошибки и упражнения", H1),
    box("<b>Частые ошибки:</b> считают только <i>nájom</i>, забывая <i>energie</i>; путают <i>depozit</i> с комиссией; переводят <i>bez</i> без Genitív; сравнивают варианты без общего критерия; пишут владельцу слишком прямо.", CREAM, colors.HexColor("#E7C76C"), TINY),
    p("Упражнение 1. Найдите факты в образце объявления", H2),
    p("Укажите: район, площадь, полную известную месячную сумму, дату доступности, размер залога и два ограничения.", TINY),
    p("Упражнение 2. Поставьте слово в Genitív", H2),
    p("1) bez ___ (balkón); 2) v blízkosti ___ (centrum); 3) vrátane ___ (energie); 4) od prvého ___ (november).", TINY),
    p("Упражнение 3. Образуйте сравнение", H2),
    p("1) byt A / lacný / byt B; 2) byt B / veľký / byt A; 3) byt A / blízko k centru; 4) byt B / vhodný pre rodinu.", TINY),
    p("Упражнение 4. Сделайте вопросы вежливыми", H2),
    p("1) Je byt voľný? 2) Sú energie v cene? 3) Koľko je depozit? 4) Kedy môžem prísť?", TINY),
    p("Упражнение 5. Передайте по-словацки", H2),
    p("Вариант A меньше и дешевле. Интернет включён, но квартира без балкона. Уточните, можно ли жить с кошкой и когда возможен просмотр.", TINY),
    p("Упражнение 6. Напишите владельцу", H2),
    p("Напишите сообщение из 5-7 предложений: приветствие, интерес к конкретному жилью, три вопроса, просьба о просмотре и вежливое завершение.", TINY),
    PageBreak(),

    p("6. Ответы и проверка мастерства", H1),
    p("Ответы", H2),
    p("<b>1.</b> Ružinov; 48 m²; 770 € без интернета; свободен с 1 октября; депозит 650 €; жильё для некурящих и без домашних животных.", TINY),
    p("<b>2.</b> 1) bez balkóna; 2) v blízkosti centra; 3) vrátane energií; 4) od prvého novembra.", TINY),
    p("<b>3.</b> 1) Byt A je lacnejší ako byt B. 2) Byt B je väčší ako byt A. 3) Byt A je bližšie k centru. 4) Byt B je vhodnejší pre rodinu.", TINY),
    p("<b>4.</b> Chcel/a by som sa opýtať, či je byt ešte voľný. Sú, prosím, energie zahrnuté v cene? Aká je, prosím, výška depozitu? Kedy by bolo možné prísť na obhliadku?", TINY),
    p("<b>5.</b> Byt A je menší a lacnejší. Internet je zahrnutý v cene, ale byt je bez balkóna. Je, prosím, možné bývať v byte s mačkou? Kedy by bolo možné prísť na obhliadku?", TINY),
    p("<b>6. Модель:</b> Dobrý deň, mám záujem o váš byt v Novom Meste. Chcel/a by som sa opýtať, či je ešte voľný. Sú energie a internet zahrnuté v cene? Aká je výška depozitu? Kedy by bolo možné prísť na obhliadku? Ďakujem za odpoveď. S pozdravom, Ari Frost. Возможны другие вежливые варианты.", TINY),
    p("Итог в четырёх пунктах", H2),
    table([
        ["OK", "Нахожу площадь, цену, дополнительные платежи и условия."],
        ["OK", "Узнаю типичные модели Genitív в объявлении."],
        ["OK", "Сравниваю варианты по одинаковым критериям."],
        ["OK", "Задаю владельцу точные и вежливые вопросы."],
    ], [12 * mm, 158 * mm], 6.2, False),
    Spacer(1, 2 * mm),
    box("<b>Финальная проверка:</b> за 90 секунд объясните, какой из двух вариантов вы выбираете, назовите полную цену и три условия, которые обязательно уточните до просмотра.", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    p("Следующий шаг", H2),
    p("В теме 6.3 вы научитесь сообщать о бытовой проблеме и договариваться о решении.", SMALL),
]

doc.build(story)
print(OUTPUT)
