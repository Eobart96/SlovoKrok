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
OUTPUT = ROOT / "output/pdf/A2/Module_08/Slovak_A2_Tema_8_6_Integrirovannaya_zadacha_reshaem_problemu.pdf"
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
BODY = ParagraphStyle("Body", fontName="Arial", fontSize=8.45, leading=11.0, textColor=INK, spaceAfter=2.4 * mm)
SMALL = ParagraphStyle("Small", parent=BODY, fontSize=7.25, leading=8.9, spaceAfter=1.15 * mm)
TINY = ParagraphStyle("Tiny", parent=BODY, fontSize=6.45, leading=7.7, spaceAfter=0.7 * mm)
TITLE = ParagraphStyle("Title", fontName="Arial-Bold", fontSize=18.0, leading=21.3, textColor=colors.white, alignment=TA_LEFT, spaceAfter=4.5 * mm)
SUBTITLE = ParagraphStyle("Subtitle", fontName="Arial", fontSize=10.8, leading=14.0, textColor=colors.HexColor("#FFD8EB"), spaceAfter=4 * mm)
H1 = ParagraphStyle("H1", fontName="Arial-Bold", fontSize=15.0, leading=17.8, textColor=PLUM, spaceBefore=0.8 * mm, spaceAfter=2.7 * mm)
H2 = ParagraphStyle("H2", fontName="Arial-Bold", fontSize=10.3, leading=12.6, textColor=PINK, spaceBefore=0.8 * mm, spaceAfter=1.2 * mm)
KICK = ParagraphStyle("Kicker", fontName="Arial-Bold", fontSize=9.7, leading=11.7, textColor=colors.HexColor("#FFD8EB"), spaceAfter=3.5 * mm)


def p(text, style=BODY):
    return Paragraph(text, style)


def box(text, bg=PALE, border=ROSE, style=BODY, pad=7):
    item = Table([[p(text, style)]], colWidths=[170 * mm])
    item.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg), ("BOX", (0, 0), (-1, -1), 0.7, border),
        ("LEFTPADDING", (0, 0), (-1, -1), pad), ("RIGHTPADDING", (0, 0), (-1, -1), pad),
        ("TOPPADDING", (0, 0), (-1, -1), pad), ("BOTTOMPADDING", (0, 0), (-1, -1), pad),
    ]))
    return item


def table(data, widths, size=7.0, header=True):
    rows = []
    for row_index, row in enumerate(data):
        cell_style = ParagraphStyle(
            f"cell_{row_index}_{size}_{len(data)}", parent=SMALL, fontSize=size, leading=size + 1.6,
            textColor=colors.white if header and row_index == 0 else INK,
            fontName="Arial-Bold" if header and row_index == 0 else "Arial", spaceAfter=0,
        )
        rows.append([p(str(value), cell_style) for value in row])
    item = Table(rows, colWidths=widths, repeatRows=1 if header else 0)
    commands = [
        ("GRID", (0, 0), (-1, -1), 0.45, ROSE), ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
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
        canvas.drawString(20 * mm, height - 12 * mm, "A2 8.6  |  Интегрированная задача: решаем проблему")
    canvas.setFont("Arial", 8)
    canvas.setFillColor(MUTED)
    canvas.drawString(20 * mm, 9 * mm, "SlovoKrok | личный учебный модуль")
    canvas.drawRightString(width - 20 * mm, 9 * mm, f"стр. {page_number} / 7")
    canvas.restoreState()


doc = BaseDocTemplate(
    str(OUTPUT), pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=20 * mm, bottomMargin=18 * mm,
    title="Slovak A2 - Тема 8.6 - Интегрированная задача: решаем проблему", author="SlovoKrok",
)
doc.addPageTemplates([PageTemplate(
    id="series", frames=[Frame(20 * mm, 18 * mm, 170 * mm, 257 * mm, id="main", leftPadding=0, rightPadding=0)], onPage=draw_page,
)])


story = [
    p("МОДУЛЬ 8  •  ОТНОШЕНИЯ, ЗДОРОВЬЕ И ИТОГ A2", KICK),
    p("Интегрированная задача:<br/>решаем проблему", TITLE),
    p("Rozumieme, spresníme, dohodneme sa a odovzdáme riešenie", SUBTITLE),
    Spacer(1, 39 * mm),
    p("В реальной ситуации отдельные правила работают вместе. Нужно понять сообщение, выбрать важные факты, вежливо уточнить недостающее, договориться и кратко пересказать решение человеку, который не участвовал в разговоре."),
    p("После модуля вы сможете:", H2),
    table([
        ["1", "извлечь из объявления кто, что, где, когда и при каком условии"],
        ["2", "задать точные вежливые вопросы без повторения всего текста"],
        ["3", "предложить вариант и явно подтвердить договорённость"],
        ["4", "передать третьему лицу факты, просьбу и итоговое решение"],
    ], [12 * mm, 158 * mm], 6.8, False),
    Spacer(1, 3 * mm),
    box("<b>Рабочая цепочка:</b> прочитать -> выделить пробел -> уточнить -> предложить -> подтвердить -> передать решение."),
    PageBreak(),

    p("1. Ситуация и исходное сообщение", H1),
    p("Вы живёте в квартире 14 и во вторник работаете до 12:00. В доме запланирован ремонт стояка. Нужно организовать доступ для техника и сообщить решение человеку, с которым вы живёте."),
    p("OZNAM SPRÁVCU DOMU", H2),
    box("V utorok 14. októbra od 8.00 do 13.00 nebude v dome tiecť voda. Dôvodom je oprava stúpačky na štvrtom poschodí. Technik potrebuje vstúpiť do bytov 12 až 16 medzi 9.00 a 11.00. Ak nemôžete byť doma, môžete odovzdať kľúč správcovi najneskôr v pondelok do 18.00. Po oprave nechajte vodu niekoľko minút odtiecť. Otázky: 0900 123 456.", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    p("Читаем по пяти опорам", H2),
    table([
        ["Опора", "Факт из сообщения", "Зачем он нужен"],
        ["čo", "oprava stúpačky", "понять причину"],
        ["kedy", "v utorok od 8.00 do 13.00", "подготовиться без воды"],
        ["kde", "byty 12 až 16", "проверить, касается ли вас"],
        ["kto", "technik a správca", "понять роли"],
        ["podmienka", "ak nemôžete byť doma", "выбрать другой способ доступа"],
        ["termín", "do pondelka do 18.00", "не пропустить срок"],
    ], [25 * mm, 68 * mm, 77 * mm], 5.05),
    p("Что известно, а чего не хватает", H2),
    table([
        ["Известно", "Нужно уточнить"],
        ["Technik príde medzi deviatou a jedenástou.", "Musí byť majiteľ bytu osobne doma?"],
        ["Kľúč možno odovzdať správcovi.", "Môže technikovi otvoriť suseda?"],
        ["Voda nepotečie päť hodín.", "Dostaneme správu, keď bude oprava hotová?"],
    ], [84 * mm, 86 * mm], 5.25),
    box("Не пересказывайте объявление целиком. Сначала отметьте факты, затем спросите только то, без чего нельзя принять решение.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    PageBreak(),

    p("2. Уточняем детали", H1),
    p("Вежливый вопрос начинается с короткой рамки. Она показывает, что вы уже поняли основное и уточняете один конкретный пробел."),
    table([
        ["Функция", "Словацкая формула", "Перевод"],
        ["проверить понимание", "Rozumiem správne, že technik príde doobeda?", "Я правильно понимаю, что техник придёт до обеда?"],
        ["уточнить возможность", "Je možné, aby technikovi otvorila suseda?", "Может ли соседка открыть технику?"],
        ["уточнить обязанность", "Musím byť osobne doma?", "Я должен лично быть дома?"],
        ["попросить подтверждение", "Mohli by ste mi potvrdiť čas návštevy?", "Не могли бы вы подтвердить время визита?"],
        ["спросить о следующем шаге", "Komu mám odovzdať kľúč?", "Кому мне передать ключ?"],
        ["спросить об условии", "Čo mám urobiť, ak sa termín zmení?", "Что делать, если время изменится?"],
    ], [40 * mm, 78 * mm, 52 * mm], 4.85),
    p("Мини-диалог с управляющим", H2),
    box("<b>Obyvateľ:</b> Dobrý deň, volám kvôli utorkovej oprave vody. Rozumiem správne, že technik potrebuje vstúpiť aj do bytu 14?<br/><b>Správca:</b> Áno, potrebuje skontrolovať potrubie v kúpeľni.<br/><b>Obyvateľ:</b> Do dvanástej som v práci. Je možné, aby mu otvorila moja suseda Marta?<br/><b>Správca:</b> Áno, ak bude v byte medzi desiatou a jedenástou.<br/><b>Obyvateľ:</b> Mohli by ste mi, prosím, poslať správu, keď technik príde?<br/><b>Správca:</b> Samozrejme. Pošlem vám správu desať minút vopred.", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    p("Короткие реакции", H2),
    table([
        ["Rozumiem.", "Понимаю."], ["To mi vyhovuje.", "Мне это подходит."],
        ["To mi, žiaľ, nevyhovuje.", "К сожалению, мне это не подходит."],
        ["Potrebujem si to ešte overiť.", "Мне нужно это ещё проверить."],
    ], [92 * mm, 78 * mm], 5.4, False),
    PageBreak(),

    p("3. Предлагаем и подтверждаем решение", H1),
    p("Договорённость должна содержать действие, исполнителя и время. После обсуждения полезно произнести итог отдельной фразой, чтобы обе стороны поняли его одинаково."),
    table([
        ["Шаг", "Формула", "Пример"],
        ["предложить", "Navrhujem, aby...", "Navrhujem, aby technikovi otvorila Marta."],
        ["дать альтернативу", "Ak to nebude možné...", "Ak to nebude možné, odovzdám kľúč správcovi."],
        ["принять", "Dobre, to mi vyhovuje.", "Dobre, čas medzi desiatou a jedenástou mi vyhovuje."],
        ["зафиксировать", "Dohodnime sa teda, že...", "Dohodnime sa teda, že správca zavolá Marte."],
        ["подтвердить", "Platí, že...", "Platí, že technik príde najskôr o desiatej."],
    ], [31 * mm, 56 * mm, 83 * mm], 4.95),
    p("Грамматика в одной цепочке", H2),
    table([
        ["Что соединяем", "Пример", "Роль"],
        ["падежи", "Správca pošle Marte správu o návšteve.", "кому + что + о чём"],
        ["прошедшее", "Včera som zavolal správcovi.", "что уже сделал"],
        ["будущее", "Marta otvorí technikovi dvere.", "что произойдёт"],
        ["вид", "Správca bude čakať. Potom zavolá.", "процесс и результат"],
        ["условие", "Ak sa čas zmení, správca mi zavolá.", "запасной сценарий"],
        ["время", "Keď opravu dokončia, pošlú správu.", "ожидаемое событие"],
        ["вежливость", "Mohli by ste zavolať aj susede?", "мягкая просьба"],
    ], [35 * mm, 77 * mm, 58 * mm], 4.85),
    p("Итог договорённости", H2),
    box("Dohodli sme sa, že technik príde do bytu 14 medzi desiatou a jedenástou. Otvorí mu suseda Marta. Správca jej desať minút vopred zavolá. Ak Marta nebude môcť prísť, odovzdám kľúč správcovi ešte v pondelok.", PALE, ROSE, SMALL),
    box("Проверка качества: понятно ли, кто действует, что делает, когда и что произойдёт при изменении условий?", CREAM, colors.HexColor("#E7C76C"), SMALL),
    PageBreak(),

    p("4. Передаём решение третьему лицу", H1),
    p("Медиация не требует дословного перевода. Сохраните только факты, просьбу и итог. Используйте <i>že</i> для сообщения и <i>aby</i> для просьбы или требуемого действия."),
    table([
        ["Исходная реплика", "Передача третьему лицу"],
        ["Technik príde medzi desiatou a jedenástou.", "Správca povedal, že technik príde medzi desiatou a jedenástou."],
        ["Buďte v byte o desiatej.", "Správca požiadal Martu, aby bola v byte o desiatej."],
        ["Zavolám desať minút vopred.", "Správca sľúbil, že zavolá desať minút vopred."],
        ["Ak sa čas zmení, dám vám vedieť.", "Povedal, že nám dá vedieť, ak sa čas zmení."],
    ], [78 * mm, 92 * mm], 4.9),
    p("Сообщение человеку, который живёт с вами", H2),
    box("Ahoj, volal som správcovi kvôli oprave vody. Potvrdil, že technik potrebuje vstúpiť aj do nášho bytu. Dohodli sme sa, že mu medzi desiatou a jedenástou otvorí Marta. Správca jej pred návštevou zavolá. Ak Marta nebude môcť prísť, ešte v pondelok odovzdám kľúč správcovi. V utorok od ôsmej do jednej nepotečie voda, preto si ráno pripravíme zásobu.", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    p("Банк фраз для всей цепочки", H2),
    table([
        ["Приём", "Фраза"],
        ["назвать источник", "V ozname sa píše, že..."],
        ["выделить главное", "Najdôležitejšie je, že..."],
        ["обозначить пробел", "Nie je však jasné, či..."],
        ["уточнить", "Chcel by som sa opýtať, či..."],
        ["предложить", "Navrhujem, aby..."],
        ["подтвердить", "Dohodli sme sa, že..."],
        ["передать просьбу", "Požiadal ma, aby som..."],
        ["передать условие", "Ak sa niečo zmení, dajú nám vedieť."],
    ], [50 * mm, 120 * mm], 5.0),
    box("Не добавляйте факты, которых не было в источнике или разговоре. Если деталь не подтверждена, скажите: <i>Zatiaľ neviem, či...</i>", CREAM, colors.HexColor("#E7C76C"), SMALL),
    PageBreak(),

    p("5. Частые ошибки и упражнения", H1),
    table([
        ["Ошибка", "Правильно", "Почему"],
        ["*Rozumiem dobre, technik príde?", "Rozumiem správne, že technik príde?", "рамка + že"],
        ["*Otvorí technik suseda.", "Suseda otvorí technikovi.", "кому = D"],
        ["*Dohodli sme, že...", "Dohodli sme sa, že...", "нужно sa"],
        ["*Povedal, aby príde.", "Povedal, že príde.", "факт = že"],
        ["*Požiadal, že otvorím.", "Požiadal ma, aby som otvoril.", "просьба = aby"],
    ], [55 * mm, 66 * mm, 49 * mm], 4.7),
    p("Упражнение 1. Извлеките факты", H2),
    p("По объявлению запишите: 1) день и время отключения 2) номера квартир 3) время визита техника 4) крайний срок передачи ключа.", SMALL),
    p("Упражнение 2. Выберите точный вопрос", H2),
    p("Нужно узнать, может ли соседка открыть дверь: a) Kedy tečie voda? b) Je možné, aby technikovi otvorila suseda? c) Kde je správca?", SMALL),
    p("Упражнение 3. Вставьте форму", H2),
    p("1) Správca pošle ___ (Marta) správu. 2) Suseda otvorí ___ (technik). 3) Zavolal som ___ (správca). 4) Technik vstúpi do ___ (byt 14).", SMALL),
    p("Упражнение 4. Соедините договорённость", H2),
    p("Используйте že / aby / ak / keď: 1) Dohodli sme sa, ___ Marta otvorí. 2) Správca ju požiadal, ___ bola doma. 3) ___ sa čas zmení, zavolá. 4) ___ opravu dokončia, pošlú správu.", SMALL),
    p("Упражнение 5. Передайте третьему лицу", H2),
    p("Преобразуйте: 1) Správca: Technik príde o desiatej. 2) Správca Marte: Buďte doma. 3) Správca: Zavolám vopred.", SMALL),
    p("Упражнение 6. Решите похожую проблему", H2),
    p("Составьте цепочку из 7-8 предложений: важный факт из сообщения, один пробел, вежливый вопрос, предложение, подтверждение, условие и сообщение третьему лицу.", SMALL),
    PageBreak(),

    p("6. Ответы и итоговая цепочка", H1),
    p("Ответы", H2),
    table([
        ["№", "Ключ"],
        ["1", "1 v utorok od 8.00 do 13.00; 2 byty 12 až 16; 3 medzi 9.00 a 11.00; 4 v pondelok do 18.00."],
        ["2", "b) Je možné, aby technikovi otvorila suseda?"],
        ["3", "1 Marte; 2 technikovi; 3 správcovi; 4 bytu 14."],
        ["4", "1 že; 2 aby; 3 Ak; 4 Keď."],
        ["5", "1 Správca povedal, že technik príde o desiatej. 2 Správca požiadal Martu, aby bola doma. 3 Správca sľúbil, že zavolá vopred."],
        ["6", "Открытое задание: решение может отличаться, но должно содержать все семь функций."],
    ], [13 * mm, 157 * mm], 4.9),
    p("Модель полной цепочки", H2),
    box("V ozname sa píše, že v stredu nepôjde výťah a technik potrebuje vstúpiť do pivnice. Nie je však jasné, či musí byť prítomný aj majiteľ bytu. Zavolám preto správcovi a opýtam sa: Mohli by ste mi potvrdiť, kto musí prísť? Navrhnem, aby pivnicu otvoril sused, ktorý pracuje z domu. Dohodneme sa, že správca mu zavolá pol hodiny vopred. Ak sused nebude doma, prídem z práce skôr. Potom napíšem partnerke, že je prístup zabezpečený a čo urobíme pri zmene plánu.", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    p("Пять опор решения", H2),
    table([
        ["1", "Рецепция: выделите только факты, влияющие на действие."],
        ["2", "Взаимодействие: задайте один точный вопрос."],
        ["3", "Решение: назовите действие, исполнителя и время."],
        ["4", "Условие: добавьте запасной вариант с <i>ak</i>."],
        ["5", "Медиация: передайте источник, просьбу и итог без домыслов."],
    ], [11 * mm, 159 * mm], 5.3, False),
    p("Финальная проверка", H2),
    box("Возьмите любое короткое объявление. За две минуты назовите главные факты, сформулируйте уточнение, предложите действие, подтвердите договорённость и передайте решение третьему лицу. Если цепочка полная и понятная, цель 8.6 достигнута.", PALE, ROSE, SMALL),
]

doc.build(story)
print(OUTPUT)
