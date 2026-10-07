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
OUTPUT = ROOT / "output/pdf/A2/Module_08/Slovak_A2_Tema_8_1_Semya_druzya_vneshnost_i_harakter.pdf"
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
BODY = ParagraphStyle("Body", fontName="Arial", fontSize=8.55, leading=11.15, textColor=INK, spaceAfter=2.6 * mm)
SMALL = ParagraphStyle("Small", parent=BODY, fontSize=7.35, leading=9.05, spaceAfter=1.25 * mm)
TINY = ParagraphStyle("Tiny", parent=BODY, fontSize=6.55, leading=7.85, spaceAfter=0.8 * mm)
TITLE = ParagraphStyle("Title", fontName="Arial-Bold", fontSize=19.5, leading=23.2, textColor=colors.white, alignment=TA_LEFT, spaceAfter=4.5 * mm)
SUBTITLE = ParagraphStyle("Subtitle", fontName="Arial", fontSize=11.2, leading=14.5, textColor=colors.HexColor("#FFD8EB"), spaceAfter=4 * mm)
H1 = ParagraphStyle("H1", fontName="Arial-Bold", fontSize=15.2, leading=18, textColor=PLUM, spaceBefore=0.8 * mm, spaceAfter=2.8 * mm)
H2 = ParagraphStyle("H2", fontName="Arial-Bold", fontSize=10.5, leading=12.8, textColor=PINK, spaceBefore=0.9 * mm, spaceAfter=1.3 * mm)
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
            f"cell_{row_index}_{size}_{len(data)}", parent=SMALL, fontSize=size, leading=size + 1.65,
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
        canvas.drawString(20 * mm, height - 12 * mm, "A2 8.1  |  Семья, друзья, внешность и характер")
    canvas.setFont("Arial", 8)
    canvas.setFillColor(MUTED)
    canvas.drawString(20 * mm, 9 * mm, "SlovoKrok | личный учебный модуль")
    canvas.drawRightString(width - 20 * mm, 9 * mm, f"стр. {page_number} / 7")
    canvas.restoreState()


doc = BaseDocTemplate(
    str(OUTPUT), pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=20 * mm, bottomMargin=18 * mm,
    title="Slovak A2 - Тема 8.1 - Семья, друзья, внешность и характер", author="SlovoKrok",
)
doc.addPageTemplates([PageTemplate(
    id="series", frames=[Frame(20 * mm, 18 * mm, 170 * mm, 257 * mm, id="main", leftPadding=0, rightPadding=0)], onPage=draw_page,
)])


story = [
    p("МОДУЛЬ 8  •  ОТНОШЕНИЯ, ЗДОРОВЬЕ И ИТОГ A2", KICK),
    p("Семья, друзья, внешность и характер", TITLE),
    p("Rodina, priatelia, vzhľad a povaha: представляем близких и сравниваем отношения", SUBTITLE),
    Spacer(1, 44 * mm),
    p("На уровне A2 мало перечислить родственников. Важно связно представить человека, описать внешность и характер, а затем объяснить, чем ваши отношения похожи или отличаются."),
    p("После модуля вы сможете:", H2),
    table([
        ["1", "назвать близких и более дальних родственников"],
        ["2", "описать внешность и характер в согласованных формах"],
        ["3", "правильно использовать свой / его / её и притяжательные прилагательные"],
        ["4", "сравнить людей и отношения в связном рассказе"],
    ], [12 * mm, 158 * mm], 7.1, False),
    Spacer(1, 3 * mm),
    box("<b>Формула рассказа:</b> кто это → как он / она выглядит → какой у него / неё характер → что вы делаете вместе → чем ваши отношения отличаются."),
    PageBreak(),

    p("1. Родство и винительный множественного числа", H1),
    p("Расширяем семейный круг: называем не только родителей и детей, но и родню партнёра, двоюродных родственников и близких людей вне семьи."),
    table([
        ["Словацкий", "Русский", "Пример"],
        ["starí rodičia", "бабушка и дедушка", "Cez víkend navštevujem starých rodičov."],
        ["vnuk / vnučka", "внук / внучка", "Majú dvoch vnukov a jednu vnučku."],
        ["bratranec / sesternica", "двоюродный брат / сестра", "Často stretávam bratrancov a sesternice."],
        ["svokor / svokra", "свёкор / тесть; свекровь / тёща", "Pozývame svokrovcov na večeru."],
        ["švagor / švagriná", "брат / сестра супруга", "Dobre poznám svojich švagrov."],
        ["zať / nevesta", "зять / невестка", "Rodičia majú radi zaťov aj nevesty."],
        ["nevlastný brat", "сводный / неродной брат", "Mám dvoch nevlastných bratov."],
        ["partner / partnerka", "партнёр / партнёрша", "Priatelia pozvali svojich partnerov."],
    ], [39 * mm, 48 * mm, 83 * mm], 5.2),
    p("Кого? Что? — Akuzatív plurálu", H2),
    table([
        ["Тип", "Модель", "Примеры"],
        ["муж. одуш.", "A pl. часто -ov", "vidím bratov, synov, kamarátov; poznám dobrých susedov"],
        ["жен. род", "A pl. = N pl.", "mám sestry; stretávam milé kolegyne"],
        ["ср. род", "A pl. = N pl.", "poznám malé deti; vidím veselé dievčatá"],
        ["неодуш.", "A pl. = N pl.", "má modré oči a krátke vlasy"],
    ], [34 * mm, 40 * mm, 96 * mm], 5.45),
    box("<b>Главный контраст:</b> <i>To sú moji dobrí kamaráti</i> (кто?) → <i>Často stretávam svojich dobrých kamarátov</i> (кого?). У одушевлённого мужского рода меняются и существительное, и согласованные слова.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    PageBreak(),

    p("2. Внешность и характер", H1),
    p("Описание звучит естественно, когда вы соединяете общий признак, одну деталь и личную оценку. Избегайте длинного списка прилагательных без связок."),
    table([
        ["Что описываем", "Полезные модели", "Пример с переводом"],
        ["рост / фигура", "vysoký, nízky, štíhly", "Môj brat je vysoký a štíhly. — Мой брат высокий и стройный."],
        ["волосы / глаза", "má kučeravé vlasy, hnedé oči", "Má krátke tmavé vlasy. — У неё короткие тёмные волосы."],
        ["деталь", "nosí okuliare / bradu", "Náš strýko nosí okuliare. — Наш дядя носит очки."],
        ["общение", "otvorený, spoločenský, tichý", "Je tichá, ale veľmi priateľská. — Она тихая, но очень дружелюбная."],
        ["надёжность", "spoľahlivý, zodpovedný", "Môžem sa naňho spoľahnúť. — Я могу на него положиться."],
        ["сложная черта", "tvrdohlavý, netrpezlivý", "Niekedy je trochu tvrdohlavý. — Иногда он немного упрямый."],
    ], [36 * mm, 55 * mm, 79 * mm], 5.15),
    p("Сравниваем людей", H2),
    table([
        ["Модель", "Пример", "Перевод"],
        ["-ší / -ejší + ako", "Eva je mladšia a otvorenejšia ako Jana.", "Ева моложе и общительнее Яны."],
        ["viac / menej + ako", "S Evou trávim viac času ako s Janou.", "С Евой я провожу больше времени, чем с Яной."],
        ["taký / taká ... ako", "Nie som taká trpezlivá ako moja mama.", "Я не такая терпеливая, как мама."],
        ["podobať sa na + A", "Dcéra sa podobá na svoju mamu.", "Дочь похожа на свою маму."],
        ["lepšie / horšie si rozumieť", "S bratom si rozumiem lepšie ako so sesternicou.", "С братом я лажу лучше, чем с кузиной."],
    ], [38 * mm, 72 * mm, 60 * mm], 5.0),
    box("<b>Нюанс:</b> для прилагательных естественна простая степень: <i>starší, mladší, vyšší, veselší, otvorenejší</i>. Слова <i>viac / menej</i> удобно использовать с количеством и действиями: <i>viac času, menej sa hádame</i>.", PALE, ROSE, SMALL),
    PageBreak(),

    p("3. Svoj, jeho, jej и притяжательные прилагательные", H1),
    p("<b>Svoj</b> указывает на владельца, который является подлежащим этого же предложения. Лицо владельца не важно: <i>ja mám svoju, ty máš svoju, oni majú svoju</i>."),
    table([
        ["Ситуация", "Правильно", "Почему"],
        ["Анна любит своего брата.", "Anna má rada svojho brata.", "владелец Anna = подлежащее"],
        ["Петер представил свою сестру.", "Peter predstavil svoju sestru.", "владелец Peter = подлежащее"],
        ["Дети навестили своих дедушку и бабушку.", "Deti navštívili svojich starých rodičov.", "владелец deti = подлежащее"],
        ["Я знаю Петера и его сестру.", "Poznám Petra a jeho sestru.", "владелец Peter ≠ подлежащее ja"],
        ["Луция говорит о Мареке и его детях.", "Lucia hovorí o Marekovi a jeho deťoch.", "дети принадлежат Мареку"],
    ], [43 * mm, 73 * mm, 54 * mm], 5.1),
    p("Притяжательные прилагательные", H2),
    p("От названий лиц можно образовать прилагательное: мужская основа обычно получает <b>-ov</b>, женская — <b>-in</b>. Оно согласуется не с владельцем, а с предметом: <i>otcov brat, otcova sestra, otcovo auto; matkin brat, matkina sestra, matkino auto</i>."),
    table([
        ["Форма", "Значение", "Пример"],
        ["otcov / otcova / otcovo", "папин", "Otcov brat je môj strýko."],
        ["matkin / matkina / matkino", "мамин", "Matkina sestra býva v Nitre."],
        ["bratov / bratova / bratovo", "брата", "Bratova dcéra je moja neter."],
        ["sestrin / sestrina / sestrino", "сестры", "Sestrin syn je môj synovec."],
    ], [46 * mm, 38 * mm, 86 * mm], 5.45),
    box("<b>Не смешивайте:</b> <i>Peter prišiel so svojou sestrou</i> — со своей сестрой. <i>Peter prišiel s jeho sestrou</i> обычно значит «с сестрой другого мужчины», известного из контекста.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    PageBreak(),

    p("4. Связный рассказ и банк живых фраз", H1),
    p("Модель: представляем близкого человека", H2),
    box("<b>Moja najlepšia kamarátka sa volá Lenka.</b> Poznáme sa od strednej školy. Je stredne vysoká, má dlhé kučeravé vlasy a zelené oči. Na prvý pohľad pôsobí ticho, ale medzi priateľmi je veselá a otvorená. Je trpezlivejšia ako ja a vždy si nájde čas na rozhovor. Máme podobný zmysel pre humor, preto si veľmi dobre rozumieme. Ja plánujem veci dopredu, kým Lenka je spontánnejšia. Práve preto sa dobre dopĺňame.<br/><br/><b>Перевод:</b> Мою лучшую подругу зовут Ленка. Мы знакомы со школы. Она среднего роста, с длинными кудрявыми волосами и зелёными глазами. На первый взгляд кажется тихой, но с друзьями весёлая и открытая. Она терпеливее меня и всегда находит время поговорить. У нас похожее чувство юмора, поэтому мы отлично ладим. Я всё планирую заранее, а Ленка более спонтанная. Именно поэтому мы хорошо дополняем друг друга.", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    p("Фразы, которые связывают описание", H2),
    table([
        ["Словацкий", "Русский"],
        ["Poznáme sa už desať rokov.", "Мы знакомы уже десять лет."],
        ["Vyrastali sme spolu.", "Мы выросли вместе."],
        ["Máme veľa spoločného.", "У нас много общего."],
        ["Máme podobný zmysel pre humor.", "У нас похожее чувство юмора."],
        ["Môžem sa na ňu vždy spoľahnúť.", "Я всегда могу на неё положиться."],
        ["Často sa stretávame cez víkend.", "Мы часто встречаемся на выходных."],
        ["Niekedy máme odlišné názory.", "Иногда у нас разные мнения."],
        ["Hádame sa menej ako kedysi.", "Мы спорим реже, чем раньше."],
        ["Sme si blízki, hoci bývame ďaleko.", "Мы близки, хотя живём далеко."],
        ["Dobre sa dopĺňame.", "Мы хорошо дополняем друг друга."],
        ["Na rozdiel odo mňa je veľmi pokojný.", "В отличие от меня он очень спокойный."],
        ["Obaja radi cestujeme.", "Мы оба любим путешествовать."],
    ], [88 * mm, 82 * mm], 5.5),
    PageBreak(),

    p("5. Частые ошибки и упражнения", H1),
    table([
        ["Ошибка", "Правильно", "Почему"],
        ["*Vidím moji kamaráti.", "Vidím svojich kamarátov.", "муж. одуш., A pl."],
        ["*Anna má rada jej brata.", "Anna má rada svojho brata.", "владелец = подлежащее"],
        ["*Poznám Peterovu sestru.", "Poznám Petrovu sestru.", "Peter → Petrov, без -er-"],
        ["*Má hnedé vlasov.", "Má hnedé vlasy.", "неодуш. A pl. = N pl."],
        ["*Je viac mladá ako ja.", "Je mladšia ako ja.", "частотная простая степень"],
    ], [50 * mm, 56 * mm, 64 * mm], 5.25),
    p("Упражнение 1. Выберите форму", H2),
    p("1) Často stretávam (moji kamaráti / svojich kamarátov). 2) Má dve (mladšie sestry / mladších sestier). 3) Poznáme (milé susedky / milých susediek). 4) Vidím (malé deti / malých detí).", SMALL),
    p("Упражнение 2. Вставьте svoj / jeho / jej", H2),
    p("1) Martin predstavil ___ partnerku. 2) Poznám Martina a ___ partnerku. 3) Eva navštívila ___ starých rodičov. 4) Hovoríme o Zuzane a ___ bratovi.", SMALL),
    p("Упражнение 3. Образуйте притяжательное прилагательное", H2),
    p("1) (otec) sestra  2) (mama) brat  3) (sestra) dcéra  4) (Peter) rodičia.", SMALL),
    p("Упражнение 4. Исправьте ошибки", H2),
    p("1) Môj brat je viac starý ako ja. 2) Lucia má rada jej sestry. 3) Často navštevujem dobrí priatelia. 4) Dcéra sa podobá so svojou mamou.", SMALL),
    p("Упражнение 5. Переведите", H2),
    p("1) Моя кузина общительнее меня. 2) Мы знакомы десять лет и хорошо ладим. 3) Петер представил своих родителей. 4) У неё короткие волосы и зелёные глаза.", SMALL),
    p("Упражнение 6. Самостоятельная речь", H2),
    p("Представьте родственника или друга в 6-7 предложениях: родство / знакомство, внешность, две черты характера, общее занятие, одно сравнение и итог об отношениях.", SMALL),
    PageBreak(),

    p("6. Ответы и проверка мастерства", H1),
    p("Ответы", H2),
    table([
        ["№", "Ключ"],
        ["1", "1 svojich kamarátov; 2 mladšie sestry; 3 milé susedky; 4 malé deti."],
        ["2", "1 svoju; 2 jeho; 3 svojich; 4 jej."],
        ["3", "1 otcova sestra; 2 matkin brat; 3 sestrina dcéra; 4 Petrovi rodičia."],
        ["4", "1 Môj brat je starší ako ja. 2 Lucia má rada svoje sestry. 3 Často navštevujem dobrých priateľov. 4 Dcéra sa podobá na svoju mamu."],
        ["5", "1 Moja sesternica je spoločenskejšia ako ja. 2 Poznáme sa desať rokov a dobre si rozumieme. 3 Peter predstavil svojich rodičov. 4 Má krátke vlasy a zelené oči."],
        ["6", "Открытое задание: возможны другие естественные ответы; проверьте все пункты условия."],
    ], [13 * mm, 157 * mm], 5.35),
    p("Модель самостоятельного ответа", H2),
    box("Môj bratranec sa volá Tomáš a poznáme sa od detstva. Je vysoký, má krátke svetlé vlasy a nosí okuliare. Je pokojný a spoľahlivý, ale niekedy trochu tvrdohlavý. Obaja radi chodíme na výlety. Tomáš je trpezlivejší ako ja, kým ja som spontánnejší. Máme odlišné názory na šport, no takmer nikdy sa nehádame. Veľmi dobre si rozumieme a môžem sa naňho spoľahnúť.", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    p("Четыре опоры темы", H2),
    table([
        ["1", "Для мужчин-лиц во множественном числе: <i>poznám dobrých kamarátov</i>."],
        ["2", "Если владелец = подлежащее, используйте <i>svoj</i>: <i>Eva predstavila svoju sestru</i>."],
        ["3", "Сравнивайте через <i>-ší/-ejší ako</i>, <i>taký ako</i>, <i>lepšie než/ako</i>."],
        ["4", "Связный портрет объясняет отношения, а не просто перечисляет признаки."],
    ], [11 * mm, 159 * mm], 5.8, False),
    p("Финальная проверка", H2),
    box("Без подсказки назовите 6 родственников; скажите, кого часто видите; опишите внешность и характер одного человека; используйте <i>svoj</i> и одно притяжательное прилагательное; сравните ваши отношения с двумя близкими. Если все пять шагов получаются связно, цель 8.1 достигнута.", PALE, ROSE, SMALL),
]

doc.build(story)
print(OUTPUT)
