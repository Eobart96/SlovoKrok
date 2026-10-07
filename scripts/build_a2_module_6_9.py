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
OUTPUT = ROOT / "output/pdf/A2/Module_06/Slovak_A2_Tema_6_9_Onlayn_zakaz_dostavka_i_vozvrat.pdf"
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
        canvas.drawString(20 * mm, height - 12 * mm, "A2 6.9  |  Онлайн-заказ, доставка и возврат")
    canvas.setFont("Arial", 8)
    canvas.setFillColor(MUTED)
    canvas.drawString(20 * mm, 9 * mm, "SlovoKrok | личный учебный модуль")
    canvas.drawRightString(width - 20 * mm, 9 * mm, f"стр. {page_number} / 7")
    canvas.restoreState()


doc = BaseDocTemplate(
    str(OUTPUT), pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm,
    topMargin=20 * mm, bottomMargin=18 * mm,
    title="Slovak A2 - Тема 6.9 - Онлайн-заказ, доставка и возврат",
    author="SlovoKrok",
)
doc.addPageTemplates([
    PageTemplate(id="series", frames=[Frame(20 * mm, 18 * mm, 170 * mm, 257 * mm, id="main", leftPadding=0, rightPadding=0)], onPage=draw_page)
])


story = [
    p("МОДУЛЬ 6  •  ДОМ, ИНТЕРНЕТ И ПОКУПКИ", KICK),
    p("Онлайн-заказ,<br/>доставка и возврат", TITLE),
    p("Online objednávka, doručenie a vrátenie: sledujeme zásielku a odovzdávame podmienky", SUBTITLE),
    Spacer(1, 38 * mm),
    p("После онлайн-покупки важно понять статус, описать, что уже произошло и что будет дальше, решить проблему с доставкой и точно передать условия получения или возврата."),
    p("После модуля вы сможете:", H2),
    table([
        ["1", "понять основные статусы онлайн-заказа"],
        ["2", "рассказать о заказе в прошлом и будущем"],
        ["3", "уточнить адрес или пункт выдачи и решить проблему"],
        ["4", "передать другому человеку условия получения или возврата"],
    ], [12 * mm, 158 * mm], 7.2, False),
    Spacer(1, 3 * mm),
    box("<b>Формула:</b> что произошло + где посылка сейчас + что будет дальше + что нужно взять, принести или сделать."),
    PageBreak(),

    p("1. Статус заказа и прошедшее время", H1),
    p("Статус часто дан короткой безличной формулой. В своём рассказе используйте прошедшее время и согласуйте форму с говорящим: <i>objednal som / objednala som</i>."),
    table([
        ["Статус", "Что это значит"],
        ["Objednávka bola prijatá.", "Заказ принят."],
        ["Platba bola prijatá.", "Оплата получена."],
        ["Tovar bol odoslaný.", "Товар отправлен."],
        ["Zásielka je na ceste.", "Посылка в пути."],
        ["Zásielka mešká.", "Посылка задерживается."],
        ["Zásielka je pripravená na vyzdvihnutie.", "Посылка готова к получению."],
        ["Zásielka bola doručená.", "Посылка доставлена."],
    ], [84 * mm, 86 * mm], 5.8),
    p("Короткий рассказ о заказе", H2),
    table([
        ["SK", "RU"],
        ["V pondelok som si objednal bundu.", "В понедельник я заказал куртку."],
        ["Hneď som zaplatil kartou.", "Я сразу заплатил картой."],
        ["Obchod v utorok balík odoslal.", "Во вторник магазин отправил посылку."],
        ["Kuriér mi včera volal.", "Курьер звонил мне вчера."],
        ["Balík však neprišiel.", "Но посылка не пришла."],
    ], [86 * mm, 84 * mm], 5.75),
    box("<b>Не путайте:</b> <i>objednávka</i> - заказ, <i>zásielka</i> - отправление, <i>balík</i> - посылка.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    PageBreak(),

    p("2. Что будет дальше: два будущих времени", H1),
    p("С несовершенным глаголом используется <i>budem + infinitív</i>: процесс или ожидание. Совершенный глагол имеет обычную личную форму, но сообщает о будущем результате."),
    table([
        ["Процесс / длительность", "Результат / один шаг"],
        ["Budem čakať na kuriéra.", "Počkám na kuriéra."],
        ["Budem sledovať zásielku.", "Skontrolujem stav zásielky."],
        ["Budem vybavovať reklamáciu.", "Vybavím reklamáciu online."],
        ["Budeme vracať tovar.", "Tovar vrátime zajtra."],
        ["Kuriér bude doručovať balík.", "Kuriér balík doručí popoludní."],
    ], [85 * mm, 85 * mm], 5.8),
    p("Маркеры времени", H2),
    table([
        ["Когда", "Пример"],
        ["dnes popoludní", "Kuriér príde dnes popoludní."],
        ["zajtra ráno", "Balík si vyzdvihnem zajtra ráno."],
        ["do piatku", "Zásielku treba prevziať do piatku."],
        ["o dva dni", "Peniaze mi vrátia o dva dni."],
        ["keď príde e-mail", "Keď príde e-mail, skontrolujem pokyny."],
    ], [48 * mm, 122 * mm], 5.8),
    box("<b>Логика:</b> <i>Budem čakať</i> описывает процесс. <i>Vyzdvihnem si balík</i> обещает конкретный результат.", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    PageBreak(),

    p("3. Vziať или priniesť: адрес и получение", H1),
    p("<i>Vziať</i> значит взять с собой или забрать. <i>Priniesť</i> значит принести к месту или человеку. Направление помогает выбрать глагол."),
    table([
        ["Глагол", "Модель", "Перевод"],
        ["vziať", "Vezmem si občiansky preukaz.", "Я возьму с собой удостоверение."],
        ["vziať", "Kto vezme balík z boxu?", "Кто заберёт посылку из бокса?"],
        ["priniesť", "Kuriér prinesie balík domov.", "Курьер принесёт посылку домой."],
        ["priniesť", "Prineste, prosím, balík na inú adresu.", "Привезите посылку на другой адрес."],
    ], [25 * mm, 78 * mm, 67 * mm], 5.7),
    p("Адрес и пункт выдачи", H2),
    table([
        ["Ситуация", "Полезная фраза"],
        ["адрес доставки", "Doručovacia adresa je Jarná 12, 821 05 Bratislava."],
        ["сменить адрес", "Potrebujem zmeniť doručovaciu adresu."],
        ["пункт выдачи", "Balík je uložený na výdajnom mieste."],
        ["автомат", "Zásielku si vyzdvihnem v samoobslužnom boxe."],
        ["код", "Na vyzdvihnutie potrebujete kód z SMS."],
        ["срок", "Balík si môžete vyzdvihnúť do piatku."],
    ], [48 * mm, 122 * mm], 5.7),
    box("<b>Для человека:</b> <i>na adresu</i> - к адресу доставки; <i>na výdajnom mieste</i> - в пункте выдачи; <i>z boxu</i> - из бокса.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    PageBreak(),

    p("4. Причина, следствие и передача условий", H1),
    p("Причина отвечает на <i>prečo?</i>: <i>pretože, lebo</i>. Следствие показывает результат: <i>preto, takže</i>. Передавайте только те условия, которые есть в сообщении магазина."),
    table([
        ["Связка", "Пример"],
        ["pretože", "Kontaktoval som podporu, pretože zásielka mešká."],
        ["lebo", "Zmenila som adresu, lebo zajtra nebudem doma."],
        ["preto", "Balík neprišiel, preto som napísal predajcovi."],
        ["takže", "Tovar je poškodený, takže ho vrátim."],
    ], [33 * mm, 137 * mm], 5.75),
    p("Передаём сообщение другому человеку", H2),
    box("<b>Správa z obchodu:</b> Zásielka je pripravená na vyzdvihnutie. Výdajné miesto je na Hlavnej 8. Prineste si kód z SMS. Balík si môžete vyzdvihnúť do piatku.<br/><br/><b>Передача:</b> Peter, balík je pripravený na výdajnom mieste na Hlavnej 8. Musíš si vziať telefón s kódom z SMS a vyzdvihnúť ho do piatku.", PALE, ROSE, SMALL),
    p("Мини-диалог с поддержкой", H2),
    box("<b>A:</b> Dobrý deň, moja zásielka mešká.<br/><b>B:</b> Prosím, nadiktujte číslo objednávky.<br/><b>A:</b> Je to 45821. Kuriér mi včera volal, ale balík nepriniesol.<br/><b>B:</b> Balík doručíme zajtra popoludní.<br/><b>A:</b> Zajtra nebudem doma. Dalo by sa zmeniť výdajné miesto?<br/><b>B:</b> Áno, pošleme vám nový kód e-mailom.<br/><b>A:</b> Ďakujem.", GREEN, colors.HexColor("#A8D5B3"), TINY),
    p("Условия возврата из письма", H2),
    box("<i>Formulár na vrátenie je v balíku. Tovar musí byť nepoužitý. Balík pošlite späť do 30 dní.</i><br/>Передача: формуляр лежит в посылке; товар должен быть неиспользованным; отправить назад нужно в течение 30 дней.", CREAM, colors.HexColor("#E7C76C"), TINY),
    PageBreak(),

    p("5. Частые ошибки и упражнения", H1),
    box("<b>Частые ошибки:</b> путать objednávka, zásielka и balík; строить будущее совершенного глагола с budem; смешивать vziať и priniesť; не указывать причину, адрес или срок; добавлять условия, которых нет в сообщении.", CREAM, colors.HexColor("#E7C76C"), TINY),
    p("Упражнение 1. Соедините статус и значение", H2),
    p("1) Zásielka je na ceste. 2) Zásielka mešká. 3) Zásielka je pripravená na vyzdvihnutie. 4) Zásielka bola doručená. Значения: a) доставлена; b) задерживается; c) в пути; d) готова к получению.", TINY),
    p("Упражнение 2. Поставьте глагол в прошедшее время", H2),
    p("1) V pondelok si ___ bundu. (objednať, мужчина) 2) Obchod balík ___. (odoslať) 3) Kuriér mi ___. (volať) 4) Zásielka ___. (neprísť)", TINY),
    p("Упражнение 3. Выберите будущее", H2),
    p("Выберите форму по русской подсказке: 1) Zajtra budem čakať/počkám na kuriéra celý deň. (буду ждать) 2) Balík si budem vyzdvihovať/vyzdvihnem zajtra. (заберу) 3) Kuriér bude doručovať/doručí balík o tretej. (доставит) 4) Večer budem sledovať/skontrolujem stav zásielky celý čas. (буду отслеживать)", TINY),
    p("Упражнение 4. Выберите vziať или priniesť", H2),
    p("1) ___ si občiansky preukaz. 2) Kuriér ___ balík domov. 3) Kto ___ zásielku z boxu? 4) Prosím, ___ balík na novú adresu.", TINY),
    p("Упражнение 5. Свяжите причину и следствие", H2),
    p("Соедините пары с pretože, preto или takže: zásielka mešká / píšem podpore; zajtra nebudem doma / mením adresu; tovar je poškodený / vrátim ho.", TINY),
    p("Упражнение 6. Передайте условия", H2),
    p("Напишите 5-7 предложений для Анны: посылка лежит в пункте на Parkovej 4; нужен код из SMS; получить до среды; при возврате заполнить формуляр и отправить товар назад до пятницы.", TINY),
    PageBreak(),

    p("6. Ответы и итоговая проверка", H1),
    p("Ответы", H2),
    p("<b>1.</b> 1c; 2b; 3d; 4a.", TINY),
    p("<b>2.</b> 1) objednal som si; 2) odoslal; 3) volal; 4) neprišla.", TINY),
    p("<b>3.</b> 1) budem čakať; 2) vyzdvihnem; 3) doručí; 4) budem sledovať.", TINY),
    p("<b>4.</b> 1) Vezmem; 2) prinesie; 3) vezme; 4) prineste.", TINY),
    p("<b>5.</b> Например: Píšem podpore, pretože zásielka mešká. Zajtra nebudem doma, preto mením adresu. Tovar je poškodený, takže ho vrátim. Возможны другие логичные варианты.", TINY),
    p("<b>6. Модель:</b><br/>Anna, tvoj balík je pripravený na výdajnom mieste na Parkovej 4. Na vyzdvihnutie potrebuješ kód z SMS. Balík si musíš vyzdvihnúť do stredy. Ak ho chceš vrátiť, vyplň formulár na vrátenie. Potom pošli tovar späť do piatku.", TINY),
    p("Итог в четырёх пунктах", H2),
    table([
        ["OK", "Понимаю, что уже произошло с заказом."],
        ["OK", "Различаю процесс в будущем и будущий результат."],
        ["OK", "Выбираю vziať или priniesť по направлению действия."],
        ["OK", "Передаю адрес, код, срок и условия возврата без искажений."],
    ], [12 * mm, 158 * mm], 6.0, False),
    p("Модуль 6 завершён: теперь вы можете действовать в бытовых, цифровых и покупательских ситуациях и передавать практическую информацию другому человеку.", SMALL),
]

doc.build(story)
print(OUTPUT)
