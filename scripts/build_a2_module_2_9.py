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
OUTPUT = ROOT / "output" / "pdf" / "A2" / "Module_02" / "Slovak_A2_Tema_2_9_Lokal_mesto_i_tema_razgovora.pdf"
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
TINY = ParagraphStyle("Tiny", parent=BODY, fontSize=7.15, leading=8.9, spaceAfter=1.25 * mm)
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
        canvas.drawString(20 * mm, height - 12 * mm, "A2 2.9  |  Lokál: место и тема разговора")
    canvas.setFont("Arial", 8)
    canvas.setFillColor(MUTED)
    canvas.drawString(20 * mm, 9 * mm, "SlovoKrok | личный учебный модуль")
    canvas.drawRightString(width - 20 * mm, 9 * mm, f"стр. {page} / 7")
    canvas.restoreState()


doc = BaseDocTemplate(
    str(OUTPUT), pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=20 * mm, bottomMargin=18 * mm,
    title="Slovak A2 - Тема 2.9 - Lokál: место и тема разговора", author="SlovoKrok",
)
frame = Frame(20 * mm, 18 * mm, 170 * mm, 257 * mm, id="main", leftPadding=0, rightPadding=0)
doc.addPageTemplates([PageTemplate(id="series", frames=[frame], onPage=draw_page)])

story = [
    p("МОДУЛЬ 2  •  ПАДЕЖИ И УПРАВЛЕНИЕ A2", COVER_KICKER),
    p("Lokál:<br/>место и тема разговора", TITLE),
    p("Lokál: miesto a téma rozhovoru", SUBTITLE),
    Spacer(1, 33 * mm),
    p("Lokál помогает ответить на два практических вопроса: <b>kde?</b> - где находится человек или предмет, и <b>o kom? o čom?</b> - о ком или о чём говорят.", BODY),
    p("После модуля вы сможете:", H2),
    styled_table([
        ["1", "описывать местонахождение с v/vo, na и pri"],
        ["2", "говорить о теме разговора с предлогом o"],
        ["3", "согласовывать существительное и прилагательное в Lokál"],
        ["4", "употреблять o mne/tebe/ňom/nej/nás/vás/nich"],
    ], [12 * mm, 158 * mm], font_size=7.85, header=False),
    Spacer(1, 3 * mm),
    box("<b>Главная формула:</b> Som <b>v novom byte</b>. Hovoríme <b>o novom byte</b>.", PALE, PINK),
    PageBreak(),

    p("1. Lokál всегда идёт после предлога", H1),
    p("В этой теме работают четыре опоры: <b>v/vo, na, pri, o + Lokál</b>. Первые три обычно описывают место, а o вводит тему речи или мысли.", BODY),
    styled_table([
        ["Вопрос", "Предлог", "Пример", "Перевод"],
        ["kde?", "v / vo", "Bývam v Bratislave.", "Я живу в Братиславе."],
        ["kde?", "na", "Som na pošte.", "Я на почте."],
        ["kde?", "pri", "Čakám pri škole.", "Я жду у школы."],
        ["o kom? o čom?", "o", "Hovoríme o práci.", "Мы говорим о работе."],
    ], [27 * mm, 25 * mm, 65 * mm, 53 * mm], font_size=6.85),
    p("Частые формы единственного числа", H2),
    styled_table([
        ["Род / модель", "Nominatív → Lokál", "С группой"],
        ["мужской", "byt → byte; park → parku", "v novom byte; v mestskom parku"],
        ["мужской, -el", "hotel → hoteli", "v dobrom hoteli"],
        ["женский, -a", "škola → škole; izba → izbe", "v novej škole; v malej izbe"],
        ["женский, мягкая", "ulica → ulici; práca → práci", "na hlavnej ulici; pri práci"],
        ["средний", "mesto → meste; auto → aute", "v malom meste; v novom aute"],
        ["средний, -ie/-um", "námestie → námestí; múzeum → múzeu", "na veľkom námestí; v múzeu"],
    ], [34 * mm, 65 * mm, 71 * mm], font_size=6.55),
    box("<b>Не угадывайте окончание только по переводу.</b> Учите частотную форму вместе с предлогом: v byte, v parku, v hoteli, na ulici, na námestí.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    PageBreak(),

    p("2. Полное согласование и множественное число", H1),
    p("Вся именная группа меняет форму. В единственном числе прилагательное получает <b>-om</b> в мужском и среднем роде, <b>-ej</b> в женском. Во множественном числе у прилагательного обычно <b>-ých</b>.", BODY),
    styled_table([
        ["Тип", "Шаблон", "Пример"],
        ["мужской, ед.", "v tom novom byte", "Bývame v tom novom byte."],
        ["женский, ед.", "na tej hlavnej ulici", "Stretneme sa na tej hlavnej ulici."],
        ["средний, ед.", "v tomto malom meste", "Pracujem v tomto malom meste."],
        ["множественное", "v tých moderných bytoch", "V tých moderných bytoch je ticho."],
        ["множественное", "na nových pracoviskách", "Hovoríme o nových pracoviskách."],
    ], [38 * mm, 62 * mm, 70 * mm], font_size=6.9),
    p("V или vo?", H2),
    p("<b>Vo</b> - произносительный вариант v. Он особенно удобен перед похожим звуком или трудной группой согласных: <b>vo vode, vo vlaku, vo veľkom meste, vo Francúzsku</b>. Смысл и падеж не меняются.", BODY),
    p("V или na? Учим сочетание целиком", H2),
    styled_table([
        ["Часто v", "Часто na"],
        ["v škole, v banke, v nemocnici", "na pošte, na stanici, na univerzite"],
        ["v meste, v budove, v kancelárii", "na Slovensku, na internete, na stretnutí"],
    ], [85 * mm, 85 * mm], font_size=7.0),
    box("<b>Ловушка для русскоязычного ученика:</b> словацкий предлог нельзя всегда копировать из русского. Говорим <b>v škole</b>, но <b>na univerzite</b> и <b>na pošte</b>.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    PageBreak(),

    p("3. Предлог o: тема разговора", H1),
    p("Если речь, мысль, вопрос или текст посвящены человеку или предмету, используйте <b>o + Lokál</b>: hovoriť o, rozprávať sa o, premýšľať o, čítať o, písať o.", BODY),
    styled_table([
        ["Местоимение", "После o", "Пример"],
        ["ja", "o mne", "Hovorili o mne."],
        ["ty", "o tebe", "Často premýšľam o tebe."],
        ["on / ono", "o ňom", "Čítal som o ňom."],
        ["ona", "o nej", "Rozprávame sa o nej."],
        ["my", "o nás", "Napísali článok o nás."],
        ["vy", "o vás", "Čo povedal o vás?"],
        ["oni / ony", "o nich", "Neviem veľa o nich."],
    ], [34 * mm, 38 * mm, 98 * mm], font_size=6.95),
    box("<b>У 3-го лица после предлога появляется ň/n:</b> o ňom, o nej, o nich. Дополнительная полезная форма: <b>o sebe</b> - о себе.", PALE, ROSE, SMALL),
    p("Тема тоже требует согласования", H2),
    styled_table([
        ["Nominatív", "o + Lokál", "Фраза"],
        ["nový projekt", "o novom projekte", "Hovoríme o novom projekte."],
        ["dobrá kolegyňa", "o dobrej kolegyni", "Píšem o dobrej kolegyni."],
        ["malé mesto", "o malom meste", "Čítame o malom meste."],
        ["nové pravidlá", "o nových pravidlách", "Diskutujeme o nových pravidlách."],
    ], [42 * mm, 55 * mm, 73 * mm], font_size=6.9),
    PageBreak(),

    p("4. Lokál в живой речи", H1),
    p("Мини-диалог", H2),
    box("<b>A:</b> Kde teraz bývaš?<br/><b>B:</b> Bývam v malom meste pri Žiline, v novom byte.<br/><b>A:</b> Pracuješ v tom meste?<br/><b>B:</b> Nie, pracujem na univerzite. Teraz som v knižnici.<br/><b>A:</b> O čom dnes hovoríte na stretnutí?<br/><b>B:</b> O novom projekte a o kolegyni z Bratislavy.<br/><b>A:</b> A hovorili ste aj o mne?<br/><b>B:</b> Áno, hovorili sme o tebe veľmi dobre.", ALT, ROSE, SMALL),
    p("Перевод: Где ты сейчас живёшь? - В небольшом городе рядом с Жилиной, в новой квартире. - Ты работаешь в этом городе? - Нет, в университете. Сейчас я в библиотеке. - О чём вы сегодня говорите на встрече? - О новом проекте и коллеге из Братиславы. - И обо мне говорили? - Да, мы говорили о тебе очень хорошо.", TINY),
    p("Банк полезных моделей", H2),
    styled_table([
        ["Словацкая модель", "Естественный перевод"],
        ["Som v kancelárii pri okne.", "Я в кабинете у окна."],
        ["Čakáme na hlavnej stanici.", "Мы ждём на главном вокзале."],
        ["Deti sú v mestskom parku.", "Дети в городском парке."],
        ["Kniha je na malom stole.", "Книга на маленьком столе."],
        ["Býva vo veľkom meste.", "Он живёт в большом городе."],
        ["Rozprávame sa o novej práci.", "Мы говорим о новой работе."],
        ["Premýšľam o našom pláne.", "Я думаю о нашем плане."],
        ["Čítam článok o moderných mestách.", "Я читаю статью о современных городах."],
    ], [86 * mm, 84 * mm], font_size=6.7),
    PageBreak(),

    p("5. Частые ошибки и упражнения", H1),
    box("<b>Алгоритм:</b> определите смысл - место или тема → выберите v/vo, na, pri или o → поставьте всю группу в Lokál → проверьте местоимение после o.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    p("Упражнение 1. Выберите предлог", H2),
    p("1) bývam ___ Bratislave; 2) čakám ___ pošte; 3) stojím ___ okne; 4) hovoríme ___ práci; 5) sedím ___ aute; 6) študujem ___ univerzite.", SMALL),
    p("Упражнение 2. Поставьте существительное в Lokál", H2),
    p("1) v (byt); 2) v (park); 3) v (hotel); 4) na (ulica); 5) na (námestie); 6) o (práca).", SMALL),
    p("Упражнение 3. Согласуйте всю группу", H2),
    p("1) v (nový byt); 2) na (hlavná stanica); 3) v (malé mesto); 4) o (dobrá kolegyňa); 5) o (nové pravidlá).", SMALL),
    p("Упражнение 4. Замените имя местоимением", H2),
    p("1) o Petrovi; 2) o Zuzane; 3) o mne a Eve; 4) o tebe a Martinovi; 5) o vás, pán Novák.", SMALL),
    p("Упражнение 5. Исправьте ошибки", H2),
    p("1) Som v nový byt. 2) Čakám v pošte. 3) Hovoríme o ona. 4) Bývam na Bratislave. 5) Čítam o moderné mestá.", SMALL),
    p("Упражнение 6. Место и тема", H2),
    p("Напишите 5-7 связанных предложений: где вы живёте, где учитесь или работаете, что находится рядом и о ком или о чём вы часто говорите. Используйте не меньше трёх предлогов из урока.", SMALL),
    PageBreak(),

    p("6. Ответы и проверка мастерства", H1),
    p("Ответы", H2),
    p("<b>1.</b> v Bratislave; na pošte; pri okne; o práci; v aute; na univerzite.", TINY),
    p("<b>2.</b> v byte; v parku; v hoteli; na ulici; na námestí; o práci.", TINY),
    p("<b>3.</b> v novom byte; na hlavnej stanici; v malom meste; o dobrej kolegyni; o nových pravidlách.", TINY),
    p("<b>4.</b> o ňom; o nej; o nás; o vás; o vás. В заданиях 3-5 возможны и другие формы, если меняется состав группы или обращение.", TINY),
    p("<b>5.</b> 1) Som v novom byte. 2) Čakám na pošte. 3) Hovoríme o nej. 4) Bývam v Bratislave. 5) Čítam o moderných mestách.", TINY),
    p("<b>6. Модель:</b> Bývam v malom meste a pracujem v modernej kancelárii. Kancelária je pri stanici. Obedujem v reštaurácii na hlavnej ulici. S kolegami často hovoríme o novom projekte. Doma rozprávam o nich a o našej práci.", TINY),
    p("Итог в четырёх пунктах", H2),
    styled_table([
        ["OK", "Я выбираю v/vo, na и pri для частых мест."],
        ["OK", "Я согласую всю группу: v novom byte, na hlavnej ulici."],
        ["OK", "Я ввожу тему с o + Lokál: o novom projekte."],
        ["OK", "Я употребляю o mne/tebe/ňom/nej/nás/vás/nich."],
    ], [12 * mm, 158 * mm], font_size=7.25, header=False),
    Spacer(1, 3 * mm),
    box("<b>Финальная проверка:</b> без подсказки скажите три фразы о месте и три фразы о теме разговора, включая одну форму множественного числа и одно личное местоимение.", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    p("Следующий шаг", H2),
    p("В теме 2.10 вы перейдёте к Inštrumentál: средство, совместность и характеристика. Направление движения и триада kde - kam - odkiaľ будут отдельно систематизированы в теме 2.11.", SMALL),
]

doc.build(story)
print(OUTPUT)
