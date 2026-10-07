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
OUTPUT = ROOT / "output/pdf/A2/Module_08/Slovak_A2_Tema_8_5_Obraz_zhizni_i_sport.pdf"
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
TITLE = ParagraphStyle("Title", fontName="Arial-Bold", fontSize=20.5, leading=24.0, textColor=colors.white, alignment=TA_LEFT, spaceAfter=4.5 * mm)
SUBTITLE = ParagraphStyle("Subtitle", fontName="Arial", fontSize=11.2, leading=14.5, textColor=colors.HexColor("#FFD8EB"), spaceAfter=4 * mm)
H1 = ParagraphStyle("H1", fontName="Arial-Bold", fontSize=15.2, leading=18, textColor=PLUM, spaceBefore=0.8 * mm, spaceAfter=2.8 * mm)
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
        canvas.drawString(20 * mm, height - 12 * mm, "A2 8.5  |  Образ жизни и спорт")
    canvas.setFont("Arial", 8)
    canvas.setFillColor(MUTED)
    canvas.drawString(20 * mm, 9 * mm, "SlovoKrok | личный учебный модуль")
    canvas.drawRightString(width - 20 * mm, 9 * mm, f"стр. {page_number} / 7")
    canvas.restoreState()


doc = BaseDocTemplate(
    str(OUTPUT), pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=20 * mm, bottomMargin=18 * mm,
    title="Slovak A2 - Тема 8.5 - Образ жизни и спорт", author="SlovoKrok",
)
doc.addPageTemplates([PageTemplate(
    id="series", frames=[Frame(20 * mm, 18 * mm, 170 * mm, 257 * mm, id="main", leftPadding=0, rightPadding=0)], onPage=draw_page,
)])


story = [
    p("МОДУЛЬ 8  •  ОТНОШЕНИЯ, ЗДОРОВЬЕ И ИТОГ A2", KICK),
    p("Образ жизни и спорт", TITLE),
    p("Môj životný štýl: описываем привычки, сравниваем активности и строим реальный план", SUBTITLE),
    Spacer(1, 44 * mm),
    p("На уровне A2 полезно не просто перечислить занятия, а связно описать режим, сравнить прошлое и настоящее и предложить небольшое изменение, которое действительно можно выполнить."),
    p("После модуля вы сможете:", H2),
    table([
        ["1", "называть занятия через отглагольные существительные"],
        ["2", "сравнивать, как часто, быстро и регулярно вы что-то делаете"],
        ["3", "различать привычку и одно завершённое действие"],
        ["4", "давать мягкий совет через mal by som / mala by som"],
        ["5", "формулировать реальный план с ak и keď"],
    ], [12 * mm, 158 * mm], 6.8, False),
    Spacer(1, 3 * mm),
    box("<b>Формула ответа:</b> моя привычка -> сравнение -> что стоит изменить -> конкретный шаг -> запасной вариант при условии."),
    PageBreak(),

    p("1. Называем активности", H1),
    p("Отглагольное существительное превращает действие в название процесса: <i>cvičiť -> cvičenie</i>. Большинство таких слов среднего рода. Но не каждое полезное название строится механически: рядом существуют обычные слова <i>chôdza, jazda, spánok, odpočinok</i>."),
    table([
        ["Глагол или выражение", "Название активности", "Пример"],
        ["cvičiť", "cvičenie", "Pravidelné cvičenie mi pomáha."],
        ["behať", "behanie", "Počas behania sa rýchlo unavím."],
        ["plávať", "plávanie", "Na plávanie chodím dvakrát týždenne."],
        ["posilňovať", "posilňovanie", "Posilňovanie striedam s chôdzou."],
        ["stravovať sa", "stravovanie", "Zdravé stravovanie nie je len diéta."],
        ["chodiť", "chôdza", "Rýchla chôdza je môj obľúbený pohyb."],
        ["jazdiť na bicykli", "jazda na bicykli", "Jazda na bicykli ma baví."],
        ["spať", "spánok", "Dobrý spánok je pre mňa dôležitý."],
    ], [42 * mm, 44 * mm, 84 * mm], 4.85),
    p("Полезное управление", H2),
    table([
        ["Модель", "Пример", "Перевод"],
        ["čas na + A", "Večer mám čas na cvičenie.", "Вечером у меня есть время на тренировку."],
        ["počas + G", "Počas plávania pokojne dýcham.", "Во время плавания я спокойно дышу."],
        ["pred + I", "Pred spaním nepoužívam telefón.", "Перед сном я не пользуюсь телефоном."],
        ["po + L", "Po behaní sa vždy ponaťahujem.", "После бега я всегда растягиваюсь."],
    ], [35 * mm, 73 * mm, 62 * mm], 5.1),
    box("<b>Ловушка:</b> суффикс <i>-nie / -tie</i> часто помогает, но не гарантирует самое естественное слово. Для режима дня обычно лучше выучить пары: <i>chodiť - chôdza, spať - spánok, oddychovať - odpočinok</i>.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    PageBreak(),

    p("2. Сравниваем через наречия", H1),
    p("Прилагательное описывает предмет: <i>rýchly beh</i>. Наречие описывает действие: <i>bežím rýchlo</i>. Для сравнения нужен вопрос <i>ako?</i>: <i>rýchlejšie, pokojnejšie, pravidelnejšie</i>."),
    table([
        ["Обычная степень", "Сравнительная", "Превосходная"],
        ["rýchlo", "rýchlejšie", "najrýchlejšie"],
        ["pomaly", "pomalšie", "najpomalšie"],
        ["často", "častejšie", "najčastejšie"],
        ["pravidelne", "pravidelnejšie", "najpravidelnejšie"],
        ["zdravo", "zdravšie", "najzdravšie"],
        ["dobre", "lepšie", "najlepšie"],
        ["veľa", "viac", "najviac"],
        ["málo", "menej", "najmenej"],
    ], [58 * mm, 56 * mm, 56 * mm], 5.35),
    p("Ako или než", H2),
    p("После сравнительной степени используются <b>ako</b> и <b>než</b>. Оба варианта нейтральны: <i>častejšie ako predtým</i>, <i>častejšie než predtým</i>."),
    table([
        ["Словацкий", "Русский"],
        ["Teraz cvičím pravidelnejšie ako vlani.", "Сейчас я тренируюсь регулярнее, чем в прошлом году."],
        ["Pri plávaní dýcham pokojnejšie než pri behu.", "При плавании я дышу спокойнее, чем при беге."],
        ["Na bicykli sa pohybujem rýchlejšie ako pešo.", "На велосипеде я передвигаюсь быстрее, чем пешком."],
        ["Po večernej prechádzke zaspím ľahšie.", "После вечерней прогулки я засыпаю легче."],
        ["Cez víkend spím dlhšie, ale vstávam neskôr.", "В выходные я сплю дольше, но встаю позже."],
        ["Tento mesiac sedím menej a chodím viac.", "В этом месяце я меньше сижу и больше хожу."],
    ], [93 * mm, 77 * mm], 5.05),
    box("Сравнивайте конкретно: не только <i>je to lepšie</i>, а <i>teraz spím lepšie, cvičím častejšie a sedím menej</i>.", PALE, ROSE, SMALL),
    PageBreak(),

    p("3. Привычка и один результат: вид", H1),
    p("Для привычки, процесса и повторения нужен несовершенный вид. Для одного ограниченного шага или достигнутого результата часто выбирается совершенный вид. Это не автоматическое правило по приставке: учите полезные пары целиком."),
    table([
        ["Привычка или процесс", "Один конкретный шаг"],
        ["Každý deň cvičím.", "Dnes si zacvičím dvadsať minút."],
        ["Cez týždeň chodím pešo.", "Po práci sa prejdem."],
        ["Trikrát týždenne plávam.", "V sobotu si zaplávam."],
        ["Ráno pijem pohár vody.", "Po tréningu vypijem pohár vody."],
        ["Večer čítam namiesto telefónu.", "Dnes večer si prečítam jednu kapitolu."],
    ], [85 * mm, 85 * mm], 5.4),
    p("Буду делать или сделаю", H2),
    table([
        ["Форма", "Значение", "Пример"],
        ["budem + infinitív", "процесс, повторение", "Budúci týždeň budem cvičiť doma."],
        ["совершенный глагол", "один завершённый шаг", "Zajtra si zacvičím po práci."],
    ], [43 * mm, 51 * mm, 76 * mm], 5.25),
    p("Как сделать план измеримым", H2),
    table([
        ["Слишком общо", "Реалистичнее"],
        ["Budem viac športovať.", "V utorok a vo štvrtok budem tridsať minút plávať."],
        ["Budem menej sedieť.", "Každú hodinu sa postavím a prejdem sa."],
        ["Budem lepšie spať.", "Trikrát tento týždeň pôjdem spať pred jedenástou."],
    ], [69 * mm, 101 * mm], 5.2),
    box("<b>A2-связка:</b> привычка в настоящем + сравнение + один будущий шаг. <i>Teraz chodím menej ako predtým, preto sa dnes večer prejdem tridsať minút.</i>", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    PageBreak(),

    p("4. Совет и реальный план", H1),
    p("Модель <b>mal by som / mala by som + infinitív</b> выражает мягкую рекомендацию самому себе. Возвратное <i>sa</i> обычно стоит после условной формы: <i>Mal by som sa viac hýbať.</i>"),
    table([
        ["Кто", "Пример", "Перевод"],
        ["мужчина", "Mal by som sa viac hýbať.", "Мне стоило бы больше двигаться."],
        ["женщина", "Mala by som chodiť spať skôr.", "Мне стоило бы раньше ложиться."],
        ["мы", "Mali by sme častejšie chodiť pešo.", "Нам стоило бы чаще ходить пешком."],
        ["ты", "Nemal by si trénovať bez oddychu.", "Тебе не стоило бы тренироваться без отдыха."],
    ], [27 * mm, 75 * mm, 68 * mm], 5.15),
    p("Ak и keď в реальном условии", H2),
    table([
        ["Союз", "Смысл", "Пример"],
        ["ak", "если, условие не гарантировано", "Ak bude pršať, budem cvičiť doma."],
        ["keď", "когда, ожидаемое будущее", "Keď prídem z práce, pôjdem sa prejsť."],
        ["keď", "когда, повторяющаяся ситуация", "Keď mám voľno, chodím plávať."],
    ], [23 * mm, 64 * mm, 83 * mm], 5.2),
    p("Мини-план на неделю", H2),
    box("Teraz sa hýbem menej ako v lete a po práci často dlho sedím. Mal by som cvičiť pravidelnejšie, ale nechcem začať príliš náročne. V pondelok a vo štvrtok budem doma cvičiť dvadsať minút. Keď prídem z práce skôr, pôjdem sa ešte prejsť. Ak bude pršať, zostanem doma a zacvičím si pri otvorenom okne. Cez víkend si zaplávam. O týždeň zhodnotím, čo sa mi podarilo.", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    p("Каркас собственного плана", H2),
    table([
        ["1", "Teraz..."], ["2", "V porovnaní s..."], ["3", "Mal / Mala by som..."],
        ["4", "V pondelok..."], ["5", "Keď..."], ["6", "Ak..., tak..."],
    ], [11 * mm, 74 * mm, 11 * mm, 74 * mm], 5.4, False),
    box("Реальный план содержит небольшой шаг, время и запасной вариант. Это убедительнее, чем обещание <i>Odteraz budem každý deň dve hodiny športovať</i>.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    PageBreak(),

    p("5. Частые ошибки и упражнения", H1),
    table([
        ["Ошибка", "Правильно", "Почему"],
        ["*rýchlejší bežím", "bežím rýchlejšie", "действие описывает наречие"],
        ["*viac lepšie", "lepšie", "двойная степень не нужна"],
        ["*mal som by cvičiť", "mal by som cvičiť", "фиксированный порядок"],
        ["*mal by som viac sa hýbať", "mal by som sa viac hýbať", "sa после условной формы"],
        ["*ak pršalo zajtra", "ak bude zajtra pršať", "реальное будущее"],
    ], [54 * mm, 62 * mm, 54 * mm], 4.9),
    p("Упражнение 1. Найдите естественное название", H2),
    p("1) cvičiť: cvičenie / cviknutie 2) plávať: plávanie / plávka 3) spať: spánok / spavosť 4) chodiť: chôdza / chodenosť.", SMALL),
    p("Упражнение 2. Поставьте наречие в сравнительную степень", H2),
    p("1) Teraz cvičím (pravidelne) ako vlani. 2) Po prechádzke spím (dobre). 3) Chcem sedieť (málo) a chodiť (veľa). 4) Na bicykli idem (rýchlo) ako pešo.", SMALL),
    p("Упражнение 3. Выберите вид", H2),
    p("1) Každý deň cvičím / si zacvičím. 2) Dnes večer sa prechádzam / sa prejdem po parku. 3) Trikrát týždenne plávam / si zaplávam. 4) Po tréningu pijem / vypijem tento pohár vody.", SMALL),
    p("Упражнение 4. Исправьте ошибки", H2),
    p("1) Mal som by viac chodiť. 2) Bežím viac rýchlejšie. 3) Mala by som skôr spať chodiť. 4) Ak zajtra prší, budem cvičiť doma.", SMALL),
    p("Упражнение 5. Соедините условие и результат", H2),
    p("1) Ak bude pršať... 2) Keď prídem z práce... 3) Keď mám voľno... + a) chodím plávať b) budem cvičiť doma c) pôjdem sa prejsť.", SMALL),
    p("Упражнение 6. Ваш реалистичный план", H2),
    p("Напишите 6-7 предложений: нынешняя привычка, одно сравнение, совет себе, два конкретных шага, предложение с keď и запасной вариант с ak.", SMALL),
    PageBreak(),

    p("6. Ответы и проверка мастерства", H1),
    p("Ответы", H2),
    table([
        ["№", "Ключ"],
        ["1", "1 cvičenie; 2 plávanie; 3 spánok; 4 chôdza."],
        ["2", "1 pravidelnejšie; 2 lepšie; 3 menej, viac; 4 rýchlejšie."],
        ["3", "1 cvičím; 2 sa prejdem; 3 plávam; 4 vypijem."],
        ["4", "1 Mal by som viac chodiť. 2 Bežím rýchlejšie. 3 Mala by som chodiť spať skôr. 4 Ak bude zajtra pršať, budem cvičiť doma."],
        ["5", "1-b Ak bude pršať, budem cvičiť doma. 2-c Keď prídem z práce, pôjdem sa prejsť. 3-a Keď mám voľno, chodím plávať."],
        ["6", "Открытое задание: возможны другие естественные планы при наличии всех пунктов условия."],
    ], [13 * mm, 157 * mm], 5.05),
    p("Модель самостоятельного ответа", H2),
    box("Cez pracovný týždeň veľa sedím a športujem menej ako cez víkend. V poslednom čase však chodím pešo častejšie ako predtým. Mala by som cvičiť pravidelnejšie a chodiť spať skôr. V utorok a v piatok budem tridsať minút plávať. Keď prídem domov včas, pôjdem sa ešte krátko prejsť. Ak bude bazén zatvorený, zacvičím si doma. Tento plán je malý, ale dokážem ho dodržať.", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    p("Пять опор темы", H2),
    table([
        ["1", "Активность: <i>cvičenie, plávanie, chôdza, spánok</i>."],
        ["2", "Сравнение действия: <i>častejšie, lepšie, menej, viac</i>."],
        ["3", "Привычка: <i>cvičím</i>; один шаг: <i>zacvičím si</i>."],
        ["4", "Мягкий совет: <i>Mal / Mala by som...</i>"],
        ["5", "Условие: <i>ak</i>; ожидаемое или повторное время: <i>keď</i>."],
    ], [11 * mm, 159 * mm], 5.3, False),
    p("Финальная проверка", H2),
    box("Без подсказки назовите четыре активности, сравните две привычки, различите регулярное и одно завершённое действие, дайте себе мягкий совет и сформулируйте план с keď и ak. Если получается связный текст из 6-7 предложений, цель 8.5 достигнута.", PALE, ROSE, SMALL),
]

doc.build(story)
print(OUTPUT)
