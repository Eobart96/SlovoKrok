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
OUTPUT = ROOT / "output/pdf/A2/Module_07/Slovak_A2_Tema_7_6_Istoriya_puteshestviya.pdf"
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
        canvas.drawString(20 * mm, height - 12 * mm, "A2 7.6  |  История путешествия")
    canvas.setFont("Arial", 8)
    canvas.setFillColor(MUTED)
    canvas.drawString(20 * mm, 9 * mm, "SlovoKrok | личный учебный модуль")
    canvas.drawRightString(width - 20 * mm, 9 * mm, f"стр. {page_number} / 7")
    canvas.restoreState()


doc = BaseDocTemplate(
    str(OUTPUT), pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=20 * mm, bottomMargin=18 * mm,
    title="Slovak A2 - Тема 7.6 - История путешествия", author="SlovoKrok",
)
doc.addPageTemplates([PageTemplate(id="series", frames=[Frame(20 * mm, 18 * mm, 170 * mm, 257 * mm, id="main", leftPadding=0, rightPadding=0)], onPage=draw_page)])


story = [
    p("A2 7.6  •  МОДУЛЬ 7  •  РАБОТА, ПУТЕШЕСТВИЯ И СТРАНА", KICK),
    p("История путешествия", TITLE),
    p("Príbeh z cesty: фон, цепочка событий, неожиданность и итог", SUBTITLE),
    Spacer(1, 41 * mm),
    p("На уровне A2 рассказ о поездке — это не перечень мест. Слушателю нужны исходная ситуация, несколько событий по порядку, одна неожиданность и понятный итог."),
    p("После модуля вы сможете:", H2),
    table([
        ["1", "задать фон рассказа в прошедшем времени"],
        ["2", "различать процесс и завершённые события"],
        ["3", "естественно использовать возвратные глаголы"],
        ["4", "связать неожиданность, решение и итог поездки"],
    ], [12 * mm, 158 * mm], 7.2, False),
    Spacer(1, 3 * mm),
    box("<b>Формула истории:</b> когда и где → что происходило → что случилось → что мы сделали → чем всё закончилось."),
    PageBreak(),

    p("1. Каркас рассказа: фон и события", H1),
    p("Прошедшее время уже знакомо с A1. Здесь задача A2 — распределить информацию: несовершенный вид создаёт фон или процесс, а совершенный продвигает историю к следующему событию."),
    table([
        ["Роль", "Словацкий пример", "Перевод"],
        ["время и место", "Minulé leto sme cestovali po Slovensku.", "Прошлым летом мы путешествовали по Словакии."],
        ["фон", "Bývali sme v malom penzióne pri lese.", "Мы жили в небольшом пансионе у леса."],
        ["процесс", "Celé dopoludnie sme chodili po meste.", "Всё утро мы ходили по городу."],
        ["событие", "Navštívili sme hrad a odfotili starý most.", "Мы посетили замок и сфотографировали старый мост."],
        ["неожиданность", "Zrazu sa pokazil náš autobus.", "Вдруг наш автобус сломался."],
        ["решение", "Zavolali sme do penziónu a dočkali sme sa pomoci.", "Мы позвонили в пансион и дождались помощи."],
        ["итог", "Nakoniec sme bezpečne dorazili do cieľa.", "В конце концов мы благополучно добрались до цели."],
    ], [34 * mm, 77 * mm, 59 * mm], 5.35),
    p("Одна история — две линии", H2),
    table([
        ["Фон: что длилось", "Цепочка: что произошло"],
        ["Bolo teplo a svietilo slnko.", "Ráno sme vyšli z hotela."],
        ["Cestovali sme úzkou horskou cestou.", "Zastavili sme sa pri jazere."],
        ["Počas cesty sme sa rozprávali.", "Potom sme pokračovali do dediny."],
        ["Čakali sme takmer hodinu.", "Nakoniec prišiel náhradný autobus."],
    ], [85 * mm, 85 * mm], 5.55),
    box("<b>Учебный ориентир:</b> фон отвечает «что происходило?», завершённое событие — «что произошло дальше?». Не превращайте весь рассказ в одну длинную цепочку одинаковых форм.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    PageBreak(),

    p("2. Вид и неожиданное событие", H1),
    p("Неожиданность обычно прерывает процесс. Удобная модель: <b>keď + процесс, совершенное событие</b>. Для двух одновременных процессов используйте <b>kým</b>."),
    table([
        ["Связь", "Пример", "Что показывает"],
        ["keď", "Keď sme išli do Popradu, pokazil sa autobus.", "событие прервало дорогу"],
        ["keď", "Keď sme hľadali hotel, stratili sme mapu.", "результат во время поиска"],
        ["kým", "Kým sme čakali, pili sme čaj.", "два параллельных процесса"],
        ["zrazu", "Zrazu začalo silno pršať.", "резкий поворот истории"],
        ["preto", "Zmeškali sme vlak, preto sme išli autobusom.", "причина и решение"],
        ["našťastie", "Našťastie nám pomohol miestny vodič.", "оценка удачного исхода"],
    ], [30 * mm, 83 * mm, 57 * mm], 5.35),
    p("Глагольный выбор", H2),
    table([
        ["Процесс / повтор", "Завершённый результат", "Контраст"],
        ["hľadali sme hotel", "našli sme hotel", "искали / нашли"],
        ["čakali sme na autobus", "dočkali sme sa pomoci", "ждали / дождались"],
        ["fotografovali sme mesto", "odfotili sme most", "фотографировали / сфотографировали"],
        ["vracali sme sa večer", "vrátili sme sa o desiatej", "возвращались / вернулись"],
    ], [59 * mm, 61 * mm, 50 * mm], 5.45),
    box("<b>Мини-сцена:</b> <i>Keď sme sa vracali z výletu, začalo pršať. Hľadali sme zastávku, ale stratili sme sa. Našťastie sme stretli ženu, ktorá nám ukázala cestu.</i>", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    PageBreak(),

    p("3. Возвратные глаголы в истории", H1),
    p("Частица <b>sa/si</b> — часть глагола или его значения. В прошедшем времени она обычно стоит после первого ударного элемента: <i>Ubytovali sme sa. Včera sme sa ubytovali.</i>"),
    table([
        ["Глагол", "Пример", "Перевод"],
        ["tešiť sa na + A", "Tešili sme sa na výlet do hôr.", "Мы радовались предстоящей поездке в горы."],
        ["ubytovať sa v + L", "Večer sme sa ubytovali v penzióne.", "Вечером мы заселились в пансион."],
        ["stratiť sa", "V centre sme sa na chvíľu stratili.", "В центре мы ненадолго заблудились."],
        ["rozhodnúť sa + infinitív", "Rozhodli sme sa pokračovať pešo.", "Мы решили продолжить пешком."],
        ["vrátiť sa", "Do hotela sme sa vrátili neskoro.", "В гостиницу мы вернулись поздно."],
        ["oddýchnuť si", "Po ceste sme si trochu oddýchli.", "После дороги мы немного отдохнули."],
        ["všimnúť si + A", "Všimli sme si nesprávne číslo autobusu.", "Мы заметили неправильный номер автобуса."],
    ], [43 * mm, 75 * mm, 52 * mm], 5.25),
    p("Порядок слов", H2),
    table([
        ["Начало фразы", "Естественный порядок"],
        ["без вводного слова", "Ubytovali sme sa blízko stanice."],
        ["время в начале", "Večer sme sa ubytovali blízko stanice."],
        ["две частицы", "Po večeri sme si oddýchli."],
        ["отрицание", "V novom meste sme sa nestratili."],
    ], [49 * mm, 121 * mm], 5.6),
    box("<b>Запоминайте управление:</b> в значении «решить сделать» используйте <i>rozhodnúť sa + infinitív</i>, а в значении «отдохнуть» — <i>oddýchnuť si</i>. Частица входит в нужную здесь модель.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    PageBreak(),

    p("4. Последовательность и итог рассказа", H1),
    p("Связки помогают слушателю не потеряться. Не ставьте <i>potom</i> перед каждым предложением: чередуйте начало, поворот, причину, решение и итог."),
    table([
        ["Шаг", "Связка", "Пример"],
        ["начало", "najprv", "Najprv sme si pozreli historické centrum."],
        ["следующий шаг", "potom / neskôr", "Neskôr sme nastúpili do autobusu."],
        ["одновременность", "medzitým", "Medzitým sa počasie zhoršilo."],
        ["поворот", "zrazu", "Zrazu vodič zastavil pri ceste."],
        ["следствие", "preto", "Preto sme museli zmeniť plán."],
        ["удачный исход", "našťastie", "Našťastie prišiel náhradný autobus."],
        ["завершение", "nakoniec", "Nakoniec sme dorazili iba hodinu neskôr."],
    ], [31 * mm, 36 * mm, 103 * mm], 5.4),
    p("Модель связного рассказа", H2),
    box("Minulú jeseň sme išli s priateľmi na víkend do Banskej Štiavnice. Bývali sme v malom penzióne neďaleko centra. V sobotu ráno bolo chladno, ale svietilo slnko. Najprv sme si pozreli námestie a starý zámok. Keď sme sa vracali do penziónu, zrazu sa nám pokazilo auto. Kým sme čakali na pomoc, začalo pršať. Našťastie majiteľ penziónu zavolal miestneho mechanika. Auto opravil a večer sme sa bezpečne vrátili. Nakoniec sa výlet vydaril, hoci sme mali nečakaný problém. Najviac sa mi páčila pokojná atmosféra mesta.", PALE, ROSE, SMALL),
    p("Сильный итог", H2),
    table([
        ["Что сообщить", "Фраза"],
        ["общая оценка", "Výlet sa nám veľmi páčil."],
        ["лучший момент", "Najväčším zážitkom bola návšteva zámku."],
        ["урок", "Poučili sme sa, že treba mať plán B."],
        ["желание", "Do Banskej Štiavnice sa chceme vrátiť."],
    ], [48 * mm, 122 * mm], 5.55),
    PageBreak(),

    p("5. Частые ошибки и упражнения", H1),
    table([
        ["Ошибка", "Правильно", "Почему"],
        ["*včera sme išli a pršalo zrazu", "zrazu začalo pršať", "для поворота нужен момент начала"],
        ["*sme sa včera stratili", "včera sme sa stratili", "sa следует за первым элементом"],
        ["*rozhodli sme pokračovať", "rozhodli sme sa pokračovať", "sa — часть глагола"],
        ["*celú hodinu sme počkali", "celú hodinu sme čakali", "длительный процесс: несовершенный вид"],
        ["*nakoniec sme vracali", "nakoniec sme sa vrátili", "возвратность и завершённость"],
    ], [55 * mm, 57 * mm, 58 * mm], 5.2),
    p("Упражнение 1. Фон или событие?", H2),
    p("Отметьте F (фон/процесс) или S (событие): 1) Bývali sme pri jazere. 2) Zrazu sa pokazil autobus. 3) Celý deň pršalo. 4) Zavolali sme pomoc. 5) Čakali sme hodinu.", SMALL),
    p("Упражнение 2. Выберите вид", H2),
    p("1) Dlho sme (hľadali / našli) hotel. 2) Nakoniec sme ho (hľadali / našli). 3) Celou cestou sme mesto (fotografovali / odfotili). 4) Na námestí sme (fotografovali / odfotili) starú radnicu.", SMALL),
    p("Упражнение 3. Вставьте sa или si", H2),
    p("1) Večer sme ___ ubytovali. 2) Po obede sme ___ oddýchli. 3) V centre sme ___ stratili. 4) Všimli sme ___ zlý smer. 5) Rozhodli sme ___ pokračovať pešo.", SMALL),
    p("Упражнение 4. Расставьте события", H2),
    p("Поставьте связки <i>najprv, zrazu, preto, našťastie, nakoniec</i>: ___ sme vyšli z hotela. ___ začalo pršať. ___ sme vošli do kaviarne. ___ nám čašník zavolal taxík. ___ sme prišli na stanicu včas.", SMALL),
    p("Упражнение 5. Исправьте рассказ", H2),
    p("<i>Včera sme sa išli do hôr. Keď sme kráčali, zrazu pršalo. Rozhodli sme vrátiť. Nakoniec sme vracali do hotela.</i>", SMALL),
    p("Упражнение 6. Расскажите свою историю", H2),
    p("Напишите 7–8 фраз: фон, два завершённых события, неожиданность с <i>keď/zrazu</i>, один возвратный глагол, решение и итог с <i>nakoniec</i>.", SMALL),
    PageBreak(),

    p("6. Ответы и проверка мастерства", H1),
    p("Ответы", H2),
    table([
        ["№", "Ключ"],
        ["1", "1 F; 2 S; 3 F; 4 S; 5 F."],
        ["2", "1 hľadali; 2 našli; 3 fotografovali; 4 odfotili."],
        ["3", "1 sa; 2 si; 3 sa; 4 si; 5 sa."],
        ["4", "Najprv; zrazu; preto; našťastie; nakoniec."],
        ["5", "Včera sme išli do hôr. Keď sme kráčali, zrazu začalo pršať. Rozhodli sme sa vrátiť. Nakoniec sme sa vrátili do hotela."],
        ["6", "Возможны разные ответы; проверьте фон, цепочку, неожиданность, sa/si, решение и итог."],
    ], [13 * mm, 157 * mm], 5.35),
    p("Модель самостоятельного рассказа", H2),
    box("Minulé leto sme cestovali vlakom do Tatier. Bývali sme v penzióne pri stanici a každý deň sme chodili na túru. V sobotu sme vyšli veľmi skoro a odfotili sme krásne jazero. Keď sme sa vracali, zrazu sme si všimli, že nemáme mapu. Chvíľu sme hľadali správnu cestu, ale potom sme sa rozhodli zavolať horskému sprievodcovi. Našťastie nám vysvetlil, kadiaľ máme ísť. Nakoniec sme sa bezpečne vrátili a poučili sme sa, že mapu treba vždy skontrolovať.", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    p("Финальная проверка", H2),
    table([
        ["Могу...", "Да / ещё раз"],
        ["задать фон истории в прошедшем времени", "□ / □"],
        ["различить процесс и завершённое событие", "□ / □"],
        ["поставить sa/si в естественную позицию", "□ / □"],
        ["передать неожиданность и решение", "□ / □"],
        ["закончить рассказ итогом и личной оценкой", "□ / □"],
    ], [128 * mm, 42 * mm], 5.65),
    box("<b>Критерий освоения:</b> не менее 5 из 6 упражнений без подсказки и связная история из 7–8 фраз, где ясно различаются фон, поворот, решение и итог.", PALE, ROSE, SMALL),
]

doc.build(story)
print(OUTPUT)
