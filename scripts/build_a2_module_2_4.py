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
OUTPUT = ROOT / "output" / "pdf" / "A2" / "Module_02" / "Slovak_A2_Tema_2_4_Akuzativ_mnozhestvennogo_chisla.pdf"
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
TITLE = ParagraphStyle("Title", fontName="Arial-Bold", fontSize=23, leading=27, textColor=colors.white, alignment=TA_LEFT, spaceAfter=5 * mm)
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
        canvas.drawString(20 * mm, height - 12 * mm, "SLOVAK A2  |  ТЕМА 2.4")
        canvas.drawRightString(width - 20 * mm, height - 12 * mm, "Akuzatív множественного числа")
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
    title="Slovak A2 - Тема 2.4 - Akuzatív множественного числа", author="SlovoKrok",
)
frame = Frame(20 * mm, 18 * mm, 170 * mm, 257 * mm, id="main", leftPadding=0, rightPadding=0)
doc.addPageTemplates([PageTemplate(id="series", frames=[frame], onPage=draw_page)])

story = [
    p("МОДУЛЬ 2  •  ПАДЕЖИ И УПРАВЛЕНИЕ A2", COVER_KICKER),
    p("Akuzatív<br/>множественного числа", TITLE),
    p("Akuzatív množného čísla", SUBTITLE),
    Spacer(1, 34 * mm),
    p("В темах 2.1-2.3 вы согласовывали группы в Nominatív и Akuzatív singular. Теперь объединяем систему: кого мы видим и приглашаем, что ищем, покупаем или выбираем во множественном числе.", BODY),
    p("После модуля вы сможете:", H2),
    styled_table([
        ["1", "различать tých для мужчин и смешанных групп и tie для остальных"],
        ["2", "строить полную цепочку tých mojich nových kolegov / tie moje nové knihy"],
        ["3", "употреблять dvoch, troch, štyroch и piatich с названиями мужчин"],
        ["4", "говорить, кого и что вы видите, ищете, приглашаете, покупаете или выбираете"],
    ], [12 * mm, 158 * mm], font_size=8.0, header=False),
    Spacer(1, 3 * mm),
    box("<b>Главная формула:</b> vidím + tých dvoch nových kolegov / tie dve nové kolegyne / tie dva nové telefóny.", PALE, PINK),
    PageBreak(),

    p("1. Tých или tie?", H1),
    p("Форма зависит не просто от значения 'люди'. Особая цепочка tých ... -ých нужна только мужскому одушевлённому роду и смешанной группе с мужским названием.", BODY),
    styled_table([
        ["Кого или что?", "Nominatív", "Akuzatív", "Перевод"],
        ["мужчины", "tí noví kolegovia", "tých nových kolegov", "тех новых коллег"],
        ["смешанная группа", "tí mladí študenti", "tých mladých študentov", "тех молодых студентов"],
        ["женщины", "tie nové kolegyne", "tie nové kolegyne", "тех новых коллег-женщин"],
        ["дети", "tie malé deti", "tie malé deti", "тех маленьких детей"],
        ["предметы, муж. род", "tie nové telefóny", "tie nové telefóny", "те новые телефоны"],
        ["женский род", "tie dôležité knihy", "tie dôležité knihy", "те важные книги"],
        ["средний род", "tie rýchle autá", "tie rýchle autá", "те быстрые машины"],
    ], [35 * mm, 48 * mm, 51 * mm, 36 * mm], font_size=6.7),
    Spacer(1, 4 * mm),
    box("<b>Ловушка:</b> женщина и ребёнок - люди, но формы другие: <b>vidím tie nové kolegyne</b>, <b>poznám tie malé deti</b>. Tých относится к мужскому одушевлённому роду.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    PageBreak(),

    p("2. Полное согласование", H1),
    p("У мужской одушевлённой группы меняются указательное, притяжательное, прилагательное слово и существительное. У остальных групп Akuzatív совпадает с Nominatív plural.", BODY),
    styled_table([
        ["Nominatív", "Akuzatív", "Перевод объекта"],
        ["tí moji noví kolegovia", "tých mojich nových kolegov", "тех моих новых коллег"],
        ["tí naši dobrí priatelia", "tých našich dobrých priateľov", "тех наших хороших друзей"],
        ["tie moje nové kolegyne", "tie moje nové kolegyne", "тех моих новых коллег-женщин"],
        ["tie naše dôležité veci", "tie naše dôležité veci", "те наши важные вещи"],
        ["tie ich malé autá", "tie ich malé autá", "те их маленькие машины"],
    ], [62 * mm, 67 * mm, 41 * mm], font_size=6.9),
    p("Частотные формы существительных", H2),
    styled_table([
        ["Nominatív", "Akuzatív", "Пример"],
        ["kolegovia", "kolegov", "Pozývam kolegov. - Я приглашаю коллег."],
        ["učitelia", "učiteľov", "Hľadám učiteľov. - Я ищу учителей."],
        ["priatelia", "priateľov", "Vidím priateľov. - Я вижу друзей."],
        ["muži", "mužov", "Poznám tých mužov. - Я знаю тех мужчин."],
        ["ľudia", "ľudí", "Čakáme tých ľudí. - Мы ждём тех людей."],
        ["hostia", "hostí", "Vítame hostí. - Мы приветствуем гостей."],
    ], [43 * mm, 42 * mm, 85 * mm], font_size=7.0),
    Spacer(1, 3 * mm),
    box("<b>Запоминайте парами:</b> ľudia - ľudí, hostia - hostí. Окончание нельзя безопасно угадать у каждого слова.", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    PageBreak(),

    p("3. Числительные с мужскими названиями людей", H1),
    p("В Nominatív используются dvaja, traja, štyria, piati. В Akuzatív особая форма числительного согласуется с мужским одушевлённым объектом, а существительное получает форму на -ov или другую словарную форму.", BODY),
    styled_table([
        ["Число", "Nominatív", "Akuzatív в предложении"],
        ["2", "dvaja kolegovia", "Pozývam dvoch kolegov. - Приглашаю двух коллег."],
        ["3", "traja priatelia", "Čakám troch priateľov. - Жду трёх друзей."],
        ["4", "štyria učitelia", "Hľadám štyroch učiteľov. - Ищу четырёх учителей."],
        ["5", "piati študenti", "Poznám piatich študentov. - Знаю пятерых студентов."],
    ], [24 * mm, 55 * mm, 91 * mm], font_size=7.1),
    p("Полная группа с числительным", H2),
    styled_table([
        ["Простая группа", "Расширенная группа"],
        ["dvoch kolegov", "tých dvoch nových kolegov"],
        ["troch priateľov", "mojich troch dobrých priateľov"],
        ["štyroch učiteľov", "tých štyroch slovenských učiteľov"],
        ["piatich študentov", "našich piatich mladých študentov"],
    ], [69 * mm, 101 * mm], font_size=7.15),
    p("Сравните", H2),
    box("<b>Vidím dvoch mužov</b>, но <b>vidím dve ženy</b>, <b>tri deti</b> и <b>dva domy</b>. Формы dvoch / troch / štyroch / piatich в этом модуле относятся к мужским названиям людей. Количество предметов от пяти системно разбирается в теме 2.6.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    PageBreak(),

    p("4. Люди и предметы в одной ситуации", H1),
    p("В реальной речи Akuzatív plural часто связывает несколько объектов. Сначала назовите группу полностью, затем замените её местоимением ich, знакомым по теме 2.3.", BODY),
    p("Модель: подготовка встречи", H2),
    box("Na stretnutie pozývam <b>tých troch nových kolegov</b> a <b>tie dve slovenské kolegyne</b>. Poznám <b>ich</b> z práce. Pre hostí objednávam <b>tie veľké šaláty</b> a kupujem <b>tie studené nápoje</b>. Potom vyberám <b>dve tiché miestnosti</b> a rezervujem <b>ich</b> na popoludnie.", PALE, ROSE, SMALL),
    p("Перевод: На встречу я приглашаю трёх новых коллег и двух словацких коллег-женщин. Я знаю их по работе. Для гостей заказываю большие салаты и покупаю холодные напитки. Затем выбираю две тихие комнаты и бронирую их на вторую половину дня.", SMALL),
    p("Мини-диалог: покупки для команды", H2),
    box("<b>A:</b> Hľadáš tie nové notebooky?<br/><b>B:</b> Áno, potrebujem ich pre kolegov.<br/><b>A:</b> Ktorých kolegov?<br/><b>B:</b> Pre tých dvoch nových programátorov.<br/><b>A:</b> A pozývaš aj tie dve dizajnérky?<br/><b>B:</b> Áno, pozývam ich na prezentáciu.", ALT, ROSE, SMALL),
    p("Перевод: Ты ищешь новые ноутбуки? - Да, они нужны мне для коллег. - Для каких коллег? - Для двух новых программистов. - А двух дизайнеров-женщин ты тоже приглашаешь? - Да, приглашаю их на презентацию.", SMALL),
    p("Банк глаголов", H2),
    styled_table([
        ["Люди", "Предметы", "Выбор"],
        ["vidieť, poznať, čakať", "hľadať, kupovať, objednávať", "vyberať, rezervovať, potrebovať"],
    ], [56 * mm, 58 * mm, 56 * mm], font_size=7.1),
    PageBreak(),

    p("5. Частые ошибки и упражнения", H1),
    box("<b>Алгоритм:</b> найдите объект -> определите, мужская ли это одушевлённая группа -> выберите tých или tie -> согласуйте всю цепочку -> проверьте числительное.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    p("Упражнение 1. Выберите tých или tie", H2),
    p("1) ___ nových kolegov; 2) ___ nové kolegyne; 3) ___ malé deti; 4) ___ mladých študentov; 5) ___ rýchle autá; 6) ___ dobrých priateľov.", SMALL),
    p("Упражнение 2. Преобразуйте всю группу", H2),
    p("1) tí moji noví kolegovia; 2) tí naši dobrí priatelia; 3) tie moje nové knihy; 4) tie malé deti; 5) tí slovenskí učitelia.", SMALL),
    p("Упражнение 3. Вставьте числительное", H2),
    p("1) Vidím ___ mužov (2). 2) Pozývam ___ kolegov (3). 3) Čakám ___ učiteľov (4). 4) Poznám ___ študentov (5). 5) Kupujem ___ knihy (2).", SMALL),
    p("Упражнение 4. Исправьте ошибки", H2),
    p("1) Vidím tie noví kolegovia. 2) Hľadám tých nové knihy. 3) Pozývam traja priatelia. 4) Čakám štyria učiteľov. 5) Kupujem tých nové telefóny.", SMALL),
    p("Упражнение 5. Переведите", H2),
    p("1) Я знаю тех двух новых коллег. 2) Мы приглашаем трёх хороших друзей. 3) Ты видишь эти новые книги? 4) Я жду четырёх словацких учителей. 5) Мы покупаем те две маленькие машины.", SMALL),
    p("Упражнение 6. Подготовьте событие", H2),
    p("Напишите 5-7 предложений о встрече или покупке. Используйте две мужские одушевлённые группы, две другие группы, dvoch / troch / štyroch / piatich и местоимение ich.", SMALL),
    PageBreak(),

    p("6. Ответы и проверка мастерства", H1),
    p("Ответы", H2),
    p("<b>1.</b> tých; tie; tie; tých; tie; tých.", TINY),
    p("<b>2.</b> tých mojich nových kolegov; tých našich dobrých priateľov; tie moje nové knihy; tie malé deti; tých slovenských učiteľov.", TINY),
    p("<b>3.</b> dvoch mužov; troch kolegov; štyroch učiteľov; piatich študentov; dve knihy.", TINY),
    p("<b>4.</b> 1) Vidím tých nových kolegov. 2) Hľadám tie nové knihy. 3) Pozývam troch priateľov. 4) Čakám štyroch učiteľov. 5) Kupujem tie nové telefóny.", TINY),
    p("<b>5.</b> 1) Poznám tých dvoch nových kolegov. 2) Pozývame troch dobrých priateľov. 3) Vidíš tieto nové knihy? 4) Čakám štyroch slovenských učiteľov. 5) Kupujeme tie dve malé autá.", TINY),
    p("<b>6. Модель:</b> Na prezentáciu pozývam tých troch nových kolegov. Čakám aj tie dve dizajnérky. Poznám ich z práce. Pre hostí objednávam tie veľké šaláty a kupujem dve minerálne vody. Hľadám štyroch dobrovoľníkov. Potom vyberám dve tiché miestnosti.", TINY),
    p("Итог в четырёх пунктах", H2),
    styled_table([
        ["OK", "Я выбираю tých для мужской одушевлённой группы и tie для остальных."],
        ["OK", "Я согласую всю цепочку: tých mojich nových kolegov."],
        ["OK", "Я употребляю dvoch, troch, štyroch и piatich с названиями мужчин."],
        ["OK", "Я говорю, кого и что вижу, ищу, приглашаю, покупаю или выбираю."],
    ], [12 * mm, 158 * mm], font_size=7.55, header=False),
    Spacer(1, 3 * mm),
    box("<b>Финальная проверка:</b> назовите две группы людей и две группы предметов, с которыми вы планируете действие. Если tých / tie и вся цепочка согласованы, цель достигнута.", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    p("Следующий шаг", H2),
    p("В модуле 2.5 вы перейдёте к Genitív singular и значениям отсутствия, происхождения и границы: <b>bez nového kolegu, do starého mesta, od dobrej priateľky</b>.", SMALL),
]

doc.build(story)
print(OUTPUT)
