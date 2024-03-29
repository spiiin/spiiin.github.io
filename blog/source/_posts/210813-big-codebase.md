---
title: Как разобраться в большой кодовой базе
abbrlink: 1160101424
date: 2021-07-13 17:42:08
tags: dev_evolution
---

Как читать и изучать код в больших кодовых базах.
<!-- more -->

[Tips for Navigating Large Game Code Bases](https://solid-angle.blogspot.com/2015/08/tips-for-navigating-large-game-code.html) - как начать, если устроился разработчиком игр.
- разобраться, как собрать проект и запустить игру
- спросить, есть ли инструкция, документация, или туториалы
- узнать, нет ли простой демки, показывающей возможности движка
- найти часть кода, которая связана с первой задачей
(поиск связанных слов по всему коду, отладчик, спросить тим-лида или кого-нибудь)
- воспользоваться редактором игры или тулзами
- почитать историю коммитов
- поискать, какие средства есть для решения задачи в движке, не решать с нуля
- найти и изучить документ, описывающий Coding Style
- разобраться с процессом добавления своего кода в репозиторий

Позже:
- попробовать найти основной игровой цикл
- изучить иерархию базовых игровых классов
- изучить основные используемые в работе классы и модули
- понять принцип разделения движка и игры на подсистемы/модули/etc
- изучить пайплайн добавления ассетов
- разобраться с используемыми скриптовыми языками
- попробовать разобрать рендер игровой сцены
- изучить используемые средства профилирования
- изучить способы сборки игры под различные платформы

[Random Things About Code](https://aras-p.info/texts/files/2018Academy%20-%20About%20Code.pdf)
Раздел `Navigating large codebases`

Смириться с тем, что большие кодовые базы:
- содежат много legacy кода
- плохо документированы
- содержат места, про которые никто не знает как/зачем/почему они были добавлены
(но большая часть кода всё же была добавлена с определенной целью, и выбросить/переделать - часто плохая идея)

Если что-то выглядит странно/непонятно/неправильно:
- 30% что есть причина (неочевидная) почему сделано так
- 30% что когда-то БЫЛА причина
- 30% что причины нет, и код просто кривой
- 10% что Ктулху Рльех Фтагн


[Reviewing ALL THE CODE](https://aras-p.info/blog/2013/07/07/reviewing-all-the-code/) - как следить за всем, что происходит в кодовой базе, Aras Pranckevičius (Unity)
Средства, упрощающие изучение всех изменений в кодовой базе

Что изучать:
`Unity`
`Unreal Engine`
`Godot`
`Doom 3`
`Cocos2d-x`

Возможно:
(что-то не поддерживается, что-то сложно получить)
`MonoGame`
`CryEngine`
`Unigine`
`Defold`
`GameMaker`

Код в Doom 3
[The Exceptional Beauty of Doom 3's Source Code](https://kotaku.com/the-exceptional-beauty-of-doom-3s-source-code-5975610)
[Doom 3 source code review](https://fabiensanglard.net/doom3/index.php)

Интервью с одним из лид-программистов Unreal
[Как Делают Игры 172. Unreal Engine](https://youtu.be/bzHevRs-cd4)
[Как Делают Игры 289. Unreal Engine 5](https://youtu.be/Q-2Nf5j71m0)


Про пайплайны:
[HANA C++ Development Environment and Processes](https://hookrace.net/blog/hana-cpp-development/) - не относится к играм, но есть ссылки на пару интересных тулзов для работы с тяжёлой кодовой базой.
[Hobby engine to game engine](https://aras-p.info/texts/files/201410-TUM-HobbyEngineToGameEngine.pdf) - отличия в пайплайне небольших движков и больших, на примере Unity.
