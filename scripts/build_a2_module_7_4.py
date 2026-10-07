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
OUTPUT = ROOT / "output/pdf/A2/Module_07/Slovak_A2_Tema_7_4_Bilet_marshrut_i_peresadka.pdf"
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
BODY = ParagraphStyle("Body", fontName="Arial", fontSize=8.65, leading=11.3, textColor=INK, spaceAfter=2.7 * mm)
SMALL = ParagraphStyle("Small", parent=BODY, fontSize=7.45, leading=9.2, spaceAfter=1.4 * mm)
TINY = ParagraphStyle("Tiny", parent=BODY, fontSize=6.65, leading=8.1, spaceAfter=0.9 * mm)
TITLE = ParagraphStyle("Title", fontName="Arial-Bold", fontSize=20, leading=24, textColor=colors.white, alignment=TA_LEFT, spaceAfter=5 * mm)
SUBTITLE = ParagraphStyle("Subtitle", fontName="Arial", fontSize=11.5, leading=15, textColor=colors.HexColor("#FFD8EB"), spaceAfter=5 * mm)
H1 = ParagraphStyle("H1", fontName="Arial-Bold", fontSize=15.5, leading=18.5, textColor=PLUM, spaceBefore=1 * mm, spaceAfter=3 * mm)
H2 = ParagraphStyle("H2", fontName="Arial-Bold", fontSize=10.7, leading=13.2, textColor=PINK, spaceBefore=1.1 * mm, spaceAfter=1.4 * mm)
KICK = ParagraphStyle("Kicker", fontName="Arial-Bold", fontSize=10, leading=12, textColor=colors.HexColor("#FFD8EB"), spaceAfter=4 * mm)


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
            f"cell_{row_index}_{size}_{len(data)}", parent=SMALL, fontSize=size, leading=size + 1.75,
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
        canvas.drawString(20 * mm, height - 12 * mm, "A2 7.4  |  Билет, маршрут и пересадка")
    canvas.setFont("Arial", 8)
    canvas.setFillColor(MUTED)
    canvas.drawString(20 * mm, 9 * mm, "SlovoKrok | личный учебный модуль")
    canvas.drawRightString(width - 20 * mm, 9 * mm, f"стр. {page_number} / 7")
    canvas.restoreState()


doc = BaseDocTemplate(
    str(OUTPUT), pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=20 * mm, bottomMargin=18 * mm,
    title="Slovak A2 - Тема 7.4 - Билет, маршрут и пересадка", author="SlovoKrok",
)
doc.addPageTemplates([PageTemplate(id="series", frames=[Frame(20 * mm, 18 * mm, 170 * mm, 257 * mm, id="main", leftPadding=0, rightPadding=0)], onPage=draw_page)])


story = [
    p("МОДУЛЬ 7  •  РАБОТА, ПУТЕШЕСТВИЯ И СТРАНА", KICK),
    p("Билет, маршрут и пересадка", TITLE),
    p("Lístok, trasa a prestup: выбираем рейс, покупаем билет и понимаем объявление", SUBTITLE),
    Spacer(1, 41 * mm),
    p("На уровне A2 важно не просто назвать пункт назначения. Нужно сравнить два рейса, купить подходящий билет, понять время и платформу в объявлении и уточнить пересадку."),
    p("После модуля вы сможете:", H2),
    table([
        ["1", "выбрать прямой рейс или маршрут с пересадкой"],
        ["2", "купить билет и уточнить время отправления"],
        ["3", "сказать, где вы, куда и откуда едете"],
        ["4", "понять задержку, платформу и место пересадки"],
    ], [12 * mm, 158 * mm], 7.2, False),
    Spacer(1, 3 * mm),
    box("<b>Формула поездки:</b> откуда → куда → какой рейс → во сколько → с какой платформы → где пересадка."),
    PageBreak(),

    p("1. Как выбрать маршрут", H1),
    p("Сначала найдите <b>odchod</b> (отправление), <b>príchod</b> (прибытие), длительность пути и число пересадок. <b>Priamy spoj</b> идёт без пересадки; <b>spoj s prestupom</b> требует сменить поезд или автобус."),
    table([
        ["Слово", "Значение", "Пример"],
        ["spoj", "рейс, сообщение", "Tento spoj ide do Žiliny."],
        ["odchod / príchod", "отправление / прибытие", "Odchod je o 8.25, príchod o 10.40."],
        ["priamy spoj", "прямой рейс", "Je to priamy spoj bez prestupu."],
        ["prestup", "пересадка", "V Trnave máme jeden prestup."],
        ["nástupište", "платформа", "Vlak odchádza z tretieho nástupišťa."],
        ["prípojný vlak", "стыковочный поезд", "Prípojný vlak čaká desať minút."],
        ["meškanie", "опоздание", "Vlak má pätnásť minút meškanie."],
    ], [34 * mm, 44 * mm, 92 * mm], 5.45),
    p("Глаголы движения", H2),
    table([
        ["Глагол", "Что происходит", "Пример"],
        ["ísť", "ехать / идти", "Ideme vlakom do Košíc."],
        ["odísť / prísť", "уехать / приехать", "Vlak odíde o deviatej a príde o jedenástej."],
        ["nastúpiť", "сесть в транспорт", "Nastúpime do autobusu číslo 61."],
        ["vystúpiť", "выйти", "Vystúpte na hlavnej stanici."],
        ["prestúpiť", "пересесть", "V Žiline prestúpime na rýchlik."],
    ], [32 * mm, 48 * mm, 90 * mm], 5.45),
    box("<b>Выбор:</b> <i>Priamy vlak ide o 9.10 a príde o 11.45. Skorší vlak ide o 8.25, ale v Trnave treba prestúpiť.</i>", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    PageBreak(),

    p("2. Kde, kam, odkiaľ", H1),
    p("Три вопроса организуют весь маршрут. <b>Kde?</b> — место без движения; <b>Kam?</b> — направление; <b>Odkiaľ?</b> — исходная точка. Запоминайте вопрос вместе с предлогом и формой слова."),
    table([
        ["Вопрос", "Модель", "Примеры"],
        ["Kde? где?", "v/na + L", "v Bratislave; na stanici; na nástupišti"],
        ["Kam? куда?", "do + G", "do Košíc; do centra; do autobusu"],
        ["Kam? куда?", "na + A", "na stanicu; na nástupište; na zastávku"],
        ["Kam? к чему?", "k + D", "k pokladnici; k východu"],
        ["Odkiaľ? откуда?", "z/zo + G", "z Bratislavy; zo stanice; z nástupišťa"],
        ["Kadial? через что?", "cez + A", "cez Žilinu; cez centrum"],
    ], [31 * mm, 39 * mm, 100 * mm], 5.7),
    p("Маршрут одной цепочкой", H2),
    box("<b>Odkiaľ cestujete?</b> — Cestujem <b>z Bratislavy</b>.<br/><b>Kam cestujete?</b> — Idem <b>do Košíc</b> cez Žilinu.<br/><b>Kde prestupujete?</b> — Prestupujem <b>v Žiline</b>.<br/><b>Kam potom idete?</b> — Idem <b>na druhé nástupište</b> a nastúpim <b>do rýchlika</b>.", PALE, ROSE, SMALL),
    p("Направление и положение", H2),
    table([
        ["Движение", "Место", "Перевод"],
        ["Idem na stanicu.", "Som na stanici.", "иду на вокзал / я на вокзале"],
        ["Idem na nástupište.", "Čakám na nástupišti.", "иду на платформу / жду на платформе"],
        ["Idem do centra.", "Som v centre.", "еду в центр / я в центре"],
        ["Vystúpim z vlaku.", "Sedím vo vlaku.", "выйду из поезда / сижу в поезде"],
    ], [57 * mm, 57 * mm, 56 * mm], 5.65),
    box("<b>Не смешивайте:</b> <i>na stanici</i> отвечает на <i>kde?</i>, а <i>na stanicu</i> — на <i>kam?</i>. После <i>z/zo</i> и <i>do</i> нужен родительный падеж.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    PageBreak(),

    p("3. Покупаем билет и говорим о времени", H1),
    p("У кассы назовите направление, тип билета, класс и время. Если нужна пересадка, уточните её место и запас времени."),
    table([
        ["Нужно", "Фраза"],
        ["один билет", "Prosím si jeden lístok do Banskej Bystrice."],
        ["туда и обратно", "Prosím si spiatočný lístok do Trenčína."],
        ["только туда", "Chcem jednosmerný lístok do Nitry."],
        ["класс / место", "Druhú triedu a jednu miestenku, prosím."],
        ["время", "Kedy odchádza najbližší vlak?"],
        ["пересадка", "Kde musím prestúpiť?"],
        ["платформа", "Z ktorého nástupišťa vlak odchádza?"],
    ], [46 * mm, 124 * mm], 5.8),
    p("Мини-диалог у кассы", H2),
    box("<b>Cestujúci:</b> Dobrý deň, prosím si jeden spiatočný lístok z Bratislavy do Žiliny.<br/><b>Pokladníčka:</b> Kedy chcete cestovať?<br/><b>Cestujúci:</b> Dnes o desiatej a späť zajtra večer. Je to priamy vlak?<br/><b>Pokladníčka:</b> Cestou tam prestúpite v Trnave. Na prestup máte dvanásť minút.<br/><b>Cestujúci:</b> Rozumiem. Druhú triedu a miestenku, prosím. Z ktorého nástupišťa vlak odchádza?<br/><b>Pokladníčka:</b> Zo štvrtého nástupišťa.", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    p("Время в пути", H2),
    table([
        ["Фраза", "Значение"],
        ["Vlak odchádza o 8.25.", "Поезд отправляется в 8:25."],
        ["Príde desať minút po deviatej.", "Он прибудет в 9:10."],
        ["Autobus príde za desať minút.", "Автобус приедет через 10 минут."],
        ["Cesta trvá dve hodiny.", "Дорога длится два часа."],
        ["Vlak mešká dvadsať minút.", "Поезд опаздывает на 20 минут."],
    ], [82 * mm, 88 * mm], 5.6),
    PageBreak(),

    p("4. Объявление и пересадка", H1),
    p("В объявлении не нужно понимать каждое слово. Слушайте четыре опоры: <b>рейс</b>, <b>задержка</b>, <b>платформа</b>, <b>пересадка</b>. Числа и названия станций важнее служебных формул."),
    p("Контролируемое аудирование", H2),
    box("<b>Hlásenie:</b> Pozor, zmena! Rýchlik číslo 603 do Košíc bude meškať pätnásť minút. Vlak príde na druhé nástupište ku koľaji číslo štyri. Cestujúci do Popradu prestúpia v Žiline na prípojný vlak číslo 341. Prípojný vlak počká na meškajúci rýchlik.", PALE, ROSE, SMALL),
    table([
        ["Что услышать", "Ответ", "Подсказка в тексте"],
        ["какой рейс?", "скорый поезд 603 до Кошице", "Rýchlik číslo 603 do Košíc"],
        ["какая задержка?", "15 минут", "meškať pätnásť minút"],
        ["куда прибывает?", "платформа 2, путь 4", "druhé nástupište ku koľaji číslo štyri"],
        ["где пересадка?", "в Жилине", "prestúpia v Žiline"],
        ["что со стыковкой?", "стыковочный поезд подождёт", "prípojný vlak počká"],
    ], [42 * mm, 53 * mm, 75 * mm], 5.4),
    p("Как тренироваться без аудиофайла", H2),
    table([
        ["1", "Закройте таблицу и прочитайте объявление вслух один раз в обычном темпе."],
        ["2", "Прочитайте или прослушайте через TTS второй раз; запишите только 603 / 15 / 2 / 4 / Žilina / 341."],
        ["3", "Откройте таблицу, проверьте опоры и перескажите маршрут двумя фразами."],
    ], [11 * mm, 159 * mm], 6.0, False),
    p("Фразы для уточнения", H2),
    box("<i>Prosím, zopakujte číslo nástupišťa. — Čaká prípojný vlak? — Koľko času mám na prestup? — Je prestup na tom istom nástupišti? — Kde nájdem koľaj číslo štyri?</i>", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    PageBreak(),

    p("5. Частые ошибки и упражнения", H1),
    table([
        ["Ошибка", "Правильно", "Почему"],
        ["*Idem v Košiciach.", "Idem do Košíc.", "направление: kam?"],
        ["*Som na stanicu.", "Som na stanici.", "место: kde?"],
        ["*Cestujem z Bratislava.", "Cestujem z Bratislavy.", "z + родительный"],
        ["*Prestupujem na Žiline.", "Prestupujem v Žiline.", "город: v + местный"],
        ["*Vlak mešká za 15 minút.", "Vlak mešká 15 minút.", "длительность опоздания без za"],
    ], [50 * mm, 56 * mm, 64 * mm], 5.35),
    p("Упражнение 1. Выберите kde / kam / odkiaľ", H2),
    p("1) ___ cestujete? — Do Prešova.  2) ___ prestupujete? — V Žiline.  3) ___ ide tento vlak? — Z Bratislavy.  4) ___ je pokladnica? — Na stanici.", SMALL),
    p("Упражнение 2. Поставьте слово в нужную форму", H2),
    p("1) Idem do (Košice).  2) Čakám na (nástupište).  3) Vystúpim z (autobus).  4) Prestúpime v (Trnava).  5) Ideme cez (Žilina).", SMALL),
    p("Упражнение 3. Выберите глагол", H2),
    p("<i>nastúpiť / vystúpiť / prestúpiť / prísť</i>: 1) V Žiline musíme ___ na rýchlik. 2) Do autobusu ___ prednými dverami. 3) Na hlavnej stanici ___. 4) Vlak má ___ o 18.40.", SMALL),
    p("Упражнение 4. Прочитайте табло", H2),
    table([
        ["Spoj", "Odchod", "Príchod", "Prestup"],
        ["R 801", "8.25", "10.40", "bez prestupu"],
        ["Os 303 + R 605", "8.05", "10.25", "Trnava, 9 min."],
    ], [42 * mm, 38 * mm, 38 * mm, 52 * mm], 5.6),
    p("Ответьте: a) Ktorý spoj odchádza skôr? b) Ktorý spoj je priamy? c) Koľko času je na prestup? d) Ktorý spoj príde skôr?", SMALL),
    p("Упражнение 5. Восстановите вопрос у кассы", H2),
    p("1) ___? — Jeden spiatočný lístok do Nitry. 2) ___? — O 14.10. 3) ___? — Z piateho nástupišťa. 4) ___? — V Trnave.", SMALL),
    p("Упражнение 6. Поймите объявление", H2),
    p("По объявлению на стр. 5 запишите: номер и направление поезда; задержку; платформу и путь; место пересадки; действие стыковочного поезда.", SMALL),
    PageBreak(),

    p("6. Ответы и проверка мастерства", H1),
    p("Ответы", H2),
    table([
        ["№", "Ключ"],
        ["1", "1 Kam; 2 Kde; 3 Odkiaľ; 4 Kde."],
        ["2", "1 Košíc; 2 nástupišti; 3 autobusu; 4 Trnave; 5 Žilinu."],
        ["3", "1 prestúpiť; 2 nastúpime; 3 vystúpime; 4 prísť."],
        ["4", "a Os 303 o 8.05; b R 801; c 9 minút; d Os 303 + R 605 o 10.25."],
        ["5", "Возможный ключ: Čo si prosíte? / Kedy vlak odchádza? / Z ktorého nástupišťa odchádza? / Kde musím prestúpiť?"],
        ["6", "Rýchlik 603 do Košíc; 15 minút; druhé nástupište, koľaj 4; v Žiline; prípojný vlak počká."],
    ], [13 * mm, 157 * mm], 5.5),
    p("Модель: от кассы до пересадки", H2),
    box("<b>Dobrý deň, prosím si jeden jednosmerný lístok z Bratislavy do Popradu. Chcem cestovať dnes poobede. Kedy odchádza najbližší vlak? Musím niekde prestúpiť? Koľko času mám na prestup a z ktorého nástupišťa odchádza prípojný vlak?</b><br/><br/>Po oznámení: <i>Rýchlik mešká pätnásť minút, ale prípojný vlak v Žiline počká. Vlak príde na druhé nástupište ku koľaji číslo štyri.</i>", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    p("Финальная проверка", H2),
    table([
        ["Могу...", "Да / ещё раз"],
        ["сравнить прямой рейс и маршрут с пересадкой", "□ / □"],
        ["купить билет, назвать класс и время", "□ / □"],
        ["правильно ответить на kde / kam / odkiaľ", "□ / □"],
        ["услышать задержку, платформу и пересадку", "□ / □"],
        ["уточнить место и запас времени на пересадку", "□ / □"],
    ], [128 * mm, 42 * mm], 5.75),
    box("<b>Критерий освоения:</b> не менее 5 из 6 упражнений без подсказки и устный маршрут из 5 фраз: откуда, куда, время, платформа, пересадка.", PALE, ROSE, SMALL),
]

doc.build(story)
print(OUTPUT)
