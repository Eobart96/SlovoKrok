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
OUTPUT = ROOT / "output" / "pdf" / "A2" / "Module_02" / "Slovak_A2_Tema_2_12_Padezhi_v_odnoy_sisteme_upravlenie_i_obrashchenie.pdf"
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
BODY = ParagraphStyle("Body", fontName="Arial", fontSize=8.9, leading=11.7, textColor=INK, spaceAfter=3.4 * mm)
SMALL = ParagraphStyle("Small", parent=BODY, fontSize=7.7, leading=9.6, spaceAfter=1.8 * mm)
TINY = ParagraphStyle("Tiny", parent=BODY, fontSize=7.05, leading=8.7, spaceAfter=1.15 * mm)
TITLE = ParagraphStyle("Title", fontName="Arial-Bold", fontSize=20, leading=24, textColor=colors.white, alignment=TA_LEFT, spaceAfter=5 * mm)
SUBTITLE = ParagraphStyle("Subtitle", fontName="Arial", fontSize=11.5, leading=15, textColor=colors.HexColor("#FFD8EB"), spaceAfter=5 * mm)
H1 = ParagraphStyle("H1", fontName="Arial-Bold", fontSize=15.5, leading=18.5, textColor=PLUM, spaceBefore=1 * mm, spaceAfter=3.4 * mm)
H2 = ParagraphStyle("H2", fontName="Arial-Bold", fontSize=10.8, leading=13.4, textColor=PINK, spaceBefore=1.7 * mm, spaceAfter=1.8 * mm)
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
            f"Cell{row_index}_{font_size}", parent=SMALL, fontSize=font_size, leading=font_size + 1.9,
            textColor=colors.white if header and row_index == 0 else INK,
            fontName="Arial-Bold" if header and row_index == 0 else "Arial", spaceAfter=0,
        )
        converted.append([p(str(cell), style) for cell in row])
    table = Table(converted, colWidths=widths, repeatRows=1 if header else 0)
    commands = [
        ("GRID", (0, 0), (-1, -1), 0.45, ROSE), ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4.5), ("RIGHTPADDING", (0, 0), (-1, -1), 4.5),
        ("TOPPADDING", (0, 0), (-1, -1), 3.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 3.5),
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
        canvas.drawString(20 * mm, height - 12 * mm, "A2 2.12  |  Падежи в одной системе: управление и обращение")
    canvas.setFont("Arial", 8)
    canvas.setFillColor(MUTED)
    canvas.drawString(20 * mm, 9 * mm, "SlovoKrok | личный учебный модуль")
    canvas.drawRightString(width - 20 * mm, 9 * mm, f"стр. {page} / 7")
    canvas.restoreState()


doc = BaseDocTemplate(
    str(OUTPUT), pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=20 * mm, bottomMargin=18 * mm,
    title="Slovak A2 - Тема 2.12 - Падежи в одной системе: управление и обращение", author="SlovoKrok",
)
frame = Frame(20 * mm, 18 * mm, 170 * mm, 257 * mm, id="main", leftPadding=0, rightPadding=0)
doc.addPageTemplates([PageTemplate(id="series", frames=[frame], onPage=draw_page)])

story = [
    p("МОДУЛЬ 2  •  ПАДЕЖИ И УПРАВЛЕНИЕ A2", COVER_KICKER),
    p("Падежи в одной системе:<br/>управление и обращение", TITLE),
    p("Pády v jednom systéme: väzby a oslovenie", SUBTITLE),
    Spacer(1, 34 * mm),
    p("Словацкий падеж выбирается не по русскому переводу, а по управляющему слову: глаголу, предлогу или формуле обращения.", BODY),
    p("После модуля вы сможете:", H2),
    styled_table([
        ["1", "видеть центр конструкции и задавать словацкий падежный вопрос"],
        ["2", "использовать частотные глагольные модели с G, D, A, L и I"],
        ["3", "собирать предлог и падеж в одну готовую модель"],
        ["4", "естественно обращаться с pán/pani и ставить запятые"],
    ], [12 * mm, 158 * mm], font_size=7.55, header=False),
    Spacer(1, 3 * mm),
    box("<b>Главная формула:</b> Найдите управление -> задайте вопрос -> выберите падеж -> измените всю именную группу.", PALE, PINK),
    PageBreak(),

    p("1. Одна карта: кто управляет формой?", H1),
    p("Падеж задаёт центр конструкции. Это может быть глагол (<b>pomáhať komu?</b>), предлог (<b>bez koho? čoho?</b>) или устойчивая модель (<b>stretnúť sa s kým?</b>). Перевод помогает понять смысл, но не выбирает форму.", BODY),
    styled_table([
        ["Падеж", "Вопрос", "Частотный центр", "Пример"],
        ["N", "kto? čo?", "быть / называться", "Som lekár."],
        ["G", "koho? čoho?", "báť sa; bez, do, od, z", "Bojím sa skúšky."],
        ["D", "komu? čomu?", "pomáhať; veriť; k, vďaka", "Pomáham susedovi."],
        ["A", "koho? čo?", "čakať na; prosiť o; pre", "Čakám na autobus."],
        ["L", "o kom? o čom?", "hovoriť o; záležať na", "Hovoríme o projekte."],
        ["I", "s kým? čím?", "stretnúť sa s; byť rolou", "Stretnem sa s lekárom."],
    ], [19 * mm, 27 * mm, 56 * mm, 68 * mm], font_size=6.65),
    p("Алгоритм на четыре шага", H2),
    styled_table([
        ["1", "Найдите центр: tešiť sa."],
        ["2", "Вспомните модель: tešiť sa na + A."],
        ["3", "Задайте вопрос: na koho? na čo?"],
        ["4", "Измените всю группу: na nový kurz."],
    ], [12 * mm, 158 * mm], font_size=7.15, header=False),
    box("<b>Не путайте:</b> <b>čakať na kolegu</b> - ждать коллегу, но <b>pomáhať kolegovi</b> - помогать коллеге. Одинаковый русский вопрос не гарантирует одинаковый словацкий падеж.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    PageBreak(),

    p("2. Глаголы: учим модель целиком", H1),
    styled_table([
        ["Модель", "Пример", "Перевод"],
        ["báť sa + G", "Bojím sa veľkého psa.", "Я боюсь большой собаки."],
        ["zúčastniť sa + G", "Zúčastním sa kurzu.", "Я приму участие в курсе."],
        ["pomáhať + D", "Pomáham starej mame.", "Я помогаю бабушке."],
        ["veriť + D", "Verím svojmu lekárovi.", "Я доверяю своему врачу."],
        ["rozumieť + D", "Rozumiem tejto otázke.", "Я понимаю этот вопрос."],
        ["čakať na + A", "Čakáme na nový vlak.", "Мы ждём новый поезд."],
        ["prosiť o + A", "Prosím o pomoc.", "Я прошу о помощи."],
        ["tešiť sa na + A", "Teším sa na víkend.", "Я жду выходных с радостью."],
        ["hovoriť o + L", "Hovoríme o novej práci.", "Мы говорим о новой работе."],
        ["záležať na + L", "Záleží mi na výsledku.", "Мне важен результат."],
        ["stretnúť sa s + I", "Stretnem sa s kolegyňou.", "Я встречусь с коллегой."],
    ], [45 * mm, 65 * mm, 60 * mm], font_size=6.35),
    p("Похожие слова, разное управление", H2),
    styled_table([
        ["Без предлога", "С предлогом"],
        ["poznám kolegu (A)", "stretnem sa s kolegom (I)"],
        ["volám Petrovi (D)", "čakám na Petra (A)"],
        ["rozumiem otázke (D)", "hovorím o otázke (L)"],
        ["potrebujem pomoc (A)", "prosím o pomoc (A)"],
    ], [85 * mm, 85 * mm], font_size=6.9),
    box("<b>Словарная запись A2:</b> пишите не <i>čakať = ждать</i>, а <b>čakať na koho? na čo? + A</b>. Так управление сразу становится частью слова.", PALE, ROSE, SMALL),
    PageBreak(),

    p("3. Предлоги: значение плюс падеж", H1),
    p("Предлог храните вместе с вопросом и типичным примером. Пространственную триаду из 2.11 здесь используем как готовую опору: <b>v škole - do školy - zo školy</b>.", BODY),
    styled_table([
        ["Падеж", "Предлоги", "Готовые сочетания"],
        ["G", "bez, do, od, z/zo", "bez cukru; do mesta; od lekára; zo školy"],
        ["D", "k/ku, vďaka, kvôli", "k susedovi; ku kamarátke; vďaka pomoci; kvôli práci"],
        ["A", "pre, cez, na", "pre dcéru; cez park; na stretnutie"],
        ["L", "o, po, pri, v/vo, na", "o kurze; po práci; pri okne; v meste; na pošte"],
        ["I", "s/so, pred, za, medzi", "so sestrou; pred domom; za školou; medzi ľuďmi"],
    ], [24 * mm, 48 * mm, 98 * mm], font_size=6.55),
    p("Три важных контраста", H2),
    styled_table([
        ["Контраст", "Примеры"],
        ["k + D / do + G", "Idem k lekárovi. / Idem do nemocnice."],
        ["na + A / na + L", "Idem na poštu. / Som na pošte."],
        ["s + I / bez + G", "Káva s mliekom. / Káva bez mlieka."],
    ], [48 * mm, 122 * mm], font_size=7.0),
    p("Изменяется вся группа", H2),
    p("<b>bez môjho nového kolegu</b> (G), <b>k mojej novej kolegyni</b> (D), <b>na môj nový kurz</b> (A), <b>o mojom novom kurze</b> (L), <b>s mojím novým kolegom</b> (I).", SMALL),
    box("<b>Полезная проверка:</b> если в группе есть местоимение или прилагательное, оно должно согласоваться с существительным в том же падеже.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    PageBreak(),

    p("4. Обращение: форма, регистр и запятые", H1),
    p("В современном словацком обращение обычно стоит в Nominatív. Для знакомого адресата в официальной ситуации употребляют <b>pán/pani + фамилия или должность</b>.", BODY),
    styled_table([
        ["Ситуация", "Естественная модель"],
        ["к знакомому мужчине", "Pán Novák, môžete mi pomôcť?"],
        ["к знакомой женщине", "Pani Kováčová, máte chvíľu?"],
        ["по должности", "Pani doktorka, prosím o radu."],
        ["внутри предложения", "Môžete mi, pán riaditeľ, zavolať?"],
        ["в конце", "Ďakujem, pani profesorka."],
        ["письмо", "Vážený pán Novák, / Vážená pani Kováčová,"],
    ], [52 * mm, 118 * mm], font_size=6.75),
    p("Запятая обязательна", H2),
    box("В начале: <b>Pani Horváthová,</b> pošlem vám správu.<br/>Внутри: Mohli by ste mi, <b>pán doktor,</b> poradiť?<br/>В конце: Dovidenia, <b>pani učiteľka.</b>", PALE, ROSE, SMALL),
    p("Остаточные формы Vokatív", H2),
    p("В словацком обычно считают шесть падежей, но несколько старых форм обращения живы. Они не образуют продуктивную таблицу: учите их как отдельные слова.", SMALL),
    styled_table([
        ["Форма", "Пример", "Регистр"],
        ["synu", "Synu, poď sem.", "семейный, возвышенный"],
        ["otče", "Otče, vypočujte ma.", "религиозный или торжественный"],
        ["Bože", "Bože, pomôž mi.", "религиозный, эмоциональный"],
        ["pane", "Prepáčte, pane.", "отдельно к незнакомому мужчине; может звучать маркированно"],
    ], [25 * mm, 55 * mm, 90 * mm], font_size=6.55),
    box("<b>Не копируйте чешскую модель:</b> по-словацки <b>pán doktor, pán Novák</b>, а не *pane doktore, *pane Nováku. Самостоятельное <b>pane</b> возможно, но в нейтральной ситуации часто проще сказать <b>Prepáčte, prosím</b>.", CREAM, colors.HexColor("#E7C76C"), TINY),
    PageBreak(),

    p("5. Частые ошибки и упражнения", H1),
    box("<b>Самопроверка:</b> центр -> модель -> вопрос -> форма всей группы. В обращении отдельно проверьте регистр и запятые.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    p("Упражнение 1. Выберите падежную модель", H2),
    p("1) pomáham (nový sused); 2) čakám na (kolega); 3) bojím sa (skúška); 4) hovoríme o (projekt); 5) stretnem sa s (lekár).", SMALL),
    p("Упражнение 2. Добавьте предлог", H2),
    p("1) káva ___ mlieka; 2) idem ___ kamarátke; 3) prosím ___ informáciu; 4) teším sa ___ dovolenku; 5) záleží mi ___ výsledku.", SMALL),
    p("Упражнение 3. Измените всю группу", H2),
    p("1) bez (môj nový kolega); 2) k (moja dobrá lekárka); 3) o (ten dôležitý kurz); 4) s (naša nová učiteľka).", SMALL),
    p("Упражнение 4. Расставьте запятые", H2),
    p("1) Pán Novák môžete mi pomôcť? 2) Ďakujem pani doktorka. 3) Mohli by ste mi pani riaditeľka zavolať? 4) Synu poď sem.", SMALL),
    p("Упражнение 5. Исправьте ошибки", H2),
    p("1) Pomáham môjho suseda. 2) Čakám kolegovi. 3) Hovoríme o nový projekt. 4) Pane doktore, prosím o radu. 5) Stretnem sa s moja kolegyňa.", SMALL),
    p("Упражнение 6. Вежливая просьба", H2),
    p("Напишите 5-7 связанных предложений коллеге или специалисту: обращение, просьба, причина, одна модель с D, одна с A или L и благодарность. Все обращения отделите запятыми.", SMALL),
    PageBreak(),

    p("6. Ответы и проверка мастерства", H1),
    p("Ответы", H2),
    p("<b>1.</b> pomáham novému susedovi; čakám na kolegu; bojím sa skúšky; hovoríme o projekte; stretnem sa s lekárom.", TINY),
    p("<b>2.</b> bez mlieka; ku kamarátke; o informáciu; na dovolenku; na výsledku.", TINY),
    p("<b>3.</b> bez môjho nového kolegu; k mojej dobrej lekárke; o tom dôležitom kurze; s našou novou učiteľkou.", TINY),
    p("<b>4.</b> Pán Novák, môžete mi pomôcť? Ďakujem, pani doktorka. Mohli by ste mi, pani riaditeľka, zavolať? Synu, poď sem.", TINY),
    p("<b>5.</b> Pomáham môjmu susedovi. Čakám na kolegu. Hovoríme o novom projekte. Pán doktor, prosím o radu. Stretnem sa s mojou kolegyňou.", TINY),
    p("<b>6. Модель:</b> Vážená pani Kováčová, prosím vás o krátku konzultáciu. Nerozumiem jednej otázke a záleží mi na správnom výsledku. Mohli by ste mi, prosím, pomôcť? Teším sa na naše stretnutie. Ďakujem vám za čas.", TINY),
    p("Итог в четырёх пунктах", H2),
    styled_table([
        ["OK", "Я учу глагол вместе с вопросом, предлогом и падежом."],
        ["OK", "Я изменяю существительное, прилагательное и местоимение как одну группу."],
        ["OK", "Я обращаюсь: pán/pani + фамилия или должность."],
        ["OK", "Я отделяю обращение запятыми и узнаю формы synu, otče, Bože."],
    ], [12 * mm, 158 * mm], font_size=7.05, header=False),
    Spacer(1, 2.5 * mm),
    box("<b>Финальная проверка:</b> без подсказки назовите по одной глагольной модели с G, D, A, L и I, затем произнесите вежливую просьбу с обращением и правильной запятой.", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    p("Следующий шаг", H2),
    p("В теме 3.1 вы систематизируете согласование прилагательных во всех уже изученных падежах.", SMALL),
]

doc.build(story)
print(OUTPUT)
