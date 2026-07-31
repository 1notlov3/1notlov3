<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/hero-dark.svg">
    <img src="assets/hero-light.svg" width="100%" alt="Максим Грачев, специалист поддержки интеграций, вторая линия, Москва. Разбираю эскалации по внутренним системам компании и довожу проблему до причины. Рабочий процесс: 01 эскалация — приём и триаж; 02 локализация — логи, API, SQL; 03 фикс — правка и автоматизация. Вторая линия поддержки: REST API, SQL, JSON, XML, Python, PowerShell.">
  </picture>
</p>

<p align="center">
  <a href="https://t.me/Grachev_M"><img alt="Telegram: @Grachev_M" src="https://img.shields.io/badge/Telegram-%40Grachev__M-FFB020?style=flat-square&logo=telegram&logoColor=0D1117&labelColor=101A2B"></a>
  <a href="resume/maksim-grachev-cv.pdf"><img alt="Резюме в PDF" src="https://img.shields.io/badge/%D0%A0%D0%B5%D0%B7%D1%8E%D0%BC%D0%B5-PDF-E9EEF7?style=flat-square&labelColor=101A2B"></a>
  <a href="https://1notlov3.github.io/Airport-It-Analytics/dashboard/"><img alt="Живая интерактивная панель проекта Airport-It-Analytics" src="https://img.shields.io/badge/%D0%96%D0%B8%D0%B2%D0%B0%D1%8F%20%D0%BF%D0%B0%D0%BD%D0%B5%D0%BB%D1%8C-%D0%B0%D1%8D%D1%80%D0%BE%D0%BF%D0%BE%D1%80%D1%82-3ED8C6?style=flat-square&labelColor=101A2B"></a>
</p>

**Специалист поддержки интеграций, вторая линия.** Разбираю эскалации по
внутренним системам компании: локализую сбой между приложением, базой данных,
сетью и внешними интеграциями и довожу проблему до причины — даже когда она не
на моей стороне.

Работаю с REST API, SQL, JSON и XML. Пишу на PowerShell и Python внутренние
инструменты автоматизации — самый большой из них, **AdminTools**, разобран
ниже.

🎓 Учусь на бакалавриате **«Прикладная информатика» (09.03.03)**, профиль
**«Искусственный интеллект и анализ данных»**, в Московском университете имени
С. Ю. Витте.

---

## 🧰 Разбор: AdminTools

Утилита техподдержки под Windows. Специалист вводит имя ПК — или ФИО, логин,
телефон, кабинет, что угодно — получает карточку машины и одним кликом выполняет
над ней любое из **26 действий**: подключение по RDP, установка принтера, работа
со службами, процессами и сеансами пользователя. Вместо прохода по нескольким
разным консолям — одно окно.

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/admintools-ui-dark.svg">
    <img src="assets/admintools-ui-light.svg" width="100%" alt="Схема интерфейса AdminTools. Строка поиска: имя ПК, ФИО, логин, телефон или кабинет — ищет в Active Directory и в локальной истории. Слева карточка машины PC-0412: пользователь, телефон, кабинет, ОС, адрес, источник данных. Справа плитка действий: подключиться по RDP, установить принтер, службы и процессы, диск и очистка, сеанс пользователя, установка ПО, и ещё 20 действий из Config.psd1. Внизу: опрос сети идёт в пуле runspace на 8 потоков, окно остаётся отзывчивым.">
  </picture>
</p>

Написана на **PowerShell 5.1 и WPF** и работает только на штатных компонентах
Windows: ни сторонних библиотек, ни `.exe`, ни RSAT — разворачивается там, где
поставить что-то дополнительное нельзя.

### Что внутри

- 🧭 **Поиск на двух ногах.** **Active Directory** и локальная накопительная
  история: программа запоминает каждый просмотренный ПК вместе с пользователем,
  телефоном и кабинетом, поэтому со временем находит машину даже по обрывку
  данных и не зависит от внешних источников;
- ⚡ **Ничего не зависает.** Вся работа с сетью уходит в **пул runspace**,
  результаты забирает таймер. В потоке интерфейса нет ни одного `DoEvents` и ни
  одного `Start-Sleep` — окно остаётся отзывчивым даже при опросе недоступной
  машины;
- 🗣 **Честность вместо видимости работы.** Недоступен сервер, лежит домен, не
  хватает дистрибутива — программа говорит об этом прямо и продолжает делать то,
  что может. Ошибки уходят в журнал, а не в пустой `catch`;
- 🖼 **Интерфейс на векторе.** Разметка только сетками, поэтому окно корректно
  тянется при DPI 125% и 150%. Иконки — контуры в нотации SVG, а не глифы
  шрифта: масштабируются без потерь и перекрашиваются под тему. Тёмная и светлая
  темы переключаются на лету;
- ⚙️ **Всё настраивается без правки кода.** Пути, списки служб и сами 26 действий
  лежат в `Config.psd1`.

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/admintools-arch-dark.svg">
    <img src="assets/admintools-arch-light.svg" width="100%" alt="Данные: Active Directory для поиска объекта в домене, локальная накопительная история с ПК, пользователем, телефоном и кабинетом, работает автономно. Выполнение: пул runspace, таймер собирает результат, без DoEvents и Start-Sleep. Интерфейс: разметка на сетках и корректный вид при DPI 125% и 150%, иконки контурами SVG, тёмная и светлая темы на лету. Только штатные компоненты Windows — без сторонних библиотек, .exe и RSAT; пути и все 26 действий описаны в Config.psd1.">
  </picture>
</p>

### Принтеры одним кликом

Отдельный экран: фильтр по каталогу, выбор принтера, кнопка «Подключить» — и
дальше программа сама ставит драйвер, перезапускает диспетчер печати, подключает
принтер пользователю и проверяет результат. Специалисту не нужно помнить
последовательность и держать открытыми оснастки.

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/admintools-printers-dark.svg">
    <img src="assets/admintools-printers-light.svg" width="100%" alt="Схема экрана печати AdminTools: фильтр по размещению, каталог принтеров, кнопка «Подключить». Таблица: принтер, размещение, драйвер, статус. Порядок действий: установка драйвера, перезапуск спулера, подключение пользователю, проверка результата.">
  </picture>
</p>

> Экраны выше — схемы интерфейса, а не снимки рабочего окна: AdminTools —
> внутренний инструмент, его содержимое наружу не выносится. Имена машин,
> принтеров и людей на схемах вымышленные.

**Стек:** PowerShell 5.1 · WPF · Active Directory · runspace pool · `Config.psd1`

---

## 🗂 Проекты

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/projects-dark.svg">
    <img src="assets/projects-light.svg" width="100%" alt="Табло проектов: AdminTools, внутренний инструмент, 26 операций над удалёнными ПК, PowerShell, WPF, Active Directory; Airport-It-Analytics, аналитика, Python и SQL; Boltushka24, фулстек, Next.js и Supabase; my-portfolio, фронтенд, React.">
  </picture>
</p>

| Проект | Что это | Стек |
| --- | --- | --- |
| **AdminTools**<br>внутренний инструмент | Утилита техподдержки: поиск ПК по имени, ФИО, логину, телефону или кабинету и 26 действий над машиной | PowerShell 5.1 · WPF · Active Directory |
| **[Airport-It-Analytics](https://github.com/1notlov3/Airport-It-Analytics)**<br>[→ живая панель](https://1notlov3.github.io/Airport-It-Analytics/dashboard/) | Учебная аналитика IT-поддержки аэропорта на сгенерированном датасете: 33 309 обращений, SLA, влияние инцидентов на рейсы | Python · pandas · SQL · Jupyter |
| **[Boltushka24](https://github.com/1notlov3/Boltushka24)**<br>[→ boltushka24.vercel.app](https://boltushka24.vercel.app) | Мессенджер для сообществ: серверы и каналы, личные сообщения, реалтайм, голос и видео, совместный просмотр YouTube | Next.js · React · TypeScript · Supabase · Prisma · LiveKit |
| **[my-portfolio](https://github.com/1notlov3/my-portfolio)**<br>[→ демо](https://1notlov3.github.io/my-portfolio/) | Личный сайт-портфолио: разделы о себе, навыках и проектах | React · JavaScript · CSS |
| **[aura-voice-landing](https://github.com/1notlov3/aura-voice-landing)** | Лендинг Aura, голосового AI-трекера калорий | HTML · CSS · JavaScript |

---

## ✈️ Разбор: аналитика аэропорта

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/proof-dark.svg">
    <img src="assets/proof-light.svg" width="100%" alt="Аналитика IT-поддержки аэропорта: 33 309 обращений за два года. 31% срывов первичной реакции сосредоточены в пиковые часы; связь нагрузки службы с расписанием рейсов r = 0,5; ≈655 задержанных рейсов в год.">
  </picture>
</p>

Учебный проект на **сгенерированном датасете**: смоделировал работу IT-поддержки
аэропорта, **33 309 обращений** за два года, проверил гипотезы, собрал панель и
написал рекомендации. Данные синтетические — с реальными обращениями
работодателя проект не связан.

- 🔍 нашёл узкое место сервиса: **31% срывов первичной реакции**, сосредоточенных в пиковые часы;
- 📈 связал нагрузку службы с расписанием рейсов (**r = 0,5**), поэтому её можно прогнозировать по расписанию;
- 💸 оценил операционную цену инцидентов: **≈655 задержанных рейсов в год**;
- 📊 собрал **[интерактивную панель](https://1notlov3.github.io/Airport-It-Analytics/dashboard/)**, её можно открыть в браузере.

**Стек:** Python (pandas, matplotlib, seaborn) · SQL (SQLite, оконные функции, CTE) · Jupyter · Chart.js

---

## 💬 Разбор: Boltushka24

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/boltushka-dark.svg">
    <img src="assets/boltushka-light.svg" width="100%" alt="Boltushka24, мессенджер сообществ. Реалтайм: шлю только id и действие, контент клиент забирает через авторизованный API. Оптимистичная отправка: показываю сообщение с временным id и меняю на реальный после ответа сервера. Права: проверяю роли ADMIN, MODERATOR и GUEST в одном модуле lib/permissions.ts.">
  </picture>
</p>

Фулстек-мессенджер для сообществ. Развернул на
**[boltushka24.vercel.app](https://boltushka24.vercel.app)**. Внутри серверы и
каналы, личные сообщения, реалтайм, голосовые и видеокомнаты, совместный
просмотр YouTube, роли и права, PWA с офлайн-очередью.

Инженерные решения:

- 🔒 **Реалтайм.** Шлю в броадкаст только `{ id, action }`, а контент клиент забирает через авторизованные API-роуты, поэтому приватные сообщения не попадают в публичный канал;
- ⚡ **Оптимистичная отправка.** Показываю сообщение сразу с временным id и меняю на реальный после ответа сервера. Пользователь не ждёт сеть;
- 🛡 **Права.** Проверяю роли `ADMIN`, `MODERATOR` и `GUEST` в одном модуле `lib/permissions.ts`.

**Стек:** Next.js · React · TypeScript · Tailwind · Supabase (Postgres, Realtime, Storage) · Prisma · Clerk · LiveKit · TanStack Query · Vercel

---

## 🧭 Опыт

| Период | Место | Роль |
| --- | --- | --- |
| окт 2025 — н.в. | Домодедово Хендлинг | Ведущий специалист технической поддержки, вторая линия |
| сен 2024 — апр 2025 | ФЦНИВТ СНПО «Элерон» | Старший техник, техническая и проектная документация |
| сен — дек 2023 | S7 IT | Стажёр, виртуальные рабочие места на VMware Horizon |
| сен 2022 — сен 2023 | Фриланс | Веб-разработчик, сайты и интеграции через API |

Полностью — в **[резюме (PDF)](resume/maksim-grachev-cv.pdf)**; исходник вёрстки
лежит рядом, в [`resume/resume.html`](resume/resume.html).

---

## 🛠 Инструменты

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/toolkit-dark.svg">
    <img src="assets/toolkit-light.svg" width="100%" alt="Инструменты. API и данные: HTTP и REST API, JSON и XML, SQL (MS SQL). Код и скрипты: Python, PowerShell, JS/TS и React. Инфраструктура: Windows Server, Active Directory, Linux и VMware. Процессы: Jira и Confluence, Git, база знаний.">
  </picture>
</p>

**API и данные:** HTTP · REST API · JSON · XML · SQL (MS SQL) · Excel ·
**Код и скрипты:** Python · PowerShell 5.1 (WPF) · Bash · JS/TS · React ·
**Инфраструктура:** Windows Server · Active Directory · Linux · VMware Horizon ·
**Процессы:** Jira · Confluence · Git · база знаний

---

## 🎯 Сейчас в фокусе

- перевожу AdminTools на модульную архитектуру: разнести 26 действий по
  отдельным модулям поверх общего пула runspace;
- продвинутый SQL — оптимизация запросов и аналитические функции;
- второй аналитический проект в портфолио.

---

## 📊 Статистика

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/stats-dark.svg">
    <img src="assets/stats-light.svg" width="100%" alt="Статистика профиля GitHub @1notlov3 на 2026-07-31. Публичных репозиториев: 16. Звёзд: 3. Подписчиков: неизвестно. Языки в публичных репозиториях: HTML — 7 из 14 репозиториев, JavaScript — 2 из 14 репозиториев, TypeScript — 1 из 14 репозиториев, Jupyter Notebook — 1 из 14 репозиториев, Astro — 1 из 14 репозиториев.">
  </picture>
</p>

<sub>Баннер собирается из GitHub API скриптом
<a href="assets/stats.py"><code>assets/stats.py</code></a> и обновляется
еженедельно через
<a href=".github/workflows/stats.yml">GitHub Actions</a> — сторонних сервисов
нет, ломаться нечему.</sub>

---

## 📫 Как связаться

- Telegram: [@Grachev_M](https://t.me/Grachev_M)
- Резюме: [PDF](resume/maksim-grachev-cv.pdf)
