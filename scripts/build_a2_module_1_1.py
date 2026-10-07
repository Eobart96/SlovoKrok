from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    KeepTogether,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output" / "pdf" / "A2" / "Module_01" / "Slovak_A2_Tema_1_1_Gotovnost_k_A2.pdf"
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
pdfmetrics.registerFont(TTFont("Arial-Italic", r"C:\Windows\Fonts\ariali.ttf"))

styles = getSampleStyleSheet()
BODY = ParagraphStyle(
    "Body", fontName="Arial", fontSize=9.1, leading=12.3, textColor=INK,
    spaceAfter=4.5 * mm,
)
SMALL = ParagraphStyle(
    "Small", parent=BODY, fontSize=8.0, leading=10.2, spaceAfter=2.2 * mm,
)
TITLE = ParagraphStyle(
    "Title", fontName="Arial-Bold", fontSize=25, leading=29, textColor=colors.white,
    alignment=TA_LEFT, spaceAfter=5 * mm,
)
SUBTITLE = ParagraphStyle(
    "Subtitle", fontName="Arial", fontSize=12, leading=16,
    textColor=colors.HexColor("#FFD8EB"), spaceAfter=5 * mm,
)
H1 = ParagraphStyle(
    "H1", fontName="Arial-Bold", fontSize=16, leading=19, textColor=PLUM,
    spaceBefore=1 * mm, spaceAfter=4 * mm,
)
H2 = ParagraphStyle(
    "H2", fontName="Arial-Bold", fontSize=11.2, leading=14, textColor=PINK,
    spaceBefore=2 * mm, spaceAfter=2.2 * mm,
)
CENTER = ParagraphStyle("Center", parent=BODY, alignment=TA_CENTER)
COVER_KICKER = ParagraphStyle(
    "CoverKicker", fontName="Arial-Bold", fontSize=10, leading=12,
    textColor=colors.HexColor("#FFD8EB"), spaceAfter=4 * mm,
)
WHITE_SMALL = ParagraphStyle(
    "WhiteSmall", fontName="Arial", fontSize=8.5, leading=11, textColor=colors.white,
)


def p(text, style=BODY):
    return Paragraph(text, style)


def box(text, background=PALE, border=ROSE, style=BODY, padding=7):
    table = Table([[p(text, style)]], colWidths=[170 * mm])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), background),
        ("BOX", (0, 0), (-1, -1), 0.7, border),
        ("LEFTPADDING", (0, 0), (-1, -1), padding),
        ("RIGHTPADDING", (0, 0), (-1, -1), padding),
        ("TOPPADDING", (0, 0), (-1, -1), padding),
        ("BOTTOMPADDING", (0, 0), (-1, -1), padding),
    ]))
    return table


def styled_table(data, widths, font_size=7.8, header=True):
    converted = []
    for row_index, row in enumerate(data):
        style = ParagraphStyle(
            f"Cell{row_index}", parent=SMALL, fontSize=font_size,
            leading=font_size + 2.0, textColor=(colors.white if header and row_index == 0 else INK),
            fontName=("Arial-Bold" if header and row_index == 0 else "Arial"),
            spaceAfter=0,
        )
        converted.append([p(str(cell), style) for cell in row])
    table = Table(converted, colWidths=widths, repeatRows=1 if header else 0)
    commands = [
        ("GRID", (0, 0), (-1, -1), 0.45, ROSE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
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
        canvas.drawString(20 * mm, height - 12 * mm, "SLOVAK A2  |  ТЕМА 1.1")
        canvas.drawRightString(width - 20 * mm, height - 12 * mm, "Диагностический мост A1 -> A2")
    canvas.setStrokeColor(PINK)
    canvas.setLineWidth(0.6)
    canvas.line(20 * mm, 14 * mm, width - 20 * mm, 14 * mm)
    canvas.setFont("Arial", 7.8)
    canvas.setFillColor(MUTED)
    canvas.drawString(20 * mm, 9 * mm, "SlovoKrok | личный учебный модуль")
    canvas.drawRightString(width - 20 * mm, 9 * mm, f"стр. {page} / 7")
    canvas.restoreState()


doc = BaseDocTemplate(
    str(OUTPUT), pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm,
    topMargin=20 * mm, bottomMargin=18 * mm,
    title="Slovak A2 - Тема 1.1 - Что нужно уметь перед A2",
    author="SlovoKrok",
)
frame = Frame(20 * mm, 18 * mm, 170 * mm, 257 * mm, id="main", leftPadding=0, rightPadding=0)
doc.addPageTemplates([PageTemplate(id="series", frames=[frame], onPage=draw_page)])

story = []

# Page 1
story += [
    p("МОДУЛЬ 1  •  ПЕРЕХОД ОТ A1 К A2", COVER_KICKER),
    p("Что нужно уметь<br/>перед A2", TITLE),
    p("Čo treba vedieť pred úrovňou A2", SUBTITLE),
    Spacer(1, 31 * mm),
    p("Это не экзамен и не повтор всего A1. Вы быстро проверите фундамент и увидите, какие темы стоит освежить перед новой грамматикой.", BODY),
    p("После модуля вы сможете:", H2),
    styled_table([
        ["1", "проверить падежные вопросы и базовое согласование"],
        ["2", "вспомнить настоящее, прошедшее и будущее время"],
        ["3", "оценить бытовую самостоятельность на словацком"],
        ["4", "составить личный маршрут подготовки к A2"],
    ], [12 * mm, 158 * mm], font_size=8.4, header=False),
    Spacer(1, 5 * mm),
    box("<b>Главная формула:</b> A2 = знакомая основа A1 + больше связности + точнее формы + самостоятельнее действие.", PALE, PINK),
    Spacer(1, 4 * mm),
    p("Маршрут: самооценка -> грамматика -> глаголы -> общение -> упражнения -> ответы.", SMALL),
    PageBreak(),
]

# Page 2
story += [
    p("1. Быстрая карта готовности", H1),
    p("Поставьте себе 0, 1 или 2 балла: <b>0</b> - не могу; <b>1</b> - могу с подсказкой; <b>2</b> - могу самостоятельно. Не угадывайте правило: попробуйте вслух сказать пример.", BODY),
    styled_table([
        ["Навык", "Попробуйте сказать или сделать", "0-2"],
        ["Представиться", "Volám sa Ari. Bývam na Slovensku. Učím sa po slovensky.", ""],
        ["Спросить", "Kde bývate? Kedy prídete? Koľko to stojí?", ""],
        ["Описать", "Môj byt je malý, ale svetlý.", ""],
        ["Рассказать о вчера", "Včera som pracoval/pracovala a potom som oddychoval/oddychovala.", ""],
        ["Сказать о плане", "Zajtra budem študovať. Večer pôjdem do obchodu.", ""],
        ["Попросить", "Mohli by ste mi pomôcť, prosím?", ""],
        ["Понять сообщение", "Stretneme sa o šiestej pred stanicou.", ""],
        ["Передать информацию", "Peter povedal, že príde neskôr.", ""],
    ], [35 * mm, 119 * mm, 16 * mm], font_size=7.6),
    Spacer(1, 4 * mm),
    box("<b>Ориентир:</b> 13-16 баллов - можно уверенно начинать A2. 8-12 - начинайте A2 и точечно повторяйте слабые места. 0-7 - сначала освежите соответствующие темы A1.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    p("Что изменится на A2", H2),
    bullet("Вы будете не только называть форму, но и выбирать её по смыслу."),
    bullet("Ответ станет длиннее: обычно 4-8 связанных предложений."),
    bullet("Появятся объяснение причины, сравнение, совет и передача чужой информации."),
    PageBreak(),
]

# Page 3
story += [
    p("2. Падежи и согласование: фундамент", H1),
    p("На A2 важно не перечислить окончания, а узнать роль слова. Сначала задайте смысловой вопрос, затем проверьте предлог или управление глагола.", BODY),
    styled_table([
        ["Функция", "Вопрос", "Пример", "Перевод"],
        ["Субъект", "kto? čo?", "Nový kolega pracuje doma.", "Новый коллега работает дома."],
        ["Прямой объект", "koho? čo?", "Hľadám nového kolegu.", "Я ищу нового коллегу."],
        ["Адресат", "komu? čomu?", "Píšem novej kolegyni.", "Я пишу новой коллеге."],
        ["Место / тема", "o kom? o čom?", "Hovoríme o novej práci.", "Мы говорим о новой работе."],
        ["Совместность", "s kým? s čím?", "Idem s dobrým kamarátom.", "Я иду с хорошим другом."],
        ["Происхождение", "odkiaľ?", "Vraciame sa z veľkého mesta.", "Мы возвращаемся из большого города."],
    ], [28 * mm, 23 * mm, 57 * mm, 62 * mm], font_size=7.15),
    Spacer(1, 3 * mm),
    box("<b>Проверка согласования:</b> меняется не только существительное. Сравните: <b>nový kolega -> nového kolegu -> novému kolegovi -> o novom kolegovi -> s novým kolegom</b>.", PALE, PINK, SMALL),
    p("Мини-проверка", H2),
    p("Закончите формы устно, затем сверьтесь с ответами: 1) Vidím (moja nová suseda). 2) Rozprávam sa s (môj dobrý priateľ). 3) Bývame v (malé mesto). 4) Píšem (nová kolegyňa).", BODY),
    p("Сигнал для повторения", H2),
    p("Если вы выбираете окончание только по русскому переводу, вернитесь к вопросам падежей A1. В A2 мы добавим множественное число, полное согласование и формы местоимений.", BODY),
    p("Алгоритм выбора формы", H2),
    styled_table([
        ["1", "Найдите главное действие или предлог."],
        ["2", "Задайте словацкий вопрос: koho? komu? o kom? s kým?"],
        ["3", "Измените существительное, прилагательное и местоимение вместе."],
        ["4", "Прочитайте фразу целиком и проверьте, сохранился ли смысл."],
    ], [12 * mm, 158 * mm], font_size=8.0, header=False),
    PageBreak(),
]

# Page 4
story += [
    p("3. Глаголы: время, вид и намерение", H1),
    p("На A1 вы научились располагать действие во времени. На A2 к этому добавится вид: процесс или результат.", BODY),
    styled_table([
        ["Задача", "Модель", "Пример", "Перевод"],
        ["Сейчас / обычно", "prézent", "Každý deň čítam po slovensky.", "Каждый день я читаю по-словацки."],
        ["Прошедший процесс", "imperfektívum", "Včera som čítal/čítala knihu.", "Вчера я читал/читала книгу."],
        ["Прошедший результат", "perfektívum", "Knihu som už prečítal/prečítala.", "Я уже прочитал/прочитала книгу."],
        ["Будущий процесс", "budem + infinitív", "Večer budem písať email.", "Вечером я буду писать письмо."],
        ["Будущий результат", "совершенная форма", "Večer napíšem email.", "Вечером я напишу письмо."],
        ["Вежливая просьба", "mohol by som", "Mohol by som dostať účet?", "Можно мне счёт?"],
    ], [30 * mm, 35 * mm, 55 * mm, 50 * mm], font_size=7.05),
    Spacer(1, 3 * mm),
    box("<b>Важно:</b> форма <b>napíšem</b> похожа на настоящее время, но совершенный глагол здесь сообщает о будущем результате.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    p("Три опоры перед A2", H2),
    bullet("Прошедшее: <b>som/si/sme/ste</b> и согласование по роду."),
    bullet("Будущее процесса: <b>budem + infinitív</b>."),
    bullet("Модальность: <b>chcem, môžem, musím, viem + infinitív</b>."),
    p("Мини-проверка", H2),
    p("Объясните разницу: <b>Budem telefonovať Petrovi.</b> / <b>Zavolám Petrovi.</b> Затем скажите по одному своему примеру на вчера, сегодня и завтра.", BODY),
    p("Как увидеть видовую пару", H2),
    styled_table([
        ["Процесс / повтор", "Результат", "Смысловой контраст"],
        ["písať", "napísať", "писать - написать"],
        ["čítať", "prečítať", "читать - прочитать"],
        ["kupovať", "kúpiť", "покупать - купить"],
    ], [49 * mm, 45 * mm, 76 * mm], font_size=7.8),
    Spacer(1, 3 * mm),
    box("<b>Личная проба:</b> выберите одно дело на завтра и скажите две версии: что вы будете делать и какого результата достигнете. Например: <b>Budem čítať článok. Prečítam ho večer.</b>", PALE, PINK, SMALL),
    PageBreak(),
]

# Page 5
story += [
    p("4. Общение: от фразы к задаче", H1),
    p("A2 начинается там, где отдельные правильные фразы складываются в самостоятельное действие: уточнить, объяснить, договориться и передать информацию.", BODY),
    styled_table([
        ["Функция", "Словацкая модель", "Естественный перевод"],
        ["Уточнить", "Prepáčte, môžete to zopakovať?", "Извините, можете повторить?"],
        ["Попросить проще", "Môžete to povedať jednoduchšie?", "Можете сказать это проще?"],
        ["Проверить", "Rozumiem správne, že stretnutie je zajtra?", "Я правильно понимаю, что встреча завтра?"],
        ["Объяснить причину", "Meškám, pretože autobus neprišiel.", "Я опаздываю, потому что автобус не пришёл."],
        ["Предложить", "Mohli by sme sa stretnúť o siedmej.", "Мы могли бы встретиться в семь."],
        ["Согласиться", "To mi vyhovuje. Platí.", "Мне подходит. Договорились."],
        ["Не согласиться", "Mrzí ma to, ale vtedy nemôžem.", "Мне жаль, но тогда я не могу."],
        ["Передать", "Anna povedala, že príde neskôr.", "Анна сказала, что придёт позже."],
    ], [31 * mm, 72 * mm, 67 * mm], font_size=7.2),
    Spacer(1, 3 * mm),
    p("Мини-диалог", H2),
    box("<b>A:</b> Dobrý deň, volám kvôli zajtrajšiemu stretnutiu.<br/><b>B:</b> Áno, počúvam.<br/><b>A:</b> Mohli by sme ho presunúť na tretiu?<br/><b>B:</b> Áno, tretia mi vyhovuje.<br/><b>A:</b> Ďakujem. Poviem kolegyni, že sa stretneme o tretej.", ALT, ROSE, SMALL),
    p("Проверьте себя", H2),
    p("Можете ли вы без перевода: 1) попросить повторить; 2) назвать причину; 3) предложить другое время; 4) передать договорённость третьему человеку?", BODY),
    p("Связки для короткого рассказа", H2),
    styled_table([
        ["Задача", "Связки", "Пример"],
        ["Порядок", "najprv, potom, nakoniec", "Najprv pracujem, potom oddychujem."],
        ["Контраст", "ale", "Chcem prísť, ale nemám čas."],
        ["Причина", "pretože", "Učím sa, pretože tu bývam."],
        ["Следствие", "preto", "Som chorý, preto zostanem doma."],
    ], [30 * mm, 48 * mm, 92 * mm], font_size=7.4),
    Spacer(1, 3 * mm),
    box("<b>Задача на 60 секунд:</b> расскажите, как пройдёт ваш завтрашний день. Используйте минимум три связки из таблицы.", ALT, ROSE, SMALL),
    PageBreak(),
]

# Page 6
story += [
    p("5. Диагностические упражнения", H1),
    p("Выполните без подсказок. Ответы находятся только на следующей странице.", BODY),
    p("Упражнение 1. Выберите форму", H2),
    p("1) Hľadám (nový kolega / nového kolegu). 2) Bývame (v malé mesto / v malom meste). 3) Píšem (moja sestra / mojej sestre). 4) Idem (s dobrým kamarátom / dobrého kamaráta).", SMALL),
    p("Упражнение 2. Поставьте глагол в прошлое время", H2),
    p("1) Ja (pracovať) doma. 2) My (stretnúť sa) v centre. 3) Anna (kúpiť) lístok. 4) Peter a Ján (prísť) neskoro.", SMALL),
    p("Упражнение 3. Процесс или результат?", H2),
    p("Выберите: 1) Večer budem písať / napíšem email a potom ho pošlem. 2) Zajtra budem čítať / prečítam dve hodiny. 3) Každý deň kupujem / kúpim chlieb.", SMALL),
    p("Упражнение 4. Соедините мысли", H2),
    p("Соедините с <b>ale, pretože, preto, že</b>: 1) Nemôžem prísť. Som chorý/chorá. 2) Mám čas. Pomôžem ti. 3) Peter povedal. Príde o šiestej.", SMALL),
    p("Упражнение 5. Переведите на словацкий", H2),
    p("1) Мы живём в маленьком городе. 2) Вчера я написал/написала коллеге. 3) Не могли бы вы повторить? 4) Анна сказала, что придёт позже.", SMALL),
    p("Упражнение 6. Самостоятельная задача", H2),
    p("Напишите 5-6 предложений: кто вы, где живёте, что делали вчера, что будете делать завтра и зачем вам словацкий. Добавьте одну причину с <b>pretože</b> и одну вежливую просьбу.", SMALL),
    box("Если вы уверенно выполнили 4 задания из 6, начинайте A2. Ошибки не запрещают двигаться дальше: отметьте их как личные темы повторения.", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    Spacer(1, 4 * mm),
    p("Мои заметки", H2),
    styled_table([
        ["Самое лёгкое", ""],
        ["Нужно повторить", ""],
        ["Мой первый шаг", ""],
    ], [45 * mm, 125 * mm], font_size=8.0, header=False),
    PageBreak(),
]

# Page 7
story += [
    p("6. Ответы и личный маршрут", H1),
    p("Ответы", H2),
    p("<b>1.</b> 1) nového kolegu; 2) v malom meste; 3) mojej sestre; 4) s dobrým kamarátom.", SMALL),
    p("<b>2.</b> 1) Pracoval som / Pracovala som doma. 2) Stretli sme sa v centre. 3) Anna kúpila lístok. 4) Peter a Ján prišli neskoro.", SMALL),
    p("<b>3.</b> 1) napíšem; 2) budem čítať; 3) kupujem.", SMALL),
    p("<b>4.</b> 1) Nemôžem prísť, pretože som chorý/chorá. 2) Mám čas, preto ti pomôžem. 3) Peter povedal, že príde o šiestej.", SMALL),
    p("<b>5.</b> 1) Bývame v malom meste. 2) Včera som napísal/napísala kolegovi/kolegyni. 3) Mohli by ste to zopakovať? 4) Anna povedala, že príde neskôr.", SMALL),
    p("<b>6. Возможный ответ:</b> Volám sa Ari a bývam na Slovensku. Učím sa po slovensky, pretože chcem komunikovať samostatne. Včera som opakoval/opakovala gramatiku. Zajtra budem čítať krátky text. Mohli by ste mi opraviť chyby, prosím?", SMALL),
    p("Итог в четырёх пунктах", H2),
    styled_table([
        ["✓", "Я определяю роль слова и вспоминаю вопрос падежа."],
        ["✓", "Я различаю прошлое, будущий процесс и будущий результат."],
        ["✓", "Я могу связать несколько мыслей и назвать причину."],
        ["✓", "Я умею уточнить и передать простую информацию."],
    ], [12 * mm, 158 * mm], font_size=8.1, header=False),
    Spacer(1, 4 * mm),
    box("<b>Моя следующая точка:</b> если труднее всего были формы слов - повторите падежи. Если времена - повторите Module 7 A1. Если отдельные фразы получаются, но диалог нет - повторите Module 8 A1. Затем переходите к PDF 1.2.", PALE, PINK, SMALL),
    p("Финальная проверка мастерства", H2),
    p("Закройте документ и скажите 6 связанных предложений о себе: настоящее, вчера, завтра, причина, просьба и переданная информация. Если смысл понятен без подсказки, мост к A2 пройден.", BODY),
    p("Личный маршрут перед PDF 1.2", H2),
    styled_table([
        ["Зона", "Что я сделаю", "Готово"],
        ["Формы слов", "Повторю нужный падеж и 5 своих примеров.", "□"],
        ["Глаголы", "Скажу по 3 фразы о вчера и завтра.", "□"],
        ["Общение", "Разыграю просьбу и перенос встречи.", "□"],
    ], [35 * mm, 115 * mm, 20 * mm], font_size=7.6),
    Spacer(1, 3 * mm),
    box("<b>Не нужно повторять весь A1.</b> Выберите только одну слабую зону, закрепите её и двигайтесь дальше. Следующая тема: вид глагола - процесс, повтор и результат.", GREEN, colors.HexColor("#A8D5B3"), SMALL),
]

doc.build(story)
print(OUTPUT)
