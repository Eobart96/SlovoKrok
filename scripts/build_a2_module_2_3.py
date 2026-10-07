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
OUTPUT = ROOT / "output" / "pdf" / "A2" / "Module_02" / "Slovak_A2_Tema_2_3_Akuzativ_edinstvennogo_chisla.pdf"
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
TITLE = ParagraphStyle("Title", fontName="Arial-Bold", fontSize=23, leading=27, textColor=colors.white, alignment=TA_LEFT, spaceAfter=5 * mm)
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
        canvas.drawString(20 * mm, height - 12 * mm, "SLOVAK A2  |  ТЕМА 2.3")
        canvas.drawRightString(width - 20 * mm, height - 12 * mm, "Akuzatív singular: согласование")
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
    title="Slovak A2 - Тема 2.3 - Akuzatív единственного числа: полное согласование", author="SlovoKrok",
)
frame = Frame(20 * mm, 18 * mm, 170 * mm, 257 * mm, id="main", leftPadding=0, rightPadding=0)
doc.addPageTemplates([PageTemplate(id="series", frames=[frame], onPage=draw_page)])

story = [
    p("МОДУЛЬ 2  •  ПАДЕЖИ И УПРАВЛЕНИЕ A2", COVER_KICKER),
    p("Akuzatív единственного числа:<br/>полное согласование", TITLE),
    p("Akuzatív jednotného čísla: úplná zhoda", SUBTITLE),
    Spacer(1, 34 * mm),
    p("Akuzatív отвечает на koho? čo? и оформляет прямой объект. На A2 важно изменить не одно существительное, а всю группу: указание, притяжательное слово, прилагательное и название объекта.", BODY),
    p("После модуля вы сможете:", H2),
    styled_table([
        ["1", "различать мужской одушевлённый и неодушевлённый объект"],
        ["2", "строить формы toho / ten, tú, to и môjho / môj, moju, moje"],
        ["3", "согласовывать прилагательное и существительное во всей группе"],
        ["4", "заменять объект местоимениями ma / ťa / ho / ju / nás / vás / ich"],
    ], [12 * mm, 158 * mm], font_size=8.0, header=False),
    Spacer(1, 3 * mm),
    box("<b>Главная формула:</b> vidím + toho môjho nového kolegu / tú moju novú kolegyňu / to moje nové auto.", PALE, PINK),
    PageBreak(),

    p("1. Четыре модели объекта", H1),
    p("Сначала определите род и одушевлённость. Затем измените всю цепочку. Мужской неодушевлённый и средний род часто совпадают с Nominatív, но мужской одушевлённый и женский получают особые формы.", BODY),
    styled_table([
        ["Тип", "Указание", "Полная группа", "Перевод"],
        ["муж. одуш.", "ten -> toho", "Vidím toho nového kolegu.", "Я вижу того нового коллегу."],
        ["муж. неодуш.", "ten -> ten", "Kupujem ten nový telefón.", "Я покупаю тот новый телефон."],
        ["женский", "tá -> tú", "Poznám tú milú učiteľku.", "Я знаю ту милую учительницу."],
        ["средний", "to -> to", "Hľadám to malé mesto.", "Я ищу тот маленький город."],
    ], [31 * mm, 32 * mm, 67 * mm, 40 * mm], font_size=6.9),
    p("Что происходит с существительным", H2),
    styled_table([
        ["Модель", "Nominatív -> Akuzatív", "Ещё примеры"],
        ["муж. одуш.", "kolega -> kolegu", "muž -> muža; učiteľ -> učiteľa; priateľ -> priateľa"],
        ["муж. неодуш.", "telefón -> telefón", "počítač -> počítač; dom -> dom"],
        ["женский на -a", "kniha -> knihu", "žena -> ženu; ulica -> ulicu; kolegyňa -> kolegyňu"],
        ["женский на согласную", "vec -> vec", "kosť -> kosť; možnosť -> možnosť"],
        ["средний", "auto -> auto", "mesto -> mesto; stretnutie -> stretnutie"],
    ], [34 * mm, 51 * mm, 85 * mm], font_size=7.0),
    Spacer(1, 3 * mm),
    box("<b>Главный контраст:</b> <b>Vidím nového učiteľa</b>, но <b>Vidím nový telefón</b>. В мужском роде именно одушевлённость меняет форму всей группы.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    PageBreak(),

    p("2. Полное согласование", H1),
    p("Указательное, притяжательное и прилагательное слово принимают ту же форму, что требует объект. Проверяйте группу слева направо.", BODY),
    styled_table([
        ["Nominatív", "Akuzatív", "Перевод объекта"],
        ["ten môj nový kolega", "toho môjho nového kolegu", "того моего нового коллегу"],
        ["ten môj nový telefón", "ten môj nový telefón", "тот мой новый телефон"],
        ["tá moja dobrá kamarátka", "tú moju dobrú kamarátku", "ту мою хорошую подругу"],
        ["to moje malé auto", "to moje malé auto", "ту мою маленькую машину"],
    ], [58 * mm, 67 * mm, 45 * mm], font_size=7.0),
    p("Формы притяжательных слов", H2),
    styled_table([
        ["Тип объекта", "môj", "náš", "Пример"],
        ["мужчина", "môjho", "nášho", "Eva čaká môjho brata. - Ева ждёт моего брата."],
        ["предмет, муж. род", "môj", "náš", "Peter má môj nový kľúč. - У Петера мой новый ключ."],
        ["женский род", "moju", "našu", "Peter pozýva moju sestru. - Петер приглашает мою сестру."],
        ["средний род", "moje", "naše", "Poznám naše mesto. - Я знаю наш город."],
    ], [38 * mm, 27 * mm, 27 * mm, 78 * mm], font_size=7.0),
    Spacer(1, 3 * mm),
    box("<b>Svoj вместо môj:</b> если объект принадлежит подлежащему, обычно нужен <b>svoj</b>: <b>Peter čaká svojho brata</b>. Форма <b>môjho</b> означает брата говорящего, а не Петера.", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    PageBreak(),

    p("3. Личные местоимения вместо объекта", H1),
    p("Когда объект уже известен, существительное заменяется местоимением. Короткие формы ma, ťa, ho - клитики: они обычно занимают вторую позицию, как в теме 1.3.", BODY),
    styled_table([
        ["Кто?", "Akuzatív", "Пример и перевод"],
        ["ja", "mňa / ma", "Peter ma pozná. - Петер меня знает."],
        ["ty", "teba / ťa", "Čakám ťa. - Я тебя жду."],
        ["on", "jeho / ho", "Poznáš ho? - Ты его знаешь?"],
        ["ona", "ju", "Vidím ju každý deň. - Я вижу её каждый день."],
        ["ono", "ho", "Mám ho doma. - Оно у меня дома."],
        ["my", "nás", "Učiteľ nás počuje. - Учитель нас слышит."],
        ["vy", "vás", "Pozývam vás na obed. - Приглашаю вас на обед."],
        ["oni / ony", "ich", "Hľadám ich. - Я их ищу."],
    ], [28 * mm, 35 * mm, 107 * mm], font_size=7.05),
    p("Короткая или полная форма?", H2),
    styled_table([
        ["Нейтрально, без акцента", "Контраст или исправление"],
        ["Peter ma pozná.", "MŇA pozná, teba nie. - Меня знает, тебя нет."],
        ["Včera som ho videl.", "JEHO som videl, nie brata. - Его я видел, не брата."],
    ], [84 * mm, 86 * mm], font_size=7.15),
    Spacer(1, 3 * mm),
    box("<b>Не ставьте клитики в начало:</b> нейтрально <b>Peter ma pozná</b> и <b>Včera som ho videl</b>. Начальная позиция возможна только у ударной формы при сильном контрасте: <b>MŇA pozná</b>.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    PageBreak(),

    p("4. Akuzatív в реальной задаче", H1),
    p("Глаголы vidieť, poznať, čakať, hľadať, mať, kupovať, vybrať si и pozvať часто вводят прямой объект. Сначала назовите его полной группой, затем используйте местоимение.", BODY),
    p("Модель: выбор покупки", H2),
    box("Hľadám <b>nový pracovný telefón</b>. Vidím <b>tento čierny model</b> a chcem si <b>ho</b> vyskúšať. Má dobrý fotoaparát, ale nemá veľkú batériu. Preto si vyberám <b>ten druhý telefón</b>. Predavač <b>ho</b> zabalí a ja <b>ho</b> kúpim.", PALE, ROSE, SMALL),
    p("Перевод: Я ищу новый рабочий телефон. Вижу эту чёрную модель и хочу её попробовать. У неё хорошая камера, но нет большой батареи. Поэтому выбираю второй телефон. Продавец его упакует, а я его куплю.", SMALL),
    p("Мини-диалог: приглашение", H2),
    box("<b>A:</b> Poznáš toho nového kolegu?<br/><b>B:</b> Áno, poznám ho. Volá sa Martin.<br/><b>A:</b> Chcem ho pozvať na obed.<br/><b>B:</b> Pozvi aj tú novú kolegyňu.<br/><b>A:</b> Dobre. Pozvem ju po stretnutí.<br/><b>B:</b> Ona ťa určite rada uvidí.", ALT, ROSE, SMALL),
    p("Перевод: Ты знаешь того нового коллегу? - Да, его зовут Мартин. - Хочу пригласить его на обед. - Пригласи и новую коллегу. - Хорошо, приглашу её после встречи. - Она наверняка будет рада тебя увидеть.", SMALL),
    p("Банк полезных сочетаний", H2),
    styled_table([
        ["Люди", "Предметы", "Места и события"],
        ["čakať dobrého priateľa", "kúpiť nový počítač", "poznať staré mesto"],
        ["pozvať milú susedu", "hľadať tú dôležitú vec", "zrušiť pracovné stretnutie"],
    ], [57 * mm, 57 * mm, 56 * mm], font_size=7.0),
    PageBreak(),

    p("5. Частые ошибки и упражнения", H1),
    box("<b>Алгоритм:</b> найдите прямой объект -> определите род и одушевлённость -> измените всю группу -> при повторе замените её подходящим местоимением.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    p("Упражнение 1. Выберите форму", H2),
    p("1) Vidím (toho / ten) učiteľa. 2) Kupujem (toho / ten) telefón. 3) Poznám (tú / tá) ženu. 4) Hľadám (to / toho) auto. 5) Čakám (tú / to) kamarátku.", SMALL),
    p("Упражнение 2. Преобразуйте всю группу", H2),
    p("1) ten nový kolega; 2) tá milá suseda; 3) môj dobrý priateľ; 4) moje malé mesto; 5) náš pracovný počítač.", SMALL),
    p("Упражнение 3. Замените объект местоимением", H2),
    p("1) Peter pozná mňa. 2) Čakám teba. 3) Vidím Martina. 4) Pozývam Janu. 5) Učiteľ počuje nás. 6) Hľadám Petra a Janu. Используйте нейтральную короткую форму, где она есть.", SMALL),
    p("Упражнение 4. Исправьте ошибки", H2),
    p("1) Vidím ten nového kolegu. 2) Hľadám tú nový knihu. 3) Kupujem toho drahého telefón. 4) Peter čaká jeho brata, если речь о брате Петера. 5) Ma Peter pozná.", SMALL),
    p("Упражнение 5. Переведите", H2),
    p("1) Я знаю эту новую учительницу. 2) Мы ждём нашего хорошего друга. 3) Ты видишь тот маленький дом? 4) Петер меня знает, но не знает тебя. 5) Я ищу его и её.", SMALL),
    p("Упражнение 6. Опишите выбор", H2),
    p("Напишите 5-7 предложений о покупке или приглашении. Используйте четыре разных модели объекта, одну группу со svoj и минимум три личных местоимения.", SMALL),
    PageBreak(),

    p("6. Ответы и проверка мастерства", H1),
    p("Ответы", H2),
    p("<b>1.</b> toho učiteľa; ten telefón; tú ženu; to auto; tú kamarátku.", TINY),
    p("<b>2.</b> toho nového kolegu; tú milú susedu; môjho dobrého priateľa; moje malé mesto; náš pracovný počítač.", TINY),
    p("<b>3.</b> Peter ma pozná. Čakám ťa. Vidím ho. Pozývam ju. Učiteľ nás počuje. Hľadám ich.", TINY),
    p("<b>4.</b> 1) Vidím toho nového kolegu. 2) Hľadám tú novú knihu. 3) Kupujem ten drahý telefón. 4) Peter čaká svojho brata. 5) Peter ma pozná.", TINY),
    p("<b>5.</b> 1) Poznám túto novú učiteľku. 2) Čakáme nášho dobrého priateľa. 3) Vidíš ten malý dom? 4) Peter ma pozná, ale teba nepozná. 5) Hľadám ho a ju. Возможны и другие естественные варианты.", TINY),
    p("<b>6. Модель:</b> Hľadám nový notebook. V obchode vidím tento ľahký model. Predavač mi ho ukáže. Páči sa mi, ale chcem väčšiu obrazovku. Predavač ponúka svoj nový model. Ja si ho vyberiem a kúpim ho.", TINY),
    p("Итог в четырёх пунктах", H2),
    styled_table([
        ["OK", "Я различаю мужской одушевлённый и неодушевлённый объект."],
        ["OK", "Я строю формы toho / ten, tú, to и согласую всю группу."],
        ["OK", "Я выбираю môjho / môj, moju / moje и использую svoj."],
        ["OK", "Я заменяю объект формами ma / ťa / ho / ju / nás / vás / ich."],
    ], [12 * mm, 158 * mm], font_size=7.6, header=False),
    Spacer(1, 3 * mm),
    box("<b>Финальная проверка:</b> назовите по одному человеку и предмету, которых вы видите или ищете, сначала полной группой, затем местоимением. Если формы согласованы, цель достигнута.", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    p("Следующий шаг", H2),
    p("В модуле 2.4 вы перенесёте эту систему во множественное число: <b>vidím tých nových kolegov</b> и <b>kupujem tie nové knihy</b>.", SMALL),
]

doc.build(story)
print(OUTPUT)
