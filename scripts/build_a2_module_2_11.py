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
OUTPUT = ROOT / "output" / "pdf" / "A2" / "Module_02" / "Slovak_A2_Tema_2_11_Gde_kuda_i_otkuda_padezhnye_triady.pdf"
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
BODY = ParagraphStyle("Body", fontName="Arial", fontSize=9.0, leading=12.0, textColor=INK, spaceAfter=3.5 * mm)
SMALL = ParagraphStyle("Small", parent=BODY, fontSize=7.7, leading=9.8, spaceAfter=1.8 * mm)
TINY = ParagraphStyle("Tiny", parent=BODY, fontSize=7.05, leading=8.8, spaceAfter=1.15 * mm)
TITLE = ParagraphStyle("Title", fontName="Arial-Bold", fontSize=20.5, leading=24.5, textColor=colors.white, alignment=TA_LEFT, spaceAfter=5 * mm)
SUBTITLE = ParagraphStyle("Subtitle", fontName="Arial", fontSize=12, leading=16, textColor=colors.HexColor("#FFD8EB"), spaceAfter=5 * mm)
H1 = ParagraphStyle("H1", fontName="Arial-Bold", fontSize=16, leading=19, textColor=PLUM, spaceBefore=1 * mm, spaceAfter=3.5 * mm)
H2 = ParagraphStyle("H2", fontName="Arial-Bold", fontSize=11.1, leading=13.5, textColor=PINK, spaceBefore=1.5 * mm, spaceAfter=1.8 * mm)
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


def styled_table(data, widths, font_size=7.3, header=True):
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
        canvas.drawString(20 * mm, height - 12 * mm, "A2 2.11  |  Где, куда и откуда: падежные триады")
    canvas.setFont("Arial", 8)
    canvas.setFillColor(MUTED)
    canvas.drawString(20 * mm, 9 * mm, "SlovoKrok | личный учебный модуль")
    canvas.drawRightString(width - 20 * mm, 9 * mm, f"стр. {page} / 7")
    canvas.restoreState()


doc = BaseDocTemplate(
    str(OUTPUT), pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=20 * mm, bottomMargin=18 * mm,
    title="Slovak A2 - Тема 2.11 - Где, куда и откуда: падежные триады", author="SlovoKrok",
)
frame = Frame(20 * mm, 18 * mm, 170 * mm, 257 * mm, id="main", leftPadding=0, rightPadding=0)
doc.addPageTemplates([PageTemplate(id="series", frames=[frame], onPage=draw_page)])

story = [
    p("МОДУЛЬ 2  •  ПАДЕЖИ И УПРАВЛЕНИЕ A2", COVER_KICKER),
    p("Где, куда и откуда:<br/>падежные триады", TITLE),
    p("Kde, kam a odkiaľ: priestorové väzby", SUBTITLE),
    Spacer(1, 34 * mm),
    p("Одно место образует не одну фразу, а маршрут из трёх точек: положение, направление и исходная точка.", BODY),
    p("После модуля вы сможете:", H2),
    styled_table([
        ["1", "различать вопросы kde, kam и odkiaľ"],
        ["2", "выбирать v/na + L для положения"],
        ["3", "выбирать do + G или na + A для движения к цели"],
        ["4", "строить z/zo + G и k + D с глаголами движения"],
    ], [12 * mm, 158 * mm], font_size=7.55, header=False),
    Spacer(1, 3 * mm),
    box("<b>Главная формула:</b> kde? v/na + L | kam? do + G или na + A | odkiaľ? z/zo + G", PALE, PINK),
    PageBreak(),

    p("1. KDE? Положение: v/vo и na + L", H1),
    p("Вопрос <b>Kde?</b> описывает место без направления. После <b>v/vo</b> и <b>na</b> здесь нужен <b>Lokál</b>.", BODY),
    styled_table([
        ["Модель", "Когда чаще", "Примеры"],
        ["v/vo + L", "внутри, город, большинство стран, учреждение", "v izbe; v Bratislave; v Rakúsku; vo firme"],
        ["na + L", "поверхность, событие, служба, отдельные страны", "na stole; na kurze; na pošte; na Slovensku"],
    ], [30 * mm, 58 * mm, 82 * mm], font_size=6.75),
    p("Готовые триады места", H2),
    styled_table([
        ["Kde?", "Kam?", "Odkiaľ?"],
        ["v škole", "do školy", "zo školy"],
        ["v banke", "do banky", "z banky"],
        ["na pošte", "na poštu", "z pošty"],
        ["na stanici", "na stanicu", "zo stanice"],
        ["v centre", "do centra", "z centra"],
    ], [56.5 * mm, 56.5 * mm, 57 * mm], font_size=7.15),
    box("<b>Важно:</b> предлог надо учить вместе с конкретным местом. По-словацки <b>v škole</b>, но <b>na pošte</b>; одна русская конструкция «в» не выбирает словацкий предлог.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    p("Сравните: <b>Som v kancelárii.</b> Я в офисе. <b>Čakám na námestí.</b> Я жду на площади. <b>Bývame na Slovensku.</b> Мы живём в Словакии.", SMALL),
    PageBreak(),

    p("2. KAM? Цель движения: do + G, na + A, k + D", H1),
    p("Вопрос <b>Kam?</b> означает направление к цели. Выбор модели зависит от типа цели.", BODY),
    styled_table([
        ["Модель", "Смысл", "Примеры"],
        ["do + G", "внутрь; город или страна", "do obchodu; do Košíc; do Rakúska"],
        ["na + A", "на поверхность; событие, служба, открытое место", "na stôl; na koncert; na poštu; na ihrisko"],
        ["k/ku + D", "к человеку или объекту, не внутрь него", "k lekárovi; ku kamarátke; k oknu"],
    ], [31 * mm, 61 * mm, 78 * mm], font_size=6.65),
    p("Do или k?", H2),
    styled_table([
        ["Движение внутрь", "Движение к адресату или объекту"],
        ["Idem do nemocnice. Я иду в больницу.", "Idem k lekárovi. Я иду к врачу."],
        ["Vošla do domu. Она вошла в дом.", "Prišla k domu. Она подошла к дому."],
        ["Ideme do susedovej izby. Мы идём в комнату соседа.", "Ideme k susedovi. Мы идём к соседу."],
    ], [85 * mm, 85 * mm], font_size=6.65),
    p("Глагол показывает способ движения, модель показывает цель", H2),
    p("<b>ísť</b> идти/ехать: Idem do práce. <b>prísť</b> прийти: Prišla na stretnutie. <b>vojsť</b> войти: Vošiel do izby. <b>vrátiť sa</b> вернуться: Vrátime sa do hotela.", SMALL),
    box("<b>Типичная ошибка:</b> *Idem v škole означает неправильное смешение движения и положения. Нужно <b>Idem do školy</b>, но <b>Som v škole</b>.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    PageBreak(),

    p("3. ODKIAĽ? Исходная точка: z/zo + G", H1),
    p("Вопрос <b>Odkiaľ?</b> спрашивает, откуда начинается движение. После <b>z/zo</b> нужен <b>Genitív</b>. Форма <b>zo</b> облегчает произношение: <b>zo školy, zo stanice, zo Slovenska</b>.", BODY),
    styled_table([
        ["Исходная точка", "Пример", "Перевод"],
        ["изнутри", "Vychádzam z obchodu.", "Я выхожу из магазина."],
        ["из города", "Vrátili sa z Bratislavy.", "Они вернулись из Братиславы."],
        ["из страны", "Prišla zo Slovenska.", "Она приехала из Словакии."],
        ["с события", "Ideme z koncertu.", "Мы идём с концерта."],
        ["со службы/места", "Volám ti z pošty.", "Я звоню тебе с почты."],
    ], [39 * mm, 66 * mm, 65 * mm], font_size=6.7),
    p("Собираем маршрут", H2),
    styled_table([
        ["Положение", "Движение к цели", "Движение оттуда"],
        ["Sme v hoteli.", "Ideme do hotela.", "Odchádzame z hotela."],
        ["Je na letisku.", "Ide na letisko.", "Vracia sa z letiska."],
        ["Čaká u lekára.", "Ide k lekárovi.", "Ide od lekára."],
    ], [56.5 * mm, 56.5 * mm, 57 * mm], font_size=6.75),
    p("Z/zo и od", H2),
    p("<b>z/zo + G</b> обозначает выход из места или движение с него: <b>zo školy, z pošty</b>. <b>od + G</b> означает «от человека/объекта»: <b>od lekára, od okna</b>. Это полезная пара к <b>k + D</b>: <b>k lekárovi - od lekára</b>.", SMALL),
    box("<b>Проверка смысла:</b> сначала задайте вопрос. Где? <b>na stanici</b>. Куда? <b>na stanicu</b>. Откуда? <b>zo stanice</b>. Окончание меняется вместе с ролью места.", PALE, ROSE, SMALL),
    PageBreak(),

    p("4. Глаголы движения в связной речи", H1),
    p("На A2 важно не только назвать форму, но и связать путь: отправная точка, цель, действие в месте и возвращение.", BODY),
    styled_table([
        ["Глагол", "Фокус", "Пример"],
        ["ísť / chodiť", "одно движение / регулярно", "Dnes idem do práce. Každý deň chodím do práce."],
        ["prísť / prichádzať", "прибыть / прибывать", "Prišli sme na stanicu. Vlak prichádza na stanicu."],
        ["vojsť / vyjsť", "войти / выйти", "Vošla do banky a potom vyšla z banky."],
        ["odísť", "уйти, уехать", "O šiestej odchádzam z kancelárie."],
        ["vrátiť sa", "вернуться", "Večer sa vrátim domov."],
    ], [38 * mm, 43 * mm, 89 * mm], font_size=6.55),
    p("Мини-диалог: маршрут по городу", H2),
    box("<b>A:</b> Kde si teraz?<br/><b>B:</b> Som na stanici. O chvíľu idem do centra.<br/><b>A:</b> Kam pôjdeš potom?<br/><b>B:</b> Najprv pôjdem na poštu a potom k lekárovi.<br/><b>A:</b> A odkiaľ mi zavoláš?<br/><b>B:</b> Zavolám ti z pošty. Od lekára sa vrátim domov.", PALE, ROSE, SMALL),
    p("Образец связного маршрута", H2),
    p("Ráno som doma. O ôsmej idem z domu na zastávku a potom do práce. V kancelárii som do piatej. Po práci idem na kurz. Z kurzu sa vraciam domov električkou.", SMALL),
    p("Утром я дома. В восемь я иду из дома на остановку, затем на работу. В офисе я до пяти. После работы иду на курс. С курса возвращаюсь домой на трамвае.", SMALL),
    box("<b>Особая форма:</b> с <b>domov</b> обычно нет предлога: <b>Som doma. Idem domov. Vraciam sa domov.</b> Откуда: <b>Idem z domu.</b>", CREAM, colors.HexColor("#E7C76C"), TINY),
    PageBreak(),

    p("5. Банк примеров и упражнения", H1),
    p("Быстрый банк триад", H2),
    styled_table([
        ["Место", "Kde?", "Kam?", "Odkiaľ?"],
        ["школа", "v škole", "do školy", "zo školy"],
        ["работа", "v práci", "do práce", "z práce"],
        ["почта", "na pošte", "na poštu", "z pošty"],
        ["рынок", "na trhu", "na trh", "z trhu"],
        ["центр", "v centre", "do centra", "z centra"],
        ["Словакия", "na Slovensku", "na Slovensko", "zo Slovenska"],
    ], [31 * mm, 46 * mm, 46 * mm, 47 * mm], font_size=6.65),
    p("Упражнение 1. Определите вопрос", H2),
    p("Напишите kde, kam или odkiaľ: 1) Som v knižnici. 2) Ideme na výlet. 3) Vracia sa z práce. 4) Prišiel k oknu.", TINY),
    p("Упражнение 2. Выберите предлог и форму", H2),
    p("1) Bývam ___ (Bratislava). 2) Idem ___ (Bratislava). 3) Vraciam sa ___ (Bratislava). 4) Čakám ___ (pošta). 5) Idem ___ (pošta).", TINY),
    p("Упражнение 3. Соберите триады", H2),
    p("Дайте kde - kam - odkiaľ для: 1) škola; 2) stanica; 3) obchod; 4) Slovensko.", TINY),
    p("Упражнение 4. Исправьте ошибки", H2),
    p("1) Som do kancelárie. 2) Idem v škole. 3) Vraciame sa zo pošty. 4) Idem do lekára. 5) Prišla z Slovenska.", TINY),
    p("Упражнение 5. Переведите", H2),
    p("1) Мы в центре. 2) Я иду на вокзал. 3) Она возвращается из школы. 4) Завтра я пойду к врачу. 5) Он вышел из банка.", TINY),
    p("Упражнение 6. Мой маршрут", H2),
    p("Напишите 5-7 связанных предложений: где вы утром, куда идёте, где бываете днём, откуда возвращаетесь и куда направляетесь вечером. Используйте минимум одну полную триаду.", TINY),
    PageBreak(),

    p("6. Ответы и проверка мастерства", H1),
    p("Ответы", H2),
    p("<b>1.</b> 1) kde; 2) kam; 3) odkiaľ; 4) kam.", TINY),
    p("<b>2.</b> 1) v Bratislave; 2) do Bratislavy; 3) z Bratislavy; 4) na pošte; 5) na poštu.", TINY),
    p("<b>3.</b> 1) v škole - do školy - zo školy; 2) na stanici - na stanicu - zo stanice; 3) v obchode - do obchodu - z obchodu; 4) na Slovensku - na Slovensko - zo Slovenska.", TINY),
    p("<b>4.</b> 1) Som v kancelárii. 2) Idem do školy. 3) Vraciame sa z pošty. 4) Idem k lekárovi. 5) Prišla zo Slovenska.", TINY),
    p("<b>5.</b> 1) Sme v centre. 2) Idem na stanicu. 3) Vracia sa zo školy. 4) Zajtra pôjdem k lekárovi. 5) Vyšiel z banky.", TINY),
    p("<b>6. Модель:</b> Ráno som doma. O ôsmej idem z domu do práce. Pracujem v kancelárii v centre. Na obed idem do malej reštaurácie. Po práci idem na kurz. Z kurzu sa vraciam domov. Večer som doma.", TINY),
    p("Итог в четырёх пунктах", H2),
    styled_table([
        ["OK", "Kde? требует положения: v/na + L."],
        ["OK", "Kam? требует цели: do + G, na + A или k + D."],
        ["OK", "Odkiaľ? требует исходной точки: z/zo + G."],
        ["OK", "Я учу место как триаду и связываю её с глаголом движения."],
    ], [12 * mm, 158 * mm], font_size=7.0, header=False),
    Spacer(1, 2.5 * mm),
    box("<b>Финальная проверка:</b> без подсказки составьте триады для škola, pošta, centrum и Slovensko, затем расскажите свой маршрут в 5 предложениях.", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    p("Следующий шаг", H2),
    p("В теме 2.12 вы объедините падежи в одну систему управления и добавите модели обращения.", SMALL),
]

doc.build(story)
print(OUTPUT)
