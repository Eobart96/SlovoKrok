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
OUTPUT = ROOT / "output/pdf/A2/Module_08/Slovak_A2_Tema_8_3_Samochuvstvie_i_razgovor_s_vrachom.pdf"
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
        canvas.drawString(20 * mm, height - 12 * mm, "A2 8.3  |  Самочувствие и разговор с врачом")
    canvas.setFont("Arial", 8)
    canvas.setFillColor(MUTED)
    canvas.drawString(20 * mm, 9 * mm, "SlovoKrok | личный учебный модуль")
    canvas.drawRightString(width - 20 * mm, 9 * mm, f"стр. {page_number} / 7")
    canvas.restoreState()


doc = BaseDocTemplate(
    str(OUTPUT), pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=20 * mm, bottomMargin=18 * mm,
    title="Slovak A2 - Тема 8.3 - Самочувствие и разговор с врачом", author="SlovoKrok",
)
doc.addPageTemplates([PageTemplate(
    id="series", frames=[Frame(20 * mm, 18 * mm, 170 * mm, 257 * mm, id="main", leftPadding=0, rightPadding=0)], onPage=draw_page,
)])


story = [
    p("МОДУЛЬ 8  •  ОТНОШЕНИЯ, ЗДОРОВЬЕ И ИТОГ A2", KICK),
    p("Самочувствие и разговор с врачом", TITLE),
    p("Ako sa cítite? Описываем симптомы, длительность и понимаем инструкции", SUBTITLE),
    Spacer(1, 44 * mm),
    p("На уровне A2 нужно точно назвать основную жалобу, сказать, когда она началась и насколько сильна, ответить на вопросы врача и понять простые инструкции при осмотре."),
    p("После модуля вы сможете:", H2),
    table([
        ["1", "сказать, что и у кого болит: Bolí ma... / Bolia ma..."],
        ["2", "описать общее состояние через Je mi..."],
        ["3", "указать начало, длительность и интенсивность симптома"],
        ["4", "ответить врачу и понять формальные инструкции"],
    ], [12 * mm, 158 * mm], 7.1, False),
    Spacer(1, 3 * mm),
    box("<b>Формула приёма:</b> главная жалоба → когда началось → насколько сильно → дополнительные симптомы → инструкции врача."),
    Spacer(1, 3 * mm),
    box("Этот модуль тренирует словацкий язык и не заменяет медицинскую консультацию.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    PageBreak(),

    p("1. Bolí ma...: что и у кого болит", H1),
    p("В словацкой модели часть тела является подлежащим, поэтому глагол согласуется с ней. Человек стоит в винительном: <i>ma, ťa, ho, ju, nás, vás, ich</i>."),
    table([
        ["Часть тела", "Модель", "Перевод"],
        ["hlava", "Bolí ma hlava.", "У меня болит голова."],
        ["hrdlo", "Bolí ťa hrdlo?", "У тебя болит горло?"],
        ["brucho", "Bolí ho brucho.", "У него болит живот."],
        ["chrbát", "Bolí ju chrbát.", "У неё болит спина."],
        ["oči", "Bolia ma oči.", "У меня болят глаза."],
        ["nohy", "Bolia vás nohy?", "У вас болят ноги?"],
        ["kĺby", "Bolia ich kĺby.", "У них болят суставы."],
    ], [32 * mm, 68 * mm, 70 * mm], 5.45),
    p("Единственное и множественное", H2),
    table([
        ["Глагол", "Когда", "Примеры"],
        ["bolí", "одна часть или неисчисляемое", "Bolí ma zub. Bolí ma pravé ucho."],
        ["bolia", "несколько частей", "Bolia ma oba členky. Bolia ho ramená."],
    ], [27 * mm, 52 * mm, 91 * mm], 5.6),
    p("Где именно?", H2),
    table([
        ["Фраза", "Перевод"],
        ["Bolí ma to tu vpravo.", "У меня болит вот здесь справа."],
        ["Bolesť ide do ľavej ruky.", "Боль отдаёт в левую руку."],
        ["Najviac ma to bolí pri pohybe.", "Сильнее всего болит при движении."],
        ["Pri prehĺtaní ma bolí hrdlo.", "При глотании у меня болит горло."],
    ], [86 * mm, 84 * mm], 5.6),
    box("<b>Русская ловушка:</b> не *<i>mám bolí hlava</i>, а <i>bolí ma hlava</i>. Если частей тела несколько, используйте <i>bolia</i>.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    PageBreak(),

    p("2. Je mi... и основные симптомы", H1),
    p("Модель <b>je mi + наречие</b> описывает общее состояние. Форма <i>mi</i> означает «мне»; при другом человеке меняется только дательный: <i>ti, mu, jej, nám, vám, im</i>."),
    table([
        ["Состояние", "Пример", "Перевод"],
        ["zle", "Je mi zle.", "Мне плохо."],
        ["nevoľno", "Od rána mi je nevoľno.", "С утра меня тошнит."],
        ["slabo", "Poobede mi bolo slabo.", "Днём я чувствовал слабость."],
        ["horúco", "V noci mi bolo veľmi horúco.", "Ночью мне было очень жарко."],
        ["chladno", "Je vám chladno?", "Вам холодно?"],
        ["lepšie / horšie", "Dnes mi je trochu lepšie.", "Сегодня мне немного лучше."],
    ], [31 * mm, 69 * mm, 70 * mm], 5.4),
    p("Банк симптомов", H2),
    table([
        ["Словацкий", "Русский", "Пример"],
        ["kašeľ", "кашель", "Mám suchý kašeľ."],
        ["nádcha", "насморк", "Už tri dni mám nádchu."],
        ["zvýšená teplota", "повышенная температура", "Večer som mal zvýšenú teplotu."],
        ["horúčka", "жар", "V noci som mala vysokú horúčku."],
        ["zimnica", "озноб", "Včera ma trápila zimnica."],
        ["závrat", "головокружение", "Ráno sa mi zatočila hlava."],
        ["únava", "усталость", "Cítim veľkú únavu."],
    ], [39 * mm, 48 * mm, 83 * mm], 5.1),
    p("Интенсивность", H2),
    box("<i>trochu</i> - немного; <i>dosť</i> - довольно; <i>veľmi</i> - очень; <i>mierna bolesť</i> - умеренная боль; <i>silná bolesť</i> - сильная боль. На вопрос <i>Ako silno vás to bolí?</i> можно ответить: <i>Asi šesť z desiatich.</i>", PALE, ROSE, SMALL),
    PageBreak(),

    p("3. Когда началось и как менялось", H1),
    p("Врач обычно уточняет начало, длительность и изменение состояния. Для завершённого события используйте прошедшее время; род говорящего виден в форме на <i>-l / -la</i>."),
    table([
        ["Вопрос врача", "Возможный ответ", "Перевод"],
        ["Kedy sa to začalo?", "Začalo sa to včera večer.", "Когда началось? - Вчера вечером."],
        ["Ako dlho vás to bolí?", "Bolí ma to už tri dni.", "Как долго болит? - Уже три дня."],
        ["Odkedy máte kašeľ?", "Kašeľ mám od pondelka.", "С каких пор кашель? - С понедельника."],
        ["Zhoršilo sa to?", "Áno, v noci sa to zhoršilo.", "Стало хуже? - Да, ночью."],
        ["Mali ste teplotu?", "Včera som mal teplotu tridsaťosem stupňov.", "Была температура? - Вчера было 38."],
        ["Čo sa stalo ráno?", "Ráno sa mi zatočila hlava.", "Что случилось утром? - Закружилась голова."],
    ], [46 * mm, 72 * mm, 52 * mm], 4.95),
    p("Полезные указатели времени", H2),
    table([
        ["Модель", "Пример"],
        ["od + G", "Od včera ma bolí hrdlo."],
        ["už + длительность", "Už dva dni sa necítim dobre."],
        ["pred + I", "Začalo sa to pred troma dňami."],
        ["celý / celú", "Celú noc som kašľala."],
        ["najprv / potom", "Najprv ma bolela hlava, potom som dostal teplotu."],
    ], [47 * mm, 123 * mm], 5.45),
    p("Мужчина или женщина", H2),
    box("Мужчина: <i>Včera som mal teplotu a bol som unavený.</i><br/>Женщина: <i>Včera som mala teplotu a bola som unavená.</i><br/>Симптом без рода: <i>Včera ma bolela hlava.</i>", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    box("<b>Порядок ответа:</b> <i>Od pondelka mám suchý kašeľ. Včera večer som mal teplotu. Dnes mi je trochu lepšie, ale stále ma bolí hrdlo.</i>", PALE, ROSE, SMALL),
    PageBreak(),

    p("4. Понимаем врача: формальный императив", H1),
    p("На приёме врач обращается вежливо на <b>vy</b>. Формы обычно оканчиваются на <b>-te</b>. В возвратных командах сохраняется <i>sa / si</i>."),
    table([
        ["Инструкция", "Перевод"],
        ["Sadnite si, prosím.", "Садитесь, пожалуйста."],
        ["Otvorte ústa.", "Откройте рот."],
        ["Zhlboka sa nadýchnite.", "Глубоко вдохните."],
        ["Pomaly vydýchnite.", "Медленно выдохните."],
        ["Nehýbte sa.", "Не двигайтесь."],
        ["Vyhrňte si rukáv.", "Поднимите рукав."],
        ["Ľahnite si na chrbát.", "Лягте на спину."],
        ["Príďte na kontrolu o tri dni.", "Приходите на контроль через три дня."],
    ], [85 * mm, 85 * mm], 5.65),
    p("Мини-диалог у врача", H2),
    box("<b>Lekár:</b> Dobrý deň. Čo vás trápi?<br/><b>Pacient:</b> Od včera ma bolí hrdlo a mám suchý kašeľ.<br/><b>Lekár:</b> Mali ste aj teplotu?<br/><b>Pacient:</b> Áno, včera večer som mal teplotu tridsaťosem stupňov.<br/><b>Lekár:</b> Ako silno vás bolí hrdlo?<br/><b>Pacient:</b> Dosť silno, najmä pri prehĺtaní.<br/><b>Lekár:</b> Dobre. Otvorte ústa a potom sa zhlboka nadýchnite.<br/><b>Pacient:</b> Rozumiem.<br/><b>Lekár:</b> Oddychujte, pite dostatok tekutín a príďte na kontrolu, ak sa stav nezlepší.", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    p("Как переспросить", H2),
    table([
        ["Prosím, zopakujte to.", "Пожалуйста, повторите."],
        ["Mám sa zhlboka nadýchnuť?", "Мне нужно глубоко вдохнуть?"],
        ["Kedy mám prísť na kontrolu?", "Когда мне прийти на контроль?"],
    ], [88 * mm, 82 * mm], 5.55, False),
    PageBreak(),

    p("5. Частые ошибки и упражнения", H1),
    table([
        ["Ошибка", "Правильно", "Почему"],
        ["*Mám bolí hlava.", "Bolí ma hlava.", "часть тела = N"],
        ["*Bolí mi hrdlo.", "Bolí ma hrdlo.", "человек = A"],
        ["*Bolí ma oči.", "Bolia ma oči.", "множественное число"],
        ["*Som zle.", "Je mi zle.", "общее состояние"],
        ["*Otvoríte ústa!", "Otvorte ústa.", "формальный императив"],
    ], [49 * mm, 59 * mm, 62 * mm], 5.1),
    p("Упражнение 1. Выберите bolí / bolia", H2),
    p("1) ___ ma hlava. 2) ___ ho obe kolená. 3) ___ vás chrbát? 4) ___ ju oči.", SMALL),
    p("Упражнение 2. Вставьте ma / vás / mi / vám", H2),
    p("1) Bolí ___ hrdlo. (я) 2) Je ___ nevoľno. (я) 3) Bolia ___ nohy? (Вы) 4) Je ___ dnes lepšie? (Вы)", SMALL),
    p("Упражнение 3. Ответьте о времени", H2),
    p("Используйте подсказку: 1) Odkedy máte kašeľ? (pondelok) 2) Ako dlho vás to bolí? (tri dni) 3) Kedy sa to začalo? (včera večer) 4) Čo sa stalo v noci? (zhoršiť sa)", SMALL),
    p("Упражнение 4. Сделайте формальную инструкцию", H2),
    p("1) otvoriť ústa 2) zhlboka sa nadýchnuť 3) nehýbať sa 4) sadnúť si 5) prísť na kontrolu.", SMALL),
    p("Упражнение 5. Переведите", H2),
    p("1) С утра меня тошнит. 2) Горло болит уже два дня. 3) Вчера вечером у меня была температура. 4) Сильнее всего болит при движении.", SMALL),
    p("Упражнение 6. Самостоятельный ответ врачу", H2),
    p("Составьте 6-7 предложений: главная жалоба, начало и длительность, интенсивность, один дополнительный симптом, изменение состояния и уточняющий вопрос врачу.", SMALL),
    PageBreak(),

    p("6. Ответы и проверка мастерства", H1),
    p("Ответы", H2),
    table([
        ["№", "Ключ"],
        ["1", "1 Bolí; 2 Bolia; 3 Bolí; 4 Bolia."],
        ["2", "1 ma; 2 mi; 3 vás; 4 vám."],
        ["3", "1 Kašeľ mám od pondelka. 2 Bolí ma to už tri dni. 3 Začalo sa to včera večer. 4 V noci sa to zhoršilo."],
        ["4", "1 Otvorte ústa. 2 Zhlboka sa nadýchnite. 3 Nehýbte sa. 4 Sadnite si. 5 Príďte na kontrolu."],
        ["5", "1 Od rána mi je nevoľno. 2 Už dva dni ma bolí hrdlo. 3 Včera večer som mal / mala teplotu. 4 Najviac ma to bolí pri pohybe."],
        ["6", "Открытое задание: возможны другие естественные ответы при сохранении всех пунктов условия."],
    ], [13 * mm, 157 * mm], 5.15),
    p("Модель самостоятельного ответа", H2),
    box("Od pondelka sa necítim dobre. Najviac ma bolí hrdlo a mám suchý kašeľ. Bolí ma to už tri dni, najmä pri prehĺtaní. Včera večer som mala zvýšenú teplotu a v noci sa mi stav zhoršil. Dnes mi je trochu lepšie, ale stále som veľmi unavená. Je táto bolesť podľa vás silná? Kedy mám prísť na kontrolu?", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    p("Четыре опоры темы", H2),
    table([
        ["1", "Одна часть: <i>Bolí ma hlava</i>; несколько: <i>Bolia ma oči</i>."],
        ["2", "Общее состояние: <i>Je mi zle / nevoľno / lepšie</i>."],
        ["3", "Всегда добавляйте время: <i>od včera, už tri dni, pred týždňom</i>."],
        ["4", "Формальная инструкция: <i>Otvorte, sadnite si, nadýchnite sa, príďte</i>."],
    ], [11 * mm, 159 * mm], 5.65, False),
    p("Финальная проверка", H2),
    box("Без подсказки назовите четыре симптома; скажите, что болит; укажите начало, длительность и силу; ответьте в прошедшем времени; выполните три инструкции врача. Если получается связный ответ, цель 8.3 достигнута.", PALE, ROSE, SMALL),
]

doc.build(story)
print(OUTPUT)
