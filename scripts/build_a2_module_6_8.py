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
OUTPUT = ROOT / "output/pdf/A2/Module_06/Slovak_A2_Tema_6_8_Odezhda_primerka_oplata_i_obmen.pdf"
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
BODY = ParagraphStyle("Body", fontName="Arial", fontSize=8.55, leading=11.2, textColor=INK, spaceAfter=2.5 * mm)
SMALL = ParagraphStyle("Small", parent=BODY, fontSize=7.35, leading=9.15, spaceAfter=1.35 * mm)
TINY = ParagraphStyle("Tiny", parent=BODY, fontSize=6.55, leading=7.95, spaceAfter=0.85 * mm)
TITLE = ParagraphStyle("Title", fontName="Arial-Bold", fontSize=20, leading=24, textColor=colors.white, alignment=TA_LEFT, spaceAfter=5 * mm)
SUBTITLE = ParagraphStyle("Subtitle", fontName="Arial", fontSize=11.4, leading=15, textColor=colors.HexColor("#FFD8EB"), spaceAfter=5 * mm)
H1 = ParagraphStyle("H1", fontName="Arial-Bold", fontSize=15.5, leading=18.5, textColor=PLUM, spaceBefore=1 * mm, spaceAfter=3 * mm)
H2 = ParagraphStyle("H2", fontName="Arial-Bold", fontSize=10.6, leading=13.1, textColor=PINK, spaceBefore=1 * mm, spaceAfter=1.35 * mm)
KICK = ParagraphStyle("Kicker", fontName="Arial-Bold", fontSize=10, leading=12, textColor=colors.HexColor("#FFD8EB"), spaceAfter=4 * mm)


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
        style = ParagraphStyle(
            f"cell_{row_index}_{size}_{len(data)}",
            parent=SMALL,
            fontSize=size,
            leading=size + 1.75,
            textColor=colors.white if header and row_index == 0 else INK,
            fontName="Arial-Bold" if header and row_index == 0 else "Arial",
            spaceAfter=0,
        )
        rows.append([p(str(value), style) for value in row])
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
        canvas.drawString(20 * mm, height - 12 * mm, "A2 6.8  |  Одежда, примерка, оплата и обмен")
    canvas.setFont("Arial", 8)
    canvas.setFillColor(MUTED)
    canvas.drawString(20 * mm, 9 * mm, "SlovoKrok | личный учебный модуль")
    canvas.drawRightString(width - 20 * mm, 9 * mm, f"стр. {page_number} / 7")
    canvas.restoreState()


doc = BaseDocTemplate(
    str(OUTPUT), pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm,
    topMargin=20 * mm, bottomMargin=18 * mm,
    title="Slovak A2 - Тема 6.8 - Одежда, примерка, оплата и обмен",
    author="SlovoKrok",
)
doc.addPageTemplates([
    PageTemplate(id="series", frames=[Frame(20 * mm, 18 * mm, 170 * mm, 257 * mm, id="main", leftPadding=0, rightPadding=0)], onPage=draw_page)
])


story = [
    p("МОДУЛЬ 6  •  ДОМ, ИНТЕРНЕТ И ПОКУПКИ", KICK),
    p("Одежда, примерка,<br/>оплата и обмен", TITLE),
    p("Oblečenie, skúšanie, platba a výmena: выбираем, примеряем и объясняем проблему", SUBTITLE),
    Spacer(1, 41 * mm),
    p("В магазине нужно назвать конкретный товар, сравнить размер или модель, уточнить способ оплаты и спокойно объяснить, почему вещь не подходит."),
    p("После модуля вы сможете:", H2),
    table([
        ["1", "выбрать одежду с правильным Akuzatív"],
        ["2", "попросить другой размер и сравнить модели"],
        ["3", "сказать, как вы хотите заплатить"],
        ["4", "вежливо попросить обмен и назвать причину"],
    ], [12 * mm, 158 * mm], 7.2, False),
    Spacer(1, 3 * mm),
    box("<b>Формула:</b> ищу конкретную вещь + примеряю и сравниваю + выбираю способ оплаты; при проблеме называю товар, причину и желаемое решение."),
    PageBreak(),

    p("1. Выбираем вещь: Akuzatív", H1),
    p("После <i>hľadať, chcieť, potrebovať, skúšať, kúpiť</i> предмет обычно стоит в Akuzatív. У прилагательного меняется прежде всего форма женского рода: <i>-á → -ú</i>."),
    table([
        ["Род / число", "Модель", "Пример"],
        ["мужской неодуш.", "čierny kabát", "Hľadám čierny kabát."],
        ["женский", "modrá bunda → modrú bundu", "Chcem modrú bundu."],
        ["средний", "biele tričko", "Potrebujem biele tričko."],
        ["множественное", "pohodlné topánky", "Skúšam pohodlné topánky."],
        ["множественное", "modré nohavice", "Kúpim si modré nohavice."],
    ], [39 * mm, 59 * mm, 72 * mm], 5.65),
    p("Полезные сочетания", H2),
    table([
        ["Вещь", "Сочетание", "Перевод"],
        ["košeľa", "bavlnenú košeľu", "хлопковую рубашку"],
        ["sveter", "teplý sveter", "тёплый свитер"],
        ["sukňa", "dlhú sukňu", "длинную юбку"],
        ["šaty", "elegantné šaty", "элегантное платье"],
        ["topánky", "čierne topánky", "чёрные туфли"],
        ["veľkosť", "veľkosť M", "размер M"],
    ], [35 * mm, 66 * mm, 69 * mm], 5.8),
    box("<b>Запомните:</b> <i>Chcem čierna bunda</i> неверно. После <i>chcem</i>: <i>Chcem čiernu bundu.</i>", CREAM, colors.HexColor("#E7C76C"), SMALL),
    PageBreak(),

    p("2. Примерка и сравнение", H1),
    p("Сначала опишите посадку, затем попросите конкретное изменение. Сравнительная степень помогает не повторять всю характеристику."),
    table([
        ["Исходная форма", "Сравнение", "Пример"],
        ["veľký", "väčší", "Potrebujem väčšiu veľkosť."],
        ["malý", "menší", "Máte menšiu bundu?"],
        ["dlhý", "dlhší", "Skúsim si dlhší kabát."],
        ["krátky", "kratší", "Chcem kratšie nohavice."],
        ["široký", "širší", "Tento strih je širší."],
        ["úzky", "užší", "Hľadám užšiu košeľu."],
        ["pohodlný", "pohodlnejší", "Tieto topánky sú pohodlnejšie."],
        ["lacný", "lacnejší", "Je tam aj lacnejší model?"],
    ], [38 * mm, 42 * mm, 90 * mm], 5.55),
    p("Как сидит одежда", H2),
    table([
        ["SK", "RU"],
        ["Sedí mi dobre.", "Мне хорошо подходит / сидит."],
        ["Je mi malá / veľká.", "Она мне мала / велика."],
        ["Tlačí ma v páse.", "Мне жмёт в поясе."],
        ["Rukávy sú príliš dlhé.", "Рукава слишком длинные."],
        ["Farba mi nepristane.", "Цвет мне не идёт."],
    ], [80 * mm, 90 * mm], 5.75),
    box("<b>В примерочной:</b> <i>Môžem si to vyskúšať? Kde sú skúšobné kabínky? Mohli by ste mi priniesť väčšiu veľkosť?</i>", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    PageBreak(),

    p("3. Оплата и вид глагола", H1),
    p("Способ оплаты часто выражается Instrumentál: <i>kartou, mobilom</i>. Для наличных обычно используется устойчивое <i>v hotovosti</i>."),
    table([
        ["Способ", "Фраза", "Перевод"],
        ["kartou", "Môžem zaplatiť kartou?", "Можно заплатить картой?"],
        ["mobilom", "Zaplatím mobilom.", "Я заплачу телефоном."],
        ["hodinkami", "Dá sa platiť hodinkami?", "Можно платить часами?"],
        ["v hotovosti", "Zaplatím v hotovosti.", "Я заплачу наличными."],
    ], [32 * mm, 75 * mm, 63 * mm], 5.75),
    p("Процесс или завершённый результат", H2),
    table([
        ["Процесс / повтор", "Результат", "Пример"],
        ["skúšať", "vyskúšať", "Chcem si vyskúšať túto bundu."],
        ["platiť", "zaplatiť", "Môžem zaplatiť kartou?"],
        ["meniť", "vymeniť", "Potrebujem vymeniť veľkosť."],
        ["vracať", "vrátiť", "Chcem vrátiť poškodený tovar."],
        ["hľadať", "nájsť", "Hľadám kabát, ale ešte som ho nenašiel."],
    ], [49 * mm, 42 * mm, 79 * mm], 5.6),
    p("На кассе", H2),
    box("<b>Predavač:</b> Budete platiť kartou alebo v hotovosti?<br/><b>Zákazník:</b> Kartou, prosím. Mohli by ste mi dať aj bloček?<br/><b>Predavač:</b> Samozrejme. Tu je bloček a vaša taška.<br/><b>Zákazník:</b> Ďakujem.", PALE, ROSE, SMALL),
    box("<b>Вид:</b> <i>platím</i> описывает процесс или привычку; <i>zaplatím</i> обозначает один завершённый платёж.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    PageBreak(),

    p("4. Обмен: причина и вежливая просьба", H1),
    p("Для обмена назовите вещь, проблему и желаемое решение. Условная форма смягчает просьбу: <i>chcel by som, mohli by ste, dalo by sa</i>."),
    table([
        ["Функция", "Модель"],
        ["начать", "Chcel by som túto košeľu vymeniť."],
        ["женщина о себе", "Chcela by som vymeniť túto bundu."],
        ["попросить размер", "Mohli by ste mi priniesť väčšiu veľkosť?"],
        ["предложить решение", "Dalo by sa ju vymeniť za inú farbu?"],
        ["уточнить", "Môžem si vybrať iný model?"],
    ], [47 * mm, 123 * mm], 5.8),
    p("Как объяснить проблему", H2),
    table([
        ["Проблема", "Фраза"],
        ["не подходит размер", "Táto veľkosť mi nesedí."],
        ["вещь мала", "Košeľa je mi malá."],
        ["не работает молния", "Zips nefunguje."],
        ["не хватает пуговицы", "Na košeli chýba gombík."],
        ["пятно", "Na rukáve je škvrna."],
        ["распускается шов", "Šev sa pára."],
    ], [54 * mm, 116 * mm], 5.75),
    p("Мини-диалог об обмене", H2),
    box("<b>A:</b> Dobrý deň, chcel by som vymeniť túto košeľu.<br/><b>B:</b> Čo s ňou nie je v poriadku?<br/><b>A:</b> Je mi malá. Mohli by ste mi priniesť väčšiu veľkosť?<br/><b>B:</b> Máte bloček?<br/><b>A:</b> Áno. Dalo by sa ju vymeniť za veľkosť M?<br/><b>B:</b> Pozriem sa, či ju máme.<br/><b>A:</b> Ďakujem.", PALE, ROSE, SMALL),
    PageBreak(),

    p("5. Частые ошибки и упражнения", H1),
    box("<b>Частые ошибки:</b> Nominatív после chcem; несогласованная сравнительная форма; hotovosťou вместо устойчивого v hotovosti; процесс вместо результата; жалоба без причины или желаемого решения.", CREAM, colors.HexColor("#E7C76C"), TINY),
    p("Упражнение 1. Поставьте группу в Akuzatív", H2),
    p("1) modrá bunda; 2) bavlnená košeľa; 3) biele tričko; 4) čierne topánky. Начните с Chcem или Hľadám.", TINY),
    p("Упражнение 2. Образуйте сравнительную форму", H2),
    p("1) veľká veľkosť → ___; 2) krátke nohavice → ___; 3) úzka košeľa → ___; 4) pohodlné topánky → ___.", TINY),
    p("Упражнение 3. Выберите способ оплаты", H2),
    p("1) Zaplatím kartou/karta. 2) Dá sa platiť mobil/mobilom? 3) Zaplatím hotovosťou/v hotovosti. 4) Budete platiť hodinky/hodinkami?", TINY),
    p("Упражнение 4. Выберите вид", H2),
    p("1) Každú sobotu si skúšam/vyskúšam oblečenie. 2) Teraz si chcem skúšať/vyskúšať bundu. 3) Často platím/zaplatím kartou. 4) Potrebujem meniť/vymeniť veľkosť.", TINY),
    p("Упражнение 5. Смягчите просьбу", H2),
    p("1) Prineste mi väčšiu veľkosť. 2) Vymeňte túto bundu. 3) Dajte mi iný model. Используйте mohli by ste / chcel by som / dalo by sa.", TINY),
    p("Упражнение 6. Составьте диалог", H2),
    p("Напишите 7-9 реплик: вы купили брюки, они жмут в поясе, у вас есть чек. Попросите больший размер, уточните обмен и завершите разговор.", TINY),
    PageBreak(),

    p("6. Ответы и итоговая проверка", H1),
    p("Ответы", H2),
    p("<b>1.</b> Например: Chcem modrú bundu. Hľadám bavlnenú košeľu. Chcem biele tričko. Hľadám čierne topánky.", TINY),
    p("<b>2.</b> 1) väčšia veľkosť; 2) kratšie nohavice; 3) užšia košeľa; 4) pohodlnejšie topánky.", TINY),
    p("<b>3.</b> 1) kartou; 2) mobilom; 3) v hotovosti; 4) hodinkami.", TINY),
    p("<b>4.</b> 1) skúšam; 2) vyskúšať; 3) platím; 4) vymeniť.", TINY),
    p("<b>5.</b> Например: Mohli by ste mi priniesť väčšiu veľkosť? Chcel by som túto bundu vymeniť. Dalo by sa vybrať iný model? Возможны другие вежливые варианты.", TINY),
    p("<b>6. Модель:</b><br/><b>A:</b> Dobrý deň, chcel by som vymeniť tieto nohavice.<br/><b>B:</b> Čo s nimi nie je v poriadku?<br/><b>A:</b> Tlačia ma v páse. Mohli by ste mi priniesť väčšiu veľkosť?<br/><b>B:</b> Máte bloček?<br/><b>A:</b> Áno. Dalo by sa ich vymeniť za veľkosť L?<br/><b>B:</b> Áno, pozriem sa na to.<br/><b>A:</b> Ďakujem pekne.", TINY),
    p("Итог в четырёх пунктах", H2),
    table([
        ["OK", "Ставлю вещь после chcem / hľadám в Akuzatív."],
        ["OK", "Сравниваю размер, длину, посадку и цену."],
        ["OK", "Говорю kartou, mobilom, но v hotovosti."],
        ["OK", "Называю причину обмена и вежливо прошу решение."],
    ], [12 * mm, 158 * mm], 6.0, False),
    p("Следующий шаг: в теме 6.9 вы будете понимать статус онлайн-заказа, решать проблему доставки и передавать условия получения или возврата.", SMALL),
]

doc.build(story)
print(OUTPUT)
