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
OUTPUT = ROOT / "output/pdf/A2/Module_06/Slovak_A2_Tema_6_5_Zvonok_soobshchenie_i_elektronnoe_pismo.pdf"
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
BODY = ParagraphStyle("Body", fontName="Arial", fontSize=8.55, leading=11.2, textColor=INK, spaceAfter=2.5 * mm)
SMALL = ParagraphStyle("Small", parent=BODY, fontSize=7.35, leading=9.15, spaceAfter=1.35 * mm)
TINY = ParagraphStyle("Tiny", parent=BODY, fontSize=6.55, leading=7.95, spaceAfter=0.85 * mm)
TITLE = ParagraphStyle("Title", fontName="Arial-Bold", fontSize=20, leading=24, textColor=colors.white, alignment=TA_LEFT, spaceAfter=5 * mm)
SUBTITLE = ParagraphStyle("Subtitle", fontName="Arial", fontSize=11.4, leading=15, textColor=colors.HexColor("#FFD8EB"), spaceAfter=5 * mm)
H1 = ParagraphStyle("H1", fontName="Arial-Bold", fontSize=15.5, leading=18.5, textColor=PLUM, spaceBefore=1 * mm, spaceAfter=3 * mm)
H2 = ParagraphStyle("H2", fontName="Arial-Bold", fontSize=10.6, leading=13.1, textColor=PINK, spaceBefore=1 * mm, spaceAfter=1.35 * mm)
KICK = ParagraphStyle("Kicker", fontName="Arial-Bold", fontSize=10, leading=12, textColor=colors.HexColor("#FFD8EB"), spaceAfter=4 * mm)


def p(text, style=BODY):
    return Paragraph(text, style)


def box(text, bg=PALE, border=ROSE, style=BODY, pad=7):
    item = Table([[p(text, style)]], colWidths=[170 * mm])
    item.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("BOX", (0, 0), (-1, -1), 0.7, border),
        ("LEFTPADDING", (0, 0), (-1, -1), pad),
        ("RIGHTPADDING", (0, 0), (-1, -1), pad),
        ("TOPPADDING", (0, 0), (-1, -1), pad),
        ("BOTTOMPADDING", (0, 0), (-1, -1), pad),
    ]))
    return item


def table(data, widths, size=7.0, header=True):
    rows = []
    for row_index, row in enumerate(data):
        style = ParagraphStyle(
            f"cell_{row_index}_{size}_{len(data)}",
            parent=SMALL,
            fontSize=size,
            leading=size + 1.75,
            textColor=colors.white if header and row_index == 0 else INK,
            fontName="Arial-Bold" if header and row_index == 0 else "Arial",
            spaceAfter=0,
        )
        rows.append([p(str(value), style) for value in row])
    item = Table(rows, colWidths=widths, repeatRows=1 if header else 0)
    commands = [
        ("GRID", (0, 0), (-1, -1), 0.45, ROSE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]
    if header:
        commands.append(("BACKGROUND", (0, 0), (-1, 0), PLUM))
    start = 1 if header else 0
    for row_index in range(start, len(data)):
        if (row_index - start) % 2:
            commands.append(("BACKGROUND", (0, row_index), (-1, row_index), ALT))
    item.setStyle(TableStyle(commands))
    return item


def draw_page(canvas, doc):
    width, height = A4
    page_number = canvas.getPageNumber()
    canvas.saveState()
    if page_number == 1:
        canvas.setFillColor(PLUM)
        canvas.rect(0, height - 91 * mm, width, 91 * mm, fill=1, stroke=0)
        canvas.setFillColor(PINK)
        canvas.rect(0, height - 94 * mm, width, 3 * mm, fill=1, stroke=0)
    else:
        canvas.setStrokeColor(PINK)
        canvas.line(20 * mm, height - 16 * mm, width - 20 * mm, height - 16 * mm)
        canvas.setFont("Arial", 8)
        canvas.setFillColor(MUTED)
        canvas.drawString(20 * mm, height - 12 * mm, "A2 6.5  |  Звонок, сообщение и электронное письмо")
    canvas.setFont("Arial", 8)
    canvas.setFillColor(MUTED)
    canvas.drawString(20 * mm, 9 * mm, "SlovoKrok | личный учебный модуль")
    canvas.drawRightString(width - 20 * mm, 9 * mm, f"стр. {page_number} / 7")
    canvas.restoreState()


doc = BaseDocTemplate(
    str(OUTPUT), pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm,
    topMargin=20 * mm, bottomMargin=18 * mm,
    title="Slovak A2 - Тема 6.5 - Звонок, сообщение и электронное письмо",
    author="SlovoKrok",
)
doc.addPageTemplates([
    PageTemplate(id="series", frames=[Frame(20 * mm, 18 * mm, 170 * mm, 257 * mm, id="main", leftPadding=0, rightPadding=0)], onPage=draw_page)
])


story = [
    p("МОДУЛЬ 6  •  ДОМ, ИНТЕРНЕТ И ПОКУПКИ", KICK),
    p("Звонок, сообщение<br/>и электронное письмо", TITLE),
    p("Telefonát, správa a e-mail: сообщаем цель, адресата и ожидаемое действие", SUBTITLE),
    Spacer(1, 41 * mm),
    p("Хорошее сообщение отвечает на четыре вопроса: кто говорит, кому, по какому поводу и что нужно сделать дальше. В словацком адресат часто стоит в дательном падеже, а тон зависит от отношений с человеком."),
    p("После модуля вы сможете:", H2),
    table([
        ["1", "оставить понятное голосовое сообщение"],
        ["2", "назвать адресата в дательном падеже"],
        ["3", "правильно поставить полные дополнения и клитики"],
        ["4", "написать личное или короткое рабочее письмо"],
    ], [12 * mm, 158 * mm], 7.2, False),
    Spacer(1, 3 * mm),
    box("<b>Формула:</b> обращение + причина сообщения + нужная информация или просьба + следующий шаг + завершение."),
    PageBreak(),

    p("1. Канал и структура сообщения", H1),
    p("Содержание остаётся тем же, но канал меняет форму. В голосовом сообщении назовите себя и номер для ответа; в чате можно писать короче; в письме нужны тема, обращение и завершение."),
    table([
        ["Канал", "Что обязательно", "Полезная модель"],
        ["голосовое сообщение", "имя, причина, обратный контакт", "Tu je Anna. Volám ohľadom stretnutia."],
        ["короткое сообщение", "контекст, конкретный вопрос", "Píšem ti kvôli zajtrajšku."],
        ["личное письмо", "обращение, новости, вопрос", "Ahoj, ozývam sa po dlhšom čase."],
        ["рабочее письмо", "предмет, цель, просьба, подпись", "Píšem Vám ohľadom objednávky."],
    ], [38 * mm, 58 * mm, 74 * mm], 5.65),
    p("Скелет голосового сообщения", H2),
    table([
        ["Шаг", "Фраза"],
        ["представиться", "Dobrý deň, tu je Nina Kováčová."],
        ["назвать причину", "Volám ohľadom zajtrajšej návštevy."],
        ["сообщить главное", "Prídem približne o desiatej."],
        ["попросить ответ", "Prosím, zavolajte mi späť na toto číslo."],
        ["завершить", "Ďakujem. Dovidenia."],
    ], [39 * mm, 131 * mm], 5.85),
    box("<b>Не начинайте только с Prosím, zavolajte mi.</b> Получателю нужны имя и причина звонка, иначе он не понимает контекст.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    PageBreak(),

    p("2. Адресат: дательный падеж", H1),
    p("После <i>písať, napísať, volať, zavolať, poslať, odpovedať</i> адресат отвечает на вопрос <i>komu?</i>. Предмет сообщения часто отвечает на вопрос <i>čo?</i> и стоит в аккузативе."),
    table([
        ["Кому?", "Форма", "Пример"],
        ["брату", "bratovi", "Napíšem bratovi správu."],
        ["подруге", "kamarátke", "Pošlem kamarátke fotografiu."],
        ["коллеге-мужчине", "kolegovi", "Zavolám kolegovi po obede."],
        ["коллеге-женщине", "kolegyni", "Odpoviem kolegyni dnes."],
        ["родителям", "rodičom", "Pošleme rodičom pozdrav."],
        ["клиентам", "klientom", "Napíšeme klientom e-mail."],
    ], [40 * mm, 42 * mm, 88 * mm], 5.8),
    p("Полные дополнения: A + D", H2),
    p("Нейтральная учебная модель: сначала предмет в аккузативе, затем адресат в дательном. Это особенно удобно, когда обе части новые или длинные.", SMALL),
    table([
        ["A: что?", "D: кому?", "Целая фраза"],
        ["správu", "vedúcemu", "Pošlem správu vedúcemu."],
        ["nový termín", "klientke", "Navrhneme nový termín klientke."],
        ["potvrdenie", "všetkým účastníkom", "Pošlite potvrdenie všetkým účastníkom."],
    ], [42 * mm, 52 * mm, 76 * mm], 5.7),
    box("Порядок можно менять ради темы и акцента: <i>Vedúcemu pošlem správu večer.</i> Но для собственной нейтральной фразы безопасно начать с модели <b>A + D</b>.", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    PageBreak(),

    p("3. Клитики: короткий известный адресат", H1),
    p("Клитики - короткие безударные формы. Они не любят стоять в самом начале нейтрального предложения и обычно занимают раннюю позицию после первого смыслового элемента."),
    table([
        ["Лицо", "D: кому?", "A: кого/что?", "Пример"],
        ["я", "mi", "ma", "Pošleš mi adresu?"],
        ["ты", "ti", "ťa", "Napíšem ti večer."],
        ["он", "mu", "ho", "Pošlem mu správu."],
        ["она", "jej", "ju", "Zavolám jej zajtra."],
        ["мы", "nám", "nás", "Pošlite nám potvrdenie."],
        ["вы", "vám", "vás", "Napíšem vám podrobnosti."],
        ["они", "im", "ich", "Odpovieme im ráno."],
    ], [25 * mm, 30 * mm, 37 * mm, 78 * mm], 5.55),
    p("Когда две клитики встречаются", H2),
    p("Если и адресат, и предмет выражены короткими формами, дательный обычно стоит перед аккузативом: <b>D + A</b>.", SMALL),
    table([
        ["Полная форма", "С клитиками", "Перевод"],
        ["Pošlem dokument Petrovi.", "Pošlem mu ho.", "Я отправлю ему его."],
        ["Dáš adresu mne?", "Dáš mi ju?", "Ты дашь мне её?"],
        ["Ukážte správu nám.", "Ukážte nám ju.", "Покажите нам её."],
    ], [58 * mm, 48 * mm, 64 * mm], 5.85),
    box("<b>Контраст:</b> полные новые дополнения часто идут A + D: <i>Pošlem dokument Petrovi.</i> Короткие известные формы образуют D + A: <i>Pošlem mu ho.</i>", PALE, ROSE, SMALL),
    p("В вежливой переписке часто пишут <i>Vám, Vás, Váš</i> с прописной буквы. Это знак уважения, а не отдельная грамматическая форма.", SMALL),
    PageBreak(),

    p("4. Неформально и формально", H1),
    p("Обращение, просьба и завершение должны быть в одном регистре. Не смешивайте <i>Ahoj</i> с официальным <i>Vám</i> без причины."),
    table([
        ["Часть", "Неформально", "Формально / нейтрально"],
        ["обращение", "Ahoj, Katka,", "Dobrý deň, pani Nováková,"],
        ["цель", "Píšem ti kvôli oslave.", "Píšem Vám ohľadom faktúry."],
        ["просьба", "Pošli mi, prosím, adresu.", "Prosím, pošlite mi potvrdenie."],
        ["вопрос", "Môžeš mi zavolať?", "Mohli by ste mi zavolať?"],
        ["завершение", "Maj sa pekne!", "Ďakujem a prajem pekný deň."],
        ["подпись", "Ari", "S pozdravom<br/>Ari Frost"],
    ], [32 * mm, 66 * mm, 72 * mm], 5.55),
    p("Структура электронного письма. Три готовые модели", H2),
    box("<b>Голосовое:</b> Dobrý deň, tu je Martin Bielik. Volám ohľadom zajtrajšej opravy. Technik môže prísť medzi deviatou a desiatou. Prosím, zavolajte mi späť na číslo 0900 123 456 a potvrďte mi čas. Ďakujem, dovidenia.", PALE, ROSE, TINY, 5),
    box("<b>Личное:</b> Ahoj, Lucia! Píšem ti kvôli sobotnému výletu. Pošlem ti večer presnú adresu. Môžeš mi, prosím, napísať, či pôjdeš autom? Ak áno, pošlem ti aj mapu. Maj sa pekne! Ari", PALE, ROSE, TINY, 5),
    box("<b>Predmet: Zmena termínu konzultácie</b><br/>Dobrý deň, pani Králová,<br/>píšem Vám ohľadom utorkovej konzultácie. V utorok sa, žiaľ, nemôžem zúčastniť. Mohli by ste mi navrhnúť nový termín vo štvrtok alebo v piatok? Potvrdenie pošlem aj kolegovi.<br/>Ďakujem Vám za odpoveď. S pozdravom, Ari Frost", PALE, ROSE, TINY, 5),
    box("<b>Пунктуация:</b> после обращения ставится запятая, а следующий абзац обычно начинается со строчной буквы: <i>Dobrý deň, pani Nováková,<br/>píšem Vám...</i>", CREAM, colors.HexColor("#E7C76C"), TINY, 5),
    PageBreak(),

    p("5. Частые ошибки и упражнения", H1),
    box("<b>Частые ошибки:</b> адресат без дательного; клитика в самом начале; порядок A + D механически переносится на две клитики; смешаны ty и Vy; нет предмета письма, причины или следующего шага.", CREAM, colors.HexColor("#E7C76C"), TINY),
    p("Упражнение 1. Поставьте адресата в D", H2),
    p("1) Napíšem (kolega) e-mail. 2) Pošleme správu (rodičia). 3) Zavolám (kamarátka). 4) Odpoviete (klientka)?", TINY),
    p("Упражнение 2. Соберите A + D", H2),
    p("1) pošlem / potvrdenie / vedúci; 2) napíšeme / krátky e-mail / zákazníci; 3) ukážte / nová ponuka / kolegyňa.", TINY),
    p("Упражнение 3. Замените выделенные части клитиками", H2),
    p("1) Pošlem dokument Petrovi. 2) Dáš adresu mne? 3) Ukážte správu nám. 4) Zavolám pani Horváthovej zajtra. Замените адресата; где возможно, замените и предмет.", TINY),
    p("Упражнение 4. Выберите подходящий регистр", H2),
    p("Письмо клиентке: 1) Ahoj / Dobrý deň; 2) píšem ti / píšem Vám; 3) pošli mi / pošlite mi; 4) Maj sa / S pozdravom.", TINY),
    p("Упражнение 5. Восстановите голосовое сообщение", H2),
    p("Расставьте: a) Prosím, zavolajte mi späť. b) Tu je Elena Malá. c) Ďakujem, dovidenia. d) Volám ohľadom objednávky. Добавьте одну конкретную информацию.", TINY),
    p("Упражнение 6. Напишите письмо", H2),
    p("Напишите рабочее письмо из 6-8 строк: попросите перенести встречу, предложите два срока и попросите подтверждение. Используйте предмет, формальное обращение, одну модель A + D и две клитики.", TINY),
    PageBreak(),

    p("6. Ответы и итоговая проверка", H1),
    p("Ответы", H2),
    p("<b>1.</b> 1) kolegovi; 2) rodičom; 3) kamarátke; 4) klientke.", TINY),
    p("<b>2.</b> 1) Pošlem potvrdenie vedúcemu. 2) Napíšeme krátky e-mail zákazníkom. 3) Ukážte novú ponuku kolegyni.", TINY),
    p("<b>3.</b> 1) Pošlem mu ho. 2) Dáš mi ju? 3) Ukážte nám ju. 4) Zavolám jej zajtra. В 4 предмета нет, поэтому заменяем только адресата.", TINY),
    p("<b>4.</b> Dobrý deň; píšem Vám; pošlite mi; S pozdravom.", TINY),
    p("<b>5.</b> Tu je Elena Malá. Volám ohľadom objednávky. Objednávka príde v piatok dopoludnia. Prosím, zavolajte mi späť. Ďakujem, dovidenia. Конкретная информация может быть другой.", TINY),
    p("<b>6. Модель:</b><br/><b>Predmet: Prosba o zmenu termínu</b><br/>Dobrý deň, pán Novák,<br/>píšem Vám ohľadom nášho stretnutia. Mohli by ste mi, prosím, navrhnutý termín zmeniť? Vyhovoval by mi štvrtok o desiatej alebo piatok o druhej. Pošlem potvrdenie aj kolegyni a potom Vám ho prepošlem. Prosím, napíšte mi, ktorý termín Vám vyhovuje.<br/>Ďakujem. S pozdravom, Ari Frost", TINY),
    p("Итог в четырёх пунктах", H2),
    table([
        ["OK", "Называю себя, причину и следующий шаг."],
        ["OK", "Ставлю адресата после komu? в дательный."],
        ["OK", "Различаю полное A + D и клитическое D + A."],
        ["OK", "Сохраняю единый неформальный или формальный тон."],
    ], [12 * mm, 158 * mm], 6.0, False),
    p("Следующий шаг: в теме 6.6 вы будете говорить об онлайн-привычках, давать совет и решать простую проблему со входом.", SMALL),
]

doc.build(story)
print(OUTPUT)
