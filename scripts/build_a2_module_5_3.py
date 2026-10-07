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
OUTPUT = ROOT / "output" / "pdf" / "A2" / "Module_05" / "Slovak_A2_Tema_5_3_Peredaem_soobshchenie_s_ze.pdf"
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
        canvas.drawString(20 * mm, height - 12 * mm, "A2 5.3  |  Передаём сообщение с že")
    canvas.setFont("Arial", 8)
    canvas.setFillColor(MUTED)
    canvas.drawString(20 * mm, 9 * mm, "SlovoKrok | личный учебный модуль")
    canvas.drawRightString(width - 20 * mm, 9 * mm, f"стр. {page} / 7")
    canvas.restoreState()


doc = BaseDocTemplate(
    str(OUTPUT), pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=20 * mm, bottomMargin=18 * mm,
    title="Slovak A2 - Тема 5.3 - Передаём сообщение с že", author="SlovoKrok",
)
frame = Frame(20 * mm, 18 * mm, 170 * mm, 257 * mm, id="main", leftPadding=0, rightPadding=0)
doc.addPageTemplates([PageTemplate(id="series", frames=[frame], onPage=draw_page)])

story = [
    p("МОДУЛЬ 5  •  СВЯЗНАЯ РЕЧЬ И СЛОЖНЫЕ ПРЕДЛОЖЕНИЯ", COVER_KICKER),
    p("Передаём сообщение<br/>с že", TITLE),
    p("Nepriama správa: что сказал, думает, надеется или просит другой человек", SUBTITLE),
    Spacer(1, 35 * mm),
    p("Союз <b>že</b> вводит содержание сообщения: что человек сказал, написал, знает, думает или надеется. Для простого косвенного сообщения важно поставить запятую, изменить лицо и выбрать время по смыслу."),
    p("После модуля вы сможете:", H2),
    styled_table([
        ["1", "строить сообщения по модели povedal/napísal, že..."],
        ["2", "передавать мнение и надежду: myslím si/dúfam/verím, že..."],
        ["3", "менять лицо, притяжательные и короткие местоимения по ситуации"],
        ["4", "выбирать настоящее, прошедшее или будущее по реальному времени"],
    ], [12 * mm, 158 * mm], font_size=7.2, header=False),
    Spacer(1, 3 * mm),
    box("<b>Формула:</b> источник + глагол сообщения <b>, že</b> + содержание с новой точки зрения.", PALE, PINK),
    PageBreak(),

    p("1. Базовая модель: кто сообщает и что", H1),
    p("Главная часть называет источник и способ сообщения. После неё ставится запятая, затем <b>že</b> и обычное предложение с подлежащим и сказуемым."),
    styled_table([
        ["Источник", "Словацкий пример", "Перевод"],
        ["сказал", "Peter povedal, že príde večer.", "Петер сказал, что придёт вечером."],
        ["написала", "Anna napísala, že je doma.", "Анна написала, что она дома."],
        ["сообщили", "Oznámili, že vlak mešká.", "Они сообщили, что поезд опаздывает."],
        ["знаю", "Viem, že obchod je zatvorený.", "Я знаю, что магазин закрыт."],
        ["слышал", "Počul som, že susedia sa sťahujú.", "Я слышал, что соседи переезжают."],
    ], [27 * mm, 76 * mm, 67 * mm], font_size=6.2),
    p("Запятая ставится перед že", H2),
    styled_table([
        ["Правильно", "Неправильно"],
        ["Mária povedala, že nemá čas.", "*Mária povedala že nemá čas."],
        ["Dúfam, že sa čoskoro uvidíme.", "*Dúfam že sa čoskoro uvidíme."],
        ["Verím, že to zvládneš.", "*Verím že to zvládneš."],
    ], [85 * mm, 85 * mm], font_size=6.5),
    box("<b>Že передаёт утверждение или содержание мысли.</b> Не используйте эту модель механически для вопроса: *Pýtal sa, že...* Здесь мы тренируем сообщения, а не косвенные вопросы.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    PageBreak(),

    p("2. Меняем лицо и точку зрения", H1),
    p("В прямой речи человек говорит <b>ja, môj, mi</b>. В косвенном сообщении формы меняются в зависимости от того, кто пересказывает и о ком идёт речь."),
    styled_table([
        ["Прямая фраза", "Косвенное сообщение", "Что изменилось"],
        ["Mária: Som unavená.", "Mária povedala, že je unavená.", "som -> je"],
        ["Peter: Mám čas.", "Peter povedal, že má čas.", "mám -> má"],
        ["My: Prídeme o šiestej.", "Povedali sme, že prídeme o šiestej.", "мы пересказываем себя"],
        ["Jana: Zavolám ti.", "Jana povedala Petrovi, že mu zavolá.", "ti -> mu"],
        ["Marek: Moja sestra býva v Nitre.", "Marek povedal, že jeho sestra býva v Nitre.", "moja -> jeho"],
    ], [47 * mm, 80 * mm, 43 * mm], font_size=5.95),
    p("Короткие местоимения после že", H2),
    p("Клитика обычно стоит близко к началу придаточной части: <b>Povedala, že mi zavolá.</b> / <b>Napísal, že sa vráti neskôr.</b> / <b>Oznámili, že nám pošlú nový termín.</b> Это продолжает порядок коротких форм из темы 1.3."),
    p("Три шага", H2),
    styled_table([
        ["1", "Кто говорил?", "Peter -> он: má, príde, jeho"],
        ["2", "Кому направлено действие?", "mne -> mu/jej/nám по ситуации"],
        ["3", "Кто пересказывает?", "я/мы сохраняем формы, если точка зрения не изменилась"],
    ], [12 * mm, 63 * mm, 95 * mm], font_size=6.25, header=False),
    box("<b>Типичная ошибка:</b> *Peter povedal, že mám čas* означает, что время есть у говорящего \"я\". Если время есть у Петера: <b>Peter povedal, že má čas.</b>", PALE, ROSE, SMALL),
    PageBreak(),

    p("3. Время выбираем по смыслу", H1),
    p("В словацком не нужно автоматически сдвигать время назад только потому, что главное сказуемое стоит в прошедшем. Форма после <b>že</b> показывает, когда происходит само содержание."),
    styled_table([
        ["Смысл сообщения", "Пример", "Перевод"],
        ["актуально сейчас", "Povedal, že pracuje doma.", "Он сказал, что работает дома."],
        ["было раньше", "Povedal, že včera pracoval doma.", "Он сказал, что вчера работал дома."],
        ["будет позже", "Povedal, že zajtra bude pracovať doma.", "Он сказал, что завтра будет работать дома."],
        ["общий факт", "Učiteľ povedal, že voda vrie pri 100 °C.", "Учитель сказал, что вода кипит при 100 °C."],
        ["результат впереди", "Mária napísala, že príde v piatok.", "Мария написала, что придёт в пятницу."],
    ], [34 * mm, 75 * mm, 61 * mm], font_size=6.1),
    p("Слова времени и места", H2),
    p("Если точка отсчёта изменилась, уточните слова <b>dnes, zajtra, tu</b>. Не меняйте их механически: сначала проверьте, остаются ли \"сегодня\", \"завтра\" и \"здесь\" теми же для нового слушателя."),
    styled_table([
        ["Исходная фраза", "Поздний пересказ"],
        ["V pondelok: Prídem zajtra.", "V pondelok povedal, že príde na druhý deň."],
        ["Som tu do piatej.", "Povedala, že tam bude do piatej."],
        ["Dnes mám voľno.", "Včera povedal, že v ten deň mal voľno."],
    ], [75 * mm, 95 * mm], font_size=6.35),
    box("<b>Ученическая опора:</b> <b>že</b> не выбирает время за вас. Спросите: содержание верно сейчас, было раньше или произойдёт позже?", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    PageBreak(),

    p("4. Мнение, надежда и простая просьба", H1),
    p("С <b>že</b> можно не только пересказать факт, но и обозначить отношение говорящего. Для просьбы на этом уровне удобно передать нужное действие через <b>mám/máme + infinitív</b>."),
    styled_table([
        ["Функция", "Словацкая модель", "Перевод"],
        ["мнение", "Myslím si, že tento plán je dobrý.", "Я думаю, что этот план хороший."],
        ["надежда", "Dúfam, že zajtra nebude pršať.", "Надеюсь, что завтра не будет дождя."],
        ["уверенность", "Verím, že skúšku zvládneš.", "Верю, что ты справишься с экзаменом."],
        ["сомнение", "Nemyslím si, že je to pravda.", "Я не думаю, что это правда."],
        ["просьба/инструкция", "Mama povedala, že mám kúpiť chlieb.", "Мама сказала, чтобы я купил хлеб."],
        ["просьба группе", "Povedala, že jej máme poslať adresu.", "Она сказала, чтобы мы прислали ей адрес."],
    ], [32 * mm, 78 * mm, 60 * mm], font_size=6.0),
    p("Мини-диалог: передаём сообщение коллеге", H2),
    box("<b>Lucia:</b> Čo napísal Marek?<br/><b>Ivan:</b> Napísal, že príde o šiestej.<br/><b>Lucia:</b> Bude stretnutie dlhé?<br/><b>Ivan:</b> Myslí si, že potrvá asi hodinu.<br/><b>Lucia:</b> Máme niečo pripraviť?<br/><b>Ivan:</b> Áno. Napísal, že máme vytlačiť dokumenty a že mu máme poslať adresu.<br/><b>Lucia:</b> Dobre. Dúfam, že všetko stihneme.", PALE, ROSE, SMALL),
    p("Медиация в одном сообщении", H2),
    box("<b>Marek napísal, že príde o šiestej. Myslí si, že stretnutie potrvá asi hodinu. Povedal, že máme vytlačiť dokumenty a poslať mu adresu. Dúfa, že všetko pripravíme včas.</b><br/>Марк написал, что придёт в шесть. Он думает, что встреча продлится около часа. Он сказал, чтобы мы распечатали документы и прислали ему адрес. Он надеется, что мы всё подготовим вовремя.", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    PageBreak(),

    p("5. Частые ошибки и упражнения", H1),
    box("<b>Частые ошибки:</b> пропускают запятую перед <b>že</b>; сохраняют <b>som/mám/môj</b> после смены говорящего; механически ставят прошедшее время; используют <b>že</b> как союз косвенного вопроса.", CREAM, colors.HexColor("#E7C76C"), TINY),
    p("Упражнение 1. Вставьте že и запятую", H2),
    p("1) Peter povedal ___ príde večer. 2) Dúfam ___ bude pekne. 3) Viem ___ obchod je otvorený. 4) Verím ___ to zvládneš.", TINY),
    p("Упражнение 2. Измените лицо", H2),
    p("Передайте слова: 1) Mária: Som doma. 2) Peter: Mám čas. 3) Jana Petrovi: Zavolám ti. 4) Marek: Moja sestra študuje v Nitre.", TINY),
    p("Упражнение 3. Выберите время", H2),
    p("1) Včera povedal, že dnes (pracuje/pracoval). 2) Povedal, že minulý týždeň (je/bol) chorý. 3) Napísala, že zajtra (prišla/príde). 4) Učiteľ povedal, že Zem (obiehala/obieha) okolo Slnka.", TINY),
    p("Упражнение 4. Исправьте ошибки", H2),
    p("1) Anna povedala že je unavená. 2) Peter povedal, že mám čas. (время у Петера) 3) Mária napísala, že zajtra prišla. 4) Marek povedal, že moja sestra býva v Nitre. (сестра Марека)", TINY),
    p("Упражнение 5. Передайте сообщение", H2),
    p("Переведите: 1) Я думаю, что план хороший. 2) Надеюсь, что завтра не будет дождя. 3) Анна написала, что придёт в пятницу. 4) Мама сказала, чтобы мы купили хлеб.", TINY),
    p("Упражнение 6. Короткая медиация", H2),
    p("Передайте другу 5-7 предложениями сообщение коллеги: когда он придёт, что думает о встрече, что нужно подготовить и на что он надеется. Используйте <b>povedal/napísal, že</b>, <b>myslí si, že</b> и <b>dúfa, že</b>.", TINY),
    PageBreak(),

    p("6. Ответы и проверка мастерства", H1),
    p("Ответы", H2),
    p("<b>1.</b> Peter povedal, že príde večer. Dúfam, že bude pekne. Viem, že obchod je otvorený. Verím, že to zvládneš.", TINY),
    p("<b>2.</b> Mária povedala, že je doma. Peter povedal, že má čas. Jana povedala Petrovi, že mu zavolá. Marek povedal, že jeho sestra študuje v Nitre.", TINY),
    p("<b>3.</b> 1) pracuje; 2) bol; 3) príde; 4) obieha.", TINY),
    p("<b>4.</b> Anna povedala, že je unavená. Peter povedal, že má čas. Mária napísala, že zajtra príde. Marek povedal, že jeho sestra býva v Nitre.", TINY),
    p("<b>5.</b> Myslím si, že plán je dobrý. Dúfam, že zajtra nebude pršať. Anna napísala, že príde v piatok. Mama povedala, že máme kúpiť chlieb.", TINY),
    p("<b>6. Модель:</b> Kolega napísal, že príde o šiestej. Myslí si, že stretnutie potrvá asi hodinu. Povedal, že máme pripraviť miestnosť a vytlačiť dokumenty. Napísal, že mu máme poslať adresu. Dúfa, že všetko stihneme. Возможны другие естественные варианты.", TINY),
    p("Итог в четырёх пунктах", H2),
    styled_table([
        ["OK", "Перед že ставлю запятую."],
        ["OK", "Меняю лицо и местоимения по новой точке зрения."],
        ["OK", "Выбираю время по смыслу, без автоматического сдвига."],
        ["OK", "Передаю факт, мнение, надежду и простую просьбу."],
    ], [12 * mm, 158 * mm], font_size=6.45, header=False),
    Spacer(1, 2 * mm),
    box("<b>Финальная проверка:</b> передайте от третьего лица: \"Я приду завтра. Думаю, что встреча будет короткой. Пожалуйста, распечатайте документы\".", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    p("Следующий шаг", H2),
    p("В теме 5.4 вы научитесь уточнять человека или предмет относительным предложением с <b>ktorý</b>.", SMALL),
]

doc.build(story)
print(OUTPUT)
