<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/hero-dark.svg">
    <img src="assets/hero-light.svg" width="100%" alt="Максим Грачев — аналитик данных. Python, SQL, визуализация. Превращаю сырые данные в выводы, на которые можно опираться при принятии решений. Рабочий процесс: 01 данные — сбор и валидация; 02 анализ — гипотезы и статистика; 03 решение — панель и рекомендации.">
  </picture>
</p>

<p align="center">
  <a href="https://t.me/Grachev_M"><img alt="Telegram: @Grachev_M" src="https://img.shields.io/badge/Telegram-%40Grachev__M-FFB020?style=flat-square&logo=telegram&logoColor=0D1117&labelColor=101A2B"></a>
  <a href="https://1notlov3.github.io/Airport-It-Analytics/dashboard/"><img alt="Живая интерактивная панель проекта Airport-It-Analytics" src="https://img.shields.io/badge/%D0%96%D0%B8%D0%B2%D0%B0%D1%8F%20%D0%BF%D0%B0%D0%BD%D0%B5%D0%BB%D1%8C-%D0%B0%D1%8D%D1%80%D0%BE%D0%BF%D0%BE%D1%80%D1%82-3ED8C6?style=flat-square&labelColor=101A2B"></a>
</p>

**Аналитик данных.** Превращаю сырые данные в выводы, на которые можно опираться
при принятии решений: от построения датасета и проверки гипотез — до наглядной
визуализации и рекомендаций.

🎓 Студент бакалавриата по направлению **«Прикладная информатика» (09.03.03)**,
профиль **«Искусственный интеллект и анализ данных»** — Московский университет
имени С. Ю. Витте.

---

## 🗂 Проекты

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/projects-dark.svg">
    <img src="assets/projects-light.svg" width="100%" alt="Табло проектов: Airport-It-Analytics — аналитика, Python и SQL; Boltushka24 — фулстек, Next.js и Supabase; my-portfolio — фронтенд, React; aura-voice-landing — лендинг, HTML, CSS, JS.">
  </picture>
</p>

| Проект | Что это | Стек |
| --- | --- | --- |
| **[Airport-It-Analytics](https://github.com/1notlov3/Airport-It-Analytics)**<br>[→ живая панель](https://1notlov3.github.io/Airport-It-Analytics/dashboard/) | Полный цикл аналитики IT-поддержки аэропорта: 33 309 обращений, SLA, влияние инцидентов на рейсы | Python · pandas · SQL · Jupyter |
| **[Boltushka24](https://github.com/1notlov3/Boltushka24)**<br>[→ boltushka24.vercel.app](https://boltushka24.vercel.app) | Мессенджер для сообществ: серверы и каналы, личные сообщения, реалтайм, голос и видео, совместный просмотр YouTube | Next.js · React · TypeScript · Supabase · Prisma · LiveKit |
| **[my-portfolio](https://github.com/1notlov3/my-portfolio)**<br>[→ демо](https://1notlov3.github.io/my-portfolio/) | Личный сайт-портфолио: разделы о себе, навыках и проектах | React · JavaScript · CSS |
| **[aura-voice-landing](https://github.com/1notlov3/aura-voice-landing)** | Лендинг Aura — голосового AI-трекера калорий | HTML · CSS · JavaScript |

---

## ✈️ Разбор: аналитика аэропорта

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/proof-dark.svg">
    <img src="assets/proof-light.svg" width="100%" alt="Аналитика IT-поддержки аэропорта: 33 309 обращений за два года. 31% срывов первичной реакции сосредоточены в пиковые часы; связь нагрузки службы с расписанием рейсов r = 0,5; ≈655 задержанных рейсов в год.">
  </picture>
</p>

Полный цикл аналитики на **33 309 обращений** за два года: от генерации
реалистичных данных до интерактивной панели и рекомендаций для руководства.

- 🔍 нашёл узкое место сервиса: **31% срывов первичной реакции**, сосредоточенных в пиковые часы;
- 📈 связал нагрузку службы с расписанием рейсов (**r = 0,5**) — нагрузку можно прогнозировать;
- 💸 оценил операционную цену инцидентов: **≈655 задержанных рейсов в год**;
- 📊 собрал **[живую интерактивную панель](https://1notlov3.github.io/Airport-It-Analytics/dashboard/)** — открой, она интерактивная.

**Стек:** Python (pandas, matplotlib, seaborn) · SQL (SQLite, оконные функции, CTE) · Jupyter · Chart.js

---

## 💬 Разбор: Boltushka24

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/boltushka-dark.svg">
    <img src="assets/boltushka-light.svg" width="100%" alt="Boltushka24 — мессенджер сообществ. Реалтайм: броадкаст шлёт только id и действие, контент идёт через авторизованный API. Оптимистичный интерфейс: сообщение видно сразу с временным id, потом подменяется реальным. Права: роли ADMIN, MODERATOR и GUEST проверяются в одном слое.">
  </picture>
</p>

Фулстек-мессенджер для сообществ, доведённый до продакшена:
**[boltushka24.vercel.app](https://boltushka24.vercel.app)**. Серверы и каналы,
личные сообщения, реалтайм, голосовые и видеокомнаты, совместный просмотр
YouTube, роли и права, PWA с офлайн-очередью.

Три решения, которыми проект интересен инженерно:

- 🔒 **Реалтайм без утечек.** Supabase Realtime рассылает только `{ id, action }`, а сам контент клиент дозапрашивает через авторизованные API-роуты — приватные сообщения не уходят в публичный броадкаст;
- ⚡ **Оптимистичная отправка.** Сообщение появляется мгновенно с временным id и подменяется реальным после ответа сервера — интерфейс не ждёт сеть;
- 🛡 **Права в одном слое.** Роли `ADMIN` / `MODERATOR` / `GUEST` проверяются централизованно, а не дублируются по коду, поэтому поведение предсказуемо.

**Стек:** Next.js · React · TypeScript · Tailwind · Supabase (Postgres, Realtime, Storage) · Prisma · Clerk · LiveKit · TanStack Query · Vercel

---

## 🛠 Инструменты

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/toolkit-dark.svg">
    <img src="assets/toolkit-light.svg" width="100%" alt="Инструменты. Язык и анализ: Python, pandas, NumPy. Визуализация: Matplotlib, seaborn, Chart.js. Данные: SQL, SQLite, Excel. Среда: Jupyter, Git, VS Code.">
  </picture>
</p>

**Язык и анализ:** Python · pandas · NumPy · **Визуализация:** Matplotlib · seaborn · Chart.js ·
**Данные:** SQL · SQLite · Excel · **Среда:** Jupyter · Git · VS Code

---

## 🎯 Сейчас в фокусе

- статистика и A/B-тесты;
- продвинутый SQL (оптимизация запросов, аналитические функции);
- второй аналитический проект в портфолио.

---

## 📊 Статистика

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://github-readme-stats.vercel.app/api?username=1notlov3&show_icons=true&locale=ru&hide_border=true&rank_icon=percentile&bg_color=0D1117&title_color=FFB020&icon_color=3ED8C6&text_color=8B99AE">
    <img height="165" alt="Статистика GitHub пользователя 1notlov3" src="https://github-readme-stats.vercel.app/api?username=1notlov3&show_icons=true&locale=ru&hide_border=true&rank_icon=percentile&bg_color=FFFFFF&title_color=A65F00&icon_color=0B8C7F&text_color=59667A">
  </picture>
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://github-readme-stats.vercel.app/api/top-langs/?username=1notlov3&layout=compact&locale=ru&hide_border=true&hide=html,css,scss,astro&bg_color=0D1117&title_color=FFB020&text_color=8B99AE">
    <img height="165" alt="Языки в репозиториях пользователя 1notlov3" src="https://github-readme-stats.vercel.app/api/top-langs/?username=1notlov3&layout=compact&locale=ru&hide_border=true&hide=html,css,scss,astro&bg_color=FFFFFF&title_color=A65F00&text_color=59667A">
  </picture>
</p>

---

## 📫 Как связаться

- Telegram: [@Grachev_M](https://t.me/Grachev_M)
