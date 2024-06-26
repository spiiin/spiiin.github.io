---
title: Making tools for big games
abbrlink: 2767873544
date: 2022-12-25 16:57:07
tags:
 - link
 - dev_method
---

Тезисы из доклада технического директора `Guerilla` Michiel van der Leeuw [Making tools for big games](https://www.guerrilla-games.com/read/making-tools-for-big-games)

<!-- more -->

**`Вступление`**
- Технология в геймдеве перестала определять игру и её геймдизайн, а является одной из фич игры
- Технология сейчас -- это не только движок игры, а её тулсет
- Тулсет позволяет поддерживать масштабирование количества контента игр, а также следить за качеством и процессом производства
- Респект автора доклада `Naughty Dog`, часть идей оттуда

**`Идея 1. Сокращение "зоны сумерек", когда QA находятся между игрой, таск-трекером, браузером, vcs, мессенджером и почтовым клиентом`**
- Кастомный интерфейс к vcs, шаблоны для заполнения полей близкие к стандартам компании
- Соединение перед пуллом с билд сервером для сверки, в порядке ли ревизия, которую собираешься получить
- In-game gui для оформления задач в Jira -- запись видео, логгирование игровых ресурсов в кадре
- Редактор видео, в котором можно отметить тайминг бага/задачи, связанные ассеты, разметить зоны и отрезать лишнее. Ссылки на фрейм видео можно добавлять в задачи
- Ассеты хранятся в базе данных с метаинформацией. Среди прочего, хранят обратные ссылки на баги, ссылающиеся на эти ассеты.

Выявить точки, из которых удобнее всего совершать действия, и из этих точек с помощью api к другим приложениям дать возможность работать с этими приложениями без переключения контекста. Убрать рутину.
Пара бонусных идей не из доклада:
- В code-review вычислять, какие из прошлых коммитов/мердж реквестов затрагивает диф кода и выводить список этих коммитов ("чей код ты потенциально мог сломать").
- Подтягивать к багу в Jira данные из всех систем аналатики (доступ ко всей полезной инфе на одной страничке)

**`Идея 2. Слежение за здоровьем билда позволяет увеличить количество итераций`**
- Бот-фермы из девкитов, которые выполняют скрипты телепортации по миру и сохраняют профилирование, телеметрию и игровую информацию в виде карты мира, отдельный редактор для визуализации и изучения этой карты
- Примеры применения -- визуализатор информации для гейм-дизайнеров и непосредственно отладка геометрических данных (карты рек, эрозии, нормалей, карты видимости неба), heat-map тормозящих мест, визуализация мест багов в jira. Всю информацию можно посмотреть в других местах, но такое картографирование позволяет оценить общую картину
- Запросы к данным для отображения на карте исторических данных (диффы, графики, экспорт в json/csv)
- Вьюер карты тесно связан с игрой (можно получать графики производительности с девайсов и кол-во потребляемой памяти, а также делать отметки на графиках и ссылаться на них)
- Метрика -- количество изменений, которое команда может позволить себе без страха делать в последние дни/недели перед релизом

{%post_link 210888-level-design-patterns %} - итерации делают игру лучше, упрощая процесс разработки
{%post_link 220809-treasure-search-system %} - итерации кроме полировки могут позволить найти новые уникальные решения

Глобальная карта для отображения оверлеями различной информации -- отличный инструмент, кажется, впервые видел идею с тепловой картой производительности еще в докладе про `starcraft 2`. Я такое тоже делал, чтобы отслеживать ассеты, которые артисты/геймдизайнеры забыли правильно разметить.

**`Идея 3. Работу с ассетами всегда можно улучшить`**
- Всё висит на сервере в памяти и стримится на девелоперские машины (10 Gb сеть в локалке)
- Позволило серьёзно уменьшить размер дубликатов ресурсов
- Можно сгенерить строковый айдишник, по которому другой человек может запустить в точности такую же версию игры
- Самописный сервер на 650 строк, БД с парами ключ значение, быстрее шеринг через SMB, NFS, файловый сервер Apache, etc
- Виртуальная файловая система, ОС не видит изменений
- 18 core cpu, 768 Gb ram, 80 Gb network, 16 tb ssd на 300 человек

Наиболее радикальная идея, работать локально с исходными версиями ассетов, и стримить ресурсы через глобальный общий сервер. Доклад 2019 года, когда все сидели в одном офисе, но в [твиттере](https://twitter.com/MvdLeeuwGG/status/1606268200143970304) автор упоминает, что адаптировали и для домашней работы. Кроме блоба ассета хранится также метаинформация (например, ссылки, в каких тасках он задействован).


**update 24-03-05**
[Building Tools Quickly: Blueprints, Menus, Utilities, and Widgets](https://www.youtube.com/watch?v=wJqOn88cU7o) -- доклад про различные способы расширения редактора Unreal от Embark Studios, а также различные связи тулзов и инфраструктуры через сервер [Embark Skyhook](https://github.com/EmbarkStudios/skyhook) - Unreal Remote Control API <--> Python Server <--> DCC/Slack/Jira etc.

