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
OUTPUT = ROOT / "output" / "pdf" / "A2" / "Module_05" / "Slovak_A2_Tema_5_2_Parnye_soyuzy_aj_aj_i_ani_ani.pdf"
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
        canvas.drawString(20 * mm, height - 12 * mm, "A2 5.2  |  Парные союзы aj - aj и ani - ani")
    canvas.setFont("Arial", 8)
    canvas.setFillColor(MUTED)
    canvas.drawString(20 * mm, 9 * mm, "SlovoKrok | личный учебный модуль")
    canvas.drawRightString(width - 20 * mm, 9 * mm, f"стр. {page} / 7")
    canvas.restoreState()


doc = BaseDocTemplate(
    str(OUTPUT), pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=20 * mm, bottomMargin=18 * mm,
    title="Slovak A2 - Тема 5.2 - Парные союзы aj - aj и ani - ani", author="SlovoKrok",
)
frame = Frame(20 * mm, 18 * mm, 170 * mm, 257 * mm, id="main", leftPadding=0, rightPadding=0)
doc.addPageTemplates([PageTemplate(id="series", frames=[frame], onPage=draw_page)])

story = [
    p("МОДУЛЬ 5  •  СВЯЗНАЯ РЕЧЬ И СЛОЖНЫЕ ПРЕДЛОЖЕНИЯ", COVER_KICKER),
    p("Парные союзы<br/>aj - aj и ani - ani", TITLE),
    p("Zdôrazňujeme obe možnosti: включаем оба или исключаем оба", SUBTITLE),
    Spacer(1, 35 * mm),
    p("Одиночное <b>a</b> просто соединяет элементы. Парные союзы делают связь заметнее: <b>aj - aj</b> подчёркивает, что верны оба элемента, а <b>ani - ani</b> исключает оба."),
    p("После модуля вы сможете:", H2),
    styled_table([
        ["1", "подчёркивать два включённых элемента конструкцией aj - aj"],
        ["2", "исключать оба элемента конструкцией ani - ani"],
        ["3", "сохранять одинаковую грамматическую форму обеих частей"],
        ["4", "согласовывать отрицание и ставить запятую перед вторым союзом"],
    ], [12 * mm, 158 * mm], font_size=7.2, header=False),
    Spacer(1, 3 * mm),
    box("<b>Формула:</b> <b>aj X, aj Y</b> = и X, и Y; <b>ani X, ani Y + отрицание</b> = ни X, ни Y.", PALE, PINK),
    PageBreak(),

    p("1. Aj - aj: включаем оба элемента", H1),
    p("<b>Aj - aj</b> значит \"и X, и Y\" или \"как X, так и Y\". Союз повторяется перед каждым равноправным элементом и подчёркивает, что важны оба."),
    styled_table([
        ["Что соединяем", "Словацкий пример", "Перевод"],
        ["людей", "Aj Anna, aj Peter pracujú doma.", "И Анна, и Петер работают дома."],
        ["предметы", "Kúpila som aj chlieb, aj mlieko.", "Я купила и хлеб, и молоко."],
        ["признаки", "Kurz je aj praktický, aj zaujímavý.", "Курс и практичный, и интересный."],
        ["действия", "Aj čítam knihy, aj počúvam podcasty.", "Я и читаю книги, и слушаю подкасты."],
        ["время", "Stretli sme sa aj v pondelok, aj v stredu.", "Мы встречались и в понедельник, и в среду."],
    ], [30 * mm, 75 * mm, 65 * mm], font_size=6.2),
    p("Сильнее, чем простое a", H2),
    styled_table([
        ["Нейтрально", "С акцентом на обоих"],
        ["Anna a Peter prišli.", "Aj Anna, aj Peter prišli."],
        ["Kúpim ovocie a zeleninu.", "Kúpim aj ovocie, aj zeleninu."],
        ["Hovoríme o práci a o škole.", "Hovoríme aj o práci, aj o škole."],
    ], [85 * mm, 85 * mm], font_size=6.5),
    box("<b>Смысл:</b> простое <b>a</b> перечисляет. <b>Aj - aj</b> отвечает на сомнение или специально подчёркивает полноту: не один элемент, а оба.", PALE, ROSE, SMALL),
    PageBreak(),

    p("2. Ani - ani: исключаем оба элемента", H1),
    p("<b>Ani - ani</b> значит \"ни X, ни Y\". В словацком отрицание согласуется: если в паре есть глагол, он обычно получает <b>ne-</b>. Одних союзов ani недостаточно."),
    styled_table([
        ["Что исключаем", "Словацкий пример", "Перевод"],
        ["людей", "Ani Anna, ani Peter dnes nepracujú.", "Ни Анна, ни Петер сегодня не работают."],
        ["предметы", "Nechcem ani čaj, ani kávu.", "Я не хочу ни чая, ни кофе."],
        ["состояния", "Nemám ani čas, ani energiu.", "У меня нет ни времени, ни сил."],
        ["места", "Neboli sme ani v múzeu, ani v galérii.", "Мы не были ни в музее, ни в галерее."],
        ["действия", "Ani mi nezavolal, ani mi nenapísal.", "Он мне ни позвонил, ни написал."],
    ], [30 * mm, 76 * mm, 64 * mm], font_size=6.15),
    p("Отрицание видно в сказуемом", H2),
    styled_table([
        ["Неправильно", "Правильно", "Почему"],
        ["*Ani Peter, ani Jana prišli.", "Ani Peter, ani Jana neprišli.", "Нужно отрицательное сказуемое."],
        ["*Mám ani čas, ani peniaze.", "Nemám ani čas, ani peniaze.", "Отрицается celý výrok."],
        ["*Ani prší, ani sneží.", "Ani neprší, ani nesneží.", "Отрицание повторяется с каждым глаголом."],
    ], [50 * mm, 65 * mm, 55 * mm], font_size=6.05),
    box("<b>Сравните:</b> <b>Aj varím, aj pečiem.</b> - Я и готовлю, и пеку. <b>Ani nevarím, ani nepečiem.</b> - Я ни готовлю, ни пеку.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    PageBreak(),

    p("3. Симметрия, падеж и согласование", H1),
    p("Обе части пары должны выполнять одну функцию и иметь параллельную форму. Если предлог нужен обоим элементам, безопаснее повторить его после каждого союза."),
    styled_table([
        ["Функция", "Симметричная модель", "Форма"],
        ["кому?", "Pomáham aj bratovi, aj sestre.", "оба элемента в Datív"],
        ["с кем?", "Hovorím aj s kolegom, aj s kolegyňou.", "дважды s + Inštrumentál"],
        ["о чём?", "Čítam aj o meste, aj o jeho histórii.", "дважды o + Lokál"],
        ["куда?", "Ideme aj do banky, aj do obchodu.", "дважды do + Genitív"],
        ["на что?", "Nemám čas ani na šport, ani na oddych.", "дважды na + Akuzatív"],
    ], [25 * mm, 87 * mm, 58 * mm], font_size=6.2),
    p("Два подлежащих - множественное число", H2),
    p("Когда пара называет двух деятелей перед сказуемым, используйте множественное число: <b>Aj mama, aj otec prišli.</b> / <b>Ani mama, ani otec neprišli.</b> Это надёжная модель для уровня A2."),
    p("Запятая перед второй частью", H2),
    styled_table([
        ["Схема", "Пример"],
        ["aj X, aj Y", "Pozná aj Bratislavu, aj Košice."],
        ["ani X, ani Y", "Nepozná ani Bratislavu, ani Košice."],
        ["aj X, aj Y, aj Z", "Kúpil aj chlieb, aj syr, aj ovocie."],
    ], [45 * mm, 125 * mm], font_size=6.45),
    box("<b>Не ставьте запятую после первого союза:</b> правильно <b>Aj Jana, aj Peter...</b>, а не *<b>Aj, Jana...</b>. Запятая стоит перед второй и каждой следующей повторённой частью.", PALE, PINK, SMALL),
    PageBreak(),

    p("4. Используем пары в связной речи", H1),
    p("Парный союз полезен, когда собеседник предполагает только один вариант или когда нужно ясно сообщить, что подходят оба либо ни один."),
    p("Мини-диалог: выбираем курс", H2),
    box("<b>Eva:</b> Chceš kurz slovenčiny alebo angličtiny?<br/><b>Martin:</b> Zaujímajú ma aj slovenčina, aj angličtina.<br/><b>Eva:</b> Máš čas aj v utorok, aj vo štvrtok?<br/><b>Martin:</b> Nie. Nemôžem ani v utorok, ani vo štvrtok.<br/><b>Eva:</b> A čo pondelok a streda?<br/><b>Martin:</b> To mi vyhovuje. Aj pondelok, aj streda sú voľné.<br/><b>Eva:</b> Výborne. Kurz nie je ani drahý, ani náročný.", PALE, ROSE, SMALL),
    p("Перевод", H2),
    p("Ты хочешь курс словацкого или английского? Меня интересуют и словацкий, и английский. У тебя есть время и во вторник, и в четверг? Нет, я не могу ни во вторник, ни в четверг. А понедельник и среда? Это мне подходит. И понедельник, и среда свободны. Отлично. Курс и не дорогой, и не сложный.", SMALL),
    p("Модель короткого сообщения", H2),
    box("<b>Na výlet môžu ísť aj dospelí, aj deti. Navštívime aj hrad, aj múzeum. Netreba si brať ani jedlo, ani vodu, pretože všetko dostaneme na mieste. Výlet nebude ani dlhý, ani náročný.</b><br/>На экскурсию могут поехать и взрослые, и дети. Мы посетим и замок, и музей. Не нужно брать ни еду, ни воду, потому что всё получим на месте. Экскурсия не будет ни долгой, ни сложной.", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    p("Короткая стратегия", H2),
    styled_table([
        ["Хотите сказать...", "Выберите"],
        ["оба варианта верны", "aj X, aj Y"],
        ["оба варианта исключены", "ani X, ani Y + отрицательное сказуемое"],
        ["элементы равноправны", "одинаковая функция, падеж и порядок"],
    ], [68 * mm, 102 * mm], font_size=6.4),
    PageBreak(),

    p("5. Частые ошибки и упражнения", H1),
    box("<b>Частые ошибки:</b> пропускают запятую перед вторым союзом; забывают <b>ne-</b> при ani - ani; соединяют разные функции; ставят сказуемое в единственном числе после двух подлежащих.", CREAM, colors.HexColor("#E7C76C"), TINY),
    p("Упражнение 1. Выберите aj - aj или ani - ani", H2),
    p("1) ___ mama, ___ otec prišli. 2) Nemám ___ čas, ___ peniaze. 3) Kurz je ___ lacný, ___ praktický. 4) Dnes ___ neprší, ___ nesneží.", TINY),
    p("Упражнение 2. Добавьте отрицание", H2),
    p("Исправьте глагол: 1) Ani Jana, ani Peter pracujú. 2) Mám ani chuť, ani čas. 3) Ani telefonoval, ani písal. 4) Boli sme ani v centre, ani na stanici.", TINY),
    p("Упражнение 3. Поставьте запятые", H2),
    p("1) Aj byt aj záhrada sú veľké. 2) Nekúpil ani chlieb ani mlieko. 3) Navštívime aj hrad aj múzeum aj park.", TINY),
    p("Упражнение 4. Сделайте структуру симметричной", H2),
    p("1) Hovorím aj s Petrom, aj Janu. 2) Myslím aj na prácu, aj o dovolenke. 3) Ideme ani do kina, ani koncert. Выберите подходящий падеж и при необходимости исправьте отрицание.", TINY),
    p("Упражнение 5. Переведите", H2),
    p("1) И Анна, и Петер говорят по-словацки. 2) Я не хочу ни чай, ни кофе. 3) Мы были и в музее, и в галерее. 4) Ни автобус, ни поезд сегодня не ходят.", TINY),
    p("Упражнение 6. Два варианта", H2),
    p("Напишите 5-7 предложений о поездке, курсе или встрече. Дважды используйте <b>aj - aj</b>, дважды <b>ani - ani</b> и хотя бы одну пару с повторённым предлогом.", TINY),
    PageBreak(),

    p("6. Ответы и проверка мастерства", H1),
    p("Ответы", H2),
    p("<b>1.</b> 1) Aj mama, aj otec prišli. 2) Nemám ani čas, ani peniaze. 3) Kurz je aj lacný, aj praktický. 4) Dnes ani neprší, ani nesneží.", TINY),
    p("<b>2.</b> 1) Ani Jana, ani Peter nepracujú. 2) Nemám ani chuť, ani čas. 3) Ani netelefonoval, ani nepísal. 4) Neboli sme ani v centre, ani na stanici.", TINY),
    p("<b>3.</b> 1) Aj byt, aj záhrada sú veľké. 2) Nekúpil ani chlieb, ani mlieko. 3) Navštívime aj hrad, aj múzeum, aj park.", TINY),
    p("<b>4.</b> 1) Hovorím aj s Petrom, aj s Janou. 2) Myslím aj na prácu, aj na dovolenku. 3) Nejdeme ani do kina, ani na koncert. Возможны другие естественные симметричные варианты.", TINY),
    p("<b>5.</b> 1) Aj Anna, aj Peter hovoria po slovensky. 2) Nechcem ani čaj, ani kávu. 3) Boli sme aj v múzeu, aj v galérii. 4) Ani autobus, ani vlak dnes nechodia.", TINY),
    p("<b>6. Модель:</b> Na výlet pôjdu aj kolegovia, aj priatelia. Navštívime aj staré mesto, aj hrad. Nemusíme myslieť ani na lístky, ani na dopravu, pretože všetko je rezervované. Výlet nebude ani drahý, ani náročný. Teším sa aj na program, aj na spoločný večer. Возможны другие естественные варианты.", TINY),
    p("Итог в четырёх пунктах", H2),
    styled_table([
        ["OK", "Aj X, aj Y подчёркивает, что верны оба элемента."],
        ["OK", "Ani X, ani Y исключает оба и требует отрицания."],
        ["OK", "Обе части имеют одинаковую функцию и грамматическую форму."],
        ["OK", "Ставлю запятую перед вторым и каждым следующим союзом."],
    ], [12 * mm, 158 * mm], font_size=6.45, header=False),
    Spacer(1, 2 * mm),
    box("<b>Финальная проверка:</b> без таблицы скажите: \"И Анна, и Петер придут\"; \"Я не был ни в банке, ни в магазине\"; \"Курс и полезный, и интересный\".", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    p("Следующий шаг", H2),
    p("В теме 5.3 вы перейдёте от сочинения равноправных элементов к передаче сообщения с союзом <b>že</b>.", SMALL),
]

doc.build(story)
print(OUTPUT)
