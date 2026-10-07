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
OUTPUT = ROOT / "output/pdf/A2/Module_07/Slovak_A2_Tema_7_7_Geografiya_regiony_i_pogoda_Slovakii.pdf"
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
TITLE = ParagraphStyle("Title", fontName="Arial-Bold", fontSize=20, leading=23, textColor=colors.white, alignment=TA_LEFT, spaceAfter=4 * mm)
SUBTITLE = ParagraphStyle("Subtitle", fontName="Arial", fontSize=11.2, leading=14.5, textColor=colors.HexColor("#FFD8EB"), spaceAfter=5 * mm)
H1 = ParagraphStyle("H1", fontName="Arial-Bold", fontSize=15.5, leading=18.5, textColor=PLUM, spaceBefore=1 * mm, spaceAfter=3 * mm)
H2 = ParagraphStyle("H2", fontName="Arial-Bold", fontSize=10.7, leading=13.2, textColor=PINK, spaceBefore=1.1 * mm, spaceAfter=1.4 * mm)
KICK = ParagraphStyle("Kicker", fontName="Arial-Bold", fontSize=10, leading=12, textColor=colors.HexColor("#FFD8EB"), spaceAfter=4 * mm)


def p(text, style=BODY):
    return Paragraph(text, style)


def box(text, bg=PALE, border=ROSE, style=BODY, pad=7):
    item = Table([[p(text, style)]], colWidths=[170 * mm])
    item.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg), ("BOX", (0, 0), (-1, -1), 0.7, border),
        ("LEFTPADDING", (0, 0), (-1, -1), pad), ("RIGHTPADDING", (0, 0), (-1, -1), pad),
        ("TOPPADDING", (0, 0), (-1, -1), pad), ("BOTTOMPADDING", (0, 0), (-1, -1), pad),
    ]))
    return item


def table(data, widths, size=7.0, header=True):
    rows = []
    for row_index, row in enumerate(data):
        cell_style = ParagraphStyle(
            f"cell_{row_index}_{size}_{len(data)}", parent=SMALL, fontSize=size, leading=size + 1.75,
            textColor=colors.white if header and row_index == 0 else INK,
            fontName="Arial-Bold" if header and row_index == 0 else "Arial", spaceAfter=0,
        )
        rows.append([p(str(value), cell_style) for value in row])
    item = Table(rows, colWidths=widths, repeatRows=1 if header else 0)
    commands = [
        ("GRID", (0, 0), (-1, -1), 0.45, ROSE), ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
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
        canvas.drawString(20 * mm, height - 12 * mm, "A2 7.7  |  География, регионы и погода Словакии")
    canvas.setFont("Arial", 8)
    canvas.setFillColor(MUTED)
    canvas.drawString(20 * mm, 9 * mm, "SlovoKrok | личный учебный модуль")
    canvas.drawRightString(width - 20 * mm, 9 * mm, f"стр. {page_number} / 7")
    canvas.restoreState()


doc = BaseDocTemplate(
    str(OUTPUT), pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=20 * mm, bottomMargin=18 * mm,
    title="Slovak A2 - Тема 7.7 - География, регионы и погода Словакии", author="SlovoKrok",
)
doc.addPageTemplates([PageTemplate(id="series", frames=[Frame(20 * mm, 18 * mm, 170 * mm, 257 * mm, id="main", leftPadding=0, rightPadding=0)], onPage=draw_page)])


story = [
    p("A2 7.7  •  МОДУЛЬ 7  •  РАБОТА, ПУТЕШЕСТВИЯ И СТРАНА", KICK),
    p("География, регионы и погода Словакии", TITLE),
    p("Geografia, regióny a počasie Slovenska: описываем страну и сравниваем", SUBTITLE),
    Spacer(1, 41 * mm),
    p("На уровне A2 важно связать факты в короткое описание: где находится страна или город, с чем граничит, какой там ландшафт и чем погода отличается от другого региона или вашей страны."),
    p("После модуля вы сможете:", H2),
    table([
        ["1", "описать положение Словакии и её городов"],
        ["2", "назвать восемь краёв и основные типы природы"],
        ["3", "использовать с + творительный после susediť"],
        ["4", "дать прогноз и сравнить погоду регионов"],
    ], [12 * mm, 158 * mm], 7.2, False),
    Spacer(1, 3 * mm),
    box("<b>Формула:</b> где находится → с чем граничит → что там есть → какая погода → чем отличается."),
    PageBreak(),

    p("1. Где находится и с чем граничит", H1),
    p("Для положения используйте <b>ležať</b> или <b>nachádzať sa</b>. Граница выражается через <b>susediť s + Instrumentál</b>, а происхождение — через <b>pochádzať z + Genitív</b>."),
    table([
        ["Модель", "Пример", "Перевод"],
        ["ležať v/na", "Slovensko leží v strednej Európe.", "Словакия находится в Центральной Европе."],
        ["nachádzať sa", "Bratislava sa nachádza na juhozápade krajiny.", "Братислава находится на юго-западе страны."],
        ["nachádzať sa", "Vysoké Tatry sa nachádzajú na severe.", "Высокие Татры находятся на севере."],
        ["susediť s + I", "Slovensko susedí s piatimi štátmi.", "Словакия граничит с пятью государствами."],
        ["pochádzať z + G", "Tento syr pochádza zo severného Slovenska.", "Этот сыр происходит из северной Словакии."],
        ["preteká cez + A", "Dunaj preteká cez Bratislavu.", "Дунай протекает через Братиславу."],
    ], [40 * mm, 78 * mm, 52 * mm], 5.35),
    p("Соседние страны: Instrumentál", H2),
    table([
        ["Страна", "Форма после s", "Пример"],
        ["Rakúsko", "s Rakúskom", "Bratislavský kraj susedí s Rakúskom."],
        ["Česko", "s Českom", "Slovensko susedí s Českom na západe."],
        ["Poľsko", "s Poľskom", "Na severe Slovensko susedí s Poľskom."],
        ["Ukrajina", "s Ukrajinou", "Na východe susedí s Ukrajinou."],
        ["Maďarsko", "s Maďarskom", "Na juhu susedí s Maďarskom."],
    ], [35 * mm, 43 * mm, 92 * mm], 5.45),
    box("<b>Не смешивайте:</b> <i>na východe</i> — на востоке, <i>z východu</i> — с востока, <i>na východ</i> — на восток. После <i>susedí s</i> нужна форма творительного падежа.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    PageBreak(),

    p("2. Восемь краёв и природа", H1),
    p("Словакия административно делится на восемь краёв. Для уровня A2 достаточно уверенно назвать край, его направление и один природный или городской ориентир."),
    table([
        ["Kraj", "Положение", "Короткое описание"],
        ["Bratislavský", "juhozápad", "Bratislava leží pri Dunaji."],
        ["Trnavský", "západ / juhozápad", "Na severe hraničí s Českom a na juhu s Maďarskom."],
        ["Trenčiansky", "západ", "Cez región preteká rieka Váh."],
        ["Nitriansky", "juhozápad", "Osou regiónu je rieka Nitra."],
        ["Žilinský", "severozápad", "Región je prevažne hornatý."],
        ["Banskobystrický", "stred", "Cez región preteká rieka Hron."],
        ["Prešovský", "severovýchod", "Na severe hraničí s Poľskom."],
        ["Košický", "juhovýchod", "Na východe hraničí s Ukrajinou."],
    ], [42 * mm, 45 * mm, 83 * mm], 5.05),
    p("Ландшафт", H2),
    table([
        ["SK", "RU", "Пример"],
        ["pohorie", "горный массив", "Tatry sú najznámejším slovenským pohorím."],
        ["nížina", "низменность", "Na juhu sa rozprestiera Podunajská nížina."],
        ["rieka", "река", "Váh je najdlhšia rieka na Slovensku."],
        ["les", "лес", "V horských oblastiach je veľa lesov."],
        ["jazero / pleso", "озеро / горное озеро", "V Tatrách sa nachádzajú horské plesá."],
        ["jaskyňa", "пещера", "Na Slovensku je veľa jaskýň."],
    ], [35 * mm, 45 * mm, 90 * mm], 5.35),
    box("<b>Общая картина:</b> <i>Stred a sever Slovenska sú hornaté, kým na juhu a východe sa nachádzajú nížiny.</i>", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    PageBreak(),

    p("3. Погода: безличные конструкции", H1),
    p("В прогнозе субъект часто не нужен. Используйте готовые безличные модели и указывайте место: <i>na severe, na juhu, v horách, pri Dunaji</i>."),
    table([
        ["Модель", "Пример", "Перевод"],
        ["je + наречие", "Dnes je slnečno a teplo.", "Сегодня солнечно и тепло."],
        ["je + наречие", "Ráno bude zamračené a hmlisto.", "Утром будет облачно и туманно."],
        ["глагол", "Na západe prší a fúka silný vietor.", "На западе идёт дождь и дует сильный ветер."],
        ["глагол", "V horách bude v noci snežiť.", "В горах ночью будет идти снег."],
        ["температура", "Teplota vystúpi na dvadsať stupňov.", "Температура поднимется до двадцати градусов."],
        ["температура", "Ráno teplota klesne pod nulu.", "Утром температура опустится ниже нуля."],
    ], [42 * mm, 75 * mm, 53 * mm], 5.35),
    p("Сравниваем наречия", H2),
    table([
        ["База", "Сравнительная", "Пример"],
        ["teplo", "teplejšie", "Na juhu je teplejšie ako na severe."],
        ["chladno", "chladnejšie", "V horách býva chladnejšie."],
        ["sucho", "suchšie", "V nížinách môže byť v lete suchšie."],
        ["často", "častejšie", "Vo vyšších polohách sneží častejšie."],
        ["veľa", "viac", "Na severe býva viac zrážok."],
    ], [35 * mm, 45 * mm, 90 * mm], 5.45),
    box("<b>Прогноз:</b> <i>Zajtra bude na západe slnečno. Na severe bude chladnejšie a v horách môže snežiť. Na juhu teplota vystúpi na osemnásť stupňov.</i>", PALE, ROSE, SMALL),
    PageBreak(),

    p("4. Описываем Словакию и сравниваем", H1),
    p("Короткое описание удобно строить из пяти частей: положение, соседи, природа, города и климат. Сравнение со своей страной добавляйте только по фактам, которые вы точно знаете."),
    p("Модель описания Словакии", H2),
    box("Slovensko leží v strednej Európe a susedí s Českom, Poľskom, Ukrajinou, Maďarskom a Rakúskom. Hlavným mestom je Bratislava, ktorá sa nachádza na juhozápade krajiny. Stred a sever sú hornatejšie, kým na juhu a východe sú nížiny. Medzi významné rieky patria Dunaj, Váh a Hron. Slovensko má mierne podnebie a štyri ročné obdobia. V horách býva chladnejšie a sneží tam častejšie ako v nížinách.", PALE, ROSE, SMALL),
    p("Модель сравнения — адаптируйте факты", H2),
    table([
        ["Шаг", "Нейтральный шаблон"],
        ["размер", "Moja krajina je väčšia / menšia ako Slovensko."],
        ["положение", "Nachádza sa severnejšie / južnejšie."],
        ["рельеф", "Je u nás viac / menej hôr a nížin."],
        ["зима", "Zimy sú u nás chladnejšie / teplejšie."],
        ["лето", "V lete býva suchšie / vlhkejšie."],
        ["общее", "Obe krajiny majú štyri ročné obdobia."],
    ], [40 * mm, 130 * mm], 5.55),
    p("Мини-диалог", H2),
    box("<b>Katka:</b> Odkiaľ pochádzaš?<br/><b>Alex:</b> Pochádzam z krajiny, ktorá leží ďalej na východe.<br/><b>Katka:</b> Aké je tam podnebie?<br/><b>Alex:</b> Zimy sú u nás chladnejšie ako na Slovensku, ale leto je v niektorých regiónoch teplejšie. Aj u nás sú veľké rozdiely medzi severom a juhom.<br/><b>Katka:</b> A je tam veľa hôr?<br/><b>Alex:</b> V mojej oblasti je viac nížin, preto ma slovenské hory veľmi zaujímajú.", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    p("Источниковая опора: официальные материалы Slovakia.travel, Štatistický úrad SR и SHMÚ; числовые показатели намеренно сведены к минимуму, чтобы модуль оставался устойчивым.", TINY),
    PageBreak(),

    p("5. Частые ошибки и упражнения", H1),
    table([
        ["Ошибка", "Правильно", "Почему"],
        ["*susedí s Poľsko", "susedí s Poľskom", "s + Instrumentál"],
        ["*Bratislava leží v juhozápade", "leží na juhozápade", "сторона света: na + L"],
        ["*Tatry nachádza na severe", "Tatry sa nachádzajú na severe", "sa и множественное число"],
        ["*dnes je daždivý", "dnes je daždivo / prší", "безличное описание погоды"],
        ["*na juhu je viac teplo", "na juhu je teplejšie", "сравнительная степень наречия"],
    ], [55 * mm, 60 * mm, 55 * mm], 5.15),
    p("Упражнение 1. Выберите глагол", H2),
    p("1) Slovensko (leží / pochádza) v strednej Európe. 2) Bratislava sa (nachádza / susedí) na juhozápade. 3) Slovensko (susedí / preteká) s Rakúskom. 4) Tento výrobok (pochádza / leží) zo Slovenska.", SMALL),
    p("Упражнение 2. Поставьте страну в Instrumentál", H2),
    p("Slovensko susedí s (Poľsko), (Česko), (Rakúsko), (Maďarsko) a (Ukrajina).", SMALL),
    p("Упражнение 3. Где находится край?", H2),
    p("Соедините: 1 Bratislavský, 2 Banskobystrický, 3 Prešovský, 4 Košický — a stred, b juhovýchod, c juhozápad, d severovýchod.", SMALL),
    p("Упражнение 4. Сделайте прогноз безличным", H2),
    p("1) Slnko svieti. → ___. 2) Dážď padá. → ___. 3) Sneh bude padať. → ___. 4) Ráno bude hmla. → ___.", SMALL),
    p("Упражнение 5. Сравните регионы", H2),
    p("Используйте <i>teplejšie, chladnejšie, častejšie, viac</i>: юг / север; горы / низменности; снег; осадки. Составьте 4 фразы.", SMALL),
    p("Упражнение 6. Сравните со своей страной", H2),
    p("Напишите 6–7 фраз: положение, один сосед или направление, природа, два погодных сравнения и одно сходство со Словакией. Не придумывайте факты — при необходимости оставьте нейтральный шаблон.", SMALL),
    PageBreak(),

    p("6. Ответы и проверка мастерства", H1),
    p("Ответы", H2),
    table([
        ["№", "Ключ"],
        ["1", "1 leží; 2 nachádza; 3 susedí; 4 pochádza."],
        ["2", "s Poľskom, Českom, Rakúskom, Maďarskom a Ukrajinou."],
        ["3", "1 c; 2 a; 3 d; 4 b."],
        ["4", "1 Je slnečno. 2 Prší. 3 Bude snežiť. 4 Bude hmlisto."],
        ["5", "Модель: Na juhu je teplejšie. Na severe je chladnejšie. V horách sneží častejšie. Na severe býva viac zrážok."],
        ["6", "Возможны разные ответы; проверьте факты, положение, природу, два сравнения и сходство."],
    ], [13 * mm, 157 * mm], 5.35),
    p("Модель самостоятельного ответа", H2),
    box("Slovensko leží v strednej Európe a má päť susedných štátov. Moja krajina sa nachádza ďalej na východe. Je väčšia ako Slovensko a v niektorých oblastiach je viac nížin. Zimy sú u nás chladnejšie, ale na juhu môže byť leto teplejšie. Na Slovensku býva v horách viac snehu ako v nížinách. Obe krajiny majú štyri ročné obdobia, no rozdiely medzi regiónmi sú u nás výraznejšie. Údaje v tomto vzore nahraďte faktmi o svojej krajine.", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    p("Финальная проверка", H2),
    table([
        ["Могу...", "Да / ещё раз"],
        ["описать положение страны и города", "□ / □"],
        ["употребить susediť s + Instrumentál", "□ / □"],
        ["назвать восемь краёв и типы ландшафта", "□ / □"],
        ["дать короткий безличный прогноз", "□ / □"],
        ["сравнить регионы и свою страну", "□ / □"],
    ], [128 * mm, 42 * mm], 5.65),
    box("<b>Критерий освоения:</b> не менее 5 из 6 упражнений без подсказки и устное описание из 6–7 фраз с положением, природой, погодой и двумя корректными сравнениями.", PALE, ROSE, SMALL),
]

doc.build(story)
print(OUTPUT)
