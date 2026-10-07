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
OUTPUT = ROOT / "output" / "pdf" / "A2" / "Module_05" / "Slovak_A2_Tema_5_6_Prichina_i_sledstvie.pdf"
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
SMALL = ParagraphStyle("Small", parent=BODY, fontSize=7.55, leading=9.45, spaceAfter=1.6 * mm)
TINY = ParagraphStyle("Tiny", parent=BODY, fontSize=6.8, leading=8.35, spaceAfter=1.0 * mm)
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
        canvas.drawString(20 * mm, height - 12 * mm, "A2 5.6  |  Причина и следствие")
    canvas.setFont("Arial", 8)
    canvas.setFillColor(MUTED)
    canvas.drawString(20 * mm, 9 * mm, "SlovoKrok | личный учебный модуль")
    canvas.drawRightString(width - 20 * mm, 9 * mm, f"стр. {page} / 7")
    canvas.restoreState()


doc = BaseDocTemplate(
    str(OUTPUT), pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=20 * mm, bottomMargin=18 * mm,
    title="Slovak A2 - Тема 5.6 - Причина и следствие", author="SlovoKrok",
)
frame = Frame(20 * mm, 18 * mm, 170 * mm, 257 * mm, id="main", leftPadding=0, rightPadding=0)
doc.addPageTemplates([PageTemplate(id="series", frames=[frame], onPage=draw_page)])

story = [
    p("МОДУЛЬ 5  •  СВЯЗНАЯ РЕЧЬ И СЛОЖНЫЕ ПРЕДЛОЖЕНИЯ", COVER_KICKER),
    p("Причина и<br/>следствие", TITLE),
    p("Príčina a následok: объясняем проблему и показываем результат", SUBTITLE),
    Spacer(1, 34 * mm),
    p("В словацком одна и та же ситуация строится с двух сторон. <b>lebo / pretože</b> вводят причину и отвечают на вопрос <b>prečo?</b>, а <b>preto</b> вводит следствие: что получилось из названной причины."),
    p("После модуля вы сможете:", H2),
    styled_table([
        ["1", "объяснять причину с lebo и pretože"],
        ["2", "сообщать следствие с preto"],
        ["3", "менять порядок частей без потери логики"],
        ["4", "ставить запятую и выбирать естественный нейтральный вариант"],
    ], [12 * mm, 158 * mm], font_size=7.2, header=False),
    Spacer(1, 3 * mm),
    box("<b>Две стрелки:</b> следствие <b>, lebo / pretože</b> причина. Причина <b>, preto</b> следствие.", PALE, PINK),
    PageBreak(),

    p("1. Lebo и pretože вводят причину", H1),
    p("Сначала сообщаем факт или проблему, затем объясняем <b>почему</b>. Перед <b>lebo</b> и <b>pretože</b> ставится запятая, если они соединяют две части с личными формами глагола."),
    styled_table([
        ["Следствие", "Причина", "Готовое предложение"],
        ["Neprišiel som.", "Bol som chorý.", "Neprišiel som, lebo som bol chorý."],
        ["Zostali sme doma.", "Pršalo.", "Zostali sme doma, pretože pršalo."],
        ["Meškám.", "Autobus neprišiel.", "Meškám, lebo autobus neprišiel."],
        ["Nemôžem telefonovať.", "Som na porade.", "Nemôžem telefonovať, pretože som na porade."],
        ["Som unavená.", "Zle som spala.", "Som unavená, lebo som zle spala."],
    ], [43 * mm, 43 * mm, 84 * mm], font_size=5.75),
    p("Lebo или pretože?", H2),
    styled_table([
        ["Форма", "Практическая опора", "Пример"],
        ["lebo", "коротко и очень обычно в разговоре", "Odídem skôr, lebo sa necítim dobre."],
        ["pretože", "полное нейтральное объяснение", "Kurz zrušili, pretože lektor ochorel."],
    ], [28 * mm, 66 * mm, 76 * mm], font_size=6.15),
    box("<b>Обе формы нормативны.</b> На A2 выбирайте <b>lebo</b> для простого разговорного объяснения, а <b>pretože</b> - когда хотите выделить полную причину. Смысл часто остаётся тем же.", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    PageBreak(),

    p("2. Preto вводит следствие", H1),
    p("С <b>preto</b> сначала называем причину, затем результат. <b>Preto</b> относится ко второй части и значит <b>поэтому</b>. Оно не заменяет <b>lebo</b> внутри той же схемы."),
    styled_table([
        ["Причина", "Следствие", "Готовое предложение"],
        ["Bol som chorý.", "Neprišiel som.", "Bol som chorý, preto som neprišiel."],
        ["Pršalo.", "Zostali sme doma.", "Pršalo, preto sme zostali doma."],
        ["Autobus neprišiel.", "Meškám.", "Autobus neprišiel, preto meškám."],
        ["Som na porade.", "Nemôžem telefonovať.", "Som na porade, preto nemôžem telefonovať."],
        ["Zle som spala.", "Som unavená.", "Zle som spala, preto som unavená."],
    ], [43 * mm, 43 * mm, 84 * mm], font_size=5.75),
    p("Одна ситуация - две конструкции", H2),
    styled_table([
        ["Фокус на результате", "Фокус на причине"],
        ["Eva neprišla, lebo je chorá.", "Eva je chorá, preto neprišla."],
        ["Ева не пришла, потому что больна.", "Ева больна, поэтому не пришла."],
        ["Nešli sme von, pretože fúkal vietor.", "Fúkal vietor, preto sme nešli von."],
        ["Мы не вышли, потому что дул ветер.", "Дул ветер, поэтому мы не вышли."],
    ], [85 * mm, 85 * mm], font_size=6.0),
    box("<b>Типичная ошибка:</b> *Pršalo, lebo sme zostali doma* меняет логику: получается, что дождь шёл из-за того, что мы остались дома. Проверяйте стрелку причины.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    PageBreak(),

    p("3. Порядок частей и запятая", H1),
    p("Нейтральные модели легко читать слева направо. С <b>lebo</b> обычно сначала идёт результат, затем причина. С <b>preto</b> сначала идёт причина, затем следствие. <b>Pretože</b>-часть может стоять и первой."),
    styled_table([
        ["Модель", "Пример", "Перевод"],
        ["следствие, lebo причина", "Ostal doma, lebo bol chorý.", "Он остался дома, потому что был болен."],
        ["следствие, pretože причина", "Ostal doma, pretože bol chorý.", "Он остался дома, потому что был болен."],
        ["pretože причина, следствие", "Pretože bol chorý, ostal doma.", "Поскольку он был болен, он остался дома."],
        ["причина, preto следствие", "Bol chorý, preto ostal doma.", "Он был болен, поэтому остался дома."],
    ], [48 * mm, 63 * mm, 59 * mm], font_size=5.9),
    p("Запятая показывает границу", H2),
    styled_table([
        ["Перед связкой", "После начальной причины"],
        ["Meškáme, lebo je zápcha.", "Pretože je zápcha, meškáme."],
        ["Je zápcha, preto meškáme.", "Причинная часть закончилась - ставим запятую."],
    ], [85 * mm, 85 * mm], font_size=6.25),
    p("Нейтральный регистр", H2),
    p("<b>Lebo</b> естественно звучит в повседневной речи и остаётся литературной формой. <b>Pretože</b> удобно для более развёрнутого объяснения. <b>Preto</b> подчёркивает вывод или практический результат. Не добавляйте лишнее <i>a</i>: для учебной нейтральной модели достаточно <b>..., preto ...</b>.", SMALL),
    box("<b>Самопроверка:</b> если после связки идёт ответ на <b>prečo?</b>, нужен <b>lebo / pretože</b>. Если после связки идёт результат, нужен <b>preto</b>.", PALE, PINK, SMALL),
    PageBreak(),

    p("4. Модель общения: опоздание на встречу", H1),
    box("<b>Lucia:</b> Prečo si neprišiel načas?<br/><b>Tomáš:</b> Meškal som, lebo autobus neprišiel.<br/><b>Lucia:</b> Prečo si mi nenapísal?<br/><b>Tomáš:</b> Vybil sa mi telefón, preto som ti nemohol zavolať.<br/><b>Lucia:</b> Stretnutie sme začali neskôr, pretože sme na teba čakali.<br/><b>Tomáš:</b> Mrzí ma to. Nabudúce vyrazím skôr, lebo ráno býva zápcha.", PALE, ROSE, SMALL),
    p("Перевод", H2),
    p("Почему ты не пришёл вовремя? Я опоздал, потому что автобус не пришёл. Почему ты мне не написал? У меня разрядился телефон, поэтому я не мог тебе позвонить. Мы начали встречу позже, потому что ждали тебя. Мне жаль. В следующий раз я выйду раньше, потому что утром бывают пробки.", SMALL),
    p("Банк полезных моделей", H2),
    styled_table([
        ["SK", "RU"],
        ["Nepracujem dnes, lebo som chorý.", "Я сегодня не работаю, потому что болен."],
        ["Nemáme čas, preto odídeme skôr.", "У нас нет времени, поэтому мы уйдём раньше."],
        ["Okno je otvorené, pretože je tu teplo.", "Окно открыто, потому что здесь жарко."],
        ["Nemala som hotovosť, preto som platila kartou.", "У меня не было наличных, поэтому я заплатила картой."],
        ["Zavolaj mi, lebo potrebujem pomoc.", "Позвони мне, потому что мне нужна помощь."],
        ["Cesta bola zatvorená, preto sme išli inou cestou.", "Дорога была закрыта, поэтому мы поехали другой дорогой."],
    ], [88 * mm, 82 * mm], font_size=5.9),
    box("<b>Хорошая связная речь:</b> не повторяйте одну форму механически. В рассказе можно чередовать: проблема <b>, lebo</b> причина; причина <b>, preto</b> решение.", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    PageBreak(),

    p("5. Частые ошибки и упражнения", H1),
    box("<b>Частые ошибки:</b> путают направление логики; используют <b>preto</b> как союз причины; пропускают запятую; добавляют лишнее <i>a</i>; считают <b>lebo</b> неправильным разговорным словом.", CREAM, colors.HexColor("#E7C76C"), TINY),
    p("Упражнение 1. Выберите lebo, pretože или preto", H2),
    p("1) Som doma, ___ som chorý. 2) Prší, ___ nejdeme von. 3) Meškám, ___ autobus neprišiel. 4) Nemám hotovosť, ___ platím kartou.", TINY),
    p("Упражнение 2. Определите причину и следствие", H2),
    p("1) Zle som spal, preto som unavený. 2) Neprišla, lebo bola chorá. 3) Kurz zrušili, pretože lektor ochorel. 4) Je zápcha, preto meškáme.", TINY),
    p("Упражнение 3. Соедините двумя способами", H2),
    p("1) Pršalo. Zostali sme doma. 2) Telefón sa vybil. Nemohol som zavolať. Используйте сначала <b>lebo</b>, затем <b>preto</b>.", TINY),
    p("Упражнение 4. Поставьте запятые и исправьте логику", H2),
    p("1) Neprišiel som lebo som bol chorý. 2) Som unavený preto som zle spal. 3) Pretože pršalo zostali sme doma. 4) Autobus neprišiel preto meškám.", TINY),
    p("Упражнение 5. Переведите", H2),
    p("1) Я дома, потому что болен. 2) Идёт дождь, поэтому мы не выходим. 3) Я опоздала, потому что автобус не пришёл. 4) Было поздно, поэтому мы ушли.", TINY),
    p("Упражнение 6. Объясните проблему и решение", H2),
    p("Напишите 5-7 предложений о проблеме на работе, в дороге или дома. Используйте <b>lebo</b>, <b>pretože</b> и <b>preto</b>; минимум один раз начните предложение с причины.", TINY),
    PageBreak(),

    p("6. Ответы и проверка мастерства", H1),
    p("Ответы", H2),
    p("<b>1.</b> 1) lebo / pretože; 2) preto; 3) lebo / pretože; 4) preto.", TINY),
    p("<b>2.</b> 1) причина: zle som spal; следствие: som unavený. 2) причина: bola chorá; следствие: neprišla. 3) причина: lektor ochorel; следствие: kurz zrušili. 4) причина: je zápcha; следствие: meškáme.", TINY),
    p("<b>3.</b> Pršalo, preto sme zostali doma. Zostali sme doma, lebo pršalo. Telefón sa vybil, preto som nemohol zavolať. Nemohol som zavolať, lebo sa mi vybil telefón.", TINY),
    p("<b>4.</b> 1) Neprišiel som, lebo som bol chorý. 2) Zle som spal, preto som unavený. 3) Pretože pršalo, zostali sme doma. 4) Autobus neprišiel, preto meškám.", TINY),
    p("<b>5.</b> Som doma, lebo som chorý. Prší, preto nejdeme von. Meškala som, lebo autobus neprišiel. Bolo neskoro, preto sme odišli.", TINY),
    p("<b>6. Модель:</b> Ráno som zaspal, preto som vyšiel neskoro. Meškal som, lebo bola zápcha. Pretože som nemal čas, nezastavil som sa na raňajky. V práci som bol hladný, preto som si objednal obed. Nabudúce si nastavím dva budíky, lebo nechcem znova meškať. Возможны другие естественные варианты.", TINY),
    p("Итог в четырёх пунктах", H2),
    styled_table([
        ["OK", "Lebo и pretože вводят причину и отвечают на prečo?"],
        ["OK", "Preto вводит следствие и значит поэтому."],
        ["OK", "Проверяю порядок: причина ведёт к следствию."],
        ["OK", "Отделяю две части запятой."],
    ], [12 * mm, 158 * mm], font_size=6.35, header=False),
    Spacer(1, 2 * mm),
    box("<b>Финальная проверка:</b> скажите двумя способами: <b>Я не пришёл, потому что был болен</b> и <b>Я был болен, поэтому не пришёл</b>.", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    p("Следующий шаг", H2),
    p("В теме 5.7 вы различите время и реальное условие с <b>keď</b> и <b>ak</b>.", SMALL),
]

doc.build(story)
print(OUTPUT)
