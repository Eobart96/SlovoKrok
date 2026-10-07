from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output" / "pdf" / "A2" / "Module_04" / "Slovak_A2_Tema_4_4_Vid_v_nastoyashchem_i_proshedshem_vremeni.pdf"
TITLE = "Slovak A2 - Тема 4.4 - Вид в настоящем и прошедшем времени"

PLUM = colors.HexColor("#7B245F")
PINK = colors.HexColor("#CE3C92")
PALE = colors.HexColor("#FFF0F7")
ROSE = colors.HexColor("#EACDD9")
ALT = colors.HexColor("#FFF8FA")
BLUE = colors.HexColor("#EAF2FA")
GREEN = colors.HexColor("#E2F3E8")
CREAM = colors.HexColor("#FFF5E5")
INK = colors.HexColor("#30272E")
MUTED = colors.HexColor("#705E68")
WHITE = colors.white


def register_fonts():
    regular = next(p for p in [Path("C:/Windows/Fonts/arial.ttf"), Path("C:/Windows/Fonts/calibri.ttf")] if p.exists())
    bold = next(p for p in [Path("C:/Windows/Fonts/arialbd.ttf"), Path("C:/Windows/Fonts/calibrib.ttf")] if p.exists())
    pdfmetrics.registerFont(TTFont("SK", str(regular)))
    pdfmetrics.registerFont(TTFont("SK-Bold", str(bold)))


register_fonts()
ST = {
    "cover_kicker": ParagraphStyle("cover_kicker", fontName="SK-Bold", fontSize=14, leading=18, textColor=colors.HexColor("#F8D8E9"), alignment=TA_CENTER, spaceAfter=8),
    "cover_title": ParagraphStyle("cover_title", fontName="SK-Bold", fontSize=25, leading=30, textColor=WHITE, alignment=TA_CENTER, spaceAfter=11),
    "cover_sub": ParagraphStyle("cover_sub", fontName="SK", fontSize=12.2, leading=17, textColor=WHITE, alignment=TA_CENTER),
    "h1": ParagraphStyle("h1", fontName="SK-Bold", fontSize=20, leading=24, textColor=PLUM, spaceAfter=8),
    "h2": ParagraphStyle("h2", fontName="SK-Bold", fontSize=13.5, leading=17, textColor=PLUM, spaceBefore=6, spaceAfter=5),
    "body": ParagraphStyle("body", fontName="SK", fontSize=9.5, leading=13.1, textColor=INK, spaceAfter=4),
    "small": ParagraphStyle("small", fontName="SK", fontSize=8.4, leading=11.5, textColor=MUTED, spaceAfter=2),
    "box": ParagraphStyle("box", fontName="SK", fontSize=9.1, leading=12.6, textColor=INK),
    "box_b": ParagraphStyle("box_b", fontName="SK-Bold", fontSize=9.4, leading=12.8, textColor=PLUM),
    "ex": ParagraphStyle("ex", fontName="SK", fontSize=9.05, leading=12.35, textColor=INK, leftIndent=6, spaceAfter=3),
    "task": ParagraphStyle("task", fontName="SK", fontSize=8.55, leading=11.55, textColor=INK, spaceAfter=4),
    "answer": ParagraphStyle("answer", fontName="SK", fontSize=8.15, leading=10.85, textColor=INK, spaceAfter=3),
}


def P(text, style="body"):
    return Paragraph(text, ST[style])


def callout(title, text, color=PALE, width=169):
    table = Table([[P(title, "box_b")], [P(text, "box")]], colWidths=[width * mm])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), color), ("BOX", (0, 0), (-1, -1), 0.7, ROSE),
        ("LINEBELOW", (0, 0), (-1, 0), 0.45, ROSE),
        ("LEFTPADDING", (0, 0), (-1, -1), 8), ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    return table


def grid(rows, widths, header=True, font="small"):
    data = [[P(cell, "box_b" if header and i == 0 else font) for cell in row] for i, row in enumerate(rows)]
    table = Table(data, colWidths=[w * mm for w in widths], repeatRows=1 if header else 0)
    rules = [
        ("GRID", (0, 0), (-1, -1), 0.45, ROSE), ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6), ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]
    if header:
        rules.append(("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#F5D4E5")))
    for row in range(1 if header else 0, len(data)):
        if row % 2 == 0:
            rules.append(("BACKGROUND", (0, row), (-1, row), ALT))
    table.setStyle(TableStyle(rules))
    return table


def first_page(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(PLUM)
    canvas.rect(0, 0, A4[0], A4[1], fill=1, stroke=0)
    canvas.setFillColor(colors.HexColor("#9E2F74"))
    canvas.circle(18 * mm, 266 * mm, 37 * mm, fill=1, stroke=0)
    canvas.circle(194 * mm, 28 * mm, 49 * mm, fill=1, stroke=0)
    canvas.setFillColor(colors.HexColor("#F8D8E9"))
    canvas.roundRect(27 * mm, 34 * mm, 156 * mm, 38 * mm, 5 * mm, fill=1, stroke=0)
    canvas.setFillColor(PLUM)
    canvas.setFont("SK-Bold", 11)
    canvas.drawCentredString(105 * mm, 57 * mm, "КОГДА? + КАК ПРОТЕКАЛО? + ЕСТЬ ЛИ РЕЗУЛЬТАТ?")
    canvas.setFont("SK", 9)
    canvas.drawCentredString(105 * mm, 47 * mm, "kedy? + ako dej prebiehal? + máme výsledok?")
    canvas.setFillColor(colors.HexColor("#F8D8E9"))
    canvas.setFont("SK", 7.5)
    canvas.drawCentredString(105 * mm, 13 * mm, "стр. 1 / 7")
    canvas.restoreState()


def later_page(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(ROSE)
    canvas.setLineWidth(0.7)
    canvas.line(20 * mm, 281 * mm, 190 * mm, 281 * mm)
    canvas.setFillColor(PLUM)
    canvas.setFont("SK-Bold", 8)
    canvas.drawString(20 * mm, 285 * mm, "SLOVOKROK  |  A2  |  ТЕМА 4.4  |  ВИД И ВРЕМЯ")
    canvas.setFillColor(MUTED)
    canvas.setFont("SK", 7.5)
    canvas.drawCentredString(105 * mm, 10 * mm, f"стр. {doc.page} / 7")
    canvas.restoreState()


doc = SimpleDocTemplate(
    str(OUT), pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm,
    topMargin=26 * mm, bottomMargin=17 * mm, title=TITLE,
    author="SlovoKrok", subject="Slovak A2 self-study module 4.4",
)
story = []

# 1. Cover
story += [
    Spacer(1, 24 * mm), P("SLOVOKROK • СЛОВАЦКИЙ A2", "cover_kicker"),
    P("ТЕМА 4.4", "cover_kicker"),
    P("Вид в настоящем<br/>и прошедшем времени", "cover_title"),
    P("Vid v prítomnom a minulom čase", "cover_sub"), Spacer(1, 15 * mm),
    Table(
        [[P("После модуля вы сможете", "box_b")],
         [P("• выбирать вид для привычки и текущего процесса;<br/>• различать прошедший процесс, факт и полученный результат;<br/>• использовать маркеры частотности и длительности;<br/>• строить связный рассказ с фоном и завершёнными событиями.", "box")]],
        colWidths=[145 * mm],
        style=TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#FFF7FB")),
            ("LEFTPADDING", (0, 0), (-1, -1), 10), ("RIGHTPADDING", (0, 0), (-1, -1), 10),
            ("TOPPADDING", (0, 0), (-1, -1), 7), ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ]),
    ), PageBreak(),
]

# 2. Present
story += [
    P("1. Настоящее: процесс и привычка", "h1"),
    P("Для действия, которое идёт <b>сейчас</b>, и для повторяющейся привычки используйте несовершенный вид. Он показывает действие изнутри, без границы и готового результата."),
    grid([
        ["Смысл", "Маркеры", "Пример"],
        ["процесс сейчас", "teraz, práve, momentálne", "Práve píšem e-mail.<br/>Сейчас я пишу письмо."],
        ["регулярность", "každý deň, často, zvyčajne", "Každý deň čítam správy.<br/>Каждый день я читаю новости."],
        ["постоянный порядок", "vždy, obyčajne", "Zvyčajne platím kartou.<br/>Обычно я плачу картой."],
    ], [39, 51, 79]),
    P("Ещё примеры", "h2"),
    P("<b>Teraz varím večeru.</b> - Сейчас я готовлю ужин.", "ex"),
    P("<b>Momentálne hľadáme nový byt.</b> - В данный момент мы ищем новую квартиру.", "ex"),
    P("<b>Často chodíme do knižnice.</b> - Мы часто ходим в библиотеку.", "ex"),
    P("<b>Každú sobotu upratujem byt.</b> - Каждую субботу я убираю квартиру.", "ex"),
    callout("Важная граница", "Формы <b>napíšem, uvarím, zaplatím</b> выглядят как настоящее время, но у совершенных глаголов они называют будущий результат: <i>Napíšem e-mail.</i> - Я напишу письмо. Подробное образование будущего времени будет в теме 4.6.", CREAM),
    callout("Быстрый вопрос", "Можно спросить <i>Čo teraz robíš?</i> - Что ты сейчас делаешь? Если ответ описывает процесс, нужен несовершенный вид: <i>Píšem. Varím. Čítam.</i>", BLUE),
    PageBreak(),
]

# 3. Past process
story += [
    P("2. Прошедшее: процесс и повтор", "h1"),
    P("В прошедшем несовершенный вид показывает фон, ход действия или повтор. Говорящий не ставит в центр конечную границу."),
    grid([
        ["Фокус", "Типичные подсказки", "Пример"],
        ["длительность", "dve hodiny, celé ráno", "Včera som čítal dve hodiny.<br/>Вчера я читал два часа."],
        ["процесс в момент события", "keď..., vtedy", "Keď si volal, varila som.<br/>Когда ты позвонил, я готовила."],
        ["повтор в прошлом", "často, každý týždeň", "Každé leto sme chodili k jazeru.<br/>Каждое лето мы ездили к озеру."],
        ["временной фон", "od... do..., celý deň", "Celé ráno som hľadal kľúče.<br/>Всё утро я искал ключи."],
    ], [37, 50, 82]),
    P("Один глагол, разные рамки", "h2"),
    P("<b>Včera som písala správu dve hodiny.</b> - Вчера я писала сообщение два часа.", "ex"),
    P("<b>Keď prišiel Peter, písala som správu.</b> - Когда пришёл Петер, я писала сообщение.", "ex"),
    P("<b>Minulý mesiac som často písala klientom.</b> - В прошлом месяце я часто писала клиентам.", "ex"),
    callout("Маркеры помогают, но не решают за вас", "Слова <i>včera</i> или <i>ráno</i> только называют время. Вид выбирает смысл: <i>Ráno som písal správu</i> - процесс; <i>Ráno som napísal správu</i> - готовый результат.", GREEN),
    callout("Фон и событие", "В связном рассказе фон часто выражен несовершенным видом, а событие, которое продвигает рассказ, совершенным: <i>Pracoval som, keď zazvonil telefón.</i> - Я работал, когда зазвонил телефон.", BLUE),
    PageBreak(),
]

# 4. Past fact/result
story += [
    P("3. Прошедшее: факт или результат", "h1"),
    P("Несовершенный вид может назвать сам факт занятия или опыт без акцента на завершении. Совершенный вид делает заметной границу: действие состоялось целиком и дало результат."),
    grid([
        ["Факт / процесс", "Результат / граница"],
        ["Čítal si ten článok?<br/>Ты читал эту статью?", "Prečítal si celý článok?<br/>Ты прочитал всю статью?"],
        ["Písala som správu.<br/>Я писала сообщение.", "Napísala som správu.<br/>Я написала сообщение."],
        ["Hľadala som doklady.<br/>Я искала документы.", "Našla som doklady.<br/>Я нашла документы."],
        ["Pozerali sme film.<br/>Мы смотрели фильм.", "Dopozerali sme film.<br/>Мы досмотрели фильм."],
    ], [84.5, 84.5]),
    P("Как выбрать", "h2"),
    grid([
        ["Вопрос к себе", "Если ответ да", "Выбор"],
        ["Важно, чем человек занимался?", "процесс, фон, опыт", "несовершенный"],
        ["Важно, что работа закончена?", "есть граница или результат", "совершенный"],
        ["Важно, сколько длилось?", "длительность в центре", "обычно несовершенный"],
        ["Важно, сколько единиц сделано?", "итог измерим", "обычно совершенный"],
    ], [56, 62, 51]),
    callout("Не путайте факт с неудачей", "<i>Čítal som knihu</i> не означает автоматически «я не дочитал». Фраза лишь не предъявляет завершение как главное. Если результат важен, скажите <i>Prečítal som knihu</i>.", CREAM),
    P("Мини-диалог", "h2"),
    callout("Po práci", "<b>Eva:</b> Písal si už tú správu?<br/><b>Martin:</b> Áno, písal som ju celé ráno.<br/><b>Eva:</b> A napísal si ju?<br/><b>Martin:</b> Áno, napísal. Už som ju aj poslal.<br/><br/><b>Перевод:</b> Эва: Ты уже писал этот отчёт? Мартин: Да, писал его всё утро. Эва: А закончил? Мартин: Да, написал. Я его уже и отправил.", BLUE),
    PageBreak(),
]

# 5. Connected story
story += [
    P("4. Вид в связном рассказе", "h1"),
    P("Сначала дайте фон и протяжённые действия, затем отмечайте завершённые шаги. Так рассказ звучит естественно, а вид помогает читателю видеть его структуру."),
    callout(
        "Včerajší pracovný deň",
        "Každé ráno vstávam o siedmej a čítam správy. Včera som čítal dôležitý článok, keď mi zavolala kolegyňa. Potom som článok prečítal do konca. Dopoludnia som písal správu dve hodiny. O jedenástej som ju napísal a poslal. Celé popoludnie som hľadal chybu v tabuľke. Nakoniec som ju našiel a opravil.<br/><br/><b>Перевод:</b> Каждое утро я встаю в семь и читаю новости. Вчера я читал важную статью, когда мне позвонила коллега. Потом я дочитал статью до конца. До обеда я два часа писал отчёт. В одиннадцать я его закончил и отправил. Всё вторую половину дня я искал ошибку в таблице. Наконец я её нашёл и исправил.",
        BLUE,
    ),
    P("Разметка рассказа", "h2"),
    grid([
        ["Фрагмент", "Роль вида"],
        ["vstávam, čítam", "привычка в настоящем: повторяющийся порядок"],
        ["som čítal, som písal, som hľadal", "прошедший фон, процесс и длительность"],
        ["zavolala", "одно событие внутри фона"],
        ["som prečítal, napísal, poslal", "законченные шаги и их результат"],
        ["som našiel, opravil", "финальная граница цепочки событий"],
    ], [69, 100]),
    callout("Три сигнала", "<b>Частотность:</b> každý deň, často, zvyčajne. <b>Длительность:</b> dve hodiny, celé popoludnie, od ôsmej do desiatej. <b>Результат:</b> do konca, nakoniec, už + готовый итог.", GREEN),
    P("Важно", "h2"),
    P("Маркер <i>nakoniec</i> часто вводит результат, но форма всё равно зависит от смысла. Сравните: <i>Nakoniec som čakal ešte hodinu</i> - в итоге я ждал ещё час; <i>Nakoniec som sa dočkal odpovede</i> - наконец я дождался ответа."),
    PageBreak(),
]

# 6. Exercises
story += [
    P("5. Ошибки и практика", "h1"),
    callout("Частые ошибки", "1) использовать совершенный вид для действия, которое идёт прямо сейчас; 2) считать любой прошедший глагол результатом; 3) выбирать вид только по слову <i>včera</i>; 4) забывать, что несовершенный вид может называть факт занятия; 5) переводить форму без контекста.", CREAM),
    P("<b>1. Назовите смысл:</b> привычка, текущий процесс, прошедший процесс, факт или результат.<br/>a) Práve upratujem kuchyňu. b) Každý piatok volám rodičom. c) Včera som čítal dve hodiny. d) Čítal si tú knihu? e) Prečítal som ju včera.", "task"),
    P("<b>2. Выберите форму.</b><br/>a) Teraz <i>(píšem / napíšem)</i> e-mail.<br/>b) Každé ráno <i>(čítam / prečítam)</i> správy.<br/>c) Keď si prišiel, <i>(varila / uvarila)</i> som večeru.<br/>d) O siedmej som večeru <i>(varila / uvarila)</i> a podávala na stôl.", "task"),
    P("<b>3. Вставьте подходящий маркер:</b> práve, každý týždeň, dve hodiny, nakoniec.<br/>a) ___ chodíme na kurz. b) ___ telefonujem klientovi. c) Písala správu ___. d) ___ správu napísala a poslala.", "task"),
    P("<b>4. Исправьте форму под заданный смысл.</b><br/>a) «Я сейчас пишу письмо»: Teraz napíšem list.<br/>b) «Каждый день я читаю новости по привычке»: Každý deň prečítam správy.<br/>c) «Когда ты позвонил, я закончила готовить»: Keď si volal, varila som večeru.<br/>d) «Я искал ключи и нашёл их»: Hľadal som kľúče a hľadal som ich.", "task"),
    P("<b>5. Переведите.</b><br/>a) Обычно я плачу картой, но сейчас ищу наличные.<br/>b) Вчера я два часа писал отчёт и в одиннадцать его закончил.<br/>c) Когда она готовила, зазвонил телефон.<br/>d) Ты читал статью или прочитал её до конца?", "task"),
    P("<b>6. Мини-дневник.</b> Напишите 6-8 предложений: одна привычка в настоящем, два прошлых процесса, одно событие на фоне и два результата. Подчеркните маркеры времени."),
    PageBreak(),
]

# 7. Answers
story += [
    P("6. Ответы и итог", "h1"),
    P("<b>1.</b> a) текущий процесс; b) привычка; c) прошедший процесс; d) факт / опыт; e) результат.", "answer"),
    P("<b>2.</b> a) <b>píšem</b> - процесс сейчас; b) <b>čítam</b> - привычка; c) <b>varila</b> - фон; d) <b>uvarila</b> - готовый ужин.", "answer"),
    P("<b>3.</b> a) <b>Každý týždeň</b>; b) <b>Práve</b>; c) <b>dve hodiny</b>; d) <b>Nakoniec</b>.", "answer"),
    P("<b>4.</b> a) Teraz <b>píšem</b> list. b) Každý deň <b>čítam</b> správy. c) Keď si volal, <b>uvarila</b> som večeru. d) Hľadal som kľúče a <b>našiel</b> som ich.", "answer"),
    P("<b>5.</b> a) Zvyčajne platím kartou, ale teraz hľadám hotovosť. b) Včera som dve hodiny písal správu a o jedenástej som ju napísal. c) Keď varila, zazvonil telefón. d) Čítal si článok alebo si ho prečítal do konca?", "answer"),
    P("Образец к заданию 6", "h2"),
    callout("Môj deň", "Zvyčajne vstávam o siedmej. Včera som ráno dlho pripravoval prezentáciu. Keď som kontroloval posledný obrázok, zavolal mi kolega. Potom som prezentáciu dokončil a poslal vedúcej. Popoludní som dve hodiny hľadal údaje. Nakoniec som ich našiel a doplnil tabuľku.<br/><br/>Обычно я встаю в семь. Вчера утром я долго готовил презентацию. Когда я проверял последнюю картинку, мне позвонил коллега. Потом я закончил презентацию и отправил руководительнице. После обеда я два часа искал данные. Наконец я их нашёл и дополнил таблицу.", BLUE),
    P("Четыре опоры", "h2"),
    grid([
        ["1", "Сейчас и обычно: несовершенный вид показывает процесс или привычку."],
        ["2", "В прошлом несовершенный вид даёт процесс, фон, повтор или факт занятия."],
        ["3", "Совершенный вид выделяет границу, завершённый шаг и полученный результат."],
        ["4", "Маркеры направляют выбор, но окончательное решение задаёт смысл фразы."],
    ], [14, 155], header=False),
    callout("Проверка освоения", "Я могу:  □ описать привычку и текущий процесс;  □ различить прошлый процесс, факт и результат;  □ объяснить контраст <i>písal/napísal</i>;  □ построить мини-рассказ с фоном и цепочкой событий.", GREEN),
]

OUT.parent.mkdir(parents=True, exist_ok=True)
doc.build(story, onFirstPage=first_page, onLaterPages=later_page)
print(OUT)
