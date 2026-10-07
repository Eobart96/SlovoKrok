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
OUTPUT = ROOT / "output" / "pdf" / "A2" / "Module_03" / "Slovak_A2_Tema_3_4_Narechiya_i_ih_sravnenie.pdf"
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
BODY = ParagraphStyle("Body", fontName="Arial", fontSize=8.9, leading=11.7, textColor=INK, spaceAfter=3.2 * mm)
SMALL = ParagraphStyle("Small", parent=BODY, fontSize=7.7, leading=9.6, spaceAfter=1.75 * mm)
TINY = ParagraphStyle("Tiny", parent=BODY, fontSize=6.95, leading=8.55, spaceAfter=1.05 * mm)
TITLE = ParagraphStyle("Title", fontName="Arial-Bold", fontSize=20, leading=24, textColor=colors.white, alignment=TA_LEFT, spaceAfter=5 * mm)
SUBTITLE = ParagraphStyle("Subtitle", fontName="Arial", fontSize=11.5, leading=15, textColor=colors.HexColor("#FFD8EB"), spaceAfter=5 * mm)
H1 = ParagraphStyle("H1", fontName="Arial-Bold", fontSize=15.5, leading=18.5, textColor=PLUM, spaceBefore=1 * mm, spaceAfter=3.2 * mm)
H2 = ParagraphStyle("H2", fontName="Arial-Bold", fontSize=10.8, leading=13.4, textColor=PINK, spaceBefore=1.5 * mm, spaceAfter=1.6 * mm)
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


def styled_table(data, widths, font_size=7.25, header=True):
    converted = []
    for row_index, row in enumerate(data):
        style = ParagraphStyle(
            f"Cell{row_index}_{font_size}_{len(data)}", parent=SMALL, fontSize=font_size, leading=font_size + 1.9,
            textColor=colors.white if header and row_index == 0 else INK,
            fontName="Arial-Bold" if header and row_index == 0 else "Arial", spaceAfter=0,
        )
        converted.append([p(str(cell), style) for cell in row])
    table = Table(converted, colWidths=widths, repeatRows=1 if header else 0)
    commands = [
        ("GRID", (0, 0), (-1, -1), 0.45, ROSE), ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4.2), ("RIGHTPADDING", (0, 0), (-1, -1), 4.2),
        ("TOPPADDING", (0, 0), (-1, -1), 3.2), ("BOTTOMPADDING", (0, 0), (-1, -1), 3.2),
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
        canvas.drawString(20 * mm, height - 12 * mm, "A2 3.4  |  Наречия и их сравнение")
    canvas.setFont("Arial", 8)
    canvas.setFillColor(MUTED)
    canvas.drawString(20 * mm, 9 * mm, "SlovoKrok | личный учебный модуль")
    canvas.drawRightString(width - 20 * mm, 9 * mm, f"стр. {page} / 7")
    canvas.restoreState()


doc = BaseDocTemplate(
    str(OUTPUT), pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=20 * mm, bottomMargin=18 * mm,
    title="Slovak A2 - Тема 3.4 - Наречия и их сравнение", author="SlovoKrok",
)
frame = Frame(20 * mm, 18 * mm, 170 * mm, 257 * mm, id="main", leftPadding=0, rightPadding=0)
doc.addPageTemplates([PageTemplate(id="series", frames=[frame], onPage=draw_page)])

story = [
    p("МОДУЛЬ 3  •  ПРИЛАГАТЕЛЬНЫЕ, МЕСТОИМЕНИЯ И ЧИСЛИТЕЛЬНЫЕ", COVER_KICKER),
    p("Наречия<br/>и их сравнение", TITLE),
    p("Príslovky a ich stupňovanie", SUBTITLE),
    Spacer(1, 34 * mm),
    p("Наречие описывает действие или обстоятельство: как человек говорит, где он живёт и насколько хорошо что-то получается. На A2 важно ещё уметь сравнивать эти действия.", BODY),
    p("После модуля вы сможете:", H2),
    styled_table([
        ["1", "отличать признак предмета от способа действия: rýchly / rýchlo"],
        ["2", "образовывать частотные наречия от прилагательных"],
        ["3", "сравнивать действия: dobre - lepšie - najlepšie, ďaleko - ďalej"],
        ["4", "точно дозировать признак словами trochu, dosť и veľmi"],
    ], [12 * mm, 158 * mm], font_size=7.35, header=False),
    Spacer(1, 3 * mm),
    box("<b>Главная формула:</b> глагол + наречие; сравнение: komparatív + <b>ako</b>; максимум: <b>naj-</b> + komparatív.", PALE, PINK),
    PageBreak(),

    p("1. Прилагательное или наречие?", H1),
    p("Прилагательное согласуется с существительным. Наречие относится к глаголу, не имеет рода, числа или падежа и отвечает прежде всего на вопросы <b>ako? kde? nakoľko?</b>", BODY),
    styled_table([
        ["Прилагательное", "Наречие", "Что меняется"],
        ["rýchly vlak", "Vlak ide rýchlo.", "быстрый поезд / поезд едет быстро"],
        ["dobrá učiteľka", "Učiteľka vysvetľuje dobre.", "хорошая учительница / объясняет хорошо"],
        ["tichá hudba", "Hudba hrá ticho.", "тихая музыка / играет тихо"],
        ["presný údaj", "Prišiel presne o ôsmej.", "точные данные / пришёл ровно в восемь"],
        ["bezpečná cesta", "Šoféruje bezpečne.", "безопасная дорога / ведёт безопасно"],
    ], [50 * mm, 61 * mm, 59 * mm], font_size=6.4),
    p("Частотные пары", H2),
    styled_table([
        ["Прилагательное", "Наречие", "Перевод наречия"],
        ["pomalý", "pomaly", "медленно"],
        ["ľahký", "ľahko", "легко"],
        ["ťažký", "ťažko", "трудно, тяжело"],
        ["pokojný", "pokojne", "спокойно"],
        ["pekný", "pekne", "красиво, хорошо"],
        ["správny", "správne", "правильно"],
    ], [57 * mm, 48 * mm, 65 * mm], font_size=6.55),
    box("<b>Не выводите форму механически:</b> окончания <b>-o</b> и <b>-e</b> частотны, но выбор зависит от слова. Учите пару целиком: <b>dobrý - dobre, ľahký - ľahko</b>.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    PageBreak(),

    p("2. Как сравнивать способ действия", H1),
    p("Сравнительная степень наречия часто заканчивается на <b>-šie / -ejšie</b>. Превосходная степень образуется добавлением <b>naj-</b> к сравнительной форме.", BODY),
    styled_table([
        ["1-я степень", "2-я степень", "3-я степень", "Перевод"],
        ["rýchlo", "rýchlejšie", "najrýchlejšie", "быстро - быстрее - быстрее всего"],
        ["pomaly", "pomalšie", "najpomalšie", "медленно - медленнее - медленнее всего"],
        ["ticho", "tichšie", "najtichšie", "тихо - тише - тише всего"],
        ["presne", "presnejšie", "najpresnejšie", "точно - точнее - точнее всего"],
        ["bezpečne", "bezpečnejšie", "najbezpečnejšie", "безопасно - безопаснее - безопаснее всего"],
        ["lacno", "lacnejšie", "najlacnejšie", "дёшево - дешевле - дешевле всего"],
    ], [35 * mm, 42 * mm, 47 * mm, 46 * mm], font_size=6.2),
    p("Неправильные и особые частотные ряды", H2),
    styled_table([
        ["1-я", "2-я", "3-я", "Значение"],
        ["dobre", "lepšie", "najlepšie", "хорошо - лучше - лучше всего"],
        ["zle", "horšie", "najhoršie", "плохо - хуже - хуже всего"],
        ["málo", "menej", "najmenej", "мало - меньше - меньше всего"],
        ["veľa", "viac", "najviac", "много - больше - больше всего"],
        ["ďaleko", "ďalej", "najďalej", "далеко - дальше - дальше всего"],
    ], [37 * mm, 39 * mm, 42 * mm, 52 * mm], font_size=6.35),
    box("<b>Опора на 3.3:</b> принцип тот же, но форма другая: <b>lepší plán</b> - лучший план, зато <b>plán funguje lepšie</b> - план работает лучше.", PALE, ROSE, SMALL),
    PageBreak(),

    p("3. Ako, расстояние и интенсивность", H1),
    p("Сравнивая два действия или обстоятельства, ставьте <b>ako</b>. Наречие не согласуется с исполнителем: форма остаётся одной и той же.", BODY),
    styled_table([
        ["Модель", "Пример и перевод"],
        ["глагол + komparatív + ako", "Eva pracuje rýchlejšie ako Peter. - Ева работает быстрее Петера."],
        ["место + komparatív + ako", "Bývame ďalej od centra ako vy. - Мы живём дальше от центра, чем вы."],
        ["изменение состояния", "Dnes sa cítim lepšie ako včera. - Сегодня я чувствую себя лучше, чем вчера."],
        ["максимум в группе", "Zuzana vysvetľuje najlepšie zo všetkých. - Зузана объясняет лучше всех."],
    ], [55 * mm, 115 * mm], font_size=6.55),
    p("Три уровня интенсивности", H2),
    styled_table([
        ["Слово", "Смысл", "Пример"],
        ["trochu", "немного", "Hovorí trochu pomaly. - Он говорит немного медленно."],
        ["dosť", "довольно / достаточно", "Pracuje dosť rýchlo. - Он работает довольно быстро."],
        ["veľmi", "очень", "Vysvetľuje veľmi dobre. - Она объясняет очень хорошо."],
    ], [30 * mm, 46 * mm, 94 * mm], font_size=6.75),
    p("Сравнительная форма усиливается иначе", H2),
    box("С базовой формой: <b>veľmi dobre</b>. Со сравнительной: <b>oveľa lepšie</b> или <b>omnoho lepšie</b>. Сочетание *veľmi lepšie в нейтральной речи не используйте.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    box("<b>Dosť</b> зависит от ситуации: <b>dosť rýchlo</b> может значить и довольно быстро, и достаточно быстро. Контекст показывает оценку говорящего.", PALE, ROSE, SMALL),
    PageBreak(),

    p("4. Живые модели в контексте", H1),
    p("Наречие помогает оценить действие, результат, расстояние и интенсивность. Смотрите на глагол, а не на род исполнителя.", BODY),
    styled_table([
        ["SK", "RU"],
        ["Peter hovorí pomaly a jasne.", "Петер говорит медленно и ясно."],
        ["Mária píše veľmi presne.", "Мария пишет очень точно."],
        ["Deti sa hrajú dosť ticho.", "Дети играют довольно тихо."],
        ["Túto úlohu vyriešime ľahko.", "Мы легко решим эту задачу."],
        ["Dnes pracujem pokojnejšie ako včera.", "Сегодня я работаю спокойнее, чем вчера."],
        ["Nový program funguje lepšie.", "Новая программа работает лучше."],
        ["Po oprave auto ide bezpečnejšie.", "После ремонта машина едет безопаснее."],
        ["Cesta autobusom trvá dlhšie.", "Поездка на автобусе длится дольше."],
        ["Oni bývajú ďalej od školy.", "Они живут дальше от школы."],
        ["Kto odpovedal najpresnejšie?", "Кто ответил точнее всех?"],
        ["Tento obchod predáva najlacnejšie.", "Этот магазин продаёт дешевле всех."],
        ["Teraz tomu rozumiem oveľa lepšie.", "Теперь я понимаю это намного лучше."],
    ], [86 * mm, 84 * mm], font_size=5.95),
    p("Мини-диалог: выбираем дорогу", H2),
    box("<b>A:</b> Ktorou cestou sa dostaneme <b>rýchlejšie</b>? - По какой дороге мы доберёмся быстрее?<br/><b>B:</b> Cez centrum, ale tam sa ide <b>pomalšie</b>. - Через центр, но там едут медленнее.<br/><b>A:</b> Je obchvat <b>ďalej</b>? - Объездная дорога дальше?<br/><b>B:</b> Áno, no zvyčajne sa po ňom ide <b>plynulejšie</b>. - Да, но по ней обычно едут плавнее.<br/><b>A:</b> Tak pôjdeme tadiaľ. Chcem prísť <b>čo najskôr</b>. - Тогда поедем там. Я хочу приехать как можно раньше.", PALE, ROSE, TINY),
    p("<b>Čo naj-</b> означает как можно: <b>čo najskôr, čo najpresnejšie, čo najbezpečnejšie</b>.", SMALL),
    PageBreak(),

    p("5. Частые ошибки и упражнения", H1),
    box("<b>Частые ошибки:</b> *pracuje rýchly -> <b>pracuje rýchlo</b>; *viac dobre -> <b>lepšie</b>; *najviac rýchlo -> <b>najrýchlejšie</b>; *veľmi lepšie -> <b>oveľa lepšie</b>; *býva ďalekejšie -> <b>býva ďalej</b>.", CREAM, colors.HexColor("#E7C76C"), TINY),
    p("Упражнение 1. Выберите прилагательное или наречие", H2),
    p("1) rýchly / rýchlo vlak; 2) vlak ide rýchly / rýchlo; 3) dobrá / dobre odpoveď; 4) odpovedá dobrá / dobre; 5) bezpečná / bezpečne cesta.", TINY),
    p("Упражнение 2. Образуйте наречие", H2),
    p("1) pomalý; 2) ľahký; 3) pokojný; 4) presný; 5) správny.", TINY),
    p("Упражнение 3. Образуйте 2-ю и 3-ю степень", H2),
    p("1) rýchlo; 2) ticho; 3) dobre; 4) zle; 5) ďaleko.", TINY),
    p("Упражнение 4. Добавьте trochu, dosť или veľmi", H2),
    p("1) Я понимаю очень хорошо. 2) Он говорит немного медленно. 3) Дети играют довольно тихо.", TINY),
    p("Упражнение 5. Исправьте ошибки", H2),
    p("1) Mária pracuje rýchla. 2) Dnes sa cítim viac dobre. 3) Bývame ďalekejšie ako vy. 4) On vysvetľuje veľmi lepšie. 5) Kto odpovedal najviac presne?", TINY),
    p("Упражнение 6. Свой мини-текст", H2),
    p("Сравните два способа учиться, работать или ехать в 5-7 предложениях. Используйте два обычных наречия, две сравнительные формы, один максимум с naj- и два слова интенсивности.", TINY),
    PageBreak(),

    p("6. Ответы и проверка мастерства", H1),
    p("Ответы", H2),
    p("<b>1.</b> rýchly vlak; vlak ide rýchlo; dobrá odpoveď; odpovedá dobre; bezpečná cesta.", TINY),
    p("<b>2.</b> pomaly; ľahko; pokojne; presne; správne.", TINY),
    p("<b>3.</b> rýchlejšie - najrýchlejšie; tichšie - najtichšie; lepšie - najlepšie; horšie - najhoršie; ďalej - najďalej.", TINY),
    p("<b>4.</b> Rozumiem veľmi dobre. Hovorí trochu pomaly. Deti sa hrajú dosť ticho.", TINY),
    p("<b>5.</b> Mária pracuje rýchlo. Dnes sa cítim lepšie. Bývame ďalej ako vy. On vysvetľuje oveľa lepšie. Kto odpovedal najpresnejšie?", TINY),
    p("<b>6. Модель:</b> Autom cestujem rýchlo, ale vlakom cestujem pokojnejšie. Vo vlaku môžem veľmi dobre pracovať. Auto ide trochu rýchlejšie, keď nie je premávka. Vlak však jazdí pravidelnejšie. Ráno býva auto dosť pomalé. Preto sa do centra dostanem najpohodlnejšie vlakom. Возможны другие естественные варианты.", TINY),
    p("Итог в четырёх пунктах", H2),
    styled_table([
        ["OK", "Различаю rýchly vlak и vlak ide rýchlo."],
        ["OK", "Строю -šie / -ejšie и добавляю naj- к сравнительной форме."],
        ["OK", "Знаю dobre - lepšie - najlepšie и ďaleko - ďalej - najďalej."],
        ["OK", "Различаю trochu, dosť, veľmi и усиливаю сравнение через oveľa."],
    ], [12 * mm, 158 * mm], font_size=6.85, header=False),
    Spacer(1, 2.2 * mm),
    box("<b>Финальная проверка:</b> без таблицы сравните, как вы добираетесь в два места, где находится каждое и насколько удобно ехать. Используйте <b>ako</b>, <b>ďalej</b>, <b>lepšie</b> и одно слово интенсивности.", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    p("Следующий шаг", H2),
    p("В теме 3.5 вы систематизируете личные местоимения в косвенных падежах и порядок кратких форм.", SMALL),
]

doc.build(story)
print(OUTPUT)
