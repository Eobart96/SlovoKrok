from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output/pdf/A2/Module_07/Slovak_A2_Tema_7_3_Poruchenie_vstrecha_i_izmenenie_plana.pdf"
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
BODY = ParagraphStyle(
    "Body", fontName="Arial", fontSize=8.65, leading=11.3,
    textColor=INK, spaceAfter=2.7 * mm,
)
SMALL = ParagraphStyle(
    "Small", parent=BODY, fontSize=7.45, leading=9.2, spaceAfter=1.4 * mm,
)
TINY = ParagraphStyle(
    "Tiny", parent=BODY, fontSize=6.65, leading=8.1, spaceAfter=0.9 * mm,
)
TITLE = ParagraphStyle(
    "Title", fontName="Arial-Bold", fontSize=20, leading=24,
    textColor=colors.white, alignment=TA_LEFT, spaceAfter=5 * mm,
)
SUBTITLE = ParagraphStyle(
    "Subtitle", fontName="Arial", fontSize=11.5, leading=15,
    textColor=colors.HexColor("#FFD8EB"), spaceAfter=5 * mm,
)
H1 = ParagraphStyle(
    "H1", fontName="Arial-Bold", fontSize=15.5, leading=18.5,
    textColor=PLUM, spaceBefore=1 * mm, spaceAfter=3 * mm,
)
H2 = ParagraphStyle(
    "H2", fontName="Arial-Bold", fontSize=10.7, leading=13.2,
    textColor=PINK, spaceBefore=1.1 * mm, spaceAfter=1.4 * mm,
)
KICK = ParagraphStyle(
    "Kicker", fontName="Arial-Bold", fontSize=10, leading=12,
    textColor=colors.HexColor("#FFD8EB"), spaceAfter=4 * mm,
)


def p(text, style=BODY):
    return Paragraph(text, style)


def box(text, bg=PALE, border=ROSE, style=BODY, pad=7):
    item = Table([[p(text, style)]], colWidths=[170 * mm])
    item.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("BOX", (0, 0), (-1, -1), 0.7, border),
        ("LEFTPADDING", (0, 0), (-1, -1), pad),
        ("RIGHTPADDING", (0, 0), (-1, -1), pad),
        ("TOPPADDING", (0, 0), (-1, -1), pad),
        ("BOTTOMPADDING", (0, 0), (-1, -1), pad),
    ]))
    return item


def table(data, widths, size=7.0, header=True):
    rows = []
    for row_index, row in enumerate(data):
        cell_style = ParagraphStyle(
            f"cell_{row_index}_{size}_{len(data)}",
            parent=SMALL,
            fontSize=size,
            leading=size + 1.75,
            textColor=colors.white if header and row_index == 0 else INK,
            fontName="Arial-Bold" if header and row_index == 0 else "Arial",
            spaceAfter=0,
        )
        rows.append([p(str(value), cell_style) for value in row])
    item = Table(rows, colWidths=widths, repeatRows=1 if header else 0)
    commands = [
        ("GRID", (0, 0), (-1, -1), 0.45, ROSE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
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
        canvas.drawString(20 * mm, height - 12 * mm, "A2 7.3  |  Поручение, встреча и изменение плана")
    canvas.setFont("Arial", 8)
    canvas.setFillColor(MUTED)
    canvas.drawString(20 * mm, 9 * mm, "SlovoKrok | личный учебный модуль")
    canvas.drawRightString(width - 20 * mm, 9 * mm, f"стр. {page_number} / 7")
    canvas.restoreState()


doc = BaseDocTemplate(
    str(OUTPUT),
    pagesize=A4,
    leftMargin=20 * mm,
    rightMargin=20 * mm,
    topMargin=20 * mm,
    bottomMargin=18 * mm,
    title="Slovak A2 - Тема 7.3 - Поручение, встреча и изменение плана",
    author="SlovoKrok",
)
doc.addPageTemplates([
    PageTemplate(
        id="series",
        frames=[Frame(20 * mm, 18 * mm, 170 * mm, 257 * mm, id="main", leftPadding=0, rightPadding=0)],
        onPage=draw_page,
    )
])


story = [
    p("МОДУЛЬ 7  •  РАБОТА, ПУТЕШЕСТВИЯ И СТРАНА", KICK),
    p("Поручение, встреча и изменение плана", TITLE),
    p("Úloha, stretnutie a zmena plánu: договариваемся, извиняемся и передаём изменение", SUBTITLE),
    Spacer(1, 41 * mm),
    p("На уровне A2 нужно не только понять рабочую просьбу, но и подтвердить результат и срок, корректно перенести встречу и ясно сообщить коллеге новый план."),
    p("После модуля вы сможете:", H2),
    table([
        ["1", "принять поручение и уточнить срок"],
        ["2", "обещать процесс или готовый результат"],
        ["3", "перенести встречу с объяснением и извинением"],
        ["4", "передать коллеге изменение письменно или устно"],
    ], [12 * mm, 158 * mm], 7.2, False),
    Spacer(1, 3 * mm),
    box("<b>Формула:</b> подтверждаю задачу + уточняю срок + называю действие + объясняю изменение + сообщаю новый план."),
    PageBreak(),

    p("1. Поручение: задача, срок, подтверждение", H1),
    p("Хорошая рабочая договорённость содержит три вещи: <b>что сделать</b>, <b>к какому сроку</b> и <b>какой результат ожидается</b>. Повторите ключевую информацию своими словами."),
    table([
        ["Шаг", "Неформально", "Формально"],
        ["попросить", "Môžeš pripraviť tabuľku?", "Mohli by ste pripraviť tabuľku?"],
        ["уточнить", "Kedy to potrebuješ?", "Dokedy to potrebujete?"],
        ["подтвердить", "Dobre, urobím to dnes.", "Samozrejme, pošlem Vám to dnes."],
        ["проверить детали", "Mám poslať aj prílohu?", "Mám priložiť aj dokumenty?"],
        ["предупредить", "Ak bude problém, ozvem sa.", "Ak vznikne problém, budem Vás informovať."],
    ], [32 * mm, 67 * mm, 71 * mm], 5.5),
    p("Полезные сроки", H2),
    table([
        ["Фраза", "Перевод", "Пример"],
        ["do obeda", "до обеда", "Pošlem to do obeda."],
        ["do konca dňa", "до конца дня", "Správu dokončím do konca dňa."],
        ["najneskôr v piatok", "не позднее пятницы", "Ozvem sa najneskôr v piatok."],
        ["čo najskôr", "как можно скорее", "Prosím, skontrolujte to čo najskôr."],
    ], [40 * mm, 48 * mm, 82 * mm], 5.65),
    box("<b>A2-привычка:</b> вместо одного <i>Áno</i> скажите результат и срок: <i>Áno, skontrolujem objednávku a odpoveď Vám pošlem do tretej.</i>", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    PageBreak(),

    p("2. Два будущих времени в рабочем плане", H1),
    p("С несовершенным глаголом используйте <b>budem + infinitív</b>, когда важны процесс или занятость. Совершенный глагол в форме настоящего времени обозначает будущий готовый результат."),
    table([
        ["Процесс / ход работы", "Готовый результат", "Разница"],
        ["Budem pripravovať prezentáciu.", "Pripravím prezentáciu.", "буду готовить / подготовлю"],
        ["Budem kontrolovať údaje.", "Skontrolujem údaje.", "буду проверять / проверю"],
        ["Budem písať správu.", "Napíšem správu.", "буду писать / напишу"],
        ["Budem volať klientovi.", "Zavolám klientovi.", "буду звонить / позвоню"],
        ["Budem posielať súbory.", "Pošlem súbory.", "буду отправлять / отправлю"],
    ], [62 * mm, 60 * mm, 48 * mm], 5.65),
    p("Что выбрать в договорённости", H2),
    table([
        ["Ситуация", "Естественная фраза", "Почему"],
        ["занятость в период", "Zajtra budem pracovať na rozpočte.", "важен процесс завтра"],
        ["обещание результата", "Rozpočet dokončím zajtra do obeda.", "важен готовый файл"],
        ["последовательность", "Najprv skontrolujem údaje a potom pošlem správu.", "два завершённых шага"],
        ["длительная задача", "Celý týždeň budeme testovať nový systém.", "важна длительность"],
    ], [39 * mm, 79 * mm, 52 * mm], 5.55),
    box("<b>Ошибка:</b> не говорите *budem pripraviť*. С совершенным <i>pripraviť</i> используйте <b>pripravím</b>; с несовершенным <i>pripravovať</i> - <b>budem pripravovať</b>.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    PageBreak(),

    p("3. Kedy/keď и pretože/preto", H1),
    p("<b>Kedy?</b> задаёт вопрос о времени. <b>Keď</b> соединяет событие и момент. <b>Pretože</b> вводит причину, а <b>preto</b> сообщает следствие."),
    table([
        ["Связка", "Пример", "Перевод"],
        ["kedy?", "Kedy sa môžeme stretnúť?", "Когда мы можем встретиться?"],
        ["keď", "Keď dokončím správu, pošlem ju.", "Когда закончу отчёт, отправлю его."],
        ["pretože", "Stretnutie presunieme, pretože Jana ochorela.", "Перенесём встречу, потому что Яна заболела."],
        ["preto", "Jana ochorela, preto stretnutie presunieme.", "Яна заболела, поэтому перенесём встречу."],
    ], [26 * mm, 79 * mm, 65 * mm], 5.7),
    p("Перенос встречи: четыре шага", H2),
    table([
        ["Шаг", "Рабочая фраза"],
        ["1. извинение", "Ospravedlňujem sa, ale zajtrajší termín mi nevyhovuje."],
        ["2. причина", "Musím stretnutie presunúť, pretože mám dôležitú poradu."],
        ["3. новый вариант", "Môžeme sa stretnúť vo štvrtok o desiatej?"],
        ["4. подтверждение", "Keď Vám termín vyhovuje, prosím, potvrďte ho."],
    ], [39 * mm, 131 * mm], 5.7),
    box("<b>Мини-диалог:</b><br/><b>Peter:</b> Kedy dokončíš prezentáciu?<br/><b>Lucia:</b> Dokončím ju dnes, ale budem ju ešte ráno kontrolovať.<br/><b>Peter:</b> Dobre. Zajtrajšie stretnutie presunieme na jedenástu, pretože klient príde neskôr.<br/><b>Lucia:</b> Rozumiem. Keď prezentáciu skontrolujem, pošlem ju aj klientovi.", PALE, ROSE, SMALL),
    PageBreak(),

    p("4. Передаём изменение коллеге", H1),
    p("При медиации вы не придумываете решение, а точно передаёте: <b>что изменилось</b>, <b>почему</b>, <b>каков новый срок</b> и <b>что должен сделать коллега</b>."),
    table([
        ["SK", "RU"],
        ["Mám pre teba novú informáciu.", "У меня для тебя новая информация."],
        ["Pôvodný termín už neplatí.", "Прежний срок больше не действует."],
        ["Porada sa presúva na štvrtok.", "Совещание переносится на четверг."],
        ["Začneme o hodinu neskôr.", "Мы начнём на час позже."],
        ["Dôvodom je návšteva klienta.", "Причина - визит клиента."],
        ["Prosím, informuj aj ostatných.", "Пожалуйста, сообщи также остальным."],
        ["Dokumenty pošli do stredy.", "Отправь документы до среды."],
        ["Keď dostaneš odpoveď, ozvi sa mi.", "Когда получишь ответ, сообщи мне."],
        ["Nový termín mi vyhovuje.", "Новый срок мне подходит."],
        ["Ďakujem za pochopenie.", "Спасибо за понимание."],
    ], [87 * mm, 83 * mm], 5.35),
    p("Модель рабочего сообщения", H2),
    box("<b>Predmet: Zmena termínu porady</b><br/>Dobrý deň, ospravedlňujem sa za zmenu. Zajtrajšia porada sa presúva z 9.00 na 11.00, pretože klient príde neskôr. Stretneme sa v zasadacej miestnosti na druhom poschodí. Prosím, pripravte aktualizované údaje a informujte aj kolegyňu Janu. Keď Vám nový termín nevyhovuje, dajte mi vedieť ešte dnes. Ďakujem za pochopenie.", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    p("Проверка точности: старое время 9.00 → новое 11.00; причина → клиент приедет позже; действие коллеги → подготовить данные и сообщить Яне.", TINY),
    PageBreak(),

    p("5. Частые ошибки и упражнения", H1),
    box("<b>Частые ошибки:</b> *budem pripraviť* вместо <b>pripravím</b>; вопрос с <i>keď</i> вместо <b>kedy</b>; причина после <b>preto</b>; перенос без нового времени; сообщение коллеге без ясного действия.", CREAM, colors.HexColor("#E7C76C"), TINY),
    p("Упражнение 1. Процесс или результат?", H2),
    p("1) Zajtra celý deň budem pripravovať/pripravím prezentáciu. 2) Prezentáciu budem pripravovať/pripravím do obeda. 3) Najprv budem kontrolovať/skontrolujem údaje a potom pošlem správu.", TINY),
    p("Упражнение 2. Вставьте kedy или keď", H2),
    p("1) ___ sa môžeme stretnúť? 2) ___ dokončím úlohu, ozvem sa. 3) Neviete, ___ príde klient? 4) ___ klient príde, začneme poradu.", TINY),
    p("Упражнение 3. Вставьте pretože или preto", H2),
    p("1) Meškám, ___ autobus neprišiel. 2) Autobus neprišiel, ___ budem meškať. 3) Stretnutie presunieme, ___ Jana je chorá.", TINY),
    p("Упражнение 4. Исправьте ошибки", H2),
    p("1) Budem dokončiť správu dnes. 2) Keď sa stretneme? 3) Meškám, preto autobus neprišiel. 4) Poradu presunieme. (Добавьте новый срок.)", TINY),
    p("Упражнение 5. Переведите", H2),
    p("1) Я закончу отчёт до конца дня. 2) Когда получишь ответ, сообщи мне. 3) Встречу перенесём на четверг, потому что клиент приедет позже. 4) Спасибо за понимание.", TINY),
    p("Упражнение 6. Передайте изменение", H2),
    p("Напишите 6-8 предложений коллеге: извинитесь, перенесите встречу со вторника 10.00 на среду 14.00, назовите причину, попросите подготовить документы и подтвердить новый срок.", TINY),
    PageBreak(),

    p("6. Ответы и проверка мастерства", H1),
    p("Ответы", H2),
    p("<b>1.</b> 1) budem pripravovať; 2) pripravím; 3) skontrolujem.", TINY),
    p("<b>2.</b> 1) Kedy; 2) Keď; 3) kedy; 4) Keď.", TINY),
    p("<b>3.</b> 1) pretože; 2) preto; 3) pretože.", TINY),
    p("<b>4.</b> 1) <b>Dokončím správu dnes</b>. 2) <b>Kedy sa stretneme?</b> 3) <b>Meškám, pretože autobus neprišiel</b>. 4) Например: <b>Poradu presunieme na štvrtok o desiatej</b>.", TINY),
    p("<b>5.</b> Správu dokončím do konca dňa. Keď dostaneš odpoveď, ozvi sa mi. Stretnutie presunieme na štvrtok, pretože klient príde neskôr. Ďakujem za pochopenie.", TINY),
    p("<b>6. Модель:</b> Dobrý deň, ospravedlňujem sa za zmenu. Stretnutie v utorok o 10.00 musíme presunúť, pretože klient nemôže prísť. Nový termín je v stredu o 14.00. Prosím, pripravte všetky dokumenty do obeda. Keď budete mať dokumenty hotové, pošlite mi ich. Prosím, potvrďte, či Vám nový termín vyhovuje. Ďakujem za pochopenie. Возможны другие естественные варианты.", TINY),
    p("Итог в четырёх пунктах", H2),
    table([
        ["OK", "Подтверждаю поручение, результат и срок."],
        ["OK", "Различаю процесс budem robiť и результат urobím."],
        ["OK", "Различаю kedy/keď и pretože/preto."],
        ["OK", "Передаю изменение: причина, новый срок и действие."],
    ], [12 * mm, 158 * mm], 6.15, False),
    Spacer(1, 2 * mm),
    box("<b>Финальная проверка:</b> за 60 секунд примите поручение, уточните срок и пообещайте результат. Затем перенесите встречу, объясните причину и передайте новый план коллеге.", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    p("Следующий шаг", H2),
    p("В теме 7.4 вы будете выбирать рейс, покупать билет и уточнять маршрут и пересадку.", SMALL),
]

doc.build(story)
print(OUTPUT)
