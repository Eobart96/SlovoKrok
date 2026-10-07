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
OUTPUT = ROOT / "output/pdf/A2/Module_06/Slovak_A2_Tema_6_7_Kolichestvo_upakovka_i_informatsiya_o_tovare.pdf"
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
BODY = ParagraphStyle("Body", fontName="Arial", fontSize=8.55, leading=11.2, textColor=INK, spaceAfter=2.5 * mm)
SMALL = ParagraphStyle("Small", parent=BODY, fontSize=7.35, leading=9.15, spaceAfter=1.35 * mm)
TINY = ParagraphStyle("Tiny", parent=BODY, fontSize=6.55, leading=7.95, spaceAfter=0.85 * mm)
TITLE = ParagraphStyle("Title", fontName="Arial-Bold", fontSize=20, leading=24, textColor=colors.white, alignment=TA_LEFT, spaceAfter=5 * mm)
SUBTITLE = ParagraphStyle("Subtitle", fontName="Arial", fontSize=11.4, leading=15, textColor=colors.HexColor("#FFD8EB"), spaceAfter=5 * mm)
H1 = ParagraphStyle("H1", fontName="Arial-Bold", fontSize=15.5, leading=18.5, textColor=PLUM, spaceBefore=1 * mm, spaceAfter=3 * mm)
H2 = ParagraphStyle("H2", fontName="Arial-Bold", fontSize=10.6, leading=13.1, textColor=PINK, spaceBefore=1 * mm, spaceAfter=1.35 * mm)
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
        canvas.drawString(20 * mm, height - 12 * mm, "A2 6.7  |  Количество, упаковка и информация о товаре")
    canvas.setFont("Arial", 8)
    canvas.setFillColor(MUTED)
    canvas.drawString(20 * mm, 9 * mm, "SlovoKrok | личный учебный модуль")
    canvas.drawRightString(width - 20 * mm, 9 * mm, f"стр. {page_number} / 7")
    canvas.restoreState()


doc = BaseDocTemplate(
    str(OUTPUT), pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm,
    topMargin=20 * mm, bottomMargin=18 * mm,
    title="Slovak A2 - Тема 6.7 - Количество, упаковка и информация о товаре",
    author="SlovoKrok",
)
doc.addPageTemplates([
    PageTemplate(id="series", frames=[Frame(20 * mm, 18 * mm, 170 * mm, 257 * mm, id="main", leftPadding=0, rightPadding=0)], onPage=draw_page)
])


story = [
    p("МОДУЛЬ 6  •  ДОМ, ИНТЕРНЕТ И ПОКУПКИ", KICK),
    p("Количество, упаковка<br/>и информация о товаре", TITLE),
    p("Množstvo, balenie a údaje o výrobku: просим нужное и читаем этикетку", SUBTITLE),
    Spacer(1, 41 * mm),
    p("В магазине нужно связать количество с правильной формой товара, уточнить цену и быстро найти на этикетке состав, происхождение, условия хранения и срок."),
    p("После модуля вы сможете:", H2),
    table([
        ["1", "попросить точный вес, объём или упаковку"],
        ["2", "использовать количественный родительный падеж"],
        ["3", "понять цену, материал и страну происхождения"],
        ["4", "найти состав, срок и инструкцию по хранению"],
    ], [12 * mm, 158 * mm], 7.2, False),
    Spacer(1, 3 * mm),
    box("<b>Формула покупки:</b> Prosím si + количество или упаковку + Genitív товара; затем уточнение о цене, составе или сроке."),
    PageBreak(),

    p("1. Мера или упаковка + Genitív", H1),
    p("После слова меры или упаковки название товара отвечает на вопрос <i>čoho?</i>. У вещества обычно Genitív singular, у считаемых предметов часто Genitív plural."),
    table([
        ["Модель", "Пример", "Перевод"],
        ["kilo + G", "kilo jabĺk", "килограмм яблок"],
        ["pol kila + G", "pol kila paradajok", "полкилограмма помидоров"],
        ["liter + G", "liter mlieka", "литр молока"],
        ["200 gramov + G", "dvesto gramov syra", "двести граммов сыра"],
        ["fľaša + G", "fľaša minerálnej vody", "бутылка минеральной воды"],
        ["balenie + G", "balenie ryže", "упаковка риса"],
        ["téglik + G", "téglik bieleho jogurtu", "стаканчик белого йогурта"],
    ], [36 * mm, 69 * mm, 65 * mm], 5.65),
    p("Неопределённое количество", H2),
    table([
        ["Слово", "Пример", "Перевод"],
        ["veľa", "veľa cukru", "много сахара"],
        ["málo", "málo soli", "мало соли"],
        ["trochu", "trochu oleja", "немного масла"],
        ["dosť", "dosť vody", "достаточно воды"],
        ["koľko", "Koľko syra chcete?", "Сколько сыра вы хотите?"],
    ], [27 * mm, 67 * mm, 76 * mm], 5.8),
    box("<b>Не путайте:</b> <i>mlieko</i> - молоко, но <i>liter mlieka</i>; <i>jablká</i> - яблоки, но <i>kilo jabĺk</i>.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    PageBreak(),

    p("2. Два, три, четыре или пять и больше", H1),
    p("С числами 2-4 у считаемых предметов обычно форма множественного числа. Начиная с 5, нужна форма Genitív plural. Эта граница особенно заметна у упаковок."),
    table([
        ["2-4", "5 и больше", "Перевод"],
        ["dve fľaše vody", "päť fliaš vody", "две / пять бутылок воды"],
        ["tri balenia cestovín", "šesť balení cestovín", "три / шесть упаковок макарон"],
        ["štyri kusy", "desať kusov", "четыре / десять штук"],
        ["dve plechovky", "osem plechoviek", "две / восемь банок"],
        ["tri kilogramy", "sedem kilogramov", "три / семь килограммов"],
    ], [56 * mm, 59 * mm, 55 * mm], 5.65),
    p("Как попросить товар", H2),
    table([
        ["Ситуация", "Фраза"],
        ["точный вес", "Prosím si dvesto gramov šunky."],
        ["одну упаковку", "Dajte mi, prosím, jedno balenie ryže."],
        ["меньший размер", "Máte aj menšie balenie?"],
        ["продажа поштучно", "Predáva sa to aj po kusoch?"],
        ["цена за единицу", "Koľko stojí kilogram?"],
        ["проверка количества", "Stačia vám dve fľaše?"],
    ], [50 * mm, 120 * mm], 5.75),
    box("<b>Вежливо:</b> <i>Prosím si...</i> естественно при покупке. <i>Dajte mi...</i> тоже возможно, но добавьте <i>prosím</i>.", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    PageBreak(),

    p("3. Что искать на этикетке", H1),
    p("На упаковке сначала найдите название и чистое количество, затем состав и аллергены, происхождение, срок, хранение и короткую инструкцию."),
    table([
        ["Поле", "По-словацки", "Пример"],
        ["чистое количество", "čisté množstvo", "Čisté množstvo: 500 g"],
        ["состав", "zloženie", "Zloženie: ovos, sušené ovocie, soľ"],
        ["аллергены", "alergény", "Môže obsahovať orechy."],
        ["происхождение", "krajina pôvodu", "Krajina pôvodu: Slovensko"],
        ["хранение", "skladovanie", "Skladujte na suchom mieste."],
        ["после открытия", "po otvorení", "Po otvorení uchovávajte v chladničke."],
        ["инструкция", "návod na použitie", "Pred použitím pretrepte."],
    ], [39 * mm, 48 * mm, 83 * mm], 5.55),
    p("Состав читается по порядку", H2),
    box("В списке <i>zloženie</i> компоненты указаны от большей доли к меньшей. Аллергены обычно выделены. Если есть ограничение, уточните: <i>Obsahuje výrobok mlieko alebo orechy?</i>", PALE, ROSE, SMALL),
    p("Материал и происхождение", H2),
    table([
        ["Значение", "Фраза", "Перевод"],
        ["материал", "Obal je z papiera.", "Упаковка из бумаги."],
        ["материал", "Fľaša je zo skla.", "Бутылка из стекла."],
        ["сырьё", "Vyrobené z kravského mlieka.", "Сделано из коровьего молока."],
        ["место изготовления", "Vyrobené na Slovensku.", "Сделано в Словакии."],
        ["страна", "Krajina pôvodu: Taliansko.", "Страна происхождения: Италия."],
    ], [32 * mm, 72 * mm, 66 * mm], 5.55),
    PageBreak(),

    p("4. Цена, срок и короткая инструкция", H1),
    p("Цена может быть указана за штуку, упаковку, 100 г или килограмм. Сравнивайте <i>jednotková cena</i>, если упаковки разного размера."),
    table([
        ["Этикетка", "Значение"],
        ["2,49 € za balenie", "2,49 евро за упаковку"],
        ["0,89 € za 100 g", "0,89 евро за 100 граммов"],
        ["jednotková cena 8,90 €/kg", "цена за единицу: 8,90 евро за кг"],
        ["akciová cena", "акционная цена"],
        ["vratný obal 0,15 €", "возвратная тара: 0,15 евро"],
    ], [75 * mm, 95 * mm], 5.8),
    p("Две разные даты", H2),
    table([
        ["Формулировка", "Что означает", "Как действовать"],
        ["spotrebujte do", "срок употребления; связан с безопасностью скоропортящегося продукта", "после даты продукт не употреблять"],
        ["minimálna trvanlivosť do", "минимальный срок сохранения качества", "проверить хранение, упаковку и инструкцию"],
    ], [45 * mm, 72 * mm, 53 * mm], 5.55),
    box("<b>Примеры:</b> <i>Spotrebujte do 15. 10. 2026.</i> - употребить до 15 октября. <i>Minimálna trvanlivosť do konca 12/2027.</i> - минимальный срок до конца декабря 2027 года.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    p("Короткие инструкции", H2),
    table([
        ["SK", "RU"],
        ["Pred použitím pretrepte.", "Перед употреблением встряхните."],
        ["Po otvorení spotrebujte do troch dní.", "После открытия употребите в течение трёх дней."],
        ["Uchovávajte pri teplote do 8 °C.", "Храните при температуре до 8 °C."],
    ], [88 * mm, 82 * mm], 5.65),
    PageBreak(),

    p("5. Модель покупки и упражнения", H1),
    p("Мини-диалог", H2),
    box("<b>A:</b> Prosím si dvesto gramov tohto syra.<br/><b>B:</b> Nech sa páči. Chcete ešte niečo?<br/><b>A:</b> Áno, jedno balenie ryže. Koľko stojí?<br/><b>B:</b> Balenie stojí 2,49 eura. Jednotková cena je 4,98 eura za kilogram.<br/><b>A:</b> Obsahuje táto ryža nejaké alergény?<br/><b>B:</b> Podľa etikety môže obsahovať stopy orechov.<br/><b>A:</b> Dobre, vezmem si ju.", PALE, ROSE, TINY),
    p("Упражнение 1. Поставьте товар в Genitív", H2),
    p("1) kilo (jablká); 2) liter (mlieko); 3) balenie (ryža); 4) dvesto gramov (syr); 5) veľa (cukor).", TINY),
    p("Упражнение 2. Выберите форму после числа", H2),
    p("1) dve fľaše/fliaš; 2) päť fľaše/fliaš; 3) tri balenia/balení; 4) šesť balenia/balení; 5) desať kusy/kusov.", TINY),
    p("Упражнение 3. Найдите поле этикетки", H2),
    p("Соедините: 1) zloženie; 2) čisté množstvo; 3) krajina pôvodu; 4) skladovanie. Данные: a) 500 g; b) Slovensko; c) ovos, cukor, soľ; d) na suchom mieste.", TINY),
    p("Упражнение 4. Выберите срок", H2),
    p("1) Для скоропортящегося продукта: spotrebujte do / minimálna trvanlivosť do. 2) Для качества сухой крупы: spotrebujte do / minimálna trvanlivosť do.", TINY),
    p("Упражнение 5. Переведите просьбы", H2),
    p("1) Дайте, пожалуйста, полкилограмма помидоров. 2) Сколько стоит килограмм? 3) У вас есть упаковка поменьше? 4) Продаётся ли это поштучно?", TINY),
    p("Упражнение 6. Прочитайте и объясните этикетку", H2),
    p("OVSENÁ KAŠA. Čisté množstvo: 500 g. Zloženie: ovos, sušené jablká, škorica. Môže obsahovať orechy. Krajina pôvodu: Slovensko. Minimálna trvanlivosť do: 31. 12. 2027. Skladujte na suchom mieste. Объясните 5 фактов покупателю.", TINY),
    PageBreak(),

    p("6. Ответы и итоговая проверка", H1),
    p("Ответы", H2),
    p("<b>1.</b> 1) kilo jabĺk; 2) liter mlieka; 3) balenie ryže; 4) dvesto gramov syra; 5) veľa cukru.", TINY),
    p("<b>2.</b> 1) dve fľaše; 2) päť fliaš; 3) tri balenia; 4) šesť balení; 5) desať kusov.", TINY),
    p("<b>3.</b> 1-c; 2-a; 3-b; 4-d.", TINY),
    p("<b>4.</b> 1) spotrebujte do; 2) minimálna trvanlivosť do.", TINY),
    p("<b>5.</b> 1) Dajte mi, prosím, pol kila paradajok. 2) Koľko stojí kilogram? 3) Máte aj menšie balenie? 4) Predáva sa to aj po kusoch?", TINY),
    p("<b>6. Модель:</b> Je to ovsená kaša v 500-gramovom balení. Obsahuje ovos, sušené jablká a škoricu. Môže obsahovať orechy. Pochádza zo Slovenska. Minimálna trvanlivosť je do 31. decembra 2027. Výrobok treba skladovať na suchom mieste. Возможны другие естественные формулировки.", TINY),
    p("Итог в четырёх пунктах", H2),
    table([
        ["OK", "После меры или упаковки ставлю Genitív."],
        ["OK", "Различаю 2-4 и 5+ у считаемых предметов."],
        ["OK", "Нахожу цену, состав, происхождение и хранение."],
        ["OK", "Различаю spotrebujte do и minimálna trvanlivosť do."],
    ], [12 * mm, 158 * mm], 6.0, False),
    p("Следующий шаг: в теме 6.8 вы будете выбирать одежду, просить размер, оплачивать и объяснять необходимость обмена.", SMALL),
]

doc.build(story)
print(OUTPUT)
