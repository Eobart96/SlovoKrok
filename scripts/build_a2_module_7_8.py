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
OUTPUT = ROOT / "output/pdf/A2/Module_07/Slovak_A2_Tema_7_8_Moya_strana_i_Slovakiya_informatsiya_dlya_gostya.pdf"
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
TITLE = ParagraphStyle("Title", fontName="Arial-Bold", fontSize=18.5, leading=21.5, textColor=colors.white, alignment=TA_LEFT, spaceAfter=4 * mm)
SUBTITLE = ParagraphStyle("Subtitle", fontName="Arial", fontSize=10.7, leading=13.5, textColor=colors.HexColor("#FFD8EB"), spaceAfter=5 * mm)
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
        canvas.drawString(20 * mm, height - 12 * mm, "A2 7.8  |  Моя страна и Словакия: информация для гостя")
    canvas.setFont("Arial", 8)
    canvas.setFillColor(MUTED)
    canvas.drawString(20 * mm, 9 * mm, "SlovoKrok | личный учебный модуль")
    canvas.drawRightString(width - 20 * mm, 9 * mm, f"стр. {page_number} / 7")
    canvas.restoreState()


doc = BaseDocTemplate(
    str(OUTPUT), pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=20 * mm, bottomMargin=18 * mm,
    title="Slovak A2 - Тема 7.8 - Моя страна и Словакия: информация для гостя", author="SlovoKrok",
)
doc.addPageTemplates([PageTemplate(id="series", frames=[Frame(20 * mm, 18 * mm, 170 * mm, 257 * mm, id="main", leftPadding=0, rightPadding=0)], onPage=draw_page)])


story = [
    p("A2 7.8  •  МОДУЛЬ 7  •  РАБОТА, ПУТЕШЕСТВИЯ И СТРАНА", KICK),
    p("Моя страна и Словакия: информация для гостя", TITLE),
    p("Moja krajina a Slovensko: vyberáme a odovzdávame hosťovi to hlavné", SUBTITLE),
    Spacer(1, 41 * mm),
    p("Медиация - это не дословный перевод. Вы читаете короткий источник, выбираете то, что нужно гостю, и передаёте смысл простыми словацкими фразами."),
    p("После модуля вы сможете:", H2),
    table([
        ["1", "найти в источнике кто, что, где и когда"],
        ["2", "передать главное из карты, прогноза, афиши и текста"],
        ["3", "упростить детали с niekto, niečo, niekde, niekoľko"],
        ["4", "уточнить культурное различие без категоричности"],
    ], [12 * mm, 158 * mm], 7.2, False),
    Spacer(1, 3 * mm),
    box("<b>Формула:</b> источник - потребность гостя - кто/что/где/когда - простое сообщение - уточнение."),
    PageBreak(),

    p("1. Не переводим всё: выбираем главное", H1),
    p("Сначала определите, что нужно гостю. Затем найдите четыре опоры: <b>kto, čo, kde, kedy</b>. Добавьте только одну полезную деталь: цену, транспорт, погоду или правило."),
    table([
        ["Вопрос", "Что искать", "Простая передача"],
        ["Kto?", "организатор, участник", "Podujatie organizuje mesto."],
        ["Čo?", "событие, место, предупреждение", "Je to večerný koncert."],
        ["Kde?", "город, площадь, зал, маршрут", "Koná sa na Hlavnom námestí."],
        ["Kedy?", "дата и время", "Začína sa v sobotu o šiestej."],
        ["Pre koho?", "кому это подходит", "Je to vhodné aj pre rodiny."],
        ["Čo treba?", "билет, одежда, бронь", "Treba si kúpiť lístok vopred."],
    ], [24 * mm, 58 * mm, 88 * mm], 5.65),
    p("От источника к сообщению", H2),
    table([
        ["Источник", "Главное для гостя", "Что можно опустить"],
        ["карта", "куда идти, ориентир, время пути", "все названия улиц"],
        ["прогноз", "температура, осадки, практический совет", "почасовые цифры"],
        ["афиша", "что, где, когда, цена/вход", "имена всех участников"],
        ["культурный текст", "значение обычая и поведение гостя", "длинную историю"],
    ], [32 * mm, 72 * mm, 66 * mm], 5.8),
    box("<b>Важно:</b> не добавляйте факты от себя. Если деталь неясна, скажите <i>Nie som si istý/istá, radšej to overíme.</i> - Я не уверен/уверена, лучше проверим.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    PageBreak(),

    p("2. Даты, время и место", H1),
    p("В афише дата часто записана цифрами, но гостю удобнее услышать её словами. После порядкового числительного используется родительный падеж названия месяца: <i>piateho mája, dvadsiateho prvého júna</i>."),
    table([
        ["В источнике", "Говорим", "Перевод"],
        ["5. 5.", "Podujatie bude piateho mája.", "Мероприятие будет пятого мая."],
        ["21. 6.", "Koncert je dvadsiateho prvého júna.", "Концерт двадцать первого июня."],
        ["18:00", "Začína sa o osemnástej.", "Начинается в 18:00."],
        ["9:30-12:00", "Trvá od pol desiatej do dvanástej.", "Длится с 9:30 до 12:00."],
        ["sobota", "Stretneme sa v sobotu.", "Встретимся в субботу."],
        ["centrum mesta", "Je to v centre mesta.", "Это в центре города."],
    ], [30 * mm, 78 * mm, 62 * mm], 5.55),
    p("Учебная афиша", H2),
    box("<b>LETNÝ DEŇ V MESTE</b><br/>sobota 21. 6., 15:00-21:00<br/>Námestie slobody<br/>hudba, tvorivé dielne, miestne jedlá<br/>vstup voľný; pri daždi program v kultúrnom dome", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    p("Передаём гостю", H2),
    box("V sobotu dvadsiateho prvého júna bude na Námestí slobody mestské podujatie. Začína sa o tretej popoludní a vstup je voľný. Bude tam hudba, niekoľko dielní a miestne jedlá. Ak bude pršať, program sa presunie do kultúrneho domu.", PALE, ROSE, SMALL),
    box("<b>Не путайте:</b> <i>v sobotu</i> - в субботу; <i>od soboty</i> - с субботы; <i>do soboty</i> - до субботы.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    PageBreak(),

    p("3. Упрощаем с неопределёнными местоимениями", H1),
    p("Когда точная деталь гостю не нужна или источник говорит обобщённо, используйте неопределённые слова. Они помогают сократить текст, но не дают права заменять неизвестный факт выдумкой."),
    table([
        ["Слово", "Значение", "Пример"],
        ["niekto", "кто-то", "Niekto z organizátorov vám poradí."],
        ["niečo", "что-то", "Môžete tam ochutnať niečo miestne."],
        ["niekde", "где-то", "Autobus zastavuje niekde pri stanici."],
        ["niekedy", "когда-нибудь / иногда", "V horách sa počasie niekedy rýchlo mení."],
        ["nejaký", "какой-то / некоторый", "Budete potrebovať nejakú nepremokavú bundu."],
        ["niekoľko", "несколько", "Program ponúka niekoľko krátkych prehliadok."],
    ], [30 * mm, 48 * mm, 92 * mm], 5.55),
    p("Сжимаем, сохраняя смысл", H2),
    table([
        ["Подробный источник", "Простое сообщение гостю"],
        ["Na trhu bude pätnásť stánkov s výrobkami...", "Na trhu bude niekoľko stánkov s miestnymi výrobkami."],
        ["Prehliadky vedú pani Nováková a pán Kováč...", "Niekto zo sprievodcov vás vezme na prehliadku."],
        ["O 14:00, 15:30 a 17:00 vystúpia tri skupiny...", "Popoludní bude niekoľko hudobných vystúpení."],
    ], [78 * mm, 92 * mm], 5.5),
    p("Полезные связки", H2),
    box("<i>Pre vás je dôležité, že...</i> - Для вас важно, что...<br/><i>Stručne povedané...</i> - Коротко говоря...<br/><i>To znamená, že...</i> - Это значит, что...<br/><i>Presný čas ešte radšej overíme.</i> - Точное время лучше ещё проверим.", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    PageBreak(),

    p("4. Четыре источника и культурное уточнение", H1),
    table([
        ["Источник", "Фрагмент", "Что сказать гостю"],
        ["карта", "stanica - centrum: električka 4, 12 min", "Do centra ide električka číslo štyri. Cesta trvá asi dvanásť minút."],
        ["прогноз", "Tatry: 8 °C, dážď, silný vietor", "V Tatrách bude chladno, dážď a silný vietor. Vezmite si teplú nepremokavú bundu."],
        ["афиша", "Múzeum: nedeľa 10:00, vstup zdarma", "V nedeľu je vstup do múzea zdarma. Múzeum sa otvára o desiatej."],
        ["текст", "Pri návšteve domácnosti si hostia často vyzúvajú topánky.", "V slovenskej domácnosti sa hostia často vyzúvajú. Ak si nie ste istý, opýtajte sa."],
    ], [27 * mm, 64 * mm, 79 * mm], 5.25),
    p("Межкультурное уточнение", H2),
    p("Не говорите, что все люди ведут себя одинаково. Смягчайте: <i>často, zvyčajne, môže sa stať</i>. Дайте гостю безопасный способ уточнить правило."),
    table([
        ["Категорично", "Лучше"],
        ["Na Slovensku sa vždy vyzúva.", "V domácnosti sa hostia často vyzúvajú."],
        ["Musíte priniesť darček.", "Malý darček môže byť milý, ale nie je vždy potrebný."],
        ["Obed je presne o dvanástej.", "Čas obeda sa môže líšiť, radšej sa opýtajte."],
    ], [70 * mm, 100 * mm], 5.65),
    p("Мини-диалог", H2),
    box("<b>Hosť:</b> Môžem ísť na hrad pešo?<br/><b>Vy:</b> Podľa mapy je to z centra asi dvadsať minút pešo, ale cesta ide do kopca.<br/><b>Hosť:</b> A čo bude večer?<br/><b>Vy:</b> Na námestí bude nejaký koncert. Začína sa o siedmej, no presný program ešte overíme.<br/><b>Hosť:</b> Mám si priniesť hotovosť?<br/><b>Vy:</b> Pre istotu áno. Pri niektorých stánkoch sa možno nedá platiť kartou.", PALE, ROSE, SMALL),
    p("Все источники на этой странице - учебные модели; перед реальной поездкой проверьте актуальные данные.", TINY),
    PageBreak(),

    p("5. Частые ошибки и упражнения", H1),
    table([
        ["Ошибка", "Правильно", "Почему"],
        ["*Koncert je na 21. júna.", "Koncert je 21. júna.", "дата без na"],
        ["*Začína v šiestej.", "Začína sa o šiestej.", "o + время; возвратный глагол"],
        ["*Niekto podujatie", "nejaké podujatie", "niekto - человек, nejaký - признак"],
        ["*Všetci Slováci vždy...", "Na Slovensku ľudia často...", "не делайте абсолютных выводов"],
        ["*Asi určite prší.", "Asi bude pršať.", "не соединяйте сомнение и уверенность"],
    ], [54 * mm, 64 * mm, 52 * mm], 5.0),
    p("Упражнение 1. Найдите четыре опоры", H2),
    p("Афиша: <i>Jarný trh, Mestský park, nedeľa 14. apríla, 10:00-16:00, vstup voľný.</i> Запишите kto/čo, kde, kedy и цену.", SMALL),
    p("Упражнение 2. Скажите дату и время словами", H2),
    p("1) 3. 8., 18:00; 2) 12. 10., 9:30; 3) sobota, 7:00-11:00.", SMALL),
    p("Упражнение 3. Замените детали", H2),
    p("Используйте <i>niekto, niečo, niekde, niekoľko</i>: 1) Päť sprievodcov poradí. 2) Tri jedlá sú miestne. 3) Štyri zastávky sú pri centre. 4) Program má šesť dielní.", SMALL),
    p("Упражнение 4. Передайте прогноз", H2),
    p("Источник: <i>Košice, sobota: 24 °C, popoludní búrky, vietor.</i> Скажите гостю 2 фразы: главное и практический совет.", SMALL),
    p("Упражнение 5. Смягчите культурное правило", H2),
    p("Переформулируйте: <i>Na Slovensku sa vždy vyzúva. Každý obeduje o dvanástej.</i> Используйте <i>často, zvyčajne, môže sa líšiť</i>.", SMALL),
    p("Упражнение 6. Медиация для гостя", H2),
    p("Выберите реальную карту, прогноз, афишу или короткий текст о своей стране. Передайте гостю 5-6 фраз: что, где, когда, одна полезная деталь, совет и одно осторожное уточнение.", SMALL),
    PageBreak(),

    p("6. Ответы и проверка мастерства", H1),
    p("Ответы", H2),
    table([
        ["№", "Ключ"],
        ["1", "Čo: Jarný trh; kde: v Mestskom parku; kedy: v nedeľu 14. apríla od 10:00 do 16:00; vstup je voľný."],
        ["2", "1 tretieho augusta o šiestej; 2 dvanásteho októbra o pol desiatej; 3 v sobotu od siedmej do jedenástej."],
        ["3", "1 Niekto zo sprievodcov poradí. 2 Môžete ochutnať niečo miestne. 3 Autobus stojí niekde pri centre. 4 Program má niekoľko dielní."],
        ["4", "V Košiciach bude v sobotu teplo, ale popoludní môžu prísť búrky a môže fúkať vietor. Vezmite si ľahkú bundu alebo dáždnik."],
        ["5", "V slovenských domácnostiach sa hostia často vyzúvajú. Čas obeda sa môže líšiť, preto sa radšej opýtajte."],
        ["6", "Возможны разные ответы; проверьте источник, 5-6 простых фраз, совет и осторожное уточнение."],
    ], [13 * mm, 157 * mm], 5.0),
    p("Модель самостоятельного ответа", H2),
    box("Podľa programu bude v sobotu v centre mesta kultúrny deň. Začína sa o tretej popoludní a vstup je voľný. Bude tam niekoľko koncertov a môžete ochutnať niečo miestne. Z hotela sa tam dostanete električkou asi za desať minút. Večer môže pršať, preto si vezmite dáždnik. Niektoré stánky možno neprijímajú karty, takže pre istotu majte aj hotovosť. Presný čas posledného koncertu ešte radšej overíme.", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    p("Финальная проверка", H2),
    table([
        ["Могу...", "Да / ещё раз"],
        ["найти кто, что, где и когда", "□ / □"],
        ["сказать дату и время словами", "□ / □"],
        ["сжать детали без искажения", "□ / □"],
        ["дать гостю практический совет", "□ / □"],
        ["осторожно уточнить культурное правило", "□ / □"],
    ], [128 * mm, 42 * mm], 5.65),
    box("<b>Критерий освоения:</b> не менее 5 из 6 упражнений без подсказки и устное сообщение из 5-6 фраз, где есть источник, главное, совет и корректное уточнение.", PALE, ROSE, SMALL),
]

doc.build(story)
print(OUTPUT)
