#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Баннер статистики GitHub: свои данные, свой SVG, без сторонних сервисов.

Работает в два шага:

  1. сбор  — GitHub API → assets/stats.json  (нужен GITHUB_TOKEN)
  2. рисование — stats.json → stats-dark.svg и stats-light.svg

    python3 assets/stats.py            # собрать и нарисовать
    python3 assets/stats.py --render   # только нарисовать из stats.json

Если сеть или токен недоступны, шаг сбора пропускается и баннер
перерисовывается из сохранённого снимка — картинка в README не ломается.
"""
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import date

import build as design

USER = "1notlov3"
API = "https://api.github.com"
HERE = os.path.dirname(os.path.abspath(__file__))
SNAPSHOT = os.path.join(HERE, "stats.json")
TOP_LANGS = 5


# ------------------------------------------------------------------- сбор
def api_get(path):
    req = urllib.request.Request(API + path, headers={
        "Accept": "application/vnd.github+json",
        "User-Agent": "1notlov3-profile-stats",
    })
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        req.add_header("Authorization", "Bearer " + token)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def collect():
    """Снимок публичного профиля. Приватные репозитории не учитываются."""
    profile = api_get("/users/%s" % USER)

    repos, page = [], 1
    while True:
        batch = api_get("/users/%s/repos?per_page=100&type=owner&page=%d"
                        % (USER, page))
        repos.extend(batch)
        if len(batch) < 100:
            break
        page += 1

    public = [r for r in repos if not r.get("private")]
    langs = {}
    for r in public:
        if r.get("language"):
            langs[r["language"]] = langs.get(r["language"], 0) + 1

    return {
        "user": USER,
        "collected": date.today().isoformat(),
        "repos": profile.get("public_repos", len(public)),
        "followers": profile.get("followers"),
        "stars": sum(r.get("stargazers_count", 0) for r in public),
        "languages": dict(sorted(langs.items(), key=lambda kv: -kv[1])),
    }


# -------------------------------------------------------------- рисование
NUMBERS = [("Публичные репозитории", "repos"),
           ("Звёзды", "stars"),
           ("Подписчики", "followers")]


def banner(data):
    def build(C):
        b = design.eyebrow(C, "GITHUB · @%s" % data["user"])

        # левая панель — числа профиля
        b.append(design.rect(64, 96, 400, 200, rx=14, fill=C["panel"],
                             stroke=C["stroke"]))
        b += [design.text(88, 128, "ПРОФИЛЬ", font=design.MONO, size=14,
                          weight="700", fill=design.AMBER, ls=2.4),
              design.line(88, 144, 440, 144, stroke=C["stroke"])]
        y = 184
        for label, key in NUMBERS:
            value = data.get(key)
            b += [design.text(88, y, label, size=16, fill=design.BODY),
                  design.text(440, y, "—" if value is None else str(value),
                              font=design.MONO, size=24, weight="700",
                              fill=design.BRIGHT, anchor="end")]
            y += 44

        # правая панель — языки
        b.append(design.rect(496, 96, 640, 200, rx=14, fill=C["panel"],
                             stroke=C["stroke"]))
        b += [design.text(520, 128, "ЯЗЫКИ В ПУБЛИЧНЫХ РЕПОЗИТОРИЯХ",
                          font=design.MONO, size=14, weight="700",
                          fill=design.AMBER, ls=2.4),
              design.line(520, 144, 1112, 144, stroke=C["stroke"])]

        langs = list(data.get("languages", {}).items())[:TOP_LANGS]
        total = sum(data.get("languages", {}).values())
        if not langs:
            b.append(design.text(520, 184, "нет данных", size=16,
                                 fill=design.BODY))
            return b

        top = max(count for _, count in langs)
        y = 176
        for i, (name, count) in enumerate(langs):
            share = count / total * 100
            width = round(300 * count / top)
            b += [design.text(520, y, name, size=16,
                              fill=design.BRIGHT if i == 0 else design.BODY),
                  design.rect(756, y - 12, 300, 10, rx=5, fill=C["inner"]),
                  design.rect(756, y - 12, max(width, 4), 10, rx=5,
                              fill=design.TEAL if i == 0 else design.BODY),
                  design.text(1112, y, "%d%%" % round(share), font=design.MONO,
                              size=15, fill=design.BODY, anchor="end")]
            y += 24

        return b

    return build


def render(data):
    langs = ", ".join("%s — %d из %d репозиториев" % (n, c, sum(
        data["languages"].values())) for n, c in
        list(data.get("languages", {}).items())[:TOP_LANGS]) or "нет данных"
    desc = ("Статистика профиля GitHub @%s на %s. Публичных репозиториев: %s. "
            "Звёзд: %s. Подписчиков: %s. Языки в публичных репозиториях: %s."
            % (data["user"], data["collected"], data["repos"], data["stars"],
               "неизвестно" if data.get("followers") is None
               else data["followers"], langs))
    design.write("stats", 1200, 350, "Статистика GitHub", desc, banner(data))


def main():
    data = None
    if "--render" not in sys.argv:
        try:
            data = collect()
        except (urllib.error.URLError, urllib.error.HTTPError, OSError) as e:
            print("сбор не удался (%s), рисую из снимка" % e, file=sys.stderr)
    if data:
        with open(SNAPSHOT, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.write("\n")
    else:
        with open(SNAPSHOT, encoding="utf-8") as f:
            data = json.load(f)
    render(data)


if __name__ == "__main__":
    main()
