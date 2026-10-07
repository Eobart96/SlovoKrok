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
OUTPUT = ROOT / "output" / "pdf" / "A2" / "Module_01" / "Slovak_A2_Tema_1_2_Vid_glagola.pdf"
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
BODY = ParagraphStyle("Body", fontName="Arial", fontSize=9.1, leading=12.2, textColor=INK, spaceAfter=4.2 * mm)
SMALL = ParagraphStyle("Small", parent=BODY, fontSize=7.9, leading=10.1, spaceAfter=2.1 * mm)
TITLE = ParagraphStyle("Title", fontName="Arial-Bold", fontSize=25, leading=29, textColor=colors.white, alignment=TA_LEFT, spaceAfter=5 * mm)
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


def styled_table(data, widths, font_size=7.7, header=True):
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
        canvas.drawString(20 * mm, height - 12 * mm, "SLOVAK A2  |  ТЕМА 1.2")
        canvas.drawRightString(width - 20 * mm, height - 12 * mm, "Вид глагола")
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
    title="Slovak A2 - Тема 1.2 - Вид глагола", author="SlovoKrok",
)
frame = Frame(20 * mm, 18 * mm, 170 * mm, 257 * mm, id="main", leftPadding=0, rightPadding=0)
doc.addPageTemplates([PageTemplate(id="series", frames=[frame], onPage=draw_page)])

story = [
    p("МОДУЛЬ 1  •  ПЕРЕХОД ОТ A1 К A2", COVER_KICKER),
    p("Вид глагола", TITLE),
    p("Dokonavé a nedokonavé slovesá", SUBTITLE),
    Spacer(1, 38 * mm),
    p("На A2 важно выбрать не только время, но и взгляд на действие: оно разворачивается, повторяется или уже привело к результату.", BODY),
    p("После модуля вы сможете:", H2),
    styled_table([
        ["1", "различать процесс, повторяемость, результат и однократность"],
        ["2", "узнавать и запоминать частые видовые пары"],
        ["3", "выбирать вид в прошедшем и будущем времени"],
        ["4", "рассказывать о действиях и их результатах связным текстом"],
    ], [12 * mm, 158 * mm], font_size=8.4, header=False),
    Spacer(1, 5 * mm),
    box("<b>Главная формула:</b> nedokonavý vid показывает действие изнутри; dokonavý vid представляет его как целый завершённый факт.", PALE, PINK),
    Spacer(1, 4 * mm),
    p("Маршрут: смысл -> пары -> прошедшее -> будущее -> примеры -> упражнения -> ответы.", SMALL),
    PageBreak(),

    p("1. Вид - это не время", H1),
    p("Каждый глагол в конкретном употреблении имеет вид. <b>Nedokonavý vid</b> показывает течение действия без обязательного результата. <b>Dokonavý vid</b> показывает действие как ограниченный, завершённый факт.", BODY),
    styled_table([
        ["Что важно", "Nedokonavý", "Dokonavý"],
        ["Процесс", "Čítal som knihu.", "Prečítal som knihu."],
        ["Повтор / один факт", "Každý deň som kupoval chlieb.", "Včera som kúpil chlieb."],
        ["Длительность", "Dve hodiny som písala správu.", "Napísala som správu."],
        ["Вопрос", "Čo si robil?", "Čo si urobil?"],
        ["Фокус", "что происходило", "какой результат получен"],
    ], [42 * mm, 64 * mm, 64 * mm], font_size=7.45),
    Spacer(1, 4 * mm),
    box("<b>Важно:</b> вид не равен длительности. Совершенное действие тоже может занять много времени: <b>Za tri dni som prečítal celú knihu.</b>", CREAM, colors.HexColor("#E7C76C"), SMALL),
    p("Как задать себе вопрос", H2),
    bullet("Важен ход, фон или привычное занятие без акцента на границе? Выбирайте недоконанный вид."),
    bullet("Важен достигнутый результат или один завершённый факт? Выбирайте доконанный вид."),
    bullet("Повтор сам по себе не запрещает доконанный вид: <b>Každé ráno si prečítam správy</b> подчёркивает завершение каждого чтения."),
    p("Мини-проверка", H2),
    p("Что важнее в каждой фразе: процесс или результат? 1) Varil som večeru. 2) Uvaril som večeru. 3) Anna písala email. 4) Anna napísala email.", BODY),
    PageBreak(),

    p("2. Как учить видовые пары", H1),
    p("Пары образуются по-разному. Приставка часто делает глагол доконанным, но может также изменить само значение. Поэтому учите пару вместе с примером.", BODY),
    styled_table([
        ["Nedokonavý", "Dokonavý", "Значение"],
        ["robiť", "urobiť", "делать - сделать"],
        ["písať", "napísať", "писать - написать"],
        ["čítať", "prečítať", "читать - прочитать"],
        ["variť", "uvariť", "готовить - приготовить"],
        ["volať", "zavolať", "звонить - позвонить"],
        ["jesť", "zjesť", "есть - съесть"],
        ["piť", "vypiť", "пить - выпить"],
        ["kupovať", "kúpiť", "покупать - купить"],
        ["otvárať", "otvoriť", "открывать - открыть"],
        ["dávať", "dať", "давать - дать"],
        ["brať", "vziať", "брать - взять"],
    ], [55 * mm, 55 * mm, 60 * mm], font_size=7.15),
    Spacer(1, 4 * mm),
    box("<b>Не стройте пару механически:</b> <b>písať - napísať</b> различаются видом, но <b>písať - prepísať</b> уже означают &quot;писать - переписать&quot;. Проверяйте значение в словаре.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    p("Практичный формат записи", H2),
    p("Записывайте сразу четыре элемента: <b>písať - napísať - písal som - napíšem</b>. Так вы связываете пару с прошедшим и будущим.", BODY),
    PageBreak(),

    p("3. Вид в прошедшем и будущем", H1),
    p("В прошедшем оба вида имеют обычные -l-формы. В будущем способы различаются.", BODY),
    styled_table([
        ["Смысл", "Прошедшее", "Будущее"],
        ["Процесс", "Včera som písal list.", "Večer budem písať list."],
        ["Результат", "Včera som napísal list.", "Večer napíšem list."],
        ["Повтор", "Často sme tam chodili.", "Budeme tam často chodiť."],
        ["Один факт", "Raz sme tam prišli neskoro.", "Zajtra tam prídeme o ôsmej."],
    ], [42 * mm, 64 * mm, 64 * mm], font_size=7.45),
    Spacer(1, 4 * mm),
    p("Совершенная форма и будущее", H2),
    p("У доконанных глаголов форма, похожая на настоящее время, обычно сообщает о будущем результате: <b>napíšem, prečítam, urobíme, zavolajú</b>. Настоящего процесса она не выражает.", BODY),
    styled_table([
        ["Без акцента на завершении", "С ожидаемым результатом", "Перевод"],
        ["Budem čítať článok.", "Prečítam článok.", "Буду читать / прочитаю статью."],
        ["Budeme variť obed.", "Uvaríme obed.", "Будем готовить / приготовим обед."],
        ["Nebudem kupovať auto.", "Nekúpim auto.", "Не буду покупать / не куплю машину."],
    ], [60 * mm, 55 * mm, 55 * mm], font_size=7.25),
    Spacer(1, 4 * mm),
    box("<b>Ориентир:</b> <b>budem + infinitív</b> сочетается с недоконанным глаголом. Для результата используйте личную форму доконанного глагола: <b>urobím</b>, не <b>budem urobiť</b>.", PALE, PINK, SMALL),
    p("Мини-проверка", H2),
    p("Сравните: <b>Zajtra budem upratovať byt.</b> / <b>Zajtra upracem byt.</b> Какая фраза обещает готовый результат?", BODY),
    PageBreak(),

    p("4. Банк примеров: действие и результат", H1),
    styled_table([
        ["Ситуация", "Процесс / повтор", "Результат"],
        ["Письмо", "Písala som email.", "Napísala som email."],
        ["Книга", "Čítal knihu celý večer.", "Prečítal knihu za týždeň."],
        ["Обед", "Mama varila obed.", "Mama uvarila obed."],
        ["Телефон", "Volal som Petrovi.", "Zavolal som Petrovi."],
        ["Покупка", "Kupovali sme darčeky.", "Kúpili sme tri darčeky."],
        ["Работа", "Robili úlohu dve hodiny.", "Urobili celú úlohu."],
        ["Напиток", "Pila čaj pomaly.", "Vypila celý čaj."],
        ["Дверь", "Otvárala okno.", "Otvorila okno."],
    ], [28 * mm, 71 * mm, 71 * mm], font_size=7.3),
    Spacer(1, 4 * mm),
    p("Мини-диалог", H2),
    box("<b>A:</b> Čo si robil večer?<br/><b>B:</b> Písal som správu pre kolegu.<br/><b>A:</b> A napísal si ju?<br/><b>B:</b> Áno, napísal. Potom som mu zavolal.", ALT, ROSE, SMALL),
    p("Почему здесь меняется вид", H2),
    p("Первый вопрос интересуется занятием. Второй проверяет результат. В ответе доконанные <b>napísal</b> и <b>zavolal</b> двигают рассказ от одного завершённого события к другому.", BODY),
    p("Личная проба", H2),
    p("Назовите одно дело, которым вы занимались вчера, и один результат, которого достигли. Используйте одну пару из таблицы.", BODY),
    PageBreak(),

    p("5. Частые ошибки и упражнения", H1),
    box("<b>Три ошибки:</b> 1) считать любую приставку только знаком вида; 2) говорить <b>budem napísať</b>; 3) выбирать доконанный вид только потому, что действие было коротким.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    p("Упражнение 1. Выберите смысл", H2),
    p("Процесс или результат? 1) Celý večer som čítal. 2) Prečítal som tri kapitoly. 3) Každý piatok sme nakupovali. 4) Kúpili sme nový stôl.", SMALL),
    p("Упражнение 2. Выберите глагол", H2),
    p("1) Včera som dve hodiny písal / napísal správu, ale nedokončil som ju. 2) Nakoniec som ju písal / napísal. 3) Keď som prišiel, Peter ešte varil / uvaril obed. 4) Obed bol hotový: Peter ho varil / uvaril.", SMALL),
    p("Упражнение 3. Образуйте будущее", H2),
    p("1) večer / čítať; 2) do večera / prečítať; 3) zajtra / variť; 4) zajtra / uvariť.", SMALL),
    p("Упражнение 4. Исправьте ошибки", H2),
    p("1) Zajtra budem napísať email. 2) Už dve hodiny prečítam noviny. 3) Včera som celý večer urobil úlohu, ale nedokončil som ju.", SMALL),
    p("Упражнение 5. Переведите", H2),
    p("1) Вчера я писал письмо два часа. 2) Я написал письмо. 3) Завтра мы будем готовить обед. 4) Мы приготовим обед к двенадцати.", SMALL),
    p("Упражнение 6. Короткий рассказ", H2),
    p("Напишите 5-6 предложений о вчерашнем дне: два процесса или повтора и три завершённых результата. Затем добавьте один план на завтра в двух вариантах: процесс и результат.", SMALL),
    PageBreak(),

    p("6. Ответы и проверка мастерства", H1),
    p("Ответы", H2),
    p("<b>1.</b> 1) процесс; 2) результат; 3) повтор; 4) результат.", SMALL),
    p("<b>2.</b> 1) písal; 2) napísal; 3) varil; 4) uvaril.", SMALL),
    p("<b>3.</b> Возможные ответы: 1) Večer budem čítať. 2) Do večera prečítam článok/knihu. 3) Zajtra budem variť. 4) Zajtra uvarím obed.", SMALL),
    p("<b>4.</b> 1) Zajtra napíšem email. 2) Už dve hodiny čítam noviny. 3) Včera som celý večer robil úlohu, ale nedokončil som ju.", SMALL),
    p("<b>5.</b> 1) Včera som dve hodiny písal list. 2) Napísal som list. 3) Zajtra budeme variť obed. 4) Obed uvaríme do dvanástej.", SMALL),
    p("<b>6. Возможный ответ:</b> Včera som dopoludnia pracoval. Čítal som dokumenty a písal poznámky. Potom som dokončil správu a poslal som ju kolegovi. Večer som uvaril večeru a zavolal som rodine. Zajtra budem čítať nový článok a do večera ho prečítam.", SMALL),
    p("Итог в четырёх пунктах", H2),
    styled_table([
        ["✓", "Я отличаю течение или повтор действия от завершённого факта."],
        ["✓", "Я учу видовые пары вместе со значением и примером."],
        ["✓", "Я строю будущее: budem písať, но napíšem."],
        ["✓", "Я могу чередовать фон и результаты в коротком рассказе."],
    ], [12 * mm, 158 * mm], font_size=8.0, header=False),
    Spacer(1, 4 * mm),
    box("<b>Финальная проверка:</b> объясните без таблицы разницу между <b>robil som - urobil som - budem robiť - urobím</b> и придумайте по одному своему примеру.", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    p("Следующий шаг", H2),
    p("Закрепите пять нужных вам пар. Не пытайтесь образовывать остальные механически: проверяйте их в словаре и записывайте вместе с контекстом. Затем переходите к PDF 1.3 о клитиках и второй позиции.", BODY),
]

doc.build(story)
print(OUTPUT)
