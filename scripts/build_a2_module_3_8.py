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
OUTPUT = ROOT / "output" / "pdf" / "A2" / "Module_03" / "Slovak_A2_Tema_3_8_Neopredelennye_otricatelnye_i_obobshchayushchie_mestoimeniya.pdf"
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
TITLE = ParagraphStyle("Title", fontName="Arial-Bold", fontSize=19.5, leading=23, textColor=colors.white, alignment=TA_LEFT, spaceAfter=5 * mm)
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
        canvas.drawString(20 * mm, height - 12 * mm, "A2 3.8  |  Неопределённые, отрицательные и обобщающие местоимения")
    canvas.setFont("Arial", 8)
    canvas.setFillColor(MUTED)
    canvas.drawString(20 * mm, 9 * mm, "SlovoKrok | личный учебный модуль")
    canvas.drawRightString(width - 20 * mm, 9 * mm, f"стр. {page} / 7")
    canvas.restoreState()


doc = BaseDocTemplate(
    str(OUTPUT), pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=20 * mm, bottomMargin=18 * mm,
    title="Slovak A2 - Тема 3.8 - Неопределённые, отрицательные и обобщающие местоимения", author="SlovoKrok",
)
frame = Frame(20 * mm, 18 * mm, 170 * mm, 257 * mm, id="main", leftPadding=0, rightPadding=0)
doc.addPageTemplates([PageTemplate(id="series", frames=[frame], onPage=draw_page)])

story = [
    p("МОДУЛЬ 3  •  ПРИЛАГАТЕЛЬНЫЕ, МЕСТОИМЕНИЯ И ЧИСЛИТЕЛЬНЫЕ", COVER_KICKER),
    p("Неопределённые, отрицательные<br/>и обобщающие местоимения", TITLE),
    p("Niekto, nikto, každý: от неизвестного к полному множеству", SUBTITLE),
    Spacer(1, 35 * mm),
    p("Эти слова помогают сказать, что человек или предмет неизвестен, отсутствует либо входит в полное множество: <b>niekto</b> - кто-то, <b>nikto</b> - никто, <b>každý</b> - каждый."),
    p("После модуля вы сможете:", H2),
    styled_table([
        ["1", "различать niekto/nikto, niečo/nič и niekde/nikde"],
        ["2", "согласовывать nejaký и žiadny с существительным"],
        ["3", "выбирать každý, všetci, všetky или všetko"],
        ["4", "строить словацкое отрицание: Nikto mi nič nepovedal"],
    ], [12 * mm, 158 * mm], font_size=7.25, header=False),
    Spacer(1, 3 * mm),
    box("<b>Главная карта:</b> <b>nie-</b> сообщает о неопределённости, <b>ni-</b> отрицает, а <b>každý / všetci / všetky / všetko</b> охватывают каждого или всё множество.", PALE, PINK),
    PageBreak(),

    p("1. Три смысловые группы", H1),
    p("Сначала выберите смысл: кто-то или что-то неизвестное; никто или ничего; каждый либо все. Затем подберите форму по роли в предложении."),
    styled_table([
        ["Значение", "Люди", "Предметы", "Место / признак"],
        ["неопределённость", "niekto - кто-то", "niečo - что-то", "niekde - где-то; nejaký - какой-то"],
        ["отсутствие", "nikto - никто", "nič - ничто", "nikde - нигде; žiadny - никакой"],
        ["полный охват", "každý - каждый; všetci - все", "všetko - всё", "všetky - все жен. и неодуш. мн. ч."],
    ], [32 * mm, 43 * mm, 39 * mm, 56 * mm], font_size=6.25),
    p("Базовые пары", H2),
    styled_table([
        ["Неопределённость", "Отрицание"],
        ["Niekto čaká pred domom. - Кто-то ждёт перед домом.", "Nikto nečaká pred domom. - Никто не ждёт перед домом."],
        ["Chcem niečo povedať. - Я хочу кое-что сказать.", "Nechcem nič povedať. - Я не хочу ничего говорить."],
        ["Býva niekde blízko. - Он живёт где-то рядом.", "Nikde tu nebýva. - Он нигде здесь не живёт."],
        ["Hľadám nejaký hotel. - Я ищу какой-нибудь отель.", "Nemáme žiadny voľný hotel. - У нас нет ни одного свободного отеля."],
    ], [85 * mm, 85 * mm], font_size=6.05),
    box("<b>Не путайте:</b> <b>Niekto neprišiel</b> значит «кто-то не пришёл», а <b>Nikto neprišiel</b> - «никто не пришёл».", CREAM, colors.HexColor("#E7C76C"), SMALL),
    PageBreak(),

    p("2. Niekto, niečo, nikto, nič в падежах", H1),
    p("Части <b>nie-</b> и <b>ni-</b> остаются перед падежной формой. После предлога слово не разделяется: <b>s niekým, od nikoho, o ničom</b>."),
    styled_table([
        ["Падеж", "кто-то / никто", "что-то / ничто"],
        ["N", "niekto / nikto", "niečo / nič"],
        ["G", "niekoho / nikoho", "niečoho / ničoho"],
        ["D", "niekomu / nikomu", "niečomu / ničomu"],
        ["A", "niekoho / nikoho", "niečo / nič"],
        ["L", "o niekom / o nikom", "o niečom / o ničom"],
        ["I", "s niekým / s nikým", "s niečím / s ničím"],
    ], [24 * mm, 73 * mm, 73 * mm], font_size=6.35),
    p("Живые модели", H2),
    styled_table([
        ["Форма", "Пример"],
        ["G", "Čakám správu od niekoho. - Я жду сообщение от кого-то."],
        ["G", "Nedostal som správu od nikoho. - Я ни от кого не получил сообщения."],
        ["D", "Musím niekomu zavolať. - Мне нужно кому-то позвонить."],
        ["D", "Nikomu to nepoviem. - Я никому этого не скажу."],
        ["L", "Rozprávame sa o niečom dôležitom. - Мы говорим о чём-то важном."],
        ["I", "Nešiel som tam s nikým. - Я ни с кем туда не ходил."],
    ], [28 * mm, 142 * mm], font_size=6.3),
    box("<b>Долгота важна:</b> правильно <b>s niekým, s niečím, s nikým, s ničím</b>.", PALE, ROSE, SMALL),
    PageBreak(),

    p("3. Nejaký и žiadny: согласование", H1),
    p("Оба слова ведут себя как прилагательные и согласуются с существительным. <b>Nejaký</b> указывает на неопределённый объект, <b>žiadny</b> отрицает наличие даже одного."),
    styled_table([
        ["Род / число", "nejaký", "žiadny"],
        ["мужской", "nejaký problém", "žiadny problém"],
        ["женский", "nejaká otázka", "žiadna otázka"],
        ["средний", "nejaké miesto", "žiadne miesto"],
        ["множественное", "nejakí ľudia / nejaké veci", "žiadni ľudia / žiadne veci"],
    ], [36 * mm, 67 * mm, 67 * mm], font_size=6.55),
    p("В предложении", H2),
    styled_table([
        ["SK", "RU"],
        ["Máš nejakú otázku?", "У тебя есть какой-нибудь вопрос?"],
        ["Nemám žiadnu otázku.", "У меня нет ни одного вопроса."],
        ["Potrebujeme nejaké riešenie.", "Нам нужно какое-нибудь решение."],
        ["Nenašli sme žiadne riešenie.", "Мы не нашли никакого решения."],
        ["Hovoril s nejakými ľuďmi.", "Он говорил с какими-то людьми."],
        ["Nehovoril so žiadnymi ľuďmi.", "Он не говорил ни с какими людьми."],
    ], [84 * mm, 86 * mm], font_size=6.35),
    box("<b>Žiadny требует отрицательного сказуемого:</b> <b>Nemám žiadny čas</b>, не *Mám žiadny čas. В нейтральной речи также встречается <b>nijaký</b>.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    PageBreak(),

    p("4. Každý, všetci, všetky, všetko", H1),
    p("<b>Každý</b> рассматривает участников по одному и обычно стоит в единственном числе. Формы <b>všetci / všetky</b> охватывают группу, а <b>všetko</b> означает «всё»."),
    styled_table([
        ["Форма", "Когда выбирать", "Пример"],
        ["každý / každá / každé", "каждый отдельный человек или предмет", "každý deň; každá rodina; každé ráno"],
        ["všetci", "все мужчины или смешанная группа людей", "Všetci študenti prišli."],
        ["všetky", "все женщины или неодушевлённые во мн. числе", "Všetky študentky prišli. Všetky knihy sú tu."],
        ["všetko", "всё как единое целое", "Všetko je pripravené."],
    ], [36 * mm, 61 * mm, 73 * mm], font_size=6.2),
    p("Смысловые контрасты", H2),
    styled_table([
        ["SK", "Точный смысл"],
        ["Každý dostal lístok.", "Каждый получил билет: акцент на каждом участнике."],
        ["Všetci dostali lístky.", "Все получили билеты: группа целиком."],
        ["Nie všetci prišli.", "Не все пришли: часть группы пришла."],
        ["Nikto neprišiel.", "Никто не пришёл: пришедших нет."],
        ["Všetky okná sú otvorené.", "Все окна открыты."],
        ["Všetko je otvorené.", "Всё открыто: обобщение без названия предметов."],
    ], [67 * mm, 103 * mm], font_size=6.3),
    box("<b>Подсказка:</b> один за другим -> <b>každý</b>; группа людей -> <b>všetci</b>; названные предметы или женщины -> <b>všetky</b>; всё вообще -> <b>všetko</b>.", PALE, PINK, SMALL),
    PageBreak(),

    p("5. Двойное отрицание и упражнения", H1),
    p("В стандартном словацком отрицательное местоимение поддерживается отрицательным глаголом. Несколько отрицательных слов не отменяют отрицание, а образуют одну отрицательную конструкцию."),
    box("<b>Nikto mi nič nepovedal.</b> - Никто мне ничего не сказал.<br/><b>Nikde som nikoho nevidel.</b> - Я нигде никого не видел.<br/><b>Nikomu som nikdy nič neposlal.</b> - Я никому никогда ничего не отправлял.", PALE, ROSE, TINY),
    box("<b>Частые ошибки:</b> *Nikto prišiel -> <b>Nikto neprišiel</b>; *Nič som kúpil -> <b>Nič som nekúpil</b>; *Nemám nejaké otázky в значении «никаких» -> <b>Nemám žiadne otázky</b>; *Všetci knihy -> <b>všetky knihy</b>.", CREAM, colors.HexColor("#E7C76C"), TINY),
    p("Упражнение 1. Выберите nie- или ni-", H2),
    p("1) ___kto zvoní. 2) ___kto neodpovedá. 3) Chcem ___čo jesť. 4) ___č som nejedol. 5) Býva ___kde blízko. 6) ___kde ho nevidím.", TINY),
    p("Упражнение 2. Поставьте в нужный падеж", H2),
    p("1) Hovorím s (niekto). 2) Nečakám na (nikto). 3) Premýšľam o (niečo). 4) Nepremýšľam o (nič). 5) Pomôžem (niekto).", TINY),
    p("Упражнение 3. Согласуйте nejaký или žiadny", H2),
    p("1) ___ otázka; 2) ___ miesto; 3) s ___ ľuďmi; 4) Nemám ___ čas; 5) Nenašli sme ___ riešenie.", TINY),
    p("Упражнение 4. Выберите každý, všetci, všetky или všetko", H2),
    p("1) ___ deň; 2) ___ študenti; 3) ___ knihy; 4) ___ je hotové; 5) ___ dieťa.", TINY),
    p("Упражнение 5. Исправьте отрицание", H2),
    p("1) Nikto čaká. 2) Nič som kúpil. 3) Nikde bývam. 4) Mám žiadne otázky. 5) Nikomu som niečo neposlal.", TINY),
    p("Упражнение 6. Мини-диалог", H2),
    p("Напишите 6 реплик о встрече. Используйте niekto, nikto, niečo, nič, каждый/все и одну фразу с двумя отрицательными словами.", TINY),
    PageBreak(),

    p("6. Ответы и проверка мастерства", H1),
    p("Ответы", H2),
    p("<b>1.</b> Niekto zvoní. Nikto neodpovedá. Chcem niečo jesť. Nič som nejedol. Býva niekde blízko. Nikde ho nevidím.", TINY),
    p("<b>2.</b> s niekým; na nikoho; o niečom; o ničom; niekomu.", TINY),
    p("<b>3.</b> nejaká otázka; nejaké miesto; s nejakými ľuďmi; Nemám žiadny čas; Nenašli sme žiadne riešenie. В первых трёх пунктах возможен žiadny при отрицательном контексте.", TINY),
    p("<b>4.</b> každý deň; všetci študenti; všetky knihy; všetko je hotové; každé dieťa.", TINY),
    p("<b>5.</b> Nikto nečaká. Nič som nekúpil. Nikde nebývam. Nemám žiadne otázky. Nikomu som nič neposlal.", TINY),
    p("<b>6. Модель:</b> A: Prišiel už niekto? B: Nie, ešte nikto neprišiel. A: Máme niečo na pitie? B: Nemáme nič studené. A: Prídu všetci kolegovia? B: Nie všetci, ale každý dostal pozvanie. Возможны другие естественные варианты.", TINY),
    p("Итог в четырёх пунктах", H2),
    styled_table([
        ["OK", "Различаю niekto/nikto, niečo/nič и niekde/nikde."],
        ["OK", "Склоняю niekoho, niekomu, s niekým и отрицательные пары."],
        ["OK", "Согласую nejaký/žiadny и выбираю každý/všetci/všetky/všetko."],
        ["OK", "Ставлю отрицательную форму глагола рядом с nikto, nič, nikde, žiadny."],
    ], [12 * mm, 158 * mm], font_size=6.55, header=False),
    Spacer(1, 2 * mm),
    box("<b>Финальная проверка:</b> без таблицы скажите «кто-то мне позвонил», «никто мне не позвонил», «я ничего никому не сказал», «не все пришли» и «все книги здесь».", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    p("Следующий шаг", H2),
    p("В теме 3.9 вы перейдёте к числительным, датам и выражению количества.", SMALL),
]

doc.build(story)
print(OUTPUT)
