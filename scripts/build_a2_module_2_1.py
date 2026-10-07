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
OUTPUT = ROOT / "output" / "pdf" / "A2" / "Module_02" / "Slovak_A2_Tema_2_1_Nominativ_mnozhestvennogo_chisla.pdf"
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
BODY = ParagraphStyle("Body", fontName="Arial", fontSize=9.0, leading=12.0, textColor=INK, spaceAfter=4.0 * mm)
SMALL = ParagraphStyle("Small", parent=BODY, fontSize=7.8, leading=9.9, spaceAfter=2.0 * mm)
TINY = ParagraphStyle("Tiny", parent=BODY, fontSize=7.2, leading=9.0, spaceAfter=1.4 * mm)
TITLE = ParagraphStyle("Title", fontName="Arial-Bold", fontSize=23, leading=27, textColor=colors.white, alignment=TA_LEFT, spaceAfter=5 * mm)
SUBTITLE = ParagraphStyle("Subtitle", fontName="Arial", fontSize=12, leading=16, textColor=colors.HexColor("#FFD8EB"), spaceAfter=5 * mm)
H1 = ParagraphStyle("H1", fontName="Arial-Bold", fontSize=16, leading=19, textColor=PLUM, spaceBefore=1 * mm, spaceAfter=4 * mm)
H2 = ParagraphStyle("H2", fontName="Arial-Bold", fontSize=11.2, leading=14, textColor=PINK, spaceBefore=2 * mm, spaceAfter=2.2 * mm)
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


def styled_table(data, widths, font_size=7.6, header=True):
    converted = []
    for row_index, row in enumerate(data):
        style = ParagraphStyle(
            f"Cell{row_index}", parent=SMALL, fontSize=font_size, leading=font_size + 2,
            textColor=colors.white if header and row_index == 0 else INK,
            fontName="Arial-Bold" if header and row_index == 0 else "Arial", spaceAfter=0,
        )
        converted.append([p(str(cell), style) for cell in row])
    table = Table(converted, colWidths=widths, repeatRows=1 if header else 0)
    commands = [
        ("GRID", (0, 0), (-1, -1), 0.45, ROSE), ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
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
        canvas.drawString(20 * mm, height - 12 * mm, "SLOVAK A2  |  ТЕМА 2.1")
        canvas.drawRightString(width - 20 * mm, height - 12 * mm, "Nominatív множественного числа")
    canvas.setStrokeColor(PINK)
    canvas.setLineWidth(0.6)
    canvas.line(20 * mm, 14 * mm, width - 20 * mm, 14 * mm)
    canvas.setFont("Arial", 7.8)
    canvas.setFillColor(MUTED)
    canvas.drawString(20 * mm, 9 * mm, "SlovoKrok | личный учебный модуль")
    canvas.drawRightString(width - 20 * mm, 9 * mm, f"стр. {page} / 7")
    canvas.restoreState()


doc = BaseDocTemplate(
    str(OUTPUT), pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=20 * mm, bottomMargin=18 * mm,
    title="Slovak A2 - Тема 2.1 - Nominatív множественного числа: предметы и понятия", author="SlovoKrok",
)
frame = Frame(20 * mm, 18 * mm, 170 * mm, 257 * mm, id="main", leftPadding=0, rightPadding=0)
doc.addPageTemplates([PageTemplate(id="series", frames=[frame], onPage=draw_page)])

story = [
    p("МОДУЛЬ 2  •  ИМЕННАЯ ГРУППА ВО МНОЖЕСТВЕННОМ ЧИСЛЕ", COVER_KICKER),
    p("Nominatív множественного числа:<br/>предметы и понятия", TITLE),
    p("Nominatív množného čísla: veci a pojmy", SUBTITLE),
    Spacer(1, 34 * mm),
    p("На A2 мало назвать несколько предметов. Нужно согласовать всю группу: указательное или притяжательное слово, прилагательное, существительное и именную часть сказуемого.", BODY),
    p("После модуля вы сможете:", H2),
    styled_table([
        ["1", "образовывать Nominatív множественного числа у неодушевлённых существительных женского и среднего рода"],
        ["2", "выбирать формы tie / tieto, moje / naše и окончание прилагательного -é"],
        ["3", "строить полную цепочку согласования в описании предметов и понятий"],
        ["4", "находить и исправлять типичные ошибки без подмены темы формами для людей"],
    ], [12 * mm, 158 * mm], font_size=8.0, header=False),
    Spacer(1, 3 * mm),
    box("<b>Главная формула:</b> tie / tieto + moje / naše + nové + knihy / mestá + sú / boli + užitočné.", PALE, PINK),
    PageBreak(),

    p("1. Женский род: четыре модели", H1),
    p("Форму множественного числа определяет не последняя буква сама по себе, а модель склонения. На A2 полезно узнавать четыре частотные группы и запоминать новое слово сразу с формой Nominatív plural.", BODY),
    styled_table([
        ["Модель", "Единственное -> множественное", "Ещё примеры"],
        ["žena", "kniha -> knihy", "otázka -> otázky; škola -> školy; firma -> firmy"],
        ["ulica", "ulica -> ulice", "práca -> práce; stanica -> stanice; informácia -> informácie"],
        ["dlaň", "dlaň -> dlane", "továreň -> továrne; báseň -> básne"],
        ["kosť", "kosť -> kosti", "vec -> veci; možnosť -> možnosti; skúsenosť -> skúsenosti"],
    ], [28 * mm, 54 * mm, 88 * mm], font_size=7.3),
    p("Как учить форму", H2),
    styled_table([
        ["Не так", "Лучше", "Почему"],
        ["informácia", "informácia - informácie", "видна смена окончания"],
        ["možnosť", "možnosť - možnosti", "видна модель на -osť"],
        ["kniha", "nová kniha - nové knihy", "сразу тренируется согласование"],
    ], [38 * mm, 62 * mm, 70 * mm], font_size=7.3),
    Spacer(1, 4 * mm),
    box("<b>Важно:</b> формы на -y, -e и -i равноправны. Нельзя механически ставить одно окончание всем существительным женского рода.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    PageBreak(),

    p("2. Средний род: три главные модели", H1),
    p("У среднего рода особенно заметно, что форма множественного числа зависит от модели. Сравните: mesto -> mestá, srdce -> srdcia, stretnutie -> stretnutia.", BODY),
    styled_table([
        ["Модель", "Единственное -> множественное", "Ещё примеры"],
        ["mesto", "mesto -> mestá", "okno -> okná; auto -> autá; číslo -> čísla"],
        ["srdce", "srdce -> srdcia", "more -> moria; pole -> polia"],
        ["vysvedčenie", "stretnutie -> stretnutia", "cvičenie -> cvičenia; námestie -> námestia; vysvedčenie -> vysvedčenia"],
    ], [31 * mm, 58 * mm, 81 * mm], font_size=7.25),
    p("Словарь темы", H2),
    styled_table([
        ["Предметы", "Места и события", "Понятия"],
        ["knihy, stoličky, okná, autá", "mestá, námestia, stretnutia", "otázky, informácie, možnosti"],
        ["čísla, cvičenia, vysvedčenia", "školy, stanice, továrne", "veci, skúsenosti, práce"],
    ], [57 * mm, 57 * mm, 56 * mm], font_size=7.2),
    Spacer(1, 4 * mm),
    box("<b>Граница темы:</b> здесь речь о предметах и понятиях. Формы для людей - например, <b>tí noví kolegovia</b> - разбираются отдельно в модуле 2.2.", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    PageBreak(),

    p("3. Полное согласование", H1),
    p("У неодушевлённых существительных женского и среднего рода формы зависимых слов в Nominatív plural совпадают. Это позволяет строить одну общую схему.", BODY),
    styled_table([
        ["Что согласуем", "Форма", "Пример"],
        ["указательное слово", "tie / tieto", "tie knihy; tieto mestá"],
        ["притяжательное слово", "moje / tvoje / svoje / naše / vaše", "moje otázky; naše autá"],
        ["его / её / их", "jeho / jej / ich не изменяются", "jej knihy; ich mestá"],
        ["прилагательное", "обычно -é", "nové knihy; malé mestá"],
        ["сказуемое", "sú / boli + форма на -é", "knihy sú nové; mestá boli pokojné"],
    ], [42 * mm, 61 * mm, 67 * mm], font_size=7.15),
    p("Из единственного числа во множественное", H2),
    styled_table([
        ["Единственное число", "Множественное число"],
        ["tá nová kniha", "tie nové knihy"],
        ["tá dôležitá informácia", "tieto dôležité informácie"],
        ["to malé mesto", "tie malé mestá"],
        ["to pracovné stretnutie", "tieto pracovné stretnutia"],
        ["moja nová kniha", "moje nové knihy"],
    ], [78 * mm, 92 * mm], font_size=7.25),
    Spacer(1, 3 * mm),
    box("<b>Tie</b> указывает на уже известные или более удалённые предметы, <b>tieto</b> - на эти, выбранные сейчас. Обычно достаточно одного определителя: <b>tieto nové knihy</b> или <b>moje nové knihy</b>. Цепочка <b>tieto moje nové knihy</b> нужна только для контраста.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    PageBreak(),

    p("4. Описание: от списка к связному тексту", H1),
    p("Сначала назовите группу, затем добавьте признак, место или оценку. Повторяйте существительное только там, где без него возникает неясность.", BODY),
    p("Модель описания", H2),
    box("<b>V našej kancelárii sú nové stoličky a veľké okná.</b> Tieto stoličky sú pohodlné a okná sú čisté. Na stole sú dôležité správy a pracovné dokumenty. Moje poznámky sú krátke, ale užitočné. Dnešné stretnutia sú dlhé. Všetky informácie sú presné.", PALE, ROSE, SMALL),
    p("Перевод", H2),
    p("В нашем офисе новые стулья и большие окна. Эти стулья удобные, а окна чистые. На столе важные сообщения и рабочие документы. Мои заметки короткие, но полезные. Сегодняшние встречи долгие. Вся информация точная.", SMALL),
    p("Мини-диалог", H2),
    box("<b>A:</b> Sú tieto knihy nové?<br/><b>B:</b> Áno, sú nové, ale nie sú moje.<br/><b>A:</b> A kde sú naše cvičenia?<br/><b>B:</b> Naše cvičenia sú v počítači.<br/><b>A:</b> Sú tie informácie aktuálne?<br/><b>B:</b> Áno, všetky informácie sú aktuálne.", ALT, ROSE, SMALL),
    p("Перевод: Эти книги новые? - Да, новые, но не мои. - А где наши упражнения? - В компьютере. - Та информация актуальна? - Да, вся информация актуальна.", SMALL),
    p("Опоры для собственного текста", H2),
    styled_table([
        ["Где?", "Что есть?", "Какие?"],
        ["v izbe, v kancelárii, na stole", "knihy, okná, veci, informácie", "nové, malé, dôležité, užitočné"],
    ], [58 * mm, 58 * mm, 54 * mm], font_size=7.15),
    PageBreak(),

    p("5. Частые ошибки и упражнения", H1),
    box("<b>Проверьте три места:</b> форму существительного; форму определителя; окончание прилагательного. Затем проверьте сказуемое: <b>sú / boli</b> и, если нужно, ещё одна форма на <b>-é</b>.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    p("Упражнение 1. Образуйте множественное число", H2),
    p("1) kniha; 2) informácia; 3) vec; 4) mesto; 5) srdce; 6) stretnutie; 7) možnosť; 8) okno.", SMALL),
    p("Упражнение 2. Преобразуйте всю группу", H2),
    p("1) tá nová kniha; 2) tá dôležitá otázka; 3) to malé mesto; 4) to pracovné stretnutie; 5) moja dobrá skúsenosť.", SMALL),
    p("Упражнение 3. Выберите форму", H2),
    p("1) (tá / tie) nové knihy; 2) (toto / tieto) veľké okná; 3) (moja / moje) dôležité informácie; 4) (náš / naše) malé mestá; 5) jej (nové / nová) autá.", SMALL),
    p("Упражнение 4. Вставьте форму сказуемого", H2),
    p("1) Knihy ___ nové. 2) Mestá ___ pokojné. 3) Stretnutia včera ___ dlhé. 4) Informácie ___ presné. Используйте sú или boli.", SMALL),
    p("Упражнение 5. Исправьте ошибки", H2),
    p("1) Tieto nová knihy sú zaujímavá. 2) Moja informácie sú presné. 3) Tie mesto boli veľké. 4) Naše stretnutie sú krátke. 5) Jej nové autá je drahé.", SMALL),
    p("Упражнение 6. Опишите место", H2),
    p("Напишите 5-7 предложений о комнате, офисе или городе. Используйте минимум две формы женского рода, две формы среднего рода, tie / tieto, притяжательное слово и конструкцию sú / boli + прилагательное.", SMALL),
    PageBreak(),

    p("6. Ответы и проверка мастерства", H1),
    p("Ответы", H2),
    p("<b>1.</b> knihy; informácie; veci; mestá; srdcia; stretnutia; možnosti; okná.", TINY),
    p("<b>2.</b> tie nové knihy; tie dôležité otázky; tie malé mestá; tie pracovné stretnutia; moje dobré skúsenosti.", TINY),
    p("<b>3.</b> tie; tieto; moje; naše; nové.", TINY),
    p("<b>4.</b> 1) sú; 2) sú; 3) boli; 4) sú.", TINY),
    p("<b>5.</b> 1) Tieto nové knihy sú zaujímavé. 2) Moje informácie sú presné. 3) Tie mestá boli veľké. 4) Naše stretnutia sú krátke. 5) Jej nové autá sú drahé.", TINY),
    p("<b>6. Модель:</b> V mojej izbe sú veľké okná a nové knihy. Tieto knihy sú zaujímavé. Moje pracovné veci sú na stole. Naše staré cvičenia sú v počítači. Okná boli čisté, ale teraz sú špinavé. Všetky informácie sú užitočné.", TINY),
    p("Итог в четырёх пунктах", H2),
    styled_table([
        ["OK", "Я различаю модели knihy, ulice, dlane, kosti."],
        ["OK", "Я образую формы mestá, srdcia, stretnutia."],
        ["OK", "Я согласую tie / tieto, moje / naše и прилагательное на -é."],
        ["OK", "Я описываю несколько предметов или понятий с sú / boli."],
    ], [12 * mm, 158 * mm], font_size=7.7, header=False),
    Spacer(1, 3 * mm),
    box("<b>Финальная проверка:</b> выберите пять предметов вокруг себя и назовите их полными группами. Если все определения и сказуемые согласованы, цель модуля достигнута.", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    p("Следующий шаг", H2),
    p("В модуле 2.2 вы добавите людей: формы <b>tí</b>, окончания прилагательных и особые формы мужского одушевлённого рода.", SMALL),
]

doc.build(story)
print(OUTPUT)
