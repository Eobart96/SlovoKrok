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
OUTPUT = ROOT / "output" / "pdf" / "A2" / "Module_05" / "Slovak_A2_Tema_5_5_Pridatochnye_s_kto_co_i_kde.pdf"
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
        canvas.drawString(20 * mm, height - 12 * mm, "A2 5.5  |  Придаточные с kto, čo и kde")
    canvas.setFont("Arial", 8)
    canvas.setFillColor(MUTED)
    canvas.drawString(20 * mm, 9 * mm, "SlovoKrok | личный учебный модуль")
    canvas.drawRightString(width - 20 * mm, 9 * mm, f"стр. {page} / 7")
    canvas.restoreState()


doc = BaseDocTemplate(
    str(OUTPUT), pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=20 * mm, bottomMargin=18 * mm,
    title="Slovak A2 - Тема 5.5 - Придаточные с kto, čo и kde", author="SlovoKrok",
)
frame = Frame(20 * mm, 18 * mm, 170 * mm, 257 * mm, id="main", leftPadding=0, rightPadding=0)
doc.addPageTemplates([PageTemplate(id="series", frames=[frame], onPage=draw_page)])

story = [
    p("МОДУЛЬ 5  •  СВЯЗНАЯ РЕЧЬ И СЛОЖНЫЕ ПРЕДЛОЖЕНИЯ", COVER_KICKER),
    p("Придаточные с<br/>kto, čo и kde", TITLE),
    p("Nepriame otázky: передаём неизвестную информацию внутри предложения", SUBTITLE),
    Spacer(1, 34 * mm),
    p("Слова <b>kto, čo, kde</b> могут не только начинать прямой вопрос. Они вводят придаточную часть после <b>viem, neviem, povedz, ukáž, pamätáš si</b> и сообщают, кто что сделал, что нужно или где находится место."),
    p("После модуля вы сможете:", H2),
    styled_table([
        ["1", "превращать прямой вопрос в часть сложного предложения"],
        ["2", "выбирать kto для человека, čo для предмета или действия, kde для места"],
        ["3", "ставить запятую перед придаточной частью"],
        ["4", "сохранять нормальный порядок слов и выбирать знак по всему предложению"],
    ], [12 * mm, 158 * mm], font_size=7.2, header=False),
    Spacer(1, 3 * mm),
    box("<b>Формула:</b> рамка сообщения <b>+ , kto / čo / kde + законченное предложение</b>. Пример: <b>Neviem, kde je zastávka.</b>", PALE, PINK),
    PageBreak(),

    p("1. Прямой вопрос и придаточная часть", H1),
    p("В прямом вопросе говорящий сам просит информацию. В сложном предложении тот же вопрос становится содержанием глагола <b>знать, сказать, показать, помнить</b>. Вопросительное слово сохраняется, но вся конструкция получает одну общую пунктуацию."),
    styled_table([
        ["Прямой вопрос", "Придаточная часть", "Перевод"],
        ["Kto tam pracuje?", "Viem, kto tam pracuje.", "Я знаю, кто там работает."],
        ["Kto volal?", "Povedz mi, kto volal.", "Скажи мне, кто звонил."],
        ["Čo potrebuješ?", "Neviem, čo potrebuješ.", "Я не знаю, что тебе нужно."],
        ["Čo sa stalo?", "Vysvetli, čo sa stalo.", "Объясни, что случилось."],
        ["Kde je vchod?", "Ukáž mi, kde je vchod.", "Покажи мне, где вход."],
        ["Kde býva Eva?", "Vieš, kde býva Eva?", "Ты знаешь, где живёт Ева?"],
    ], [43 * mm, 61 * mm, 66 * mm], font_size=5.95),
    p("Знак в конце выбираем по главной части", H2),
    styled_table([
        ["Сообщение", "Viem, kde býva."],
        ["Просьба", "Povedz mi, kde býva."],
        ["Общий вопрос", "Vieš, kde býva?"],
    ], [37 * mm, 133 * mm], font_size=6.55, header=False),
    box("<b>Важно:</b> внутреннее <b>kde</b> не делает всё предложение вопросом. Сравните: <b>Neviem, kde býva.</b> и <b>Vieš, kde býva?</b>", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    PageBreak(),

    p("2. Kto и čo: человек или информация", H1),
    p("Используйте <b>kto</b>, когда неизвестен человек, и <b>čo</b>, когда неизвестен предмет, содержание, событие или действие. Эти слова одновременно связывают части предложения и выполняют роль внутри придаточной части."),
    styled_table([
        ["Нужно узнать", "Модель", "Пример и перевод"],
        ["кто действует", "kto + глагол", "Neviem, kto otvoril okno. - Не знаю, кто открыл окно."],
        ["кто придёт", "kto + глагол", "Zistíme, kto príde. - Узнаем, кто придёт."],
        ["что произошло", "čo + sa + глагол", "Povedz, čo sa stalo. - Скажи, что случилось."],
        ["что человек делает", "čo + лицо + глагол", "Vidím, čo robíš. - Я вижу, что ты делаешь."],
        ["что нужно", "čo + лицо + глагол", "Napíš, čo potrebuješ. - Напиши, что тебе нужно."],
        ["что это такое", "čo + byť", "Vysvetli, čo je to. - Объясни, что это."],
    ], [38 * mm, 39 * mm, 93 * mm], font_size=5.8),
    p("Kto или ktorý?", H2),
    styled_table([
        ["Без названного человека", "С названным человеком"],
        ["Neviem, kto tam pracuje.", "Poznám človeka, ktorý tam pracuje."],
        ["Я не знаю, кто там работает.", "Я знаю человека, который там работает."],
    ], [85 * mm, 85 * mm], font_size=6.25),
    box("<b>Связь с темой 5.4:</b> <b>ktorý</b> уточняет уже названное существительное. <b>Kto</b> сам обозначает неизвестного человека и не требует слова <i>človek</i> перед собой.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    PageBreak(),

    p("3. Kde: неизвестное место", H1),
    p("Используйте <b>kde</b>, когда речь о месте, где кто-то или что-то находится либо где происходит действие. В этой теме тренируем только статичное <b>где</b>; направление <b>куда</b> и источник <b>откуда</b> относятся к отдельной пространственной теме."),
    styled_table([
        ["Рамка", "Пример", "Перевод"],
        ["viem / neviem", "Neviem, kde sú moje kľúče.", "Я не знаю, где мои ключи."],
        ["ukáž mi", "Ukáž mi, kde je recepcia.", "Покажи мне, где ресепшен."],
        ["povedz mi", "Povedz mi, kde máme čakať.", "Скажи мне, где нам ждать."],
        ["pamätám si", "Pamätám si, kde sme sa stretli.", "Я помню, где мы встретились."],
        ["zistím", "Zistím, kde sa koná kurz.", "Я выясню, где проходит курс."],
        ["vieš?", "Vieš, kde je najbližšia lekáreň?", "Ты знаешь, где ближайшая аптека?"],
    ], [34 * mm, 70 * mm, 66 * mm], font_size=6.0),
    p("Порядок слов", H2),
    styled_table([
        ["Нейтральная опора", "Что запомнить"],
        ["Vieš, kde je stanica?", "связка je обычно стоит перед существительным"],
        ["Povedz, kde býva Peter.", "подлежащее после глагола звучит нейтрально"],
        ["Ukáž mi, kde sa začína cesta.", "sa занимает обычную позицию в группе"],
    ], [85 * mm, 85 * mm], font_size=6.2),
    box("<b>Надёжная опора:</b> после <b>kto, čo, kde</b> стройте обычное словацкое предложение. Клитика <b>sa</b> остаётся рядом с глагольной группой: <b>čo sa stalo</b>, <b>kde sa koná kurz</b>.", PALE, PINK, SMALL),
    PageBreak(),

    p("4. Модель общения: первый день на курсе", H1),
    box("<b>Anna:</b> Vieš, kto je náš lektor?<br/><b>Marek:</b> Áno, pán Novák. Neviem však, kde je naša učebňa.<br/><b>Anna:</b> Ukážem ti, kde je. Je na druhom poschodí.<br/><b>Marek:</b> A vieš, čo dnes budeme robiť?<br/><b>Anna:</b> Lektor povedal, že vysvetlí, čo potrebujeme na projekt.<br/><b>Marek:</b> Dobre. Ešte zistím, kto je v mojej skupine.", PALE, ROSE, SMALL),
    p("Перевод", H2),
    p("Ты знаешь, кто наш преподаватель? Да, господин Новак. Но я не знаю, где наша аудитория. Я покажу тебе, где она. Она на втором этаже. А ты знаешь, что мы сегодня будем делать? Преподаватель сказал, что объяснит, что нам нужно для проекта. Хорошо. Я ещё выясню, кто в моей группе.", SMALL),
    p("Полезные рамки", H2),
    styled_table([
        ["SK", "RU"],
        ["Neviem, kto má zoznam.", "Я не знаю, у кого список."],
        ["Povedz mi, čo máme priniesť.", "Скажи мне, что нам принести."],
        ["Ukáž mi, kde si môžem sadnúť.", "Покажи мне, где я могу сесть."],
        ["Vieš, kto nám môže pomôcť?", "Ты знаешь, кто может нам помочь?"],
        ["Pamätáš si, čo povedal lektor?", "Ты помнишь, что сказал преподаватель?"],
        ["Zistíme, kde bude stretnutie.", "Мы выясним, где будет встреча."],
    ], [86 * mm, 84 * mm], font_size=6.05),
    box("<b>Запятая:</b> граница видна перед <b>kto, čo, kde</b>: <b>Neviem, kto...</b>; <b>Povedz, čo...</b>; <b>Ukáž, kde...</b>", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    PageBreak(),

    p("5. Частые ошибки и упражнения", H1),
    box("<b>Частые ошибки:</b> путают <b>kto</b> и <b>ktorý</b>; ставят вопросительный знак после сообщения; теряют запятую; меняют нейтральный порядок слов; ломают модель <b>čo sa stalo</b>.", CREAM, colors.HexColor("#E7C76C"), TINY),
    p("Упражнение 1. Выберите kto, čo или kde", H2),
    p("1) Neviem, ___ volal. 2) Ukáž mi, ___ je výťah. 3) Povedz, ___ potrebuješ. 4) Vieš, ___ otvoril okno?", TINY),
    p("Упражнение 2. Превратите вопрос в придаточную часть", H2),
    p("1) Kto tam pracuje? - Viem, ___. 2) Čo sa stalo? - Vysvetli, ___. 3) Kde je vchod? - Ukáž mi, ___. 4) Čo robí Eva? - Neviem, ___.", TINY),
    p("Упражнение 3. Выберите знак и поставьте запятую", H2),
    p("1) Vieš kde býva Peter  2) Neviem kto má kľúč  3) Povedz mi čo máme robiť  4) Pamätáš si kde sme sa stretli", TINY),
    p("Упражнение 4. Исправьте ошибку", H2),
    p("1) Poznám kto tam pracuje. 2) Ukáž mi kde recepcia je. 3) Povedz, čo stalo sa. 4) Viem, kde je lekáreň?", TINY),
    p("Упражнение 5. Переведите", H2),
    p("1) Я знаю, кто звонил. 2) Скажи, что тебе нужно. 3) Покажи мне, где вход. 4) Ты помнишь, где мы встретились?", TINY),
    p("Упражнение 6. Передайте информацию", H2),
    p("Напишите 5-7 предложений о первом дне на курсе, работе или в отеле. Используйте минимум по одному придаточному с <b>kto</b>, <b>čo</b> и <b>kde</b>, а также одно общее вопросительное предложение.", TINY),
    PageBreak(),

    p("6. Ответы и проверка мастерства", H1),
    p("Ответы", H2),
    p("<b>1.</b> 1) kto; 2) kde; 3) čo; 4) kto.", TINY),
    p("<b>2.</b> 1) Viem, kto tam pracuje. 2) Vysvetli, čo sa stalo. 3) Ukáž mi, kde je vchod. 4) Neviem, čo robí Eva.", TINY),
    p("<b>3.</b> 1) Vieš, kde býva Peter? 2) Neviem, kto má kľúč. 3) Povedz mi, čo máme robiť. 4) Pamätáš si, kde sme sa stretli?", TINY),
    p("<b>4.</b> 1) Viem, kto tam pracuje. / Poznám človeka, ktorý tam pracuje. 2) Ukáž mi, kde je recepcia. 3) Povedz, čo sa stalo. 4) Viem, kde je lekáreň.", TINY),
    p("<b>5.</b> Viem, kto volal. Povedz, čo potrebuješ. Ukáž mi, kde je vchod. Pamätáš si, kde sme sa stretli?", TINY),
    p("<b>6. Модель:</b> Neviem, kto je vedúci kurzu. Chcem zistiť, čo budeme robiť. Recepčná mi ukázala, kde je učebňa. Vieš, kto má zoznam účastníkov? Lektor vysvetlil, čo potrebujeme. Teraz už viem, kde sa stretneme. Возможны другие естественные варианты.", TINY),
    p("Итог в четырёх пунктах", H2),
    styled_table([
        ["OK", "Kto обозначает неизвестного человека, čo - содержание или событие, kde - место."],
        ["OK", "После рамки знания, просьбы или памяти ставлю запятую."],
        ["OK", "Строю после вопросительного слова обычное законченное предложение."],
        ["OK", "Знак в конце выбираю по смыслу всей конструкции."],
    ], [12 * mm, 158 * mm], font_size=6.25, header=False),
    Spacer(1, 2 * mm),
    box("<b>Финальная проверка:</b> без таблицы скажите: <b>Я не знаю, кто звонил</b>; <b>Скажи, что случилось</b>; <b>Покажи, где вход</b>.", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    p("Следующий шаг", H2),
    p("В теме 5.6 вы свяжете причину и следствие с <b>lebo, pretože</b> и <b>preto</b>.", SMALL),
]

doc.build(story)
print(OUTPUT)
