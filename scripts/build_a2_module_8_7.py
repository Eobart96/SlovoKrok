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
OUTPUT = ROOT / "output/pdf/A2/Module_08/Slovak_A2_Tema_8_7_Itog_A2_moy_opyt_plany_i_samostoyatelnost.pdf"
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
BODY = ParagraphStyle("Body", fontName="Arial", fontSize=8.45, leading=11.0, textColor=INK, spaceAfter=2.4 * mm)
SMALL = ParagraphStyle("Small", parent=BODY, fontSize=7.25, leading=8.9, spaceAfter=1.15 * mm)
TINY = ParagraphStyle("Tiny", parent=BODY, fontSize=6.35, leading=7.55, spaceAfter=0.65 * mm)
TITLE = ParagraphStyle("Title", fontName="Arial-Bold", fontSize=18.1, leading=21.3, textColor=colors.white, alignment=TA_LEFT, spaceAfter=4.5 * mm)
SUBTITLE = ParagraphStyle("Subtitle", fontName="Arial", fontSize=10.8, leading=14.0, textColor=colors.HexColor("#FFD8EB"), spaceAfter=4 * mm)
H1 = ParagraphStyle("H1", fontName="Arial-Bold", fontSize=15.0, leading=17.8, textColor=PLUM, spaceBefore=0.8 * mm, spaceAfter=2.7 * mm)
H2 = ParagraphStyle("H2", fontName="Arial-Bold", fontSize=10.3, leading=12.6, textColor=PINK, spaceBefore=0.8 * mm, spaceAfter=1.2 * mm)
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
            f"cell_{row_index}_{size}_{len(data)}", parent=SMALL, fontSize=size, leading=size + 1.6,
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
        canvas.drawString(20 * mm, height - 12 * mm, "A2 8.7  |  Итог A2: мой опыт, планы и самостоятельность")
    canvas.setFont("Arial", 8)
    canvas.setFillColor(MUTED)
    canvas.drawString(20 * mm, 9 * mm, "SlovoKrok | итоговый учебный модуль")
    canvas.drawRightString(width - 20 * mm, 9 * mm, f"стр. {page_number} / 8")
    canvas.restoreState()


doc = BaseDocTemplate(
    str(OUTPUT), pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=20 * mm, bottomMargin=18 * mm,
    title="Slovak A2 - Тема 8.7 - Итог A2: мой опыт, планы и самостоятельность", author="SlovoKrok",
)
doc.addPageTemplates([PageTemplate(
    id="series", frames=[Frame(20 * mm, 18 * mm, 170 * mm, 257 * mm, id="main", leftPadding=0, rightPadding=0)], onPage=draw_page,
)])


story = [
    p("МОДУЛЬ 8  •  ФИНАЛЬНАЯ ПРОВЕРКА A2", KICK),
    p("Итог A2:<br/>мой опыт, планы и самостоятельность", TITLE),
    p("Rozumiem, hovorím, píšem, reagujem a odovzdávam informácie", SUBTITLE),
    Spacer(1, 38 * mm),
    p("Это самостоятельная итоговая работа SlovoKrok, а не официальный языковой экзамен. Все задания связаны с поездкой на практический языковой уикенд, но каждая часть оценивается отдельно."),
    p("Четыре независимые части", H2),
    table([
        ["Часть", "Задания", "Что проверяем", "Баллы"],
        ["1. Рецепция", "1-2", "чтение и короткое аудирование", "12"],
        ["2. Продукция", "3-4", "устный рассказ и письмо", "14"],
        ["3. Взаимодействие", "5", "уточнение и договорённость", "7"],
        ["4. Медиация", "6", "передача важных фактов", "7"],
    ], [33 * mm, 26 * mm, 89 * mm, 22 * mm], 5.7),
    p("Правила", H2),
    box("Работайте без ответов на страницах 7-8. На задания 1-2 дайте краткие ответы. Устную часть запишите на диктофон. Письмо проверьте только после завершения. В открытых заданиях возможны разные естественные ответы."),
    Spacer(1, 2 * mm),
    box("<b>Ориентир:</b> 32-40 баллов - уверенное выполнение учебной проверки; 24-31 - уровень развивается; меньше 24 - повторите слабые части и пройдите работу ещё раз.", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    PageBreak(),

    p("Часть 1. Рецепция", H1),
    p("Задание 1. Чтение", H2),
    p("Прочитайте объявление один раз для общего смысла, затем второй раз для деталей. Ответьте по-русски или по-словацки. 6 баллов."),
    box("<b>VÍKENDOVÝ PROGRAM SLOVENČINA V PRAXI</b><br/><br/>Pozývame vás na jazykový víkend v Banskej Bystrici od 18. do 20. októbra. V piatok sa stretneme o 17.30 pri informačnom centre na železničnej stanici. Ubytovanie je zabezpečené v študentskom domove neďaleko centra.<br/><br/>V sobotu dopoludnia bude konverzačný workshop. Popoludní účastníci splnia v malých skupinách praktickú úlohu v meste. V nedeľu predstavia krátky projekt a program sa skončí o 14.00.<br/><br/>Cena 75 eur zahŕňa dve noci, raňajky a celý program. Nezahŕňa cestu ani večeru. Účasť potvrďte do 10. októbra. Vopred nám oznámte aj potravinové obmedzenia.", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    p("Вопросы", H2),
    table([
        ["1", "В каком городе и в какие даты проходит программа?"],
        ["2", "Где и когда встречаются участники в пятницу?"],
        ["3", "Какие три вещи входят в стоимость?"],
        ["4", "Какие две вещи не входят в стоимость?"],
        ["5", "Что участники делают в субботу после обеда?"],
        ["6", "Что нужно сообщить организаторам заранее?"],
    ], [11 * mm, 159 * mm], 6.1, False),
    p("Критерий", H2),
    box("1 балл за каждый точный ответ. Грамматические ошибки не снижают балл, если смысл понятен и факт взят из текста.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    PageBreak(),

    p("Часть 1. Рецепция", H1),
    p("Задание 2. Короткое аудирование", H2),
    p("Попросите человека или голосовой инструмент прочитать скрипт со страницы 7 два раза, не показывая вам текст. Первый раз слушайте общий смысл, второй раз записывайте детали. 6 баллов."),
    box("Вы уже прочитали объявление. Теперь организатор оставляет голосовое сообщение с изменениями. Не открывайте страницу 7 до завершения задания.", PALE, ROSE, SMALL),
    p("Заполните карточку", H2),
    table([
        ["Вопрос", "Ваш ответ"],
        ["1. Почему изменили место встречи?", ""],
        ["2. Где теперь встречаются участники?", ""],
        ["3. Во сколько состоится встреча?", ""],
        ["4. Как узнать организатора Яну?", ""],
        ["5. Что нужно принести?", ""],
        ["6. Что делать при опоздании?", ""],
    ], [84 * mm, 86 * mm], 6.0),
    p("После прослушивания", H2),
    table([
        ["Главное изменение", "______________________________"],
        ["Действие участника", "______________________________"],
        ["Контакт при проблеме", "______________________________"],
    ], [55 * mm, 115 * mm], 6.1, False),
    p("Критерий", H2),
    box("1 балл за каждый верный факт. Допустимы синонимы и краткая запись. Не вычитайте балл за орфографию, если информация однозначна.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    PageBreak(),

    p("Часть 2. Устная и письменная продукция", H1),
    p("Задание 3. Устный рассказ", H2),
    p("Говорите 1,5-2 минуты без чтения готового текста. Можно подготовить пять ключевых слов. 7 баллов."),
    table([
        ["Обязательно скажите", "Языковая опора"],
        ["какой опыт у вас уже был", "Zúčastnil som sa... - Я участвовал..."],
        ["что вы умеете сейчас", "Teraz dokážem... - Сейчас я умею..."],
        ["что пока трудно", "Najťažšie je pre mňa... - Самое трудное для меня..."],
        ["что будете делать на уикенде", "Počas víkendu budem... - На выходных я буду..."],
        ["какова цель на три месяца", "Do troch mesiacov chcem... - За три месяца я хочу..."],
        ["что сделаете при трудности", "Ak niečomu nerozumiem... - Если я чего-то не понимаю..."],
    ], [78 * mm, 92 * mm], 5.3),
    p("Задание 4. Письмо организатору", H2),
    p("Напишите 80-100 слов. 7 баллов. В письме:"),
    table([
        ["1", "подтвердите участие"], ["2", "сообщите время прибытия"],
        ["3", "уточните размещение"], ["4", "назовите пищевое ограничение или сообщите, что его нет"],
        ["5", "задайте один практический вопрос"], ["6", "закончите письмо вежливо"],
    ], [11 * mm, 74 * mm, 11 * mm, 74 * mm], 5.3, False),
    p("Полезные рамки", H2),
    table([
        ["Rád / Rada by som potvrdil / potvrdila účasť.", "Я хотел(а) бы подтвердить участие."],
        ["Prídem približne o...", "Я приеду примерно в..."],
        ["Chcel / Chcela by som sa opýtať, či...", "Я хотел(а) бы спросить, ..."],
        ["Ďakujem za informáciu a teším sa na program.", "Спасибо за информацию, жду программу."],
    ], [96 * mm, 74 * mm], 5.0, False),
    PageBreak(),

    p("Часть 3. Взаимодействие", H1),
    p("Задание 5. Решаем проблему по телефону", H2),
    p("Ваш поезд задерживается. Вы приедете в 18.20, после общей встречи. Разыграйте разговор с организатором. Если работаете один, прочитайте реплики организатора вслух с паузой и отвечайте без подготовки. 7 баллов."),
    table([
        ["Ход разговора", "Карточка организатора"],
        ["1. Поздоровайтесь, представьтесь и назовите причину звонка.", "Dobrý deň, tu je Jana z programu."],
        ["2. Объясните задержку и назовите новое время прибытия.", "Rozumiem. Spoločné stretnutie sa skončí o 18.15."],
        ["3. Уточните, куда идти после 18.15.", "Choďte priamo do študentského domova."],
        ["4. Спросите, сохранено ли место в комнате.", "Áno, izbu máte rezervovanú."],
        ["5. Подтвердите решение и завершите разговор.", "Dobre, budeme vás čakať na recepcii."],
    ], [90 * mm, 80 * mm], 5.25),
    p("Фразы для управления разговором", H2),
    table([
        ["Volám kvôli oneskoreniu vlaku.", "Я звоню из-за задержки поезда."],
        ["Prídem asi o dvadsať minút neskôr.", "Я приеду примерно на двадцать минут позже."],
        ["Rozumiem správne, že mám ísť priamo na internát?", "Я правильно понимаю, что нужно идти прямо в общежитие?"],
        ["Mohli by ste mi zopakovať adresu?", "Не могли бы вы повторить адрес?"],
        ["Dohodnime sa teda, že...", "Давайте тогда договоримся, что..."],
        ["Ďakujem za pomoc, dovidenia.", "Спасибо за помощь, до свидания."],
    ], [93 * mm, 77 * mm], 4.9, False),
    p("Оценивание", H2),
    table([
        ["решение задачи", "3"], ["реакция на реплики", "2"],
        ["понятность и вежливость", "1"], ["достаточный язык A2", "1"],
    ], [145 * mm, 25 * mm], 5.7, False),
    box("Не требуется идеальная грамматика. Важно объяснить проблему, получить нужную информацию и ясно подтвердить решение.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    PageBreak(),

    p("Часть 4. Медиация", H1),
    p("Задание 6. Передаём изменения другу", H2),
    p("Ваш русскоязычный друг едет вместе с вами, но не понимает сообщение организатора. Прочитайте его и передайте только важные действия и сроки. 7 баллов."),
    box("Ahojte, účastníci! Pre silný dážď sa sobotná mestská úloha nezačne o 9.30 na námestí, ale o 10.30 v mestskej knižnici. Prineste si zápisník a preukaz účastníka. Obed bude o 13.00 v reštaurácii vedľa knižnice. Kto má potravinovú alergiu, nech to oznámi Jane najneskôr v piatok do 12.00. Ďakujeme za pochopenie.", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    p("Выполните два шага", H2),
    table([
        ["A", "По-русски передайте другу 5 важных фактов в 4-5 предложениях."],
        ["B", "По-словацки ответьте Яне в 2-3 предложениях: подтвердите, что поняли изменение, и сообщите об аллергии или её отсутствии."],
    ], [13 * mm, 157 * mm], 5.6, False),
    p("Фразы для точной передачи", H2),
    table([
        ["V správe sa píše, že...", "В сообщении написано, что..."],
        ["Pôvodný čas sa zmenil.", "Первоначальное время изменилось."],
        ["Namiesto námestia pôjdeme do knižnice.", "Вместо площади мы пойдём в библиотеку."],
        ["Treba si priniesť...", "Нужно принести..."],
        ["Najneskôr do piatku treba oznámiť...", "Не позднее пятницы нужно сообщить..."],
        ["Rozumiem zmene a potvrdzujem účasť.", "Я понял(а) изменение и подтверждаю участие."],
    ], [95 * mm, 75 * mm], 4.9, False),
    p("Оценивание", H2),
    table([
        ["5 точных фактов без домыслов", "3"], ["понятный русский пересказ", "1"],
        ["словацкое подтверждение", "2"], ["уместная форма и срок", "1"],
    ], [145 * mm, 25 * mm], 5.7, False),
    box("Медиация оценивает передачу смысла, а не дословный перевод. Не добавляйте советов и фактов, которых нет в сообщении.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    PageBreak(),

    p("Ответы к рецепции", H1),
    p("Задание 1. Чтение", H2),
    table([
        ["1", "Banská Bystrica, od 18. do 20. októbra."],
        ["2", "V piatok o 17.30 pri informačnom centre na železničnej stanici."],
        ["3", "Dve noci, raňajky a celý program."],
        ["4", "Cesta a večera."],
        ["5", "Praktickú úlohu v meste v malých skupinách."],
        ["6", "Účasť do 10. októbra a potravinové obmedzenia."],
    ], [11 * mm, 159 * mm], 5.65, False),
    p("Задание 2. Скрипт аудирования", H2),
    box("Dobrý deň, tu je Jana z programu Slovenčina v praxi. Volám vám kvôli zmene piatkového stretnutia. Pre opravu železničnej stanice sa nestretneme pri informačnom centre. Prosím, príďte o 18.00 na autobusovú stanicu k nástupišťu číslo šesť. Budem mať zelenú bundu a tabuľku s názvom programu. Prineste si občiansky preukaz alebo pas. Ak budete meškať, zavolajte mi na číslo 0911 222 333. Tešíme sa na vás.", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    p("Ключ к аудированию", H2),
    table([
        ["1", "Pre opravu železničnej stanice."],
        ["2", "Na autobusovej stanici pri nástupišti číslo šesť."],
        ["3", "O 18.00."],
        ["4", "Bude mať zelenú bundu a tabuľku s názvom programu."],
        ["5", "Občiansky preukaz alebo pas."],
        ["6", "Zavolať Jane na číslo 0911 222 333."],
    ], [11 * mm, 159 * mm], 5.6, False),
    box("Если вы увидели скрипт до выполнения, не выставляйте балл за аудирование. Попросите прочитать другой раз или повторите эту часть позже.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    PageBreak(),

    p("Модели и итоговая оценка", H1),
    p("Модель устного ответа", H2),
    box("Slovenčinu sa učím už viac ako rok. Minulé leto som ju prvýkrát použil počas cesty do Bratislavy. Teraz dokážem nakúpiť, opýtať sa na cestu a hovoriť o svojej práci. Najťažšie je pre mňa porozumieť rýchlej reči. Počas víkendu budem veľa počúvať a rozprávať sa s ostatnými účastníkmi. Ak niečomu nerozumiem, požiadam o zopakovanie. Do troch mesiacov chcem hovoriť istejšie a napísať krátky text bez prekladača.", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    p("Модель письма", H2),
    box("Dobrý deň, pani organizátorka,<br/><br/>rada by som potvrdila svoju účasť na programe Slovenčina v praxi. Do Banskej Bystrice prídem v piatok vlakom približne o 17.10. Chcela by som sa opýtať, či dostaneme presnú adresu študentského domova ešte pred cestou. Nemám žiadne potravinové alergie, ale nejem mäso. Prosím, potvrďte mi, či je možné pripraviť vegetariánske raňajky. Tiež by som chcela vedieť, či je v izbe posteľná bielizeň a uterák. Pas si prinesiem.<br/><br/>Ďakujem za informácie a teším sa na program.<br/>S pozdravom<br/>Anna", PALE, ROSE, TINY),
    p("Модель взаимодействия", H2),
    box("Dobrý deň, tu je Alex Petrov. Volám kvôli oneskoreniu vlaku. Podľa novej informácie prídem až o 18.20. Rozumiem správne, že po skončení stretnutia mám ísť priamo do študentského domova? Je moja izba stále rezervovaná? Dobre, dohodnime sa teda, že prídem na recepciu a tam na mňa počkáte. Ďakujem za pomoc, dovidenia.", PALE, ROSE, TINY),
    p("Модель медиации", H2),
    box("В субботу встречаемся не в 9:30 на площади, а в 10:30 в городской библиотеке. Нужно взять блокнот и карточку участника. Обед будет в 13:00 в ресторане рядом с библиотекой. Об аллергии надо сообщить Яне не позднее пятницы до 12:00.<br/><br/><i>Dobrý deň, Jana. Rozumiem zmene a potvrdzujem, že prídem do knižnice o 10.30. Nemám žiadne potravinové alergie. Ďakujem.</i>", PALE, ROSE, TINY),
    p("Итог", H2),
    table([
        ["Рецепция", "__/12"], ["Продукция", "__/14"],
        ["Взаимодействие", "__/7"], ["Медиация", "__/7"],
        ["Всего", "__/40"],
    ], [140 * mm, 30 * mm], 5.7, False),
    box("Финальная проверка: вы поняли два источника, связно рассказали об опыте и планах, написали практическое письмо, решили проблему в разговоре и передали информацию без домыслов. Это и есть цель 8.7.", GREEN, colors.HexColor("#A8D5B3"), SMALL),
]

doc.build(story)
print(OUTPUT)
