from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output" / "pdf" / "A2" / "Module_04" / "Slovak_A2_Tema_4_10_Kondicional_s_chastitsey_by.pdf"
TITLE = "Slovak A2 - Тема 4.10 - Кондиционал с частицей by"

PLUM = colors.HexColor("#7B245F")
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
    "cover_title": ParagraphStyle("cover_title", fontName="SK-Bold", fontSize=23, leading=28, textColor=WHITE, alignment=TA_CENTER, spaceAfter=11),
    "cover_sub": ParagraphStyle("cover_sub", fontName="SK", fontSize=12.2, leading=17, textColor=WHITE, alignment=TA_CENTER),
    "h1": ParagraphStyle("h1", fontName="SK-Bold", fontSize=20, leading=24, textColor=PLUM, spaceAfter=8),
    "h2": ParagraphStyle("h2", fontName="SK-Bold", fontSize=13.5, leading=17, textColor=PLUM, spaceBefore=6, spaceAfter=5),
    "body": ParagraphStyle("body", fontName="SK", fontSize=9.45, leading=13.0, textColor=INK, spaceAfter=4),
    "small": ParagraphStyle("small", fontName="SK", fontSize=8.25, leading=11.25, textColor=MUTED, spaceAfter=2),
    "box": ParagraphStyle("box", fontName="SK", fontSize=9.0, leading=12.4, textColor=INK),
    "box_b": ParagraphStyle("box_b", fontName="SK-Bold", fontSize=9.35, leading=12.7, textColor=PLUM),
    "task": ParagraphStyle("task", fontName="SK", fontSize=8.4, leading=11.25, textColor=INK, spaceAfter=4),
    "answer": ParagraphStyle("answer", fontName="SK", fontSize=7.95, leading=10.45, textColor=INK, spaceAfter=3),
}


def P(text, style="body"):
    return Paragraph(text, ST[style])


def callout(title, text, color=PALE, width=169):
    table = Table([[P(title, "box_b")], [P(text, "box")]], colWidths=[width * mm])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), color), ("BOX", (0, 0), (-1, -1), 0.7, ROSE),
        ("LINEBELOW", (0, 0), (-1, 0), 0.45, ROSE),
        ("LEFTPADDING", (0, 0), (-1, -1), 8), ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    return table


def grid(rows, widths, header=True, font="small"):
    data = [[P(cell, "box_b" if header and i == 0 else font) for cell in row] for i, row in enumerate(rows)]
    table = Table(data, colWidths=[w * mm for w in widths], repeatRows=1 if header else 0)
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
    table.setStyle(TableStyle(rules))
    return table


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
    canvas.drawCentredString(105 * mm, 57 * mm, "PÍSAL BY SOM - PÍSALA BY SOM")
    canvas.setFont("SK", 9)
    canvas.drawCentredString(105 * mm, 47 * mm, "želanie, predstava a zdvorilý návrh")
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
    canvas.drawString(20 * mm, 285 * mm, "SLOVOKROK  |  A2  |  ТЕМА 4.10  |  КОНДИЦИОНАЛ")
    canvas.setFillColor(MUTED)
    canvas.setFont("SK", 7.5)
    canvas.drawCentredString(105 * mm, 10 * mm, f"стр. {doc.page} / 7")
    canvas.restoreState()


doc = SimpleDocTemplate(
    str(OUT), pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm,
    topMargin=26 * mm, bottomMargin=17 * mm, title=TITLE,
    author="SlovoKrok", subject="Slovak A2 self-study module 4.10",
)
story = []

# 1. Cover
story += [
    Spacer(1, 23 * mm), P("SLOVOKROK • СЛОВАЦКИЙ A2", "cover_kicker"),
    P("ТЕМА 4.10", "cover_kicker"),
    P("Кондиционал<br/>с частицей by", "cover_title"),
    P("Podmieňovací spôsob s časticou by", "cover_sub"), Spacer(1, 14 * mm),
    Table(
        [[P("После модуля вы сможете", "box_b")],
         [P("• построить кондиционал для всех лиц;<br/>• согласовать форму по роду и числу;<br/>• выразить желание и воображаемое действие;<br/>• сделать предложение или вопрос мягче и естественнее.", "box")]],
        colWidths=[145 * mm],
        style=TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#FFF7FB")),
            ("LEFTPADDING", (0, 0), (-1, -1), 10), ("RIGHTPADDING", (0, 0), (-1, -1), 10),
            ("TOPPADDING", (0, 0), (-1, -1), 7), ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ]),
    ), PageBreak(),
]

# 2. Formation
story += [
    P("1. Формула: l-форма + by", "h1"),
    callout("Самая надёжная опора", "Возьмите форму, похожую на прошедшее время, добавьте <b>by</b> и нужную короткую форму: <i>Písal by som. Písala by si. Písali by sme.</i> В 3-м лице отдельного <i>som/si/sú</i> нет: <i>On by prišiel. Oni by prišli.</i>"),
    grid([
        ["Лицо", "Модель", "Пример и перевод"],
        ["ja", "by som", "Písal / písala by som. - Я бы написал / написала."],
        ["ty", "by si", "Písal / písala by si. - Ты бы написал / написала."],
        ["on / ona / ono", "by", "Písal / písala / písalo by. - Он бы написал / она бы написала / оно бы написало."],
        ["my", "by sme", "Písali by sme. - Мы бы написали."],
        ["vy", "by ste", "Písali by ste. - Вы бы написали."],
        ["oni / ony", "by", "Písali by. - Они бы написали."],
    ], [33, 34, 102]),
    P("Сравните с прошедшим временем", "h2"),
    grid([
        ["Прошедшее", "Кондиционал"],
        ["Písal som správu. - Я написал сообщение.", "Písal by som správu. - Я бы написал сообщение."],
        ["Išla si domov. - Ты пошла домой.", "Išla by si domov. - Ты бы пошла домой."],
        ["Prišli sme načas. - Мы пришли вовремя.", "Prišli by sme načas. - Мы бы пришли вовремя."],
    ], [84.5, 84.5]),
    callout("Не переносите русское бы отдельно", "В нейтральной форме держите блок рядом с l-формой: <i>urobil by som, išla by si, zostali by sme</i>. Не используйте *<i>bych</i> и не добавляйте *<i>sú</i> в 3-м лице.", CREAM),
    PageBreak(),
]

# 3. Agreement
story += [
    P("2. Род и число видны в l-форме", "h1"),
    P("Частица <i>by</i> не меняется. Кто говорит или действует, показывает l-форма: <i>-l, -la, -lo, -li</i>. Это особенно важно в 1-м и 2-м лице, где подлежащее часто опускается."),
    grid([
        ["Кто", "ísť", "byť", "Перевод"],
        ["я, мужчина", "išiel by som", "bol by som", "я бы пошёл / был"],
        ["я, женщина", "išla by som", "bola by som", "я бы пошла / была"],
        ["ты, мужчина", "išiel by si", "bol by si", "ты бы пошёл / был"],
        ["ты, женщина", "išla by si", "bola by si", "ты бы пошла / была"],
        ["оно", "išlo by", "bolo by", "оно бы пошло / было"],
        ["мы / вы / они", "išli by sme / ste / by", "boli by sme / ste / by", "мы / вы / они бы пошли / были"],
    ], [31, 46, 48, 44]),
    callout("В множественном числе проще, чем по-русски", "В современном словацком l-форма множественного числа оканчивается на <b>-li</b> независимо от рода: <i>ženy by prišli, deti by prišli, muži by prišli</i>.", BLUE),
    P("Желание с rád / rada / radi", "h2"),
    grid([
        ["Фраза", "Перевод"],
        ["Rád by som býval bližšie k centru.", "Я бы хотел жить ближе к центру. (говорит мужчина)"],
        ["Rada by som sa lepšie naučila po slovensky.", "Я бы хотела лучше выучить словацкий. (говорит женщина)"],
        ["Radi by sme cestovali častejšie.", "Мы бы хотели путешествовать чаще."],
        ["Rada by si pracovala z domu?", "Ты хотела бы работать из дома? (к женщине)"],
    ], [84, 85]),
    callout("Частая ошибка", "*<i>Rád by som išla</i> смешивает мужскую форму <i>rád</i> и женскую <i>išla</i>. Нужна одна линия согласования: <i>Rád by som išiel</i> или <i>Rada by som išla</i>.", CREAM),
    PageBreak(),
]

# 4. Meanings
story += [
    P("3. Желание, гипотеза и мягкое предложение", "h1"),
    grid([
        ["Функция", "Пример", "Перевод"],
        ["желание", "Rada by som si oddýchla.", "Я бы хотела отдохнуть."],
        ["воображаемое действие", "Bez mapy by sme sa stratili.", "Без карты мы бы заблудились."],
        ["гипотеза", "Keby som mal čas, išiel by som do hôr.", "Если бы у меня было время, я бы пошёл в горы."],
        ["предложение", "Išli by sme v sobotu na výlet?", "Не съездить ли нам в субботу на экскурсию?"],
        ["вежливое предложение", "Dali by ste si čaj?", "Вы бы хотели чаю?"],
        ["мягкий вопрос", "Požičal by si mi pero?", "Ты бы одолжил мне ручку?"],
    ], [40, 69, 60]),
    P("Keby уже содержит by", "h2"),
    callout("Рабочая схема", "<b>Keby + прошедшая форма, ... by + кондиционал.</b><br/><i>Keby som býval bližšie, chodil by som pešo.</i> - Если бы я жил ближе, я бы ходил пешком.<br/><i>Keby pršalo, zostali by sme doma.</i> - Если бы шёл дождь, мы бы остались дома.", BLUE),
    callout("Не удваивайте частицу", "Правильно: <i>Keby som vedel, povedal by som ti to.</i> Неправильно: *<i>Keby by som vedel...</i> После <i>keby</i> используется форма как в прошедшем времени: <i>keby som vedel, keby si prišla, keby sme mali</i>.", CREAM),
    P("Мини-диалог: свободный день", "h2"),
    callout("Čo by si robil?", "<b>Marek:</b> Čo by si robila, keby si mala voľný deň?<br/><b>Eva:</b> Ráno by som dlho spala. Potom by som išla do parku. A ty?<br/><b>Marek:</b> Ja by som navštívil kamarátov. Večer by sme si pozreli film.<br/><b>Eva:</b> To by bolo príjemné.<br/><br/><b>Перевод:</b> Марек: Что бы ты делала, если бы у тебя был свободный день? Ева: Утром я бы долго спала. Потом пошла бы в парк. А ты? Марек: Я бы навестил друзей. Вечером мы бы посмотрели фильм. Ева: Было бы приятно.", PALE),
    PageBreak(),
]

# 5. Word order
story += [
    P("4. Короткие формы и порядок слов", "h1"),
    P("<i>By, som, si, sme, ste, sa, si</i> - короткие безударные формы. В нейтральной фразе они стремятся к ранней позиции и образуют компактную группу."),
    grid([
        ["Модель", "Естественный пример", "Перевод"],
        ["l-форма + by som", "Zavolal by som ti večer.", "Я бы позвонил тебе вечером."],
        ["l-форма + by si", "Povedala by si mi pravdu?", "Ты бы сказала мне правду?"],
        ["by som + sa", "Vrátil by som sa skôr.", "Я бы вернулся раньше."],
        ["by som + si", "Kúpila by som si lístok.", "Я бы купила себе билет."],
        ["by sme + sa", "Stretli by sme sa pri stanici.", "Мы бы встретились у вокзала."],
        ["by ste + mi", "Poslali by ste mi adresu?", "Вы бы прислали мне адрес?"],
    ], [41, 68, 60]),
    callout("Короткая цепочка", "Практическая модель: <b>l-форма + by + som/si/sme/ste + sa/si + короткое местоимение</b>.<br/><i>Požičal by si mi ho?</i> - Ты бы одолжил мне его?<br/><i>Vysvetlili by ste nám to?</i> - Вы бы объяснили нам это?", BLUE),
    P("Отрицание", "h2"),
    grid([
        ["Утверждение", "Отрицание"],
        ["Išiel by som tam.", "Nešiel by som tam."],
        ["Kúpila by si si to.", "Nekúpila by si si to."],
        ["Prišli by sme načas.", "Neprišli by sme načas."],
    ], [84.5, 84.5]),
    callout("Порядок меняется ради акцента", "Возможны <i>Ja by som tam nešiel</i> и <i>Tam by som nešiel</i>: первое подчёркивает говорящего, второе - место. Для уверенной нейтральной речи начинайте с модели <i>Nešiel by som tam</i>.", CREAM),
    P("Граница следующей темы", "h2"),
    P("Здесь мы строим сам кондиционал и используем его без отдельного модального глагола. Условные просьбы и советы с особыми модальными значениями разбираются отдельно в следующем модуле."),
    PageBreak(),
]

# 6. Exercises
story += [
    P("5 - Ошибки и практика", "h1"),
    callout("Частые ошибки", "1) *<i>bych</i> вместо <i>by som</i>; 2) *<i>on by je prišiel</i> вместо <i>on by prišiel</i>; 3) несогласованный род; 4) *<i>keby by som</i>; 5) потеря <i>sa/si</i>; 6) разрыв коротких форм тяжёлыми словами.", CREAM),
    P("<b>1. Определите лицо и род, где это возможно.</b><br/>a) išla by som b) písali by ste c) prišiel by d) bola by si e) zostali by sme f) išlo by.", "task"),
    P("<b>2. Постройте кондиционал.</b><br/>a) ja, muž: ísť b) ja, žena: pracovať c) ty, žena: prísť d) my: zostať e) vy: napísať f) oni: bývať.", "task"),
    P("<b>3. Выберите согласованную форму.</b><br/>a) Anna by (prišiel / prišla). b) Peter by som to (urobil / urobila) - исправьте всё предложение. c) Rada by som (išiel / išla). d) Deti by (boli / bola) doma.", "task"),
    P("<b>4. Исправьте порядок и форму.</b><br/>a) *Ja išiel by som domov. b) *Keby by som mal čas, čítal by som. c) *Vrátil sa by som skôr. d) *Ona by je prišla. e) *Ne by som tam išiel.", "task"),
    P("<b>5. Переведите.</b><br/>a) Я бы хотела отдохнуть. b) Если бы шёл дождь, мы бы остались дома. c) Ты бы одолжил мне ручку? d) Вы бы хотели чаю? e) Я бы не пошёл туда.", "task"),
    P("<b>6. Воображаемый свободный день.</b> Напишите 5-7 предложений: что вы делали бы, куда пошли бы и с кем встретились бы. Используйте <i>keby</i>, одну отрицательную форму, <i>sa/si</i> и согласование со своим родом.", "task"),
    PageBreak(),
]

# 7. Answers
story += [
    P("6. Ответы и итог", "h1"),
    P("<b>1.</b> a) 1-е лицо ед. ч., женщина; b) 2-е лицо мн. ч. / вежливое Вы; c) 3-е лицо ед. ч., мужчина; d) 2-е лицо ед. ч., женщина; e) 1-е лицо мн. ч.; f) 3-е лицо ед. ч., средний род.", "answer"),
    P("<b>2.</b> a) išiel by som; b) pracovala by som; c) prišla by si; d) zostali by sme; e) napísali by ste; f) bývali by.", "answer"),
    P("<b>3.</b> a) Anna by <b>prišla</b>. b) Peter by to <b>urobil</b>. c) Rada by som <b>išla</b>. d) Deti by <b>boli</b> doma.", "answer"),
    P("<b>4.</b> a) Išiel by som domov. / Ja by som išiel domov. b) Keby som mal čas, čítal by som. c) Vrátil by som sa skôr. d) Ona by prišla. e) Nešiel by som tam. / Ja by som tam nešiel.", "answer"),
    P("<b>5.</b> a) Rada by som si oddýchla. b) Keby pršalo, zostali by sme doma. c) Požičal by si mi pero? d) Dali by ste si čaj? e) Nešiel by som tam.", "answer"),
    P("Образец к заданию 6", "h2"),
    callout("Môj voľný deň", "Keby som mal voľný deň, ráno by som dlho spal. Potom by som si pripravil dobré raňajky. Poobede by som išiel do lesa a stretol by som sa s kamarátom. Nezostal by som celý deň doma. Večer by sme si pozreli film. Rád by som si taký deň čoskoro zopakoval.<br/><br/>Если бы у меня был свободный день, утром я бы долго спал. Потом приготовил бы себе хороший завтрак. После обеда пошёл бы в лес и встретился с другом. Я бы не остался дома на весь день. Вечером мы посмотрели бы фильм. Я хотел бы вскоре повторить такой день.", BLUE),
    P("Четыре опоры", "h2"),
    grid([
        ["1", "Форма: l-форма + by; для ja/ty/my/vy добавляются som/si/sme/ste."],
        ["2", "Род виден в ед. числе: išiel / išla / išlo; множественное число имеет -li."],
        ["3", "Keby уже содержит by: keby som mal, не *keby by som mal."],
        ["4", "Короткие формы держатся группой: vrátil by som sa, kúpil by som si."],
    ], [14, 155], header=False),
    callout("Проверка освоения", "Я могу:  □ построить формы всех лиц;  □ согласовать род;  □ выразить желание и гипотезу;  □ удержать естественный порядок коротких форм.", GREEN),
]

OUT.parent.mkdir(parents=True, exist_ok=True)
doc.build(story, onFirstPage=first_page, onLaterPages=later_page)
print(OUT)
