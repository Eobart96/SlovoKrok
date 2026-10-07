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
OUTPUT = ROOT / "output" / "pdf" / "A2" / "Module_02" / "Slovak_A2_Tema_2_2_Nominativ_mnozhestvennogo_chisla_lyudi.pdf"
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
        canvas.drawString(20 * mm, height - 12 * mm, "SLOVAK A2  |  ТЕМА 2.2")
        canvas.drawRightString(width - 20 * mm, height - 12 * mm, "Nominatív plural: люди")
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
    title="Slovak A2 - Тема 2.2 - Nominatív множественного числа: люди", author="SlovoKrok",
)
frame = Frame(20 * mm, 18 * mm, 170 * mm, 257 * mm, id="main", leftPadding=0, rightPadding=0)
doc.addPageTemplates([PageTemplate(id="series", frames=[frame], onPage=draw_page)])

story = [
    p("МОДУЛЬ 2  •  ПАДЕЖИ И УПРАВЛЕНИЕ A2", COVER_KICKER),
    p("Nominatív множественного числа:<br/>люди", TITLE),
    p("Nominatív množného čísla: ľudia", SUBTITLE),
    Spacer(1, 34 * mm),
    p("В теме 2.1 вы согласовывали предметы и понятия: tie nové knihy. Теперь добавляем особую цепочку для мужчин и смешанных групп: tí noví kolegovia.", BODY),
    p("После модуля вы сможете:", H2),
    styled_table([
        ["1", "образовывать частотные формы мужского одушевлённого рода на -i, -ia и -ovia"],
        ["2", "согласовывать tí / títo, moji / naši и прилагательные на -í"],
        ["3", "говорить о профессиях, национальностях и смешанных группах людей"],
        ["4", "употреблять dvaja, traja, štyria и различать конструкции от пяти"],
    ], [12 * mm, 158 * mm], font_size=8.0, header=False),
    Spacer(1, 3 * mm),
    box("<b>Главная формула:</b> tí / títo + naši + noví + kolegovia + sú / boli + milí.", PALE, PINK),
    PageBreak(),

    p("1. Три частотных окончания", H1),
    p("У мужских названий людей Nominatív plural нельзя надёжно построить по одной универсальной формуле. Запоминайте новое слово вместе с формой множественного числа.", BODY),
    styled_table([
        ["Окончание", "Единственное -> множественное", "Перевод"],
        ["-i", "chlap -> chlapi", "мужчина / парень -> мужчины / парни"],
        ["-i", "študent -> študenti", "студент -> студенты"],
        ["-i", "Slovák -> Slováci", "словак -> словаки"],
        ["-i", "pracovník -> pracovníci", "работник -> работники"],
        ["-ia", "učiteľ -> učitelia", "учитель -> учителя"],
        ["-ia", "priateľ -> priatelia", "друг -> друзья"],
        ["-ia", "brat -> bratia", "брат -> братья"],
        ["-ovia", "kolega -> kolegovia", "коллега -> коллеги"],
        ["-ovia", "otec -> otcovia", "отец -> отцы"],
        ["-ovia", "syn -> synovia", "сын -> сыновья"],
    ], [27 * mm, 75 * mm, 68 * mm], font_size=7.1),
    Spacer(1, 3 * mm),
    box("<b>Не угадывайте окончание:</b> учите парами <b>učiteľ - učitelia</b>, <b>kolega - kolegovia</b>. У формы на -i возможна смена согласной: Slovák - Slováci, pracovník - pracovníci.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    PageBreak(),

    p("2. Профессии, национальности и исключения", H1),
    p("Эти формы особенно нужны, чтобы представить команду, описать соседей или сказать, кто участвует в событии.", BODY),
    styled_table([
        ["Форма", "Пример", "Перевод"],
        ["programátori", "Programátori pracujú z domu.", "Программисты работают из дома."],
        ["lekári", "Lekári sú dnes v nemocnici.", "Врачи сегодня в больнице."],
        ["predavači", "Predavači sú veľmi ochotní.", "Продавцы очень отзывчивые."],
        ["kuchári", "Kuchári pripravujú obed.", "Повара готовят обед."],
        ["Slováci", "Slováci hovoria po slovensky.", "Словаки говорят по-словацки."],
        ["Česi", "Česi sú naši susedia.", "Чехи - наши соседи."],
        ["Nemci", "Tí Nemci bývajú v hoteli.", "Те немцы живут в гостинице."],
        ["Taliani", "Taliani prišli včera.", "Итальянцы приехали вчера."],
    ], [32 * mm, 78 * mm, 60 * mm], font_size=7.05),
    p("Частотные формы, которые нужно знать", H2),
    styled_table([
        ["človek -> ľudia", "muž -> muži", "pán -> páni"],
        ["sused -> susedia", "rodič -> rodičia", "hosť -> hostia"],
    ], [57 * mm, 56 * mm, 57 * mm], font_size=7.35, header=False),
    Spacer(1, 3 * mm),
    box("<b>Смешанная группа:</b> если в группе есть мужчины и женщины, обычно используется мужская одушевлённая форма: <b>študenti, kolegovia, Slováci</b>. Только о женщинах: <b>študentky, kolegyne, Slovenky</b>.", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    PageBreak(),

    p("3. Полная цепочка согласования", H1),
    p("Особая форма видна во всей именной группе. Сравните цепочку для мужчин с общей формой для женщин, детей и предметов.", BODY),
    styled_table([
        ["Кого называем", "Указание + принадлежность", "Прилагательное + существительное"],
        ["мужчины / смешанная группа", "tí / títo; moji / naši", "noví kolegovia; dobrí priatelia"],
        ["женщины", "tie / tieto; moje / naše", "nové kolegyne; dobré priateľky"],
        ["дети", "tie / tieto; moje / naše", "malé deti; milé deti"],
    ], [45 * mm, 58 * mm, 67 * mm], font_size=7.2),
    p("От единственного числа к множественному", H2),
    styled_table([
        ["Единственное число", "Множественное число", "Перевод"],
        ["ten nový kolega", "tí noví kolegovia", "те новые коллеги"],
        ["tento mladý učiteľ", "títo mladí učitelia", "эти молодые учителя"],
        ["môj dobrý priateľ", "moji dobrí priatelia", "мои хорошие друзья"],
        ["náš slovenský študent", "naši slovenskí študenti", "наши словацкие студенты"],
        ["ten cudzí muž", "tí cudzí muži", "те иностранные мужчины"],
    ], [55 * mm, 61 * mm, 54 * mm], font_size=7.05),
    Spacer(1, 3 * mm),
    box("<b>Проверяйте четыре формы:</b> <b>tí naši noví kolegovia sú milí</b>. У мягкого прилагательного форма не меняется на письме: <b>cudzí muž - cudzí muži</b>.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    PageBreak(),

    p("4. Два, три, четыре человека", H1),
    p("Перед мужскими названиями людей используются специальные формы числительных. С существительными других групп остаются dva / dve, tri, štyri.", BODY),
    styled_table([
        ["Число", "Мужчины", "Для сравнения"],
        ["2", "dvaja muži; dvaja kolegovia", "dve ženy; dve deti; dva domy"],
        ["3", "traja priatelia; traja učitelia", "tri ženy; tri deti; tri domy"],
        ["4", "štyria študenti; štyria Slováci", "štyri ženy; štyri deti; štyri domy"],
    ], [25 * mm, 73 * mm, 72 * mm], font_size=7.2),
    p("Пять и больше", H2),
    p("Для людей возможны две модели: <b>piati študenti prišli</b> и <b>päť študentov prišlo</b>. Первая подчёркивает людей как действующую группу; вторая считает количество и требует Genitív plural. Здесь запомните контраст, а формы Genitív системно появятся в следующих темах.", SMALL),
    p("Модель текста", H2),
    box("<b>V našom tíme pracujú štyria Slováci a dvaja Česi.</b> Títo noví kolegovia sú skúsení programátori. Dvaja kolegovia pracujú z domu a štyria chodia do kancelárie. Naši vedúci sú priateľskí a všetci pracovníci sú spokojní.", PALE, ROSE, SMALL),
    p("Перевод: В нашей команде работают четыре словака и два чеха. Эти новые коллеги - опытные программисты. Два коллеги работают из дома, а четверо ходят в офис. Наши руководители дружелюбны, и все работники довольны.", SMALL),
    p("Мини-диалог", H2),
    box("<b>A:</b> Kto sú tí noví ľudia?<br/><b>B:</b> To sú naši kolegovia z Prahy.<br/><b>A:</b> Koľkí prišli?<br/><b>B:</b> Prišli traja kolegovia a dvaja vedúci.<br/><b>A:</b> Sú všetci Česi?<br/><b>B:</b> Nie, dvaja sú Česi a traja sú Slováci.", ALT, ROSE, SMALL),
    PageBreak(),

    p("5. Частые ошибки и упражнения", H1),
    box("<b>Три сигнала:</b> мужчины или смешанная группа -> <b>tí / moji / noví</b>; только женщины и дети -> <b>tie / moje / nové</b>; 2-4 мужчины -> <b>dvaja / traja / štyria</b>.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    p("Упражнение 1. Образуйте множественное число", H2),
    p("1) študent; 2) učiteľ; 3) kolega; 4) Slovák; 5) otec; 6) človek; 7) priateľ; 8) pracovník.", SMALL),
    p("Упражнение 2. Преобразуйте всю группу", H2),
    p("1) ten nový kolega; 2) tento mladý lekár; 3) môj dobrý priateľ; 4) náš slovenský učiteľ; 5) ten cudzí muž.", SMALL),
    p("Упражнение 3. Выберите форму", H2),
    p("1) (tí / tie) milí susedia; 2) (moji / moje) dobrí priatelia; 3) (noví / nové) kolegyne; 4) (naši / naše) malé deti; 5) (títo / tieto) slovenskí študenti.", SMALL),
    p("Упражнение 4. Вставьте числительное", H2),
    p("1) ___ muži (2); 2) ___ učitelia (3); 3) ___ študenti (4); 4) ___ ženy (2); 5) ___ deti (3).", SMALL),
    p("Упражнение 5. Исправьте ошибки", H2),
    p("1) Tie nový kolegovia sú milé. 2) Moje dobrí priatelia prišli. 3) Traja ženy pracujú. 4) Títo slovenské študenti sú mladé. 5) Dva učitelia sú v škole.", SMALL),
    p("Упражнение 6. Представьте группу", H2),
    p("Напишите 5-7 предложений о команде, семье или группе туристов. Используйте минимум четыре формы людей, полную цепочку согласования, dvaja / traja / štyria и один контраст с группой женщин или детей.", SMALL),
    PageBreak(),

    p("6. Ответы и проверка мастерства", H1),
    p("Ответы", H2),
    p("<b>1.</b> študenti; učitelia; kolegovia; Slováci; otcovia; ľudia; priatelia; pracovníci.", TINY),
    p("<b>2.</b> tí noví kolegovia; títo mladí lekári; moji dobrí priatelia; naši slovenskí učitelia; tí cudzí muži.", TINY),
    p("<b>3.</b> tí; moji; nové; naše; títo.", TINY),
    p("<b>4.</b> dvaja muži; traja učitelia; štyria študenti; dve ženy; tri deti.", TINY),
    p("<b>5.</b> 1) Tí noví kolegovia sú milí. 2) Moji dobrí priatelia prišli. 3) Tri ženy pracujú. 4) Títo slovenskí študenti sú mladí. 5) Dvaja učitelia sú v škole.", TINY),
    p("<b>6. Модель:</b> V našej skupine sú traja Slováci a dve Slovenky. Tí slovenskí študenti sú moji dobrí priatelia. Dvaja študenti pracujú a jeden študuje. Slovenky sú nové kolegyne. Všetci ľudia sú mladí a priateľskí. Naši učitelia sú spokojní.", TINY),
    p("Итог в четырёх пунктах", H2),
    styled_table([
        ["OK", "Я знаю частотные формы на -i, -ia и -ovia."],
        ["OK", "Я согласую tí / títo, moji / naši и прилагательное на -í."],
        ["OK", "Я различаю группы мужчин, женщин, детей и смешанные группы."],
        ["OK", "Я употребляю dvaja, traja и štyria с мужскими названиями людей."],
    ], [12 * mm, 158 * mm], font_size=7.7, header=False),
    Spacer(1, 3 * mm),
    box("<b>Финальная проверка:</b> представьте трёх знакомых одной фразой и назовите их профессию или национальность. Если вся цепочка согласована, цель модуля достигнута.", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    p("Следующий шаг", H2),
    p("В модуле 2.3 вы перенесёте полное согласование в Akuzatív единственного числа: <b>vidím toho nového kolegu</b>, <b>poznám tú milú učiteľku</b>.", SMALL),
]

doc.build(story)
print(OUTPUT)
