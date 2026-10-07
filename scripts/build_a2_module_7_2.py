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
OUTPUT = ROOT / "output/pdf/A2/Module_07/Slovak_A2_Tema_7_2_Vakansiya_anketa_i_usloviya_raboty.pdf"
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
        canvas.drawString(20 * mm, height - 12 * mm, "A2 7.2  |  Вакансия, анкета и условия работы")
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
    title="Slovak A2 - Тема 7.2 - Вакансия, анкета и условия работы",
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
    p("Вакансия, анкета и условия работы", TITLE),
    p("Pracovná ponuka, formulár a pracovné podmienky: понимаем объявление и вежливо уточняем детали", SUBTITLE),
    Spacer(1, 41 * mm),
    p("На уровне A2 важно быстро найти в вакансии практические сведения, без ошибок заполнить базовые поля и задать работодателю несколько ясных формальных вопросов."),
    p("После модуля вы сможете:", H2),
    table([
        ["1", "найти должность, обязанности и требования"],
        ["2", "понять график, место, оплату и дату начала"],
        ["3", "заполнить основную анкету кандидата"],
        ["4", "вежливо уточнить условия работы"],
    ], [12 * mm, 158 * mm], 7.2, False),
    Spacer(1, 3 * mm),
    box("<b>Маршрут:</b> читаю заголовки вакансии → отмечаю обязательные условия → заполняю только запрошенные данные → задаю 2-3 конкретных вопроса."),
    PageBreak(),

    p("1. Как читать вакансию", H1),
    p("Не переводите объявление слово за словом. Сначала найдите разделы и решите: подходит ли вам работа, соответствуете ли вы требованиям и какие детали нужно уточнить."),
    table([
        ["Раздел", "Что означает", "Пример"],
        ["pracovná pozícia", "должность", "administratívny pracovník / pracovníčka"],
        ["miesto výkonu práce", "место работы", "Bratislava, Ružinov"],
        ["náplň práce", "обязанности", "komunikácia s klientmi, evidencia objednávok"],
        ["požiadavky", "требования", "stredoškolské vzdelanie, práca s PC"],
        ["pracovný čas", "график", "pondelok až piatok, 8.00-16.00"],
        ["mzda", "оплата", "od 1 300 eur brutto mesačne"],
        ["termín nástupu", "дата начала", "ihneď / od 1. októbra / dohodou"],
        ["benefity", "дополнительные условия", "stravné, pružný pracovný čas"],
    ], [40 * mm, 49 * mm, 81 * mm], 5.25),
    p("Мини-вакансия", H2),
    box("<b>Hľadáme recepčnú / recepčného do menšieho hotela v centre Žiliny.</b> Náplň práce: komunikácia s hosťami, rezervácie a jednoduchá administratíva. Požadujeme znalosť angličtiny na úrovni B1 a prácu s počítačom. Pracovný čas je na zmeny. Nástup od 15. októbra alebo dohodou. Ponúkame mzdu od 1 200 eur brutto a stravné.", PALE, ROSE, SMALL),
    box("<b>Важно:</b> <i>od 1 300 eur brutto</i> означает исходную сумму до удержаний. В языковом задании достаточно понять формулировку; расчёт зарплаты не входит в эту тему.", CREAM, colors.HexColor("#E7C76C"), TINY),
    PageBreak(),

    p("2. Даты, Akuzatív и Lokál", H1),
    p("В вакансии Akuzatív часто показывает, <b>кого ищут</b> или <b>что нужно отправить и знать</b>. Lokál отвечает, <b>где</b> проходит работа или обучение."),
    table([
        ["Модель", "Пример", "Перевод"],
        ["hľadáme + A", "Hľadáme predavača / predavačku.", "Ищем продавца / продавщицу."],
        ["poslať + A", "Pošlite životopis a formulár.", "Пришлите резюме и анкету."],
        ["ovládať + A", "Ovládam angličtinu a Excel.", "Я владею английским и Excel."],
        ["pracovať v + L", "Práca je v novom sklade.", "Работа находится на новом складе."],
        ["pracovať na + L", "Pracujem na recepcii.", "Я работаю на ресепшене."],
        ["skúsenosti v + L", "Mám prax v administratíve.", "У меня есть опыт в администрировании."],
    ], [38 * mm, 69 * mm, 63 * mm], 5.55),
    p("Даты и срок начала", H2),
    table([
        ["Форма", "Пример", "Смысл"],
        ["od + даты", "Nástup je možný od 1. novembra 2026.", "начиная с 1 ноября 2026"],
        ["do + даты", "Pošlite žiadosť do 20. októbra.", "не позднее 20 октября"],
        ["ihneď", "Môžem nastúpiť ihneď.", "могу начать сразу"],
        ["dohodou", "Termín nástupu je dohodou.", "дата по договорённости"],
    ], [31 * mm, 80 * mm, 59 * mm], 5.55),
    box("<b>Русскоязычная ловушка:</b> <i>do 20. októbra</i> - срок до даты, а <i>od 20. októbra</i> - начало с даты. В названии месяца после числа употребляется Genitív: <i>októbra, novembra</i>.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    PageBreak(),

    p("3. Анкета и личные местоимения", H1),
    p("Базовая анкета кандидата обычно просит факты, а не длинный рассказ. Пишите кратко, правдиво и в том формате, который указан в поле."),
    table([
        ["Поле", "Что вписать", "Пример"],
        ["meno a priezvisko", "имя и фамилия", "Anna Petrova"],
        ["dátum narodenia", "дата рождения", "12. 4. 1995"],
        ["adresa", "улица, индекс, город", "Jarná 8, 010 01 Žilina"],
        ["telefón / e-mail", "контактные данные", "+421 ... / anna@example.com"],
        ["vzdelanie", "уровень и направление", "stredoškolské s maturitou"],
        ["prax", "период, место, должность", "2022-2025, hotel, recepčná"],
        ["jazykové znalosti", "язык и уровень", "angličtina B1, slovenčina A2"],
        ["termín nástupu", "когда можете начать", "od 1. novembra / dohodou"],
    ], [42 * mm, 59 * mm, 69 * mm], 5.15),
    p("Местоимения в рабочем контакте", H2),
    table([
        ["Кого / кому", "Фраза", "Перевод"],
        ["ma / mi", "Kontaktujte ma. Termín mi vyhovuje.", "Свяжитесь со мной. Срок мне подходит."],
        ["vás / vám", "Chcem sa vás opýtať. Pošlem vám formulár.", "Хочу вас спросить. Пришлю вам анкету."],
        ["nás / nám", "Pozvali nás. Poslali nám informácie.", "Нас пригласили. Нам прислали сведения."],
    ], [30 * mm, 77 * mm, 63 * mm], 5.55),
    box("<b>Формальный регистр:</b> к незнакомому работодателю обращайтесь на <i>vy</i>. В личном письме формы <b>Vás, Vám, Váš</b> часто пишут с прописной буквы как знак уважения.", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    PageBreak(),

    p("4. Вежливые вопросы об условиях", H1),
    p("Сначала представьтесь и назовите вакансию. Затем задайте один вопрос в одном предложении. Формулы с <i>chcel/a by som</i> и <i>mohli by ste</i> звучат мягче прямого требования."),
    table([
        ["Что уточнить", "Формальный вопрос", "Перевод"],
        ["график", "Aký je, prosím, pracovný čas?", "Какой график работы?"],
        ["смены", "Pracuje sa aj cez víkend?", "Работают ли также по выходным?"],
        ["место", "Kde presne je miesto výkonu práce?", "Где именно находится место работы?"],
        ["начало", "Kedy je možný nástup?", "Когда можно приступить?"],
        ["обязанности", "Mohli by ste spresniť náplň práce?", "Не могли бы вы уточнить обязанности?"],
        ["обучение", "Ponúkate zaškolenie?", "Предлагаете ли вы обучение на месте?"],
        ["оплата", "Aká je ponúkaná mzda?", "Какая предлагается зарплата?"],
    ], [31 * mm, 80 * mm, 59 * mm], 5.35),
    p("Мини-диалог по телефону", H2),
    box("<b>Uchádzačka:</b> Dobrý deň, volám sa Anna Petrova. Volám kvôli ponuke na pozíciu recepčnej.<br/><b>Zamestnávateľ:</b> Dobrý deň, nech sa páči.<br/><b>Uchádzačka:</b> Chcela by som sa opýtať, či sa pracuje aj cez víkend.<br/><b>Zamestnávateľ:</b> Áno, pracuje sa na dve zmeny, ale rozpis dostanete vopred.<br/><b>Uchádzačka:</b> Ďakujem. A kedy je možný nástup?<br/><b>Zamestnávateľ:</b> Od 15. októbra alebo dohodou.<br/><b>Uchádzačka:</b> Rozumiem, ďakujem za informácie. Dovidenia.", PALE, ROSE, SMALL),
    p("Короткое начало письма: <i>Dobrý deň, reagujem na Vašu ponuku na pozíciu administratívnej pracovníčky. V prílohe Vám posielam vyplnený formulár. Chcela by som sa opýtať na pracovný čas.</i>", TINY),
    PageBreak(),

    p("5. Банк фраз и упражнения", H1),
    table([
        ["SK", "RU"],
        ["Ponuka ma zaujala.", "Предложение меня заинтересовало."],
        ["Mám o túto pozíciu záujem.", "Меня интересует эта должность."],
        ["Spĺňam základné požiadavky.", "Я соответствую основным требованиям."],
        ["Formulár som vyplnila elektronicky.", "Я заполнила анкету электронно."],
        ["Životopis Vám posielam v prílohe.", "Резюме отправляю Вам во вложении."],
        ["Prosím, kontaktujte ma e-mailom.", "Пожалуйста, свяжитесь со мной по электронной почте."],
        ["Termín pohovoru mi vyhovuje.", "Время собеседования мне подходит."],
        ["Môžem nastúpiť od 1. novembra.", "Я могу приступить с 1 ноября."],
    ], [87 * mm, 83 * mm], 5.45),
    box("<b>Частые ошибки:</b> *zaujímam sa tú pozíciu* вместо <b>mám záujem o túto pozíciu</b>; *pracujem v recepcii* вместо <b>na recepcii</b>; путаница <b>od/do</b>; разговорное <i>Chcem vedieť...</i> вместо вежливого вопроса; лишние личные данные, которых анкета не просит.", CREAM, colors.HexColor("#E7C76C"), TINY),
    p("Упражнение 1. Найдите раздел вакансии", H2),
    p("Соотнесите: 1) náplň práce; 2) požiadavky; 3) pracovný čas; 4) termín nástupu. a) ihneď; b) angličtina B1; c) evidencia objednávok; d) 8.00-16.00.", TINY),
    p("Упражнение 2. Выберите od или do", H2),
    p("1) Pošlite formulár ___ 20. októbra. 2) Môžem nastúpiť ___ 1. novembra. 3) Ponuka platí ___ konca mesiaca.", TINY),
    p("Упражнение 3. Вставьте местоимение", H2),
    p("1) Prosím, kontaktujte ___. (я) 2) Pošlem ___ životopis. (Вы) 3) Termín ___ vyhovuje. (я) 4) Pozvali ___ na pohovor. (мы)", TINY),
    p("Упражнение 4. Исправьте ошибки", H2),
    p("1) Pracujem v recepcii. 2) Zaujímam sa túto pozíciu. 3) Chcem vedieť pracovný čas. 4) Nástup je do 1. novembra, то есть с 1 ноября.", TINY),
    p("Упражнение 5. Переведите", H2),
    p("1) Меня интересует эта должность. 2) Я могу приступить с 15 октября. 3) Не могли бы Вы уточнить обязанности? 4) Пришлю Вам заполненную анкету.", TINY),
    p("Упражнение 6. Мини-отклик", H2),
    p("Напишите 5-7 предложений: назовите вакансию, укажите два подходящих навыка, срок начала и задайте два вежливых вопроса. Используйте <i>Vám/Vás</i> и одну дату.", TINY),
    PageBreak(),

    p("6. Ответы и проверка мастерства", H1),
    p("Ответы", H2),
    p("<b>1.</b> 1-c; 2-b; 3-d; 4-a.", TINY),
    p("<b>2.</b> 1) <b>do</b> 20. októbra; 2) <b>od</b> 1. novembra; 3) <b>do</b> konca mesiaca.", TINY),
    p("<b>3.</b> 1) kontaktujte <b>ma</b>; 2) pošlem <b>Vám</b>; 3) <b>mi</b> vyhovuje; 4) pozvali <b>nás</b>.", TINY),
    p("<b>4.</b> 1) Pracujem <b>na recepcii</b>. 2) <b>Mám záujem o túto pozíciu</b>. 3) <b>Chcel/a by som sa opýtať na pracovný čas</b>. 4) Nástup je <b>od 1. novembra</b>.", TINY),
    p("<b>5.</b> Mám záujem o túto pozíciu. Môžem nastúpiť od 15. októbra. Mohli by ste spresniť náplň práce? Pošlem Vám vyplnený formulár.", TINY),
    p("<b>6. Модель:</b> Dobrý deň, reagujem na Vašu ponuku na pozíciu recepčnej. Mám skúsenosti s klientmi a viem pracovať s rezervačným programom. Môžem nastúpiť od 15. októbra. Chcela by som sa Vás opýtať, či sa pracuje aj cez víkend. Mohli by ste mi, prosím, povedať, či ponúkate zaškolenie? Vyplnený formulár Vám posielam v prílohe. Возможны другие естественные варианты.", TINY),
    p("Итог в четырёх пунктах", H2),
    table([
        ["OK", "Нахожу в вакансии обязанности, требования и условия."],
        ["OK", "Различаю od и do и читаю даты начала и срока."],
        ["OK", "Заполняю базовые поля кратко и правдиво."],
        ["OK", "Задаю формальные вопросы с Vám/Vás и условным наклонением."],
    ], [12 * mm, 158 * mm], 6.15, False),
    Spacer(1, 2 * mm),
    box("<b>Финальная проверка:</b> возьмите короткую вакансию и за 3 минуты выпишите должность, место, две обязанности, два требования, график, оплату и дату начала. Затем устно задайте два вежливых вопроса.", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    p("Следующий шаг", H2),
    p("В теме 7.3 вы будете договариваться о поручении, переносить встречу и передавать коллеге изменение плана.", SMALL),
]

doc.build(story)
print(OUTPUT)
