from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output/pdf/A2/Module_06/Slovak_A2_Tema_6_1_Zhile_i_rayon.pdf"
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
BODY = ParagraphStyle(
    "Body", fontName="Arial", fontSize=8.65, leading=11.3,
    textColor=INK, spaceAfter=2.7 * mm,
)
SMALL = ParagraphStyle(
    "Small", parent=BODY, fontSize=7.45, leading=9.2, spaceAfter=1.4 * mm,
)
TINY = ParagraphStyle(
    "Tiny", parent=BODY, fontSize=6.65, leading=8.1, spaceAfter=0.9 * mm,
)
TITLE = ParagraphStyle(
    "Title", fontName="Arial-Bold", fontSize=20, leading=24,
    textColor=colors.white, alignment=TA_LEFT, spaceAfter=5 * mm,
)
SUBTITLE = ParagraphStyle(
    "Subtitle", fontName="Arial", fontSize=11.5, leading=15,
    textColor=colors.HexColor("#FFD8EB"), spaceAfter=5 * mm,
)
H1 = ParagraphStyle(
    "H1", fontName="Arial-Bold", fontSize=15.5, leading=18.5,
    textColor=PLUM, spaceBefore=1 * mm, spaceAfter=3 * mm,
)
H2 = ParagraphStyle(
    "H2", fontName="Arial-Bold", fontSize=10.7, leading=13.2,
    textColor=PINK, spaceBefore=1.1 * mm, spaceAfter=1.4 * mm,
)
KICK = ParagraphStyle(
    "Kicker", fontName="Arial-Bold", fontSize=10, leading=12,
    textColor=colors.HexColor("#FFD8EB"), spaceAfter=4 * mm,
)


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
        cell_style = ParagraphStyle(
            f"cell_{row_index}_{size}_{len(data)}",
            parent=SMALL,
            fontSize=size,
            leading=size + 1.75,
            textColor=colors.white if header and row_index == 0 else INK,
            fontName="Arial-Bold" if header and row_index == 0 else "Arial",
            spaceAfter=0,
        )
        rows.append([p(str(value), cell_style) for value in row])
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
        canvas.drawString(20 * mm, height - 12 * mm, "A2 6.1  |  Жильё и район")
    canvas.setFont("Arial", 8)
    canvas.setFillColor(MUTED)
    canvas.drawString(20 * mm, 9 * mm, "SlovoKrok | личный учебный модуль")
    canvas.drawRightString(width - 20 * mm, 9 * mm, f"стр. {page_number} / 7")
    canvas.restoreState()


doc = BaseDocTemplate(
    str(OUTPUT),
    pagesize=A4,
    leftMargin=20 * mm,
    rightMargin=20 * mm,
    topMargin=20 * mm,
    bottomMargin=18 * mm,
    title="Slovak A2 - Тема 6.1 - Жильё и район",
    author="SlovoKrok",
)
doc.addPageTemplates([
    PageTemplate(
        id="series",
        frames=[Frame(20 * mm, 18 * mm, 170 * mm, 257 * mm, id="main", leftPadding=0, rightPadding=0)],
        onPage=draw_page,
    )
])


story = [
    p("МОДУЛЬ 6  •  ДОМ, ИНТЕРНЕТ И ПОКУПКИ", KICK),
    p("Жильё и район", TITLE),
    p("Bývanie a okolie: описываем пространство, удобства и личные предпочтения", SUBTITLE),
    Spacer(1, 41 * mm),
    p("На уровне A2 важно не просто назвать <i>byt</i> или <i>dom</i>, а связно объяснить, где вы живёте, что есть внутри, каким является район и почему такой вариант вам подходит."),
    p("После модуля вы сможете:", H2),
    table([
        ["1", "назвать комнаты, мебель и бытовую технику"],
        ["2", "описать место с v/na + Lokál"],
        ["3", "различать bývať и žiť в типичных ситуациях"],
        ["4", "дать связный устный или письменный профиль жилья"],
    ], [12 * mm, 158 * mm], 7.2, False),
    Spacer(1, 3 * mm),
    box("<b>Формула профиля:</b> где живу + какое жильё + что в нём есть + что есть рядом + что мне нравится и что я предпочитаю."),
    PageBreak(),

    p("1. Пространство: от жилья к комнате", H1),
    p("Начинайте с общего и постепенно добавляйте детали. Так описание звучит как связный профиль, а не как список отдельных слов."),
    table([
        ["Уровень", "Полезные слова", "Готовый пример"],
        ["жильё", "byt, dom, garsónka", "Bývam v dvojizbovom byte."],
        ["части дома", "balkón, pivnica, výťah", "V dome je nový výťah."],
        ["комнаты", "obývačka, spálňa, kuchyňa", "Byt má svetlú obývačku."],
        ["удобства", "kúpeľňa, toaleta, chodba", "Kúpeľňa je vedľa spálne."],
    ], [29 * mm, 58 * mm, 83 * mm], 6.1),
    p("V или na + Lokál", H2),
    table([
        ["Модель", "Пример", "Перевод"],
        ["v + помещение/город", "Bývam v byte v centre.", "Я живу в квартире в центре."],
        ["v + комната", "V kuchyni máme stôl.", "На кухне у нас есть стол."],
        ["na + поверхность", "Na stole je lampa.", "На столе стоит лампа."],
        ["na + типичное место", "Na sídlisku je park.", "В жилом районе есть парк."],
        ["na + этаж", "Bývame na treťom poschodí.", "Мы живём на третьем этаже."],
    ], [38 * mm, 67 * mm, 65 * mm], 5.8),
    box("<b>Русскоязычная ловушка:</b> выбор предлога нельзя всегда переводить буквально. Учите готовые сочетания: <b>v centre</b>, <b>na sídlisku</b>, <b>na poschodí</b>, <b>v izbe</b>, <b>na stole</b>.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    PageBreak(),

    p("2. Мебель, техника и расположение", H1),
    p("Чтобы описание стало точным, соединяйте предмет с комнатой и функцией: где он находится и для чего вы его используете."),
    table([
        ["Комната", "Мебель и техника", "Естественная фраза"],
        ["obývačka", "pohovka, kreslo, televízor", "V obývačke je pohovka a televízor."],
        ["spálňa", "posteľ, skriňa, nočný stolík", "Vedľa postele stojí nočný stolík."],
        ["kuchyňa", "chladnička, sporák, umývačka", "V kuchyni máme novú umývačku."],
        ["pracovňa", "písací stôl, stolička, počítač", "Na stole mám počítač."],
        ["kúpeľňa", "práčka, sprcha, vaňa", "Práčka je v kúpeľni."],
    ], [30 * mm, 64 * mm, 76 * mm], 5.7),
    p("Где именно?", H2),
    table([
        ["Связка", "Пример", "Перевод"],
        ["vedľa + G", "Skrinka je vedľa okna.", "Шкафчик стоит рядом с окном."],
        ["oproti + D", "Pohovka je oproti televízoru.", "Диван стоит напротив телевизора."],
        ["medzi + I", "Stôl je medzi oknom a dverami.", "Стол находится между окном и дверью."],
        ["pri + L", "Pri dome je malé ihrisko.", "Возле дома есть небольшая площадка."],
    ], [31 * mm, 71 * mm, 68 * mm], 5.9),
    box("<b>A2-шаг:</b> добавляйте причину или функцию: <i>V pracovni mám veľký stôl, pretože často pracujem z domu.</i> - В кабинете у меня большой стол, потому что я часто работаю из дома.", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    PageBreak(),

    p("3. Bývať, žiť и личные предпочтения", H1),
    p("<b>Bývať</b> обычно описывает место и тип проживания. <b>Žiť</b> шире: жить, вести жизнь, существовать в определённой среде. Иногда оба глагола возможны, но смысловой фокус различается."),
    table([
        ["Фокус", "Пример", "Перевод"],
        ["адрес/жильё", "Bývam v prenajatom byte.", "Я живу в арендованной квартире."],
        ["с кем живу", "Bývam s kamarátkou.", "Я живу с подругой."],
        ["образ жизни", "Chcem žiť pokojnejšie.", "Я хочу жить спокойнее."],
        ["страна/город как среда", "Žije sa mi tu dobre.", "Мне здесь хорошо живётся."],
    ], [35 * mm, 67 * mm, 68 * mm], 6.0),
    p("Сравниваем и объясняем выбор", H2),
    table([
        ["Модель", "Пример"],
        ["radšej + глагол", "Radšej bývam bližšie k centru."],
        ["X je ... ako Y", "Náš byt je tichší ako starý byt."],
        ["pre mňa je dôležité", "Pre mňa je dôležité dobré spojenie."],
        ["páči sa mi / nepáči sa mi", "Páči sa mi zeleň, ale nepáči sa mi hluk."],
    ], [54 * mm, 116 * mm], 6.15),
    p("Мини-диалог", H2),
    box("<b>Eva:</b> Kde teraz bývaš?<br/><b>Marek:</b> Bývam na sídlisku neďaleko centra.<br/><b>Eva:</b> Páči sa ti tam?<br/><b>Marek:</b> Áno. Byt je menší, ale je svetlý a pokojný. Pri dome je park a zastávka.<br/><b>Eva:</b> Chcel by si bývať inde?<br/><b>Marek:</b> Radšej by som býval bližšie k práci, ale v tejto štvrti sa mi žije dobre.", PALE, ROSE, SMALL),
    p("Перевод: Где ты сейчас живёшь? - В жилом районе недалеко от центра. Тебе там нравится? - Да. Квартира меньше, но светлая и тихая. Возле дома парк и остановка. Ты хотел бы жить в другом месте? - Я предпочёл бы жить ближе к работе, но в этом районе мне хорошо живётся.", TINY),
    PageBreak(),

    p("4. Банк фраз и связный профиль", H1),
    table([
        ["SK", "RU"],
        ["Bývam v pokojnej štvrti.", "Я живу в тихом районе."],
        ["Náš byt je na druhom poschodí.", "Наша квартира на втором этаже."],
        ["Máme dve izby a veľkú kuchyňu.", "У нас две комнаты и большая кухня."],
        ["Obývačka je svetlá a útulná.", "Гостиная светлая и уютная."],
        ["Z balkóna vidím park.", "С балкона я вижу парк."],
        ["V spálni nie je veľa nábytku.", "В спальне немного мебели."],
        ["Chladnička stojí vedľa sporáka.", "Холодильник стоит рядом с плитой."],
        ["Na chodbe máme veľkú skriňu.", "В прихожей у нас большой шкаф."],
        ["Pri dome je zastávka autobusu.", "Возле дома есть автобусная остановка."],
        ["Do centra sa dostanem za desať minút.", "До центра я добираюсь за десять минут."],
        ["V okolí sú obchody a lekáreň.", "Поблизости есть магазины и аптека."],
        ["Chýba mi tu športové centrum.", "Мне здесь не хватает спортивного центра."],
    ], [87 * mm, 83 * mm], 5.55),
    p("Модель письменного профиля", H2),
    box("<b>Bývam v dvojizbovom byte v pokojnej štvrti neďaleko centra.</b> Byt je na druhom poschodí a má obývačku, spálňu, kuchyňu a malý balkón. V obývačke máme pohovku, knižnicu a televízor. Najviac sa mi páči kuchyňa, pretože je svetlá a priestranná. Pri dome je park, zastávka a niekoľko obchodov. Do práce sa dostanem rýchlo električkou. Byt je menší ako môj starý byt, ale táto štvrť je tichšia. Radšej bývam tu, lebo mám všetko blízko.", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    p("Маршрут текста: 1) место; 2) тип и состав жилья; 3) детали внутри; 4) район и транспорт; 5) сравнение; 6) личный вывод.", SMALL),
    PageBreak(),

    p("5. Частые ошибки и упражнения", H1),
    box("<b>Частые ошибки:</b> *v sídlisku* вместо <b>na sídlisku</b>; *na centre* вместо <b>v centre</b>; <b>žiť</b> там, где нужен конкретный адрес; список слов без связок; неверный падеж после <b>v/na</b> при ответе на вопрос <i>kde?</i>.", CREAM, colors.HexColor("#E7C76C"), TINY),
    p("Упражнение 1. Выберите v или na", H2),
    p("1) ___ centre; 2) ___ sídlisku; 3) ___ kuchyni; 4) ___ treťom poschodí; 5) ___ stole.", TINY),
    p("Упражнение 2. Соедините предмет и место", H2),
    p("1) chladnička; 2) posteľ; 3) pohovka; 4) práčka. Места: a) v kúpeľni; b) v spálni; c) v kuchyni; d) v obývačke.", TINY),
    p("Упражнение 3. Вставьте bývať или žiť в нужной форме", H2),
    p("1) Teraz ___ v malom byte. 2) Chcem ___ pokojnejšie. 3) S kým ___? 4) V tejto štvrti sa mi ___ dobre.", TINY),
    p("Упражнение 4. Исправьте ошибки", H2),
    p("1) Bývam v sídlisku. 2) Na kuchyni je nový stôl. 3) Žijem na treťom poschodí s bratom. 4) V stole je lampa.", TINY),
    p("Упражнение 5. Переведите", H2),
    p("1) Мы живём в тихом районе. 2) В гостиной есть диван и телевизор. 3) Возле дома есть парк. 4) Я предпочитаю жить ближе к центру.", TINY),
    p("Упражнение 6. Ваш профиль", H2),
    p("Напишите 6-8 предложений о реальном или желаемом жилье. Укажите комнаты, два предмета, два места в районе, одно сравнение и личное предпочтение. Затем расскажите тот же профиль вслух без чтения.", TINY),
    PageBreak(),

    p("6. Ответы и проверка мастерства", H1),
    p("Ответы", H2),
    p("<b>1.</b> 1) v centre; 2) na sídlisku; 3) v kuchyni; 4) na treťom poschodí; 5) na stole.", TINY),
    p("<b>2.</b> 1-c: chladnička v kuchyni; 2-b: posteľ v spálni; 3-d: pohovka v obývačke; 4-a: práčka v kúpeľni.", TINY),
    p("<b>3.</b> 1) Teraz <b>bývam</b> v malom byte. 2) Chcem <b>žiť</b> pokojnejšie. 3) S kým <b>bývaš</b>? 4) V tejto štvrti sa mi <b>žije</b> dobre.", TINY),
    p("<b>4.</b> 1) Bývam <b>na sídlisku</b>. 2) <b>V kuchyni</b> je nový stôl. 3) <b>Bývam</b> na treťom poschodí s bratom. 4) <b>Na stole</b> je lampa.", TINY),
    p("<b>5.</b> Bývame v pokojnej štvrti. V obývačke je pohovka a televízor. Pri dome je park. Radšej bývam bližšie k centru.", TINY),
    p("<b>6. Модель:</b> Bývam v malom byte na okraji mesta. Máme obývačku, spálňu a kuchyňu. V obývačke je pohovka a pri okne stojí knižnica. V kuchyni máme chladničku a umývačku. Pri dome je obchod a zastávka. Byt je menší ako byt mojich rodičov, ale je tichší. Radšej bývam mimo centra, pretože mám blízko do prírody. Возможны другие естественные варианты.", TINY),
    p("Итог в четырёх пунктах", H2),
    table([
        ["OK", "Описываю жильё от общего к деталям."],
        ["OK", "Использую v/na + Lokál в ответе на kde?"],
        ["OK", "Различаю место проживания bývať и более широкое žiť."],
        ["OK", "Сравниваю варианты и объясняю своё предпочтение."],
    ], [12 * mm, 158 * mm], 6.25, False),
    Spacer(1, 2 * mm),
    box("<b>Финальная проверка:</b> за 60-90 секунд опишите жильё и район без списка слов. Назовите место, комнаты, обстановку, удобства рядом, сравнение и личный вывод.", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    p("Следующий шаг", H2),
    p("В теме 6.2 вы будете читать объявления, сравнивать условия и писать владельцу жилья.", SMALL),
]

doc.build(story)
print(OUTPUT)
