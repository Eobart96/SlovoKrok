from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    KeepTogether,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output" / "pdf" / "A2" / "Module_04" / "Slovak_A2_Tema_4_1_Vid_v_svyaznom_rasskaze.pdf"
TITLE = "Slovak A2 - Тема 4.1 - Вид в связном рассказе: фон и цепочка событий"

BURGUNDY = colors.HexColor("#741B47")
WINE = colors.HexColor("#8E244D")
PINK = colors.HexColor("#F7D6E4")
PALE = colors.HexColor("#FFF4F8")
CREAM = colors.HexColor("#FFF9F3")
INK = colors.HexColor("#2F2630")
MUTED = colors.HexColor("#6C5A65")
GREEN = colors.HexColor("#DFF1E6")
BLUE = colors.HexColor("#E8F1FA")
WHITE = colors.white


def register_fonts():
    candidates = [
        Path("C:/Windows/Fonts/arial.ttf"),
        Path("C:/Windows/Fonts/calibri.ttf"),
        Path("C:/Windows/Fonts/DejaVuSans.ttf"),
    ]
    bolds = [
        Path("C:/Windows/Fonts/arialbd.ttf"),
        Path("C:/Windows/Fonts/calibrib.ttf"),
        Path("C:/Windows/Fonts/DejaVuSans-Bold.ttf"),
    ]
    regular = next(p for p in candidates if p.exists())
    bold = next(p for p in bolds if p.exists())
    pdfmetrics.registerFont(TTFont("SK", str(regular)))
    pdfmetrics.registerFont(TTFont("SK-Bold", str(bold)))


register_fonts()


def esc(text):
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


styles = getSampleStyleSheet()
S = {
    "cover_kicker": ParagraphStyle("cover_kicker", fontName="SK-Bold", fontSize=14, leading=17, textColor=PINK, alignment=TA_CENTER, spaceAfter=7),
    "cover_title": ParagraphStyle("cover_title", fontName="SK-Bold", fontSize=27, leading=31, textColor=WHITE, alignment=TA_CENTER, spaceAfter=10),
    "cover_sub": ParagraphStyle("cover_sub", fontName="SK", fontSize=12.5, leading=17, textColor=WHITE, alignment=TA_CENTER),
    "h1": ParagraphStyle("h1", fontName="SK-Bold", fontSize=20, leading=24, textColor=BURGUNDY, spaceAfter=8),
    "h2": ParagraphStyle("h2", fontName="SK-Bold", fontSize=13.2, leading=16, textColor=WINE, spaceBefore=6, spaceAfter=5),
    "body": ParagraphStyle("body", fontName="SK", fontSize=9.55, leading=13.2, textColor=INK, spaceAfter=4),
    "small": ParagraphStyle("small", fontName="SK", fontSize=8.5, leading=11.5, textColor=MUTED, spaceAfter=3),
    "example": ParagraphStyle("example", fontName="SK", fontSize=9.25, leading=12.6, textColor=INK, leftIndent=5, rightIndent=4, spaceAfter=3),
    "box": ParagraphStyle("box", fontName="SK", fontSize=9.4, leading=13, textColor=INK),
    "box_b": ParagraphStyle("box_b", fontName="SK-Bold", fontSize=9.5, leading=13, textColor=BURGUNDY),
    "task": ParagraphStyle("task", fontName="SK", fontSize=8.85, leading=12.1, textColor=INK, spaceAfter=4),
    "answer": ParagraphStyle("answer", fontName="SK", fontSize=8.45, leading=11.5, textColor=INK, spaceAfter=4),
    "footer": ParagraphStyle("footer", fontName="SK", fontSize=7.5, leading=9, textColor=MUTED, alignment=TA_CENTER),
}


def P(text, style="body"):
    return Paragraph(text, S[style])


def box(title, body, color=PALE):
    t = Table([[P(title, "box_b")], [P(body, "box")]], colWidths=[169 * mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), color),
        ("BOX", (0, 0), (-1, -1), 0.8, PINK),
        ("LINEBELOW", (0, 0), (-1, 0), 0.5, PINK),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    return t


def comparison(rows, widths=(40, 57, 72), header=True):
    data = [[P(cell, "box_b" if i == 0 and header else "small") for cell in row] for i, row in enumerate(rows)]
    t = Table(data, colWidths=[w * mm for w in widths], repeatRows=1 if header else 0)
    style = [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.45, colors.HexColor("#D8B8C6")),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]
    if header:
        style += [("BACKGROUND", (0, 0), (-1, 0), PINK), ("TEXTCOLOR", (0, 0), (-1, 0), BURGUNDY)]
    for r in range(1 if header else 0, len(data)):
        if r % 2 == 0:
            style.append(("BACKGROUND", (0, r), (-1, r), CREAM))
    t.setStyle(TableStyle(style))
    return t


def header_footer(canvas, doc):
    canvas.saveState()
    if doc.page > 1:
        canvas.setStrokeColor(PINK)
        canvas.setLineWidth(0.7)
        canvas.line(20 * mm, 281 * mm, 190 * mm, 281 * mm)
        canvas.setFont("SK-Bold", 8)
        canvas.setFillColor(BURGUNDY)
        canvas.drawString(20 * mm, 285 * mm, "SLOVOKROK  |  A2  |  ТЕМА 4.1")
    canvas.setFont("SK", 7.5)
    canvas.setFillColor(MUTED)
    canvas.drawCentredString(105 * mm, 10 * mm, f"стр. {doc.page} / 7")
    canvas.restoreState()


def cover(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(BURGUNDY)
    canvas.rect(0, 0, A4[0], A4[1], fill=1, stroke=0)
    canvas.setFillColor(WINE)
    canvas.circle(18 * mm, 265 * mm, 36 * mm, fill=1, stroke=0)
    canvas.setFillColor(colors.HexColor("#A93668"))
    canvas.circle(193 * mm, 32 * mm, 48 * mm, fill=1, stroke=0)
    canvas.setFillColor(PINK)
    canvas.roundRect(28 * mm, 36 * mm, 154 * mm, 36 * mm, 5 * mm, fill=1, stroke=0)
    canvas.setFont("SK-Bold", 11)
    canvas.setFillColor(BURGUNDY)
    canvas.drawCentredString(105 * mm, 57 * mm, "ФОН  ->  СОБЫТИЕ  ->  РЕЗУЛЬТАТ")
    canvas.setFont("SK", 9)
    canvas.drawCentredString(105 * mm, 47 * mm, "pozadie  ->  udalosť  ->  výsledok")
    canvas.setFont("SK", 7.5)
    canvas.setFillColor(PINK)
    canvas.drawCentredString(105 * mm, 14 * mm, "стр. 1 / 7")
    canvas.restoreState()


doc = BaseDocTemplate(
    str(OUT), pagesize=A4, rightMargin=20 * mm, leftMargin=20 * mm,
    topMargin=26 * mm, bottomMargin=17 * mm,
    title=TITLE, author="SlovoKrok", subject="Slovak A2 self-study module 4.1",
)
frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="main")
def decorate_page(canvas, doc):
    if doc.page == 1:
        cover(canvas, doc)
    else:
        header_footer(canvas, doc)


doc.addPageTemplates([PageTemplate(id="all", frames=frame, onPage=decorate_page)])

story = []

# 1. Cover
story += [Spacer(1, 32 * mm), P("SLOVOKROK • СЛОВАЦКИЙ A2", "cover_kicker"),
          P("ТЕМА 4.1", "cover_kicker"),
          P("Вид в связном рассказе:<br/>фон и цепочка событий", "cover_title"),
          P("Ako striedať pozadie, priebeh a ukončené udalosti", "cover_sub"),
          Spacer(1, 22 * mm),
          Table([[P("После модуля вы сможете", "box_b")],
                 [P("• отделять фон от событий, которые двигают рассказ;<br/>• показывать одновременность и прерывание;<br/>• строить ясную цепочку результатов с <b>keď, kým, potom, nakoniec</b>;<br/>• написать короткий связный рассказ из 6-8 предложений.", "box")]],
                colWidths=[145 * mm], style=TableStyle([
                    ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#FFF4F8")),
                    ("BOX", (0, 0), (-1, -1), 0, WHITE),
                    ("LEFTPADDING", (0, 0), (-1, -1), 10), ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                    ("TOPPADDING", (0, 0), (-1, -1), 7), ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
                ])), PageBreak()]

# 2. Roles
story += [P("1. Три роли глагола в рассказе", "h1"),
          P("В теме 1.2 вы уже познакомились с видами. Здесь мы не учим пары заново, а выбираем форму по роли в тексте. Спросите: <b>это фон, процесс в кадре или завершённое событие?</b>"),
          comparison([
              ["Роль", "Что видит слушатель", "Типичный выбор и вопрос"],
              ["ФОН", "Обстановка, состояние, повторяющаяся ситуация.", "Обычно несовершенный вид. Что происходило?"],
              ["ПРОЦЕСС", "Действие уже шло в выбранный момент.", "Обычно несовершенный вид. Что было в процессе?"],
              ["СОБЫТИЕ", "Целое действие с границей или результатом.", "Обычно совершенный вид. Что случилось дальше?"],
          ]), Spacer(1, 4),
          box("Ключевой принцип", "Несовершенный вид открывает сцену и удерживает камеру внутри действия. Совершенный вид ставит границу и переводит рассказ к следующему событию. Это не правило «долго = несовершенный, быстро = совершенный»: важна роль действия в данном рассказе.", BLUE),
          P("Сравните", "h2"),
          P("<b>Bolo chladno a pršalo.</b> - Было холодно и шёл дождь. (фон)", "example"),
          P("<b>Ľudia čakali pred kinom.</b> - Люди ждали перед кинотеатром. (процесс на фоне)", "example"),
          P("<b>Peter prišiel a otvoril dvere.</b> - Петер пришёл и открыл дверь. (два завершённых события)", "example"),
          P("<b>Kým som písala správu, kolega pripravoval tabuľku.</b> - Пока я писала сообщение, коллега готовил таблицу. (два параллельных процесса)", "example"),
          P("<b>Keď som napísala správu, poslala som ju vedúcej.</b> - Когда я написала сообщение, я отправила его руководительнице. (результат и следующий шаг)", "example"),
          box("Подсказка русскоязычному ученику", "Словацкий и русский используют вид похоже, но не переносите русскую приставку механически. Сначала определите роль действия, затем выбирайте уже знакомую словацкую форму.", PALE),
          PageBreak()]

# 3. Simultaneity and interruption
story += [P("2. Одновременность и прерывание", "h1"),
          P("Связки <b>kým</b> и <b>keď</b> показывают временную связь. Сам союз не выбирает вид автоматически: форму определяет то, как рассказчик видит действие."),
          comparison([
              ["Модель", "Словацкий пример", "Смысл"],
              ["процесс + процесс", "Kým som varil večeru, deti sa hrali.", "Пока я готовил ужин, дети играли."],
              ["процесс + событие", "Keď som varil večeru, zazvonil telefón.", "Когда я готовил ужин, зазвонил телефон."],
              ["событие + событие", "Keď som uvaril večeru, zavolal som deti.", "Когда я приготовил ужин, я позвал детей."],
          ], widths=(39, 69, 61)),
          P("Как читать три модели", "h2"),
          P("1. <b>Kým som upratoval kuchyňu, deti sa hrali.</b> - Пока я убирал кухню, дети играли. Камера остаётся внутри двух процессов.", "example"),
          P("2. <b>Keď som upratoval kuchyňu, spadol pohár.</b> - Когда я убирал кухню, упал стакан. Длительный процесс создаёт рамку, событие её прерывает.", "example"),
          P("3. <b>Keď som upratal kuchyňu, sadol som si.</b> - Когда я убрал кухню, я сел. Первое действие завершено, после него начинается следующее.", "example"),
          box("Не путайте", "<b>kým</b> удобно для длительности и параллельности, но не означает «всегда несовершенный вид». <b>keď</b> может вводить и процесс, и завершённое событие. Смотрите на границы действий.", PALE),
          P("Мини-анализ", "h2"),
          P("<b>Vonku snežilo, keď som vyšiel z domu.</b> - На улице шёл снег, когда я вышел из дома. <i>snežilo</i> рисует фон; <i>vyšiel</i> отмечает событие.", "example"),
          P("<b>Kým Eva čítala, Martin napísal tri e-maily.</b> - Пока Эва читала, Мартин написал три письма. Один процесс служит временной рамкой, а результат второго действия подсчитан.", "example"),
          P("<b>Keď hostia odišli, umyli sme riad.</b> - Когда гости ушли, мы помыли посуду. Два ограниченных события образуют последовательность.", "example"),
          PageBreak()]

# 4. Chain of events
story += [P("3. Как строится цепочка событий", "h1"),
          P("В связном рассказе фон обычно занимает несколько слов или предложений, а затем завершённые события двигают время вперёд. Маркеры делают порядок прозрачным."),
          comparison([
              ["Маркер", "Функция", "Пример"],
              ["najprv", "первый шаг", "Najprv som otvoril okno."],
              ["potom", "следующий шаг", "Potom som uvaril čaj."],
              ["keď", "временная граница", "Keď som dopil čaj, odišiel som."],
              ["zrazu", "неожиданное событие", "Zrazu niekto zaklopal."],
              ["nakoniec", "финал цепочки", "Nakoniec som zavolal sestre."],
          ], widths=(30, 50, 89)),
          P("Одна сцена - две версии", "h2"),
          box("Камера внутри процесса", "<b>Ráno som čítal správu a pil kávu.</b><br/>Утром я читал новости и пил кофе. Рассказчик показывает занятие без важной конечной точки.", BLUE),
          Spacer(1, 5),
          box("Цепочка результатов", "<b>Ráno som prečítal správu, dopil kávu a odišiel.</b><br/>Утром я прочитал новости, допил кофе и ушёл. Каждый результат открывает следующий шаг.", GREEN),
          P("Соберите скелет рассказа", "h2"),
          P("<b>1. Фон:</b> Bolo skoro ráno a ulice boli prázdne. - Было раннее утро, и улицы были пусты.", "example"),
          P("<b>2. Процесс:</b> Čakal som na autobus a počúval hudbu. - Я ждал автобус и слушал музыку.", "example"),
          P("<b>3. Перелом:</b> Zrazu mi zazvonil telefón. - Вдруг у меня зазвонил телефон.", "example"),
          P("<b>4. Цепочка:</b> Zdvihol som telefón, vypočul som si správu a nastúpil som do autobusu. - Я поднял трубку, выслушал сообщение и сел в автобус.", "example"),
          P("<b>5. Финал:</b> Nakoniec som prišiel do práce načas. - В конце концов я пришёл на работу вовремя.", "example"),
          box("Ритм хорошего рассказа", "Не превращайте весь текст в список результатов. Чередуйте: <b>фон -> событие -> новый фон/реакция -> следующее событие</b>. Так слушатель понимает и обстановку, и движение сюжета.", PALE),
          PageBreak()]

# 5. Model story
story += [P("4. Образец связного рассказа", "h1"),
          P("Прочитайте текст сначала целиком, затем проследите, как вид меняет роль каждого предложения."),
          box("Sobotné raňajky", "<b>V sobotu ráno bolo doma ticho a vonku pršalo.</b> Pripravoval som raňajky, kým dcéra čítala správu v telefóne. Keď som otvoril chladničku, zistil som, že nemáme mlieko. Obliekol som sa a zišiel som dolu. Cestou stále pršalo a ľudia sa ponáhľali pod dáždnikmi. V obchode som kúpil mlieko a chlieb. Potom som sa vrátil domov a uvaril som kávu. Nakoniec sme si sadli k stolu a spolu sme raňajkovali.", BLUE),
          P("Перевод", "h2"),
          P("В субботу утром дома было тихо, а на улице шёл дождь. Я готовил завтрак, пока дочь читала сообщение в телефоне. Когда я открыл холодильник, я обнаружил, что у нас нет молока. Я оделся и спустился вниз. По дороге всё ещё шёл дождь, а люди спешили под зонтами. В магазине я купил молоко и хлеб. Потом я вернулся домой и сварил кофе. Наконец мы сели за стол и позавтракали вместе."),
          P("Разметка ролей", "h2"),
          comparison([
              ["Фрагмент", "Роль", "Почему"],
              ["bolo ticho, pršalo", "фон", "обстановка не двигает время вперёд"],
              ["pripravoval som, čítala", "параллельные процессы", "оба действия уже шли"],
              ["otvoril som, zistil som", "перелом", "два результата меняют план героя"],
              ["obliekol som sa, zišiel som", "цепочка", "последовательные завершённые шаги"],
              ["pršalo, ponáhľali sa", "новый фон", "камера снова показывает сцену"],
              ["kúpil, vrátil sa, uvaril", "цепочка результатов", "сюжет приходит к решению"],
              ["sadli sme si, raňajkovali sme", "финал", "граница и затем совместное занятие"],
          ], widths=(57, 48, 64)),
          box("Что делает текст связным", "Повторный фон не ошибка: он связывает отдельные события в одну сцену. Маркеры <b>keď, kým, potom, nakoniec</b> показывают отношения, а вид уточняет, видим ли мы процесс или его границу.", PALE),
          PageBreak()]

# 6. Exercises
story += [P("5. Практика", "h1"),
          P("Выполните задания письменно. Ответы и образец - на следующей странице."),
          P("<b>1. Определите роль:</b> фон (Ф), процесс (П) или событие (С).<br/>a) Vonku fúkal vietor.  b) Čakala som na lekára.  c) Lekár otvoril dvere.  d) Potom ma zavolal dnu.", "task"),
          P("<b>2. Выберите форму.</b><br/>a) Kým som <i>(písal / napísal)</i> správu, kolega telefonoval.<br/>b) Keď som <i>(písal / napísal)</i> správu, poslal som ju.<br/>c) Zrazu niekto <i>(otváral / otvoril)</i> okno.<br/>d) Celý večer sme <i>(pozerali / pozreli)</i> film.", "task"),
          P("<b>3. Вставьте keď, kým, potom или nakoniec.</b><br/>a) ___ som varila, sestra prestierala stôl.<br/>b) ___ som dovarila polievku, zavolala som rodinu.<br/>c) Najprv sme jedli, ___ sme umyli riad.<br/>d) ___ sme si sadli a oddýchli si.", "task"),
          P("<b>4. Исправьте выбор вида.</b><br/>a) Keď som písal list do konca, vložil som ho do obálky.<br/>b) Vonku zasnežilo a ľudia čakali na autobus.<br/>c) Najprv som upratoval izbu, potom som dokončil a odišiel.<br/>d) Kým som prečítal knihu, brat pozeral televíziu.", "task"),
          P("<b>5. Переведите на словацкий.</b><br/>a) Пока я готовила кофе, дети завтракали.<br/>b) Когда я приготовила кофе, я села за стол.<br/>c) Было темно, и шёл снег.<br/>d) Потом мы закрыли магазин и ушли домой.", "task"),
          P("<b>6. Собственный рассказ.</b> Напишите 6-8 предложений на тему «Неожиданное утро». Обязательно используйте: 1 фон, 2 параллельных процесса, 1 прерывающее событие, цепочку из 3 завершённых действий и маркеры <i>kým, keď, potom, nakoniec</i>.", "task"),
          box("Самопроверка перед ответами", "Подчеркните несовершенные формы одной линией, совершенные - двумя. Стрелками соедините результаты в хронологическом порядке. Если рассказ понятен без перевода, структура работает.", GREEN),
          PageBreak()]

# 7. Answers
story += [P("6. Ответы и итог", "h1"),
          P("<b>1.</b> a) Ф; b) П; c) С; d) С.", "answer"),
          P("<b>2.</b> a) <b>písal</b> - процесс параллелен звонку; b) <b>napísal</b> - сообщение закончено перед отправкой; c) <b>otvoril</b> - внезапное завершённое событие; d) <b>pozerali</b> - занятие в течение вечера.", "answer"),
          P("<b>3.</b> a) <b>Kým</b>; b) <b>Keď</b>; c) <b>potom</b>; d) <b>Nakoniec</b>.", "answer"),
          P("<b>4.</b> Возможные исправления:<br/>a) Keď som <b>napísal</b> list, vložil som ho do obálky.<br/>b) Vonku <b>snežilo</b> a ľudia čakali na autobus.<br/>c) Najprv som <b>upratal</b> izbu, potom som odišiel.<br/>d) Kým som <b>čítal</b> knihu, brat pozeral televíziu.", "answer"),
          P("<b>5.</b> a) Kým som varila kávu, deti raňajkovali. b) Keď som uvarila kávu, sadla som si k stolu. c) Bola tma a snežilo. d) Potom sme zatvorili obchod a odišli domov.", "answer"),
          P("Образец к заданию 6", "h2"),
          box("Nečakané ráno", "Bolo ešte skoro a v byte bolo ticho. Kým som si čistil zuby, manželka pripravovala raňajky. Zrazu zazvonil zvonček. Otvoril som dvere a našiel som pred nimi malý balík. Vzal som ho dnu, prečítal som adresu a zavolal som susedovi. Potom si sused prišiel po balík. Nakoniec sme sa zasmiali a vrátili sme sa k raňajkám.", BLUE),
          P("Четыре опоры", "h2"),
          comparison([
              ["1", "Фон и незавершённый процесс обычно удерживают камеру внутри действия."],
              ["2", "Завершённое событие ставит границу и двигает время рассказа вперёд."],
              ["3", "Kým подчёркивает временную рамку; keď связывает момент или ситуацию с другим действием."],
              ["4", "Potom и nakoniec делают порядок и финал цепочки явными."],
          ], widths=(15, 154), header=False),
          box("Проверка освоения", "Я могу:  □ назвать роль каждого глагола;  □ показать одновременность и прерывание;  □ выстроить цепочку результатов;  □ написать 6-8 связанных предложений без механического копирования русского вида.", GREEN)]

OUT.parent.mkdir(parents=True, exist_ok=True)
doc.build(story)
print(OUT)
