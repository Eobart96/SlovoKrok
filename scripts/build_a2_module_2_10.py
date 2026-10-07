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
OUTPUT = ROOT / "output" / "pdf" / "A2" / "Module_02" / "Slovak_A2_Tema_2_10_Instrumental_sredstvo_sovmestnost_i_harakteristika.pdf"
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
TINY = ParagraphStyle("Tiny", parent=BODY, fontSize=7.15, leading=8.9, spaceAfter=1.25 * mm)
TITLE = ParagraphStyle("Title", fontName="Arial-Bold", fontSize=21, leading=25, textColor=colors.white, alignment=TA_LEFT, spaceAfter=5 * mm)
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
        canvas.drawString(20 * mm, height - 12 * mm, "A2 2.10  |  Inštrumentál: средство, совместность и характеристика")
    canvas.setFont("Arial", 8)
    canvas.setFillColor(MUTED)
    canvas.drawString(20 * mm, 9 * mm, "SlovoKrok | личный учебный модуль")
    canvas.drawRightString(width - 20 * mm, 9 * mm, f"стр. {page} / 7")
    canvas.restoreState()


doc = BaseDocTemplate(
    str(OUTPUT), pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=20 * mm, bottomMargin=18 * mm,
    title="Slovak A2 - Тема 2.10 - Inštrumentál: средство, совместность и характеристика", author="SlovoKrok",
)
frame = Frame(20 * mm, 18 * mm, 170 * mm, 257 * mm, id="main", leftPadding=0, rightPadding=0)
doc.addPageTemplates([PageTemplate(id="series", frames=[frame], onPage=draw_page)])

story = [
    p("МОДУЛЬ 2  •  ПАДЕЖИ И УПРАВЛЕНИЕ A2", COVER_KICKER),
    p("Inštrumentál:<br/>средство, совместность<br/>и характеристика", TITLE),
    p("Inštrumentál: prostriedok, sprievod a charakteristika", SUBTITLE),
    Spacer(1, 24 * mm),
    p("Inštrumentál отвечает на вопросы <b>kým? čím?</b> и помогает назвать инструмент, транспорт, спутника, положение предмета и роль человека.", BODY),
    p("После модуля вы сможете:", H2),
    styled_table([
        ["1", "говорить, чем выполняется действие и на чём едут"],
        ["2", "различать средство без предлога и совместность с s/so"],
        ["3", "описывать положение с pred, za, medzi, nad и pod"],
        ["4", "называть профессию и согласовывать формы singular/plural"],
    ], [12 * mm, 158 * mm], font_size=7.75, header=False),
    Spacer(1, 3 * mm),
    box("<b>Главная формула:</b> Píšem <b>perom</b>. Idem <b>s kolegom</b>. Stal sa <b>lekárom</b>.", PALE, PINK),
    PageBreak(),

    p("1. Формы единственного числа", H1),
    p("У существительных мужского рода чаще всего встречается -om. В среднем роде форма зависит от модели: -om или -ím. В женском роде типично -ou. Прилагательное согласуется со всем сочетанием.", BODY),
    styled_table([
        ["Род / модель", "Nominatív → Inštrumentál", "С группой"],
        ["мужской", "brat → bratom; kolega → kolegom", "s dobrým bratom; s novým kolegom"],
        ["мужской, мягкий", "učiteľ → učiteľom; priateľ → priateľom", "s mladým učiteľom"],
        ["женский, -a", "žena → ženou; sestra → sestrou", "s dobrou sestrou"],
        ["женский, мягкая", "kolegyňa → kolegyňou; ulica → ulicou", "s novou kolegyňou"],
        ["женский, согласная", "dlaň → dlaňou; kosť → kosťou", "pravou dlaňou"],
        ["средний", "mesto → mestom; auto → autom", "nad starým mestom; novým autom"],
        ["средний, особая", "námestie → námestím; dieťa → dieťaťom", "nad námestím; s malým dieťaťom"],
    ], [34 * mm, 68 * mm, 68 * mm], font_size=6.45),
    p("Согласование", H2),
    styled_table([
        ["Мужской / средний", "Женский"],
        ["s mojím dobrým kolegom", "s mojou dobrou kolegyňou"],
        ["pred tým veľkým domom", "za tou novou školou"],
    ], [85 * mm, 85 * mm], font_size=7.0),
    box("<b>Надёжная привычка:</b> учите не отдельное окончание, а готовую группу: s kolegom, s kolegyňou, novým autom, pred domom.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    PageBreak(),

    p("2. Средство без предлога, спутник с s/so", H1),
    styled_table([
        ["Смысл", "Вопрос", "Модель", "Пример"],
        ["инструмент", "čím?", "без предлога", "Píšem perom."],
        ["способ оплаты", "čím?", "без предлога", "Platím kartou."],
        ["транспорт", "čím?", "без предлога", "Cestujem vlakom."],
        ["совместность", "s kým?", "s/so + I", "Idem s kolegom."],
    ], [32 * mm, 27 * mm, 43 * mm, 68 * mm], font_size=6.85),
    p("Главный контраст", H2),
    box("<b>Idem autobusom.</b> - Я еду автобусом / на автобусе.<br/><b>Idem s kamarátom.</b> - Я иду вместе с другом.<br/><b>Otvorím to kľúčom.</b> - Я открою это ключом.<br/><b>Otvorím to s kolegom.</b> - Я открою это вместе с коллегой.", PALE, ROSE, SMALL),
    p("Когда нужно so", H2),
    p("Форма <b>so</b> облегчает произношение перед s, š, z, ž: <b>so sestrou, so šéfom, so Zuzanou, so ženou</b>. Отдельно запомните <b>so mnou</b>.", BODY),
    styled_table([
        ["Лицо", "Форма", "Пример"],
        ["ja / ty", "so mnou / s tebou", "Pôjdeš so mnou?"],
        ["on / ona", "s ním / s ňou", "Hovorím s ním a s ňou."],
        ["my / vy", "s nami / s vami", "Zostanú s nami."],
        ["oni / ony", "s nimi", "Stretávam sa s nimi."],
    ], [32 * mm, 52 * mm, 86 * mm], font_size=6.9),
    PageBreak(),

    p("3. Pred, za, medzi, nad, pod: где находится?", H1),
    p("Когда эти предлоги описывают неподвижное положение и отвечают на <b>kde?</b>, после них стоит Inštrumentál. Направление движения будет отдельно систематизировано в теме 2.11.", BODY),
    styled_table([
        ["Предлог", "Модель", "Пример", "Перевод"],
        ["pred", "перед", "Auto je pred domom.", "Машина перед домом."],
        ["za", "за", "Záhrada je za školou.", "Сад за школой."],
        ["medzi", "между", "Kaviareň je medzi bankou a poštou.", "Кафе между банком и почтой."],
        ["nad", "над", "Lampa je nad stolom.", "Лампа над столом."],
        ["pod", "под", "Taška je pod stoličkou.", "Сумка под стулом."],
    ], [23 * mm, 28 * mm, 73 * mm, 46 * mm], font_size=6.55),
    p("Полные группы", H2),
    styled_table([
        ["Единственное число", "Множественное число"],
        ["pred starým domom", "pred starými domami"],
        ["za vysokou školou", "za vysokými školami"],
        ["medzi novou budovou a parkom", "medzi novými budovami"],
        ["nad modrým stolom", "nad modrými stolmi"],
        ["pod veľkým mostom", "pod veľkými mostami"],
    ], [85 * mm, 85 * mm], font_size=6.85),
    box("<b>Не переносите русский падеж механически.</b> Сначала выберите словацкий предлог и его смысл, затем задайте словацкий вопрос: s kým? čím? kde?", CREAM, colors.HexColor("#E7C76C"), SMALL),
    PageBreak(),

    p("4. Множественное число и профессия", H1),
    p("Во множественном числе прилагательное получает -ými/-imi. У существительных встречаются -mi и -ami; частотные формы лучше запоминать готовыми сочетаниями.", BODY),
    styled_table([
        ["Группа", "Пример"],
        ["s dobrými kolegami", "Pracujem s dobrými kolegami."],
        ["s novými učiteľmi", "Rozprávam sa s novými učiteľmi."],
        ["medzi starými domami", "Park je medzi starými domami."],
        ["pred malými deťmi", "Učiteľ stojí pred malými deťmi."],
        ["vlakmi / autami", "Cestujeme vlakmi a autami."],
        ["s ľuďmi / s deťmi", "Pracuje s ľuďmi a s deťmi."],
    ], [70 * mm, 100 * mm], font_size=6.85),
    p("Как назвать профессию", H2),
    styled_table([
        ["Модель", "Нюанс", "Пример"],
        ["Som + N", "нейтральная идентификация", "Som lekár. Som učiteľka."],
        ["byť + I", "роль или характеристика", "Je skúseným lekárom."],
        ["stať sa + I", "стать кем-то", "Stala sa učiteľkou."],
        ["pracovať ako + N", "естественно о работе", "Pracujem ako programátor."],
    ], [48 * mm, 55 * mm, 67 * mm], font_size=6.75),
    box("<b>Важно:</b> для обычного ответа о профессии безопасно сказать <b>Som lekár</b> или <b>Pracujem ako lekár</b>. После <b>stať sa</b> нужен Inštrumentál: <b>Stal sa lekárom</b>.", PALE, ROSE, SMALL),
    p("Мини-диалог", H2),
    box("<b>A:</b> Ako cestuješ do práce?<br/><b>B:</b> Väčšinou vlakom, dnes s kolegyňou.<br/><b>A:</b> Čím sa zaoberáš?<br/><b>B:</b> Pracujem ako technik. Kolegyňa je projektantkou.<br/><b>A:</b> Kde máte kanceláriu?<br/><b>B:</b> Medzi bankou a poštou, pod veľkým nápisom.", ALT, ROSE, TINY),
    p("Перевод: Как ты ездишь на работу? - Обычно поездом, сегодня с коллегой. - Чем занимаешься? - Работаю техником. Коллега работает проектировщицей. - Где ваш офис? - Между банком и почтой, под большой вывеской.", TINY),
    PageBreak(),

    p("5. Частые ошибки и упражнения", H1),
    box("<b>Алгоритм:</b> средство или транспорт → без предлога; спутник → s/so; неподвижное положение → pred/za/medzi/nad/pod; роль после stať sa → Inštrumentál.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    p("Упражнение 1. Добавьте предлог, только если он нужен", H2),
    p("1) cestujem ___ autobusom; 2) idem ___ kamarátom; 3) píšem ___ perom; 4) hovorím ___ šéfom; 5) platím ___ kartou; 6) bývam ___ sestrou.", SMALL),
    p("Упражнение 2. Поставьте существительное в Inštrumentál", H2),
    p("1) s (kolega); 2) s (sestra); 3) pred (dom); 4) za (škola); 5) nad (mesto); 6) s (dieťa).", SMALL),
    p("Упражнение 3. Согласуйте всю группу", H2),
    p("1) s (nový kolega); 2) s (dobrá kolegyňa); 3) pod (veľký most); 4) medzi (staré domy); 5) s (malé deti).", SMALL),
    p("Упражнение 4. Выберите форму профессии", H2),
    p("1) Som (lekár / lekárom). 2) Stala sa (učiteľka / učiteľkou). 3) Pracujem ako (technik / technikom). 4) Je skúseným (programátor / programátorom).", SMALL),
    p("Упражнение 5. Исправьте ошибки", H2),
    p("1) Idem s autobusom. 2) Píšem s perom. 3) Hovorím s sestrou. 4) Stal sa lekár. 5) Park je medzi staré domy.", SMALL),
    p("Упражнение 6. Рабочий день", H2),
    p("Напишите 5-7 связанных предложений: как и с кем вы едете, чем пользуетесь, где находится рабочее место и кем вы работаете или хотите стать.", SMALL),
    PageBreak(),

    p("6. Ответы и проверка мастерства", H1),
    p("Ответы", H2),
    p("<b>1.</b> autobusom; s kamarátom; perom; so šéfom; kartou; so sestrou.", TINY),
    p("<b>2.</b> s kolegom; so sestrou; pred domom; za školou; nad mestom; s dieťaťom.", TINY),
    p("<b>3.</b> s novým kolegom; s dobrou kolegyňou; pod veľkým mostom; medzi starými domami; s malými deťmi.", TINY),
    p("<b>4.</b> Som lekár; Stala sa učiteľkou; Pracujem ako technik; Je skúseným programátorom. В первой фразе возможно Som lekárom при акценте на роли, но нейтральный ответ - Som lekár.", TINY),
    p("<b>5.</b> 1) Idem autobusom. 2) Píšem perom. 3) Hovorím so sestrou. 4) Stal sa lekárom. 5) Park je medzi starými domami.", TINY),
    p("<b>6. Модель:</b> Do práce cestujem vlakom a niekedy idem s kolegyňou. V kancelárii pracujem na počítači a poznámky píšem perom. Naša budova je medzi bankou a hotelom. Pracujem ako technik, ale chcem sa stať projektovým manažérom.", TINY),
    p("Итог в четырёх пунктах", H2),
    styled_table([
        ["OK", "Я называю средство без предлога: perom, kartou, vlakom."],
        ["OK", "Я выражаю совместность с s/so: s kolegom, so sestrou."],
        ["OK", "Я описываю положение с pred, za, medzi, nad и pod."],
        ["OK", "Я называю профессию и использую stať sa + Inštrumentál."],
    ], [12 * mm, 158 * mm], font_size=7.2, header=False),
    Spacer(1, 3 * mm),
    box("<b>Финальная проверка:</b> без подсказки скажите две фразы о средстве или транспорте, две о совместности, одну о положении и одну о профессии.", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    p("Следующий шаг", H2),
    p("В теме 2.11 вы соберёте пространственные падежные триады и научитесь различать положение, направление и исходную точку: kde - kam - odkiaľ.", SMALL),
]

doc.build(story)
print(OUTPUT)
