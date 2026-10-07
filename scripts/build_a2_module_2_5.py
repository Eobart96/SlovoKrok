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
OUTPUT = ROOT / "output" / "pdf" / "A2" / "Module_02" / "Slovak_A2_Tema_2_5_Genitiv_edinstvennogo_chisla.pdf"
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
TITLE = ParagraphStyle("Title", fontName="Arial-Bold", fontSize=22, leading=26, textColor=colors.white, alignment=TA_LEFT, spaceAfter=5 * mm)
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
        canvas.drawString(20 * mm, height - 12 * mm, "SLOVAK A2  |  ТЕМА 2.5")
        canvas.drawRightString(width - 20 * mm, height - 12 * mm, "Genitív единственного числа")
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
    title="Slovak A2 - Тема 2.5 - Genitív единственного числа", author="SlovoKrok",
)
frame = Frame(20 * mm, 18 * mm, 170 * mm, 257 * mm, id="main", leftPadding=0, rightPadding=0)
doc.addPageTemplates([PageTemplate(id="series", frames=[frame], onPage=draw_page)])

story = [
    p("МОДУЛЬ 2  •  ПАДЕЖИ И УПРАВЛЕНИЕ A2", COVER_KICKER),
    p("Genitív единственного числа:<br/>отсутствие, происхождение и границы", TITLE),
    p("Genitív jednotného čísla", SUBTITLE),
    Spacer(1, 29 * mm),
    p("Genitív отвечает не только на otázku koho? čoho? В повседневной речи он показывает, чего нет, откуда и к кому мы идём, рядом с чем находимся и где проходят временные границы.", BODY),
    p("После модуля вы сможете:", H2),
    styled_table([
        ["1", "говорить об отсутствии с bez"],
        ["2", "различать направление do и исходную точку z/zo или od"],
        ["3", "описывать положение с okolo, blízko, vedľa и u"],
        ["4", "согласовывать существительное, прилагательное и местоимение в Genitív singular"],
    ], [12 * mm, 158 * mm], font_size=8.0, header=False),
    Spacer(1, 3 * mm),
    box("<b>Формула:</b> предлог + Genitív: bez teplej vody • do starého mesta • z malej kancelárie • od dobrého priateľa.", PALE, PINK),
    PageBreak(),

    p("1. Восемь ключевых предлогов", H1),
    p("После этих предлогов используйте Genitív. Смысл выбирает предлог, а форма существительного и зависимых слов показывает падеж.", BODY),
    styled_table([
        ["Предлог", "Значение", "Пример", "Перевод"],
        ["bez", "без, отсутствие", "bez teplej vody", "без тёплой воды"],
        ["do", "внутрь; до границы", "do starého mesta", "в старый город"],
        ["z / zo", "изнутри; происхождение", "z kancelárie / zo Slovenska", "из офиса / из Словакии"],
        ["od", "от лица или точки", "od lekára", "от врача"],
        ["okolo", "вокруг, около", "okolo veľkého parku", "вокруг большого парка"],
        ["blízko", "близко от", "blízko stanice", "недалеко от станции"],
        ["vedľa", "рядом с", "vedľa nášho hotela", "рядом с нашим отелем"],
        ["u", "у кого-то; у специалиста", "u mojej sestry / u lekára", "у сестры / у врача"],
    ], [22 * mm, 37 * mm, 61 * mm, 50 * mm], font_size=6.65),
    Spacer(1, 4 * mm),
    box("<b>Граница во времени:</b> od pondelka do piatka - с понедельника до пятницы; od rána do večera - с утра до вечера; do konca týždňa - до конца недели.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    PageBreak(),

    p("2. Формы существительных", H1),
    p("Род помогает выбрать модель, но у мужского рода окончание часто нужно запоминать вместе со словом.", BODY),
    styled_table([
        ["Род / модель", "Nominatív → Genitív", "Пример с предлогом"],
        ["муж., лицо", "kolega → kolegu; učiteľ → učiteľa", "bez kolegu; od učiteľa"],
        ["муж., -a", "brat → brata; hotel → hotela", "od brata; vedľa hotela"],
        ["муж., -u", "dom → domu; obchod → obchodu", "do domu; z obchodu"],
        ["жен., -y", "žena → ženy", "od ženy"],
        ["жен., -e", "ulica → ulice; práca → práce", "do ulice; z práce"],
        ["жен., согласная", "dlaň → dlane; soľ → soli", "bez dlane; bez soli"],
        ["сред., -a", "mesto → mesta; auto → auta; more → mora", "do mesta; vedľa auta; z mora"],
        ["сред., -ia", "námestie → námestia; stretnutie → stretnutia", "do námestia; zo stretnutia"],
        ["сред., особая", "dieťa → dieťaťa", "od dieťaťa"],
    ], [39 * mm, 65 * mm, 66 * mm], font_size=6.6),
    Spacer(1, 3 * mm),
    box("<b>Учите словарной парой:</b> dom - domu, park - parku, hotel - hotela, stôl - stola. У мужских неодушевлённых существительных нельзя всегда надёжно угадать -a или -u.", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    PageBreak(),

    p("3. Полное согласование и местоимения", H1),
    p("Вся именная группа получает Genitív. Для мужского и среднего рода зависимые слова обычно имеют -ého / -ho, для женского - -ej.", BODY),
    styled_table([
        ["Род", "Nominatív", "Genitív в группе", "Перевод"],
        ["муж.", "ten nový kolega", "bez toho nového kolegu", "без того нового коллеги"],
        ["муж.", "môj dobrý priateľ", "od môjho dobrého priateľa", "от моего хорошего друга"],
        ["жен.", "tá malá kancelária", "z tej malej kancelárie", "из того маленького офиса"],
        ["жен.", "moja staršia sestra", "u mojej staršej sestry", "у моей старшей сестры"],
        ["сред.", "to staré mesto", "do toho starého mesta", "в тот старый город"],
        ["сред.", "naše nové auto", "vedľa nášho nového auta", "рядом с нашей новой машиной"],
    ], [22 * mm, 42 * mm, 64 * mm, 42 * mm], font_size=6.75),
    p("Личные местоимения после предлога", H2),
    styled_table([
        ["Лицо", "Genitív", "Пример"],
        ["ja / ty", "mňa / teba", "bez mňa; vedľa teba"],
        ["on / ona", "neho / nej", "od neho; u nej"],
        ["my / vy", "nás / vás", "blízko nás; bez vás"],
        ["oni / ony", "nich", "okolo nich; bez nich"],
    ], [35 * mm, 43 * mm, 92 * mm], font_size=7.0),
    box("<b>После предлога:</b> neho, nej, nich - с начальным n: u neho, od nej, bez nich.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    PageBreak(),

    p("4. Z/zo или od? Do или u?", H1),
    p("Выбирайте предлог по образу движения или положения, а не переводите русское «из/от/у» автоматически.", BODY),
    styled_table([
        ["Ситуация", "Выбор", "Пример"],
        ["движение изнутри места", "z / zo", "Idem z kancelárie. - Я иду из офиса."],
        ["происхождение", "z / zo", "Som zo Slovenska. - Я из Словакии."],
        ["движение от человека", "od", "Idem od lekára. - Я иду от врача."],
        ["начальная граница", "od", "Pracujem od pondelka. - Работаю с понедельника."],
        ["движение внутрь", "do", "Idem do banky. - Я иду в банк."],
        ["нахождение у человека", "u", "Som u sestry. - Я у сестры."],
    ], [47 * mm, 27 * mm, 96 * mm], font_size=7.05),
    p("Мини-история", H2),
    box("Ráno idem <b>z domu do práce</b>. Pracujem <b>od ôsmej do štvrtej</b>. Po práci idem <b>z kancelárie</b> a potom <b>od lekára</b>. Večer som <b>u svojej sestry</b>. Býva <b>blízko hlavnej stanice</b>, <b>vedľa veľkého parku</b>.", PALE, ROSE, SMALL),
    p("Утром я иду из дома на работу. Работаю с восьми до четырёх. После работы выхожу из офиса, а затем иду от врача. Вечером я у своей сестры. Она живёт недалеко от главного вокзала, рядом с большим парком.", SMALL),
    box("<b>Сравните:</b> z kancelárie - движение изнутри места; od lekára - движение от человека.", ALT, ROSE, SMALL),
    PageBreak(),

    p("5. Частые ошибки и упражнения", H1),
    box("<b>Алгоритм:</b> выберите смысл → предлог → род и словарную форму существительного → согласуйте всю группу.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    p("Упражнение 1. Выберите предлог", H2),
    p("1) ___ teplej vody (без); 2) idem ___ kancelárie (из); 3) som ___ lekára (у); 4) bývam ___ stanice (близко); 5) idem ___ brata (от); 6) ___ pondelka ___ piatka (с ... до).", SMALL),
    p("Упражнение 2. Поставьте существительное в Genitív", H2),
    p("1) do (mesto); 2) z (práca); 3) bez (kolega); 4) vedľa (hotel); 5) u (sestra); 6) zo (stretnutie); 7) od (dieťa).", SMALL),
    p("Упражнение 3. Согласуйте всю группу", H2),
    p("1) bez (ten nový kolega); 2) do (to staré mesto); 3) z (tá malá kancelária); 4) od (môj dobrý priateľ); 5) vedľa (naše nové auto).", SMALL),
    p("Упражнение 4. Замените местоимением", H2),
    p("1) bez Petra; 2) u Márie; 3) blízko mňa a Petra; 4) od vás; 5) okolo študentov.", SMALL),
    p("Упражнение 5. Исправьте ошибки", H2),
    p("1) Idem z dom. 2) Som u moja sestra. 3) Býva vedľa nový hotel. 4) Som od Slovenska. 5) Bez ona nejdem.", SMALL),
    p("Упражнение 6. Переведите", H2),
    p("1) Я из Словакии. 2) Мы работаем с утра до вечера. 3) Он живёт рядом с нашим отелем. 4) Я иду от своего хорошего друга. 5) Без тебя я не пойду.", SMALL),
    PageBreak(),

    p("6. Ответы и проверка мастерства", H1),
    p("Ответы", H2),
    p("<b>1.</b> bez teplej vody; z kancelárie; u lekára; blízko stanice; od brata; od pondelka do piatka.", TINY),
    p("<b>2.</b> do mesta; z práce; bez kolegu; vedľa hotela; u sestry; zo stretnutia; od dieťaťa.", TINY),
    p("<b>3.</b> bez toho nového kolegu; do toho starého mesta; z tej malej kancelárie; od môjho dobrého priateľa; vedľa nášho nového auta.", TINY),
    p("<b>4.</b> bez neho; u nej; blízko nás; od vás; okolo nich.", TINY),
    p("<b>5.</b> 1) Idem z domu. 2) Som u mojej sestry. 3) Býva vedľa nového hotela. 4) Som zo Slovenska. 5) Bez nej nejdem.", TINY),
    p("<b>6.</b> 1) Som zo Slovenska. 2) Pracujeme od rána do večera. 3) Býva vedľa nášho hotela. 4) Idem od svojho dobrého priateľa. 5) Bez teba nejdem.", TINY),
    p("Итог в четырёх пунктах", H2),
    styled_table([
        ["OK", "Я использую bez, do, z/zo, od, okolo, blízko, vedľa и u с Genitív."],
        ["OK", "Я различаю z/zo для движения изнутри и od для движения от человека или границы."],
        ["OK", "Я согласую всю группу: bez toho nového kolegu / z tej malej kancelárie."],
        ["OK", "После предлога я говорю neho, nej, nich."],
    ], [12 * mm, 158 * mm], font_size=7.45, header=False),
    Spacer(1, 3 * mm),
    box("<b>Финальная проверка:</b> скажите, откуда вы пришли, у кого были, рядом с чем живёте и в какие временные границы работаете. Используйте четыре разных предлога.", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    p("Следующий шаг", H2),
    p("В теме 2.6 Genitív будет выражать количество и меру: <b>kilo, liter, kus, kúsok, plátok, trochu, veľa, málo, viac, menej</b>, а также сочетания с числительными от пяти.", SMALL),
]

doc.build(story)
print(OUTPUT)
