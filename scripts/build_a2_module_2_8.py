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
OUTPUT = ROOT / "output" / "pdf" / "A2" / "Module_02" / "Slovak_A2_Tema_2_8_Dativ_adresat_polza_i_prichina.pdf"
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
        canvas.drawString(20 * mm, height - 12 * mm, "SLOVAK A2  |  ТЕМА 2.8")
        canvas.drawRightString(width - 20 * mm, height - 12 * mm, "Datív: адресат, польза и причина")
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
    title="Slovak A2 - Тема 2.8 - Datív: адресат, польза и причина", author="SlovoKrok",
)
frame = Frame(20 * mm, 18 * mm, 170 * mm, 257 * mm, id="main", leftPadding=0, rightPadding=0)
doc.addPageTemplates([PageTemplate(id="series", frames=[frame], onPage=draw_page)])

story = [
    p("МОДУЛЬ 2  •  ПАДЕЖИ И УПРАВЛЕНИЕ A2", COVER_KICKER),
    p("Datív:<br/>адресат, польза и причина", TITLE),
    p("Datív: adresát, prospech a príčina", SUBTITLE),
    Spacer(1, 33 * mm),
    p("Datív отвечает на вопрос komu? čomu? и показывает получателя действия, направление к человеку или точке, а также того, кому что-то помогает, мешает или приносит пользу.", BODY),
    p("После модуля вы сможете:", H2),
    styled_table([
        ["1", "говорить, кому дают, пишут, звонят, показывают или помогают"],
        ["2", "строить модель Akuzatív + Datív: даю что кому"],
        ["3", "употреблять mi/mne, ti/tebe, mu/nemu, jej/nej, nám, vám, im/nim"],
        ["4", "выбирать k/ku, vďaka, kvôli, oproti и proti"],
    ], [12 * mm, 158 * mm], font_size=7.85, header=False),
    Spacer(1, 3 * mm),
    box("<b>Главная формула:</b> dávam <b>knihu</b> (čo? A) <b>kolegovi</b> (komu? D).", PALE, PINK),
    PageBreak(),

    p("1. Формы существительных и прилагательных", H1),
    p("Datív singular зависит от рода и модели слова. У мужских названий людей часто встречается -ovi, у женского рода -e / -i, у среднего -u.", BODY),
    styled_table([
        ["Род / модель", "Nominatív → Datív", "Пример"],
        ["муж., человек", "kolega → kolegovi; učiteľ → učiteľovi", "píšem kolegovi"],
        ["муж., предмет", "dom → domu; hotel → hotelu", "idem k hotelu"],
        ["жен., -e", "žena → žene; sestra → sestre", "pomáham sestre"],
        ["жен., -i", "ulica → ulici; práca → práci", "kvôli práci"],
        ["жен., согласная", "dlaň → dlani; kosť → kosti", "proti bolesti"],
        ["сред., -u", "mesto → mestu; auto → autu", "oproti mestu"],
        ["сред., особая", "dieťa → dieťaťu", "dávam dieťaťu vodu"],
    ], [35 * mm, 75 * mm, 60 * mm], font_size=6.75),
    p("Полное согласование", H2),
    styled_table([
        ["Мужской / средний", "Женский", "Множественное число"],
        ["tomu novému kolegovi", "tej dobrej priateľke", "tým novým kolegom"],
        ["môjmu malému dieťaťu", "našej starej mame", "našim dobrým priateľom"],
    ], [57 * mm, 57 * mm, 56 * mm], font_size=7.0),
    box("<b>Опора:</b> tomu / môjmu / novému для мужского и среднего рода; tej / mojej / novej для женского; tým / mojim / novým во множественном числе.", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    PageBreak(),

    p("2. Личные местоимения: короткие и полные", H1),
    styled_table([
        ["Лицо", "Без предлога", "После предлога", "Пример"],
        ["ja", "mi / mne", "ku mne", "Daj mi vedieť."],
        ["ty", "ti / tebe", "kvôli tebe", "Napíšem ti."],
        ["on / ono", "mu / jemu", "k nemu", "Pomôžem mu."],
        ["ona", "jej", "k nej", "Zavolám jej."],
        ["my", "nám", "vďaka nám", "Ukážte nám cestu."],
        ["vy", "vám", "oproti vám", "Pošlem vám správu."],
        ["oni / ony", "im", "proti nim", "Dám im adresu."],
    ], [24 * mm, 40 * mm, 45 * mm, 61 * mm], font_size=6.85),
    p("Короткая форма занимает вторую позицию", H2),
    box("<b>Dnes ti zavolám.</b> - Сегодня я тебе позвоню.<br/><b>Včera som mu poslal správu.</b> - Вчера я отправил ему сообщение.<br/><b>Jemu zavolám, nie Petrovi.</b> - Я позвоню именно ему, а не Петеру.", PALE, ROSE, SMALL),
    box("<b>После предлога у 3-го лица появляется n:</b> k nemu, k nej, vďaka nim. Без предлога: mu, jej, im.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    PageBreak(),

    p("3. Модель Akuzatív + Datív", H1),
    p("Некоторые глаголы связывают предмет и адресата: что? ставим в Akuzatív, кому? - в Datív.", BODY),
    styled_table([
        ["Глагол", "Модель", "Пример"],
        ["dať / dávať", "dať čo komu", "Dám knihu kolegovi."],
        ["poslať", "poslať čo komu", "Pošlem správu mame."],
        ["ukázať", "ukázať čo komu", "Ukážem projekt klientovi."],
        ["priniesť", "priniesť čo komu", "Prinesiem čaj hosťovi."],
        ["kúpiť", "kúpiť čo komu", "Kúpime darček sestre."],
        ["požičať", "požičať čo komu", "Požičiam auto priateľovi."],
    ], [37 * mm, 53 * mm, 80 * mm], font_size=7.0),
    p("Если появляются два местоимения", H2),
    styled_table([
        ["Состав", "Порядок", "Пример"],
        ["D-местоимение + A-слово", "местоимение раньше", "Pošlem mu správu."],
        ["A-местоимение + D-слово", "местоимение раньше", "Pošlem ju Petrovi."],
        ["D-местоимение + A-местоимение", "Datív перед Akuzatív", "Pošlem mu ju večer."],
    ], [50 * mm, 48 * mm, 72 * mm], font_size=7.0),
    box("<b>Без прямого объекта:</b> pomáhať, telefonovať / zavolať, veriť, ďakovať + Datív: <b>Pomáham susedovi. Verím ti. Ďakujem vám.</b>", ALT, ROSE, SMALL),
    PageBreak(),

    p("4. Предлоги с Datív", H1),
    styled_table([
        ["Предлог", "Смысл", "Пример", "Перевод"],
        ["k / ku", "к человеку или точке", "Idem k lekárovi / ku kamarátovi.", "Иду к врачу / другу."],
        ["vďaka", "благоприятная причина", "Vďaka tvojej rade som uspel.", "Благодаря твоему совету я справился."],
        ["kvôli", "мотив или практическая причина", "Meškáme kvôli zápche.", "Опаздываем из-за пробки."],
        ["oproti", "напротив; по сравнению", "Bývam oproti škole.", "Живу напротив школы."],
        ["proti", "против; средство защиты", "Som proti návrhu.", "Я против предложения."],
    ], [24 * mm, 45 * mm, 65 * mm, 36 * mm], font_size=6.65),
    p("Vďaka или kvôli?", H2),
    box("<b>Vďaka tebe sme prišli včas.</b> - Благодаря тебе мы пришли вовремя.<br/><b>Kvôli zápche sme prišli neskoro.</b> - Из-за пробки мы пришли поздно.<br/><b>Robím to kvôli deťom.</b> - Я делаю это ради детей.", PALE, ROSE, SMALL),
    p("Мини-диалог", H2),
    box("<b>A:</b> Kam ideš?<br/><b>B:</b> K lekárovi. Zavolám mu a ukážem mu výsledky.<br/><b>A:</b> Ideš tam kvôli bolesti?<br/><b>B:</b> Áno. Vďaka tvojej rade som si termín rezervoval včas.<br/><b>A:</b> Držím ti palce!", ALT, ROSE, SMALL),
    p("Перевод: Куда идёшь? - К врачу. Позвоню ему и покажу результаты. - Ты идёшь из-за боли? - Да. Благодаря твоему совету я вовремя записался. - Держу за тебя кулаки!", SMALL),
    PageBreak(),

    p("5. Частые ошибки и упражнения", H1),
    box("<b>Алгоритм:</b> найдите адресата или предлог → задайте komu? čomu? → выберите форму Datív → проверьте порядок короткого местоимения.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    p("Упражнение 1. Поставьте существительное в Datív", H2),
    p("1) píšem (kolega); 2) pomáham (sestra); 3) idem k (lekár); 4) dávam vodu (dieťa); 5) oproti (škola); 6) proti (bolesť).", SMALL),
    p("Упражнение 2. Выберите местоимение", H2),
    p("1) Daj ___ vedieť (ja). 2) Zavolám ___ (ty). 3) Pošleme ___ správu (on). 4) Ukážem ___ cestu (ona). 5) Ďakujem ___ (vy). 6) Pomôžeme ___ (oni).", SMALL),
    p("Упражнение 3. После предлога", H2),
    p("1) k ___ (on); 2) kvôli ___ (ty); 3) vďaka ___ (oni); 4) oproti ___ (vy); 5) ku ___ (ja); 6) k ___ (ona).", SMALL),
    p("Упражнение 4. Соберите A + D", H2),
    p("1) dať / kniha / kolega; 2) poslať / správa / mama; 3) ukázať / projekt / klient; 4) kúpiť / darček / sestra; 5) požičať / auto / priateľ.", SMALL),
    p("Упражнение 5. Исправьте ошибки", H2),
    p("1) Dám kolega knihu. 2) Zavolám k on. 3) Vďaka tvoja rada som uspel. 4) Pošlem ju mu večer. 5) Pomáham môj nový sused.", SMALL),
    p("Упражнение 6. Помогите другу", H2),
    p("Напишите 5-7 предложений: кому вы звоните, что отправляете или показываете, куда идёте и благодаря кому либо из-за чего изменился план.", SMALL),
    PageBreak(),

    p("6. Ответы и проверка мастерства", H1),
    p("Ответы", H2),
    p("<b>1.</b> píšem kolegovi; pomáham sestre; idem k lekárovi; dávam vodu dieťaťu; oproti škole; proti bolesti.", TINY),
    p("<b>2.</b> mi; ti; mu; jej; vám; im.", TINY),
    p("<b>3.</b> k nemu; kvôli tebe; vďaka nim; oproti vám; ku mne; k nej.", TINY),
    p("<b>4.</b> Dám knihu kolegovi. Pošlem správu mame. Ukážem projekt klientovi. Kúpim darček sestre. Požičiam auto priateľovi.", TINY),
    p("<b>5.</b> 1) Dám kolegovi knihu. 2) Zavolám mu. / Idem k nemu. 3) Vďaka tvojej rade som uspel. 4) Pošlem mu ju večer. 5) Pomáham môjmu novému susedovi.", TINY),
    p("<b>6. Модель:</b> Dnes zavolám kamarátovi. Pošlem mu adresu a ukážem mu nový plán. Potom pôjdem k nemu. Vďaka jeho pomoci skončíme skôr. Kvôli dažďu však zostaneme doma. Večer mu poďakujem.", TINY),
    p("Итог в четырёх пунктах", H2),
    styled_table([
        ["OK", "Я образую частые формы Datív и согласую всю группу."],
        ["OK", "Я различаю короткие mi/ti/mu/jej/im и формы после предлога nemu/nej/nim."],
        ["OK", "Я строю модель A + D и ставлю два местоимения в порядке D + A."],
        ["OK", "Я выбираю k/ku, vďaka, kvôli, oproti или proti по смыслу."],
    ], [12 * mm, 158 * mm], font_size=7.3, header=False),
    Spacer(1, 3 * mm),
    box("<b>Финальная проверка:</b> скажите, кому вы сегодня позвоните, что ему отправите, к кому пойдёте и благодаря кому или из-за чего изменится ваш план.", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    p("Следующий шаг", H2),
    p("В теме 2.9 вы перейдёте к Lokál: место и тема разговора, предлоги v/vo, na, pri, o, формы существительных и прилагательных, а также o mne/tebe/ňom/nej/nás/vás/nich.", SMALL),
]

doc.build(story)
print(OUTPUT)
