#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Генератор SVG-баннеров профиля: светлая и тёмная версия каждого.

Собирает hero, projects, toolkit и три экрана AdminTools. Баннеры proof-* и
boltushka-* сделаны раньше вручную и здесь не пересобираются.

    python3 assets/build.py
"""
import os
from xml.sax.saxutils import escape as esc

OUT = os.path.dirname(os.path.abspath(__file__))

MONO = ('ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, '
        '"Liberation Mono", monospace')
SANS = ('system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, '
        '"Helvetica Neue", Arial, sans-serif')

DARK = dict(bg="#0D1117", panel="#101A2B", inner="#0B1421", stroke="#1E2C42",
            rule="#24334A", eyebrow="#8B99AE", title="#E9EEF7", muted="#59667A",
            accent="#FFB020", note="#8B99AE")
LIGHT = dict(bg="#FFFFFF", panel="#0E1726", inner="#0A1220", stroke="#22304A",
             rule="#E1E7F0", eyebrow="#59667A", title="#0B1220", muted="#59667A",
             accent="#A65F00", note="#59667A")

# цвета внутри тёмных панелей одинаковы в обеих темах
BODY = "#93A1B5"
BRIGHT = "#E9EEF7"
AMBER = "#FFB020"
TEAL = "#3ED8C6"


def a(**kw):
    out = []
    for k, v in kw.items():
        if v is None:
            continue
        out.append('%s="%s"' % (k.rstrip("_").replace("_", "-"),
                                esc(str(v), {'"': "&quot;"})))
    return " ".join(out)


def text(x, y, s, *, font=SANS, size=18, weight="400", fill=BODY,
         ls=None, anchor=None, opacity=None):
    return '  <text %s>%s</text>' % (
        a(x=x, y=y, font_family=font, font_size=size, font_weight=weight,
          fill=fill, letter_spacing=ls, text_anchor=anchor, opacity=opacity),
        esc(s))


def rich(x, y, spans, *, font=SANS, size=18, fill=BODY):
    inner = "".join(
        '<tspan %s>%s</tspan>' % (
            a(fill=sp.get("fill"), font_weight=sp.get("weight"),
              font_family=sp.get("font")), esc(sp["t"]))
        for sp in spans)
    return '  <text %s>%s</text>' % (
        a(x=x, y=y, font_family=font, font_size=size, fill=fill), inner)


def rect(x, y, w, h, *, rx=0, fill="none", stroke=None, sw=1, opacity=None):
    return '  <rect %s/>' % a(x=x, y=y, width=w, height=h, rx=rx, fill=fill,
                              stroke=stroke, stroke_width=sw if stroke else None,
                              opacity=opacity)


def line(x1, y1, x2, y2, *, stroke, sw=1, opacity=None):
    return '  <line %s/>' % a(x1=x1, y1=y1, x2=x2, y2=y2, stroke=stroke,
                              stroke_width=sw, opacity=opacity)


def circle(cx, cy, r, *, fill):
    return '  <circle %s/>' % a(cx=cx, cy=cy, r=r, fill=fill)


def svg(w, h, title, desc, body):
    head = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" '
            'width="%d" height="%d" role="img" aria-labelledby="ttl dsc">'
            % (w, h, w, h),
            '  <title id="ttl">%s</title>' % esc(title),
            '  <desc id="dsc">%s</desc>' % esc(desc)]
    return "\n".join(head + body + ['</svg>', ''])


def write(name, w, h, title, desc, builder):
    for suffix, C in (("dark", DARK), ("light", LIGHT)):
        body = [rect(0, 0, w, h, fill=C["bg"])] + builder(C)
        path = os.path.join(OUT, "%s-%s.svg" % (name, suffix))
        with open(path, "w", encoding="utf-8") as f:
            f.write(svg(w, h, title, desc, body))
        print(path)


def eyebrow(C, s, y=58, w=1200):
    return [text(64, y, s, font=MONO, size=17, fill=C["eyebrow"], ls=3.4),
            line(64, y + 18, w - 64, y + 18, stroke=C["rule"])]


# ---------------------------------------------------------------- hero
HERO_W, HERO_H = 1200, 372
HERO_STEPS = [("01", "ЭСКАЛАЦИЯ", " — приём и триаж"),
              ("02", "ЛОКАЛИЗАЦИЯ", " — логи, API, SQL"),
              ("03", "ФИКС", " — правка и автоматизация")]


def hero(C):
    b = [text(64, 100, "IT SUPPORT · 2ND LINE · INTEGRATIONS", font=MONO,
              size=17, fill=C["eyebrow"], ls=3.4),
         text(64, 172, "Максим Грачев", size=58, weight="700", fill=C["title"]),
         rich(64, 212, [{"t": "Поддержка интеграций", "fill": C["accent"],
                         "weight": "700"},
                        {"t": "  ·  вторая линия  ·  Москва"}],
              size=21, fill=C["eyebrow"]),
         text(64, 258, "Разбираю эскалации по внутренним системам", size=20,
              fill=C["eyebrow"]),
         text(64, 286, "аэропорта и довожу проблему до причины.", size=20,
              fill=C["eyebrow"]),
         rect(688, 68, 448, 224, rx=14, fill=C["panel"], stroke=C["stroke"]),
         rect(712, 86, 4, 14, rx=2, fill=TEAL),
         text(726, 98, "WORKFLOW", font=MONO, size=15, weight="700", fill=AMBER,
              ls=2.6),
         line(712, 112, 1112, 112, stroke=C["stroke"])]
    y = 148
    for i, (num, cap, tail) in enumerate(HERO_STEPS):
        b.append(rich(712, y, [{"t": num, "fill": AMBER, "weight": "700",
                                "font": MONO},
                               {"t": "  " + cap, "fill": BRIGHT, "weight": "700"},
                               {"t": tail}], size=18))
        if i < len(HERO_STEPS) - 1:
            b.append(line(712, y + 24, 1112, y + 24, stroke=C["stroke"],
                          opacity=0.7))
        y += 60
    b += [line(64, 316, 1136, 316, stroke=C["rule"]),
          text(64, 346, "Домодедово Хендлинг · 10–15 эскалаций в день · "
                        "REST API · SQL · Python", size=16.5, fill=C["eyebrow"])]
    return b


# ------------------------------------------------------------ projects
PROJ_ROWS = [
    ("AdminTools", "26 операций над удалёнными ПК", "PowerShell · WPF · AD",
     "TOOLING", AMBER),
    ("Airport-It-Analytics", "33 309 обращений, SLA, рейсы",
     "Python · pandas · SQL", "ANALYTICS", TEAL),
    ("Boltushka24", "мессенджер: чаты, голос, видео", "Next.js · Supabase",
     "FULLSTACK", BRIGHT),
    ("my-portfolio", "личный сайт-портфолио на React", "React · CSS",
     "FRONTEND", BODY),
]
PROJ_H = 96 + 46 + 64 * len(PROJ_ROWS) + 32


def projects(C):
    top = 96
    inner_h = 46 + 64 * len(PROJ_ROWS) + 16
    b = eyebrow(C, "SELECTED WORK")
    b.append(rect(64, top, 1072, inner_h, rx=14, fill=C["panel"],
                  stroke=C["stroke"]))
    heads = [(88, "ПРОЕКТ"), (352, "ЧТО ЭТО"), (756, "СТЕК"), (1000, "ТИП")]
    for x, s in heads:
        b.append(text(x, top + 30, s, size=16, fill=BODY, ls=2))
    b.append(line(88, top + 46, 1112, top + 46, stroke=C["stroke"]))
    y = top + 86
    for i, (name, what, stack, tag, color) in enumerate(PROJ_ROWS):
        b += [text(88, y, name, font=MONO, size=20, weight="700", fill=BRIGHT),
              text(352, y, what, size=18, fill=BODY),
              text(756, y, stack, font=MONO, size=16, fill=TEAL),
              rect(1000, y - 18, 112, 26, rx=13, stroke=color, sw=1.2,
                   opacity=0.8),
              text(1056, y, tag, font=MONO, size=16, fill=color, ls=1,
                   anchor="middle")]
        if i < len(PROJ_ROWS) - 1:
            b.append(line(88, y + 24, 1112, y + 24, stroke=C["stroke"],
                          opacity=0.7))
        y += 64
    return b


# ------------------------------------------------------------- toolkit
TOOL_COLS = [
    ("API и данные", ["HTTP / REST API", "JSON · XML", "SQL (MS SQL)"]),
    ("Код и скрипты", ["Python", "PowerShell", "JS / TS · React"]),
    ("Инфраструктура", ["Windows Server", "Active Directory", "Linux · VMware"]),
    ("Процессы", ["Jira · Confluence", "Git", "База знаний"]),
]


def toolkit(C):
    b = eyebrow(C, "TOOLKIT")
    for ci, (head, items) in enumerate(TOOL_COLS):
        x = 64 + ci * 273
        b.append(text(x, 114, head, size=19, weight="700", fill=C["accent"]))
        for ri, item in enumerate(items):
            y = 132 + ri * 48
            b += [rect(x, y, 253, 40, rx=10, fill=C["panel"], stroke=C["stroke"]),
                  text(x + 18, y + 26, item, font=MONO, size=17, fill=BRIGHT)]
    return b


# -------------------------------------------------- admintools: экран 1
AT_ACTIONS = ["Подключиться по RDP", "Установить принтер",
              "Восстановить службы ИБ", "Диск и очистка",
              "Сеанс пользователя", "Установка ПО"]
AT_CARD = [("Пользователь", "Иванов Иван Иванович"),
           ("Телефон", "4512"),
           ("Кабинет", "214"),
           ("ОС", "Windows 10 22H2"),
           ("Адрес", "10.0.14.87"),
           ("Источник", "AD + локальная история")]


def admintools_ui(C):
    b = eyebrow(C, "ADMINTOOLS · ПОИСК И КАРТОЧКА ПК")
    b += [rect(64, 96, 1072, 512, rx=14, fill=C["panel"], stroke=C["stroke"]),
          text(88, 128, "AdminTools — техподдержка", font=MONO, size=17,
               weight="700", fill=BRIGHT),
          text(1112, 128, "PowerShell 5.1 · WPF", font=MONO, size=15,
               fill=AMBER, anchor="end"),
          line(88, 144, 1112, 144, stroke=C["stroke"])]
    # строка поиска
    b += [rect(88, 164, 800, 44, rx=10, fill=C["inner"], stroke=C["stroke"]),
          text(110, 192, "Иванов", font=MONO, size=18, fill=BRIGHT),
          rect(180, 174, 2, 24, fill=TEAL),
          rect(908, 164, 204, 44, rx=10, fill="none", stroke=TEAL, sw=1.2),
          text(1010, 192, "НАЙТИ", font=MONO, size=16, fill=TEAL, ls=1.4,
               anchor="middle"),
          text(88, 234, "имя ПК · ФИО · логин · телефон · кабинет — "
                        "ищет в Active Directory и в локальной истории",
               size=15, fill=BODY)]
    # карточка машины
    b += [rect(88, 254, 420, 250, rx=10, fill=C["inner"], stroke=C["stroke"]),
          text(112, 290, "PC-0412", font=MONO, size=20, weight="700",
               fill=BRIGHT),
          text(484, 290, "в сети", font=MONO, size=14, fill=TEAL,
               anchor="end"),
          circle(428, 285, 4, fill=TEAL)]
    y = 326
    for label, value in AT_CARD:
        b += [text(112, y, label, size=14, fill=BODY),
              text(484, y, value, font=MONO, size=14, fill=BRIGHT,
                   anchor="end")]
        y += 29
    # плитка действий
    b += [text(532, 272, "ДЕЙСТВИЯ", font=MONO, size=14, fill=BODY, ls=2),
          text(1112, 272, "26 в списке", font=MONO, size=14, fill=AMBER,
               anchor="end")]
    for i, op in enumerate(AT_ACTIONS):
        x = 532 + (i % 2) * 304
        y = 290 + (i // 2) * 60
        b += [rect(x, y, 280, 46, rx=10, fill=C["inner"], stroke=C["stroke"]),
              rect(x + 16, y + 17, 12, 12, rx=3, fill="none", stroke=TEAL,
                   sw=1.2),
              text(x + 40, y + 30, op, size=16, fill=BRIGHT)]
    b.append(text(532, 486, "…и ещё 20 — состав действий задан в Config.psd1",
                  size=15, fill=BODY))
    # статус и журнал
    b += [line(88, 522, 1112, 522, stroke=C["stroke"]),
          text(88, 552, "Опрос сети идёт в пуле runspace — окно остаётся "
                        "отзывчивым", size=15, fill=BODY),
          text(1112, 552, "8 потоков", font=MONO, size=14, fill=AMBER,
               anchor="end"),
          rich(88, 582, [{"t": "[14:02:14]", "fill": AMBER},
                         {"t": " Печать: драйвер установлен под SYSTEM · "
                               "спулер перезапущен · "},
                         {"t": "OK", "fill": TEAL}], font=MONO, size=14)]
    return b


# -------------------------------------------------- admintools: экран 2
PRINTERS = [
    ("PRN-T2-0143", "Терминал 2 · стойка 14", "Kyocera P3145dn", True),
    ("PRN-T2-0187", "Терминал 2 · зона вылета", "HP LaserJet M507", True),
    ("PRN-T2-0204", "Терминал 2 · багаж", "Zebra ZT411", False),
    ("PRN-T2-0219", "Терминал 2 · регистрация", "Kyocera P3145dn", True),
]
PRINT_FLOW = ["драйвер под SYSTEM", "перезапуск спулера",
              "подключение пользователю", "проверка результата"]


def admintools_printers(C):
    b = eyebrow(C, "ADMINTOOLS · КАТАЛОГ ПРИНТЕРОВ")
    b += [rect(64, 96, 1072, 420, rx=14, fill=C["panel"], stroke=C["stroke"]),
          text(88, 128, "AdminTools — печать и драйверы", font=MONO, size=17,
               weight="700", fill=BRIGHT),
          text(1112, 128, "каталог сервера печати · 818 принтеров", font=MONO,
               size=15, fill=AMBER, anchor="end"),
          line(88, 144, 1112, 144, stroke=C["stroke"]),
          rect(88, 164, 680, 44, rx=10, fill=C["inner"], stroke=C["stroke"]),
          text(110, 192, "терминал 2", font=MONO, size=18, fill=BRIGHT),
          rect(218, 174, 2, 24, fill=TEAL),
          rect(788, 164, 324, 44, rx=10, fill="none", stroke=TEAL, sw=1.2),
          text(950, 192, "ПОДКЛЮЧИТЬ", font=MONO, size=16, fill=TEAL, ls=1.4,
               anchor="middle"),
          text(88, 240, "ПРИНТЕР", size=15, fill=BODY, ls=2),
          text(340, 240, "РАЗМЕЩЕНИЕ", size=15, fill=BODY, ls=2),
          text(700, 240, "ДРАЙВЕР", size=15, fill=BODY, ls=2),
          text(1000, 240, "СТАТУС", size=15, fill=BODY, ls=2),
          line(88, 256, 1112, 256, stroke=C["stroke"])]
    y = 292
    for i, (name, place, drv, online) in enumerate(PRINTERS):
        if i == 0:
            b += [rect(88, y - 26, 1024, 38, rx=8, fill=C["inner"]),
                  rect(88, y - 26, 3, 38, rx=1.5, fill=AMBER)]
        b += [text(104, y, name, font=MONO, size=17, weight="700", fill=BRIGHT),
              text(340, y, place, size=16, fill=BODY),
              text(700, y, drv, font=MONO, size=15, fill=TEAL),
              circle(1008, y - 5, 4, fill=TEAL if online else BODY),
              text(1024, y, "ГОТОВ" if online else "ОФЛАЙН", font=MONO,
                   size=15, fill=TEAL if online else BODY)]
        if i < len(PRINTERS) - 1:
            b.append(line(104, y + 20, 1112, y + 20, stroke=C["stroke"],
                          opacity=0.7))
        y += 44
    b.append(line(88, 452, 1112, 452, stroke=C["stroke"]))
    x = 88
    for i, step in enumerate(PRINT_FLOW):
        b.append(text(x, 486, step, font=MONO, size=15,
                      fill=BRIGHT if i == 0 else BODY))
        x += len(step) * 9.2 + 24
        if i < len(PRINT_FLOW) - 1:
            b.append(text(x - 17, 486, "→", font=MONO, size=15, fill=AMBER))
    return b


# -------------------------------------------------- admintools: экран 3
ARCH_CARDS = [
    ("ДАННЫЕ", [("Active Directory", "поиск объекта в домене"),
                ("Локальная история", "ПК, пользователь, телефон, кабинет"),
                ("Без файловых шар", "отваливаться нечему")]),
    ("ВЫПОЛНЕНИЕ", [("Пул runspace", "сеть уходит в фоновые потоки"),
                    ("Таймер собирает результат", "интерфейс не ждёт ответа"),
                    ("Без DoEvents и Start-Sleep", "окно не подвисает")]),
    ("БЕЗОПАСНОСТЬ", [("Задача через COM", "а не через schtasks.exe"),
                      ("Пароль не в командной строке", "и не в журналах аудита"),
                      ("Без временных XML", "ничего не пишем на общий диск")]),
]


def admintools_arch(C):
    b = eyebrow(C, "ADMINTOOLS · КАК УСТРОЕНО")
    for ci, (head, items) in enumerate(ARCH_CARDS):
        x = 64 + ci * 370
        b += [rect(x, 96, 332, 252, rx=12, fill=C["panel"], stroke=C["stroke"]),
              text(x + 24, 132, head, font=MONO, size=15, weight="700",
                   fill=AMBER, ls=2.4),
              line(x + 24, 148, x + 308, 148, stroke=C["stroke"])]
        y = 186
        for title, note in items:
            b += [rect(x + 24, y - 9, 8, 8, rx=2, fill=TEAL),
                  text(x + 44, y, title, size=15, weight="700", fill=BRIGHT),
                  text(x + 44, y + 22, note, size=14, fill=BODY)]
            y += 56
    b += [line(64, 376, 1136, 376, stroke=C["rule"]),
          text(64, 406, "Только штатные компоненты Windows — без сторонних "
                        "библиотек, .exe и RSAT.", size=16, fill=C["eyebrow"]),
          text(64, 432, "Пути, серверы и все 26 действий описаны в "
                        "Config.psd1 — без правки кода.", size=16,
               fill=C["eyebrow"])]
    return b


if __name__ == "__main__":
    write("hero", HERO_W, HERO_H, "Максим Грачев — поддержка интеграций",
          "Максим Грачев, специалист поддержки интеграций, вторая линия, Москва. "
          "Разбираю эскалации по внутренним системам аэропорта и довожу проблему "
          "до причины. Рабочий процесс: 01 эскалация — приём и триаж; "
          "02 локализация — логи, API, SQL; 03 фикс — правка и автоматизация. "
          "Домодедово Хендлинг, 10–15 эскалаций в день, REST API, SQL, Python.",
          hero)
    write("projects", 1200, PROJ_H, "Проекты",
          "AdminTools — 26 операций над удалёнными ПК; PowerShell, WPF, Active "
          "Directory; внутренний инструмент. Airport-It-Analytics — 33 309 "
          "обращений, SLA, влияние на рейсы; Python, pandas, SQL; аналитика. "
          "Boltushka24 — мессенджер сообществ: чаты, голос и видео; Next.js, "
          "Supabase; фулстек. my-portfolio — личный сайт-портфолио на React.",
          projects)
    write("toolkit", 1200, 296, "Инструменты",
          "API и данные: HTTP и REST API, JSON, XML, SQL (MS SQL). Код и "
          "скрипты: Python, PowerShell, JS/TS и React. Инфраструктура: Windows "
          "Server, Active Directory, Linux, VMware. Процессы: Jira, Confluence, "
          "Git, база знаний.",
          toolkit)
    write("admintools-ui", 1200, 640, "AdminTools — поиск и карточка ПК",
          "Схема интерфейса AdminTools. Строка поиска: имя ПК, ФИО, логин, "
          "телефон или кабинет — ищет в Active Directory и в локальной "
          "истории. Слева карточка машины PC-0412: пользователь, телефон, "
          "кабинет, ОС, адрес, источник данных. Справа плитка действий: "
          "подключиться по RDP, установить принтер, восстановить службы "
          "информационной безопасности, диск и очистка, сеанс пользователя, "
          "установка ПО, и ещё 20 действий из Config.psd1. Внизу: опрос сети "
          "идёт в пуле runspace на 8 потоков, окно остаётся отзывчивым.",
          admintools_ui)
    write("admintools-printers", 1200, 545, "AdminTools — каталог принтеров",
          "Схема экрана печати AdminTools: фильтр по запросу «терминал 2», "
          "каталог сервера печати на 818 принтеров, кнопка «Подключить». "
          "Таблица: принтер, размещение, драйвер, статус. Порядок действий: "
          "драйвер под SYSTEM, перезапуск спулера, подключение пользователю, "
          "проверка результата.",
          admintools_printers)
    write("admintools-arch", 1200, 460, "AdminTools — как устроено",
          "Данные: Active Directory для поиска объекта в домене, локальная "
          "накопительная история с ПК, пользователем, телефоном и кабинетом, "
          "без файловых шар. Выполнение: пул runspace, таймер собирает "
          "результат, без DoEvents и Start-Sleep. Безопасность: задача "
          "регистрируется через COM, а не через schtasks.exe, пароль не "
          "попадает в командную строку и в журналы аудита, временные XML на "
          "общий диск не пишутся. Только штатные компоненты Windows — без "
          "сторонних библиотек, .exe и RSAT; пути, серверы и все 26 действий "
          "описаны в Config.psd1.",
          admintools_arch)
