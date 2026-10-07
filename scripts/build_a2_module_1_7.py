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
OUTPUT = ROOT / "output" / "pdf" / "A2" / "Module_01" / "Slovak_A2_Tema_1_7_Proiznoshenie_svyaznaya_rech.pdf"
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
TITLE = ParagraphStyle("Title", fontName="Arial-Bold", fontSize=24, leading=28, textColor=colors.white, alignment=TA_LEFT, spaceAfter=5 * mm)
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
        canvas.drawString(20 * mm, height - 12 * mm, "SLOVAK A2  |  ТЕМА 1.7")
        canvas.drawRightString(width - 20 * mm, height - 12 * mm, "Произношение: связная речь")
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
    title="Slovak A2 - Тема 1.7 - Произношение A2: связная речь", author="SlovoKrok",
)
frame = Frame(20 * mm, 18 * mm, 170 * mm, 257 * mm, id="main", leftPadding=0, rightPadding=0)
doc.addPageTemplates([PageTemplate(id="series", frames=[frame], onPage=draw_page)])

story = [
    p("МОДУЛЬ 1  •  ПЕРЕХОД ОТ A1 К A2", COVER_KICKER),
    p("Произношение A2:<br/>связная речь", TITLE),
    p("Výslovnosť A2: súvislá reč", SUBTITLE),
    Spacer(1, 37 * mm),
    p("На A2 важно произнести не только отдельное слово, но и длинную фразу: сохранить долготу, соединить согласные, выделить смысл и закончить предложение правильной мелодией.", BODY),
    p("После модуля вы сможете:", H2),
    styled_table([
        ["1", "слышать и применять оглушение и озвончение в потоке речи"],
        ["2", "произносить группы согласных без вставных гласных"],
        ["3", "различать долготу и ударение, учитывать ритмическое сокращение"],
        ["4", "делить длинную фразу на группы и выбирать мелодию сообщения или вопроса"],
    ], [12 * mm, 158 * mm], font_size=8.2, header=False),
    Spacer(1, 4 * mm),
    box("<b>Главная формула:</b> смысловая группа -> чёткие звуки -> сохранённая долгота -> одно главное ударение -> завершённая мелодия.", PALE, PINK),
    PageBreak(),

    p("1. Оглушение и озвончение", H1),
    p("В связной речи соседние шумные согласные подстраиваются по звонкости. Пишем слово как обычно, но произносим стык слитно. Подсказки в квадратных скобках здесь учебные, а не строгая фонетическая транскрипция.", BODY),
    styled_table([
        ["Позиция", "Написание -> звучание", "Пример и перевод"],
        ["в конце перед паузой", "b -> p, d -> t, z -> s, ž -> š", "<b>hrad</b> [hrat] - замок; <b>dub</b> [dup] - дуб"],
        ["перед глухим", "звонкий -> глухой", "<b>pod stolom</b> [pot stolom] - под столом"],
        ["перед звонким", "глухой -> звонкий", "<b>prosba</b> [prozba] - просьба"],
        ["предлог s", "s -> z перед звонким", "<b>s bratom</b> [z bratom] - с братом"],
        ["предлог z", "z -> s перед глухим", "<b>z práce</b> [s práce] - с работы"],
        ["между словами", "стык работает без паузы", "<b>vlak ide</b> [vlag ide] - поезд едет"],
    ], [35 * mm, 54 * mm, 81 * mm], font_size=7.1),
    p("Главные пары", H2),
    styled_table([
        ["Глухая", "p", "f", "t", "s", "c", "š", "č", "ť", "k", "ch"],
        ["Звонкая", "b", "v", "d", "z", "dz", "ž", "dž", "ď", "g", "h"],
    ], [30 * mm] + [14 * mm] * 10, font_size=7.2, header=False),
    Spacer(1, 4 * mm),
    box("<b>Не переносите звучание в письмо.</b> Произносим [pot stolom], но пишем <b>pod stolom</b>. Если между словами есть смысловая пауза, стык может не объединяться.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    PageBreak(),

    p("2. Группы согласных и речевые такты", H1),
    p("В русском хочется вставить гласный или проглотить часть группы. В словацком лучше замедлиться и пройти согласные по порядку, не добавляя лишнее <i>ы</i> или <i>э</i>.", BODY),
    styled_table([
        ["Слово", "Деление для тренировки", "Перевод"],
        ["štvrtok", "štvr-tok", "четверг"],
        ["štvrť", "один слог; r несёт слог", "четверть"],
        ["prst", "один слог; r несёт слог", "палец"],
        ["vlk", "один слог; l несёт слог", "волк"],
        ["vstup", "v-stup, без гласной после v", "вход"],
        ["stretnúť", "stret-núť", "встретить"],
        ["zdravotný", "zdra-vot-ný", "медицинский"],
    ], [38 * mm, 72 * mm, 60 * mm], font_size=7.2),
    p("Не слово за словом, а группами", H2),
    styled_table([
        ["Запись", "Как читать", "Перевод"],
        ["V stredu stretneme nových kolegov.", "V stredu / stretneme nových kolegov.", "В среду мы встретим новых коллег."],
        ["Štvrtý vlak odchádza o štvrť na štyri.", "Štvrtý vlak / odchádza / o štvrť na štyri.", "Четвёртый поезд отправляется в четверть четвёртого."],
        ["Dnes ráno som išiel do práce novým autobusom.", "Dnes ráno / som išiel do práce / novým autobusom.", "Сегодня утром я ехал на работу новым автобусом."],
        ["Po stretnutí vám pošlem všetky dokumenty.", "Po stretnutí / vám pošlem / všetky dokumenty.", "После встречи я пришлю вам все документы."],
    ], [63 * mm, 66 * mm, 41 * mm], font_size=6.95),
    Spacer(1, 4 * mm),
    box("<b>Техника:</b> сначала прочитайте каждый такт отдельно, затем соедините. Пауза обозначена знаком /. Внутри такта не останавливайтесь перед трудной группой.", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    PageBreak(),

    p("3. Долгота, ударение и ритм", H1),
    p("Долгая гласная длится заметно дольше, но не обязана нести ударение. Словацкое словесное ударение обычно падает на первый слог; знак долготы показывает количество, а не силу.", BODY),
    styled_table([
        ["Контраст", "Значение", "Фраза"],
        ["rad - rád", "совет - рад", "Dám ti radu. - Rád ti pomôžem."],
        ["sud - súd", "бочка - суд", "Sud je plný. - Súd rozhodol."],
        ["dom - dóm", "дом - собор", "To je dom. - To je starý dóm."],
        ["pani - páni", "госпожа - господа", "Tá pani čaká. - Tí páni čakajú."],
        ["drahá - dráha", "дорогая - трасса/путь", "Drahá cesta. - Dlhá dráha."],
    ], [35 * mm, 50 * mm, 85 * mm], font_size=7.1),
    p("Ритмический закон", H2),
    p("Внутри слова две долгие слоговые вершины обычно не стоят подряд. Поэтому после долгого корня окончание часто сокращается. Это продуктивная подсказка, но у правила есть исключения.", SMALL),
    styled_table([
        ["Короткая основа", "Долгая основа", "Что слышим"],
        ["pekná, pekný", "krásna, krásny", "после krás- окончание короткое"],
        ["červená, červený", "biela, biely", "ie уже делает первый слог долгим"],
        ["nosím", "súdim", "после súd- личное окончание короткое"],
    ], [53 * mm, 53 * mm, 64 * mm], font_size=7.2),
    Spacer(1, 3 * mm),
    box("<b>Ловушка для русскоязычных:</b> не растягивайте ударный слог автоматически и не сокращайте á/í/ú в безударной позиции. В <b>slovenčina</b> ударение в начале, а в <b>hovorím</b> í всё равно долгое.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    PageBreak(),

    p("4. Интонация длинной фразы", H1),
    p("Интонация объединяет слова в сообщение. Сначала определите тип фразы, затем смысловые группы и только после этого главное слово.", BODY),
    styled_table([
        ["Тип", "Мелодия", "Пример и перевод"],
        ["сообщение", "в конце тон уверенно идёт вниз", "Zajtra pracujem doma. - Завтра я работаю дома."],
        ["вопрос без вопросительного слова", "для A2: тон к концу идёт вверх", "Prídeš zajtra? - Ты придёшь завтра?"],
        ["вопрос с kto, čo, kde, kedy...", "обычно тон идёт вниз", "Kedy prídeš? - Когда ты придёшь?"],
        ["контраст", "главное слово сильнее, конец завершён", "Prídem ZAJTRA, nie dnes. - Я приду ЗАВТРА, не сегодня."],
    ], [41 * mm, 57 * mm, 72 * mm], font_size=7.15),
    p("Модель чтения", H2),
    box("<b>Dnes popoludní / máme dôležité stretnutie.</b> Тон продолжается после первого такта и падает только в конце.<br/><b>Príde aj nový kolega?</b> Вопрос без вопросительного слова: конец поднимается.<br/><b>Kedy sa stretnutie začne?</b> Вопросительное слово уже показывает вопрос: конец обычно опускается.<br/><b>Stretnutie sa začne o TRETEJ, nie o štvrtej.</b> Голосом выделяем исправленную информацию.", ALT, ROSE, SMALL),
    p("Мини-диалог с разметкой", H2),
    box("<b>A:</b> Kedy odchádza vlak?<br/><b>B:</b> Vlak odchádza / o štvrť na štyri.<br/><b>A:</b> Ide priamo do Bratislavy?<br/><b>B:</b> Nie. V Trnave / musíme prestúpiť.<br/><b>A:</b> Máme dosť času?<br/><b>B:</b> Áno, / máme dvadsať minút.", PALE, ROSE, SMALL),
    p("Перевод: Когда отправляется поезд? - В четверть четвёртого. - Он идёт прямо в Братиславу? - Нет, в Трнаве нужно пересесть. - У нас достаточно времени? - Да, двадцать минут.", SMALL),
    PageBreak(),

    p("5. Частые ошибки и упражнения", H1),
    box("<b>Четыре ошибки:</b> читать точно по буквам без ассимиляции; вставлять гласную в группу согласных; путать долготу с ударением; поднимать тон в каждом вопросе.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    p("Упражнение 1. Выберите звучание", H2),
    p("1) pod stolom: [pod] или [pot]? 2) s bratom: [s] или [z]? 3) z práce: [z] или [s]? 4) prosba: [prosba] или [prozba]? 5) hrad перед паузой: [hrad] или [hrat]?", SMALL),
    p("Упражнение 2. Сохраните различие", H2),
    p("Прочитайте пары и объясните значение: 1) rad - rád; 2) sud - súd; 3) dom - dóm; 4) pani - páni; 5) drahá - dráha.", SMALL),
    p("Упражнение 3. Разделите на такты", H2),
    p("1) Zajtra ráno pôjdeme vlakom do Bratislavy. 2) Po stretnutí vám pošlem všetky dokumenty. 3) V piatok večer sa stretneme pred kinom.", SMALL),
    p("Упражнение 4. Выберите мелодию", H2),
    p("Тон вниз или вверх: 1) Zajtra pracujem doma. 2) Prídeš zajtra? 3) Kedy prídeš? 4) Máte voľnú izbu?", SMALL),
    p("Упражнение 5. Исправьте чтение", H2),
    p("1) [pod stolom] без оглушения. 2) [s bratom] без озвончения. 3) št-vr-tok со вставными гласными. 4) hovorím: ударение на последнем í. 5) Kde bývate? с обязательным подъёмом в конце.", SMALL),
    p("Упражнение 6. Запишите себя", H2),
    p("Подготовьте 5-7 предложений о поездке или рабочем дне. Отметьте / границы тактов, подчеркните долгие гласные и одно главное слово. Запишите два чтения и сравните разборчивость.", SMALL),
    PageBreak(),

    p("6. Ответы и проверка мастерства", H1),
    p("Ответы", H2),
    p("<b>1.</b> 1) [pot]; 2) [z]; 3) [s]; 4) [prozba]; 5) [hrat].", TINY),
    p("<b>2.</b> rad - совет, rád - рад; sud - бочка, súd - суд; dom - дом, dóm - собор; pani - госпожа, páni - господа; drahá - дорогая, dráha - путь или трасса.", TINY),
    p("<b>3. Возможное деление:</b> 1) Zajtra ráno / pôjdeme vlakom / do Bratislavy. 2) Po stretnutí / vám pošlem / všetky dokumenty. 3) V piatok večer / sa stretneme / pred kinom.", TINY),
    p("<b>4.</b> 1) вниз; 2) вверх; 3) обычно вниз; 4) вверх.", TINY),
    p("<b>5.</b> 1) [pot stolom]; 2) [z bratom]; 3) štvr-tok, без вставной гласной; 4) ударение на первом слоге, í остаётся долгим; 5) вопросительное слово <i>kde</i> позволяет обычное понижение в конце.", TINY),
    p("<b>6. Модель разметки:</b> Dnes ráno / som išiel do PRÁCE / novým autobusom. Cesta bola dlhá, / ale pokojná. Prišiel som načas / a pripravil som dokumenty. Po stretnutí / som zavolal kolegovi. Večer / som sa vrátil domov.", TINY),
    p("Итог в четырёх пунктах", H2),
    styled_table([
        ["OK", "Я соединяю согласные и применяю оглушение или озвончение."],
        ["OK", "Я не вставляю гласные в группы и читаю фразу тактами."],
        ["OK", "Я сохраняю долготу независимо от словесного ударения."],
        ["OK", "Я различаю мелодию сообщения, общего и специального вопроса."],
    ], [12 * mm, 158 * mm], font_size=7.7, header=False),
    Spacer(1, 3 * mm),
    box("<b>Финальная проверка:</b> запись понятна без текста, долгие гласные различимы, внутри такта нет лишних пауз, а слушатель слышит, где сообщение закончилось и что в нём главное.", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    p("Следующий шаг", H2),
    p("Переходите к модулю 2.1: Nominatív множественного числа для предметов и понятий. Новые формы сразу читайте в коротких смысловых группах.", SMALL),
]

doc.build(story)
print(OUTPUT)
