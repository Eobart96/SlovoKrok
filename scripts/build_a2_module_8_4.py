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
OUTPUT = ROOT / "output/pdf/A2/Module_08/Slovak_A2_Tema_8_4_Apteka_travma_i_pervaya_pomoshch.pdf"
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
TINY = ParagraphStyle("Tiny", parent=BODY, fontSize=6.45, leading=7.7, spaceAfter=0.7 * mm)
TITLE = ParagraphStyle("Title", fontName="Arial-Bold", fontSize=19.5, leading=23.2, textColor=colors.white, alignment=TA_LEFT, spaceAfter=4.5 * mm)
SUBTITLE = ParagraphStyle("Subtitle", fontName="Arial", fontSize=11.2, leading=14.5, textColor=colors.HexColor("#FFD8EB"), spaceAfter=4 * mm)
H1 = ParagraphStyle("H1", fontName="Arial-Bold", fontSize=15.2, leading=18, textColor=PLUM, spaceBefore=0.8 * mm, spaceAfter=2.8 * mm)
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
        canvas.drawString(20 * mm, height - 12 * mm, "A2 8.4  |  Аптека, травма и первая помощь")
    canvas.setFont("Arial", 8)
    canvas.setFillColor(MUTED)
    canvas.drawString(20 * mm, 9 * mm, "SlovoKrok | личный учебный модуль")
    canvas.drawRightString(width - 20 * mm, 9 * mm, f"стр. {page_number} / 7")
    canvas.restoreState()


doc = BaseDocTemplate(
    str(OUTPUT), pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=20 * mm, bottomMargin=18 * mm,
    title="Slovak A2 - Тема 8.4 - Аптека, травма и первая помощь", author="SlovoKrok",
)
doc.addPageTemplates([PageTemplate(
    id="series", frames=[Frame(20 * mm, 18 * mm, 170 * mm, 257 * mm, id="main", leftPadding=0, rightPadding=0)], onPage=draw_page,
)])


story = [
    p("МОДУЛЬ 8  •  ОТНОШЕНИЯ, ЗДОРОВЬЕ И ИТОГ A2", KICK),
    p("Аптека, травма и первая помощь", TITLE),
    p("V lekárni a pri úraze: просим средство, понимаем дозировку и объясняем травму", SUBTITLE),
    Spacer(1, 43 * mm),
    p("На уровне A2 важно вежливо попросить нужное в аптеке, уточнить количество и правила применения, кратко объяснить простую травму и понять базовые указания при первой помощи."),
    p("После модуля вы сможете:", H2),
    table([
        ["1", "попросить средство через вежливое условное наклонение"],
        ["2", "понять количество, частоту и время применения"],
        ["3", "сказать, как вы получили травму: zraniť si / zlomiť si"],
        ["4", "описать состояние через пассивное причастие"],
        ["5", "попросить принести предмет и дать простую безопасную команду"],
    ], [12 * mm, 158 * mm], 6.75, False),
    Spacer(1, 3 * mm),
    box("<b>Сценарий:</b> просьба в аптеке -> вопрос о применении -> описание травмы -> короткая команда -> обращение за профессиональной помощью."),
    Spacer(1, 3 * mm),
    box("Это языковой модуль, а не медицинская инструкция. Реальные лекарства применяйте только по листку-вкладышу и указанию врача или фармацевта. При опасной ситуации звоните 155 или 112.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    PageBreak(),

    p("1. В аптеке: вежливая просьба", H1),
    p("Условное наклонение смягчает просьбу. Полезные формы: <b>mohol by som / mohla by som</b>, <b>prosil by som / prosila by som</b>, <b>potreboval by som / potrebovala by som</b>. Форма зависит от пола говорящего."),
    table([
        ["Фраза", "Перевод"],
        ["Mohli by ste mi odporučiť niečo na drobnú ranu?", "Не могли бы вы посоветовать что-нибудь для небольшой раны?"],
        ["Prosil by som si jedno balenie náplastí.", "Я бы хотел одну упаковку пластырей."],
        ["Prosila by som si dezinfekciu.", "Я бы хотела средство для дезинфекции."],
        ["Potrebovala by som elastický obväz.", "Мне нужен эластичный бинт."],
        ["Máte niečo na štípance?", "У вас есть что-нибудь от укусов насекомых?"],
        ["Je tento prípravok bez receptu?", "Это средство продаётся без рецепта?"],
    ], [94 * mm, 76 * mm], 5.2),
    p("Что можно попросить", H2),
    table([
        ["Слово", "Значение", "Количество"],
        ["náplasť", "пластырь", "dve náplasti"],
        ["obväz", "бинт, повязка", "tri obväzy"],
        ["dezinfekcia", "дезинфицирующее средство", "jedna fľaštička dezinfekcie"],
        ["masť", "мазь", "jedna tuba masti"],
        ["gél", "гель", "jedno balenie gélu"],
        ["lekárnička", "аптечка", "jedna lekárnička"],
    ], [35 * mm, 56 * mm, 79 * mm], 5.15),
    box("<b>На + A:</b> <i>niečo na ranu, na popáleninu, na bolesť</i>. Для точной просьбы добавьте количество: <i>Prosila by som si dve náplasti a jeden obväz.</i>", PALE, ROSE, SMALL),
    PageBreak(),

    p("2. Как понять дозировку и применение", H1),
    p("Не угадывайте способ применения. Уточняйте его у фармацевта и сверяйте с <i>príbalový leták</i>, то есть листком-вкладышем. В учебных примерах ниже нет назначения конкретного лекарства."),
    table([
        ["Вопрос", "Что уточняет"],
        ["Ako často to mám užívať?", "Как часто это принимать?"],
        ["Koľko tabliet mám užiť?", "Сколько таблеток принять?"],
        ["Mám to užívať pred jedlom alebo po jedle?", "До или после еды?"],
        ["Ako dlho to mám používať?", "Как долго это применять?"],
        ["Mám to zapiť vodou?", "Нужно запить водой?"],
        ["Môžem to používať spolu s iným liekom?", "Можно ли применять вместе с другим лекарством?"],
    ], [91 * mm, 79 * mm], 5.2),
    p("Читаем нейтральную учебную этикетку", H2),
    box("<b>Jazykový príklad, nie lekárske odporúčanie</b><br/>Použite jednu dávku dvakrát denne po jedle. Zapite vodou. Neprekračujte odporúčanú dávku. Uchovávajte mimo dosahu detí. Pred použitím si prečítajte príbalový leták.", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    table([
        ["Фрагмент", "Перевод"],
        ["jedna dávka", "одна доза"],
        ["dvakrát denne", "два раза в день"],
        ["po jedle / pred jedlom", "после еды / до еды"],
        ["zapiť vodou", "запить водой"],
        ["neprekračovať dávku", "не превышать дозу"],
        ["uchovávať mimo dosahu detí", "хранить вне доступа детей"],
    ], [76 * mm, 94 * mm], 5.3),
    p("Мини-диалог", H2),
    box("<b>Lekárnik:</b> Dobrý deň, nech sa páči.<br/><b>Zákazníčka:</b> Prosila by som si jedno balenie náplastí a elastický obväz.<br/><b>Lekárnik:</b> Nech sa páči. Potrebujete ešte niečo?<br/><b>Zákazníčka:</b> Áno. Ako často môžem použiť tento gél?<br/><b>Lekárnik:</b> Presný spôsob použitia nájdete v príbalovom letáku. Ak užívate iné lieky, poraďte sa s lekárom alebo lekárnikom.<br/><b>Zákazníčka:</b> Rozumiem, ďakujem.", PALE, ROSE, SMALL),
    PageBreak(),

    p("3. Объясняем травму: zraniť si / zlomiť si", H1),
    p("Возвратное <b>si</b> показывает, что человек повредил часть своего тела. В прошедшем времени форма меняется по роду: <i>zranil / zranila</i>, <i>zlomil / zlomila</i>. Часть тела обычно стоит в винительном падеже."),
    table([
        ["Что произошло", "Пример", "Перевод"],
        ["zraniť si", "Zranil som si zápästie.", "Я повредил запястье."],
        ["zlomiť si", "Zlomila si ruku.", "Она сломала руку."],
        ["porezať si", "Porezal som si prst.", "Я порезал палец."],
        ["popáliť si", "Popálila som si dlaň.", "Я обожгла ладонь."],
        ["vyvrtnúť si", "Vyvrtol si členok.", "Он подвернул лодыжку."],
        ["udrieť si", "Udrel som si koleno.", "Я ударился коленом."],
    ], [31 * mm, 70 * mm, 69 * mm], 5.15),
    p("Как уточнить обстоятельства", H2),
    table([
        ["Otázka", "Odpoveď"],
        ["Čo sa stalo?", "Spadol som z bicykla."],
        ["Kedy sa to stalo?", "Stalo sa to pred hodinou."],
        ["Kde vás to bolí?", "Bolí ma pravý členok."],
        ["Môžete s tým hýbať?", "Len trochu. Pri pohybe to bolí."],
        ["Krváca rana?", "Už nie, ale rana je hlboká."],
    ], [60 * mm, 110 * mm], 5.3),
    p("Пассивные причастия как признаки", H2),
    p("Формы на <b>-ný / -ná / -né</b> согласуются с предметом или частью тела: <i>prst je porezaný</i>, но <i>ruka je porezaná</i>."),
    table([
        ["Мужской род", "Женский род", "Средний род"],
        ["Prst je porezaný.", "Ruka je opuchnutá.", "Koleno je poranené."],
        ["Členok je vyvrtnutý.", "Koža je začervenaná.", "Miesto je zakryté."],
    ], [57 * mm, 57 * mm, 56 * mm], 5.2),
    box("Если перелом только предполагается, говорите осторожно: <i>Asi som si zlomil ruku</i> или <i>Myslím, že je ruka zlomená</i>. Диагноз подтверждает специалист.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    PageBreak(),

    p("4. Первая помощь и две конструкции с D + A", H1),
    p("В экстренной ситуации нужны короткие и ясные команды. Формы на <b>-te</b> обращены к одному незнакомому человеку или к нескольким людям."),
    table([
        ["Команда", "Перевод"],
        ["Zavolajte 155 alebo 112.", "Позвоните 155 или 112."],
        ["Prineste lekárničku, prosím.", "Принесите аптечку, пожалуйста."],
        ["Nehýbte sa.", "Не двигайтесь."],
        ["Pritlačte čistú látku na ranu.", "Прижмите чистую ткань к ране."],
        ["Počkajte na pomoc.", "Подождите помощи."],
        ["Povedzte, kde presne ste.", "Скажите, где именно вы находитесь."],
    ], [89 * mm, 81 * mm], 5.4),
    p("Priniesť + D + A: принести кому-то что-то", H2),
    table([
        ["Кому? D", "Что? A", "Полная фраза"],
        ["mi", "lekárničku", "Prineste mi lekárničku."],
        ["jej", "čistý obväz", "Priniesol som jej čistý obväz."],
        ["mu", "vodu", "Prineste mu vodu, prosím."],
    ], [37 * mm, 52 * mm, 81 * mm], 5.3),
    p("Zobrať + D + A: забрать у кого-то что-то", H2),
    p("С <i>zobrať</i> дательный часто обозначает человека, у которого что-то забрали. Не путайте это со значением «принести»."),
    table([
        ["Zobral som mu tašku.", "Я забрал у него сумку."],
        ["Neberte jej telefón.", "Не забирайте у неё телефон."],
        ["Záchranár mu zobral poškodenú topánku.", "Спасатель снял с него повреждённую обувь."],
    ], [88 * mm, 82 * mm], 5.1, False),
    p("Мини-диалог после травмы", H2),
    box("<b>A:</b> Čo sa stalo?<br/><b>B:</b> Spadla som na schodoch a zranila som si členok. Je opuchnutý a pri pohybe bolí.<br/><b>A:</b> Nehýbte sa. Zavolám pomoc. Peter, prineste jej lekárničku a čistý obväz.<br/><b>B:</b> Ďakujem. Prosím, povedzte záchranárom, že sa to stalo pred desiatimi minútami.", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    box("При сильном кровотечении, потере сознания, проблемах с дыханием или подозрении на серьёзную травму не ограничивайтесь языковым диалогом: вызывайте профессиональную помощь.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    PageBreak(),

    p("5. Частые ошибки и упражнения", H1),
    table([
        ["Ошибка", "Правильно", "Почему"],
        ["*Ja by chcem obväz.", "Prosil by som si obväz.", "условная просьба"],
        ["*jedna balenie", "jedno balenie", "balenie = средний род"],
        ["*Zranil som ruku.", "Zranil som si ruku.", "своя часть тела"],
        ["*Ruka je opuchnutý.", "Ruka je opuchnutá.", "согласование"],
        ["*Prineste ja lekárničku.", "Prineste mi lekárničku.", "получатель = D"],
    ], [50 * mm, 64 * mm, 56 * mm], 5.0),
    p("Упражнение 1. Выберите форму говорящего", H2),
    p("1) Мужчина: Prosil / Prosila by som si obväz. 2) Женщина: Potreboval / Potrebovala by som náplasti. 3) Мужчина: Mohol / Mohla by som dostať jedno balenie?", SMALL),
    p("Упражнение 2. Добавьте количество", H2),
    p("Соедините: 1) dve 2) jeden 3) jedna 4) jedno + a) balenie b) náplasti c) tuba masti d) obväz.", SMALL),
    p("Упражнение 3. Составьте вопрос о применении", H2),
    p("1) ako často / užívať 2) pred jedlom / po jedle 3) ako dlho / používať 4) zapiť / vodou.", SMALL),
    p("Упражнение 4. Поставьте глагол в прошедшее время", H2),
    p("1) Ja, muž: (zraniť si) zápästie. 2) Ja, žena: (popáliť si) dlaň. 3) On: (vyvrtnúť si) členok. 4) Ona: (porezať si) prst.", SMALL),
    p("Упражнение 5. Согласуйте причастие", H2),
    p("1) Ruka je (opuchnutý). 2) Prst je (porezaná). 3) Koleno je (poranený). 4) Koža je (začervenané).", SMALL),
    p("Упражнение 6. Переведите", H2),
    p("1) Принесите мне аптечку. 2) Я повредила лодыжку. 3) Как часто это применять? 4) Позвоните 112 и подождите помощи. 5) Она хотела бы одну упаковку пластырей.", SMALL),
    PageBreak(),

    p("6. Ответы и проверка мастерства", H1),
    p("Ответы", H2),
    table([
        ["№", "Ключ"],
        ["1", "1 Prosil; 2 Potrebovala; 3 Mohol."],
        ["2", "1-b dve náplasti; 2-d jeden obväz; 3-c jedna tuba masti; 4-a jedno balenie."],
        ["3", "1 Ako často to mám užívať? 2 Mám to užívať pred jedlom alebo po jedle? 3 Ako dlho to mám používať? 4 Mám to zapiť vodou?"],
        ["4", "1 Zranil som si zápästie. 2 Popálila som si dlaň. 3 Vyvrtol si členok. 4 Porezala si prst."],
        ["5", "1 opuchnutá; 2 porezaný; 3 poranené; 4 začervenaná."],
        ["6", "1 Prineste mi lekárničku. 2 Zranila som si členok. 3 Ako často to mám používať? 4 Zavolajte 112 a počkajte na pomoc. 5 Prosila by si jedno balenie náplastí."],
    ], [13 * mm, 157 * mm], 4.95),
    p("Модель связного ответа", H2),
    box("Včera som spadla z bicykla a zranila som si pravý členok. Je opuchnutý a pri pohybe dosť bolí. V lekárni by som si prosila elastický obväz a jedno balenie náplastí. Mohli by ste mi povedať, ako mám tento prípravok používať? Presný spôsob použitia si prečítam aj v príbalovom letáku. Ak sa stav zhorší, zavolám lekára.", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    p("Пять опор темы", H2),
    table([
        ["1", "Вежливая просьба: <i>Prosil / Prosila by som si...</i>"],
        ["2", "Количество: <i>jedno balenie, jedna tuba, dve náplasti</i>."],
        ["3", "Травма своей части тела: <i>Zranil som si členok</i>."],
        ["4", "Признак согласуется: <i>ruka je opuchnutá</i>."],
        ["5", "Получатель в D: <i>Prineste mi lekárničku</i>."],
    ], [11 * mm, 159 * mm], 5.35, False),
    p("Финальная проверка", H2),
    box("Без подсказки попросите два предмета в аптеке, уточните частоту и время применения, объясните одну травму в прошедшем времени, опишите повреждённую часть тела и дайте три ясные команды. Если получается связный диалог, цель 8.4 достигнута.", PALE, ROSE, SMALL),
]

doc.build(story)
print(OUTPUT)
