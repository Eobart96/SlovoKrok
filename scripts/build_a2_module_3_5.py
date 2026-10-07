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
OUTPUT = ROOT / "output" / "pdf" / "A2" / "Module_03" / "Slovak_A2_Tema_3_5_Lichnye_mestoimeniya_v_kosvennyh_padezhah.pdf"
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
TITLE = ParagraphStyle("Title", fontName="Arial-Bold", fontSize=19.5, leading=23, textColor=colors.white, alignment=TA_LEFT, spaceAfter=5 * mm)
SUBTITLE = ParagraphStyle("Subtitle", fontName="Arial", fontSize=11.5, leading=15, textColor=colors.HexColor("#FFD8EB"), spaceAfter=5 * mm)
H1 = ParagraphStyle("H1", fontName="Arial-Bold", fontSize=15.5, leading=18.5, textColor=PLUM, spaceBefore=1 * mm, spaceAfter=3.0 * mm)
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
        canvas.drawString(20 * mm, height - 12 * mm, "A2 3.5  |  Личные местоимения в косвенных падежах")
    canvas.setFont("Arial", 8)
    canvas.setFillColor(MUTED)
    canvas.drawString(20 * mm, 9 * mm, "SlovoKrok | личный учебный модуль")
    canvas.drawRightString(width - 20 * mm, 9 * mm, f"стр. {page} / 7")
    canvas.restoreState()


doc = BaseDocTemplate(
    str(OUTPUT), pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=20 * mm, bottomMargin=18 * mm,
    title="Slovak A2 - Тема 3.5 - Личные местоимения в косвенных падежах", author="SlovoKrok",
)
frame = Frame(20 * mm, 18 * mm, 170 * mm, 257 * mm, id="main", leftPadding=0, rightPadding=0)
doc.addPageTemplates([PageTemplate(id="series", frames=[frame], onPage=draw_page)])

story = [
    p("МОДУЛЬ 3  •  ПРИЛАГАТЕЛЬНЫЕ, МЕСТОИМЕНИЯ И ЧИСЛИТЕЛЬНЫЕ", COVER_KICKER),
    p("Личные местоимения<br/>в косвенных падежах", TITLE),
    p("Osobné zámená v nepriamych pádoch", SUBTITLE),
    Spacer(1, 31 * mm),
    p("В разговоре мы редко повторяем имя: просим <b>его</b>, отвечаем <b>ей</b>, говорим <b>о них</b>. В словацком важно выбрать падеж, затем решить: нужна короткая форма, полная форма или вариант после предлога.", BODY),
    p("После модуля вы сможете:", H2),
    styled_table([
        ["1", "выбирать формы личных местоимений в G/D/A/L/I"],
        ["2", "различать нейтральные клитики mi, ti, mu, ma, ťa, ho и полные формы"],
        ["3", "правильно использовать формы после предлогов: pre mňa, k nej, o nich, s nimi"],
        ["4", "ставить дательный объект перед винительным: Dám ti ho."],
    ], [12 * mm, 158 * mm], font_size=7.25, header=False),
    Spacer(1, 3 * mm),
    box("<b>Алгоритм:</b> роль в предложении -> падеж -> есть ли предлог или логическое ударение -> форма -> место в предложении.", PALE, PINK),
    PageBreak(),

    p("1. Сначала определите падеж", H1),
    p("Форма местоимения зависит не от русского перевода, а от управления словацкого глагола или предлога. Сначала задайте падежный вопрос.", BODY),
    styled_table([
        ["Падеж", "Вопрос и сигнал", "Пример"],
        ["G genitív", "koho? без кого?", "Bojím sa ho. - Я боюсь его."],
        ["D datív", "komu? кому?", "Pomôžem jej. - Я помогу ей."],
        ["A akuzatív", "koho? кого вижу?", "Poznáš ma? - Ты меня знаешь?"],
        ["L lokál", "o kom? только после предлога", "Hovoríme o nich. - Мы говорим о них."],
        ["I inštrumentál", "s kým? с кем?", "Idem s ním. - Я иду с ним."],
    ], [34 * mm, 54 * mm, 82 * mm], font_size=6.55),
    p("Формы ja, ty, my, vy", H2),
    styled_table([
        ["Падеж", "ja", "ty", "my", "vy"],
        ["G", "mňa / ma", "teba / ťa", "nás", "vás"],
        ["D", "mne / mi", "tebe / ti", "nám", "vám"],
        ["A", "mňa / ma", "teba / ťa", "nás", "vás"],
        ["L", "mne", "tebe", "nás", "vás"],
        ["I", "mnou", "tebou", "nami", "vami"],
    ], [30 * mm, 35 * mm, 35 * mm, 35 * mm, 35 * mm], font_size=6.7),
    box("<b>Два koho?</b> G и A различайте по управлению: <b>báť sa + G</b>, но <b>vidieť + A</b>. Формы иногда совпадают, функция различна.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    PageBreak(),

    p("2. Третье лицо: on, ona, ono, oni", H1),
    p("В третьем лице особенно заметны три ряда: форма без предлога, короткая клитика и форма с начальным <b>n-</b> после предлога.", BODY),
    styled_table([
        ["Падеж", "on / ono", "ona", "oni / ony"],
        ["G", "jeho / ho; po predl. neho", "jej; po predl. nej", "ich; po predl. nich"],
        ["D", "jemu / mu; po predl. nemu", "jej; po predl. nej", "im; po predl. nim"],
        ["A", "on: jeho / ho; pre neho<br/>ono: ho; naň", "ju; po predl. ňu", "ich; po predl. nich"],
        ["L", "ňom", "nej", "nich"],
        ["I", "ním", "ňou", "nimi"],
    ], [27 * mm, 55 * mm, 45 * mm, 43 * mm], font_size=6.25),
    p("Короткая или полная форма?", H2),
    styled_table([
        ["Ситуация", "Модель", "Пример"],
        ["Нейтральное сообщение", "короткая клитика", "Vidím ho každý deň. - Я вижу его каждый день."],
        ["Контраст или исправление", "полная форма", "Pozvali mňa, nie jeho. - Позвали меня, не его."],
        ["Начало ответа с акцентом", "полная форма", "Jemu to nepoviem. - Ему я этого не скажу."],
        ["После предлога", "полная форма; 3-е лицо с n-", "Bez nej nepôjdem. - Без неё я не пойду."],
    ], [44 * mm, 46 * mm, 80 * mm], font_size=6.35),
    box("Формы <b>jej, ju, nás, vás, ich, im</b> без предлога не имеют отдельной длинной пары. Контраст передаётся позицией и ударением; после предлога у 3-го лица появляется <b>n-</b>.", PALE, ROSE, SMALL),
    PageBreak(),

    p("3. После предлога: n- в третьем лице", H1),
    p("Предлог требует полной формы. У местоимений третьего лица используйте ряд с <b>n-</b>. Короткие <b>ho, mu</b> после предлога не ставятся.", BODY),
    styled_table([
        ["Управление", "Правильная форма", "Пример"],
        ["bez + G", "bez neho / nej / nich", "Bez nich nezačneme. - Без них не начнём."],
        ["od + G", "od neho / nej / nich", "Mám správu od nej. - У меня сообщение от неё."],
        ["k + D", "k nemu / nej / nim", "Prídem k nemu večer. - Я приду к нему вечером."],
        ["pre + A", "pre neho / ňu / nich", "Je to pre ňu. - Это для неё."],
        ["o + L", "o ňom / nej / nich", "Často o ňom hovorí. - Она часто говорит о нём."],
        ["s + I", "s ním / ňou / nimi", "Pracujem s nimi. - Я работаю с ними."],
    ], [35 * mm, 55 * mm, 80 * mm], font_size=6.35),
    p("Первое и второе лицо после предлога", H2),
    styled_table([
        ["G / A", "D / L", "I"],
        ["pre mňa, bez teba, na nás, za vás", "ku mne, k tebe, o nás, o vás", "so mnou, s tebou, s nami, s vami"],
    ], [57 * mm, 57 * mm, 56 * mm], font_size=6.45),
    box("<b>Сравните:</b> <b>Dám mu kľúč.</b> - Дам ему ключ. Но: <b>Idem k nemu.</b> - Иду к нему. Предлог <b>k</b> включает форму <b>nemu</b>.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    box("<b>Произношение и письмо:</b> so mnou, s tebou, s ním; перед некоторыми сочетаниями предлог получает форму <b>so</b> для удобства произношения.", PALE, ROSE, SMALL),
    PageBreak(),

    p("4. Клитики и порядок слов", H1),
    p("Короткие формы без ударения тянутся к началу предложения и обычно входят в группу после первого смыслового блока. Если рядом D и A, порядок такой: <b>дательный + винительный</b>.", BODY),
    styled_table([
        ["Модель", "Пример и перевод"],
        ["первый блок + клитика", "Dnes mu zavolám. - Сегодня я ему позвоню."],
        ["D + A", "Dám ti ho zajtra. - Я дам его тебе завтра."],
        ["прошедшее: som + D + A", "Včera som mu ju poslal. - Вчера я послал её ему."],
        ["sa/si + D + A", "Peter si ju odo mňa požičal. - Петер одолжил её у меня."],
        ["условие: by + som + D + A", "Ukázal by som vám ho. - Я бы показал его вам."],
    ], [57 * mm, 113 * mm], font_size=6.45),
    box("<b>Рабочая цепочка:</b> <b>by - som/si/sme/ste - sa/si - D - A</b>. Не все элементы обязательны, но их относительный порядок сохраняется.", PALE, PINK, SMALL),
    p("Мини-диалог: передаём сообщение", H2),
    box("<b>A:</b> Máš správu od Lenky? - У тебя есть сообщение от Ленки?<br/><b>B:</b> Áno, ráno <b>mi ju</b> poslala. - Да, утром она прислала её мне.<br/><b>A:</b> Môžeš <b>mi ju</b> ukázať? - Можешь показать её мне?<br/><b>B:</b> Teraz nie. O chvíľu <b>ti ju</b> prepošlem. - Сейчас нет. Через минуту я перешлю её тебе.<br/><b>A:</b> Dobre. Potom <b>jej</b> odpoviem. - Хорошо. Потом я ей отвечу.<br/><b>B:</b> Napíš <b>jej</b>, že sa s <b>ňou</b> stretneme zajtra. - Напиши ей, что мы встретимся с ней завтра.", PALE, ROSE, TINY),
    p("В диалоге <b>mi ju / ti ju</b> - две клитики, а <b>s ňou</b> - форма после предлога.", SMALL),
    PageBreak(),

    p("5. Частые ошибки и упражнения", H1),
    box("<b>Частые ошибки:</b> *pre ju -> <b>pre ňu</b>; *k mu -> <b>k nemu</b>; *o ho -> <b>o ňom</b>; *Dám ho ti -> <b>Dám ti ho</b>; *Mi to povedal -> нейтрально <b>Povedal mi to</b>, но при контрасте <b>Mne to povedal</b>.", CREAM, colors.HexColor("#E7C76C"), TINY),
    p("Упражнение 1. Назовите падеж", H2),
    p("1) Pomáham jej. 2) Hovoríme o nich. 3) Bojím sa ho. 4) Idem s tebou. 5) Poznáte nás?", TINY),
    p("Упражнение 2. Замените имя местоимением", H2),
    p("1) Volám Petrovi. 2) Čakám na Evu. 3) Hovorím o Petrovi a Eve. 4) Pracujem s Annou. 5) Mám správu od kolegov.", TINY),
    p("Упражнение 3. Выберите короткую или полную форму", H2),
    p("1) Dnes mi / mne zavolá. 2) Mňa / Ma pozvali, nie Petra. 3) Vidím ho / jeho každý deň. 4) Jemu / Mu to vysvetlím, tebe nie. 5) Poznáš ma / mňa?", TINY),
    p("Упражнение 4. Добавьте форму после предлога", H2),
    p("1) bez (ona); 2) k (on); 3) o (oni); 4) s (ona); 5) pre (ja).", TINY),
    p("Упражнение 5. Исправьте ошибки", H2),
    p("1) Je to pre ju. 2) Zajtra idem k mu. 3) Dám ho ti večer. 4) Hovoríme o ich. 5) Mi poslala fotografiu.", TINY),
    p("Упражнение 6. Своё сообщение", H2),
    p("Напишите 5-7 предложений: кто прислал вам сообщение, кому вы его покажете, о ком в нём говорится и с кем вы встретитесь. Используйте две клитики вместе и две формы после предлога.", TINY),
    PageBreak(),

    p("6. Ответы и проверка мастерства", H1),
    p("Ответы", H2),
    p("<b>1.</b> D; L; G; I; A.", TINY),
    p("<b>2.</b> Volám mu. Čakám na ňu. Hovorím o nich. Pracujem s ňou. Mám správu od nich.", TINY),
    p("<b>3.</b> Dnes mi zavolá. Mňa pozvali, nie Petra. Vidím ho každý deň. Jemu to vysvetlím, tebe nie. Poznáš ma?", TINY),
    p("<b>4.</b> bez nej; k nemu; o nich; s ňou; pre mňa.", TINY),
    p("<b>5.</b> Je to pre ňu. Zajtra idem k nemu. Dám ti ho večer. Hovoríme o nich. Poslala mi fotografiu. Последний вариант нейтрален; <b>Mne poslala fotografiu</b> возможен при контрасте.", TINY),
    p("<b>6. Модель:</b> Ráno mi Jana poslala správu. Večer ti ju ukážem. Píše v nej o nových kolegoch. Zajtra sa s nimi stretneme. Bez nich nemôžeme začať projekt. Potom im odpovieme. Возможны другие естественные варианты.", TINY),
    p("Итог в четырёх пунктах", H2),
    styled_table([
        ["OK", "Выбираю G/D/A/L/I по управлению словацкого слова."],
        ["OK", "Различаю нейтральное mi/ti/mu/ma/ťa/ho и ударное mne/tebe/jemu/mňa/teba/jeho."],
        ["OK", "После предлога использую pre ňu, k nemu, o nich, s nimi."],
        ["OK", "Ставлю две объектные клитики в порядке D + A: mi ho, ti ju, mu ich."],
    ], [12 * mm, 158 * mm], font_size=6.65, header=False),
    Spacer(1, 2 * mm),
    box("<b>Финальная проверка:</b> без таблицы скажите: кто вам позвонил, кому вы ответили, кого ждёте, о ком говорили и с кем встретитесь. Затем замените один нейтральный ответ контрастным.", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    p("Следующий шаг", H2),
    p("В теме 3.6 вы научитесь точно показывать, кому принадлежит предмет и связан ли владелец с субъектом предложения.", SMALL),
]

doc.build(story)
print(OUTPUT)
