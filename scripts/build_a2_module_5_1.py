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
OUTPUT = ROOT / "output" / "pdf" / "A2" / "Module_05" / "Slovak_A2_Tema_5_1_Soedinyaem_mysli_a_ale_alebo.pdf"
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
BODY = ParagraphStyle("Body", fontName="Arial", fontSize=8.75, leading=11.5, textColor=INK, spaceAfter=3 * mm)
SMALL = ParagraphStyle("Small", parent=BODY, fontSize=7.6, leading=9.5, spaceAfter=1.65 * mm)
TINY = ParagraphStyle("Tiny", parent=BODY, fontSize=6.85, leading=8.45, spaceAfter=1.0 * mm)
TITLE = ParagraphStyle("Title", fontName="Arial-Bold", fontSize=20, leading=24, textColor=colors.white, alignment=TA_LEFT, spaceAfter=5 * mm)
SUBTITLE = ParagraphStyle("Subtitle", fontName="Arial", fontSize=11.5, leading=15, textColor=colors.HexColor("#FFD8EB"), spaceAfter=5 * mm)
H1 = ParagraphStyle("H1", fontName="Arial-Bold", fontSize=15.5, leading=18.5, textColor=PLUM, spaceBefore=1 * mm, spaceAfter=3 * mm)
H2 = ParagraphStyle("H2", fontName="Arial-Bold", fontSize=10.7, leading=13.2, textColor=PINK, spaceBefore=1.3 * mm, spaceAfter=1.5 * mm)
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


def styled_table(data, widths, font_size=7.1, header=True):
    converted = []
    for row_index, row in enumerate(data):
        style = ParagraphStyle(
            f"Cell{row_index}_{font_size}_{len(data)}", parent=SMALL, fontSize=font_size,
            leading=font_size + 1.8, textColor=colors.white if header and row_index == 0 else INK,
            fontName="Arial-Bold" if header and row_index == 0 else "Arial", spaceAfter=0,
        )
        converted.append([p(str(cell), style) for cell in row])
    table = Table(converted, colWidths=widths, repeatRows=1 if header else 0)
    commands = [
        ("GRID", (0, 0), (-1, -1), 0.45, ROSE), ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4.0), ("RIGHTPADDING", (0, 0), (-1, -1), 4.0),
        ("TOPPADDING", (0, 0), (-1, -1), 3.0), ("BOTTOMPADDING", (0, 0), (-1, -1), 3.0),
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
        canvas.drawString(20 * mm, height - 12 * mm, "A2 5.1  |  Соединяем мысли: a, ale, alebo")
    canvas.setFont("Arial", 8)
    canvas.setFillColor(MUTED)
    canvas.drawString(20 * mm, 9 * mm, "SlovoKrok | личный учебный модуль")
    canvas.drawRightString(width - 20 * mm, 9 * mm, f"стр. {page} / 7")
    canvas.restoreState()


doc = BaseDocTemplate(
    str(OUTPUT), pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=20 * mm, bottomMargin=18 * mm,
    title="Slovak A2 - Тема 5.1 - Соединяем мысли: a, ale, alebo", author="SlovoKrok",
)
frame = Frame(20 * mm, 18 * mm, 170 * mm, 257 * mm, id="main", leftPadding=0, rightPadding=0)
doc.addPageTemplates([PageTemplate(id="series", frames=[frame], onPage=draw_page)])

story = [
    p("МОДУЛЬ 5  •  СВЯЗНАЯ РЕЧЬ И СЛОЖНЫЕ ПРЕДЛОЖЕНИЯ", COVER_KICKER),
    p("Соединяем мысли:<br/>a, ale, alebo", TITLE),
    p("Spájame myšlienky: добавляем, противопоставляем, выбираем", SUBTITLE),
    Spacer(1, 35 * mm),
    p("На A2 важно не только сказать две правильные фразы, но и показать связь между ними. Три коротких союза дают основу связного ответа: <b>a</b> добавляет, <b>ale</b> меняет направление мысли, <b>alebo</b> предлагает выбор."),
    p("После модуля вы сможете:", H2),
    styled_table([
        ["1", "соединять совместимые факты и действия союзом a"],
        ["2", "показывать контраст или неожиданное ограничение союзом ale"],
        ["3", "предлагать два варианта и задавать вопрос с alebo"],
        ["4", "ставить запятую перед ale и не добавлять её автоматически перед a/alebo"],
    ], [12 * mm, 158 * mm], font_size=7.2, header=False),
    Spacer(1, 3 * mm),
    box("<b>Формула:</b> факт <b>a</b> факт; ожидание, <b>ale</b> контраст; вариант <b>alebo</b> вариант.", PALE, PINK),
    PageBreak(),

    p("1. Союз a: добавляем и продолжаем", H1),
    p("<b>A</b> обычно соответствует русскому \"и\". Он соединяет равноправные слова, признаки, факты или действия. Между частями нет конфликта: вторая мысль продолжает первую."),
    styled_table([
        ["Связь", "Словацкий пример", "Перевод"],
        ["предметы", "Kúpim chlieb a mlieko.", "Куплю хлеб и молоко."],
        ["признаки", "Byt je malý a útulný.", "Квартира маленькая и уютная."],
        ["действия", "Otvoril okno a zavolal Petrovi.", "Он открыл окно и позвонил Петеру."],
        ["факты", "Ja pracujem doma a sestra pracuje v kancelárii.", "Я работаю дома, а сестра работает в офисе."],
        ["последовательность", "Najprv sa najeme a potom pôjdeme von.", "Сначала поедим, а потом выйдем."],
    ], [28 * mm, 74 * mm, 68 * mm], font_size=6.35),
    p("Русское \"а\" не всегда означает ale", H2),
    p("В русском \"а\" может просто сопоставлять два нейтральных факта. По-словацки здесь часто нужен <b>a</b>, а не <b>ale</b>: <b>Ja bývam v Bratislave a brat býva v Nitre.</b> Никакого противоречия нет."),
    box("<b>Проверка смысла:</b> если вторую часть можно спокойно добавить словами \"и ещё\", выбирайте <b>a</b>. Если она ломает ожидание, понадобится <b>ale</b>.", PALE, ROSE, SMALL),
    p("Ещё три модели", H2),
    styled_table([
        ["SK", "RU"],
        ["Ráno cvičím a večer čítam.", "Утром я занимаюсь, а вечером читаю."],
        ["Kurz je praktický a učiteľ vysvetľuje jasne.", "Курс практичный, и преподаватель объясняет ясно."],
        ["Sadli sme si a objednali sme si kávu.", "Мы сели и заказали кофе."],
    ], [85 * mm, 85 * mm], font_size=6.35),
    PageBreak(),

    p("2. Союз ale: поворачиваем мысль", H1),
    p("<b>Ale</b> соответствует \"но\" или контрастному \"а\". Первая часть создаёт ожидание, а вторая его ограничивает, исправляет или показывает противоположный факт."),
    styled_table([
        ["Ожидание", "Контраст с ale", "Перевод"],
        ["есть желание", "Chcem ísť, ale nemám čas.", "Я хочу пойти, но у меня нет времени."],
        ["качество +", "Hotel je pekný, ale drahý.", "Отель красивый, но дорогой."],
        ["обычная ситуация", "Je leto, ale dnes je chladno.", "Лето, но сегодня холодно."],
        ["ожидали результат", "Veľa som sa učil, ale test bol ťažký.", "Я много учился, но тест был трудным."],
        ["разные привычки", "Peter vstáva skoro, ale Jana spí dlho.", "Петер встаёт рано, а Яна долго спит."],
    ], [31 * mm, 72 * mm, 67 * mm], font_size=6.25),
    p("Главный сигнал: запятая", H2),
    p("Перед одиночным <b>ale</b> ставьте запятую: <b>Rozumiem, ale nesúhlasím.</b> Это надёжная практическая модель и внутри короткой фразы, и между двумя предложениями."),
    box("<b>Не усиливайте контраст случайно:</b> <i>Ja pracujem doma, ale sestra pracuje v kancelárii</i> звучит так, будто между фактами есть противопоставление. Для нейтрального сопоставления лучше <b>a</b>.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    p("Мягкий ответ", H2),
    p("<b>Ale</b> помогает сначала согласиться, а затем добавить ограничение: <b>To je dobrý nápad, ale dnes to nestihnem.</b> - Это хорошая идея, но сегодня я не успею. Такой ответ звучит естественнее резкого отказа."),
    PageBreak(),

    p("3. Союз alebo: предлагаем выбор", H1),
    p("<b>Alebo</b> соответствует \"или\". Он соединяет варианты: предметы, время, действия или целые решения. В обычной паре перед одиночным <b>alebo</b> запятая не нужна."),
    styled_table([
        ["Задача", "Словацкая модель", "Перевод"],
        ["выбор предмета", "Dáš si čaj alebo kávu?", "Будешь чай или кофе?"],
        ["выбор времени", "Stretneme sa dnes alebo zajtra?", "Встретимся сегодня или завтра?"],
        ["два действия", "Môžeme ísť pešo alebo cestovať autobusom.", "Можем пойти пешком или поехать автобусом."],
        ["альтернатива", "Zavolaj mi alebo mi napíš správu.", "Позвони мне или напиши сообщение."],
        ["решение", "Ponáhľaj sa, alebo zmeškáme vlak.", "Поторопись, иначе мы опоздаем на поезд."],
    ], [29 * mm, 76 * mm, 65 * mm], font_size=6.2),
    p("В вопросе: выбор или подтверждение?", H2),
    styled_table([
        ["Вопрос", "Что ожидает собеседник"],
        ["Chceš čaj alebo kávu?", "Выбрать один из названных вариантов."],
        ["Prídeš večer, alebo nie?", "Подтвердить или отрицать действие."],
        ["Pôjdeme pešo, alebo vezmeme taxík?", "Выбрать между двумя полными решениями."],
    ], [78 * mm, 92 * mm], font_size=6.45),
    p("Короткая карта пунктуации", H2),
    styled_table([
        ["Союз", "Обычная модель", "Запятая"],
        ["a", "čaj a káva; prišiel a sadol si", "обычно нет"],
        ["ale", "chcem, ale nemôžem", "ставим перед ale"],
        ["alebo", "dnes alebo zajtra", "обычно нет"],
    ], [24 * mm, 94 * mm, 52 * mm], font_size=6.35),
    box("<b>Практическое ограничение A2:</b> эта карта покрывает нейтральные одиночные союзы. Парные и повторяющиеся конструкции будут отдельно в теме 5.2.", PALE, PINK, SMALL),
    PageBreak(),

    p("4. Строим короткое связное высказывание", H1),
    p("Сначала решите, какую работу выполняет каждая связь. Не переводите русский союз механически: обозначьте добавление, контраст или выбор, а затем выберите словацкий союз."),
    styled_table([
        ["Шаг", "Вопрос к себе", "Пример"],
        ["1. Основа", "Какие два факта я сообщаю?", "V sobotu mám voľno. Chcem ísť von."],
        ["2. Связь", "Они совместимы или конфликтуют?", "Совместимы: a."],
        ["3. Продолжение", "Есть препятствие или выбор?", "Prší: ale. Kino či múzeum: alebo."],
        ["4. Фраза", "Логика слышна без пояснений?", "Mám voľno a chcem ísť von, ale prší."],
    ], [27 * mm, 66 * mm, 77 * mm], font_size=6.25),
    p("Мини-диалог: план на вечер", H2),
    box("<b>Marta:</b> Dnes mám voľno a chcela by som ísť von.<br/><b>Ivan:</b> Môžeme ísť do kina alebo na koncert.<br/><b>Marta:</b> Koncert je zaujímavý, ale lístky sú drahé.<br/><b>Ivan:</b> Tak pôjdeme do kina a potom si dáme večeru.<br/><b>Marta:</b> Dobre. Kúpime lístky online alebo pri pokladni?<br/><b>Ivan:</b> Kúpme ich online, ale najprv vyberme film.", PALE, ROSE, SMALL),
    p("Перевод", H2),
    p("Сегодня я свободна и хотела бы куда-нибудь пойти. Мы можем пойти в кино или на концерт. Концерт интересный, но билеты дорогие. Тогда пойдём в кино, а потом поужинаем. Купим билеты онлайн или в кассе? Купим онлайн, но сначала выберем фильм.", SMALL),
    p("Модель короткого сообщения", H2),
    box("<b>V piatok končím o piatej a potom mám voľno. Môžeme sa stretnúť v centre alebo pri stanici. Centrum je bližšie, ale býva tam veľa ľudí. Napíš mi a dohodneme sa.</b><br/>В пятницу я заканчиваю в пять и потом свободен. Можем встретиться в центре или у вокзала. Центр ближе, но там обычно много людей. Напиши мне, и мы договоримся.", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    PageBreak(),

    p("5. Частые ошибки и упражнения", H1),
    box("<b>Частые ошибки:</b> нейтральное русское \"а\" переводят как *ale; забывают запятую перед <b>ale</b>; ставят лишнюю запятую в <b>čaj alebo kávu</b>; выбирают союз по русскому слову, а не по логике.", CREAM, colors.HexColor("#E7C76C"), TINY),
    p("Упражнение 1. Определите связь", H2),
    p("Пометьте: добавление, контраст или выбор. 1) Byt je malý, ___ útulný. 2) Dáš si vodu ___ džús? 3) Prišiel domov ___ uvaril večeru. 4) Chcem pomôcť, ___ neviem ako.", TINY),
    p("Упражнение 2. Вставьте a, ale или alebo", H2),
    p("1) Ráno pracujem ___ večer študujem. 2) Zavoláš mi ___ mi napíšeš? 3) Jedlo je chutné, ___ porcia je malá. 4) Otvorila dvere ___ vošla dnu. 5) Pôjdeme vlakom ___ autobusom?", TINY),
    p("Упражнение 3. Поставьте запятые", H2),
    p("1) Mám čas ale som unavený. 2) Kúpime chlieb a syr. 3) Prídeš dnes alebo zajtra? 4) Izba je čistá ale veľmi malá.", TINY),
    p("Упражнение 4. Исправьте союз", H2),
    p("1) Ja bývam v Košiciach, ale brat býva v Žiline. (нейтрально) 2) Chcem spať a musím pracovať. (контраст) 3) Dáš si polievku, ale šalát? (выбор)", TINY),
    p("Упражнение 5. Переведите", H2),
    p("1) Квартира светлая, но дорогая. 2) Позвони мне или напиши сообщение. 3) Утром я работаю, а вечером учусь. 4) Мы можем остаться дома или пойти в кино.", TINY),
    p("Упражнение 6. Ваш план", H2),
    p("Напишите 5-7 связанных предложений о плане на выходной. Используйте <b>a</b> минимум дважды, <b>ale</b> для одного ограничения и <b>alebo</b> для одного выбора.", TINY),
    PageBreak(),

    p("6. Ответы и проверка мастерства", H1),
    p("Ответы", H2),
    p("<b>1.</b> 1) контраст: ale; 2) выбор: alebo; 3) добавление/последовательность: a; 4) контраст: ale.", TINY),
    p("<b>2.</b> 1) a; 2) alebo; 3) ale; 4) a; 5) alebo.", TINY),
    p("<b>3.</b> 1) Mám čas, ale som unavený. 2) Kúpime chlieb a syr. 3) Prídeš dnes alebo zajtra? 4) Izba je čistá, ale veľmi malá.", TINY),
    p("<b>4.</b> 1) Ja bývam v Košiciach a brat býva v Žiline. 2) Chcem spať, ale musím pracovať. 3) Dáš si polievku alebo šalát?", TINY),
    p("<b>5.</b> 1) Byt je svetlý, ale drahý. 2) Zavolaj mi alebo mi napíš správu. 3) Ráno pracujem a večer študujem. 4) Môžeme zostať doma alebo ísť do kina.", TINY),
    p("<b>6. Модель:</b> V sobotu mám voľno a chcem si oddýchnuť. Ráno si zacvičím a potom pripravím raňajky. Chcel by som ísť na výlet, ale možno bude pršať. Môžem navštíviť múzeum alebo zostať doma. Večer zavolám kamarátovi a dohodneme sa. Возможны другие естественные варианты.", TINY),
    p("Итог в четырёх пунктах", H2),
    styled_table([
        ["OK", "A соединяет совместимые факты, признаки и действия."],
        ["OK", "Ale показывает контраст; перед ним ставлю запятую."],
        ["OK", "Alebo предлагает выбор; в простой паре запятая не нужна."],
        ["OK", "Сначала определяю логику, затем выбираю союз."],
    ], [12 * mm, 158 * mm], font_size=6.55, header=False),
    Spacer(1, 2 * mm),
    box("<b>Финальная проверка:</b> без подсказки соедините четыре мысли: вы свободны; хотите встретиться; на улице дождь; можно выбрать кафе или кино. Используйте все три союза.", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    p("Следующий шаг", H2),
    p("В теме 5.2 вы научитесь подчёркивать включение и исключение с парными союзами <b>aj - aj</b> и <b>ani - ani</b>.", SMALL),
]

doc.build(story)
print(OUTPUT)
