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
OUTPUT = ROOT / "output" / "pdf" / "A2" / "Module_03" / "Slovak_A2_Tema_3_1_Prilagatelnye_soglasovanie_v_padezhah.pdf"
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
BODY = ParagraphStyle("Body", fontName="Arial", fontSize=8.9, leading=11.7, textColor=INK, spaceAfter=3.2 * mm)
SMALL = ParagraphStyle("Small", parent=BODY, fontSize=7.7, leading=9.6, spaceAfter=1.75 * mm)
TINY = ParagraphStyle("Tiny", parent=BODY, fontSize=6.95, leading=8.55, spaceAfter=1.05 * mm)
TITLE = ParagraphStyle("Title", fontName="Arial-Bold", fontSize=20, leading=24, textColor=colors.white, alignment=TA_LEFT, spaceAfter=5 * mm)
SUBTITLE = ParagraphStyle("Subtitle", fontName="Arial", fontSize=11.5, leading=15, textColor=colors.HexColor("#FFD8EB"), spaceAfter=5 * mm)
H1 = ParagraphStyle("H1", fontName="Arial-Bold", fontSize=15.5, leading=18.5, textColor=PLUM, spaceBefore=1 * mm, spaceAfter=3.2 * mm)
H2 = ParagraphStyle("H2", fontName="Arial-Bold", fontSize=10.8, leading=13.4, textColor=PINK, spaceBefore=1.5 * mm, spaceAfter=1.6 * mm)
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


def styled_table(data, widths, font_size=7.25, header=True):
    converted = []
    for row_index, row in enumerate(data):
        style = ParagraphStyle(
            f"Cell{row_index}_{font_size}_{len(data)}", parent=SMALL, fontSize=font_size, leading=font_size + 1.9,
            textColor=colors.white if header and row_index == 0 else INK,
            fontName="Arial-Bold" if header and row_index == 0 else "Arial", spaceAfter=0,
        )
        converted.append([p(str(cell), style) for cell in row])
    table = Table(converted, colWidths=widths, repeatRows=1 if header else 0)
    commands = [
        ("GRID", (0, 0), (-1, -1), 0.45, ROSE), ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4.2), ("RIGHTPADDING", (0, 0), (-1, -1), 4.2),
        ("TOPPADDING", (0, 0), (-1, -1), 3.2), ("BOTTOMPADDING", (0, 0), (-1, -1), 3.2),
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
        canvas.drawString(20 * mm, height - 12 * mm, "A2 3.1  |  Прилагательные: согласование в падежах")
    canvas.setFont("Arial", 8)
    canvas.setFillColor(MUTED)
    canvas.drawString(20 * mm, 9 * mm, "SlovoKrok | личный учебный модуль")
    canvas.drawRightString(width - 20 * mm, 9 * mm, f"стр. {page} / 7")
    canvas.restoreState()


doc = BaseDocTemplate(
    str(OUTPUT), pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=20 * mm, bottomMargin=18 * mm,
    title="Slovak A2 - Тема 3.1 - Прилагательные: согласование во всех изученных падежах", author="SlovoKrok",
)
frame = Frame(20 * mm, 18 * mm, 170 * mm, 257 * mm, id="main", leftPadding=0, rightPadding=0)
doc.addPageTemplates([PageTemplate(id="series", frames=[frame], onPage=draw_page)])

story = [
    p("МОДУЛЬ 3  •  ПРИЛАГАТЕЛЬНЫЕ, МЕСТОИМЕНИЯ И ЧИСЛИТЕЛЬНЫЕ", COVER_KICKER),
    p("Прилагательные:<br/>согласование во всех изученных падежах", TITLE),
    p("Prídavné mená: zhoda vo všetkých prebraných pádoch", SUBTITLE),
    Spacer(1, 32 * mm),
    p("На A2 важно менять не одно существительное, а всю именную группу: род, падеж и одушевлённость вместе управляют формой прилагательного.", BODY),
    p("После модуля вы сможете:", H2),
    styled_table([
        ["1", "согласовывать твёрдое прилагательное с существительным в N/G/D/A/L/I"],
        ["2", "контролировать мужской, женский и средний род в единственном числе"],
        ["3", "различать A мужского рода: одушевлённое = G, неодушевлённое = N"],
        ["4", "использовать частотную мягкую модель cudzí и проверять всю группу"],
    ], [12 * mm, 158 * mm], font_size=7.35, header=False),
    Spacer(1, 3 * mm),
    box("<b>Главная формула:</b> существительное задаёт род и падеж -> прилагательное получает согласующееся окончание.", PALE, PINK),
    PageBreak(),

    p("1. Твёрдая модель pekný", H1),
    p("Сначала определите род существительного, затем падеж всей группы. Таблица ниже относится к <b>единственному числу</b>; множественное число будет отдельной темой 3.2.", BODY),
    styled_table([
        ["Падеж", "Мужской род", "Женский род", "Средний род"],
        ["N", "pekný sused", "pekná ulica", "pekné mesto"],
        ["G", "pekného suseda", "peknej ulice", "pekného mesta"],
        ["D", "peknému susedovi", "peknej ulici", "peknému mestu"],
        ["A", "pekného suseda / pekný dom", "peknú ulicu", "pekné mesto"],
        ["L", "o peknom susedovi", "na peknej ulici", "v peknom meste"],
        ["I", "s pekným susedom", "peknou ulicou", "pekným mestom"],
    ], [19 * mm, 50 * mm, 50 * mm, 51 * mm], font_size=6.35),
    p("Карта окончаний", H2),
    styled_table([
        ["Род", "N", "G", "D", "A", "L", "I"],
        ["m", "-ý", "-ého", "-ému", "-ého / -ý", "-om", "-ým"],
        ["f", "-á", "-ej", "-ej", "-ú", "-ej", "-ou"],
        ["n", "-é", "-ého", "-ému", "-é", "-om", "-ým"],
    ], [20 * mm, 22 * mm, 26 * mm, 26 * mm, 30 * mm, 22 * mm, 24 * mm], font_size=6.8),
    box("<b>Русскоязычная ловушка:</b> окончание нельзя выбирать по русскому слову. Проверяйте словацкое существительное: <b>nová adresa</b> (f), <b>nový problém</b> (m), <b>moderné múzeum</b> (n).", CREAM, colors.HexColor("#E7C76C"), SMALL),
    PageBreak(),

    p("2. Где решают род и одушевлённость", H1),
    p("В G, D, L и I мужской и средний род имеют одинаковые окончания прилагательного. Женский род легко узнать по цепочке <b>-ej, -ej, -ej</b> и отдельным формам A <b>-ú</b>, I <b>-ou</b>.", BODY),
    styled_table([
        ["Сигнал", "Модель", "Пример и перевод"],
        ["G m/n", "bez + -ého", "bez nového telefónu - без нового телефона"],
        ["G/D/L f", "-ej", "k novej kolegyni - к новой коллеге"],
        ["D m/n", "-ému", "k malému dieťaťu - к маленькому ребёнку"],
        ["A f", "-ú", "hľadám lacnú izbu - ищу недорогую комнату"],
        ["L m/n", "-om", "v modernom múzeu - в современном музее"],
        ["I f", "-ou", "s dobrou lekárkou - с хорошим врачом"],
        ["I m/n", "-ým", "s dôležitým dokumentom - с важным документом"],
    ], [29 * mm, 35 * mm, 106 * mm], font_size=6.55),
    p("Akuzatív мужского рода", H2),
    styled_table([
        ["Тип", "Правило", "Пример"],
        ["одушевлённый", "A = G", "Čakám na nového lekára. - Я жду нового врача."],
        ["неодушевлённый", "A = N", "Hľadám nový hotel. - Я ищу новый отель."],
    ], [34 * mm, 32 * mm, 104 * mm], font_size=6.85),
    p("Изменяется вся группа", H2),
    box("N <b>nová pracovná ponuka</b> -> G <b>bez novej pracovnej ponuky</b> -> D <b>k novej pracovnej ponuke</b> -> A <b>na novú pracovnú ponuku</b> -> L <b>o novej pracovnej ponuke</b> -> I <b>s novou pracovnou ponukou</b>.", PALE, ROSE, SMALL),
    box("<b>Орфографическая деталь:</b> после долгого слога окончания модели иногда сокращаются: <b>krásny, krásneho, krásnemu, krásnom, krásnym</b>. Это та же твёрдая модель, а не новый падежный набор.", CREAM, colors.HexColor("#E7C76C"), TINY),
    PageBreak(),

    p("3. Мягкая модель cudzí", H1),
    p("Частотные прилагательные на <b>-í</b>, например <b>cudzí, ďalší, domáci, horúci</b>, используют мягкий набор. Принцип согласования не меняется: форму по-прежнему задаёт существительное.", BODY),
    styled_table([
        ["Падеж", "Мужской род", "Женский род", "Средний род"],
        ["N", "cudzí človek", "cudzia reč", "cudzie mesto"],
        ["G", "cudzieho človeka", "cudzej reči", "cudzieho mesta"],
        ["D", "cudziemu človeku", "cudzej reči", "cudziemu mestu"],
        ["A", "cudzieho človeka / cudzí jazyk", "cudziu reč", "cudzie mesto"],
        ["L", "o cudzom človeku", "v cudzej reči", "v cudzom meste"],
        ["I", "s cudzím človekom", "cudzou rečou", "cudzím mestom"],
    ], [19 * mm, 50 * mm, 50 * mm, 51 * mm], font_size=6.3),
    p("Твёрдое и мягкое рядом", H2),
    styled_table([
        ["Падеж", "pekný", "cudzí"],
        ["N f / n", "pekná / pekné", "cudzia / cudzie"],
        ["G m/n / f", "pekného / peknej", "cudzieho / cudzej"],
        ["D m/n / f", "peknému / peknej", "cudziemu / cudzej"],
        ["A f", "peknú", "cudziu"],
        ["L m/n / f", "peknom / peknej", "cudzom / cudzej"],
        ["I m/n / f", "pekným / peknou", "cudzím / cudzou"],
    ], [33 * mm, 68 * mm, 69 * mm], font_size=6.55),
    box("<b>Не смешивайте наборы:</b> правильно <b>o novom kurze</b>, но <b>o ďalšom kurze</b>; правильно <b>s novou kolegyňou</b>, но <b>s ďalšou kolegyňou</b>.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    PageBreak(),

    p("4. Живые модели в контексте", H1),
    p("Читайте сочетание целиком: предлог или глагол выбирает падеж, существительное задаёт род, прилагательное показывает согласование.", BODY),
    styled_table([
        ["SK", "RU"],
        ["Nový sused je veľmi milý.", "Новый сосед очень добрый."],
        ["Bez nového telefónu nemôžem pracovať.", "Без нового телефона я не могу работать."],
        ["Zavolám novej kolegyni.", "Я позвоню новой коллеге."],
        ["Čakám na nového lekára.", "Я жду нового врача."],
        ["Hľadám lacný hotel.", "Я ищу недорогой отель."],
        ["Hovoríme o novej zmluve.", "Мы говорим о новом договоре."],
        ["Cestujem s malým dieťaťom.", "Я путешествую с маленьким ребёнком."],
        ["Bývame v tichom meste.", "Мы живём в тихом городе."],
        ["Rozumiem cudziemu človeku.", "Я понимаю иностранца."],
        ["Učím sa cudziu reč.", "Я учу иностранный язык."],
        ["Rozprávame sa o ďalšej možnosti.", "Мы говорим о следующей возможности."],
        ["Prídem s ďalším kolegom.", "Я приду с ещё одним коллегой."],
    ], [84 * mm, 86 * mm], font_size=6.05),
    p("Мини-диалог", H2),
    box("<b>A:</b> Hľadám <b>pokojnú izbu</b> v <b>tichom hoteli</b>. - Я ищу спокойную комнату в тихом отеле.<br/><b>B:</b> Máme izbu s <b>veľkým balkónom</b>. - У нас есть комната с большим балконом.<br/><b>A:</b> Je blízko <b>hlavnej stanice</b>? - Она рядом с главным вокзалом?<br/><b>B:</b> Áno, k <b>hlavnej stanici</b> pôjdete päť minút. - Да, до главного вокзала идти пять минут.<br/><b>A:</b> Prosím si tú <b>pokojnú izbu</b>. - Я возьму эту спокойную комнату.", PALE, ROSE, TINY),
    p("Быстрая проверка группы", H2),
    p("1) Какой падеж требует центр? 2) Какого рода словацкое существительное? 3) Для A m оно одушевлённое? 4) Твёрдая или мягкая модель? 5) Все слова группы изменены вместе?", SMALL),
    PageBreak(),

    p("5. Частые ошибки и упражнения", H1),
    box("<b>Частые ошибки:</b> *o nový projekte -> <b>o novom projekte</b>; *s dobrým lekárkou -> <b>s dobrou lekárkou</b>; *čakám na nový kolegu -> <b>na nového kolegu</b>; *v cudziem meste -> <b>v cudzom meste</b>.", CREAM, colors.HexColor("#E7C76C"), TINY),
    p("Упражнение 1. Выберите окончание", H2),
    p("1) bez nov(ý/ého) pasu; 2) k dobr(ej/ú) lekárke; 3) v tich(om/ým) meste; 4) s mal(ému/ým) dieťaťom; 5) hľadám lacn(ý/ého) hotel.", TINY),
    p("Упражнение 2. Поставьте pekný в нужную форму", H2),
    p("1) o ___ ulici; 2) s ___ susedom; 3) bez ___ mesta; 4) k ___ dieťaťu; 5) vidím ___ kolegyňu.", TINY),
    p("Упражнение 3. Поставьте cudzí или ďalší", H2),
    p("1) bez (cudzí) pasu; 2) rozumiem (cudzí) osobe; 3) hovoríme o (ďalší) stretnutí; 4) prídem s (ďalší) kolegyňou; 5) poznám (cudzí) študenta.", TINY),
    p("Упражнение 4. Исправьте ошибки", H2),
    p("1) Bývam v nový byte. 2) Čakám na milý suseda. 3) Idem k dobrej lekárovi. 4) Hovorím s cudziou človekom. 5) Bez modernému telefónu nepracujem.", TINY),
    p("Упражнение 5. Переведите", H2),
    p("1) без важного документа; 2) к новой коллеге; 3) о тихом городе; 4) с иностранным студентом; 5) я ищу недорогую комнату.", TINY),
    p("Упражнение 6. Свой мини-текст", H2),
    p("Напишите 5-7 связанных предложений о гостинице, курсе или новом знакомом. Используйте единственное число, минимум четыре падежа, один мужской одушевлённый A и одну форму cudzí или ďalší.", TINY),
    PageBreak(),

    p("6. Ответы и проверка мастерства", H1),
    p("Ответы", H2),
    p("<b>1.</b> bez nového pasu; k dobrej lekárke; v tichom meste; s malým dieťaťom; hľadám lacný hotel.", TINY),
    p("<b>2.</b> o peknej ulici; s pekným susedom; bez pekného mesta; k peknému dieťaťu; vidím peknú kolegyňu.", TINY),
    p("<b>3.</b> bez cudzieho pasu; rozumiem cudzej osobe; hovoríme o ďalšom stretnutí; prídem s ďalšou kolegyňou; poznám cudzieho študenta.", TINY),
    p("<b>4.</b> Bývam v novom byte. Čakám na milého suseda. Idem k dobrému lekárovi. Hovorím s cudzím človekom. Bez moderného telefónu nepracujem.", TINY),
    p("<b>5.</b> bez dôležitého dokumentu; k novej kolegyni; o tichom meste; s cudzím študentom; hľadám lacnú izbu.", TINY),
    p("<b>6. Модель:</b> Bývam v tichom hoteli. Hotel je blízko hlavnej stanice. Každé ráno sa rozprávam s milým recepčným. Včera som čakal na nového hosťa. Potom som pomohol cudziemu turistovi. Večer sme hovorili o ďalšom výlete. Возможны другие естественные варианты.", TINY),
    p("Итог в четырёх пунктах", H2),
    styled_table([
        ["OK", "Я сначала нахожу падеж и род существительного."],
        ["OK", "Я меняю прилагательное и существительное как одну группу."],
        ["OK", "В A мужского рода я различаю человека и предмет."],
        ["OK", "Я не смешиваю окончания моделей pekný и cudzí."],
    ], [12 * mm, 158 * mm], font_size=7.0, header=False),
    Spacer(1, 2.2 * mm),
    box("<b>Финальная проверка:</b> без таблицы измените <b>nový kolega</b>, <b>nová práca</b>, <b>nové mesto</b> и <b>cudzí človek</b> в двух падежах по своему выбору и объясните каждое окончание.", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    p("Следующий шаг", H2),
    p("В теме 3.2 вы перенесёте согласование на множественное число и отдельно отработаете одушевлённость.", SMALL),
]

doc.build(story)
print(OUTPUT)
