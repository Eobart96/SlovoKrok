"use client";

import { useEffect, useRef, useState } from "react";

const welcomeKey = "slovokrok-welcome-v1";
const sections = [
  ["Обучение", "Начните здесь: выберите модуль и тему, прочитайте объяснение и выполните короткую практику."],
  ["Шпаргалки", "Повторяйте правила и сохраняйте свои заметки."],
  ["Упражнения", "Тренируйте завершённые темы. Задания можно создавать по теме, разделу, модулю или прогрессу."],
  ["Домашнее задание", "Пишите ответы на более свободные задания и получайте объяснение результата."],
  ["Чтение", "Читайте словацкий текст и пересказывайте смысл. В поддерживаемом браузере можно надиктовать пересказ."],
  ["Ошибки", "Добавляйте сложные места кнопкой «Записать ошибку», затем разбирайте и повторяйте их."],
  ["Слова", "Повторяйте словарь пройденных тем. Переводчик рядом с настройками помогает с незнакомыми фразами."],
];

export function CourseWelcome({ onStart, onProfile }: { onStart: () => void; onProfile: () => void }) {
  const dialog = useRef<HTMLDialogElement>(null);
  const [step, setStep] = useState(0);
  const [storageError, setStorageError] = useState("");
  const open = () => { setStep(0); dialog.current?.showModal(); };
  useEffect(() => {
    try { if (window.localStorage.getItem(welcomeKey) !== "seen") dialog.current?.showModal(); }
    catch { dialog.current?.showModal(); }
  }, []);
  const finish = (action?: () => void) => {
    try { window.localStorage.setItem(welcomeKey, "seen"); }
    catch { setStorageError("Браузер не запомнил просмотр знакомства. При следующем входе оно может появиться снова."); }
    dialog.current?.close(); action?.();
  };
  return <>
    <button type="button" onClick={open} aria-haspopup="dialog">Как пользоваться</button>
    <dialog ref={dialog} className="course-welcome" aria-labelledby="course-welcome-title" onCancel={(event) => { event.preventDefault(); finish(); }}>
      <div className="course-welcome-heading"><span className="course-welcome-brand">SlovoKrok · знакомство</span><button type="button" className="course-welcome-close" onClick={() => finish()} aria-label="Закрыть знакомство">✕</button></div>
      <div className="course-welcome-progress" aria-label={`Шаг ${step + 1} из 4`}>{[0, 1, 2, 3].map((index) => <span key={index} className={index <= step ? "active" : ""} />)}</div>
      <div className="course-welcome-content" key={step}>
        <p className="course-welcome-eyebrow">{step + 1} / 4</p>
        <h2 id="course-welcome-title">{["Словацкий, шаг за шагом", "Где что находится", "Практика и проверка", "Ваш первый шаг"][step]}</h2>
        {step === 0 && <><p>SlovoKrok — курс словацкого A1 с объяснениями на русском, короткой практикой и работой над ошибками. Сейчас это версия для тестирования: нам важно понять, что понятно, удобно и что стоит исправить.</p><div className="course-welcome-highlight"><strong>Читайте → пробуйте → повторяйте</strong><p>Пройдите тему, закрепите её заданиями и возвращайтесь к трудным местам. Здесь 8 модулей и 83 урока. Материалы A2 пока не доступны в интерфейсе.</p></div><p>Приложение работает на вашем компьютере. Прогресс и задания сохраняются локально — общего аккаунта и облачной синхронизации нет.</p></>}
        {step === 1 && <div className="course-welcome-map">{sections.map(([title, description]) => <article key={title}><h3>{title}</h3><p>{description}</p></article>)}<article><h3>Настройки</h3><p>Профиль «О себе», тема и размер текста, режим проверки, подключение ИИ, перенос заданий и резервная копия.</p></article></div>}
        {step === 2 && <><div className="course-welcome-map"><article><h3>Онлайн</h3><p>Новые задания и свободные ответы используют выбранный ИИ. Задания с точным эталоном проверяются сразу, без запроса к ИИ.</p></article><article><h3>Офлайн</h3><p>Читайте уроки и выполняйте сохранённые задания с эталоном. Проверка свободного текста приблизительная; старым заданиям без эталона нужен ИИ.</p></article><article><h3>О себе</h3><p>Укажите имя и деятельность для примеров. Передача профиля ИИ включается отдельно. Фиксированные тесты и ранее созданные задания сохраняют свои условия.</p></article><article><h3>Продолжение</h3><p>В упражнениях, чтении и домашнем задании кнопка «Вернуться к последнему заданию» возвращает к последней работе.</p></article></div><div className="course-welcome-highlight"><strong>Полезные подсказки: словацкие буквы</strong><p>В полях ответа со словацкой клавиатурой нажмите Alt + букву на её английской клавише: Alt + A → á, Alt + C → č, Alt + S → š. Сочетания работают при русской и английской раскладке.</p><p>Повторное нажатие Alt + A меняет á на ä; Alt + L переключает ĺ / ľ, Alt + O — ó / ô. Для заглавной буквы добавьте Shift. Символы можно также выбрать на экранной клавиатуре под полем ответа.</p></div><p>Для новых заданий подключите свой Codex CLI, OpenAI или Polza в настройках. Внешний ИИ получает текст запроса; API может быть платным. Без подключения можно начать с уроков и встроенной практики.</p></>}
        {step === 3 && <><ol className="course-welcome-steps"><li>Откройте «Обучение» и начните с первой темы.</li><li>В «Настройки → Задания» добавьте базовый пакет: по 20 упражнений, 2 текста и 2 ДЗ на каждую тему. ИИ для добавления не нужен.</li><li>После завершения темы попробуйте её упражнения или чтение. По желанию заполните «О себе».</li><li>Сохраните трудное место в «Ошибки» и повторите его позже.</li></ol><div className="course-welcome-highlight"><strong>Помогите сделать курс лучше</strong><p>Значок сообщения внизу слева открывает обращение. Место ошибки определяется автоматически. Добавьте описание и снимок экрана, скачайте ZIP и отправьте автору. Само приложение ничего не отправляет.</p></div><p>Резервная копия курса находится в настройках. Профиль «О себе» и обращения хранятся отдельно и в неё не входят.</p></>}
      </div>
      <div className="course-welcome-footer"><button type="button" className="course-welcome-secondary" onClick={() => step ? setStep(step - 1) : finish()}>{step ? "Назад" : "Позже"}</button><div>{step === 3 && <button type="button" className="course-welcome-secondary" onClick={() => finish(onProfile)}>Заполнить профиль</button>}<button type="button" className="course-welcome-primary" onClick={() => step < 3 ? setStep(step + 1) : finish(onStart)}>{step < 3 ? "Далее" : "Начать обучение"}</button></div></div>
    </dialog>
    {storageError && <p className="course-welcome-storage" role="status">{storageError}</p>}
  </>;
}
