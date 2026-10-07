# SlovoKrok

[Русский](README.md) · [English](README.en.md) · **Slovenčina**

[GitHub](https://github.com/Eobart96/SlovoKrok)

Lokálna aplikácia pre jedného používateľa na učenie slovenčiny. Kurz A1 má
8 modulov a 83 tém, vysvetlenia v ruštine, cvičenia, čítanie, domáce úlohy,
slovník a precvičovanie chýb. Preklady README nemenia jazyk aplikácie.

## Inštalácia vo Windows

Potrebujete **Python 3.12+**, **Node.js 22+** a internet na inštaláciu závislostí.
Pri inštalácii Pythonu zapnite pridanie do PATH. Git je voliteľný.

1. Stiahnite a rozbaľte ZIP repozitára alebo ho naklonujte:

   ```powershell
   git clone https://github.com/Eobart96/SlovoKrok.git
   cd SlovoKrok
   ```

2. V priečinku projektu spustite `install.cmd` na inštaláciu závislostí.
3. Spustite `start.cmd`. Prehliadač otvorí http://127.0.0.1:3000/.
4. Otvorte **Настройки → Задания → Добавить базовый пакет** a pridajte základné úlohy.

`doctor.cmd` slúži na diagnostiku, `stop.cmd` na zastavenie aplikácie.
ZIP obsahuje zdrojový kód, nie samostatný inštalátor. Spúšťacie skripty sú
určené pre Windows. Nasadenie na verejný server nie je podporované.

## Základný balík úloh

Každá z 83 tém A1 obsahuje **20 cvičení, 2 texty na čítanie a 2 domáce úlohy**.
Spolu je to 1660 cvičení, 166 textov a 166 domácich úloh bez mien, osobného
profilu, odpovedí používateľa a hodnotení.
Úlohy sú dostupné po dokončení príslušnej témy. Opätovné pridanie balíka
preskočí rovnaké úlohy a zachová pokrok.

[Stiahnuť JSON](frontend/public/task-packs/slovokrok-a1-basic-v1.json) ·
[Zdroje balíka a jeho zostavenie](course-content/basic-task-pack/README.md).

## Pridané funkcie

- Úvodný sprievodca, ktorý možno znova otvoriť tlačidlom pomocníka.
- Uloženie pozície v sekciách a návrat k poslednému cvičeniu, textu alebo domácej úlohe.
- Lokálna kontrola úloh s presnými vzorovými odpoveďami aj v online režime.
- Zaznamenanie chyby, vysvetlenie, precvičenie a upevnenie vedomostí.
- Diktovanie prerozprávania textu. Online hodnotenie pomocou AI posudzuje význam
  a zohľadňuje chyby rozpoznávania reči aj slovenské slová v ruskom prejave.
  Rozpoznávanie reči závisí od prehliadača a internetu.
- Voliteľný profil na prispôsobenie príkladov; nastavenie témy a veľkosti textu.
- Hlásenia chýb s kontextom obrazovky, snímkou obrazovky, exportom ZIP a vymazaním zoznamu.
- Prenos úloh cez JSON, správa úloh a zálohovanie pokroku.
- 72 študijných PDF A2; interaktívny pilot A2 zatiaľ nie je sprístupnený.

Sekcie: učenie → prehľady pravidiel → cvičenia → domáce úlohy → čítanie → chyby
→ slovíčka. Rozhranie a výučbové vysvetlenia sú zatiaľ v ruštine.

## AI a osobné údaje

Lekcie a základný balík fungujú bez poskytovateľa AI. Úlohy s presným vzorom
sa kontrolujú lokálne. Offline hodnotenie otvorených odpovedí je približné.
Hodnotenie významu a tvorba nových úloh vyžadujú vlastný Codex CLI alebo
poskytovateľa kompatibilného s OpenAI API; používanie API môže byť platené.
Poskytovateľa vyberte v nastaveniach. `.env` je voliteľný; pozrite `.env.example`.
Voliteľný profil sa odosiela AI iba so súhlasom.

Vo Windows sa údaje ukladajú do `%LOCALAPPDATA%\SlovoKrok`, mimo repozitára.
Zdrojový kód neobsahuje databázu, kľúče API ani pokrok autora.
Nový priečinok aplikácie na tom istom počítači používa existujúce údaje.
Na prenos na iný počítač použite zálohu; export samotných úloh neobsahuje
odpovede ani hodnotenia. Aplikácia nemá účty ani cloudovú synchronizáciu.

## Aktualizácia

1. V nastaveniach vytvorte zálohu a zastavte aplikáciu cez `stop.cmd`.
2. Pri inštalácii cez Git spustite v priečinku projektu `git pull --ff-only`.
   Najprv si uložte vlastné zmeny kódu; nepoužívajte vynútený reset.
   Pri inštalácii zo ZIP rozbaľte novú verziu do nového priečinka.
3. Znova spustite `install.cmd` a potom `start.cmd`.
4. Podľa potreby pridajte základný balík; rovnaké úlohy sa preskočia.

## Štruktúra a stav projektu

`frontend/`: Next.js, React, TypeScript a obsah kurzu.
`backend/`: FastAPI, SQLAlchemy, SQLite a integrácia AI.
`course-content/`: metodika a upraviteľné zdroje balíka.
`output/pdf/A2/`: PDF A2. `scripts/`: spúšťanie a overovanie.
`.github/`: CI a šablóny spätnej väzby. `docs/`: technická dokumentácia.

Ide o verziu na testovanie. Moduly 7–8 ešte čakajú na úplné ručné schválenie.
Inštalácia na čistom počítači a ručné schválenie aktuálneho rozhrania nie sú
potvrdené. Prihlasovanie, viacerí používatelia a verejné nasadenie nie sú súčasťou tejto verzie.

[Príručka pre testerov (po rusky)](TESTING_START.md) · [Novinky](UPDATES.md) ·
[Architektúra](docs/ARCHITECTURE.md) · [API](docs/API.md) ·
[Údaje](docs/DATABASE.md) · [Overovanie](docs/TESTING.md) · [Bezpečnosť](SECURITY.md).

## Licencia

[MIT](LICENSE).
