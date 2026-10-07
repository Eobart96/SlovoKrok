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
OUTPUT = ROOT / "output/pdf/A2/Module_07/Slovak_A2_Tema_7_1_Professiya_obyazannosti_i_opyt.pdf"
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
        canvas.drawString(20 * mm, height - 12 * mm, "A2 7.1  |  Профессия, обязанности и опыт")
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
    title="Slovak A2 - Тема 7.1 - Профессия, обязанности и опыт",
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
    p("МОДУЛЬ 7  •  РАБОТА, ПУТЕШЕСТВИЯ И СТРАНА", KICK),
    p("Профессия, обязанности и опыт", TITLE),
    p("Povolanie, pracovné povinnosti a skúsenosti: связно рассказываем о своей работе", SUBTITLE),
    Spacer(1, 41 * mm),
    p("На уровне A2 мало назвать профессию. Нужно коротко объяснить, где и кем вы работаете, что делаете регулярно, что делали раньше и какие навыки приобрели."),
    p("После модуля вы сможете:", H2),
    table([
        ["1", "представить профессию и место работы"],
        ["2", "описать регулярные обязанности"],
        ["3", "рассказать о прошлом опыте и результате"],
        ["4", "назвать навыки и сравнить две работы"],
    ], [12 * mm, 158 * mm], 7.2, False),
    Spacer(1, 3 * mm),
    box("<b>Формула рассказа:</b> кто я сейчас + где работаю + за что отвечаю + где работал раньше + что умею + чем две работы отличаются."),
    PageBreak(),

    p("1. Нынешняя работа и обязанности", H1),
    p("Для профессии используйте <b>som + профессия</b> или <b>pracujem ako + профессия</b>. После <i>ako</i> название остаётся в Nominatív: <i>ako technik</i>, не *ako technikom*."),
    table([
        ["Что сообщаем", "Модель", "Пример и перевод"],
        ["профессия", "Som / Pracujem ako...", "Pracujem ako účtovníčka. - Я работаю бухгалтером."],
        ["место", "Pracujem v/na...", "Pracujem v malej firme. - Я работаю в небольшой фирме."],
        ["сфера", "Pracujem v oblasti...", "Pracujem v oblasti IT. - Я работаю в сфере IT."],
        ["главная задача", "Mám na starosti + A", "Mám na starosti faktúry. - Я отвечаю за счета."],
        ["ответственность", "Zodpovedám za + A", "Zodpovedám za tím. - Я отвечаю за команду."],
    ], [34 * mm, 48 * mm, 88 * mm], 5.65),
    p("Полезные связки для обязанностей", H2),
    table([
        ["Связка", "Пример", "Перевод"],
        ["starať sa o + A", "Starám sa o zákazníkov.", "Я занимаюсь клиентами."],
        ["venovať sa + D", "Venujem sa marketingu.", "Я занимаюсь маркетингом."],
        ["komunikovať s + I", "Komunikujem s dodávateľmi.", "Я общаюсь с поставщиками."],
        ["pomáhať + D", "Pomáham novým kolegom.", "Я помогаю новым коллегам."],
    ], [38 * mm, 66 * mm, 66 * mm], 5.8),
    box("<b>Не перечисляйте только существительные.</b> Связывайте 2-3 обязанности: <i>Pripravujem ponuky, komunikujem so zákazníkmi a kontrolujem objednávky.</i>", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    PageBreak(),

    p("2. Прошлый опыт и вид глагола", H1),
    p("Прошлую работу вводят слова <b>predtým</b>, <b>minulý rok</b>, <b>od roku... do roku...</b>. В прошедшем времени форма согласуется с говорящим: <i>pracoval som</i> / <i>pracovala som</i>."),
    table([
        ["Задача", "Процесс / повтор", "Завершённый результат"],
        ["документы", "pripravovať dokumenty", "pripraviť správu"],
        ["проблема", "riešiť problémy", "vyriešiť problém"],
        ["контроль", "kontrolovať objednávky", "skontrolovať objednávku"],
        ["организация", "organizovať stretnutia", "zorganizovať stretnutie"],
    ], [31 * mm, 67 * mm, 72 * mm], 5.8),
    p("Как выбирать вид в рассказе", H2),
    table([
        ["Смысл", "Пример", "Перевод"],
        ["обычная обязанность", "Každý deň som kontroloval objednávky.", "Каждый день я проверял заказы."],
        ["один готовый результат", "Včera som skontroloval veľkú objednávku.", "Вчера я проверил крупный заказ."],
        ["длительный опыт", "Tri roky som pracovala v banke.", "Я три года работала в банке."],
        ["достижение", "Zorganizovala som odbornú konferenciu.", "Я организовала профессиональную конференцию."],
    ], [38 * mm, 72 * mm, 60 * mm], 5.6),
    box("<b>Русскоязычная ловушка:</b> продолжительность не требует совершенного вида. <i>Dva roky som pracoval v hoteli</i> описывает период опыта. Совершенный вид нужен, когда важен достигнутый итог.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    PageBreak(),

    p("3. Навыки: vedieť, poznať, môcť", H1),
    table([
        ["Глагол", "Когда употреблять", "Пример"],
        ["vedieť", "уметь + infinitív; знать факт", "Viem pracovať s Excelom. / Viem, kde je kancelária."],
        ["poznať", "знать человека, место, систему", "Poznám tento program a našich klientov."],
        ["môcť", "мочь: есть возможность или разрешение", "Môžem pracovať samostatne aj v tíme."],
    ], [25 * mm, 61 * mm, 84 * mm], 5.8),
    p("Опыт и уверенная самооценка", H2),
    table([
        ["Модель", "Естественный пример", "Перевод"],
        ["mať skúsenosti s + I", "Mám skúsenosti s predajom.", "У меня есть опыт в продажах."],
        ["dobre ovládať + A", "Dobre ovládam slovenčinu.", "Я хорошо владею словацким."],
        ["byť dobrý/dobrá v + L", "Som dobrá v organizovaní.", "Я хорошо умею организовывать."],
        ["dokázať + infinitív", "Dokážem rýchlo vyriešiť problém.", "Я способен быстро решить проблему."],
    ], [46 * mm, 66 * mm, 58 * mm], 5.55),
    p("Сравниваем две работы", H2),
    box("<b>Moja súčasná práca je náročnejšia, ale aj zaujímavejšia.</b> V predchádzajúcej práci som mal menej zodpovednosti. Teraz pracujem samostatnejšie a častejšie komunikujem s klientmi.<br/><br/>Моя нынешняя работа сложнее, но и интереснее. На прошлой работе у меня было меньше ответственности. Сейчас я работаю более самостоятельно и чаще общаюсь с клиентами.", PALE, ROSE, SMALL),
    p("Не путайте: <i>vedieť programovať</i> - уметь программировать; <i>poznať program</i> - знать конкретную программу; <i>môcť programovať z domu</i> - иметь возможность программировать из дома.", TINY),
    PageBreak(),

    p("4. Банк фраз и модель рассказа", H1),
    table([
        ["SK", "RU"],
        ["Som zdravotná sestra.", "Я медсестра."],
        ["Pracujem ako kuchár v hoteli.", "Я работаю поваром в отеле."],
        ["Naša firma predáva zdravotnícke pomôcky.", "Наша фирма продаёт медицинские принадлежности."],
        ["Mojou hlavnou úlohou je plánovať projekty.", "Моя главная задача - планировать проекты."],
        ["Každé ráno odpovedám na e-maily.", "Каждое утро я отвечаю на письма."],
        ["Často pripravujem prezentácie.", "Я часто готовлю презентации."],
        ["Raz za mesiac píšem správu.", "Раз в месяц я пишу отчёт."],
        ["Predtým som pracoval v obchode.", "Раньше я работал в магазине."],
        ["Mal som na starosti sklad.", "Я отвечал за склад."],
        ["Naučil som sa komunikovať so zákazníkmi.", "Я научился общаться с клиентами."],
        ["Poznám naše výrobky veľmi dobre.", "Я очень хорошо знаю наши товары."],
        ["Viem používať účtovný program.", "Я умею пользоваться бухгалтерской программой."],
        ["Môžem pracovať aj cez víkend.", "Я могу работать и по выходным."],
        ["Táto práca je pokojnejšia ako predchádzajúca.", "Эта работа спокойнее предыдущей."],
    ], [88 * mm, 82 * mm], 5.25),
    p("Модель устного рассказа", H2),
    box("<b>Pracujem ako projektová koordinátorka v malej technologickej firme.</b> Mám na starosti harmonogramy a komunikáciu s klientmi. Každý deň kontrolujem úlohy a pomáham kolegom. Predtým som tri roky pracovala v cestovnej kancelárii, kde som pripravovala ponuky a riešila problémy zákazníkov. Naučila som sa dobre organizovať čas. Viem pracovať s viacerými programami a poznám potreby klientov. Moja súčasná práca je náročnejšia, ale je tvorivejšia a mám v nej viac samostatnosti.", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    PageBreak(),

    p("5. Частые ошибки и упражнения", H1),
    box("<b>Частые ошибки:</b> *pracujem účtovníkom* вместо <b>pracujem ako účtovník</b>; *zodpovedám o tím* вместо <b>za tím</b>; <b>poznať</b> перед infinitív; совершенный вид для регулярной обязанности; рассказ только в настоящем времени без прошлого опыта.", CREAM, colors.HexColor("#E7C76C"), TINY),
    p("Упражнение 1. Выберите подходящий глагол", H2),
    p("1) ___ pracovať s databázou. (Viem/Poznám) 2) ___ tento program. (Viem/Poznám) 3) Zajtra ___ pracovať z domu. (viem/môžem) 4) ___, že porada je o desiatej. (Viem/Poznám)", TINY),
    p("Упражнение 2. Дополните связку", H2),
    p("1) Mám na starosti ___ (objednávky). 2) Zodpovedám ___ (malý tím). 3) Starám sa ___ (zákazníci). 4) Komunikujem ___ (dodávatelia).", TINY),
    p("Упражнение 3. Выберите вид", H2),
    p("1) Každý pondelok som pripravoval/pripravil správu. 2) Včera som konečne riešil/vyriešil problém. 3) Minulý rok som pravidelne organizoval/zorganizoval školenia.", TINY),
    p("Упражнение 4. Исправьте ошибки", H2),
    p("1) Pracujem manažérom. 2) Poznám používať Excel. 3) Zodpovedám o faktúry. 4) Každý deň som skontroloval e-maily.", TINY),
    p("Упражнение 5. Переведите", H2),
    p("1) Я работаю техником в небольшой фирме. 2) Я отвечаю за оборудование. 3) Раньше я работала в школе. 4) Я умею работать самостоятельно. 5) Эта работа интереснее предыдущей.", TINY),
    p("Упражнение 6. Ваш опыт", H2),
    p("Подготовьте 7-9 предложений о реальной или воображаемой работе. Назовите профессию и место, 2-3 обязанности, один прошлый период, одно достижение, два навыка и одно сравнение. Затем расскажите текст за 60-90 секунд без чтения.", TINY),
    PageBreak(),

    p("6. Ответы и проверка мастерства", H1),
    p("Ответы", H2),
    p("<b>1.</b> 1) <b>Viem</b> pracovať s databázou. 2) <b>Poznám</b> tento program. 3) Zajtra <b>môžem</b> pracovať z domu. 4) <b>Viem</b>, že porada je o desiatej.", TINY),
    p("<b>2.</b> 1) objednávky; 2) <b>za</b> malý tím; 3) <b>o</b> zákazníkov; 4) <b>s</b> dodávateľmi.", TINY),
    p("<b>3.</b> 1) pripravoval; 2) vyriešil; 3) organizoval.", TINY),
    p("<b>4.</b> 1) Pracujem <b>ako manažér/manažérka</b>. 2) <b>Viem používať</b> Excel. 3) Zodpovedám <b>za faktúry</b>. 4) Každý deň som <b>kontroloval/kontrolovala</b> e-maily.", TINY),
    p("<b>5.</b> Pracujem ako technik/technička v malej firme. Zodpovedám za technické vybavenie. Predtým som pracovala v škole. Viem pracovať samostatne. Táto práca je zaujímavejšia ako predchádzajúca.", TINY),
    p("<b>6. Модель:</b> Pracujem ako administratívny pracovník v malej firme. Mám na starosti dokumenty a objednávky. Každý deň komunikujem so zákazníkmi a kontrolujem faktúry. Predtým som dva roky pracoval v hoteli. Minulý mesiac som úspešne zorganizoval veľké stretnutie. Viem dobre plánovať čas a poznám niekoľko kancelárskych programov. Moja súčasná práca je náročnejšia, ale zaujímavejšia. Возможны другие естественные варианты.", TINY),
    p("Итог в четырёх пунктах", H2),
    table([
        ["OK", "Представляю профессию через som или pracujem ako."],
        ["OK", "Связываю обязанности с правильным управлением."],
        ["OK", "Различаю повторный процесс и завершённый результат."],
        ["OK", "Различаю vedieť, poznať и môcť и сравниваю опыт."],
    ], [12 * mm, 158 * mm], 6.2, False),
    Spacer(1, 2 * mm),
    box("<b>Финальная проверка:</b> за 60-90 секунд расскажите о нынешней и прошлой работе. Назовите обязанности, один конкретный результат, два навыка и одно сравнение. Если всё это есть без подсказки, практический результат темы достигнут.", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    p("Следующий шаг", H2),
    p("В теме 7.2 вы будете читать вакансию, заполнять основную анкету и задавать формальные вопросы об условиях работы.", SMALL),
]

doc.build(story)
print(OUTPUT)
