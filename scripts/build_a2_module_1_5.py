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
OUTPUT = ROOT / "output" / "pdf" / "A2" / "Module_01" / "Slovak_A2_Tema_1_5_Karta_padezhey.pdf"
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
TINY = ParagraphStyle("Tiny", parent=BODY, fontSize=7.2, leading=9.0, spaceAfter=1.5 * mm)
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
        canvas.drawString(20 * mm, height - 12 * mm, "SLOVAK A2  |  ТЕМА 1.5")
        canvas.drawRightString(width - 20 * mm, height - 12 * mm, "Карта падежей и управление")
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
    title="Slovak A2 - Тема 1.5 - Карта падежей и управление", author="SlovoKrok",
)
frame = Frame(20 * mm, 18 * mm, 170 * mm, 257 * mm, id="main", leftPadding=0, rightPadding=0)
doc.addPageTemplates([PageTemplate(id="series", frames=[frame], onPage=draw_page)])

story = [
    p("МОДУЛЬ 1  •  ПЕРЕХОД ОТ A1 К A2", COVER_KICKER),
    p("Карта падежей<br/>и управление", TITLE),
    p("Mapa pádov a väzby", SUBTITLE),
    Spacer(1, 37 * mm),
    p("На A2 важно не только помнить окончания, но и понимать, <b>почему</b> слово стоит в конкретном падеже: из-за роли в предложении, предлога или управления глагола.", BODY),
    p("После модуля вы сможете:", H2),
    styled_table([
        ["1", "определять падеж по функции и вопросу"],
        ["2", "различать место и направление в предложных конструкциях"],
        ["3", "запоминать глагол вместе с вопросом, предлогом и падежом"],
        ["4", "узнавать редкие остаточные формы звательного падежа"],
    ], [12 * mm, 158 * mm], font_size=8.4, header=False),
    Spacer(1, 5 * mm),
    box("<b>Главная формула:</b> роль -> вопрос -> предлог или управляющее слово -> нужная форма.", PALE, PINK),
    Spacer(1, 4 * mm),
    p("Это обзорная карта. Подробные окончания каждого падежа будут отрабатываться отдельно в следующих модулях.", SMALL),
    PageBreak(),

    p("1. Шесть рабочих падежей", H1),
    p("Современная словацкая система использует шесть падежей. Начинайте не с таблицы окончаний, а со смысла: кто действует, на кого направлено действие, кому, где, куда или с чем.", BODY),
    styled_table([
        ["Падеж и вопрос", "Главная функция", "Пример и перевод"],
        ["Nominatív<br/><b>kto? čo?</b>", "субъект, название", "<b>Nový kolega pracuje doma.</b><br/>Новый коллега работает дома."],
        ["Genitív<br/><b>koho? čoho?</b>", "исходная точка, отсутствие, принадлежность", "<b>Vraciame sa z mesta.</b><br/>Мы возвращаемся из города."],
        ["Datív<br/><b>komu? čomu?</b>", "адресат, получатель помощи", "<b>Píšem novej kolegyni.</b><br/>Я пишу новой коллеге."],
        ["Akuzatív<br/><b>koho? čo?</b>", "прямой объект, направление с na", "<b>Vidím suseda.</b><br/>Я вижу соседа."],
        ["Lokál<br/><b>o kom? o čom?</b>", "место или тема, всегда с предлогом", "<b>Hovoríme o práci.</b><br/>Мы говорим о работе."],
        ["Inštrumentál<br/><b>s kým? s čím?</b>", "совместность, орудие", "<b>Píšem perom.</b><br/>Я пишу ручкой."],
    ], [39 * mm, 52 * mm, 79 * mm], font_size=7.0),
    Spacer(1, 4 * mm),
    box("<b>Важно:</b> вопросы помогают проверить решение, но не всегда выбирают падеж сами. В сочетании <b>čakať na autobus</b> форму задаёт вся связь <b>čakať na + Akuzatív</b>.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    PageBreak(),

    p("2. Четыре маршрута к падежу", H1),
    p("Одно и то же окончание может выполнять разные задачи. Поэтому ищите самый сильный сигнал в предложении.", BODY),
    styled_table([
        ["Сигнал", "Как рассуждать", "Пример"],
        ["1. Функция", "кто выполняет действие?", "<b>Dieťa</b> kreslí. -> Nominatív"],
        ["2. Объект", "кого или что затрагивает действие?", "Čítam <b>knihu</b>. -> Akuzatív"],
        ["3. Предлог", "какого падежа требует предлог в этом значении?", "Som <b>v škole</b>. -> Lokál"],
        ["4. Управление", "какую связь требует глагол?", "Pomáham <b>susedovi</b>. -> Datív"],
    ], [30 * mm, 72 * mm, 68 * mm], font_size=7.35),
    p("Учите связь целиком", H2),
    styled_table([
        ["Связь", "Вопрос и падеж", "Пример"],
        ["pomáhať", "komu? Datív", "Pomáham starému otcovi."],
        ["rozumieť", "komu? čomu? Datív", "Rozumiem tejto otázke."],
        ["čakať na", "koho? čo? Akuzatív", "Čakáme na autobus."],
        ["tešiť sa na", "koho? čo? Akuzatív", "Teším sa na víkend."],
        ["báť sa", "koho? čoho? Genitív", "Bojím sa skúšky."],
        ["zúčastniť sa", "koho? čoho? Genitív", "Zúčastním sa kurzu."],
        ["hovoriť o", "kom? čom? Lokál", "Hovoríme o novom projekte."],
        ["stretnúť sa s", "kým? čím? Inštrumentál", "Stretnem sa s kolegyňou."],
    ], [45 * mm, 52 * mm, 73 * mm], font_size=7.05),
    Spacer(1, 3 * mm),
    box("Карточка управления: <b>rozumieť - komu? čomu? - D - Rozumiem učiteľovi.</b> Одна такая строка полезнее, чем глагол без контекста.", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    PageBreak(),

    p("3. Место и направление", H1),
    p("Русское где? и куда? дают полезную подсказку, но окончательное решение принимает словацкая конструкция.", BODY),
    styled_table([
        ["Где? Место", "Куда? Направление", "Откуда?"],
        ["<b>Som v škole.</b><br/>Я в школе.<br/>v + Lokál", "<b>Idem do školy.</b><br/>Я иду в школу.<br/>do + Genitív", "<b>Idem zo školy.</b><br/>Я иду из школы.<br/>z/zo + Genitív"],
        ["<b>Som na stanici.</b><br/>Я на вокзале.<br/>na + Lokál", "<b>Idem na stanicu.</b><br/>Я иду на вокзал.<br/>na + Akuzatív", "<b>Idem zo stanice.</b><br/>Я иду с вокзала.<br/>z/zo + Genitív"],
        ["<b>Kniha je na stole.</b><br/>Книга на столе.<br/>na + Lokál", "<b>Dám knihu na stôl.</b><br/>Я положу книгу на стол.<br/>na + Akuzatív", "<b>Vezmem knihu zo stola.</b><br/>Я возьму книгу со стола.<br/>z/zo + Genitív"],
    ], [56.7 * mm, 56.7 * mm, 56.6 * mm], font_size=7.05),
    p("Ещё три направления", H2),
    styled_table([
        ["Конструкция", "Значение", "Пример"],
        ["k/ku + Datív", "к человеку или ориентиру", "Idem k lekárovi. - Я иду к врачу."],
        ["od + Genitív", "от человека или места", "Vraciame sa od lekára. - Мы возвращаемся от врача."],
        ["s/so + Inštrumentál", "вместе с кем-то", "Idem s kolegom. - Я иду с коллегой."],
    ], [40 * mm, 51 * mm, 79 * mm], font_size=7.25),
    Spacer(1, 4 * mm),
    box("<b>Ловушка:</b> один предлог <b>na</b> связан с двумя падежами: <b>na stanici</b> (место, Lokál), но <b>na stanicu</b> (направление, Akuzatív).", CREAM, colors.HexColor("#E7C76C"), SMALL),
    PageBreak(),

    p("4. Управление в живой речи", H1),
    p("Сначала найдите слово, которое управляет формой. Затем назовите связь целиком и только потом выбирайте окончание.", BODY),
    p("Мини-диалог", H2),
    box("<b>A:</b> Čakáš na novú kolegyňu?<br/><b>B:</b> Áno. Chcem jej pomôcť s projektom.<br/><b>A:</b> Rozumie už nášmu systému?<br/><b>B:</b> Ešte nie. Po stretnutí sa porozprávame o práci a pôjdeme spolu k vedúcemu.<br/><br/><b>Перевод:</b> Ты ждёшь новую коллегу? - Да. Я хочу помочь ей с проектом. - Она уже понимает нашу систему? - Ещё нет. После встречи мы поговорим о работе и вместе пойдём к руководителю.", ALT, ROSE, SMALL),
    p("Разбор связей", H2),
    styled_table([
        ["Фрагмент", "Что управляет", "Падеж"],
        ["na novú kolegyňu", "čakať na koho?", "Akuzatív"],
        ["jej", "pomôcť komu?", "Datív"],
        ["s projektom", "pomôcť s čím?", "Inštrumentál"],
        ["nášmu systému", "rozumieť čomu?", "Datív"],
        ["po stretnutí", "po čom?", "Lokál"],
        ["o práci", "porozprávať sa o čom?", "Lokál"],
        ["k vedúcemu", "k komu?", "Datív"],
    ], [64 * mm, 66 * mm, 40 * mm], font_size=7.15),
    p("А что со звательным падежом?", H2),
    p("В современной норме обращение обычно имеет форму Nominatív: <b>Peter, poď sem.</b> Сохранились отдельные формы, например <b>pane, človeče, bože, majstre, šéfe, chlapče, otče, synu, priateľu, mami, oci</b>. Узнавайте их как готовые слова, но не стройте по ним новую полную парадигму.", SMALL),
    PageBreak(),

    p("5. Частые ошибки и упражнения", H1),
    box("<b>Три ошибки:</b> переводить управление с русского; выбирать падеж только по вопросу; учить предлог без значения и примера.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    p("Упражнение 1. Назовите падеж и функцию", H2),
    p("1) <b>Sestra</b> pracuje doma. 2) Pomáham <b>bratovi</b>. 3) Čítam <b>správu</b>. 4) Hovoríme <b>o kurze</b>. 5) Píšem <b>ceruzkou</b>.", SMALL),
    p("Упражнение 2. Выберите форму", H2),
    p("1) Čakám na autobus / autobuse. 2) Idem do mesto / mesta. 3) Som na stanici / stanicu. 4) Rozumiem otázku / otázke. 5) Stretnem sa s kolegyňu / kolegyňou.", SMALL),
    p("Упражнение 3. Дополните предлог", H2),
    p("1) Hovoríme ___ práci. 2) Idem ___ lekárovi. 3) Vraciame sa ___ školy. 4) Teším sa ___ víkend. 5) Idem ___ kamarátom.", SMALL),
    p("Упражнение 4. Исправьте управление", H2),
    p("1) Pomáham moju sestru. 2) Bojím sa skúšku. 3) Rozumiem nový systém. 4) Zúčastním sa na kurze. 5) Čakáme autobus.", SMALL),
    p("Упражнение 5. Переведите", H2),
    p("1) Я говорю о новой работе. 2) Мы идём к врачу. 3) Она ждёт коллегу. 4) Я боюсь экзамена. 5) Книга лежит на столе.", SMALL),
    p("Упражнение 6. Своя карта", H2),
    p("Напишите 5-6 предложений о дороге на работу или учёбу. Используйте минимум четыре падежа и подчеркните управляющее слово или предлог.", SMALL),
    PageBreak(),

    p("6. Ответы и проверка мастерства", H1),
    p("Ответы", H2),
    p("<b>1.</b> Sestra - Nominatív, субъект; bratovi - Datív, адресат помощи; správu - Akuzatív, прямой объект; o kurze - Lokál, тема; ceruzkou - Inštrumentál, орудие.", TINY),
    p("<b>2.</b> 1) autobus; 2) mesta; 3) stanici; 4) otázke; 5) kolegyňou.", TINY),
    p("<b>3.</b> 1) o; 2) k; 3) zo; 4) na; 5) s.", TINY),
    p("<b>4.</b> 1) Pomáham mojej sestre. 2) Bojím sa skúšky. 3) Rozumiem novému systému. 4) Zúčastním sa kurzu. 5) Čakáme na autobus.", TINY),
    p("<b>5.</b> 1) Hovorím o novej práci. 2) Ideme k lekárovi. 3) Čaká na kolegu. 4) Bojím sa skúšky. 5) Kniha leží na stole.", TINY),
    p("<b>6. Возможный ответ:</b> Ráno idem do práce autobusom. Na zastávke čakám na kolegyňu. V autobuse hovoríme o novom projekte. Po príchode pomáham kolegovi. Večer sa vraciam z práce s kamarátom.", TINY),
    p("Итог в четырёх пунктах", H2),
    styled_table([
        ["OK", "Я определяю падеж по функции, вопросу, предлогу и управлению."],
        ["OK", "Я различаю место, направление и исходную точку."],
        ["OK", "Я учу глагол вместе с вопросом, предлогом и примером."],
        ["OK", "Я узнаю остаточные формы обращения, но не считаю их полной системой."],
    ], [12 * mm, 158 * mm], font_size=7.8, header=False),
    Spacer(1, 3 * mm),
    box("<b>Финальная проверка:</b> возьмите пять новых глаголов и сделайте карточки по формуле: глагол -> вопрос -> предлог -> падеж -> собственный пример.", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    p("Следующий шаг", H2),
    p("В PDF 1.6 вы будете строить связный текст: задавать тему, добавлять новую информацию и менять смысловой акцент, сохраняя правильные формы и управление.", SMALL),
]

doc.build(story)
print(OUTPUT)
