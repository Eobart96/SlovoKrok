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
OUT = ROOT / "output" / "pdf" / "A2" / "Module_04" / "Slovak_A2_Tema_4_2_Vidovye_pary_s_pristavkami.pdf"
TITLE = "Slovak A2 - Тема 4.2 - Видовые пары с приставками"

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
    regulars = [Path("C:/Windows/Fonts/arial.ttf"), Path("C:/Windows/Fonts/calibri.ttf")]
    bolds = [Path("C:/Windows/Fonts/arialbd.ttf"), Path("C:/Windows/Fonts/calibrib.ttf")]
    regular = next(p for p in regulars if p.exists())
    bold = next(p for p in bolds if p.exists())
    pdfmetrics.registerFont(TTFont("SK", str(regular)))
    pdfmetrics.registerFont(TTFont("SK-Bold", str(bold)))


register_fonts()

S = getSampleStyleSheet()
ST = {
    "cover_kicker": ParagraphStyle("cover_kicker", fontName="SK-Bold", fontSize=14, leading=18, textColor=colors.HexColor("#F8D8E9"), alignment=TA_CENTER, spaceAfter=8),
    "cover_title": ParagraphStyle("cover_title", fontName="SK-Bold", fontSize=29, leading=34, textColor=WHITE, alignment=TA_CENTER, spaceAfter=11),
    "cover_sub": ParagraphStyle("cover_sub", fontName="SK", fontSize=12.5, leading=17, textColor=WHITE, alignment=TA_CENTER),
    "h1": ParagraphStyle("h1", fontName="SK-Bold", fontSize=20, leading=24, textColor=PLUM, spaceAfter=8),
    "h2": ParagraphStyle("h2", fontName="SK-Bold", fontSize=13.5, leading=17, textColor=PLUM, spaceBefore=6, spaceAfter=5),
    "body": ParagraphStyle("body", fontName="SK", fontSize=9.55, leading=13.2, textColor=INK, spaceAfter=4),
    "small": ParagraphStyle("small", fontName="SK", fontSize=8.45, leading=11.5, textColor=MUTED, spaceAfter=2),
    "box": ParagraphStyle("box", fontName="SK", fontSize=9.2, leading=12.7, textColor=INK),
    "box_b": ParagraphStyle("box_b", fontName="SK-Bold", fontSize=9.4, leading=12.8, textColor=PLUM),
    "ex": ParagraphStyle("ex", fontName="SK", fontSize=9.1, leading=12.4, textColor=INK, leftIndent=6, spaceAfter=3),
    "task": ParagraphStyle("task", fontName="SK", fontSize=8.65, leading=11.8, textColor=INK, spaceAfter=4),
    "answer": ParagraphStyle("answer", fontName="SK", fontSize=8.25, leading=11.1, textColor=INK, spaceAfter=3),
}


def P(text, style="body"):
    return Paragraph(text, ST[style])


def callout(title, text, color=PALE, width=169):
    t = Table([[P(title, "box_b")], [P(text, "box")]], colWidths=[width * mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), color),
        ("BOX", (0, 0), (-1, -1), 0.7, ROSE),
        ("LINEBELOW", (0, 0), (-1, 0), 0.45, ROSE),
        ("LEFTPADDING", (0, 0), (-1, -1), 8), ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    return t


def grid(rows, widths, header=True, font="small"):
    data = []
    for i, row in enumerate(rows):
        data.append([P(cell, "box_b" if header and i == 0 else font) for cell in row])
    t = Table(data, colWidths=[w * mm for w in widths], repeatRows=1 if header else 0)
    rules = [
        ("GRID", (0, 0), (-1, -1), 0.45, ROSE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
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
    canvas.drawCentredString(105 * mm, 57 * mm, "ОСНОВА + ПРИСТАВКА: ВИД ИЛИ НОВОЕ ЗНАЧЕНИЕ?")
    canvas.setFont("SK", 9)
    canvas.drawCentredString(105 * mm, 47 * mm, "základ + predpona: vid alebo nový význam?")
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
    canvas.drawString(20 * mm, 285 * mm, "SLOVOKROK  |  A2  |  ТЕМА 4.2  |  ВИДОВЫЕ ПАРЫ")
    canvas.setFillColor(MUTED)
    canvas.setFont("SK", 7.5)
    canvas.drawCentredString(105 * mm, 10 * mm, f"стр. {doc.page} / 7")
    canvas.restoreState()


doc = SimpleDocTemplate(
    str(OUT), pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm,
    topMargin=26 * mm, bottomMargin=17 * mm,
    title=TITLE, author="SlovoKrok", subject="Slovak A2 self-study module 4.2",
)

story = []

# 1. Cover
story += [Spacer(1, 28 * mm), P("SLOVOKROK • СЛОВАЦКИЙ A2", "cover_kicker"),
          P("ТЕМА 4.2", "cover_kicker"),
          P("Видовые пары<br/>с приставками", "cover_title"),
          P("Vidové dvojice s predponami", "cover_sub"), Spacer(1, 22 * mm),
          Table([[P("После модуля вы сможете", "box_b")],
                 [P("• узнавать пять частотных видовых пар;<br/>• видеть, когда приставка только ставит границу действия;<br/>• отличать результат от нового словарного значения;<br/>• записывать пару так, чтобы не угадывать форму наугад.", "box")]],
                colWidths=[145 * mm], style=TableStyle([
                    ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#FFF7FB")),
                    ("LEFTPADDING", (0, 0), (-1, -1), 10), ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                    ("TOPPADDING", (0, 0), (-1, -1), 7), ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
                ])), PageBreak()]

# 2. Core distinction
story += [P("1. Что делает приставка", "h1"),
          P("Вы уже знаете разницу между процессом и результатом. Теперь смотрим на форму слова: приставка иногда создаёт совершенный партнёр, а иногда одновременно меняет словарный смысл."),
          grid([
              ["Ситуация", "Что меняется", "Пример"],
              ["Чистая граница", "Действие остаётся тем же, но показано как целое.", "písať -> napísať<br/>писать -> написать"],
              ["Граница + новый оттенок", "Приставка уточняет направление, объём или способ.", "písať -> prepísať<br/>писать -> переписать"],
              ["Новое словарное слово", "Связь с основой видна, но перевод надо учить отдельно.", "písať -> podpísať<br/>писать -> подписать"],
          ], [43, 68, 58]), Spacer(1, 5),
          callout("Главное правило A2", "Нельзя считать любую форму «приставка + знакомый глагол» его совершенным видом. Сначала проверьте значение. Если приставка добавила новый смысл, перед вами отдельная лексема со своей видовой парой.", CREAM),
          P("Одна основа - разные результаты", "h2"),
          P("<b>Písal som e-mail.</b> - Я писал электронное письмо. (процесс)", "ex"),
          P("<b>Napísal som e-mail.</b> - Я написал электронное письмо. (готовый текст)", "ex"),
          P("<b>Prepísal som e-mail.</b> - Я переписал электронное письмо. (изменил или набрал заново)", "ex"),
          P("<b>Podpísal som dokument.</b> - Я подписал документ. (другое действие)", "ex"),
          callout("Приставка не всегда «приклеивается»", "Пара может выглядеть иначе: <b>kupovať/kúpiť</b> и <b>hľadať/nájsť</b>. Эти формы надо узнавать как готовые пары. Систему суффиксов и изменений основы разберём отдельно в теме 4.3.", BLUE),
          PageBreak()]

# 3. Required pairs
story += [P("2. Пять частотных пар", "h1"),
          P("Учите обе формы вместе с одним типичным дополнением. Порядок в таблице: несовершенный вид -> совершенный вид."),
          grid([
              ["Пара", "Процесс / повтор", "Результат"],
              ["písať -> napísať", "Písala som správu.<br/>Я писала сообщение.", "Napísala som správu.<br/>Я написала сообщение."],
              ["robiť -> urobiť", "Robili sme úlohu.<br/>Мы делали задание.", "Urobili sme úlohu.<br/>Мы сделали задание."],
              ["kupovať -> kúpiť", "Kupoval chlieb každý deň.<br/>Он покупал хлеб каждый день.", "Kúpil chlieb.<br/>Он купил хлеб."],
              ["platiť -> zaplatiť", "Platila kartou.<br/>Она платила картой.", "Zaplatila účet.<br/>Она оплатила счёт."],
              ["hľadať -> nájsť", "Hľadám kľúče.<br/>Я ищу ключи.", "Našiel som kľúče.<br/>Я нашёл ключи."],
          ], [43, 63, 63]),
          P("Три разных типа формы", "h2"),
          P("<b>1. Приставка без смены основы:</b> písať/napísať, robiť/urobiť, platiť/zaplatiť. Форму всё равно проверяем по словарю."),
          P("<b>2. Вторичный несовершенный партнёр:</b> kúpiť/kupovať. Нельзя получить пару простым удалением приставки."),
          P("<b>3. Непредсказуемая пара:</b> hľadať/nájsť. Формы различаются сильно, но в ситуации «искать -> найти» работают как процесс и результат."),
          callout("Не меняйте порядок смысла", "<b>hľadať</b> означает пытаться найти, а <b>nájsť</b> - получить результат. Фраза <i>Hľadal som kľúče, ale nenašiel som ich</i> естественна: «Я искал ключи, но не нашёл их».", GREEN),
          P("Ещё три контраста", "h2"),
          P("<b>Čo robíš?</b> - Что ты делаешь? / <b>Čo si urobil?</b> - Что ты сделал?", "ex"),
          P("<b>Kupovali sme darček.</b> - Мы выбирали и покупали подарок. / <b>Kúpili sme darček.</b> - Мы купили подарок.", "ex"),
          P("<b>Platil som, keď zazvonil telefón.</b> - Я расплачивался, когда зазвонил телефон. / <b>Zaplatil som a odišiel.</b> - Я заплатил и ушёл.", "ex"),
          PageBreak()]

# 4. Prefix meanings
story += [P("3. Когда приставка добавляет значение", "h1"),
          P("Сравнивайте не только вид, но и перевод. У одной основы несколько приставочных глаголов, и каждый отвечает на свой вопрос."),
          grid([
              ["Форма", "Практический смысл", "Пример"],
              ["napísať", "написать до готового текста", "Napíš mi adresu. - Напиши мне адрес."],
              ["dopísať", "дописать, закончить писать", "Dopísal som poslednú vetu. - Я дописал последнее предложение."],
              ["prepísať", "переписать, написать заново", "Prepísala chybný údaj. - Она переписала ошибочные данные."],
              ["podpísať", "подписать", "Podpísali sme zmluvu. - Мы подписали договор."],
              ["zapísať", "записать, внести", "Zapísal som si termín. - Я записал дату."],
          ], [35, 62, 72]),
          P("Семья platiť", "h2"),
          grid([
              ["Глагол", "Не путайте"],
              ["zaplatiť", "оплатить, погасить сумму: zaplatiť účet"],
              ["doplatiť", "доплатить остаток: doplatiť desať eur"],
              ["priplatiť", "доплатить за улучшение: priplatiť si za izbu"],
              ["vyplatiť", "выплатить кому-то деньги: vyplatiť odmenu"],
              ["preplatiť", "переплатить: preplatiť za službu"],
          ], [40, 129]),
          callout("Предел продуктивного угадывания", "Значение приставки может быть прозрачным, но не гарантированным. <b>za-</b> в <i>zaplatiť</i> в основном ставит границу оплате, а <b>pre-</b> в <i>preplatiť</i> добавляет смысл «слишком много». Проверяйте форму и управление по словарю.", CREAM),
          P("Ловушка с покупками", "h2"),
          P("<b>Kúpil som si košeľu.</b> - Я купил себе рубашку. Один результат.", "ex"),
          P("<b>Nakupoval som celé popoludnie.</b> - Я делал покупки весь день. Здесь <i>nakupovať</i> - отдельный глагол «ходить за покупками», а не просто форма слова <i>kúpiť</i>.", "ex"),
          PageBreak()]

# 5. Method and mini-dialogue
story += [P("4. Как учить пару без угадывания", "h1"),
          P("Записывайте не один инфинитив, а маленькую карточку: <b>две формы + управление + один процесс + один результат</b>."),
          grid([
              ["Пара и управление", "Процесс", "Результат"],
              ["písať/napísať čo", "Píšem žiadosť.<br/>Я пишу заявление.", "Napísal som žiadosť.<br/>Я написал заявление."],
              ["robiť/urobiť čo", "Robíme večeru.<br/>Мы готовим ужин.", "Urobili sme večeru.<br/>Мы приготовили ужин."],
              ["kupovať/kúpiť čo", "Kupujem lístok.<br/>Я покупаю билет.", "Kúpil som lístok.<br/>Я купил билет."],
              ["platiť/zaplatiť čo, za čo", "Platím za obed.<br/>Я плачу за обед.", "Zaplatil som účet.<br/>Я оплатил счёт."],
              ["hľadať/nájsť koho/čo", "Hľadáme hotel.<br/>Мы ищем отель.", "Našli sme hotel.<br/>Мы нашли отель."],
          ], [51, 59, 59]),
          P("Мини-диалог: перед поездкой", "h2"),
          callout("Plán a výsledok", "<b>Eva:</b> Už si <b>kúpil</b> lístok?<br/><b>Martin:</b> Ešte ho <b>kupujem</b>. <b>Hľadám</b> lacnejšie spojenie.<br/><b>Eva:</b> Ja som ho už <b>našla</b> a <b>zaplatila</b> kartou.<br/><b>Martin:</b> Dobre. Najprv <b>napíšem</b> správu Petrovi a potom to <b>urobím</b>.<br/><b>Eva:</b> Nezabudni <b>zapísať</b> čas odchodu.<br/><br/><b>Перевод:</b> Эва: Ты уже купил билет? Мартин: Я ещё его покупаю. Ищу более дешёвое сообщение. Эва: Я уже его нашла и оплатила картой. Мартин: Хорошо. Сначала напишу сообщение Петеру, а потом это сделаю. Эва: Не забудь записать время отправления.", BLUE),
          P("Что видно в диалоге", "h2"),
          P("• <b>kupujem, hľadám</b> держат нас внутри процесса; <b>kúpil, našla, zaplatila</b> называют результат."),
          P("• <b>napíšem, urobím</b> имеют форму настоящего времени, но у совершенных глаголов обозначают будущий результат. Подробно это будет в теме 4.6."),
          P("• <b>zapísať</b> не является простой заменой <i>písať</i>: здесь это «зафиксировать, записать».", "body"),
          callout("Проверка карточки", "Если вы можете назвать перевод обеих форм, дополнение и два контрастных предложения, пара усвоена. Если знаете только приставку, форма ещё не надёжна.", GREEN),
          PageBreak()]

# 6. Exercises
story += [P("5. Ошибки и практика", "h1"),
          callout("Частые ошибки", "1) считать любую приставку только показателем результата; 2) строить несуществующую форму по русскому образцу; 3) учить <i>nájsť</i> без <i>hľadať</i>; 4) путать <i>zaplatiť</i> и <i>preplatiť</i>; 5) записывать глагол без дополнения.", CREAM),
          P("<b>1. Соедините пары.</b><br/>a) písať  b) robiť  c) kupovať  d) platiť  e) hľadať<br/>1) nájsť  2) zaplatiť  3) urobiť  4) napísať  5) kúpiť", "task"),
          P("<b>2. Выберите процесс или результат.</b><br/>a) Celé ráno som <i>(písal / napísal)</i> správu.<br/>b) Už som ju <i>(písal / napísal)</i> a poslal.<br/>c) Kým Eva <i>(platila / zaplatila)</i>, čakal som pri dverách.<br/>d) Eva <i>(platila / zaplatila)</i> účet a odišla.", "task"),
          P("<b>3. Вставьте нужный глагол.</b><br/>a) Včera som ___ nový kabát. (kupovať/kúpiť)<br/>b) Dlho som ___ kľúče, ale nenašiel som ich. (hľadať/nájsť)<br/>c) Prosím, ___ si moje číslo. (písať/zapísať)<br/>d) Musím ___ posledný odsek. (dopísať/podpísať)", "task"),
          P("<b>4. Исправьте смысловую ошибку.</b><br/>a) Účet bol desať eur, ale omylom som ho preplatil presne desať eur.<br/>b) Hľadal som peňaženku a po chvíli som ju hľadal.<br/>c) Podpísal som kamarátovi krátku správu.<br/>d) Kúpil som potraviny celé tri hodiny.", "task"),
          P("<b>5. Переведите.</b><br/>a) Я писал заявление, а вечером написал его.<br/>b) Мы искали гостиницу и наконец нашли её.<br/>c) Она оплатила счёт, но случайно переплатила пять евро.<br/>d) Запиши адрес и подпиши документ.", "task"),
          P("<b>6. Собственная карточка.</b> Выберите одну семью <i>písať</i> или <i>platiť</i>. Запишите 4 формы, точный русский смысл каждой и короткий рассказ из 5-6 предложений, где есть процесс, результат и одна приставка с новым значением.", "task"),
          PageBreak()]

# 7. Answers
story += [P("6. Ответы и итог", "h1"),
          P("<b>1.</b> a-4; b-3; c-5; d-2; e-1.", "answer"),
          P("<b>2.</b> a) <b>písal</b> - длительный процесс; b) <b>napísal</b> - готовый текст перед отправкой; c) <b>platila</b> - процесс служит временной рамкой; d) <b>zaplatila</b> - результат перед уходом.", "answer"),
          P("<b>3.</b> a) <b>kúpil</b>; b) <b>hľadal</b>; c) <b>zapíš</b>; d) <b>dopísať</b>.", "answer"),
          P("<b>4.</b> Возможные исправления:<br/>a) Účet bol desať eur a zaplatil som presne desať eur. / Omylom som preplatil päť eur.<br/>b) Hľadal som peňaženku a po chvíli som ju našiel.<br/>c) Napísal som kamarátovi krátku správu.<br/>d) Kupoval som potraviny celé tri hodiny. / Kúpil som potraviny.", "answer"),
          P("<b>5.</b> a) Písal som žiadosť a večer som ju napísal. b) Hľadali sme hotel a nakoniec sme ho našli. c) Zaplatila účet, ale omylom preplatila päť eur. d) Zapíš adresu a podpíš dokument.", "answer"),
          P("Образец к заданию 6", "h2"),
          callout("Rodina písať", "Ráno som písal dôležitý e-mail. Po obede som ho konečne napísal. Potom som si zapísal termín stretnutia. V texte som našiel chybu, preto som jednu vetu prepísal. Nakoniec som vytlačil dokument a podpísal som ho.<br/><br/>Утром я писал важное письмо. После обеда я наконец его написал. Потом я записал дату встречи. В тексте я нашёл ошибку, поэтому переписал одно предложение. Наконец я распечатал документ и подписал его.", BLUE),
          P("Четыре опоры", "h2"),
          grid([
              ["1", "Пара показывает процесс и его границу, но значение действия должно совпадать."],
              ["2", "Приставка может одновременно добавить направление, объём или новый словарный смысл."],
              ["3", "Формы kupovať/kúpiť и hľadať/nájsť нельзя надёжно получить простым правилом."],
              ["4", "Учите две формы вместе с управлением и контрастными примерами."],
          ], [14, 155], header=False),
          callout("Проверка освоения", "Я могу:  □ назвать пять пар;  □ объяснить разницу napísať/prepísať/podpísať;  □ различить zaplatiť и preplatiť;  □ отказаться от угадывания и проверить пару в словаре.", GREEN)]

OUT.parent.mkdir(parents=True, exist_ok=True)
doc.build(story, onFirstPage=first_page, onLaterPages=later_page)
print(OUT)
