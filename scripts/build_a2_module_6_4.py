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
OUTPUT = ROOT / "output/pdf/A2/Module_06/Slovak_A2_Tema_6_4_Ustroystva_fayly_i_prilozheniya.pdf"
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
BODY = ParagraphStyle("Body", fontName="Arial", fontSize=8.65, leading=11.3, textColor=INK, spaceAfter=2.7 * mm)
SMALL = ParagraphStyle("Small", parent=BODY, fontSize=7.45, leading=9.2, spaceAfter=1.4 * mm)
TINY = ParagraphStyle("Tiny", parent=BODY, fontSize=6.65, leading=8.1, spaceAfter=0.9 * mm)
TITLE = ParagraphStyle("Title", fontName="Arial-Bold", fontSize=20, leading=24, textColor=colors.white, alignment=TA_LEFT, spaceAfter=5 * mm)
SUBTITLE = ParagraphStyle("Subtitle", fontName="Arial", fontSize=11.5, leading=15, textColor=colors.HexColor("#FFD8EB"), spaceAfter=5 * mm)
H1 = ParagraphStyle("H1", fontName="Arial-Bold", fontSize=15.5, leading=18.5, textColor=PLUM, spaceBefore=1 * mm, spaceAfter=3 * mm)
H2 = ParagraphStyle("H2", fontName="Arial-Bold", fontSize=10.7, leading=13.2, textColor=PINK, spaceBefore=1.1 * mm, spaceAfter=1.4 * mm)
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
        canvas.drawString(20 * mm, height - 12 * mm, "A2 6.4  |  Устройства, файлы и приложения")
    canvas.setFont("Arial", 8)
    canvas.setFillColor(MUTED)
    canvas.drawString(20 * mm, 9 * mm, "SlovoKrok | личный учебный модуль")
    canvas.drawRightString(width - 20 * mm, 9 * mm, f"стр. {page_number} / 7")
    canvas.restoreState()


doc = BaseDocTemplate(
    str(OUTPUT), pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm,
    topMargin=20 * mm, bottomMargin=18 * mm,
    title="Slovak A2 - Тема 6.4 - Устройства, файлы и приложения",
    author="SlovoKrok",
)
doc.addPageTemplates([
    PageTemplate(id="series", frames=[Frame(20 * mm, 18 * mm, 170 * mm, 257 * mm, id="main", leftPadding=0, rightPadding=0)], onPage=draw_page)
])


story = [
    p("МОДУЛЬ 6  •  ДОМ, ИНТЕРНЕТ И ПОКУПКИ", KICK),
    p("Устройства, файлы<br/>и приложения", TITLE),
    p("Zariadenia, súbory a aplikácie: объясняем цифровой процесс шаг за шагом", SUBTITLE),
    Spacer(1, 41 * mm),
    p("Хорошая цифровая инструкция на уровне A2 должна быть короткой, последовательной и проверяемой. Называйте действие, объект и место на экране, а затем показывайте, какой результат должен появиться."),
    p("После модуля вы сможете:", H2),
    table([
        ["1", "понимать основные действия с устройством и файлом"],
        ["2", "давать инструкции с вежливым императивом"],
        ["3", "выбирать вид для процесса и завершённого шага"],
        ["4", "связывать шаги и выполнять инструкцию на слух"],
    ], [12 * mm, 158 * mm], 7.2, False),
    Spacer(1, 3 * mm),
    box("<b>Формула инструкции:</b> najprv действие + объект; potom следующий шаг; ak нужно, проверка; nakoniec видимый результат."),
    PageBreak(),

    p("1. Устройство, экран и файл", H1),
    p("Связывайте глагол с точным объектом. Это помогает понять инструкцию даже тогда, когда интерфейс устройства немного отличается."),
    table([
        ["Действие", "Сочетание", "Перевод"],
        ["zapnúť / vypnúť", "zapnúť telefón", "включить / выключить телефон"],
        ["otvoriť / zavrieť", "otvoriť aplikáciu", "открыть / закрыть приложение"],
        ["vybrať", "vybrať fotografiu", "выбрать фотографию"],
        ["uložiť", "uložiť súbor do priečinka", "сохранить файл в папку"],
        ["stiahnuť", "stiahnuť dokument", "скачать документ"],
        ["priložiť", "priložiť súbor k správe", "прикрепить файл к сообщению"],
        ["zdieľať", "zdieľať odkaz", "поделиться ссылкой"],
    ], [35 * mm, 70 * mm, 65 * mm], 5.65),
    p("Где искать элемент", H2),
    table([
        ["Фраза", "Перевод"],
        ["v pravom hornom rohu", "в правом верхнем углу"],
        ["v dolnej časti obrazovky", "в нижней части экрана"],
        ["v priečinku Stiahnuté", "в папке Загрузки"],
        ["vedľa názvu súboru", "рядом с названием файла"],
        ["pod tlačidlom Uložiť", "под кнопкой Сохранить"],
    ], [78 * mm, 92 * mm], 6.0),
    box("<b>Точная фраза:</b> <i>Ťuknite na ikonu v pravom hornom rohu.</i> - Нажмите на значок в правом верхнем углу. На компьютере чаще говорят <i>kliknite</i>, на сенсорном экране - <i>ťuknite</i>.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    PageBreak(),

    p("2. Императив: один ясный шаг", H1),
    p("Для вежливой инструкции одному человеку используйте форму 2-го лица множественного числа. Она подходит и для обращения к группе."),
    table([
        ["Инфинитив", "Вежливая команда", "Перевод"],
        ["otvoriť", "Otvorte aplikáciu.", "Откройте приложение."],
        ["kliknúť", "Kliknite na tlačidlo Pridať.", "Нажмите кнопку Добавить."],
        ["vybrať", "Vyberte správny súbor.", "Выберите нужный файл."],
        ["zadať", "Zadajte názov dokumentu.", "Введите название документа."],
        ["uložiť", "Uložte zmeny.", "Сохраните изменения."],
        ["počkať", "Počkajte na potvrdenie.", "Дождитесь подтверждения."],
    ], [32 * mm, 76 * mm, 62 * mm], 5.75),
    p("Отрицательная инструкция", H2),
    table([
        ["Ситуация", "Фраза"],
        ["не закрывать", "Nezatvárajte aplikáciu počas sťahovania."],
        ["не удалять", "Nevymazávajte pôvodný súbor."],
        ["не нажимать снова", "Neklikajte na tlačidlo druhýkrát."],
    ], [48 * mm, 122 * mm], 6.0),
    p("Проверка понимания", H2),
    box("После важного шага добавьте проверку: <i>Keď sa zobrazí zelená značka, súbor je uložený.</i> - Когда появится зелёный значок, файл сохранён. Если результат не появился: <i>Ak sa nič nezobrazí, skúste to znova.</i>", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    PageBreak(),

    p("3. Вид и порядок действий", H1),
    p("Несовершенный вид называет процесс или повтор. Совершенный вид ведёт к завершённому шагу. В инструкции чаще нужен результат: открыть, выбрать, сохранить, отправить."),
    table([
        ["Процесс / повтор", "Результат", "Пример результата"],
        ["sťahovať", "stiahnuť", "Stiahnite súbor do telefónu."],
        ["ukladať", "uložiť", "Uložte fotografiu do priečinka."],
        ["pripájať", "pripojiť", "Pripojte dokument k správe."],
        ["inštalovať", "nainštalovať", "Nainštalujte aplikáciu."],
        ["posielať", "poslať", "Pošlite hotový súbor."],
    ], [52 * mm, 44 * mm, 74 * mm], 5.7),
    p("Связки последовательности", H2),
    table([
        ["Связка", "Роль", "Пример"],
        ["najprv", "первый шаг", "Najprv otvorte aplikáciu."],
        ["potom", "следующий шаг", "Potom vyberte fotografiu."],
        ["neskôr", "более поздний этап", "Neskôr môžete zmeniť názov."],
        ["nakoniec", "последний результат", "Nakoniec súbor uložte."],
    ], [30 * mm, 48 * mm, 92 * mm], 5.9),
    p("Модель: прикрепить фотографию", H2),
    box("<b>Najprv otvorte správu.</b> Potom ťuknite na ikonu kancelárskej sponky. Vyberte možnosť Fotografia a označte správny obrázok. Počkajte, kým sa zobrazí náhľad. Nakoniec ťuknite na tlačidlo Odoslať.", PALE, ROSE, SMALL),
    PageBreak(),

    p("4. Полная инструкция и уточнение", H1),
    p("Полная инструкция содержит цель, 4-6 шагов и заметный финальный результат. Если собеседник потерялся, уточните последний выполненный шаг, а не повторяйте всё с начала."),
    p("Как сохранить документ в PDF", H2),
    table([
        ["Шаг", "Инструкция"],
        ["1", "Najprv otvorte dokument v počítači."],
        ["2", "Potom kliknite na Súbor a vyberte možnosť Tlačiť."],
        ["3", "V zozname tlačiarní vyberte Uložiť ako PDF."],
        ["4", "Kliknite na Uložiť a zadajte názov súboru."],
        ["5", "Vyberte priečinok Dokumenty a potvrďte uloženie."],
        ["6", "Nakoniec skontrolujte, či sa súbor dá otvoriť."],
    ], [15 * mm, 155 * mm], 6.0),
    p("Мини-диалог", H2),
    box("<b>A:</b> Otvoril som dokument, ale nevidím možnosť PDF.<br/><b>B:</b> Klikol si už na Súbor?<br/><b>A:</b> Áno, teraz vidím možnosť Tlačiť.<br/><b>B:</b> Dobre. Vyber Uložiť ako PDF a potom klikni na Uložiť.<br/><b>A:</b> Kam mám súbor uložiť?<br/><b>B:</b> Ulož ho do priečinka Dokumenty. Nakoniec ho otvor a skontroluj.", PALE, ROSE, SMALL),
    p("Полезные уточнения", H2),
    table([
        ["SK", "RU"],
        ["Ktorý krok ste už urobili?", "Какой шаг вы уже выполнили?"],
        ["Čo sa zobrazuje na obrazovke?", "Что отображается на экране?"],
        ["Skúste aplikáciu zavrieť a znovu otvoriť.", "Попробуйте закрыть и снова открыть приложение."],
    ], [88 * mm, 82 * mm], 5.75),
    PageBreak(),

    p("5. Частые ошибки и упражнения", H1),
    box("<b>Частые ошибки:</b> несколько действий в одном длинном предложении; процесс вместо завершённого шага; нет объекта или места на экране; пропущена проверка результата; шаги перечислены без связок.", CREAM, colors.HexColor("#E7C76C"), TINY),
    p("Упражнение 1. Соедините действие и объект", H2),
    p("1) otvoriť; 2) uložiť; 3) priložiť; 4) zdieľať. Объекты: a) odkaz; b) aplikáciu; c) súbor k správe; d) dokument do priečinka.", TINY),
    p("Упражнение 2. Образуйте вежливый императив", H2),
    p("1) vybrať súbor; 2) kliknúť na tlačidlo; 3) zadať názov; 4) počkať na potvrdenie.", TINY),
    p("Упражнение 3. Выберите вид", H2),
    p("1) Každý deň ___ fotografie. (ukladám/uložím) 2) Teraz ___ tento súbor. (sťahujem/stiahnem) 3) Najprv ___ aplikáciu. (inštalujte/nainštalujte) 4) Nakoniec dokument ___. (posielajte/pošlite)", TINY),
    p("Упражнение 4. Расставьте шаги", H2),
    p("a) súbor odošlite; b) otvorte správu; c) vyberte fotografiu; d) ťuknite na sponku. Добавьте najprv, potom и nakoniec.", TINY),
    p("Упражнение 5. Контролируемое аудирование", H2),
    p("Не смотрите на аудиоскрипт на странице 7. Попросите другого человека или синтезатор речи прочитать его два раза. Запишите: цель, четыре действия по порядку и финальную проверку.", TINY),
    p("Упражнение 6. Дайте свою инструкцию", H2),
    p("Напишите 6-8 предложений: как скачать файл, переименовать его и переместить в нужную папку. Используйте четыре формы императива, одну видовую пару и три связки порядка.", TINY),
    PageBreak(),

    p("6. Ответы, аудиоскрипт и проверка", H1),
    p("Ответы", H2),
    p("<b>1.</b> 1-b: otvoriť aplikáciu; 2-d: uložiť dokument do priečinka; 3-c: priložiť súbor k správe; 4-a: zdieľať odkaz.", TINY),
    p("<b>2.</b> Vyberte súbor. Kliknite na tlačidlo. Zadajte názov. Počkajte na potvrdenie.", TINY),
    p("<b>3.</b> 1) ukladám; 2) sťahujem; 3) nainštalujte; 4) pošlite.", TINY),
    p("<b>4.</b> Najprv otvorte správu. Potom ťuknite na sponku a vyberte fotografiu. Nakoniec súbor odošlite.", TINY),
    p("<b>5.</b> Цель - сохранить фотографию в отдельную папку. Порядок: открыть приложение Galéria; выбрать фотографию; нажать Presunúť; выбрать папку Dovolenka; проверить фотографию в новой папке.", TINY),
    p("<b>6. Модель:</b> Najprv otvorte priečinok Stiahnuté. Potom vyberte súbor a kliknite na Premenovať. Zadajte nový názov a zmenu potvrďte. Neskôr kliknite na Presunúť a vyberte priečinok Dokumenty. Nakoniec súbor otvorte a skontrolujte. Возможны другие естественные варианты.", TINY),
    p("Аудиоскрипт к упражнению 5", H2),
    box("Najprv otvorte aplikáciu Galéria. Potom vyberte fotografiu, ktorú chcete uložiť. Ťuknite na tri bodky a vyberte možnosť Presunúť. Otvorte priečinok Dovolenka a presun potvrďte. Nakoniec priečinok otvorte a skontrolujte, či je fotografia na novom mieste.", PALE, ROSE, TINY),
    p("Итог в четырёх пунктах", H2),
    table([
        ["OK", "Называю действие, объект и место на экране."],
        ["OK", "Использую вежливый императив и нужный вид."],
        ["OK", "Связываю шаги словами najprv, potom, nakoniec."],
        ["OK", "Проверяю видимый результат последнего шага."],
    ], [12 * mm, 158 * mm], 6.05, False),
    p("Следующий шаг: в теме 6.5 вы будете оставлять голосовое сообщение и писать личное или рабочее письмо.", SMALL),
]

doc.build(story)
print(OUTPUT)
