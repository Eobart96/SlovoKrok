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
OUTPUT = ROOT / "output/pdf/A2/Module_06/Slovak_A2_Tema_6_3_Bytovaya_problema_i_dogovorennost.pdf"
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
        canvas.drawString(20 * mm, height - 12 * mm, "A2 6.3  |  Бытовая проблема и договорённость")
    canvas.setFont("Arial", 8)
    canvas.setFillColor(MUTED)
    canvas.drawString(20 * mm, 9 * mm, "SlovoKrok | личный учебный модуль")
    canvas.drawRightString(width - 20 * mm, 9 * mm, f"стр. {page_number} / 7")
    canvas.restoreState()


doc = BaseDocTemplate(
    str(OUTPUT), pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm,
    topMargin=20 * mm, bottomMargin=18 * mm,
    title="Slovak A2 - Тема 6.3 - Бытовая проблема и договорённость",
    author="SlovoKrok",
)
doc.addPageTemplates([
    PageTemplate(id="series", frames=[Frame(20 * mm, 18 * mm, 170 * mm, 257 * mm, id="main", leftPadding=0, rightPadding=0)], onPage=draw_page)
])


story = [
    p("МОДУЛЬ 6  •  ДОМ, ИНТЕРНЕТ И ПОКУПКИ", KICK),
    p("Бытовая проблема и<br/>договорённость", TITLE),
    p("Porucha a dohoda: объясняем, просим, согласуем и передаём решение", SUBTITLE),
    Spacer(1, 41 * mm),
    p("При бытовой проблеме важно дать владельцу или мастеру достаточно фактов: что именно не работает, когда это началось, что уже проверено и когда вы будете дома. Затем нужно точно передать договорённость соседу."),
    p("После модуля вы сможете:", H2),
    table([
        ["1", "понятно описать неисправность и её последствия"],
        ["2", "попросить о помощи вежливо и конкретно"],
        ["3", "согласовать время визита и следующий шаг"],
        ["4", "передать соседу решение владельца через že"],
    ], [12 * mm, 158 * mm], 7.2, False),
    Spacer(1, 3 * mm),
    box("<b>Формула сообщения:</b> проблема + место и время + уже сделанное + просьба + доступное время + подтверждённое решение."),
    PageBreak(),

    p("1. Что случилось и где", H1),
    p("Начните с наблюдаемого факта. Не пытайтесь ставить технический диагноз, если вы его не знаете: <i>voda tečie</i> полезнее, чем неточное объяснение причины."),
    table([
        ["Проблема", "Естественная фраза", "Перевод"],
        ["вода", "Z kohútika kvapká voda.", "Из крана капает вода."],
        ["отопление", "Kúrenie nefunguje.", "Отопление не работает."],
        ["стиральная машина", "Práčka sa pokazila.", "Стиральная машина сломалась."],
        ["электричество", "V kuchyni nejde elektrina.", "На кухне нет электричества."],
        ["окно", "Okno sa nedá zavrieť.", "Окно не закрывается."],
        ["потолок", "Zo stropu zateká.", "С потолка протекает вода."],
    ], [34 * mm, 70 * mm, 66 * mm], 5.65),
    p("Добавляем точные детали", H2),
    table([
        ["Вопрос", "Пример ответа"],
        ["Kde?", "Problém je v kúpeľni pri umývadle."],
        ["Odkedy?", "Začalo sa to včera večer."],
        ["Ako často?", "Voda kvapká stále."],
        ["Čo ste urobili?", "Zatvoril som hlavný ventil."],
        ["Aký je následok?", "Na podlahe je voda."],
    ], [34 * mm, 136 * mm], 6.0),
    box("<b>Безопасность:</b> при запахе газа, дыме, искрах или быстро прибывающей воде сначала действуйте по экстренным правилам дома и вызывайте соответствующую службу. Учебный диалог не заменяет реальную аварийную инструкцию.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    PageBreak(),

    p("2. Вид и следующий результат", H1),
    p("Несовершенный вид описывает процесс или повтор, совершенный - один результат. В договорённости обычно нужны оба: что происходит сейчас и что конкретно будет сделано."),
    table([
        ["Процесс / повтор", "Результат", "Пример"],
        ["opravovať", "opraviť", "Technik bude opravovať kotol. / Technik kotol opraví."],
        ["kontrolovať", "skontrolovať", "Majiteľ kontroluje ventil. / Majiteľ ventil skontroluje."],
        ["volať", "zavolať", "Volám správcovi. / Zavolám správcovi."],
        ["posielať", "poslať", "Posielam fotografiu. / Pošlem fotografiu."],
        ["meniť", "vymeniť", "Menia tesnenie. / Vymenia tesnenie."],
    ], [52 * mm, 44 * mm, 74 * mm], 5.45),
    p("Будущее в договорённости", H2),
    table([
        ["Функция", "Пример", "Перевод"],
        ["процесс", "Technik bude kontrolovať kúrenie.", "Мастер будет проверять отопление."],
        ["результат", "Technik príde a kotol opraví.", "Мастер придёт и починит котёл."],
        ["доступность", "Zajtra budem doma po tretej.", "Завтра я буду дома после трёх."],
        ["обещание", "Pošlem vám fotografiu.", "Я пришлю вам фотографию."],
    ], [34 * mm, 71 * mm, 65 * mm], 5.8),
    box("<b>Смысловой контраст:</b> <i>Technik bude opravovať práčku</i> говорит о процессе. <i>Technik práčku opraví</i> обещает ожидаемый результат, но не обязательно сообщает длительность работы.", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    PageBreak(),

    p("3. Просьба, инструкция и время", H1),
    p("Императив удобен для короткой инструкции. Условная форма делает просьбу мягче, особенно в общении с владельцем, управляющим или незнакомым мастером."),
    table([
        ["Функция", "Пример", "Перевод"],
        ["инструкция", "Vypnite, prosím, práčku.", "Пожалуйста, выключите стиральную машину."],
        ["запрет", "Neotvárajte hlavný ventil.", "Не открывайте главный вентиль."],
        ["просьба", "Mohli by ste poslať technika?", "Не могли бы вы прислать мастера?"],
        ["вариант", "Bolo by možné prísť zajtra?", "Можно было бы прийти завтра?"],
        ["уточнение", "Dajte mi, prosím, vedieť čas.", "Сообщите мне, пожалуйста, время."],
    ], [33 * mm, 72 * mm, 65 * mm], 5.7),
    p("Согласуем визит", H2),
    table([
        ["Шаг", "Готовая фраза"],
        ["предложить", "Môžem byť doma v stredu od štvrtej."],
        ["уточнить", "Vyhovuje vám čas medzi štvrtou a šiestou?"],
        ["изменить", "O piatej nemôžem. Mohli by sme sa dohodnúť na šiestej?"],
        ["подтвердить", "Dobre, platí streda o šiestej."],
        ["контакт", "Technik mi pred príchodom zavolá."],
    ], [32 * mm, 138 * mm], 5.9),
    p("Мини-диалог", H2),
    box("<b>Nájomník:</b> Dobrý deň, v kúpeľni nám tečie voda spod umývadla. Mohli by ste poslať technika?<br/><b>Majiteľ:</b> Áno. Môže prísť zajtra medzi treťou a piatou.<br/><b>Nájomník:</b> O tretej ešte nie som doma. Bolo by možné prísť o štvrtej?<br/><b>Majiteľ:</b> Dobre, technik príde o štvrtej a pred príchodom vám zavolá.<br/><b>Nájomník:</b> Ďakujem, platí.", PALE, ROSE, SMALL),
    PageBreak(),

    p("4. Передаём решение через že", H1),
    p("После разговора передайте только подтверждённые факты. Союз <b>že</b> вводит содержание сообщения; лицо и время меняются по ситуации."),
    table([
        ["Исходное сообщение", "Передача соседу"],
        ["Technik príde o štvrtej.", "Majiteľ povedal, že technik príde o štvrtej."],
        ["Pred príchodom vám zavolá.", "Napísal, že nám technik pred príchodom zavolá."],
        ["Neotvárajte hlavný ventil.", "Prosil nás, aby sme neotvárali hlavný ventil."],
        ["Pošlite mi fotografiu.", "Požiadal ma, aby som mu poslal fotografiu."],
    ], [72 * mm, 98 * mm], 5.75),
    p("Устная медиация", H2),
    box("<b>Ahoj, hovoril som s majiteľom.</b> Povedal, že technik príde zajtra o štvrtej a pred príchodom nám zavolá. Dovtedy nemáme otvárať hlavný ventil. Poslal som mu fotografiu a potvrdil som, že budem doma. Ak technik zavolá tebe, prosím, povedz mu, že problém je pod umývadlom.", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    p("Письменная медиация", H2),
    box("<b>Správa susedke:</b> Majiteľ potvrdil návštevu technika na stredu o 18.00. Technik skontroluje kúrenie vo všetkých izbách. Prosím, nechaj otvorené dvere do spálne. Ak sa oneskorí, majiteľ nám napíše.", PALE, ROSE, SMALL),
    p("Не добавляйте догадки. Если время ещё не подтверждено, скажите: <i>Majiteľ napísal, že ešte preverí čas.</i> - Владелец написал, что ещё уточнит время.", SMALL),
    PageBreak(),

    p("5. Частые ошибки и упражнения", H1),
    box("<b>Частые ошибки:</b> называют только предмет без симптома; смешивают процесс и результат; используют резкий императив вместо просьбы; не подтверждают время; передают соседу неподтверждённую догадку как факт.", CREAM, colors.HexColor("#E7C76C"), TINY),
    p("Упражнение 1. Соедините проблему и описание", H2),
    p("1) kúrenie; 2) práčka; 3) okno; 4) kohútik. Фразы: a) sa nedá zavrieť; b) kvapká; c) nefunguje; d) sa pokazila.", TINY),
    p("Упражнение 2. Выберите вид", H2),
    p("1) Teraz technik ___ kotol. (opravuje/opraví) 2) Zajtra ho ___. (opravuje/opraví) 3) Každý deň ___ správcovi. (volám/zavolám) 4) Večer mu ___. (volám/zavolám)", TINY),
    p("Упражнение 3. Сделайте просьбу вежливой", H2),
    p("1) Pošlite technika. 2) Príďte zajtra. 3) Povedzte mi čas. 4) Skontrolujte kúrenie.", TINY),
    p("Упражнение 4. Согласуйте время", H2),
    p("Ответьте полными фразами: мастер предлагает stredu o 15.00; вы дома až od 17.00. Предложите другое время и подтвердите итог stredu o 18.00.", TINY),
    p("Упражнение 5. Передайте соседу через že", H2),
    p("Majiteľ: Technik príde o šiestej. Pred príchodom vám zavolá. Najprv skontroluje ventil. Opravu dokončí večer.", TINY),
    p("Упражнение 6. Сообщение владельцу", H2),
    p("Напишите 6-8 предложений: назовите проблему, место и начало; скажите, что уже сделали; попросите помощь; предложите два времени и попросите подтверждение.", TINY),
    PageBreak(),

    p("6. Ответы и проверка мастерства", H1),
    p("Ответы", H2),
    p("<b>1.</b> 1-c: kúrenie nefunguje; 2-d: práčka sa pokazila; 3-a: okno sa nedá zavrieť; 4-b: kohútik kvapká.", TINY),
    p("<b>2.</b> 1) Teraz technik <b>opravuje</b> kotol. 2) Zajtra ho <b>opraví</b>. 3) Každý deň <b>volám</b> správcovi. 4) Večer mu <b>zavolám</b>.", TINY),
    p("<b>3.</b> Mohli by ste poslať technika? Bolo by možné prísť zajtra? Mohli by ste mi, prosím, povedať čas? Mohli by ste skontrolovať kúrenie? Возможны другие вежливые варианты.", TINY),
    p("<b>4.</b> O tretej ešte nie som doma. Mohol by technik prísť po piatej? - Áno, môže prísť o šiestej. - Ďakujem, platí streda o šiestej.", TINY),
    p("<b>5.</b> Majiteľ povedal, že technik príde o šiestej, pred príchodom nám zavolá, najprv skontroluje ventil a opravu dokončí večer.", TINY),
    p("<b>6. Модель:</b> Dobrý deň, v kuchyni nám od včera nefunguje elektrina. Istič som skontroloval, ale problém zostal. Mohli by ste, prosím, poslať technika? Zajtra budem doma od štvrtej, vo štvrtok celý deň. Dajte mi, prosím, vedieť, ktorý čas vám vyhovuje. Ďakujem za pomoc. Возможны другие естественные варианты.", TINY),
    p("Итог в четырёх пунктах", H2),
    table([
        ["OK", "Описываю симптом, место, время и последствие."],
        ["OK", "Различаю процесс и ожидаемый результат."],
        ["OK", "Вежливо прошу и подтверждаю время визита."],
        ["OK", "Передаю соседу подтверждённое решение через že."],
    ], [12 * mm, 158 * mm], 6.2, False),
    Spacer(1, 2 * mm),
    box("<b>Финальная проверка:</b> за 90 секунд сообщите о протечке, попросите мастера, договоритесь о времени и затем передайте соседу четыре подтверждённых факта.", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    p("Следующий шаг", H2),
    p("В теме 6.4 вы научитесь давать последовательные инструкции для устройств, файлов и приложений.", SMALL),
]

doc.build(story)
print(OUTPUT)
