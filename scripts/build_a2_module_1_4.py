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
OUTPUT = ROOT / "output" / "pdf" / "A2" / "Module_01" / "Slovak_A2_Tema_1_4_Semji_slov.pdf"
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
        canvas.drawString(20 * mm, height - 12 * mm, "SLOVAK A2  |  ТЕМА 1.4")
        canvas.drawRightString(width - 20 * mm, height - 12 * mm, "Семьи слов")
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
    title="Slovak A2 - Тема 1.4 - Семьи слов", author="SlovoKrok",
)
frame = Frame(20 * mm, 18 * mm, 170 * mm, 257 * mm, id="main", leftPadding=0, rightPadding=0)
doc.addPageTemplates([PageTemplate(id="series", frames=[frame], onPage=draw_page)])

story = [
    p("МОДУЛЬ 1  •  ПЕРЕХОД ОТ A1 К A2", COVER_KICKER),
    p("Семьи слов", TITLE),
    p("Slovné rodiny a tvorenie slov", SUBTITLE),
    Spacer(1, 37 * mm),
    p("На A2 словарь растёт быстрее, если вы учите не отдельные слова, а связи между ними: действие, человек, предмет, качество и признак.", BODY),
    p("После модуля вы сможете:", H2),
    styled_table([
        ["1", "видеть общий корень даже при небольшом изменении основы"],
        ["2", "узнавать частые суффиксы названий людей, действий и качеств"],
        ["3", "строить полезные словарные цепочки и проверять догадку"],
        ["4", "использовать родственные слова в коротком связном тексте"],
    ], [12 * mm, 158 * mm], font_size=8.4, header=False),
    Spacer(1, 5 * mm),
    box("<b>Главная формула:</b> знакомая основа + смысловой элемент = подсказка, но не гарантия. Сначала предположите значение, затем проверьте слово и контекст.", PALE, PINK),
    Spacer(1, 4 * mm),
    p("Маршрут: корень -> названия людей -> действие и качество -> модели -> словарный банк -> упражнения.", SMALL),
    PageBreak(),

    p("1. Что такое семья слов", H1),
    p("Родственные слова имеют общую смысловую основу. Они могут принадлежать к разным частям речи и менять форму корня. Семья помогает одновременно понять новое слово и вспомнить уже знакомые.", BODY),
    styled_table([
        ["Семья", "Слова", "Связь"],
        ["práca", "pracovať, pracovník, pracovný", "работа, работать, работник, рабочий"],
        ["učiť", "učenie, učiteľ, učiteľka", "учить, обучение, учитель, учительница"],
        ["cestovať", "cesta, cestovanie, cestovateľ", "путешествовать, путь, путешествие, путешественник"],
        ["zdravie", "zdravý, zdravotný, zdravotník", "здоровье, здоровый, медицинский, медработник"],
        ["informovať", "informácia, informačný", "информировать, информация, информационный"],
    ], [31 * mm, 70 * mm, 69 * mm], font_size=7.25),
    Spacer(1, 4 * mm),
    box("<b>Не путайте родство и внешнее сходство.</b> В семье <b>práca - pracovať</b> исчезает долгота á. В <b>ruka - ručný</b> меняется согласный. Такие изменения нужно замечать, а не выводить наугад.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    p("Алгоритм A2", H2),
    bullet("Найдите знакомую основу и определите общую тему."),
    bullet("Посмотрите на окончание или приставку и предположите часть речи."),
    bullet("Проверьте значение и форму в словаре; затем запишите свой пример."),
    p("Мини-проверка", H2),
    p("Что объединяет слова <b>bezpečný, bezpečnosť, nebezpečný</b>? Какую часть речи показывает окончание <b>-osť</b>?", BODY),
    PageBreak(),

    p("2. Названия людей и женские формы", H1),
    p("Суффикс часто подсказывает, что слово называет человека по профессии, занятию или роли. Но одной универсальной модели нет: учите мужскую и женскую формы парой.", BODY),
    styled_table([
        ["Модель", "Примеры", "Женская форма"],
        ["-ár / -iar", "lekár, kuchár, novinár", "lekárka, kuchárka, novinárka"],
        ["-ník", "pracovník, zdravotník, úradník", "pracovníčka, zdravotníčka, úradníčka"],
        ["разные деятели", "učiteľ, predajca, cestovateľ", "učiteľka, predajkyňa, cestovateľka"],
        ["-ista / профессия", "špecialista, turista, kolega", "špecialistka, turistka, kolegyňa"],
        ["другие модели", "predavač, psychológ, vodič", "predavačka, psychologička, vodička"],
    ], [35 * mm, 69 * mm, 66 * mm], font_size=7.15),
    Spacer(1, 4 * mm),
    p("Согласование в предложении", H2),
    styled_table([
        ["Форма", "Пример", "Перевод"],
        ["мужская", "Náš nový kolega je skúsený pracovník.", "Наш новый коллега - опытный сотрудник."],
        ["женская", "Naša nová kolegyňa je skúsená pracovníčka.", "Наша новая коллега - опытная сотрудница."],
        ["роль", "Môj brat pracuje ako zdravotník.", "Мой брат работает медработником."],
        ["роль", "Jeho sestra je zdravotníčka.", "Его сестра - медработница."],
    ], [29 * mm, 79 * mm, 62 * mm], font_size=7.15),
    Spacer(1, 4 * mm),
    box("<b>Осторожно:</b> не добавляйте <b>-ka</b> механически. Например, <b>kolega - kolegyňa</b> и <b>predajca - predajkyňa</b>. Словарь должен подтверждать форму.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    PageBreak(),

    p("3. Действие, качество и признак", H1),
    p("Несколько продуктивных элементов помогают узнавать часть речи и строить словарную цепочку. Они дают направление, но не отменяют проверку.", BODY),
    styled_table([
        ["Элемент", "Обычно выражает", "Примеры"],
        ["-anie / -enie", "процесс или действие", "cestovanie, nakupovanie, bývanie, platenie, učenie"],
        ["-osť", "качество или состояние", "rýchlosť, možnosť, bezpečnosť, spokojnosť"],
        ["-ný", "признак или отношение", "pracovný, zdravotný, bezpečný, rodinný"],
        ["-ový", "отношение к предмету/сфере", "internetový, cenový, jazykový, víkendový"],
        ["ne-", "отрицание или противоположность", "neznámy, nespokojný, nemožný, nepracovať"],
    ], [37 * mm, 57 * mm, 76 * mm], font_size=7.3),
    Spacer(1, 4 * mm),
    p("Как меняется предложение", H2),
    styled_table([
        ["Исходное сообщение", "Та же идея другим словом"],
        ["Cestujem často.", "Cestovanie ma baví."],
        ["Táto cesta je bezpečná.", "Bezpečnosť je pre mňa dôležitá."],
        ["Nie som spokojný.", "Chcem vyjadriť nespokojnosť."],
        ["Pracujem z domu.", "Dnes mám pracovný deň doma."],
    ], [78 * mm, 92 * mm], font_size=7.35),
    Spacer(1, 4 * mm),
    box("<b>Значение может сузиться.</b> <b>zdravý človek</b> - здоровый человек, но <b>zdravotný problém</b> - медицинская проблема. Родственные прилагательные не всегда взаимозаменяемы.", PALE, PINK, SMALL),
    PageBreak(),

    p("4. Прозрачные семьи и предел догадки", H1),
    p("Международные слова часто образуют удобные цепочки. На A2 они помогают понимать объявления, документы и рабочие сообщения.", BODY),
    styled_table([
        ["Существительное", "Глагол", "Прилагательное", "Пример"],
        ["informácia", "informovať", "informačný", "informačný systém"],
        ["organizácia", "organizovať", "organizačný", "organizačné zmeny"],
        ["komunikácia", "komunikovať", "komunikačný", "komunikačné schopnosti"],
        ["rezervácia", "rezervovať", "rezervačný", "rezervačný formulár"],
        ["kontrola", "kontrolovať", "kontrolný", "kontrolná otázka"],
    ], [38 * mm, 40 * mm, 42 * mm, 50 * mm], font_size=7.1),
    Spacer(1, 4 * mm),
    p("Три уровня уверенности", H2),
    styled_table([
        ["Уровень", "Что делать", "Пример"],
        ["Понятно", "слово и контекст совпадают", "rezervovať izbu"],
        ["Вероятно", "проверьте часть речи и сочетаемость", "organizačný problém"],
        ["Сомнительно", "не создавайте слово сами", "*informáciový -> informačný"],
    ], [32 * mm, 78 * mm, 60 * mm], font_size=7.35),
    Spacer(1, 4 * mm),
    box("<b>Полезная карточка:</b> записывайте 3-4 члена семьи и одну фразу: <b>rezervácia - rezervovať - rezervačný - Chcem rezervovať izbu.</b>", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    p("Мини-диалог", H2),
    box("<b>A:</b> Máte rezerváciu?<br/><b>B:</b> Áno, rezervoval som izbu online.<br/><b>A:</b> Ukážte mi, prosím, rezervačný email.<br/><b>B:</b> Samozrejme, tu je potvrdenie.", ALT, ROSE, SMALL),
    PageBreak(),

    p("5. Частые ошибки и упражнения", H1),
    box("<b>Три ошибки:</b> считать похожие слова полными синонимами; механически добавлять суффикс; учить форму без собственного примера.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    p("Упражнение 1. Найдите семью", H2),
    p("Разделите на три семьи: <b>pracovať, bezpečnosť, pracovník, cestovanie, bezpečný, pracovný, cestovať, nebezpečný, cestovateľ</b>.", SMALL),
    p("Упражнение 2. Выберите слово", H2),
    p("1) Mám pracovný / pracovník deň. 2) Cestovať / Cestovanie ma baví. 3) Toto je bezpečnosť / bezpečné miesto. 4) Potrebujem informačný / informovať systém.", SMALL),
    p("Упражнение 3. Образуйте нужное слово", H2),
    p("1) rýchly -> качество; 2) spokojný -> отрицательное качество; 3) rezervácia -> глагол; 4) učiť -> человек, мужчина и женщина.", SMALL),
    p("Упражнение 4. Исправьте", H2),
    p("1) Moja sestra je učiteľ. 2) Potrebujem informáciový formulár. 3) Bezpečný je pre nás dôležitá. 4) Náš kolega je skúsená pracovníčka.", SMALL),
    p("Упражнение 5. Переведите", H2),
    p("1) Путешествия меня радуют. 2) Это безопасное место. 3) Мне нужна информация о бронировании. 4) Наша новая коллега - специалист.", SMALL),
    p("Упражнение 6. Личная словарная сеть", H2),
    p("Выберите тему: работа, учёба или путешествия. Напишите 5-6 предложений и используйте минимум пять родственных слов из двух семей.", SMALL),
    PageBreak(),

    p("6. Ответы и проверка мастерства", H1),
    p("Ответы", H2),
    p("<b>1.</b> práca: pracovať, pracovník, pracovný; bezpečný: bezpečnosť, bezpečný, nebezpečný; cesta: cestovať, cestovanie, cestovateľ.", SMALL),
    p("<b>2.</b> 1) pracovný; 2) Cestovanie; 3) bezpečné; 4) informačný.", SMALL),
    p("<b>3.</b> 1) rýchlosť; 2) nespokojnosť; 3) rezervovať; 4) učiteľ, učiteľka.", SMALL),
    p("<b>4.</b> 1) Moja sestra je učiteľka. 2) Potrebujem informačný formulár. 3) Bezpečnosť je pre nás dôležitá. 4) Náš kolega je skúsený pracovník.", SMALL),
    p("<b>5.</b> 1) Cestovanie ma baví. 2) Toto je bezpečné miesto. 3) Potrebujem informáciu o rezervácii. 4) Naša nová kolegyňa je špecialistka.", SMALL),
    p("<b>6. Возможный ответ:</b> Pracujem v malej organizácii. Moja práca je zaujímavá. Som spokojný pracovník a mám dobrú kolegyňu. Organizujeme informačné stretnutia. Dobrá organizácia práce je pre nás dôležitá.", SMALL),
    p("Итог в четырёх пунктах", H2),
    styled_table([
        ["✓", "Я нахожу общую смысловую основу и замечаю её изменения."],
        ["✓", "Я узнаю частые элементы -anie/-enie, -osť, -ný/-ový и ne-."],
        ["✓", "Я учу названия людей вместе с женскими формами."],
        ["✓", "Я проверяю догадку и записываю слово в живом контексте."],
    ], [12 * mm, 158 * mm], font_size=8.0, header=False),
    Spacer(1, 4 * mm),
    box("<b>Финальная проверка:</b> составьте сеть из шести слов вокруг одной знакомой основы. Отметьте часть речи, перевод и придумайте три предложения без подсказки.", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    p("Следующий шаг", H2),
    p("Добавляйте к каждому новому слову хотя бы два родственника. Если форма или значение неочевидны, не угадывайте продуктивность модели - проверьте словарь. Затем переходите к PDF 1.5 с картой падежей и управления.", BODY),
]

doc.build(story)
print(OUTPUT)
