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
OUTPUT = ROOT / "output" / "pdf" / "A2" / "Module_01" / "Slovak_A2_Tema_1_3_Klitiki_i_poryadok_slov.pdf"
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
        canvas.drawString(20 * mm, height - 12 * mm, "SLOVAK A2  |  ТЕМА 1.3")
        canvas.drawRightString(width - 20 * mm, height - 12 * mm, "Клитики и порядок слов")
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
    title="Slovak A2 - Тема 1.3 - Клитики и порядок слов", author="SlovoKrok",
)
frame = Frame(20 * mm, 18 * mm, 170 * mm, 257 * mm, id="main", leftPadding=0, rightPadding=0)
doc.addPageTemplates([PageTemplate(id="series", frames=[frame], onPage=draw_page)])

story = [
    p("МОДУЛЬ 1  •  ПЕРЕХОД ОТ A1 К A2", COVER_KICKER),
    p("Клитики и<br/>порядок слов", TITLE),
    p("Druhá pozícia a poradie krátkych tvarov", SUBTITLE),
    Spacer(1, 31 * mm),
    p("На A2 короткие безударные слова уже встречаются группами. Чтобы фраза звучала естественно, нужно выбрать для всей группы правильное место и внутренний порядок.", BODY),
    p("После модуля вы сможете:", H2),
    styled_table([
        ["1", "находить вторую синтаксическую позицию в предложении"],
        ["2", "собирать цепочку by - som - sa/si - datív - akuzatív"],
        ["3", "ставить короткие формы после že, keď, lebo и aby"],
        ["4", "различать нейтральные и ударные формы местоимений"],
    ], [12 * mm, 158 * mm], font_size=8.4, header=False),
    Spacer(1, 5 * mm),
    box("<b>Главная формула:</b> первый смысловой блок + группа клитик + остальная часть предложения.", PALE, PINK),
    Spacer(1, 4 * mm),
    p("Маршрут: вторая позиция -> состав группы -> порядок внутри -> придаточные -> контраст форм -> упражнения.", SMALL),
    PageBreak(),

    p("1. Что такое вторая позиция", H1),
    p("Клитики - короткие безударные формы: <b>by, som, si, sme, ste, sa, mi, ti, mu, ho</b> и другие. Они не любят начинать предложение и обычно образуют группу после первого смыслового блока.", BODY),
    styled_table([
        ["Первый блок", "Группа", "Продолжение", "Перевод"],
        ["Včera", "som mu", "zavolal.", "Вчера я ему позвонил."],
        ["Po práci", "som mu", "zavolal.", "После работы я ему позвонил."],
        ["Tú správu", "som mu", "poslal ráno.", "То сообщение я отправил ему утром."],
        ["V novom byte", "sa mi", "dobre býva.", "В новой квартире мне хорошо живётся."],
    ], [41 * mm, 30 * mm, 52 * mm, 47 * mm], font_size=7.3),
    Spacer(1, 4 * mm),
    box("<b>Позиция считается по блокам, а не по отдельным словам.</b> В сочетании <b>Po náročnom pracovnom dni som si oddýchol</b> весь длинный оборот стоит первым, а <b>som si</b> следует после него.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    p("Что может быть первым блоком", H2),
    bullet("слово времени: <b>Dnes sa učím doma.</b>"),
    bullet("группа слов: <b>Po večeri som si čítal.</b>"),
    bullet("объект с акцентом: <b>Túto knihu som mu dal.</b>"),
    p("Мини-проверка", H2),
    p("Найдите первый блок и группу клитик: 1) Ráno som sa ponáhľal. 2) Po dlhej porade som mu to vysvetlil. 3) Tento film sa mi páči.", BODY),
    PageBreak(),

    p("2. Порядок внутри группы", H1),
    p("Если клитик несколько, они располагаются в относительно устойчивой последовательности. Не все позиции обязаны быть заполнены.", BODY),
    styled_table([
        ["1", "2", "3", "4", "5"],
        ["by", "som/si/sme/ste", "sa/si", "mi/ti/mu/jej/nám/vám/im", "ma/ťa/ho/ju/nás/vás/ich"],
        ["условие", "вспомогательная форма", "возвратность", "кому?", "кого? что?"],
    ], [22 * mm, 41 * mm, 28 * mm, 43 * mm, 36 * mm], font_size=7.05),
    Spacer(1, 4 * mm),
    p("Готовые цепочки", H2),
    styled_table([
        ["Цепочка", "Пример", "Перевод"],
        ["som + sa", "Včera som sa vrátil.", "Вчера я вернулся."],
        ["som + ti + ho", "Ráno som ti ho poslal.", "Утром я отправил его тебе."],
        ["by + som + sa + ti", "Určite by som sa ti ospravedlnil.", "Я бы точно перед тобой извинился."],
        ["by + som + si + ho", "Možno by som si ho kúpil.", "Возможно, я бы его себе купил."],
        ["sa + mi", "Tento nápad sa mi páči.", "Эта идея мне нравится."],
    ], [42 * mm, 73 * mm, 55 * mm], font_size=7.35),
    Spacer(1, 4 * mm),
    box("<b>Собирайте группу целиком:</b> <b>Chcel by som sa ti poďakovať.</b> При переносе первого блока сама цепочка остаётся вместе: <b>Poďakovať by som sa ti chcel.</b>", PALE, PINK, SMALL),
    p("Частая ошибка", H2),
    p("Не переставляйте элементы по русской логике: <b>Včera mu som to povedal</b> -> <b>Včera som mu to povedal.</b>", BODY),
    PageBreak(),

    p("3. Прошедшее, условие и придаточные", H1),
    p("Знакомые формы A1 становятся сложнее, когда собираются в одну группу. На A2 важно удерживать порядок автоматически.", BODY),
    styled_table([
        ["Ситуация", "Модель", "Пример"],
        ["Прошедшее", "som + sa/si + pron.", "Včera som sa ti ozval."],
        ["Условие", "by + som + sa/si + pron.", "Rád by som ti pomohol."],
        ["že", "že + группа", "Viem, že sa ti to páči."],
        ["keď", "keď + группа", "Keď som sa vrátil, zavolal som mu."],
        ["lebo", "lebo + группа", "Neprišiel, lebo sa mu nechcelo."],
        ["aby", "aby + sa/si + pron.", "Prosím ho, aby mi zavolal."],
    ], [29 * mm, 55 * mm, 86 * mm], font_size=7.25),
    Spacer(1, 4 * mm),
    p("После подчинительного слова", H2),
    p("В придаточной части <b>že, keď, lebo, aby</b> открывают новый отрезок. Клитики обычно идут сразу после них: <b>že som sa</b>, <b>keď si mi</b>, <b>lebo sa mu</b>.", BODY),
    styled_table([
        ["Неправильно", "Правильно", "Почему"],
        ["Viem, že ti sa páči.", "Viem, že sa ti páči.", "sa стоит перед дательным ti"],
        ["Keď vrátil som sa...", "Keď som sa vrátil...", "som sa образуют группу после keď"],
        ["Chcel som, aby zavolal mi.", "Chcel som, aby mi zavolal.", "mi следует после aby"],
    ], [52 * mm, 61 * mm, 57 * mm], font_size=7.35),
    Spacer(1, 4 * mm),
    box("<b>Практический ориентир:</b> после союза сначала произнесите всю короткую группу одним ритмическим блоком, затем добавьте смысловой глагол.", PALE, PINK, SMALL),
    PageBreak(),

    p("4. Короткая или ударная форма", H1),
    p("Короткая форма нейтрально передаёт уже известного участника. Полная форма получает ударение, подчёркивает контраст или используется после предлога.", BODY),
    styled_table([
        ["Нейтрально", "С контрастом", "Перевод"],
        ["Dal mi knihu.", "Mne dal knihu, nie Petrovi.", "Он дал книгу мне, не Петру."],
        ["Videl ho v meste.", "Videl práve jeho.", "Он увидел именно его."],
        ["Povedal ti pravdu.", "Tebe povedal pravdu.", "Он сказал правду тебе."],
        ["Pomôžem mu.", "Pomôžem jemu, nie jej.", "Я помогу ему, не ей."],
    ], [54 * mm, 65 * mm, 51 * mm], font_size=7.35),
    Spacer(1, 4 * mm),
    p("После предлога", H2),
    styled_table([
        ["Нельзя", "Нужно", "Пример"],
        ["pre ma", "pre mňa", "Toto je pre mňa."],
        ["k mu", "k nemu", "Idem k nemu."],
        ["o ho", "o ňom", "Hovoríme o ňom."],
        ["s ju", "s ňou", "Stretol som sa s ňou."],
    ], [40 * mm, 40 * mm, 90 * mm], font_size=7.4),
    Spacer(1, 4 * mm),
    box("<b>Выбор:</b> без особого акцента используйте короткую форму в группе клитик. Для противопоставления или после предлога выбирайте полную форму.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    p("Мини-диалог", H2),
    box("<b>A:</b> Poslal si Petrovi ten dokument?<br/><b>B:</b> Áno, ráno som mu ho poslal.<br/><b>A:</b> A poslal si ho aj Anne?<br/><b>B:</b> Nie, jej som ho neposlal.", ALT, ROSE, SMALL),
    PageBreak(),

    p("5. Частые ошибки и упражнения", H1),
    box("<b>Три ошибки:</b> начинать фразу с som/sa/mi; разрывать группу; ставить дательный перед sa/si. Сначала найдите первый блок, затем соберите цепочку.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    p("Упражнение 1. Найдите первый блок", H2),
    p("Подчеркните первый блок и обведите клитики: 1) Včera som mu zavolal. 2) Po dlhej ceste som si oddýchol. 3) Tento nový byt sa mi páči.", SMALL),
    p("Упражнение 2. Расставьте слова", H2),
    p("1) včera / som / mu / to / povedal; 2) ráno / som / ti / ho / poslal; 3) určite / by / som / sa / ti / ospravedlnil.", SMALL),
    p("Упражнение 3. Вставьте короткую форму", H2),
    p("1) Peter dal ___ knihu. (мне) 2) Ráno som ___ ___ poslal. (тебе её) 3) Tento film sa ___ páči. (ему)", SMALL),
    p("Упражнение 4. Исправьте", H2),
    p("1) Som mu to vysvetlil včera. 2) Viem, že ti sa to páči. 3) Keď vrátil som sa, zavolal som mu. 4) Chcel by sa ti som poďakovať.", SMALL),
    p("Упражнение 5. Переведите", H2),
    p("1) Вчера я отправил ему это. 2) Я знаю, что тебе это нравится. 3) Я бы хотел перед вами извиниться. 4) После работы я отдохнул.", SMALL),
    p("Упражнение 6. Мини-диалог", H2),
    p("Напишите 5 реплик о документе или подарке. Используйте минимум три цепочки: som mu ho, sa mi, že si mi, by som ti.", SMALL),
    PageBreak(),

    p("6. Ответы и проверка мастерства", H1),
    p("Ответы", H2),
    p("<b>1.</b> Первые блоки: Včera; Po dlhej ceste; Tento nový byt. Клитики: som mu; som si; sa mi.", SMALL),
    p("<b>2.</b> 1) Včera som mu to povedal. 2) Ráno som ti ho poslal. 3) Určite by som sa ti ospravedlnil.", SMALL),
    p("<b>3.</b> 1) mi; 2) ti ju; 3) mu.", SMALL),
    p("<b>4.</b> 1) Včera som mu to vysvetlil. 2) Viem, že sa ti to páči. 3) Keď som sa vrátil, zavolal som mu. 4) Chcel by som sa ti poďakovať.", SMALL),
    p("<b>5.</b> 1) Včera som mu to poslal. 2) Viem, že sa ti to páči. 3) Chcel by som sa vám ospravedlniť. 4) Po práci som si oddýchol.", SMALL),
    p("<b>6. Возможный ответ:</b> Poslal si Anne ten dokument? Áno, včera som jej ho poslal. Viem, že sa jej páči. Mohol by som jej poslať aj prílohu. Dobre, pošlem jej ju večer.", SMALL),
    p("Итог в четырёх пунктах", H2),
    styled_table([
        ["✓", "Я нахожу первый смысловой блок и ставлю клитики после него."],
        ["✓", "Я сохраняю порядок by - som - sa/si - datív - akuzatív."],
        ["✓", "Я ставлю группу сразу после že, keď, lebo и aby."],
        ["✓", "Я выбираю короткую или полную форму по смысловому акценту."],
    ], [12 * mm, 158 * mm], font_size=8.0, header=False),
    Spacer(1, 4 * mm),
    box("<b>Финальная проверка:</b> перестройте фразу <b>Ráno som mu ho poslal</b>, поставив первым объект, длинное обстоятельство и придаточную часть. Группа клитик должна остаться в правильном порядке.", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    p("Следующий шаг", H2),
    p("Читайте примеры вслух целыми ритмическими блоками. Так порядок коротких форм станет автоматическим и не будет собираться по одному слову. Затем переходите к PDF 1.4 о семьях слов.", BODY),
]

doc.build(story)
print(OUTPUT)
