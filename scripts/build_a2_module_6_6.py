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
OUTPUT = ROOT / "output/pdf/A2/Module_06/Slovak_A2_Tema_6_6_Sotsialnye_seti_i_tsifrovaya_bezopasnost.pdf"
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
        canvas.drawString(20 * mm, height - 12 * mm, "A2 6.6  |  Социальные сети и цифровая безопасность")
    canvas.setFont("Arial", 8)
    canvas.setFillColor(MUTED)
    canvas.drawString(20 * mm, 9 * mm, "SlovoKrok | личный учебный модуль")
    canvas.drawRightString(width - 20 * mm, 9 * mm, f"стр. {page_number} / 7")
    canvas.restoreState()


doc = BaseDocTemplate(
    str(OUTPUT), pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm,
    topMargin=20 * mm, bottomMargin=18 * mm,
    title="Slovak A2 - Тема 6.6 - Социальные сети и цифровая безопасность",
    author="SlovoKrok",
)
doc.addPageTemplates([
    PageTemplate(id="series", frames=[Frame(20 * mm, 18 * mm, 170 * mm, 257 * mm, id="main", leftPadding=0, rightPadding=0)], onPage=draw_page)
])


story = [
    p("МОДУЛЬ 6  •  ДОМ, ИНТЕРНЕТ И ПОКУПКИ", KICK),
    p("Социальные сети<br/>и цифровая безопасность", TITLE),
    p("Sociálne siete a digitálna bezpečnosť: привычки, совет и помощь со входом", SUBTITLE),
    Spacer(1, 41 * mm),
    p("На уровне A2 важно не только назвать действие в сети, но и объяснить привычку, дать простой безопасный совет и описать проблему так, чтобы поддержка могла помочь."),
    p("После модуля вы сможете:", H2),
    table([
        ["1", "рассказать, что вы делаете и не делаете онлайн"],
        ["2", "различать niekto / nikto, niečo / nič и похожие пары"],
        ["3", "связать части фразы местоимением ktorý"],
        ["4", "дать совет и решить простую проблему со входом"],
    ], [12 * mm, 158 * mm], 7.2, False),
    Spacer(1, 3 * mm),
    box("<b>Формула безопасной помощи:</b> описать проблему + назвать сообщение на экране + предложить один безопасный шаг + проверить результат."),
    PageBreak(),

    p("1. Онлайн-привычки: что я делаю", H1),
    p("Для рассказа о привычках используйте настоящее время и слова частоты. Не перегружайте ответ техническими словами: действие, частота и причина уже дают связный A2-текст."),
    table([
        ["Действие", "Пример", "Перевод"],
        ["sledovať", "Sledujem správy na internete.", "Я слежу за новостями в интернете."],
        ["zverejniť", "Fotografie zverejňujem zriedka.", "Я редко публикую фотографии."],
        ["komentovať", "Niekedy komentujem príspevky.", "Иногда я комментирую публикации."],
        ["zdieľať", "Odkazy zdieľam iba s priateľmi.", "Я делюсь ссылками только с друзьями."],
        ["sledovať profil", "Tento profil sledujem každý deň.", "Я слежу за этим профилем каждый день."],
        ["nastaviť súkromie", "Súkromie kontrolujem každý mesiac.", "Я проверяю приватность каждый месяц."],
    ], [35 * mm, 72 * mm, 63 * mm], 5.65),
    p("Слова частоты и ограничения", H2),
    table([
        ["SK", "RU", "Пример"],
        ["často", "часто", "Často si čítam komentáre."],
        ["niekedy", "иногда", "Niekedy odpovedám na správy."],
        ["zriedka", "редко", "Zriedka pridávam verejné príspevky."],
        ["iba", "только", "Osobné údaje posielam iba rodine."],
        ["nikdy", "никогда", "Nikdy nezdieľam heslo."],
    ], [30 * mm, 35 * mm, 105 * mm], 5.7),
    box("<b>Практический минимум:</b> используйте уникальный пароль, включите двухфакторную проверку, проверяйте настройки приватности и не отправляйте никому код подтверждения.", GREEN, colors.HexColor("#A8D5B3"), SMALL),
    PageBreak(),

    p("2. Niekto или nikto: кто-то или никто", H1),
    p("Формы с <b>nie-</b> обозначают неопределённого человека, предмет, место или время. Формы с <b>ni-</b> дают отрицательное значение и требуют отрицательного глагола."),
    table([
        ["Неопределённо", "Отрицательно", "Контраст"],
        ["niekto - кто-то", "nikto - никто", "Niekto mi písal. / Nikto mi nepísal."],
        ["niečo - что-то", "nič - ничто", "Niečo som zverejnil. / Nič som nezverejnil."],
        ["niekde - где-то", "nikde - нигде", "Niekde je chyba. / Nikde nevidím chybu."],
        ["niekedy - иногда", "nikdy - никогда", "Niekedy píšem komentár. / Nikdy neurážam ľudí."],
    ], [45 * mm, 43 * mm, 82 * mm], 5.55),
    p("Отрицательное согласование", H2),
    box("По-словацки отрицательное местоимение и глагол отрицательны вместе: <i>Nikto mi <b>ne</b>napísal. Nič som <b>ne</b>otvoril. Nikde som heslo <b>ne</b>uložil. Nikdy <b>ne</b>posielajte overovací kód.</i>", PALE, ROSE, SMALL),
    p("Типичные ситуации", H2),
    table([
        ["Ситуация", "Фраза"],
        ["неизвестный запрос", "Niekto mi poslal žiadosť o priateľstvo."],
        ["нет ответа", "Nikto mi ešte neodpovedal."],
        ["подозрительная ссылка", "Niečo na tomto odkaze nie je v poriadku."],
        ["код не вводили", "Nikde som nezadal overovací kód."],
        ["правило", "Nikdy neposielam heslo cez správu."],
    ], [52 * mm, 118 * mm], 5.8),
    box("<b>Ошибка:</b> <i>Nikto mi písal.</i> Правильно: <i>Nikto mi nepísal.</i> Русского одного отрицания здесь недостаточно.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    PageBreak(),

    p("3. Ktorý и совет mal by som", H1),
    p("Относительное местоимение <i>ktorý</i> соединяет информацию без повтора. Оно согласуется с существительным, а падеж зависит от роли внутри второй части."),
    table([
        ["Форма", "Модель", "Перевод"],
        ["ktorý", "Profil, ktorý sledujem, je užitočný.", "Профиль, за которым я слежу, полезный."],
        ["ktorú", "Stránka, ktorú si otvoril, je falošná.", "Страница, которую ты открыл, поддельная."],
        ["ktoré", "Heslo, ktoré používam, je jedinečné.", "Пароль, который я использую, уникален."],
        ["ktoré", "Správy, ktoré dostávam, kontrolujem.", "Сообщения, которые я получаю, я проверяю."],
        ["ktorému", "Človek, ktorému dôverujem, mi pomohol.", "Человек, которому я доверяю, мне помог."],
    ], [27 * mm, 87 * mm, 56 * mm], 5.45),
    p("Мягкий совет", H2),
    p("Модель <i>mal by som + infinitív</i> означает, что действие желательно. Форма меняется по роду и лицу; отрицание ставится на <i>mal</i>.", SMALL),
    table([
        ["Кому", "Совет", "Перевод"],
        ["мужчина о себе", "Mal by som si zmeniť heslo.", "Мне следует сменить пароль."],
        ["женщина о себе", "Mala by som skontrolovať účet.", "Мне следует проверить аккаунт."],
        ["другу", "Mal by si zapnúť dvojfaktorové overenie.", "Тебе следует включить 2FA."],
        ["вежливо", "Mali by ste kontaktovať podporu.", "Вам следует обратиться в поддержку."],
        ["не делать", "Nemali by ste otvárať podozrivý odkaz.", "Не следует открывать подозрительную ссылку."],
    ], [34 * mm, 83 * mm, 53 * mm], 5.45),
    box("<b>Порядок:</b> <i>Mal by som si zmeniť heslo.</i> Частицы <i>by som</i> и короткое <i>si</i> стоят рано; не переносите их в конец предложения.", CREAM, colors.HexColor("#E7C76C"), SMALL),
    PageBreak(),

    p("4. Проблема со входом и онлайн-комментарий", H1),
    p("Безопасная помощь не просит пароль или код. Сначала уточните, что видно на экране, затем используйте официальный сайт или приложение."),
    p("Пять безопасных шагов", H2),
    table([
        ["Шаг", "Действие"],
        ["1", "Skontrolujte adresu stránky alebo názov oficiálnej aplikácie."],
        ["2", "Ak ste zabudli heslo, obnovte ho cez oficiálnu stránku."],
        ["3", "Vytvorte si nové jedinečné heslo a zapnite dvojfaktorové overenie."],
        ["4", "Ak máte podozrenie, že niekto napadol účet, odhláste sa na ostatných zariadeniach."],
        ["5", "Nikomu neposielajte heslo ani jednorazový overovací kód."],
    ], [15 * mm, 155 * mm], 5.8),
    p("Мини-диалог", H2),
    box("<b>A:</b> Nemôžem sa prihlásiť. Prišla mi správa s odkazom.<br/><b>B:</b> Zobrazuje sa ti nejaké upozornenie?<br/><b>A:</b> Áno, stránka odo mňa žiada overovací kód.<br/><b>B:</b> Na ten odkaz by si nemal klikať. Otvor oficiálnu aplikáciu a zmeň si heslo.<br/><b>A:</b> Mám sa odhlásiť aj na notebooku?<br/><b>B:</b> Áno. Potom zapni dvojfaktorové overenie.", PALE, ROSE, SMALL),
    p("Модель онлайн-комментария", H2),
    box("Sociálne siete používam každý deň, ale verejne zverejňujem iba niektoré fotografie. Nikdy nepíšem adresu ani telefónne číslo do komentára. Profily, ktoré nepoznám, nesledujem. Ak mi niekto pošle podozrivý odkaz, neotvorím ho. Každý by si mal kontrolovať súkromie a používať jedinečné heslo.", PALE, ROSE, SMALL),
    PageBreak(),

    p("5. Частые ошибки и упражнения", H1),
    box("<b>Частые ошибки:</b> nikto без отрицательного глагола; неизменяемое ktorý; жёсткое musíte вместо мягкого совета; пароль или код в сообщении; расплывчатая просьба без текста ошибки и безопасного следующего шага.", CREAM, colors.HexColor("#E7C76C"), TINY),
    p("Упражнение 1. Выберите подходящую форму", H2),
    p("1) Niekto/Nikto mi poslal žiadosť. 2) Niekto/Nikto mi neodpovedal. 3) Niečo/Nič na stránke nefunguje. 4) Niekedy/Nikdy nezdieľam heslo. Проверьте, нужно ли отрицание у глагола.", TINY),
    p("Упражнение 2. Вставьте ktorý / ktorú / ktoré / ktorému", H2),
    p("1) Profil, ___ sledujem. 2) Stránka, ___ som otvoril. 3) Heslo, ___ používam. 4) Človek, ___ dôverujem.", TINY),
    p("Упражнение 3. Дайте мягкий совет", H2),
    p("Преобразуйте: 1) Zmeň si heslo. 2) Zapnite 2FA. 3) Neotváraj ten odkaz. 4) Kontaktujte podporu. Используйте mal by si / mali by ste.", TINY),
    p("Упражнение 4. Исправьте опасные советы", H2),
    p("1) Pošli mi svoje heslo. 2) Klikni na odkaz v neznámej správe. 3) Pošli overovací kód kamarátovi. 4) Používaj rovnaké heslo všade.", TINY),
    p("Упражнение 5. Ответьте поддержке", H2),
    p("Сообщите в 4 фразах: вы не можете войти; видите текст Nesprávne heslo; ссылку из сообщения не открывали; просите безопасную инструкцию.", TINY),
    p("Упражнение 6. Напишите онлайн-комментарий", H2),
    p("Напишите 6-8 предложений о своих привычках. Используйте два слова nie-/ni-, одну фразу с ktorý, один совет с mal by и одно правило безопасности.", TINY),
    PageBreak(),

    p("6. Ответы и итоговая проверка", H1),
    p("Ответы", H2),
    p("<b>1.</b> 1) Niekto mi poslal žiadosť. 2) Nikto mi neodpovedal. 3) Niečo na stránke nefunguje. 4) Nikdy nezdieľam heslo.", TINY),
    p("<b>2.</b> 1) ktorý; 2) ktorú; 3) ktoré; 4) ktorému.", TINY),
    p("<b>3.</b> 1) Mal by si si zmeniť heslo. 2) Mali by ste zapnúť dvojfaktorové overenie. 3) Nemal by si otvárať ten odkaz. 4) Mali by ste kontaktovať podporu.", TINY),
    p("<b>4.</b> Например: Nikomu neposielaj heslo. Neklikaj na odkaz v neznámej správe. Nikomu neposielaj overovací kód. Pre každý účet používaj jedinečné heslo.", TINY),
    p("<b>5.</b> Dobrý deň, nemôžem sa prihlásiť do svojho účtu. Zobrazuje sa mi hlásenie Nesprávne heslo. Odkaz zo správy som neotvoril. Mohli by ste mi, prosím, poslať bezpečný postup na obnovenie hesla?", TINY),
    p("<b>6. Модель:</b> Sociálne siete používam každý deň, ale niekedy si dám prestávku. Nikdy nezverejňujem svoju adresu. Ak mi niekto pošle žiadosť, najprv si pozriem profil. Správy, ktoré vyzerajú podozrivo, neotváram. Každý by si mal zapnúť dvojfaktorové overenie. Nikomu neposielam svoje heslo ani kód. Возможны другие естественные варианты.", TINY),
    p("Итог в четырёх пунктах", H2),
    table([
        ["OK", "Описываю онлайн-привычки и частоту."],
        ["OK", "Согласую отрицательное местоимение с глаголом."],
        ["OK", "Связываю информацию формами ktorý."],
        ["OK", "Даю мягкий и безопасный совет без запроса пароля или кода."],
    ], [12 * mm, 158 * mm], 6.0, False),
    p("Следующий шаг: в теме 6.7 вы будете просить нужное количество и понимать этикетку или короткую инструкцию о товаре.", SMALL),
]

doc.build(story)
print(OUTPUT)
