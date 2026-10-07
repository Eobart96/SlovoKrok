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
OUTPUT = ROOT / "output" / "pdf" / "A2" / "Module_03" / "Slovak_A2_Tema_3_6_Prityazhatelnye_slova_i_svoj.pdf"
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
        canvas.drawString(20 * mm, height - 12 * mm, "A2 3.6  |  Притяжательные слова и местоимение svoj")
    canvas.setFont("Arial", 8)
    canvas.setFillColor(MUTED)
    canvas.drawString(20 * mm, 9 * mm, "SlovoKrok | личный учебный модуль")
    canvas.drawRightString(width - 20 * mm, 9 * mm, f"стр. {page} / 7")
    canvas.restoreState()


doc = BaseDocTemplate(
    str(OUTPUT), pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=20 * mm, bottomMargin=18 * mm,
    title="Slovak A2 - Тема 3.6 - Притяжательные слова и местоимение svoj", author="SlovoKrok",
)
frame = Frame(20 * mm, 18 * mm, 170 * mm, 257 * mm, id="main", leftPadding=0, rightPadding=0)
doc.addPageTemplates([PageTemplate(id="series", frames=[frame], onPage=draw_page)])

story = [
    p("МОДУЛЬ 3  •  ПРИЛАГАТЕЛЬНЫЕ, МЕСТОИМЕНИЯ И ЧИСЛИТЕЛЬНЫЕ", COVER_KICKER),
    p("Притяжательные слова<br/>и местоимение svoj", TITLE),
    p("Privlastňovacie zámená a zámeno svoj", SUBTITLE),
    Spacer(1, 31 * mm),
    p("Словацкое <b>svoj</b> связывает владельца с субъектом действия. Поэтому русское свой и обычные мой, твой, его не всегда переводятся буквально: сначала надо понять, кто действует и кому принадлежит предмет.", BODY),
    p("После модуля вы сможете:", H2),
    styled_table([
        ["1", "выбирать môj/tvoj/jeho/jej/náš/váš/ich по владельцу"],
        ["2", "использовать svoj, когда владелец совпадает с субъектом"],
        ["3", "отличать Peter hľadá svoj telefón от Peter hľadá jeho telefón"],
        ["4", "согласовывать изменяемое притяжательное слово с предметом"],
    ], [12 * mm, 158 * mm], font_size=7.25, header=False),
    Spacer(1, 3 * mm),
    box("<b>Главный вопрос:</b> владелец и субъект действия - одно лицо? Да -> обычно <b>svoj</b>. Нет -> <b>môj, tvoj, jeho, jej, náš, váš, ich</b>.", PALE, PINK),
    PageBreak(),

    p("1. Кто владелец?", H1),
    p("Притяжательное слово отвечает на <b>čí? čia? čie?</b> и стоит при названии предмета или человека. Выбор основы зависит от владельца, а форма - от существительного.", BODY),
    styled_table([
        ["Владелец", "Слово", "Пример"],
        ["ja", "môj", "môj plán, moja izba, moje auto"],
        ["ty", "tvoj", "tvoj brat, tvoja práca, tvoje miesto"],
        ["on / ono", "jeho", "jeho pas, jeho rodina, jeho veci"],
        ["ona", "jej", "jej telefón, jej adresa, jej deti"],
        ["my", "náš", "náš dom, naša škola, naše mesto"],
        ["vy", "váš", "váš účet, vaša otázka, vaše doklady"],
        ["oni / ony", "ich", "ich byt, ich dcéra, ich fotografie"],
    ], [31 * mm, 30 * mm, 109 * mm], font_size=6.35),
    p("Что изменяется", H2),
    styled_table([
        ["Изменяются", "Не изменяются"],
        ["môj, tvoj, náš, váš, svoj", "jeho, jej, ich"],
        ["o mojej práci; s našimi deťmi", "o jej práci; s ich deťmi"],
    ], [85 * mm, 85 * mm], font_size=6.7),
    box("<b>Важно:</b> в сочетании <b>s jej novou kolegyňou</b> форма <b>jej</b> остаётся той же, а <b>novou kolegyňou</b> получает Instrumentál.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    PageBreak(),

    p("2. Svoj: владелец совпадает с субъектом", H1),
    p("В нейтральной словацкой речи <b>svoj</b> относится к любой грамматической личности, если именно субъект является владельцем. Оно заменяет и môj, и tvoj, и его аналоги.", BODY),
    styled_table([
        ["Субъект", "Нейтральная модель", "Перевод"],
        ["ja", "Kontrolujem svoju rezerváciu.", "Я проверяю своё бронирование."],
        ["ty", "Vezmi si svoj pas.", "Возьми свой паспорт."],
        ["on", "Peter hľadá svoj telefón.", "Петер ищет свой телефон."],
        ["ona", "Eva volá svojej sestre.", "Ева звонит своей сестре."],
        ["my", "Chránime svoje údaje.", "Мы защищаем свои данные."],
        ["vy", "Skontrolujte svoju adresu.", "Проверьте свой адрес."],
        ["oni", "Deti upratali svoju izbu.", "Дети убрали свою комнату."],
    ], [25 * mm, 78 * mm, 67 * mm], font_size=6.25),
    p("Svoj или jeho/jej/ich?", H2),
    styled_table([
        ["Фраза", "Кому принадлежит предмет"],
        ["Peter hľadá <b>svoj</b> telefón.", "Петеру: владелец = субъект Peter"],
        ["Peter hľadá <b>jeho</b> telefón.", "другому мужчине, известному из контекста"],
        ["Anna číta <b>svoj</b> list.", "Анне: она читает своё письмо"],
        ["Anna číta <b>jej</b> list.", "другой женщине: Анна читает её письмо"],
    ], [79 * mm, 91 * mm], font_size=6.45),
    box("<b>Не ищите только слово он или она.</b> Найдите грамматический субъект всего действия. Именно с ним сравнивается владелец.", PALE, ROSE, SMALL),
    PageBreak(),

    p("3. Когда svoj не подходит", H1),
    p("Если владелец не является субъектом действия, используйте личное притяжательное слово. В именной части предложения и в группе подлежащего также называйте владельца прямо.", BODY),
    styled_table([
        ["Ситуация", "Пример и перевод"],
        ["Владелец не субъект", "Ukážem Eve <b>jej</b> izbu. - Я покажу Еве её комнату."],
        ["Предмет принадлежит собеседнику", "Mám <b>tvoje</b> kľúče. - У меня твои ключи."],
        ["Именная часть", "To je <b>môj</b> byt. - Это моя квартира."],
        ["Группа подлежащего", "<b>Jeho</b> brat pracuje doma. - Его брат работает дома."],
        ["Общий владелец не только субъект", "Naša krajina je krásna. - Наша страна красива."],
    ], [55 * mm, 115 * mm], font_size=6.45),
    p("Форма согласуется с предметом, не с владельцем", H2),
    styled_table([
        ["Предмет", "Форма", "Пример"],
        ["мужской род", "svoj / môj / náš", "svoj doklad, môj kurz, náš sused"],
        ["женский род", "svoja / moja / naša", "svoja taška, moja práca, naša ulica"],
        ["средний род", "svoje / moje / naše", "svoje heslo, moje auto, naše mesto"],
        ["мн. ч., лица м. рода", "svoji / moji / naši", "svoji kolegovia, moji bratia, naši hostia"],
        ["остальное мн. число", "svoje / moje / naše", "svoje veci, moje deti, naše otázky"],
    ], [40 * mm, 49 * mm, 81 * mm], font_size=6.35),
    box("<b>Русская ловушка:</b> словацкое <b>svoj</b> часто обязательно и при 1-м и 2-м лице: <b>Ja poznám svoju adresu. Ty poznáš svoju adresu.</b>", CREAM, colors.HexColor("#E7C76C"), SMALL),
    PageBreak(),

    p("4. Согласование во всех нужных формах", H1),
    p("Модели <b>môj, tvoj, svoj</b> изменяются одинаково. Ниже - форма <b>svoj</b>; подставляйте нужную основу. <b>Náš</b> и <b>váš</b> выражают те же категории: nášho, našej, našimi; vášho, vašej, vašimi.", BODY),
    styled_table([
        ["Падеж", "м. род", "ж. род", "ср. род"],
        ["N", "svoj", "svoja", "svoje"],
        ["G", "svojho", "svojej", "svojho"],
        ["D", "svojmu", "svojej", "svojmu"],
        ["A", "svojho (лицо) / svoj (предмет)", "svoju", "svoje"],
        ["L", "svojom", "svojej", "svojom"],
        ["I", "svojím", "svojou", "svojím"],
    ], [24 * mm, 58 * mm, 44 * mm, 44 * mm], font_size=6.45),
    p("Множественное число", H2),
    styled_table([
        ["Падеж", "лица м. рода", "остальные"],
        ["N", "svoji kolegovia", "svoje knihy / mestá"],
        ["G", "svojich kolegov", "svojich kníh / miest"],
        ["D", "svojim kolegom", "svojim knihám / mestám"],
        ["A", "svojich kolegov", "svoje knihy / mestá"],
        ["L", "o svojich kolegoch", "o svojich knihách / mestách"],
        ["I", "so svojimi kolegami", "so svojimi knihami / mestami"],
    ], [26 * mm, 72 * mm, 72 * mm], font_size=6.25),
    box("<b>Проверяйте два шага:</b> 1) кто владелец - выбор svoj или личного слова; 2) какой предмет и падеж - окончание изменяемого слова.", PALE, PINK, SMALL),
    PageBreak(),

    p("5. Живые модели и упражнения", H1),
    styled_table([
        ["SK", "RU"],
        ["Môj kolega pozná tvoju sestru.", "Мой коллега знает твою сестру."],
        ["Jej syn študuje v našom meste.", "Её сын учится в нашем городе."],
        ["Ich deti sa hrajú s našimi deťmi.", "Их дети играют с нашими детьми."],
        ["Pošlem vám našu novú adresu.", "Я пришлю вам наш новый адрес."],
        ["Eva si zapisuje svoje heslo.", "Ева записывает свой пароль."],
        ["O svojom pláne zatiaľ nehovorím.", "О своём плане я пока не говорю."],
        ["Peter cestuje so svojou dcérou.", "Петер путешествует со своей дочерью."],
        ["Stretli sme sa s jeho kolegami.", "Мы встретились с его коллегами."],
    ], [86 * mm, 84 * mm], font_size=5.95),
    p("Мини-диалог", H2),
    box("<b>A:</b> Máš <b>svoj</b> pas? - У тебя есть свой паспорт?<br/><b>B:</b> Áno, ale neviem nájsť <b>svoje</b> lístky. - Да, но я не могу найти свои билеты.<br/><b>A:</b> Nie sú v <b>tvojej</b> taške? - Они не в твоей сумке?<br/><b>B:</b> Nie. Jana má <b>moju</b> tašku a ja mám <b>jej</b> kufor. - Нет. У Яны моя сумка, а у меня её чемодан.<br/><b>A:</b> Zavolaj jej. Možno dala lístky do <b>svojho</b> kufra. - Позвони ей. Возможно, она положила билеты в свой чемодан.", PALE, ROSE, TINY),
    box("<b>Частые ошибки:</b> *Peter hľadá jeho telefón (свой) -> <b>svoj telefón</b>; *s jejou sestrou -> <b>s jej sestrou</b>; *ichom autom -> <b>ich autom</b>; *svoj brat prišiel -> <b>môj/jeho brat prišiel</b>.", CREAM, colors.HexColor("#E7C76C"), TINY),
    p("Упражнения 1-3", H2),
    p("<b>1.</b> Выберите: Peter predal svoj / jeho byt (квартира Петера). Anna číta svoj / jej list (письмо другой женщины). To je svoj / môj pas.<br/><b>2.</b> Вставьте: ja -> ___ plán; ona -> ___ rodina; my -> ___ mesto; oni -> ___ deti.<br/><b>3.</b> Согласуйте svoj: o ___ práci; so ___ bratom; pre ___ deti; k ___ rodičom; v ___ aute.", TINY),
    p("Упражнения 4-6", H2),
    p("<b>4.</b> Исправьте: Eva volá jej mame (своей). Ideme s ichými priateľmi. Môj sestra pracuje doma.<br/><b>5.</b> Переведите: Я проверяю свой адрес. У нас её документы. Они говорят о своих детях.<br/><b>6.</b> Напишите 5-7 фраз о поездке: чьи документы, сумка, билеты и чемодан; кто проверяет свои вещи и кто несёт чужие.", TINY),
    PageBreak(),

    p("6. Ответы и проверка мастерства", H1),
    p("Ответы", H2),
    p("<b>1.</b> Peter predal svoj byt. Anna číta jej list. To je môj pas.", TINY),
    p("<b>2.</b> môj plán; jej rodina; naše mesto; ich deti.", TINY),
    p("<b>3.</b> o svojej práci; so svojím bratom; pre svoje deti; k svojim rodičom; vo svojom aute.", TINY),
    p("<b>4.</b> Eva volá svojej mame. Ideme s ich priateľmi. Moja sestra pracuje doma.", TINY),
    p("<b>5.</b> Kontrolujem svoju adresu. Máme jej doklady. Hovoria o svojich deťoch.", TINY),
    p("<b>6. Модель:</b> Pred cestou kontrolujem svoje doklady. Môj pas je v mojej taške. Jana hľadá svoje lístky. Ja mám jej malý kufor. Ona nesie moju tašku. Naši priatelia už čakajú pri svojom aute. Возможны другие естественные варианты.", TINY),
    p("Итог в четырёх пунктах", H2),
    styled_table([
        ["OK", "Выбираю môj/tvoj/jeho/jej/náš/váš/ich по владельцу."],
        ["OK", "Использую svoj, когда владелец является субъектом действия."],
        ["OK", "Не изменяю jeho/jej/ich, но согласую môj/tvoj/náš/váš/svoj."],
        ["OK", "Различаю svoj telefón субъекта и jeho telefón другого мужчины."],
    ], [12 * mm, 158 * mm], font_size=6.65, header=False),
    Spacer(1, 2 * mm),
    box("<b>Финальная проверка:</b> без таблицы опишите три предмета: свой, предмет собеседника и предмет третьего лица. Затем поставьте каждое сочетание после предлога.", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    p("Следующий шаг", H2),
    p("В теме 3.7 вы изучите отдельные прилагательные индивидуальной принадлежности, образованные от названий людей.", SMALL),
]

doc.build(story)
print(OUTPUT)
