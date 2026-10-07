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
OUTPUT = ROOT / "output" / "pdf" / "A2" / "Module_03" / "Slovak_A2_Tema_3_7_Prityazhatelnye_prilagatelnye.pdf"
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
        canvas.drawString(20 * mm, height - 12 * mm, "A2 3.7  |  Притяжательные прилагательные")
    canvas.setFont("Arial", 8)
    canvas.setFillColor(MUTED)
    canvas.drawString(20 * mm, 9 * mm, "SlovoKrok | личный учебный модуль")
    canvas.drawRightString(width - 20 * mm, 9 * mm, f"стр. {page} / 7")
    canvas.restoreState()


doc = BaseDocTemplate(
    str(OUTPUT), pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=20 * mm, bottomMargin=18 * mm,
    title="Slovak A2 - Тема 3.7 - Притяжательные прилагательные", author="SlovoKrok",
)
frame = Frame(20 * mm, 18 * mm, 170 * mm, 257 * mm, id="main", leftPadding=0, rightPadding=0)
doc.addPageTemplates([PageTemplate(id="series", frames=[frame], onPage=draw_page)])

story = [
    p("МОДУЛЬ 3  •  ПРИЛАГАТЕЛЬНЫЕ, МЕСТОИМЕНИЯ И ЧИСЛИТЕЛЬНЫЕ", COVER_KICKER),
    p("Притяжательные<br/>прилагательные", TITLE),
    p("Privlastňovacie prídavné mená: otcov a matkin", SUBTITLE),
    Spacer(1, 32 * mm),
    p("Слова <b>otcov</b> и <b>matkin</b> называют индивидуального владельца: папин, мамин, Петров, Янин. Они образуются от названия человека, а затем согласуются с предметом в роде, числе и падеже.", BODY),
    p("После модуля вы сможете:", H2),
    styled_table([
        ["1", "образовывать естественные модели -ov и -in от названий людей"],
        ["2", "согласовывать otcov/matkin с предметом в N/G/D/A/L/I"],
        ["3", "различать otcov kabát, otcova kniha и otcovo auto"],
        ["4", "выбирать прилагательное или более ясную конструкцию с Genitív"],
    ], [12 * mm, 158 * mm], font_size=7.25, header=False),
    Spacer(1, 3 * mm),
    box("<b>Формула:</b> владелец-мужчина -> основа + <b>-ov</b>; владелец-женщина -> основа + <b>-in</b>; окончание показывает форму предмета.", PALE, PINK),
    PageBreak(),

    p("1. Две модели образования", H1),
    p("Эти прилагательные отвечают на вопрос <b>čí? čia? čie?</b> и называют одного конкретного владельца. Формы от имён собственных пишутся с прописной буквы.", BODY),
    styled_table([
        ["Основа", "Модель", "Готовая форма"],
        ["otec", "-ov", "otcov kabát, otcova kniha, otcovo auto"],
        ["brat", "-ov", "bratov bicykel, bratova izba, bratovo miesto"],
        ["Peter", "-ov", "Petrov kľúč, Petrova taška, Petrovo číslo"],
        ["Ján", "-ov", "Jánov plán, Jánova práca, Jánovo rozhodnutie"],
        ["matka", "-in", "matkin kabát, matkina kniha, matkino auto"],
        ["mama", "-in", "mamin hlas, mamina kabelka, mamino miesto"],
        ["sestra", "-in", "sestrin syn, sestrina izba, sestrino auto"],
        ["Jana", "-in", "Janin zošit, Janina správa, Janino miesto"],
    ], [31 * mm, 26 * mm, 113 * mm], font_size=6.15),
    box("<b>Не всегда достаточно механически отбросить окончание.</b> Есть изменения основы: <b>otec -> otcov, matka -> matkin, sestra -> sestrin</b>. Частотную форму лучше проверять как отдельное слово.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    p("Сравните с темой 3.6", H2),
    styled_table([
        ["Притяжательное слово", "Индивидуальное прилагательное"],
        ["jeho kabát - его пальто", "otcov kabát - папино пальто"],
        ["jej správa - её сообщение", "Janina správa - сообщение Яны"],
    ], [85 * mm, 85 * mm], font_size=6.6),
    PageBreak(),

    p("2. Согласование в единственном числе", H1),
    p("Владелец задаёт основу <b>otcov- / matkin-</b>, но род и падеж выбираются по предмету. Обе модели получают одинаковые падежные окончания.", BODY),
    styled_table([
        ["Падеж", "мужской род", "женский род", "средний род"],
        ["N", "otcov / matkin", "otcova / matkina", "otcovo / matkino"],
        ["G", "otcovho / matkinho", "otcovej / matkinej", "otcovho / matkinho"],
        ["D", "otcovmu / matkinmu", "otcovej / matkinej", "otcovmu / matkinmu"],
        ["A", "-ho лицо / N предмет", "otcovu / matkinu", "otcovo / matkino"],
        ["L", "otcovom / matkinom", "otcovej / matkinej", "otcovom / matkinom"],
        ["I", "otcovým / matkiným", "otcovou / matkinou", "otcovým / matkiným"],
    ], [23 * mm, 49 * mm, 49 * mm, 49 * mm], font_size=6.05),
    p("Живые падежные модели", H2),
    styled_table([
        ["Форма", "Пример и перевод"],
        ["G", "Bez otcovho súhlasu nepôjdem. - Без папиного согласия я не пойду."],
        ["D", "Vrátim sa k maminmu autu. - Я вернусь к маминой машине."],
        ["A лицо", "Poznám Petrovho brata. - Я знаю брата Петера."],
        ["A предмет", "Mám Petrov telefón. - У меня телефон Петера."],
        ["L", "Hovoríme o matkinej práci. - Мы говорим о маминой работе."],
        ["I", "Prišiel s otcovým kolegom. - Он пришёл с папиным коллегой."],
    ], [33 * mm, 137 * mm], font_size=6.35),
    box("<b>Аккузатив мужского рода:</b> человек получает форму <b>-ho</b>, предмет совпадает с N: <b>vidím otcovho priateľa</b>, но <b>vidím otcov dom</b>.", PALE, ROSE, SMALL),
    PageBreak(),

    p("3. Множественное число", H1),
    p("Во множественном числе различайте лица мужского рода и остальные существительные. Долгие окончания сохраняются: <b>-ých, -ým, -ými</b>.", BODY),
    styled_table([
        ["Падеж", "лица мужского рода", "остальные"],
        ["N", "otcovi / matkini kolegovia", "otcove / matkine knihy"],
        ["G", "otcových / matkiných kolegov", "otcových / matkiných kníh"],
        ["D", "otcovým / matkiným kolegom", "otcovým / matkiným knihám"],
        ["A", "otcových / matkiných kolegov", "otcove / matkine knihy"],
        ["L", "o otcových / matkiných kolegoch", "o otcových / matkiných knihách"],
        ["I", "s otcovými / matkinými kolegami", "s otcovými / matkinými knihami"],
    ], [24 * mm, 73 * mm, 73 * mm], font_size=6.15),
    p("Ещё четыре контраста", H2),
    styled_table([
        ["SK", "RU"],
        ["Prišli Petrovi bratia.", "Пришли братья Петера."],
        ["Vidím Petrových bratov.", "Я вижу братьев Петера."],
        ["Na stole sú Janine knihy.", "На столе книги Яны."],
        ["Rozprávame sa o Janiných knihách.", "Мы говорим о книгах Яны."],
    ], [84 * mm, 86 * mm], font_size=6.55),
    box("<b>Не смягчайте n:</b> пишется <b>matkini, matkine, matkiných</b>, а не *matkiňi или *matkiňe.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    PageBreak(),

    p("4. Где форма естественна, а где лучше Genitív", H1),
    p("Модели продуктивны, но в реальной речи выбор зависит от длины и типа названия владельца. Для A2 безопасно держать активным короткое индивидуальное владение.", BODY),
    styled_table([
        ["Естественно и живо", "Часто яснее через Genitív"],
        ["otcov kabát, mamina taška", "názor vedúcej projektu"],
        ["Petrov telefón, Janina správa", "rozhodnutie doktora Petra Nováka"],
        ["bratova izba, sestrine deti", "izba malého dievčatka"],
        ["Štúrova ulica, Galileov ďalekohľad", "kniha pani Novákovej"],
    ], [85 * mm, 85 * mm], font_size=6.45),
    p("Почему не строим форму автоматически", H2),
    styled_table([
        ["Случай", "Решение"],
        ["название человека среднего рода", "genitív: úsmev dievčaťa, izba dievčatka"],
        ["длинное имя или имя с титулом", "genitív после предмета: názor doktora Nováka"],
        ["фамилия уже имеет форму прилагательного", "genitív: kniha pani Novákovej"],
        ["не лицо и не конкретный владелец", "обычное относительное прилагательное или genitív"],
    ], [59 * mm, 111 * mm], font_size=6.4),
    box("<b>Практический выбор:</b> если короткая форма звучит знакомо и владелец один - используйте её. Если название длинное, необычное или не обозначает лицо, выбирайте прозрачный Genitív.", PALE, PINK, SMALL),
    PageBreak(),

    p("5. Контекст, ошибки и упражнения", H1),
    p("Мини-диалог: семейные вещи", H2),
    box("<b>A:</b> Čí je tento kabát? - Чьё это пальто?<br/><b>B:</b> To je <b>otcov kabát</b>. - Это папино пальто.<br/><b>A:</b> A táto taška? - А эта сумка?<br/><b>B:</b> Je <b>mamina</b>. Vnútri sú <b>mamine okuliare</b>. - Мамина. Внутри мамины очки.<br/><b>A:</b> Kde sú <b>Janine kľúče</b>? - Где ключи Яны?<br/><b>B:</b> Ležia vedľa <b>Petrovho telefónu</b>. - Они лежат рядом с телефоном Петера.", PALE, ROSE, TINY),
    box("<b>Частые ошибки:</b> *otecov kabát -> <b>otcov kabát</b>; *matkov taška -> <b>matkina taška</b>; *Petrová kniha -> <b>Petrova kniha</b>; *s otcovim kolegom -> <b>s otcovým kolegom</b>; *dievčatkova izba -> <b>izba dievčatka</b>.", CREAM, colors.HexColor("#E7C76C"), TINY),
    p("Упражнение 1. Образуйте базовую форму", H2),
    p("1) otec + kabát; 2) matka + taška; 3) Peter + telefón; 4) Jana + správa; 5) sestra + auto.", TINY),
    p("Упражнение 2. Согласуйте по роду", H2),
    p("Сделайте три формы: 1) bratov + dom/kniha/auto; 2) mamin + plán/izba/miesto.", TINY),
    p("Упражнение 3. Поставьте в нужный падеж", H2),
    p("1) bez (otcov súhlas); 2) o (matkina práca); 3) s (Petrov kolega); 4) k (Janino auto); 5) vidím (Petrov brat).", TINY),
    p("Упражнение 4. Исправьте ошибки", H2),
    p("1) Matkov kabát je nový. 2) Hovorím s otcovim kolegom. 3) Toto je Petrová taška. 4) Poznám Janiného brata. 5) Dievčatkova izba je malá.", TINY),
    p("Упражнение 5. Выберите прилагательное или Genitív", H2),
    p("1) папина книга; 2) мнение руководителя проекта; 3) комната маленькой девочки; 4) телефон Яна; 5) решение доктора Петера Новака.", TINY),
    p("Упражнение 6. Свой мини-текст", H2),
    p("Опишите 5-7 семейных вещей. Используйте -ov, -in, один косвенный падеж, одно множественное число и одну конструкцию с Genitív.", TINY),
    PageBreak(),

    p("6. Ответы и проверка мастерства", H1),
    p("Ответы", H2),
    p("<b>1.</b> otcov kabát; matkina taška; Petrov telefón; Janina správa; sestrino auto.", TINY),
    p("<b>2.</b> bratov dom, bratova kniha, bratovo auto; mamin plán, mamina izba, mamino miesto.", TINY),
    p("<b>3.</b> bez otcovho súhlasu; o matkinej práci; s Petrovým kolegom; k Janinmu autu; vidím Petrovho brata.", TINY),
    p("<b>4.</b> Matkin kabát je nový. Hovorím s otcovým kolegom. Toto je Petrova taška. Poznám Janinho brata. Izba dievčatka je malá.", TINY),
    p("<b>5.</b> otcova kniha; názor vedúceho projektu; izba malého dievčaťa; Jánov telefón; rozhodnutie doktora Petra Nováka.", TINY),
    p("<b>6. Модель:</b> V predsieni visí otcov kabát. Vedľa neho je mamina taška. V taške sú mamine okuliare. Na stole ležia Janine kľúče. Hovoríme o Petrovom novom telefóne. Prišli aj matkini bratia. Fotografia našej rodiny stojí pri okne. Возможны другие естественные варианты.", TINY),
    p("Итог в четырёх пунктах", H2),
    styled_table([
        ["OK", "Образую -ov от названия мужчины и -in от названия женщины."],
        ["OK", "Согласую форму с предметом, а не с владельцем."],
        ["OK", "Различаю otcovi kolegovia, otcove knihy и otcových kolegov."],
        ["OK", "Выбираю Genitív для длинного, необычного или среднего по роду владельца."],
    ], [12 * mm, 158 * mm], font_size=6.65, header=False),
    Spacer(1, 2 * mm),
    box("<b>Финальная проверка:</b> без таблицы образуйте по три рода от Peter и matka, затем скажите эти сочетания в G, L и I. Для длинного имени дайте вариант с Genitív.", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    p("Следующий шаг", H2),
    p("В теме 3.8 вы систематизируете слова для неопределённого, отсутствующего и полного множества людей, предметов и мест.", SMALL),
]

doc.build(story)
print(OUTPUT)
