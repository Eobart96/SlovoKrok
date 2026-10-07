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
OUTPUT = ROOT / "output" / "pdf" / "A2" / "Module_01" / "Slovak_A2_Tema_1_6_Svyaznost_i_akcent.pdf"
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
TITLE = ParagraphStyle("Title", fontName="Arial-Bold", fontSize=22, leading=26, textColor=colors.white, alignment=TA_LEFT, spaceAfter=5 * mm)
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


def bullet(text):
    return p(f"<font color='#CE3C92'>●</font> {text}", BODY)


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
        canvas.drawString(20 * mm, height - 12 * mm, "SLOVAK A2  |  ТЕМА 1.6")
        canvas.drawRightString(width - 20 * mm, height - 12 * mm, "Связность и смысловой акцент")
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
    title="Slovak A2 - Тема 1.6 - Связность: тема, новая информация и смысловой акцент", author="SlovoKrok",
)
frame = Frame(20 * mm, 18 * mm, 170 * mm, 257 * mm, id="main", leftPadding=0, rightPadding=0)
doc.addPageTemplates([PageTemplate(id="series", frames=[frame], onPage=draw_page)])

story = [
    p("МОДУЛЬ 1  •  ПЕРЕХОД ОТ A1 К A2", COVER_KICKER),
    p("Связность: тема,<br/>новая информация<br/>и смысловой акцент", TITLE),
    p("Téma, nová informácia a dôraz", SUBTITLE),
    Spacer(1, 24 * mm),
    p("На A2 отдельные правильные предложения нужно соединять в понятное сообщение. Порядок слов показывает, от чего вы отталкиваетесь и что сообщаете как главное.", BODY),
    p("После модуля вы сможете:", H2),
    styled_table([
        ["1", "различать тему сообщения и новую информацию"],
        ["2", "менять порядок слов ради понятного смыслового акцента"],
        ["3", "связывать предложения местоимениями, повтором и связками"],
        ["4", "строить короткий связный текст без скачков и двусмысленности"],
    ], [12 * mm, 158 * mm], font_size=8.3, header=False),
    Spacer(1, 4 * mm),
    box("<b>Нейтральная формула:</b> известное -> новое. Следующее предложение подхватывает уже названную тему и добавляет следующий шаг.", PALE, PINK),
    PageBreak(),

    p("1. Тема и новая информация", H1),
    p("<b>Тема</b> - то, от чего мы отталкиваемся. <b>Новая информация</b>, или <b>рема</b>, - то, что слушатель должен узнать. В нейтральном сообщении известная часть обычно появляется раньше, а новая - позже.", BODY),
    styled_table([
        ["Контекст или вопрос", "Естественный ответ", "Тема -> новое"],
        ["Kto prišiel?<br/>Кто пришёл?", "Prišla <b>nová kolegyňa</b>.<br/>Пришла новая коллега.", "всё сообщение новое; главное в конце"],
        ["Čo urobila kolegyňa?<br/>Что сделала коллега?", "Kolegyňa <b>poslala správu</b>.<br/>Коллега отправила сообщение.", "kolegyňa -> poslala správu"],
        ["Kedy poslala správu?<br/>Когда она отправила сообщение?", "Správu poslala <b>ráno</b>.<br/>Сообщение она отправила утром.", "správa -> ráno"],
        ["Kam pôjdeme zajtra?<br/>Куда мы пойдём завтра?", "Zajtra pôjdeme <b>do múzea</b>.<br/>Завтра мы пойдём в музей.", "zajtra -> do múzea"],
        ["Čo je na stole?<br/>Что на столе?", "Na stole je <b>nový formulár</b>.<br/>На столе лежит новый бланк.", "na stole -> nový formulár"],
    ], [42 * mm, 77 * mm, 51 * mm], font_size=7.1),
    Spacer(1, 4 * mm),
    box("<b>Учебное упрощение:</b> новое часто стоит ближе к концу, но это не механическое правило. Контекст, контраст и интонация могут изменить порядок.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    p("Проверка вопросом", H2),
    bullet("Задайте вопрос к главному новому фрагменту."),
    bullet("Поставьте известную опору раньше, а ответ на вопрос - ближе к концу."),
    PageBreak(),

    p("2. Порядок слов меняет акцент", H1),
    p("Словацкий порядок слов относительно свободен, потому что формы слов показывают их грамматическую роль. Но перестановка не случайна: она должна отвечать контексту и выделять нужную часть.", BODY),
    styled_table([
        ["Что хотим выделить", "Словацкий ответ", "Перевод"],
        ["нейтральное событие", "Peter kúpil lístok online.", "Петер купил билет онлайн."],
        ["кто купил билет?", "Lístok kúpil <b>Peter</b>, nie Martin.", "Билет купил Петер, а не Мартин."],
        ["что купил Петер?", "Peter kúpil <b>lístok</b>, nie rezerváciu.", "Петер купил билет, а не бронь."],
        ["как он купил билет?", "Lístok kúpil <b>online</b>.", "Билет он купил онлайн."],
        ["когда он позвонит?", "Peter zavolá <b>večer</b>.", "Петер позвонит вечером."],
        ["именно завтра", "Prídem <b>zajtra</b>, nie dnes.", "Я приду завтра, не сегодня."],
    ], [42 * mm, 67 * mm, 61 * mm], font_size=7.15),
    p("Вынос в начало", H2),
    styled_table([
        ["Начальная опора", "Пример", "Что происходит"],
        ["объект", "Túto knihu som už čítal.", "Эту книгу я уже читал: книга известна."],
        ["место", "V Bratislave býva moja sestra.", "В Братиславе живёт моя сестра: место задаёт рамку."],
        ["время", "V pondelok začíname nový kurz.", "В понедельник мы начинаем новый курс: время задаёт рамку."],
    ], [35 * mm, 65 * mm, 70 * mm], font_size=7.15),
    Spacer(1, 3 * mm),
    box("<b>Опора на PDF 1.3:</b> при выносе темы короткие клитики сохраняют своё грамматическое место: <b>Túto správu som mu už poslal.</b> Здесь меняется тема, а не правило расположения клитик.", PALE, PINK, SMALL),
    PageBreak(),

    p("3. Как связать предложения", H1),
    p("Связный текст не повторяет каждое существительное полностью, но и не заставляет читателя угадывать, к чему относится местоимение.", BODY),
    styled_table([
        ["Средство", "Схема", "Связный пример"],
        ["точный повтор", "новое слово -> то же слово", "Mária našla <b>kurz</b>. <b>Kurz</b> sa začína v pondelok."],
        ["местоимение", "существительное -> местоимение", "Mária našla kurz. Prihlásila sa <b>naň</b>."],
        ["пропуск субъекта", "имя -> понятный субъект", "Mária pracuje a večer <b>študuje</b>."],
        ["связка", "факт -> отношение -> результат", "Kurz je večer, <b>preto</b> sa Mária prihlásila."],
    ], [33 * mm, 63 * mm, 74 * mm], font_size=7.05),
    p("Полезные связки", H2),
    styled_table([
        ["Функция", "Слова", "Пример и перевод"],
        ["последовательность", "najprv, potom, nakoniec", "Najprv zavolám, potom napíšem. - Сначала позвоню, потом напишу."],
        ["причина", "pretože", "Zostanem doma, pretože som chorý. - Я останусь дома, потому что болен."],
        ["следствие", "preto", "Som chorý, preto zostanem doma. - Я болен, поэтому останусь дома."],
        ["контраст", "ale", "Kurz je náročný, ale užitočný. - Курс трудный, но полезный."],
        ["добавление", "aj, navyše", "Kurz je lacný a navyše je online. - Курс дешёвый и вдобавок проходит онлайн."],
        ["пример", "napríklad", "Cvičím každý deň, napríklad cestou do práce. - Я занимаюсь каждый день, например по дороге на работу."],
    ], [36 * mm, 43 * mm, 91 * mm], font_size=6.9),
    Spacer(1, 3 * mm),
    box("<b>Избегайте двусмысленности:</b> <i>Anna povedala Márii, že príde.</i> Неясно, кто придёт. Если это важно, используйте прямую речь: <b>Anna povedala Márii: &quot;Prídem.&quot;</b>", CREAM, colors.HexColor("#E7C76C"), SMALL),
    PageBreak(),

    p("4. От предложений к тексту", H1),
    p("Хорошая цепочка движется так: вводит объект, подхватывает его, добавляет причину или контраст и завершает личным результатом.", BODY),
    p("Модель текста", H2),
    box("<b>V našom meste otvorili nové jazykové centrum.</b> Centrum ponúka večerný kurz slovenčiny. Kurz sa začína v októbri, preto sa naň chcem prihlásiť. Učím sa už rok, ale pri hovorení ešte robím chyby. Najviac potrebujem precvičiť rozhovory v práci. Po kurze by som chcel hovoriť istejšie.<br/><br/><b>Перевод:</b> В нашем городе открыли новый языковой центр. Центр предлагает вечерний курс словацкого. Курс начинается в октябре, поэтому я хочу на него записаться. Я учусь уже год, но в речи всё ещё делаю ошибки. Больше всего мне нужно потренировать разговоры на работе. После курса я хотел бы говорить увереннее.", ALT, ROSE, SMALL),
    p("Почему текст держится вместе", H2),
    styled_table([
        ["Шаг", "Опора", "Новая информация"],
        ["1", "v našom meste", "nové jazykové centrum"],
        ["2", "centrum", "večerný kurz slovenčiny"],
        ["3", "kurz -> naň", "začiatok a rozhodnutie"],
        ["4", "učím sa", "контраст через ale"],
        ["5", "моё обучение", "главная потребность"],
        ["6", "po kurze", "желаемый результат"],
    ], [20 * mm, 63 * mm, 87 * mm], font_size=7.15),
    p("Мини-диалог: меняем акцент", H2),
    box("<b>A:</b> Kto otvoril nové centrum?<br/><b>B:</b> Nové centrum otvorilo <b>mesto</b>.<br/><b>A:</b> A čo tam ponúkajú?<br/><b>B:</b> Ponúkajú tam <b>večerný kurz slovenčiny</b>.<br/><b>A:</b> Kedy sa kurz začína?<br/><b>B:</b> Kurz sa začína <b>v októbri</b>.", PALE, ROSE, SMALL),
    PageBreak(),

    p("5. Частые ошибки и упражнения", H1),
    box("<b>Три ошибки:</b> начинать каждую фразу с нового объекта; повторять полное существительное в каждой строке; переставлять слова без контекста и ломать положение клитик.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    p("Упражнение 1. Найдите тему и новое", H2),
    p("Определите известную опору и главный новый фрагмент: 1) Kurz sa začína v pondelok. 2) Na stole je nový formulár. 3) Správu poslala Mária.", SMALL),
    p("Упражнение 2. Ответьте с нужным акцентом", H2),
    p("Расставьте слова: 1) Kto kúpil lístok? (lístok / Peter / kúpil) 2) Kedy príde Anna? (Anna / večer / príde) 3) Kde býva tvoja sestra? (v Košiciach / moja sestra / býva)", SMALL),
    p("Упражнение 3. Свяжите без лишнего повтора", H2),
    p("1) Eva našla kurz. Eva sa prihlásila na kurz. 2) Tomáš pracuje. Tomáš večer študuje. 3) Kúpil som knihu. Kniha je veľmi užitočná.", SMALL),
    p("Упражнение 4. Выберите связку", H2),
    p("1) Som chorý, preto / pretože zostanem doma. 2) Zostanem doma, preto / pretože som chorý. 3) Kurz je náročný, ale / potom užitočný. 4) Najprv zavolám, ale / potom napíšem.", SMALL),
    p("Упражнение 5. Исправьте", H2),
    p("1) Včera ja som mu správu poslal. 2) Mária ukázala Eve nový kurz. Prihlásila sa naň. (Уточните: записалась Ева.) 3) Anna povedala Zuzane, že dostala prácu. (Уточните: работу получила Анна.)", SMALL),
    p("Упражнение 6. Свой связный текст", H2),
    p("Напишите 6-7 предложений о курсе, поездке или рабочей задаче. Введите тему, подхватите её местоимением или повтором, добавьте причину, контраст и итог.", SMALL),
    PageBreak(),

    p("6. Ответы и проверка мастерства", H1),
    p("Ответы", H2),
    p("<b>1.</b> 1) тема: kurz; новое: v pondelok. 2) тема-рамка: na stole; новое: nový formulár. 3) тема: správa; новое и контрастный акцент: Mária.", TINY),
    p("<b>2.</b> 1) Lístok kúpil Peter. 2) Anna príde večer. 3) Moja sestra býva v Košiciach.", TINY),
    p("<b>3.</b> 1) Eva našla kurz a prihlásila sa naň. 2) Tomáš pracuje a večer študuje. 3) Kúpil som knihu. Je veľmi užitočná.", TINY),
    p("<b>4.</b> 1) preto; 2) pretože; 3) ale; 4) potom.", TINY),
    p("<b>5.</b> 1) Včera som mu poslal správu. 2) Mária ukázala Eve nový kurz. <i>Eva</i> sa naň prihlásila. 3) Anna povedala Zuzane: <i>&quot;Dostala som prácu.&quot;</i>", TINY),
    p("<b>6. Возможный ответ:</b> V práci máme nový projekt. Projekt sa začína v pondelok, preto dnes pripravujem plán. Kolega mi pošle údaje a ja ich skontrolujem. Úloha je náročná, ale zaujímavá. Najprv dokončíme rozpočet, potom zavoláme klientovi. Nakoniec mu pošleme hotový návrh.", TINY),
    p("Итог в четырёх пунктах", H2),
    styled_table([
        ["OK", "Я отличаю известную тему от новой информации."],
        ["OK", "Я меняю порядок слов только ради понятного акцента."],
        ["OK", "Я связываю фразы повтором, местоимением и связкой."],
        ["OK", "Я сохраняю правила клитик, когда выношу тему в начало."],
    ], [12 * mm, 158 * mm], font_size=7.8, header=False),
    Spacer(1, 3 * mm),
    box("<b>Финальная проверка:</b> прочитайте свой текст без исходного задания. Если местоимения однозначны, каждое предложение подхватывает предыдущее, а главное легко назвать, текст связный.", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    p("Следующий шаг", H2),
    p("В PDF 1.7 вы перенесёте эту связность в речь: потренируете ритм, группы согласных, оглушение и озвончение, долготу и интонацию более длинной фразы.", SMALL),
]

doc.build(story)
print(OUTPUT)
