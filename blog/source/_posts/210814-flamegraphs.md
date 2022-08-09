---
title: Flamegraphs
abbrlink: 2779627234
date: 2021-07-14 09:53:59
tags: dev_method
---

[Флеймграфы](https://www.brendangregg.com/flamegraphs.html) - удобный способ представления информации, собранной профайлером.

<!-- more -->

{% youtuber video nZfNehCzGdw %}
{% endyoutuber %}

Видео с объяснением, зачем нужны, и примерами применения (на сайте есть более свежие версии, но в этой собрано всё сразу).

На вход тулзе подаётся текстовый файл с собранными профайлером данными. Чаще всего используются статистические профайлеры, которые генерируют сэмплы с определённой частотой и собирают информацию о стеках вызовов.

Однако текстовый вывод таких профайлеров громоздкий и малоинформативный, поэтому они преобразуются с помощью скриптов на перле в `CPU Samples Flamegraph`, который позволяет визуально увидеть, чем именно был занят процессор.

Граф представляет собой SVG-файл с JavaScript-кодом, который можно рассматривать и изучать в Google Chrome интерактивно. Размер файла - ~500кб, что позволяет хранить графы различных измерений программы (например, в системе задач, для передачи между програмистами, QA и инженерами по производительности) и сравнивать их между собой.

Получить данные в нужном для построения графа виде позволяет практически любой профайлер: 
`perf, eBPF, SystemTap, and ktap, DTrace, XCode instruments, XPerf - Linux/MacOSX/Windows`
Также есть способы собрать данные для различных интерпретируемых языков и виртуальных машин.

Мобильные системы идут немного своим путём, но также можно получить данные для:
[Android](https://blog.rhye.org/post/android-profiling-flamegraphs/) ([онлайн-конвертер](https://aflame.rhye.org/))
[iOS](https://github.com/lennet/FlameGraph) ([ещё](https://schani.wordpress.com/2012/11/16/flame-graphs-for-instruments/))

Больше примеров - [github](https://github.com/brendangregg/FlameGraph), [сайт автора](https://www.brendangregg.com/flamegraphs.html)

Автор показывает способы, как профилировать не только CPU, но и память, обращения к диску и сетевые события.

Производные от Flamegraph способы представления профилируемых данных:
`Facebook Icicle charts`
`Google Flame charts`

Инструменты для Linux, которые представляют информацию в том числе в виде флеймграфов:
[Hotspot](https://github.com/KDAB/hotspot) - CPU сэмплы
[Heaptrack](https://github.com/KDE/heaptrack) - потребление памяти в куче

Для Windows:
[etwprof](https://github.com/Donpedro13/etwprof)

Применение в играх:
[Profiling: Measuring and Analysis](https://technology.riotgames.com/news/profiling-measurement-and-analysis) - серия статей Tony Albrecht, на основе видео [Pitfalls of Object Oriented Programming, Revisited - Tony Albrecht (TGC 2017)](https://youtu.be/VAT9E-M-PoE).
[FlameGraphs: Understand where your program is spending time](https://johnysswlab.com/flamegraphs-understand-where-your-program-is-spending-time/)


