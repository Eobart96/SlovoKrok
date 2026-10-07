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
OUTPUT = ROOT / "output/pdf/A2/Module_07/Slovak_A2_Tema_7_5_Bronirovanie_i_plan_poezdki.pdf"
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
        canvas.drawString(20 * mm, height - 12 * mm, "A2 7.5  |  Бронирование и план поездки")
    canvas.setFont("Arial", 8)
    canvas.setFillColor(MUTED)
    canvas.drawString(20 * mm, 9 * mm, "SlovoKrok | личный учебный модуль")
    canvas.drawRightString(width - 20 * mm, 9 * mm, f"стр. {page_number} / 7")
    canvas.restoreState()


doc = BaseDocTemplate(
    str(OUTPUT), pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=20 * mm, bottomMargin=18 * mm,
    title="Slovak A2 - Тема 7.5 - Бронирование и план поездки", author="SlovoKrok",
)
doc.addPageTemplates([PageTemplate(id="series", frames=[Frame(20 * mm, 18 * mm, 170 * mm, 257 * mm, id="main", leftPadding=0, rightPadding=0)], onPage=draw_page)])


story = [
    p("A2 7.5  •  МОДУЛЬ 7  •  РАБОТА, ПУТЕШЕСТВИЯ И СТРАНА", KICK),
    p("Бронирование и план поездки", TITLE),
    p("Rezervácia a plán cesty: сравниваем варианты, бронируем и договариваемся", SUBTITLE),
    Spacer(1, 41 * mm),
    p("На уровне A2 вы не просто спрашиваете цену. Вы сравниваете жильё и транспорт, вежливо предлагаете вариант, бронируете его и согласовываете общий план с попутчиком."),
    p("После модуля вы сможете:", H2),
    table([
        ["1", "сравнить жильё и способы добраться"],
        ["2", "уточнить условия и забронировать вариант"],
        ["3", "предложить план с кондиционалом и будущим временем"],
        ["4", "согласиться, возразить и договориться о решении"],
    ], [12 * mm, 158 * mm], 7.2, False),
    Spacer(1, 3 * mm),
    box("<b>Формула:</b> сравниваем → предлагаем → уточняем условия → бронируем → подтверждаем общий план."),
    PageBreak(),

    p("1. Сравниваем жильё и транспорт", H1),
    p("Для выбора нужны не отдельные прилагательные, а ясный критерий: цена, расположение, время или удобство. Сравнивайте через <b>ako</b> и сразу объясняйте, почему вариант подходит."),
    table([
        ["Критерий", "Сравнение", "Перевод"],
        ["цена", "Penzión je lacnejší ako hotel.", "Пансион дешевле гостиницы."],
        ["комфорт", "Vlak je pohodlnejší ako autobus.", "Поезд удобнее автобуса."],
        ["скорость", "Lietadlo je rýchlejšie, ale drahšie.", "Самолёт быстрее, но дороже."],
        ["место", "Apartmán je bližšie k centru.", "Апартаменты ближе к центру."],
        ["условия", "Hotel má lepšie raňajky.", "В гостинице завтрак лучше."],
        ["итог", "Najvýhodnejší je nočný vlak.", "Самый выгодный вариант — ночной поезд."],
    ], [35 * mm, 74 * mm, 61 * mm], 5.45),
    p("Сравнение по двум критериям", H2),
    table([
        ["Вариант", "Плюс", "Минус", "Решение"],
        ["hotel", "bližšie k centru", "drahší", "vyhovuje pri krátkom pobyte"],
        ["penzión", "lacnejší", "ďalej od stanice", "dobrý na tri noci"],
        ["vlak", "pohodlnejší", "ide neskôr", "môžeme pracovať cestou"],
        ["autobus", "odchádza skôr", "menej miesta", "prídeme pred obedom"],
    ], [27 * mm, 47 * mm, 43 * mm, 53 * mm], 5.3),
    box("<b>Естественный выбор:</b> <i>Penzión je ďalej od centra, ale je lacnejší a raňajky sú v cene. Na tri noci je to pre nás lepší variant.</i>", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    PageBreak(),

    p("2. Условия и бронирование", H1),
    p("Перед подтверждением проверьте даты, тип номера, цену, питание и условия отмены. В сообщении сначала сформулируйте просьбу, затем перечислите данные и задайте конкретные вопросы."),
    table([
        ["Что уточнить", "Полезная фраза"],
        ["свободные места", "Máte voľnú dvojlôžkovú izbu?"],
        ["даты", "Chceli by sme zostať od 12. do 15. augusta."],
        ["цена", "Koľko stojí izba na noc?"],
        ["завтрак", "Sú raňajky v cene?"],
        ["отмена", "Je možné rezerváciu bezplatne zrušiť?"],
        ["заезд", "Od ktorej hodiny sa môžeme ubytovať?"],
        ["подтверждение", "Prosím, potvrďte nám rezerváciu e-mailom."],
    ], [49 * mm, 121 * mm], 5.7),
    p("Модель письма", H2),
    box("<b>Predmet: Rezervácia izby</b><br/>Dobrý deň, chceli by sme si rezervovať dvojlôžkovú izbu pre dve osoby od 12. do 15. augusta. Prosím, napíšte nám, či sú raňajky v cene a či môžeme rezerváciu bezplatne zrušiť. Prídeme približne o 18.00. Dúfam, že máte izbu s vlastnou kúpeľňou. Prosím, potvrďte nám cenu a rezerváciu e-mailom. Ďakujem.", PALE, ROSE, SMALL),
    p("Ответ гостиницы", H2),
    box("Dobrý deň, izba je voľná. Cena je 78 eur za noc a raňajky sú v cene. Bezplatné zrušenie je možné najneskôr dva dni pred príchodom. Ubytovať sa môžete od 15.00. Rezerváciu Vám potvrdzujeme.", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    box("<b>Не забывайте:</b> <i>rezervovať si izbu</i> — забронировать себе номер; <i>potvrdiť rezerváciu</i> — подтвердить бронирование; <i>zrušiť rezerváciu</i> — отменить его.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    PageBreak(),

    p("3. Предложение: кондиционал и будущее", H1),
    p("Кондиционал делает предложение мягким: <b>mohli by sme</b>, <b>radšej by som</b>, <b>bolo by lepšie</b>. Будущее время фиксирует уже согласованный план."),
    table([
        ["Функция", "Фраза", "Перевод"],
        ["предложить", "Mohli by sme ísť vlakom.", "Мы могли бы поехать поездом."],
        ["предпочесть", "Radšej by som býval v penzióne.", "Я бы предпочёл жить в пансионе."],
        ["оценить", "Bolo by lepšie zostať tri noci.", "Было бы лучше остаться на три ночи."],
        ["условие", "Keby sme išli ráno, prišli by sme pred obedom.", "Если бы мы поехали утром, прибыли бы до обеда."],
        ["план-процесс", "V sobotu budeme cestovať do Tatier.", "В субботу будем ехать в Татры."],
        ["результат", "Večer sa ubytujeme a zarezervujeme výlet.", "Вечером заселимся и забронируем экскурсию."],
    ], [33 * mm, 78 * mm, 59 * mm], 5.35),
    p("Надежда и уверенность", H2),
    table([
        ["Модель", "Нюанс", "Пример"],
        ["Dúfam, že...", "надеюсь", "Dúfam, že bude izba voľná."],
        ["Verím, že...", "верю / уверен", "Verím, že nám termín potvrdia."],
        ["Myslím si, že...", "считаю", "Myslím si, že vlak bude pohodlnejší."],
    ], [40 * mm, 41 * mm, 89 * mm], 5.55),
    box("<b>Связный план:</b> <i>Mohli by sme cestovať v piatok večer. V sobotu ráno sa ubytujeme. Dúfam, že bude pekné počasie, a potom pôjdeme na výlet.</i>", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    PageBreak(),

    p("4. Согласовываем общий план", H1),
    p("Хорошее обсуждение не заканчивается на <i>áno/nie</i>. Назовите, что подходит, вежливо обозначьте проблему и предложите замену."),
    table([
        ["Действие", "Фраза", "Перевод"],
        ["согласиться", "Súhlasím, tento variant mi vyhovuje.", "Согласен, этот вариант мне подходит."],
        ["частично согласиться", "To je dobrý nápad, ale hotel je drahý.", "Это хорошая идея, но гостиница дорогая."],
        ["не согласиться", "Nemyslím si, že autobus je najlepší.", "Не думаю, что автобус — лучший вариант."],
        ["предложить замену", "Navrhujem lacnejší penzión pri stanici.", "Предлагаю более дешёвый пансион у вокзала."],
        ["уточнить", "Vyhovuje ti odchod o siedmej?", "Тебе подходит отправление в семь?"],
        ["закрепить решение", "Dohodnuté, dnes rezervujem izbu.", "Договорились, сегодня забронирую номер."],
    ], [36 * mm, 76 * mm, 58 * mm], 5.25),
    p("Мини-диалог", H2),
    box("<b>Eva:</b> Mohli by sme ísť autobusom. Je lacnejší.<br/><b>Martin:</b> To je pravda, ale cesta trvá o dve hodiny dlhšie. Radšej by som išiel vlakom.<br/><b>Eva:</b> Súhlasím. A čo ubytovanie?<br/><b>Martin:</b> Navrhujem penzión pri stanici. Je lacnejší ako hotel a raňajky sú v cene.<br/><b>Eva:</b> Dobre. Ja rezervujem izbu a ty kúpiš lístky.<br/><b>Martin:</b> Dohodnuté. Dúfam, že ešte budú voľné miesta.", PALE, ROSE, SMALL),
    p("Общий план", H2),
    table([
        ["Kedy", "Čo urobíme", "Kto"],
        ["dnes", "rezervujeme izbu a kúpime lístky", "Eva / Martin"],
        ["piatok 17.30", "stretneme sa na stanici", "obaja"],
        ["piatok večer", "prídeme a ubytujeme sa", "obaja"],
        ["sobota ráno", "pôjdeme na výlet", "obaja"],
    ], [42 * mm, 88 * mm, 40 * mm], 5.45),
    PageBreak(),

    p("5. Частые ошибки и упражнения", H1),
    table([
        ["Ошибка", "Правильно", "Почему"],
        ["*penzión je lacnejšie", "penzión je lacnejší", "согласование с мужским родом"],
        ["*mohli sme ísť zajtra", "mohli by sme ísť zajtra", "предложение: by + прошедшая форма"],
        ["*dúfam, aby bola izba", "dúfam, že bude izba", "после dúfam здесь že"],
        ["*budeme zarezervovať", "zarezervujeme", "совершенный глагол даёт результат"],
        ["*súhlasím s tento plán", "súhlasím s týmto plánom", "s + творительный"],
    ], [52 * mm, 56 * mm, 62 * mm], 5.25),
    p("Упражнение 1. Выберите лучший вариант", H2),
    p("1) Hotel stojí 110 €, penzión 75 €. Penzión je (lacnejší / najdrahší). 2) Vlak trvá 3 h, autobus 5 h. Vlak je (rýchlejší / pomalší). 3) Apartmán je 500 m od centra, hotel 3 km. Apartmán je (bližšie / ďalej).", SMALL),
    p("Упражнение 2. Дополните бронирование", H2),
    p("<i>voľnú / v cene / zrušiť / potvrďte</i>: Máte ___ dvojlôžkovú izbu? Sú raňajky ___? Je možné rezerváciu bezplatne ___? Prosím, ___ nám rezerváciu e-mailom.", SMALL),
    p("Упражнение 3. Сделайте предложение мягче", H2),
    p("Модель: <i>Ideme vlakom. → Mohli by sme ísť vlakom.</i> 1) Zostaneme tri noci. 2) Bývame v penzióne. 3) Cestujeme v piatok večer.", SMALL),
    p("Упражнение 4. Выберите форму будущего", H2),
    p("1) V sobotu (budeme cestovať / budeme pricestovať) do Tatier. 2) Večer sa (ubytujeme / budeme ubytovať). 3) Dnes (zarezervujem / budem zarezervovať) izbu. 4) Cestou (budeme porovnávať / porovnáme celý čas) ponuky.", SMALL),
    p("Упражнение 5. Ответьте партнёру", H2),
    p("Партнёр говорит: <i>Poďme autobusom a rezervujme drahší hotel v centre.</i> Согласитесь с одной частью, возразите против другой и предложите замену — 3 фразы.", SMALL),
    p("Упражнение 6. Составьте общий план", H2),
    p("Напишите 5–6 фраз: сравните два варианта, сделайте предложение с <i>mohli by sme</i>, назовите бронирование, будущий план и надежду с <i>dúfam/verím, že</i>.", SMALL),
    PageBreak(),

    p("6. Ответы и проверка мастерства", H1),
    p("Ответы", H2),
    table([
        ["№", "Ключ"],
        ["1", "1 lacnejší; 2 rýchlejší; 3 bližšie."],
        ["2", "voľnú; v cene; zrušiť; potvrďte."],
        ["3", "1 Mohli by sme zostať tri noci. 2 Mohli by sme bývať v penzióne. 3 Mohli by sme cestovať v piatok večer."],
        ["4", "1 budeme cestovať; 2 ubytujeme; 3 zarezervujem; 4 budeme porovnávať."],
        ["5", "Модель: Súhlasím, autobus je lacnejší. Hotel v centre je však príliš drahý. Navrhujem lacnejší penzión pri stanici."],
        ["6", "Возможны разные ответы; проверьте сравнение, kondicionál, бронирование, будущее и že."],
    ], [13 * mm, 157 * mm], 5.35),
    p("Модель общего плана", H2),
    box("Hotel je bližšie k centru, ale penzión je o 30 eur lacnejší a raňajky sú v cene. Mohli by sme preto bývať v penzióne a ísť pohodlnejším vlakom. Dnes zarezervujem dvojlôžkovú izbu a požiadam o potvrdenie e-mailom. V piatok budeme cestovať do Popradu a večer sa ubytujeme. V sobotu pôjdeme na výlet. Dúfam, že bude pekné počasie a že nám tento plán bude vyhovovať.", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    p("Финальная проверка", H2),
    table([
        ["Могу...", "Да / ещё раз"],
        ["сравнить жильё и транспорт по двум критериям", "□ / □"],
        ["уточнить цену, питание, отмену и время заезда", "□ / □"],
        ["сделать мягкое предложение с by", "□ / □"],
        ["согласовать действия в будущем времени", "□ / □"],
        ["согласиться или возразить и предложить замену", "□ / □"],
    ], [128 * mm, 42 * mm], 5.65),
    box("<b>Критерий освоения:</b> не менее 5 из 6 упражнений без подсказки и общий план из 5–6 связанных фраз с одним сравнением, одним предложением и одним подтверждённым действием.", PALE, ROSE, SMALL),
]

doc.build(story)
print(OUTPUT)
