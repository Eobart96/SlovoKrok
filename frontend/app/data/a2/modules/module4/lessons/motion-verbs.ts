import { defineA2Module4Lesson } from "../lessonFactory";

export const a2MotionVerbsLesson = defineA2Module4Lesson("a2-motion-verbs", {
  "duration": "45–55 мин",
  "goals": [
    "Различать конкретное движение и обычный маршрут",
    "Называть способ передвижения",
    "Использовать прошедшее и будущее движения",
    "Описывать прибытие, посадку, выход и пересадку"
  ],
  "theory": {
    "summary": "Ísť — конкретное направленное движение, chodiť — обычный маршрут, повтор или ходьба вообще. Оба могут описывать поездку на транспорте: способ задают pešo, autobusom, vlakom. Одно будущее перемещение — pôjdem, регулярное — budem chodiť.",
    "rules": [
      "Ísť: idem, ideš, ide, ideme, idete, idú.",
      "Chodiť: chodím, chodíš, chodí, chodíme, chodíte, chodia.",
      "Ísť не означает только идти пешком: idem autobusom — еду автобусом.",
      "Прошедшее ísť: išiel/išla/išli; chodiť: chodil/chodila/chodili.",
      "Будущее ísť: pôjdem, pôjdeš, pôjde, pôjdeme, pôjdete, pôjdu; обычный шаблон не budem ísť.",
      "Направление: do + Genitív, na + Akuzatív, k + Datív; исходная точка z/zo или od + Genitív.",
      "Посадка do autobusu, выход z električky, пересадка na vlak; учим модель вместе с глаголом."
    ],
    "examples": [
      {
        "slovak": "Teraz idem do práce.",
        "russian": "Сейчас я иду / еду на работу.",
        "explanation": "Одно актуальное движение."
      },
      {
        "slovak": "Každý deň chodím do práce vlakom.",
        "russian": "Каждый день я езжу на работу поездом.",
        "explanation": "Привычный маршрут и способ."
      },
      {
        "slovak": "Dnes idem domov pešo.",
        "russian": "Сегодня я иду домой пешком.",
        "explanation": "Pešo уточняет способ."
      },
      {
        "slovak": "Včera som išla do centra.",
        "russian": "Вчера я пошла / поехала в центр.",
        "explanation": "Женский род, конкретное движение."
      },
      {
        "slovak": "Zajtra pôjdeme do Košíc.",
        "russian": "Завтра мы поедем в Кошице.",
        "explanation": "Одно будущее перемещение."
      },
      {
        "slovak": "V zime budem chodiť autobusom.",
        "russian": "Зимой я буду ездить автобусом.",
        "explanation": "Будущая привычка."
      },
      {
        "slovak": "V Trnave prestúpime na vlak.",
        "russian": "В Трнаве мы пересядем на поезд.",
        "explanation": "Завершённый шаг маршрута."
      }
    ]
  },
  "sections": [
    {
      "title": "Движение: одна цель или обычный маршрут",
      "importance": "core",
      "paragraphs": [
        "Kam ideš? — куда ты сейчас идёшь / едешь? Teraz idem do práce — сейчас направляюсь на работу. Kam chodíš cez víkend? — куда обычно ходишь по выходным? Radi chodíme do kina — любим ходить в кино.",
        "В обычной привычке выбираем chodím. Но Každý deň idem... не объявляем всегда неграмматичным: можно описывать конкретный направленный шаг повторяющегося расписания. В заданиях прямо укажем, что нужен обычный маршрут без выделения отдельного выхода."
      ],
      "items": [
        "ísť: idem / ideš / ide / ideme / idete / idú",
        "chodiť: chodím / chodíš / chodí / chodíme / chodíte / chodia"
      ],
      "note": "Ísť/chodiť — два несовершенных глагола, не пара «процесс / готовый результат»."
    },
    {
      "title": "Способ передвижения задаёт дополнение",
      "importance": "core",
      "paragraphs": [
        "Idem domov pešo — иду домой пешком; Do práce chodím autobusom — езжу на работу автобусом; Dnes idem na bicykli — сегодня еду на велосипеде. Сам ísť не сообщает, идёте ли вы пешком.",
        "Radi cestujeme vlakom — любим путешествовать поездом. Cestovať описывает поездку шире, ísť — направленное движение к цели. Rád cestujem po Slovensku — люблю путешествовать по Словакии; Často cestuje do zahraničia — часто ездит за границу."
      ],
      "items": [
        "pešo — пешком",
        "autobusom / vlakom / autom — автобусом / поездом / машиной",
        "na bicykli — на велосипеде"
      ],
      "note": "Средство часто стоит в Inštrumentál без предлога; велосипед — готовая модель na bicykli."
    },
    {
      "title": "Вчера и завтра: išiel и pôjdem",
      "importance": "core",
      "paragraphs": [
        "Včera som išiel/išla pešo — вчера я пошёл/пошла пешком. V detstve som chodil/chodila pešo — в детстве обычно ходил/ходила пешком. Во множественном: Včera sme išli do centra — вчера мы пошли в центр.",
        "Zajtra pôjdem k lekárovi — завтра пойду к врачу. Формы: pôjdem, pôjdeš, pôjde, pôjdeme, pôjdete, pôjdu. Для будущей регулярности: Budem chodiť na kurz dvakrát týždenne — буду ходить на курс два раза в неделю."
      ],
      "items": [
        "один будущий путь: pôjdem",
        "обычный будущий маршрут: budem chodiť",
        "не обычная форма будущего: budem ísť"
      ],
      "note": "Не стройте išiel по обычному отрезанию -ť: форма учится целиком."
    },
    {
      "title": "Шаги поездки и предлоги",
      "importance": "core",
      "paragraphs": [
        "Прибытие: prísť/prichádzať; отправление: odísť/odchádzať. Посадка: nastúpiť/nastupovať; выход: vystúpiť/vystupovať; пересадка: prestúpiť/prestupovať. Первым дан завершённый шаг, вторым процесс или повтор.",
        "Prídem do Bratislavy — приеду в Братиславу; Idem na stanicu — иду на вокзал; Pôjdem k lekárovi — пойду к врачу; Odišla z kancelárie — ушла из офиса; Vraciame sa od rodičov — возвращаемся от родителей. Посадка: nastúpiť do autobusu; выход: vystúpiť z električky; пересадка: prestúpiť na vlak."
      ],
      "items": [
        "do Bratislavy — Genitív",
        "na stanicu — Akuzatív",
        "k lekárovi — Datív",
        "z kancelárie / od rodičov — Genitív"
      ],
      "note": "Не путайте поездку автобусом с посадкой в него; в заданиях тренируем именно данные модели."
    },
    {
      "title": "Маршрут: фон и завершённые шаги",
      "importance": "core",
      "paragraphs": [
        "Zajtra odídem z domu o šiestej. Na stanicu pôjdem pešo. Potom nastúpim do vlaku. V Trnave prestúpim na autobus. V Nitre vystúpim a prídem na univerzitu pred deviatou. — Завтра выйду из дома в шесть, пешком дойду до вокзала, сяду в поезд. В Трнаве пересяду на автобус. В Нитре выйду и приду в университет до девяти.",
        "Keď autobus prichádzal, ľudia už čakali — когда автобус подъезжал, люди уже ждали. Autobus prišiel o šiestej — автобус прибыл в шесть. Vlak ide o siedmej — поезд отправляется в семь; Tento autobus chodí každú hodinu — этот автобус ходит каждый час."
      ],
      "items": [
        "odídem → pôjdem → nastúpim → prestúpim → vystúpim → prídem",
        "процесс прибытия: prichádzal",
        "граница прибытия: prišiel"
      ],
      "note": "Совершенные шаги могут входить и в описание повторяющегося маршрута."
    },
    {
      "title": "Как добираетесь обычно и как поедете завтра",
      "importance": "core",
      "paragraphs": [
        "Eva: Ako chodíš do Nitry? Martin: Zvyčajne cestujem vlakom, ale dnes idem autobusom. Eva: Kedy prídeš? Martin: Prídem asi o tretej. — Как обычно добираешься до Нитры? — Обычно поездом, но сегодня автобусом. — Когда приедешь? — Примерно в три.",
        "Напишите 6–8 предложений: привычный маршрут и завтрашняя поездка. Используйте chodiť, форму ísť, вид транспорта и минимум три шага поездки. Свободный текст проверяем в чате; в коротких заданиях форма, лицо и предлог указаны."
      ],
      "items": [
        "Куда? — do / na / k + нужная форма",
        "Откуда? — z / od + Genitív",
        "Как? — pešo / vlakom / autobusom"
      ],
      "note": "Проверьте направление, способ, время и завершённость каждого шага."
    }
  ],
  "stepPractices": [
    {
      "sectionIndex": 0,
      "type": "text",
      "prompt": "Вставьте chodiť в 1-м лице настоящего для обычного маршрута: Každý deň ___ do práce.",
      "answer": "chodím",
      "showSlovakKeyboard": true,
      "hint": "Целевая модель привычки: chodím.",
      "explanation": "Целевая модель привычки: chodím."
    },
    {
      "sectionIndex": 1,
      "type": "choice",
      "prompt": "Что сообщает Idem autobusom?",
      "options": [
        "Я еду автобусом",
        "Я обязательно иду пешком",
        "Я уже пересел на поезд"
      ],
      "answer": "Я еду автобусом",
      "hint": "Способ выражен autobusom.",
      "explanation": "Способ выражен autobusom."
    },
    {
      "sectionIndex": 2,
      "type": "pairs",
      "prompt": "Введите указанную форму движения.",
      "pairs": [
        {
          "prompt": "ísť: ona, прошедшее, только форма без som",
          "answer": "išla"
        },
        {
          "prompt": "ísť: my, будущее",
          "answer": "pôjdeme"
        },
        {
          "prompt": "chodiť: ja, будущее, оба слова",
          "answer": "budem chodiť"
        }
      ],
      "answer": "išla; pôjdeme; budem chodiť",
      "showSlovakKeyboard": true,
      "hint": "Ísť: išla/pôjdeme; повторное движение: budem chodiť.",
      "explanation": "Ísť: išla/pôjdeme; повторное движение: budem chodiť."
    },
    {
      "sectionIndex": 3,
      "type": "text",
      "prompt": "Заполните оба слова модели «к врачу»: Pôjdeme ___. Используйте k + lekár.",
      "answer": "k lekárovi",
      "showSlovakKeyboard": true,
      "hint": "K требует Datív: lekárovi.",
      "explanation": "K требует Datív: lekárovi."
    },
    {
      "sectionIndex": 3,
      "type": "pairs",
      "prompt": "Заполните предлог и существительное именно по указанной модели.",
      "pairs": [
        {
          "prompt": "посадка: nastúpiť + автобус",
          "answer": "do autobusu"
        },
        {
          "prompt": "выход: vystúpiť + трамвай",
          "answer": "z električky"
        },
        {
          "prompt": "пересадка: prestúpiť + поезд",
          "answer": "na vlak"
        }
      ],
      "answer": "do autobusu; z električky; na vlak",
      "showSlovakKeyboard": true,
      "hint": "Do/z + Genitív; пересадка na + Akuzatív.",
      "explanation": "Do/z + Genitív; пересадка na + Akuzatív."
    },
    {
      "sectionIndex": 4,
      "type": "order",
      "prompt": "Соберите «В Трнаве мы пересядем на поезд»: V Trnave → prestúpime → na vlak.",
      "tokens": [
        "V",
        "Trnave",
        "prestúpime",
        "na",
        "vlak."
      ],
      "answer": "V Trnave prestúpime na vlak.",
      "hint": "Prestúpime — один завершённый шаг.",
      "explanation": "Prestúpime — один завершённый шаг."
    },
    {
      "sectionIndex": 5,
      "type": "text",
      "prompt": "Вставьте prísť в 1-м лице будущего результата: ___ asi o tretej.",
      "answer": "prídem",
      "showSlovakKeyboard": true,
      "hint": "Prísť → prídem; прибытие примерно в три.",
      "explanation": "Prísť → prídem; прибытие примерно в три."
    },
    {
      "sectionIndex": 5,
      "type": "choice",
      "prompt": "Как описать будущую привычку ездить автобусом зимой?",
      "options": [
        "V zime budem chodiť autobusom.",
        "V zime budem ísť autobusom.",
        "V zime som išla autobusom."
      ],
      "answer": "V zime budem chodiť autobusom.",
      "hint": "Для будущей привычки: budem chodiť.",
      "explanation": "Для будущей привычки: budem chodiť."
    }
  ],
  "knowledgeChecks": [
    {
      "question": "Выбирает ли ísť сам по себе движение пешком?",
      "options": [
        "Нет, способ уточняют отдельно",
        "Да, всегда только пешком",
        "Нет, он всегда значит поездку поездом"
      ],
      "answer": "Нет, способ уточняют отдельно",
      "explanation": "Idem pešo и idem autobusom возможны."
    },
    {
      "question": "Какой вопрос относится к конкретному движению?",
      "options": [
        "Kam ideš teraz?",
        "Kam chodíš zvyčajne?",
        "Ako často cestuješ?"
      ],
      "answer": "Kam ideš teraz?",
      "explanation": "Teraz задаёт актуальное направление."
    },
    {
      "question": "Какая модель означает пересадку на поезд?",
      "options": [
        "prestúpiť na vlak",
        "vystúpiť z vlaku",
        "nastúpiť do vlaku"
      ],
      "answer": "prestúpiť na vlak",
      "explanation": "Пересадка, выход и посадка — разные шаги."
    }
  ],
  "finalChecks": [
    {
      "question": "Выберите обычное будущее ísť для «Завтра мы поедем в Кошице».",
      "options": [
        "Zajtra pôjdeme do Košíc.",
        "Zajtra budeme ísť do Košíc.",
        "Včera sme išli do Košíc."
      ],
      "answer": "Zajtra pôjdeme do Košíc.",
      "explanation": "Будущее my: pôjdeme."
    },
    {
      "question": "Как описать посадку в автобус по изученной модели?",
      "options": [
        "Nastúpim do autobusu.",
        "Vystúpim z autobusu.",
        "Prestúpim na vlak."
      ],
      "answer": "Nastúpim do autobusu.",
      "explanation": "Nastúpiť do + Genitív."
    }
  ],
  "vocabulary": [
    {
      "word": "ísť / chodiť",
      "translation": "идти, ехать / ходить, ездить регулярно"
    },
    {
      "word": "pešo",
      "translation": "пешком"
    },
    {
      "word": "autobusom",
      "translation": "автобусом"
    },
    {
      "word": "vlakom",
      "translation": "поездом"
    },
    {
      "word": "na bicykli",
      "translation": "на велосипеде"
    },
    {
      "word": "cestovať",
      "translation": "путешествовать; ездить"
    },
    {
      "word": "do zahraničia",
      "translation": "за границу"
    },
    {
      "word": "prísť / prichádzať",
      "translation": "прибыть / прибывать"
    },
    {
      "word": "odísť / odchádzať",
      "translation": "уйти, уехать / уходить, уезжать"
    },
    {
      "word": "nastúpiť / nastupovať",
      "translation": "сесть в транспорт / садиться"
    },
    {
      "word": "vystúpiť / vystupovať",
      "translation": "выйти из транспорта / выходить"
    },
    {
      "word": "prestúpiť / prestupovať",
      "translation": "пересесть / пересаживаться"
    },
    {
      "word": "stanica",
      "translation": "вокзал; станция"
    },
    {
      "word": "zastávka",
      "translation": "остановка"
    }
  ],
  "assessmentMode": "quiz",
  "chatPrompt": "Попроси 6–8 предложений: обычный маршрут и завтрашняя поездка, chodiť, форма ísť, транспорт и три шага. Проверь pôjdem, išiel/išla, do/na/k/z/od и управление шагов. Не объявляй ísť только пешей ходьбой, не называй ísť/chodiť видовой парой и не запрещай конкретное idem внутри повторяемого расписания. Принимай естественные альтернативы.",
  "chatSuggestions": [
    "Опишу маршрут на работу",
    "Потренируем пересадки",
    "Проверь pôjdem и budem chodiť"
  ]
});
