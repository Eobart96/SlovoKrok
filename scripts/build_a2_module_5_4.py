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
OUTPUT = ROOT / "output" / "pdf" / "A2" / "Module_05" / "Slovak_A2_Tema_5_4_Otnositelnye_predlozheniya_s_ktory.pdf"
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
        canvas.drawString(20 * mm, height - 12 * mm, "A2 5.4  |  Относительные предложения с ktorý")
    canvas.setFont("Arial", 8)
    canvas.setFillColor(MUTED)
    canvas.drawString(20 * mm, 9 * mm, "SlovoKrok | личный учебный модуль")
    canvas.drawRightString(width - 20 * mm, 9 * mm, f"стр. {page} / 7")
    canvas.restoreState()


doc = BaseDocTemplate(
    str(OUTPUT), pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=20 * mm, bottomMargin=18 * mm,
    title="Slovak A2 - Тема 5.4 - Относительные предложения с ktorý", author="SlovoKrok",
)
frame = Frame(20 * mm, 18 * mm, 170 * mm, 257 * mm, id="main", leftPadding=0, rightPadding=0)
doc.addPageTemplates([PageTemplate(id="series", frames=[frame], onPage=draw_page)])

story = [
    p("МОДУЛЬ 5  •  СВЯЗНАЯ РЕЧЬ И СЛОЖНЫЕ ПРЕДЛОЖЕНИЯ", COVER_KICKER),
    p("Относительные предложения<br/>с ktorý", TITLE),
    p("Vzťažné vety: уточняем человека или предмет без второй отдельной фразы", SUBTITLE),
    Spacer(1, 35 * mm),
    p("Форма <b>ktorý</b> связывает существительное с уточняющим предложением: <b>človek, ktorý pomáha</b>; <b>kniha, ktorú čítam</b>. Род и число берём у существительного, а падеж выбираем по роли внутри придаточной части."),
    p("После модуля вы сможете:", H2),
    styled_table([
        ["1", "выбирать ktorý/ktorá/ktoré/ktorí по существительному"],
        ["2", "различать Nominatív и частотные косвенные формы"],
        ["3", "ставить предлог перед формой: o ktorom, s ktorou, do ktorého"],
        ["4", "размещать уточнение сразу после существительного и отделять запятыми"],
    ], [12 * mm, 158 * mm], font_size=7.2, header=False),
    Spacer(1, 3 * mm),
    box("<b>Формула:</b> существительное <b>, ktorý...</b> Род и число - от существительного; падеж - от функции внутри придаточной части.", PALE, PINK),
    PageBreak(),

    p("1. Nominatív: ktorý сам выполняет действие", H1),
    p("Если уточняемое лицо или предмет является подлежащим придаточной части, используйте Nominatív. Форма согласуется с родом и числом существительного перед запятой."),
    styled_table([
        ["Существительное", "Форма", "Пример"],
        ["muž / kolega", "ktorý", "To je kolega, ktorý pracuje doma."],
        ["žena / firma", "ktorá", "Poznám firmu, ktorá hľadá ľudí."],
        ["auto / mesto", "ktoré", "To je auto, ktoré stojí pred domom."],
        ["muži / študenti", "ktorí", "To sú študenti, ktorí bývajú vedľa."],
        ["ženy / veci / mestá", "ktoré", "To sú knihy, ktoré ležia na stole."],
    ], [42 * mm, 25 * mm, 103 * mm], font_size=6.25),
    p("Из двух фраз в одну", H2),
    styled_table([
        ["Две фразы", "Одно предложение"],
        ["Hľadám lekára. Lekár hovorí po rusky.", "Hľadám lekára, ktorý hovorí po rusky."],
        ["Máme izbu. Izba má balkón.", "Máme izbu, ktorá má balkón."],
        ["Vybral som si tričko. Tričko je lacnejšie.", "Vybral som si tričko, ktoré je lacnejšie."],
    ], [78 * mm, 92 * mm], font_size=6.35),
    box("<b>Проверка:</b> после ktorý/ktorá/ktoré/ktorí сразу идёт сказуемое, потому что относительное местоимение само отвечает на вопрос \"кто/что выполняет действие?\"", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    PageBreak(),

    p("2. Падеж зависит от роли внутри придаточного", H1),
    p("Форма существительного в главной части не определяет падеж <b>ktorý</b>. Сначала мысленно восстановите пропуск внутри придаточного предложения и задайте к нему вопрос."),
    styled_table([
        ["Смысл внутри уточнения", "Форма", "Пример"],
        ["он работает", "N: ktorý", "Poznám muža, ktorý tu pracuje."],
        ["ты ищешь его", "A: ktorého", "Poznám muža, ktorého hľadáš."],
        ["я пишу ему", "D: ktorému", "To je kolega, ktorému píšem."],
        ["мы говорим о нём", "L: o ktorom", "To je projekt, o ktorom hovoríme."],
        ["я работаю с ним", "I: s ktorým", "To je kolega, s ktorým pracujem."],
        ["мы едем до него", "G: do ktorého", "To je mesto, do ktorého cestujeme."],
    ], [52 * mm, 34 * mm, 84 * mm], font_size=6.15),
    p("Главный контраст", H2),
    styled_table([
        ["Фраза", "Роль формы", "Почему"],
        ["Poznám muža, ktorý spieva.", "Nominatív", "мужчина сам поёт"],
        ["Poznám muža, ktorého počúvaš.", "Akuzatív", "ты слушаешь мужчину"],
        ["Poznám muža, o ktorom hovoríš.", "Lokál", "ты говоришь о мужчине"],
    ], [79 * mm, 34 * mm, 57 * mm], font_size=6.25),
    box("<b>Типичная ошибка:</b> *Poznám muža, ktorého pracuje...* Нельзя копировать падеж слова <b>muža</b>. Внутри придаточного мужчина - подлежащее: <b>ktorý pracuje</b>.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    PageBreak(),

    p("3. Частотные формы: женщина и множественное число", H1),
    p("<b>Ktorý</b> склоняется как прилагательное. Для A2 достаточно уверенно узнавать и употреблять формы, которые часто нужны в описании людей, вещей, мест и тем разговора."),
    styled_table([
        ["Падеж", "Муж./ср.", "Женский", "Множественное"],
        ["N", "ktorý / ktoré", "ktorá", "ktorí люди / ktoré прочие"],
        ["A", "ktorého лицо; ktorý/ktoré вещь", "ktorú", "ktorých лица; ktoré прочие"],
        ["D", "ktorému", "ktorej", "ktorým"],
        ["L", "o ktorom", "o ktorej", "o ktorých"],
        ["I", "s ktorým", "s ktorou", "s ktorými"],
    ], [22 * mm, 50 * mm, 43 * mm, 55 * mm], font_size=5.85),
    p("Примеры по моделям", H2),
    styled_table([
        ["SK", "RU"],
        ["To je žena, ktorú som včera stretol.", "Это женщина, которую я вчера встретил."],
        ["To je kolegyňa, ktorej často pomáham.", "Это коллега, которой я часто помогаю."],
        ["To je téma, o ktorej sa učíme.", "Это тема, которую мы изучаем."],
        ["To je kamarátka, s ktorou cestujem.", "Это подруга, с которой я путешествую."],
        ["To sú ľudia, ktorým dôverujem.", "Это люди, которым я доверяю."],
        ["To sú problémy, o ktorých hovoríme.", "Это проблемы, о которых мы говорим."],
        ["To sú kolegovia, s ktorými pracujem.", "Это коллеги, с которыми я работаю."],
    ], [88 * mm, 82 * mm], font_size=6.0),
    box("<b>Предлог ставится перед местоимением:</b> <b>o ktorej, s ktorou, do ktorého, na ktorý</b>. Он относится к роли внутри придаточной части.", PALE, PINK, SMALL),
    PageBreak(),

    p("4. Позиция и запятые", H1),
    p("Относительное предложение ставьте сразу после существительного, которое оно уточняет. Так слушатель без труда понимает, к какому слову относится <b>ktorý</b>."),
    styled_table([
        ["Позиция", "Пример", "Пунктуация"],
        ["в конце", "Hľadám byt, ktorý má balkón.", "запятая перед придаточным"],
        ["в середине", "Muž, ktorý tam čaká, je môj sused.", "запятые с двух сторон"],
        ["в середине", "Kniha, ktorú si mi požičal, je výborná.", "после придаточного запятая"],
    ], [28 * mm, 89 * mm, 53 * mm], font_size=6.2),
    p("Мини-диалог: выбираем квартиру", H2),
    box("<b>Eva:</b> Našiel si byt, ktorý sa ti páči?<br/><b>Martin:</b> Áno. Je to byt, ktorý má veľký balkón.<br/><b>Eva:</b> Je v tej štvrti, o ktorej sme včera hovorili?<br/><b>Martin:</b> Presne. Majiteľ, s ktorým som telefonoval, tam bude o piatej.<br/><b>Eva:</b> A dokumenty, ktoré potrebuješ?<br/><b>Martin:</b> Už mám všetky dokumenty, ktoré si pýtala.", PALE, ROSE, SMALL),
    p("Перевод", H2),
    p("Ты нашёл квартиру, которая тебе нравится? Да. Это квартира с большим балконом. Она в том районе, о котором мы вчера говорили? Именно. Владелец, с которым я говорил по телефону, будет там в пять. А документы, которые тебе нужны? У меня уже есть все документы, которые ты просила.", SMALL),
    box("<b>Не отрывайте уточнение:</b> вместо *Hľadám byt v centre, ktorý má balkón* при возможной неясности лучше <b>Hľadám v centre byt, ktorý má balkón.</b>", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    PageBreak(),

    p("5. Частые ошибки и упражнения", H1),
    box("<b>Частые ошибки:</b> используют одну форму *ktorý для всех родов; копируют падеж существительного из главной части; теряют предлог; забывают вторую запятую у вставленного уточнения.", CREAM, colors.HexColor("#E7C76C"), TINY),
    p("Упражнение 1. Выберите форму Nominatív", H2),
    p("1) kolega, ktorý/ktorá pracuje doma; 2) firma, ktorý/ktorá hľadá ľudí; 3) auto, ktoré/ktorí stojí vonku; 4) študenti, ktoré/ktorí bývajú vedľa.", TINY),
    p("Упражнение 2. Выберите падеж", H2),
    p("1) muž, ktorý/ktorého spieva; 2) muž, ktorý/ktorého hľadáš; 3) projekt, ktorý/o ktorom hovoríme; 4) kolegyňa, ktorá/s ktorou pracujem.", TINY),
    p("Упражнение 3. Вставьте форму", H2),
    p("1) To je žena, ___ som stretol. 2) To je kolega, ___ píšem. 3) To sú ľudia, ___ dôverujem. 4) To je mesto, do ___ cestujeme.", TINY),
    p("Упражнение 4. Поставьте запятые", H2),
    p("1) Muž ktorý tam stojí je lekár. 2) Kniha ktorú čítam je zaujímavá. 3) Hľadám byt ktorý má balkón.", TINY),
    p("Упражнение 5. Соедините и переведите", H2),
    p("1) Это коллега. Я работаю с ним. 2) Это тема. Мы говорим о ней. 3) Я ищу врача. Он говорит по-русски. 4) Это люди. Я им доверяю.", TINY),
    p("Упражнение 6. Опишите выбор", H2),
    p("Напишите 5-7 предложений о квартире, курсе или человеке. Используйте одну форму Nominatív и минимум три косвенные формы, включая одну с предлогом.", TINY),
    PageBreak(),

    p("6. Ответы и проверка мастерства", H1),
    p("Ответы", H2),
    p("<b>1.</b> kolega, ktorý pracuje; firma, ktorá hľadá; auto, ktoré stojí; študenti, ktorí bývajú.", TINY),
    p("<b>2.</b> muž, ktorý spieva; muž, ktorého hľadáš; projekt, o ktorom hovoríme; kolegyňa, s ktorou pracujem.", TINY),
    p("<b>3.</b> žena, ktorú som stretol; kolega, ktorému píšem; ľudia, ktorým dôverujem; mesto, do ktorého cestujeme.", TINY),
    p("<b>4.</b> Muž, ktorý tam stojí, je lekár. Kniha, ktorú čítam, je zaujímavá. Hľadám byt, ktorý má balkón.", TINY),
    p("<b>5.</b> To je kolega, s ktorým pracujem. To je téma, o ktorej hovoríme. Hľadám lekára, ktorý hovorí po rusky. To sú ľudia, ktorým dôverujem.", TINY),
    p("<b>6. Модель:</b> Hľadám kurz, ktorý je praktický. Chcem učiteľa, ktorému môžem dôverovať. Potrebujem skupinu, v ktorej sa veľa rozpráva. Zaujíma ma téma, o ktorej môžem diskutovať. Chcem spolužiakov, s ktorými budem hovoriť po slovensky. Возможны другие естественные варианты.", TINY),
    p("Итог в четырёх пунктах", H2),
    styled_table([
        ["OK", "Род и число формы беру у уточняемого существительного."],
        ["OK", "Падеж выбираю по роли внутри придаточного предложения."],
        ["OK", "Ставлю предлог перед формой: o ktorom, s ktorou."],
        ["OK", "Ставлю уточнение рядом с существительным и отделяю запятыми."],
    ], [12 * mm, 158 * mm], font_size=6.4, header=False),
    Spacer(1, 2 * mm),
    box("<b>Финальная проверка:</b> без таблицы скажите: \"человек, который здесь работает\"; \"женщина, которой я пишу\"; \"проект, о котором мы говорим\".", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    p("Следующий шаг", H2),
    p("В теме 5.5 вы освоите другие придаточные модели с <b>kto, čo</b> и <b>kde</b>.", SMALL),
]

doc.build(story)
print(OUTPUT)
