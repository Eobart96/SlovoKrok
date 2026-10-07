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
OUTPUT = ROOT / "output" / "pdf" / "A2" / "Module_03" / "Slovak_A2_Tema_3_2_Prilagatelnye_vo_mnozhestvennom_chisle.pdf"
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
        canvas.drawString(20 * mm, height - 12 * mm, "A2 3.2  |  Прилагательные во множественном числе")
    canvas.setFont("Arial", 8)
    canvas.setFillColor(MUTED)
    canvas.drawString(20 * mm, 9 * mm, "SlovoKrok | личный учебный модуль")
    canvas.drawRightString(width - 20 * mm, 9 * mm, f"стр. {page} / 7")
    canvas.restoreState()


doc = BaseDocTemplate(
    str(OUTPUT), pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=20 * mm, bottomMargin=18 * mm,
    title="Slovak A2 - Тема 3.2 - Прилагательные во множественном числе", author="SlovoKrok",
)
frame = Frame(20 * mm, 18 * mm, 170 * mm, 257 * mm, id="main", leftPadding=0, rightPadding=0)
doc.addPageTemplates([PageTemplate(id="series", frames=[frame], onPage=draw_page)])

story = [
    p("МОДУЛЬ 3  •  ПРИЛАГАТЕЛЬНЫЕ, МЕСТОИМЕНИЯ И ЧИСЛИТЕЛЬНЫЕ", COVER_KICKER),
    p("Прилагательные<br/>во множественном числе", TITLE),
    p("Prídavné mená v množnom čísle", SUBTITLE),
    Spacer(1, 34 * mm),
    p("Во множественном числе род почти исчезает из окончаний прилагательного, но в N и A решающим остаётся различие между группой лиц мужского рода и всеми остальными группами.", BODY),
    p("После модуля вы сможете:", H2),
    styled_table([
        ["1", "выбирать -í для лиц мужского рода и -é для остальных групп в N"],
        ["2", "различать A: новých kolegov, но nové domy, knihy, mestá"],
        ["3", "использовать общие формы G/D/L/I независимо от рода"],
        ["4", "согласовывать модели pekný и cudzí с существительными во всех падежах"],
    ], [12 * mm, 158 * mm], font_size=7.35, header=False),
    Spacer(1, 3 * mm),
    box("<b>Главная формула:</b> N/A имеют две дорожки: мужские лица и все остальные; G/D/L/I имеют по одной форме для всех родов.", PALE, PINK),
    PageBreak(),

    p("1. Nominatív: -í или -é?", H1),
    p("Для модели <b>pekný</b> в N множественного числа используйте <b>-í</b> с группой лиц мужского рода. С предметами мужского рода, женским и средним родом используйте <b>-é</b>.", BODY),
    styled_table([
        ["Группа", "Окончание", "Пример", "Перевод"],
        ["мужские лица", "-í", "noví kolegovia", "новые коллеги-мужчины"],
        ["мужские предметы", "-é", "nové stoly", "новые столы"],
        ["женский род", "-é", "nové kolegyne", "новые коллеги-женщины"],
        ["средний род", "-é", "nové mestá", "новые города"],
    ], [38 * mm, 24 * mm, 49 * mm, 59 * mm], font_size=6.7),
    p("Окончание показывает тип группы", H2),
    styled_table([
        ["SK", "Что видно"],
        ["Milí hostia čakajú pred hotelom.", "hostia - лица мужского рода, поэтому milí"],
        ["Dobré knihy sú na stole.", "knihy - женский род, поэтому dobré"],
        ["Moderné hotely sú drahé.", "hotely - предметы мужского рода, поэтому moderné"],
        ["Malé mestá sú pokojné.", "mestá - средний род, поэтому malé"],
    ], [78 * mm, 92 * mm], font_size=6.75),
    box("<b>Орфография:</b> <b>pekný chlapec -> pekní chlapci</b>. В единственном числе пишется <b>-ý</b>, а у группы лиц мужского рода во множественном числе - <b>-í</b>.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    box("<b>Практическое сокращение:</b> сначала спросите: это группа лиц мужского рода? Да -> <b>-í</b>. Нет -> <b>-é</b>.", PALE, ROSE, SMALL),
    p("<b>Почему именно лица?</b> Названия животных мужского рода во множественном числе обычно идут по дорожке предметов: <b>veľké psy, divé vlky</b>. У <b>pes, vlk, vták</b> возможны также личные варианты <b>veľkí psi, diví vlci, sťahovaví vtáci</b>; запоминайте их как допустимые пары.", TINY),
    PageBreak(),

    p("2. Akuzatív: люди и всё остальное", H1),
    p("В A множественного числа группа лиц мужского рода получает форму как G: <b>-ých</b>. Для предметов мужского рода, женского и среднего рода A совпадает с N: <b>-é</b>.", BODY),
    styled_table([
        ["Тип", "N", "A", "Пример"],
        ["мужские лица", "noví kolegovia", "nových kolegov", "Vidím nových kolegov."],
        ["мужские предметы", "nové stoly", "nové stoly", "Kupujeme nové stoly."],
        ["женский род", "nové knihy", "nové knihy", "Čítam nové knihy."],
        ["средний род", "nové mestá", "nové mestá", "Navštevujeme nové mestá."],
    ], [34 * mm, 43 * mm, 43 * mm, 50 * mm], font_size=6.55),
    p("Три быстрые пары", H2),
    styled_table([
        ["Кто действует? N", "Кого / что видим? A"],
        ["Noví študenti prichádzajú.", "Poznám nových študentov."],
        ["Milí susedia pomáhajú.", "Pozdravím milých susedov."],
        ["Nové autobusy meškajú.", "Čakáme na nové autobusy."],
    ], [85 * mm, 85 * mm], font_size=6.85),
    p("Согласование всей группы", H2),
    box("<b>tí noví slovenskí kolegovia</b> -> vidím <b>tých nových slovenských kolegov</b>.<br/><b>tie nové pracovné ponuky</b> -> čítam <b>tie nové pracovné ponuky</b>.", PALE, ROSE, SMALL),
    box("<b>Не переносите правило людей на предметы:</b> *vidím nových hotely неверно. Правильно <b>vidím nové hotely</b>.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    PageBreak(),

    p("3. Косвенные падежи: одна форма для всех", H1),
    p("В G, D, L и I окончание прилагательного не зависит от рода. Меняются только падеж и модель; окончания существительных при этом остаются разными.", BODY),
    styled_table([
        ["Падеж", "pekný", "Примеры разных родов"],
        ["G", "-ých", "bez nových kolegov / kníh / miest"],
        ["D", "-ým", "k novým kolegom / knihám / mestám"],
        ["L", "-ých", "o nových kolegoch / knihách / mestách"],
        ["I", "-ými", "s novými kolegami / knihami / mestami"],
    ], [26 * mm, 29 * mm, 115 * mm], font_size=6.75),
    p("Мягкая модель cudzí", H2),
    styled_table([
        ["Падеж", "Лица мужского рода", "Остальные группы"],
        ["N", "cudzí turisti", "cudzie jazyky / otázky / slová"],
        ["G", "cudzích turistov", "cudzích jazykov / otázok / slov"],
        ["D", "cudzím turistom", "cudzím jazykom / otázkam / slovám"],
        ["A", "cudzích turistov", "cudzie jazyky / otázky / slová"],
        ["L", "o cudzích turistoch", "o cudzích jazykoch / otázkach / slovách"],
        ["I", "s cudzími turistami", "s cudzími jazykmi / otázkami / slovami"],
    ], [26 * mm, 65 * mm, 79 * mm], font_size=6.3),
    box("<b>Твёрдая / мягкая:</b> <b>-ých, -ým, -ými</b> у pekný; <b>-ích, -ím, -ími</b> у cudzí. Сравните: <b>o nových témach</b>, но <b>o cudzích slovách</b>.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    PageBreak(),

    p("4. Живые модели в контексте", H1),
    p("Определяйте форму по цепочке: падеж -> тип группы в N/A -> твёрдая или мягкая модель -> окончание всей группы.", BODY),
    styled_table([
        ["SK", "RU"],
        ["Noví kolegovia začínajú v pondelok.", "Новые коллеги начинают в понедельник."],
        ["Cudzí turisti sa pýtajú na cestu.", "Иностранные туристы спрашивают дорогу."],
        ["Nové stoly sú v kancelárii.", "Новые столы находятся в офисе."],
        ["Dobré knihy rýchlo zmizli.", "Хорошие книги быстро разобрали."],
        ["Malé mestá majú príjemnú atmosféru.", "В маленьких городах приятная атмосфера."],
        ["Poznám nových susedov.", "Я знаю новых соседей."],
        ["Kupujeme lacné lístky.", "Мы покупаем недорогие билеты."],
        ["Bez nových údajov sa nerozhodneme.", "Без новых данных мы не решим."],
        ["Pomáham novým študentom.", "Я помогаю новым студентам."],
        ["Hovoríme o dôležitých zmenách.", "Мы говорим о важных изменениях."],
        ["Pracujem s novými kolegyňami.", "Я работаю с новыми коллегами-женщинами."],
        ["K ďalším otázkam sa vrátime.", "Мы вернёмся к следующим вопросам."],
    ], [86 * mm, 84 * mm], font_size=6.0),
    p("Мини-диалог", H2),
    box("<b>A:</b> Prídu aj <b>noví zahraniční partneri</b>? - Приедут и новые зарубежные партнёры?<br/><b>B:</b> Áno, čakáme <b>troch nových partnerov</b>. - Да, мы ждём трёх новых партнёров.<br/><b>A:</b> Máme pre nich <b>nové materiály</b>? - У нас есть для них новые материалы?<br/><b>B:</b> Áno, budeme hovoriť o <b>dôležitých projektoch</b>. - Да, мы будем говорить о важных проектах.<br/><b>A:</b> Potom pôjdeme s <b>novými partnermi</b> na večeru. - Потом мы пойдём с новыми партнёрами на ужин.", PALE, ROSE, TINY),
    p("Подсказка", H2),
    p("С числительными форма группы может зависеть от конструкции. Здесь <b>troch nových partnerov</b> дано как готовая частотная модель; системно числительные изучаются позже в модуле 3.", SMALL),
    PageBreak(),

    p("5. Частые ошибки и упражнения", H1),
    box("<b>Частые ошибки:</b> *nový kolegovia -> <b>noví kolegovia</b>; *dobrí knihy -> <b>dobré knihy</b>; *vidím noví kolegovia -> <b>vidím nových kolegov</b>; *s cudzými turistami -> <b>s cudzími turistami</b>.", CREAM, colors.HexColor("#E7C76C"), TINY),
    p("Упражнение 1. Выберите -í или -é", H2),
    p("1) nov(í/é) študenti; 2) nov(í/é) autobusy; 3) dobr(í/é) lekári; 4) dobr(í/é) správy; 5) mal(í/é) mestá.", TINY),
    p("Упражнение 2. Поставьте новый в N или A", H2),
    p("1) ___ kolegovia prichádzajú. 2) Vidím ___ kolegov. 3) ___ hotely sú drahé. 4) Hľadáme ___ hotely. 5) Čítam ___ knihy.", TINY),
    p("Упражнение 3. Поставьте прилагательное в нужный падеж", H2),
    p("1) bez (dôležitý) údajov; 2) k (nový) študentom; 3) o (nový) projektoch; 4) s (dobrý) kolegyňami; 5) bez (cudzí) slov.", TINY),
    p("Упражнение 4. Исправьте ошибки; одна фраза уже верна", H2),
    p("1) Milé susedia pomáhajú. 2) Poznám noví študenti. 3) Hovoríme o nové projekty. 4) Pracujem s ďalšími kolegami. 5) Cudzie turisti čakajú.", TINY),
    p("Упражнение 5. Переведите", H2),
    p("1) новые врачи; 2) я вижу новые столы; 3) без важных документов; 4) о маленьких городах; 5) с иностранными студентами.", TINY),
    p("Упражнение 6. Свой мини-текст", H2),
    p("Напишите 5-7 связанных предложений о группе коллег, туристов или товаров. Используйте N и A для людей и предметов, два косвенных падежа и одну форму модели cudzí или ďalší.", TINY),
    PageBreak(),

    p("6. Ответы и проверка мастерства", H1),
    p("Ответы", H2),
    p("<b>1.</b> noví študenti; nové autobusy; dobrí lekári; dobré správy; malé mestá.", TINY),
    p("<b>2.</b> Noví kolegovia prichádzajú. Vidím nových kolegov. Nové hotely sú drahé. Hľadáme nové hotely. Čítam nové knihy.", TINY),
    p("<b>3.</b> bez dôležitých údajov; k novým študentom; o nových projektoch; s dobrými kolegyňami; bez cudzích slov.", TINY),
    p("<b>4.</b> Milí susedia pomáhajú. Poznám nových študentov. Hovoríme o nových projektoch. Pracujem s ďalšími kolegami. Cudzí turisti čakajú.", TINY),
    p("<b>5.</b> noví lekári; vidím nové stoly; bez dôležitých dokumentov; o malých mestách; s cudzími študentmi.", TINY),
    p("<b>6. Модель:</b> Noví kolegovia dnes začínajú. Poznám nových kolegov. Ďalší kolegovia pracujú na nových projektoch. Pomáham novým kolegom s dokumentmi. Na obed idem s novými kolegami. Neskôr budeme hovoriť o ďalších úlohách. Возможны другие естественные варианты.", TINY),
    p("Итог в четырёх пунктах", H2),
    styled_table([
        ["OK", "В N выбираю -í для мужских лиц и -é для остальных групп."],
        ["OK", "В A различаю nových kolegov и nové stoly / knihy / mestá."],
        ["OK", "В G/D/L/I использую одну форму прилагательного для всех родов."],
        ["OK", "Различаю -ých/-ým/-ými и мягкие -ích/-ím/-ími."],
    ], [12 * mm, 158 * mm], font_size=6.9, header=False),
    Spacer(1, 2.2 * mm),
    box("<b>Финальная проверка:</b> без таблицы скажите по одной группе людей и предметов в N и A, затем измените <b>nové projekty</b> и <b>cudzí študenti</b> в G, D, L и I.", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    p("Следующий шаг", H2),
    p("В теме 3.3 вы научитесь сравнивать людей, места, товары и варианты с помощью степеней сравнения.", SMALL),
]

doc.build(story)
print(OUTPUT)
