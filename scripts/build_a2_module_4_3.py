from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output" / "pdf" / "A2" / "Module_04" / "Slovak_A2_Tema_4_3_Vidovye_pary_s_suffiksami_i_izmeneniem_osnovy.pdf"
TITLE = "Slovak A2 - Тема 4.3 - Видовые пары с суффиксами и изменением основы"

PLUM = colors.HexColor("#7B245F")
PINK = colors.HexColor("#CE3C92")
PALE = colors.HexColor("#FFF0F7")
ROSE = colors.HexColor("#EACDD9")
ALT = colors.HexColor("#FFF8FA")
BLUE = colors.HexColor("#EAF2FA")
GREEN = colors.HexColor("#E2F3E8")
CREAM = colors.HexColor("#FFF5E5")
INK = colors.HexColor("#30272E")
MUTED = colors.HexColor("#705E68")
WHITE = colors.white


def register_fonts():
    regular = next(p for p in [Path("C:/Windows/Fonts/arial.ttf"), Path("C:/Windows/Fonts/calibri.ttf")] if p.exists())
    bold = next(p for p in [Path("C:/Windows/Fonts/arialbd.ttf"), Path("C:/Windows/Fonts/calibrib.ttf")] if p.exists())
    pdfmetrics.registerFont(TTFont("SK", str(regular)))
    pdfmetrics.registerFont(TTFont("SK-Bold", str(bold)))


register_fonts()
ST = {
    "cover_kicker": ParagraphStyle("cover_kicker", fontName="SK-Bold", fontSize=14, leading=18, textColor=colors.HexColor("#F8D8E9"), alignment=TA_CENTER, spaceAfter=8),
    "cover_title": ParagraphStyle("cover_title", fontName="SK-Bold", fontSize=25, leading=30, textColor=WHITE, alignment=TA_CENTER, spaceAfter=11),
    "cover_sub": ParagraphStyle("cover_sub", fontName="SK", fontSize=12.2, leading=17, textColor=WHITE, alignment=TA_CENTER),
    "h1": ParagraphStyle("h1", fontName="SK-Bold", fontSize=20, leading=24, textColor=PLUM, spaceAfter=8),
    "h2": ParagraphStyle("h2", fontName="SK-Bold", fontSize=13.5, leading=17, textColor=PLUM, spaceBefore=6, spaceAfter=5),
    "body": ParagraphStyle("body", fontName="SK", fontSize=9.5, leading=13.1, textColor=INK, spaceAfter=4),
    "small": ParagraphStyle("small", fontName="SK", fontSize=8.4, leading=11.5, textColor=MUTED, spaceAfter=2),
    "box": ParagraphStyle("box", fontName="SK", fontSize=9.15, leading=12.7, textColor=INK),
    "box_b": ParagraphStyle("box_b", fontName="SK-Bold", fontSize=9.4, leading=12.8, textColor=PLUM),
    "ex": ParagraphStyle("ex", fontName="SK", fontSize=9.05, leading=12.35, textColor=INK, leftIndent=6, spaceAfter=3),
    "task": ParagraphStyle("task", fontName="SK", fontSize=8.65, leading=11.75, textColor=INK, spaceAfter=4),
    "answer": ParagraphStyle("answer", fontName="SK", fontSize=8.2, leading=11.0, textColor=INK, spaceAfter=3),
}


def P(text, style="body"):
    return Paragraph(text, ST[style])


def callout(title, text, color=PALE, width=169):
    t = Table([[P(title, "box_b")], [P(text, "box")]], colWidths=[width * mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), color), ("BOX", (0, 0), (-1, -1), 0.7, ROSE),
        ("LINEBELOW", (0, 0), (-1, 0), 0.45, ROSE),
        ("LEFTPADDING", (0, 0), (-1, -1), 8), ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    return t


def grid(rows, widths, header=True, font="small"):
    data = [[P(cell, "box_b" if header and i == 0 else font) for cell in row] for i, row in enumerate(rows)]
    t = Table(data, colWidths=[w * mm for w in widths], repeatRows=1 if header else 0)
    rules = [
        ("GRID", (0, 0), (-1, -1), 0.45, ROSE), ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6), ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]
    if header:
        rules.append(("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#F5D4E5")))
    for row in range(1 if header else 0, len(data)):
        if row % 2 == 0:
            rules.append(("BACKGROUND", (0, row), (-1, row), ALT))
    t.setStyle(TableStyle(rules))
    return t


def first_page(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(PLUM)
    canvas.rect(0, 0, A4[0], A4[1], fill=1, stroke=0)
    canvas.setFillColor(colors.HexColor("#9E2F74"))
    canvas.circle(18 * mm, 266 * mm, 37 * mm, fill=1, stroke=0)
    canvas.circle(194 * mm, 28 * mm, 49 * mm, fill=1, stroke=0)
    canvas.setFillColor(colors.HexColor("#F8D8E9"))
    canvas.roundRect(27 * mm, 34 * mm, 156 * mm, 38 * mm, 5 * mm, fill=1, stroke=0)
    canvas.setFillColor(PLUM)
    canvas.setFont("SK-Bold", 11)
    canvas.drawCentredString(105 * mm, 57 * mm, "ДВЕ ФОРМЫ + ОДНО ЗНАЧЕНИЕ + УПРАВЛЕНИЕ")
    canvas.setFont("SK", 9)
    canvas.drawCentredString(105 * mm, 47 * mm, "dve podoby + jeden význam + väzba")
    canvas.setFillColor(colors.HexColor("#F8D8E9"))
    canvas.setFont("SK", 7.5)
    canvas.drawCentredString(105 * mm, 13 * mm, "стр. 1 / 7")
    canvas.restoreState()


def later_page(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(ROSE)
    canvas.setLineWidth(0.7)
    canvas.line(20 * mm, 281 * mm, 190 * mm, 281 * mm)
    canvas.setFillColor(PLUM)
    canvas.setFont("SK-Bold", 8)
    canvas.drawString(20 * mm, 285 * mm, "SLOVOKROK  |  A2  |  ТЕМА 4.3  |  ВИДОВЫЕ ПАРЫ")
    canvas.setFillColor(MUTED)
    canvas.setFont("SK", 7.5)
    canvas.drawCentredString(105 * mm, 10 * mm, f"стр. {doc.page} / 7")
    canvas.restoreState()


doc = SimpleDocTemplate(str(OUT), pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm,
                        topMargin=26 * mm, bottomMargin=17 * mm, title=TITLE,
                        author="SlovoKrok", subject="Slovak A2 self-study module 4.3")
story = []

# 1. Cover
story += [Spacer(1, 25 * mm), P("SLOVOKROK • СЛОВАЦКИЙ A2", "cover_kicker"),
          P("ТЕМА 4.3", "cover_kicker"),
          P("Видовые пары<br/>с суффиксами<br/>и изменением основы", "cover_title"),
          P("Vidové dvojice so zmenou kmeňa", "cover_sub"), Spacer(1, 16 * mm),
          Table([[P("После модуля вы сможете", "box_b")],
                 [P("• узнавать четыре частотные пары без опоры на приставку;<br/>• различать изменение суффикса и полную смену основы;<br/>• учитывать значение и управление каждой формы;<br/>• вести надёжную словарную запись пары.", "box")]],
                colWidths=[145 * mm], style=TableStyle([
                    ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#FFF7FB")),
                    ("LEFTPADDING", (0, 0), (-1, -1), 10), ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                    ("TOPPADDING", (0, 0), (-1, -1), 7), ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
                ])), PageBreak()]

# 2. System
story += [P("1. Пара не обязана выглядеть похоже", "h1"),
          P("В теме 4.2 вид часто был виден по приставке. Здесь формы могут менять суффикс, гласную или всю основу. Поэтому правило одно: <b>учим пару по конкретному значению</b>."),
          grid([
              ["Тип связи", "Пара", "Что запомнить"],
              ["суффикс и долгота", "dávať -> dať", "длительное/повторное «давать» -> одно «дать»"],
              ["другая основа", "brať -> vziať", "«брать» -> «взять»; форму нельзя вывести"],
              ["супплетивная связь", "hovoriť -> povedať", "«говорить» -> «сказать» только в совпадающем значении"],
              ["суффикс + изменение основы", "vracať sa -> vrátiť sa", "«возвращаться» -> «вернуться»"],
          ], [43, 48, 78]), Spacer(1, 5),
          callout("Надёжная словарная строка", "Пишите так: <b>несовершенный / совершенный + управление + общий перевод + два примера</b>. Например: <i>dávať / dať komu čo - давать / дать кому что</i>.", GREEN),
          P("Почему недостаточно перевода", "h2"),
          P("<b>Dával mi rady.</b> - Он давал мне советы. / <b>Dal mi jednu radu.</b> - Он дал мне один совет.", "ex"),
          P("<b>Brala knihy z police.</b> - Она брала книги с полки. / <b>Vzala jednu knihu.</b> - Она взяла одну книгу.", "ex"),
          P("<b>Hovoril o probléme.</b> - Он говорил о проблеме. / <b>Povedal mi riešenie.</b> - Он сказал мне решение.", "ex"),
          P("<b>Vracali sme sa domov.</b> - Мы возвращались домой. / <b>Vrátili sme sa domov.</b> - Мы вернулись домой.", "ex"),
          callout("Не забегаем в 4.4", "На этих страницах мы распознаём и записываем формы. Подробный выбор вида в настоящем и прошедшем времени будет в следующей теме.", BLUE),
          PageBreak()]

# 3. dat/brat
story += [P("2. dávať/dať и brať/vziať", "h1"),
          P("Обе пары очень частотны и имеют много значений. На A2 сначала закрепите бытовое ядро и управление."),
          grid([
              ["Словарная запись", "Несовершенный процесс", "Совершенный результат"],
              ["dávať / dať komu čo", "Dávala deťom ovocie.<br/>Она давала детям фрукты.", "Dala Petrovi kľúč.<br/>Она дала Петеру ключ."],
              ["dávať si / dať si čo", "Dával som si kávu bez cukru.<br/>Я обычно брал кофе без сахара.", "Dal som si čaj.<br/>Я заказал себе чай."],
              ["brať / vziať koho, čo", "Bral lieky každý deň.<br/>Он принимал лекарства каждый день.", "Vzal si jednu tabletu.<br/>Он принял одну таблетку."],
              ["brať si / vziať si čo", "Brala si knihy z police.<br/>Она брала книги с полки.", "Vzala si dáždnik.<br/>Она взяла с собой зонт."],
          ], [49, 60, 60]),
          P("Форма меняется, управление остаётся", "h2"),
          P("<b>Komu?</b> Dávam <b>sestre</b> darček. / Dám <b>sestre</b> darček. - Я даю / дам сестре подарок.", "ex"),
          P("<b>Čo?</b> Beriem <b>doklady</b>. / Vezmem <b>doklady</b>. - Я беру / возьму документы.", "ex"),
          callout("Ловушка русского сходства", "Русское «брать» помогает узнать <i>brať</i>, но не предсказывает <i>vziať</i>. Не создавайте формы вроде *zbrať. Современный разговорный вариант <i>zobrať</i> встречается часто, но базовую словарную пару этого модуля записываем как <b>brať/vziať</b>.", CREAM),
          P("Мини-контрасты", "h2"),
          P("<b>Čašník nám dával jedálny lístok.</b> - Официант подавал нам меню. / <b>Čašník nám dal účet.</b> - Официант дал нам счёт.", "ex"),
          P("<b>Bral som antibiotiká päť dní.</b> - Я принимал антибиотики пять дней. / <b>Vzal som si poslednú tabletu.</b> - Я принял последнюю таблетку.", "ex"),
          PageBreak()]

# 4. hovorit/povedat
story += [P("3. hovoriť/povedať: пара только по значению", "h1"),
          P("Эти формы образуют видовую связь, когда речь идёт о сообщении: процесс говорения и одно законченное высказывание. Но <b>hovoriť</b> имеет более широкие модели, где простая замена на <b>povedať</b> невозможна."),
          grid([
              ["Модель", "hovoriť", "povedať"],
              ["содержание", "Hovoril o práci.<br/>Он говорил о работе.", "Povedal mi pravdu.<br/>Он сказал мне правду."],
              ["прямая реплика", "Učiteľ hovoril pomaly.<br/>Учитель говорил медленно.", "Učiteľ povedal jednu vetu.<br/>Учитель сказал одну фразу."],
              ["язык", "Hovorím po slovensky.<br/>Я говорю по-словацки.", "Нет простой замены: это навык, а не одно высказывание."],
              ["разговор", "Hovorila s lekárom.<br/>Она разговаривала с врачом.", "Povedala lekárovi, čo ju bolí.<br/>Она сказала врачу, что у неё болит."],
          ], [40, 61, 68]),
          P("Разное управление", "h2"),
          P("<b>hovoriť s kým o čom:</b> Hovorili sme <b>s kolegom o projekte</b>. - Мы говорили с коллегой о проекте.", "ex"),
          P("<b>hovoriť po slovensky:</b> Na kurze hovoríme <b>po slovensky</b>. - На курсе мы говорим по-словацки.", "ex"),
          P("<b>povedať komu čo:</b> Povedala <b>mi adresu</b>. - Она сказала мне адрес.", "ex"),
          P("<b>povedať, že...:</b> Povedal, <b>že príde neskôr</b>. - Он сказал, что придёт позже.", "ex"),
          callout("Проверка значения", "Спросите: речь о длительном говорении, языке или разговоре? Тогда обычно нужно <b>hovoriť</b>. Речь об одном сообщении или законченной реплике? Тогда подходит <b>povedať</b>.", BLUE),
          P("Сравните вопрос", "h2"),
          P("<b>O čom ste hovorili?</b> - О чём вы говорили? / <b>Čo ste povedali?</b> - Что вы сказали?", "ex"),
          PageBreak()]

# 5. return and cards
story += [P("4. vracať sa/vrátiť sa и карточка пары", "h1"),
          P("У возвратной пары сохраняется частица <b>sa</b>. Меняется основа и суффикс, а значение движения назад остаётся общим."),
          grid([
              ["Процесс / повтор", "Граница / результат"],
              ["Každý večer sa vraciam domov o šiestej.<br/>Каждый вечер я возвращаюсь домой в шесть.", "Dnes som sa vrátil domov o šiestej.<br/>Сегодня я вернулся домой в шесть."],
              ["Keď sme sa vracali z výletu, pršalo.<br/>Когда мы возвращались с экскурсии, шёл дождь.", "Vrátili sme sa z výletu večer.<br/>Мы вернулись с экскурсии вечером."],
              ["Eva sa často vracia k tejto téme.<br/>Эва часто возвращается к этой теме.", "Eva sa vrátila k hlavnej otázke.<br/>Эва вернулась к главному вопросу."],
          ], [84.5, 84.5]),
          callout("Частица входит в словарную форму", "Записывайте <b>vracať sa / vrátiť sa</b>, а не отдельные *vracať/vrátiť*. В предложении <i>sa</i> занимает обычное место краткой формы, но не исчезает.", CREAM),
          P("Четыре готовые карточки", "h2"),
          grid([
              ["Пара", "Управление и ядро"],
              ["dávať / dať", "komu čo - давать / дать кому что"],
              ["brať / vziať", "koho, čo - брать / взять кого, что"],
              ["hovoriť / povedať", "s kým o čom / komu čo - говорить / сказать в общем значении сообщения"],
              ["vracať sa / vrátiť sa", "kam, odkiaľ - возвращаться / вернуться куда, откуда"],
          ], [51, 118]),
          P("Мини-диалог", "h2"),
          callout("Po stretnutí", "<b>Anna:</b> Čo ti dal vedúci?<br/><b>Peter:</b> Dal mi nové dokumenty. Vzal som si ich domov.<br/><b>Anna:</b> Hovoril aj o termíne?<br/><b>Peter:</b> Áno, povedal, že sa máme vrátiť v pondelok.<br/><b>Anna:</b> Dobre. Keď sa budem vracať z práce, zavolám ti.<br/><br/><b>Перевод:</b> Анна: Что тебе дал руководитель? Петер: Он дал мне новые документы. Я взял их домой. Анна: Он говорил и о сроке? Петер: Да, сказал, что мы должны вернуться в понедельник. Анна: Хорошо. Когда буду возвращаться с работы, позвоню тебе.", BLUE),
          PageBreak()]

# 6. Exercises
story += [P("5. Ошибки и практика", "h1"),
          callout("Частые ошибки", "1) искать общую приставку там, где меняется основа; 2) писать только один член пары; 3) считать hovoriť/povedať взаимозаменяемыми во всех значениях; 4) терять sa; 5) не записывать управление.", CREAM),
          P("<b>1. Соедините пары.</b><br/>a) dávať  b) brať  c) hovoriť  d) vracať sa<br/>1) povedať  2) vrátiť sa  3) dať  4) vziať", "task"),
          P("<b>2. Выберите форму.</b><br/>a) Každý deň mi <i>(dával / dal)</i> nové úlohy.<br/>b) Včera mi <i>(dával / dal)</i> jednu dôležitú úlohu.<br/>c) Keď som odchádzal, <i>(bral / vzal)</i> som si dáždnik.<br/>d) Celý týždeň som <i>(bral / vzal)</i> lieky.", "task"),
          P("<b>3. hovoriť или povedať?</b><br/>a) Jana ___ po slovensky veľmi dobre.<br/>b) Jana mi ___ svoje telefónne číslo.<br/>c) Dlho sme ___ o novej práci.<br/>d) Lekár ___, že výsledky sú dobré.", "task"),
          P("<b>4. Исправьте ошибку или сделайте результат явным.</b><br/>a) Každý večer sa vrátil domov o šiestej.<br/>b) Včera som sa vracal domov a potom som už bol doma.<br/>c) Povedal som po slovensky s kolegom dve hodiny.<br/>d) Dával som Petrovi kľúč a potom ho Peter mal.", "task"),
          P("<b>5. Переведите.</b><br/>a) Она давала мне советы и наконец дала один хороший совет.<br/>b) Я брал документы со стола и взял последний документ.<br/>c) Мы говорили о встрече, а Мария сказала точное время.<br/>d) Когда они возвращались домой, они вернулись к этому вопросу.", "task"),
          P("<b>6. Собственная словарная карточка.</b> Выберите одну пару. Запишите обе формы, управление, общий перевод и мини-текст из 5-6 предложений: два процесса, два результата и одно отрицание.", "task"),
          PageBreak()]

# 7. Answers
story += [P("6. Ответы и итог", "h1"),
          P("<b>1.</b> a-3; b-4; c-1; d-2.", "answer"),
          P("<b>2.</b> a) <b>dával</b> - повтор; b) <b>dal</b> - одна полученная задача; c) <b>vzal</b> - результат перед уходом; d) <b>bral</b> - процесс в течение недели.", "answer"),
          P("<b>3.</b> a) <b>hovorí</b>; b) <b>povedala</b>; c) <b>hovorili</b>; d) <b>povedal</b>.", "answer"),
          P("<b>4.</b> Возможные исправления:<br/>a) Každý večer <b>sa vracal</b> domov o šiestej.<br/>b) Včera <b>som sa vrátil</b> domov.<br/>c) <b>Hovoril som po slovensky s kolegom</b> dve hodiny.<br/>d) <b>Dal som Petrovi kľúč</b> a potom ho Peter mal.", "answer"),
          P("<b>5.</b> a) Dávala mi rady a nakoniec mi dala jednu dobrú radu. b) Bral som dokumenty zo stola a vzal som posledný dokument. c) Hovorili sme o stretnutí a Mária povedala presný čas. d) Keď sa vracali domov, vrátili sa k tejto otázke.", "answer"),
          P("Образец к заданию 6", "h2"),
          callout("hovoriť / povedať", "Včera sme dlho hovorili o novom projekte. Vedúci hovoril pokojne a vysvetľoval plán. Potom povedal presný termín. Kolega mu nepovedal, že bude chýbať. Po stretnutí som povedal kolegovi najdôležitejšie informácie.<br/><br/>Вчера мы долго говорили о новом проекте. Руководитель говорил спокойно и объяснял план. Потом он назвал точный срок. Коллега не сказал ему, что будет отсутствовать. После встречи я сообщил коллеге самую важную информацию.", BLUE),
          P("Четыре опоры", "h2"),
          grid([
              ["1", "Видовая пара может менять суффикс, гласную или всю основу."],
              ["2", "Пара существует по конкретному общему значению, а не только по похожему переводу."],
              ["3", "Управление и частица sa входят в словарную запись."],
              ["4", "Надёжная карточка содержит обе формы и два контрастных примера."],
          ], [14, 155], header=False),
          callout("Проверка освоения", "Я могу:  □ назвать четыре пары;  □ выбрать hovoriť или povedať по значению;  □ сохранить sa в паре возвращения;  □ записать пару вместе с управлением.", GREEN)]

OUT.parent.mkdir(parents=True, exist_ok=True)
doc.build(story, onFirstPage=first_page, onLaterPages=later_page)
print(OUT)
