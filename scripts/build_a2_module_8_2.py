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
OUTPUT = ROOT / "output/pdf/A2/Module_08/Slovak_A2_Tema_8_2_Emocii_nedorazumenie_i_podderzhka.pdf"
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
        canvas.drawString(20 * mm, height - 12 * mm, "A2 8.2  |  Эмоции, недоразумение и поддержка")
    canvas.setFont("Arial", 8)
    canvas.setFillColor(MUTED)
    canvas.drawString(20 * mm, 9 * mm, "SlovoKrok | личный учебный модуль")
    canvas.drawRightString(width - 20 * mm, 9 * mm, f"стр. {page_number} / 7")
    canvas.restoreState()


doc = BaseDocTemplate(
    str(OUTPUT), pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=20 * mm, bottomMargin=18 * mm,
    title="Slovak A2 - Тема 8.2 - Эмоции, недоразумение и поддержка", author="SlovoKrok",
)
doc.addPageTemplates([PageTemplate(
    id="series", frames=[Frame(20 * mm, 18 * mm, 170 * mm, 257 * mm, id="main", leftPadding=0, rightPadding=0)], onPage=draw_page,
)])


story = [
    p("МОДУЛЬ 8  •  ОТНОШЕНИЯ, ЗДОРОВЬЕ И ИТОГ A2", KICK),
    p("Эмоции, недоразумение и поддержка", TITLE),
    p("Emócie, nedorozumenie a podpora: объясняем, извиняемся и помогаем", SUBTITLE),
    Spacer(1, 44 * mm),
    p("На уровне A2 важно не только назвать чувство, но и спокойно объяснить его причину, исправить простое недоразумение и предложить человеку понятную поддержку."),
    p("После модуля вы сможете:", H2),
    table([
        ["1", "выразить эмоцию через byť и cítiť sa"],
        ["2", "употребить páčiť sa и конструкции с дательным падежом"],
        ["3", "объяснить недоразумение и естественно извиниться"],
        ["4", "поддержать собеседника и дать мягкий совет"],
    ], [12 * mm, 158 * mm], 7.1, False),
    Spacer(1, 3 * mm),
    box("<b>Формула разговора:</b> чувство → причина → что произошло на самом деле → извинение → поддержка или совет."),
    PageBreak(),

    p("1. Как назвать эмоцию", H1),
    p("Для состояния используйте две основные модели. <b>Som + прилагательное</b> согласуется с говорящим; <b>cítim sa + наречие</b> не меняется. После <i>cítiť sa</i> возможно и прилагательное: <i>Cítim sa unavená</i>."),
    table([
        ["Модель", "Пример", "Перевод"],
        ["byť + прилагательное", "Som rád, že si prišiel.", "Я рад, что ты пришёл."],
        ["byť + прилагательное", "Bola som sklamaná z výsledku.", "Я была разочарована результатом."],
        ["cítiť sa + наречие", "Dnes sa cítim pokojne.", "Сегодня я чувствую себя спокойно."],
        ["cítiť sa + прилагательное", "Po rozhovore sa cítim istejšia.", "После разговора я чувствую себя увереннее."],
        ["mať + существительное", "Mám radosť z tvojej správy.", "Я рад твоему сообщению."],
        ["báť sa + G", "Bojím sa jeho reakcie.", "Я боюсь его реакции."],
        ["tešiť sa na + A", "Teším sa na naše stretnutie.", "Я жду нашей встречи с радостью."],
    ], [43 * mm, 67 * mm, 60 * mm], 5.2),
    p("Возвратные глаголы: sa нельзя потерять", H2),
    table([
        ["Глагол", "Пример", "Значение"],
        ["cítiť sa", "Necítim sa dnes dobre.", "Сегодня я неважно себя чувствую."],
        ["hnevať sa na + A", "Hnevám sa na Petra.", "Я сержусь на Петера."],
        ["mýliť sa", "Asi som sa mýlil.", "Наверное, я ошибался."],
        ["tešiť sa z + G", "Teším sa z tvojho úspechu.", "Я радуюсь твоему успеху."],
    ], [36 * mm, 70 * mm, 64 * mm], 5.4),
    box("<b>Не смешивайте:</b> <i>teším sa na stretnutie</i> - жду будущую встречу; <i>teším sa zo stretnutia</i> - радуюсь самой встрече или её результату.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    PageBreak(),

    p("2. Páčiť sa, Je mi ľúto и дательный", H1),
    p("В конструкциях <b>páčiť sa</b> и <b>je mi ľúto</b> человек выражается дательным: <i>mi, ti, mu, jej, nám, vám, im</i>. То, что нравится, управляет числом глагола: <i>páči sa</i> в единственном, <i>páčia sa</i> во множественном."),
    table([
        ["Кому", "Единственное", "Множественное"],
        ["mi", "Páči sa mi tento nápad.", "Páčia sa mi tvoje návrhy."],
        ["ti", "Páči sa ti táto hudba?", "Páčia sa ti tie fotografie?"],
        ["mu / jej", "Jemu sa páči nový kurz.", "Jej sa páčia slovenské filmy."],
        ["nám / vám / im", "Nám sa páči riešenie.", "Im sa páčia spoločné výlety."],
    ], [24 * mm, 73 * mm, 73 * mm], 5.25),
    p("Je mi ľúto: сочувствие или извинение", H2),
    table([
        ["Функция", "Словацкий", "Русский"],
        ["сочувствие", "Je mi ľúto, že sa to stalo.", "Мне жаль, что это случилось."],
        ["извинение", "Je mi ľúto, že som neprišiel.", "Мне жаль, что я не пришёл."],
        ["реакция", "To ma naozaj mrzí.", "Мне действительно очень жаль."],
        ["признание", "Chápem, že ťa to nahnevalo.", "Я понимаю, что тебя это рассердило."],
    ], [36 * mm, 72 * mm, 62 * mm], 5.35),
    p("Позиция коротких форм", H2),
    box("Короткие <i>sa, mi, ti, mu</i> обычно стоят близко к началу фразы: <i>Dnes sa mi ten plán páči.</i> - Сегодня мне нравится этот план. В нейтральном вопросе: <i>Prečo sa ti nepáči môj návrh?</i> - Почему тебе не нравится моё предложение?", PALE, ROSE, SMALL),
    box("<b>Типичная ошибка:</b> по-русски «я нравлюсь / мне нравится» легко перепутать. <i>Páči sa mi Lucia</i> = Луция нравится мне. Человек в дательном - тот, кто испытывает чувство.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    PageBreak(),

    p("3. Объясняем недоразумение и извиняемся", H1),
    p("Хорошее объяснение не спорит с эмоцией собеседника. Сначала назовите факт, затем причину и исправление. Связки помогают показать логику, а не оправдываться."),
    table([
        ["Связка", "Как работает", "Пример"],
        ["pretože / lebo", "называет причину", "Neprišiel som, pretože som si pomýlil čas."],
        ["preto", "показывает результат", "Pomýlil som si čas, preto som meškal."],
        ["takže", "вывод / следствие", "Správa mi neprišla, takže som o zmene nevedel."],
        ["ale", "контраст", "Chcel som ti zavolať, ale vybil sa mi telefón."],
    ], [33 * mm, 48 * mm, 89 * mm], 5.35),
    p("Четыре шага извинения", H2),
    table([
        ["Шаг", "Полезная фраза", "Перевод"],
        ["1. признать", "Prepáč, že som ti nenapísal.", "Прости, что я тебе не написал."],
        ["2. признать чувство", "Chápem, že si bola sklamaná.", "Понимаю, что ты была разочарована."],
        ["3. объяснить", "Myslel som si, že stretnutie je o siedmej.", "Я думал, что встреча в семь."],
        ["4. исправить", "Nabudúce si čas hneď potvrdím.", "В следующий раз я сразу подтвержу время."],
    ], [28 * mm, 79 * mm, 63 * mm], 5.25),
    p("Мини-диалог", H2),
    box("<b>Eva:</b> Prečo si neprišiel? Čakala som na teba pol hodiny.<br/><b>Martin:</b> Je mi to ľúto. Myslel som si, že stretnutie je o siedmej, nie o šiestej.<br/><b>Eva:</b> Bola som sklamaná, pretože si mi nenapísal.<br/><b>Martin:</b> Chápem. Mal som ti zavolať. Prepáč, prosím.<br/><b>Eva:</b> Dobre. Nabudúce by si mal potvrdiť čas.<br/><b>Martin:</b> Máš pravdu. Hneď si ho zapíšem.", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    box("<b>Важно:</b> <i>Prepáč</i> - неформально одному человеку; <i>Prepáčte</i> - вежливо или нескольким. <i>Je mi to ľúto</i> сильнее показывает сожаление, но не заменяет конкретное признание ошибки.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    PageBreak(),

    p("4. Поддержка и мягкий совет", H1),
    p("Поддержка начинается не с совета, а с короткого признания чувства. Затем спросите, нужна ли помощь. Совет через <b>mal by si / mala by si</b> звучит прямее; <b>mohol by si / mohla by si</b> и <b>skús</b> обычно мягче."),
    table([
        ["Задача", "Фраза", "Перевод"],
        ["признать", "Chápem, ako sa cítiš.", "Я понимаю, что ты чувствуешь."],
        ["сочувствовать", "To ma mrzí. Muselo to byť nepríjemné.", "Мне жаль. Наверное, это было неприятно."],
        ["быть рядом", "Som tu pre teba.", "Я рядом с тобой."],
        ["спросить", "Chceš sa o tom porozprávať?", "Хочешь об этом поговорить?"],
        ["предложить", "Môžem ti nejako pomôcť?", "Я могу тебе чем-то помочь?"],
        ["мягкий совет", "Mohla by si mu pokojne napísať.", "Ты могла бы спокойно ему написать."],
        ["совет", "Mal by si sa s ňou porozprávať.", "Тебе стоит с ней поговорить."],
        ["вариант", "Skús jej vysvetliť, čo sa stalo.", "Попробуй объяснить ей, что случилось."],
    ], [36 * mm, 72 * mm, 62 * mm], 5.0),
    p("Mal by som: формы, которые нужны в разговоре", H2),
    table([
        ["Лицо", "Модель", "Пример"],
        ["я", "mal by som / mala by som", "Mala by som sa ospravedlniť."],
        ["ты", "mal by si / mala by si", "Mal by si mu povedať pravdu."],
        ["он / она", "mal by / mala by", "Mala by mu pokojne zavolať."],
        ["вы", "mali by ste", "Mali by ste sa pokojne porozprávať."],
    ], [29 * mm, 57 * mm, 84 * mm], 5.25),
    p("Короткий разговор поддержки", H2),
    box("<b>Lucia:</b> Som nahnevaná, lebo Zuzana neodpovedala na moju správu.<br/><b>Peter:</b> Chápem, ako sa cítiš. Možno si správu ešte neprečítala.<br/><b>Lucia:</b> Myslíš, že jej mám zavolať?<br/><b>Peter:</b> Mohla by si chvíľu počkať a potom jej pokojne zavolať. Chceš, aby som zostal s tebou?<br/><b>Lucia:</b> Ďakujem. To by mi pomohlo.", PALE, ROSE, SMALL),
    PageBreak(),

    p("5. Частые ошибки и упражнения", H1),
    table([
        ["Ошибка", "Правильно", "Почему"],
        ["*Ja sa cítim nervózny dobre.", "Cítim sa nervózne / Som nervózny.", "две разные модели"],
        ["*Ja páčim tento film.", "Páči sa mi tento film.", "человек в D"],
        ["*Páči sa mi tie knihy.", "Páčia sa mi tie knihy.", "множественное число"],
        ["*Je ma ľúto.", "Je mi ľúto.", "устойчивая форма D"],
        ["*Mal by si porozprávať s ňou.", "Mal by si sa s ňou porozprávať.", "нужно sa"],
    ], [51 * mm, 65 * mm, 54 * mm], 5.05),
    p("Упражнение 1. Выберите модель", H2),
    p("1) (Som / Cítim sa) sklamaná. 2) Dnes sa (cítim / som) pokojne. 3) (Mám / Som) radosť z tvojej správy. 4) Teším sa (na / z) zajtrajší výlet.", SMALL),
    p("Упражнение 2. Вставьте дательную форму и глагол", H2),
    p("1) ___ sa ___ tento nápad. (ja, páčiť) 2) ___ sa ___ nové fotografie. (ona, páčiť) 3) ___ je ľúto, že mešká. (on) 4) Prečo sa ___ nepáči môj návrh? (ty)", SMALL),
    p("Упражнение 3. Соедините причину и следствие", H2),
    p("Используйте <i>pretože, preto, takže</i>: 1) Pomýlil som si čas. Meškal som. 2) Správa neprišla. O zmene som nevedela. 3) Som sklamaná. Nenapísal si mi.", SMALL),
    p("Упражнение 4. Исправьте ошибки", H2),
    p("1) Páči sa mi tvoje návrhy. 2) Je ma ľúto, že som neprišiel. 3) Mal by si s ňou porozprávať. 4) Hnevám Petra.", SMALL),
    p("Упражнение 5. Переведите", H2),
    p("1) Мне жаль, что это случилось. 2) Я понимаю, что ты разочарована. 3) Тебе стоит спокойно ему написать. 4) Я думал, что встреча в семь.", SMALL),
    p("Упражнение 6. Самостоятельный мини-диалог", H2),
    p("Напишите 6-8 реплик: один человек расстроен из-за недоразумения; второй признаёт чувство, объясняет факт, извиняется и предлагает один мягкий совет или помощь.", SMALL),
    PageBreak(),

    p("6. Ответы и проверка мастерства", H1),
    p("Ответы", H2),
    table([
        ["№", "Ключ"],
        ["1", "1 Som sklamaná; 2 cítim pokojne; 3 Mám radosť; 4 na zajtrajší výlet."],
        ["2", "1 Mne sa páči; 2 Jej sa páčia; 3 Jemu je ľúto; 4 ti."],
        ["3", "Возможные ответы: Pomýlil som si čas, preto som meškal. Správa neprišla, takže som o zmene nevedela. Som sklamaná, pretože si mi nenapísal."],
        ["4", "1 Páčia sa mi tvoje návrhy. 2 Je mi ľúto, že som neprišiel. 3 Mal by si sa s ňou porozprávať. 4 Hnevám sa na Petra."],
        ["5", "1 Je mi ľúto, že sa to stalo. 2 Chápem, že si sklamaná. 3 Mal by si mu pokojne napísať. 4 Myslel som si, že stretnutie je o siedmej."],
        ["6", "Открытое задание: возможны другие естественные ответы при сохранении всех четырёх действий."],
    ], [13 * mm, 157 * mm], 5.05),
    p("Модель самостоятельного диалога", H2),
    box("<b>Jana:</b> Som sklamaná, pretože si neprišla na kávu.<br/><b>Mária:</b> Je mi to ľúto. Myslela som si, že sme sa dohodli na zajtra.<br/><b>Jana:</b> Písala som ti dnes ráno.<br/><b>Mária:</b> Správu som nevidela, lebo som mala vypnutý telefón. Chápem, že ťa to nahnevalo. Prepáč.<br/><b>Jana:</b> Dobre, bolo to nedorozumenie.<br/><b>Mária:</b> Nabudúce by sme si mali čas potvrdiť. Môžem ťa pozvať zajtra?<br/><b>Jana:</b> Áno, to sa mi páči.", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    p("Четыре опоры темы", H2),
    table([
        ["1", "<i>Som nervózny</i>, но <i>cítim sa nervózne</i>; возвратное <i>sa</i> обязательно."],
        ["2", "<i>Páči sa mi nápad / Páčia sa mi návrhy</i>: глагол согласуется с тем, что нравится."],
        ["3", "Извинение: признать чувство, объяснить факт, сказать <i>prepáč</i>, предложить исправление."],
        ["4", "Сначала поддержка, затем совет: <i>Chápem... Mohol by si... Mal by si...</i>"],
    ], [11 * mm, 159 * mm], 5.55, False),
    p("Финальная проверка", H2),
    box("Без подсказки назовите три эмоции; скажите, что вам нравится; объясните недоразумение через причину и следствие; извинитесь в двух шагах; поддержите человека и дайте мягкий совет. Если получается связный диалог, цель 8.2 достигнута.", PALE, ROSE, SMALL),
]

doc.build(story)
print(OUTPUT)
