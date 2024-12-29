---
title: "Плюсовики в геймдеве + материалы по геймдеву"
abbrlink: 2794788536
date: 2024-05-25 22:03:31
tags:
  - gamedev
  - cpp
  - dev_method
  - link
  - longread
---

Я давно писал про использование C++ как языка в геймдеве
- {% post_link 220130-about-cpp-gamedev %}

Тут о людях, которые пишут на С++, банальное, но немного наболевшее и скопившееся, наверное в последний раз на эту тему.

<!-- toc -->

## Специализации в геймдеве

С какого-то доклада я стащил такое разделение программистов по специальностям в AAA-студиях:
`Game - Gameplay/Generalist/AI`
`Game Tech - AI/Animation/Physics/Render/Network/Generalist/Tools`
`Core Tech Engine - Animation/Physics/Render/Network/Generalist/Tools`

Я бы разделил всю пачку специализаций геймдева просто на `рендер/геймплей/технологии`

`Рендер`
Вообще отдельный мир, постоянное изучение пейперов, куча математики, ковыряние с API программирования gpu и с архитектурой железок.
- {% post_link 240222-graphic-programming %}

[Life and Death of a Graphics Programmer](https://www.elopezr.com/life-and-death-of-a-graphics-programmer/)
[The engine of the future.The keynote nobody (quite literally) asked for](https://c0de517e.com/014_future_engines.htm)

`Геймплей`
Взаимодействие с геймдизайнерами, артистами, продюсерами -- изучение особенностей работы смежных дисциплин, быстрый фидбек -- результаты своей работы видишь в игре. Бешеный драйв, горящие глаза, сроки, да и сам быстрее выгораешь. Требует быстрых итераций (как вначале, когда нужно прототипировать, искать фановые механики, так в конце при полишинге), и предсказуемости -- игры-сервисы требуют регулярного выхода апдейтов.

`Технологии`
Не так весело, но зато и не так жгутся сроки. Задачи могут как требовать низкоуровневого кода (движки/компиляторы), так и высокоуровневого (редакторы, ui для артистов). Главный навык чаще всего -- эмпатия и понимание образа мысли и действий юзеров. 
- {% post_link 240202-design-ideas-2-md %} - раздел про эмпатию "Имперсонификация и поиск паттернов вокруг"

## Проблема плюсовиков в геймдеве

В не-топовых командах работают чаще просто **`"программисты на C++"`**.

По С++ много книг, конференций (в том числе на русском), курсов. Наверное, один из главных евангелистов языка на русском - Антон Полухин.

Из его докладов, где применяется С++ -- браузеры/поисковые запросы/языки программирования/кодеки/торренты/игровые движки/космос/самолёты/автомобили/медицинское по/распознавание образов/обработки изображений/web фреймворки/web-страницы/базы данных/proxy/embedded/компиляторы/виртуальные машины/драйверы/биржа/офисные приложения/банкоматы/сапр/рендеры/химия/физика/машинное обучение. Все эти скоупы объединяет то, что в них может потребоваться писать код на низком уровне.

Тем не менее в каждой из областей есть и другие требования, и применяются также другие языки, которые лучше соответствуют этим требованиям. Например -- надёжность (верифицируемость, работа в изолированной среде), простота использования, синтаксическая выразительность, простота работы в многопоточной среде, battery-included (соотвествие стандартной или вендорной библиотеки предметной области), скорость компиляции, скорость итерации разработки (hot-reload, repl, интерпретация). Об этом редко говорят на конференциях и в книгах по С++ (что в принципе и логично).

В то же время, геймдев, как индустрия, достаточно закрытая, и информации по разработке игр, как и книг и коференций, сильно меньше. Вдобавок, конференции освещают не только техническую сторону разработки, а ещё и представляют из себя шоу (как на уровне больших игр, так и инди), или обсуждение вопросов как лучше зарабатывать, что еще сильнее уменьшает их интересность для технарей. В книгах также редко удаётся передать современные проблемы геймдева по множеству причин -- объём предметной области, более узкая специализация и более высокоуровневые темы относительно общих идиом и практик языка, устаревание информации с появлением новых поколений игровых устройств, закрытость информации (как от вендеров платформ, так и от ведущих студий).

Как результат открытости С++ и закрытости сферы разработки игр, приходящие в геймдев программисты имеют "C++-майндсет" -- знают как принято писать на С++ "в общем", но открывают для себя специфику разработки игр только в процессе работы.

**Способ писать на C++, нахватавшись знаний из разных областей его применения, находится далеко от того, что нужно конкретно для разработки игр**.

Последствия этого -- иногда "плюсовики в геймдеве", сталкиваясь с какой-то проблемой, начинают решать её таким методом заново, не вникая в то, что наступают на те же грабли, по которым проходили их коллеги в индустрии разработки игр лет так 10-15 назад.

- {% post_link 240202-design-ideas-2-md %} -- одна из таких проблем, дизайн GameObject-а.
[The GDC 2003 Game Object Structure Roundtable](https://www.gamearchitect.net/Articles/GameObjectRoundtable.html) -- как делить игровые объекты между программистами, гейм-дизайнерами и артистами -- *c++/scripts/visual-programming*

*Иногда и примеры сложно разобрать более детально из-за NDA, но вот ещё несколько примеров дискуссий, касающихся того, что есть в каждой игре, т.е. с дизайном этого сталкиваются все разработчики игр*

`ui`
[Why I think Immediate Mode GUI is way to go for GameDev tools](https://gist.github.com/bkaradzic/853fd21a15542e0ec96f7268150f1b62) -- gui для тулзов и игр, сильно шире, чем в названии. Immediate/Retained/Reactive, Native/Web, Foss/Proprietary 
- {%post_link 240323-reactive-gui-push-pull%}

`containers/allocators/pointers`
[Best Practices for Authoring Generic Data Structures](https://www.jeremyong.com/c++/graphics/2018/11/17/best-practices-for-authoring-generic-data-structures/) -- альтернативный дизайн интерфейсов для контейнеров, [Bitsquid Foundation Library](https://bitsquid.blogspot.com/2012/11/bitsquid-foundation-library.html), дальше по обратным ссылкам дискуссии не только о дизайне контейнеров, но и базовых структур стандартной библиотеки, аллокаторах, указателях и сериализации/кодогенерации -- *class-centric vs data centric design* ([Blob and I](https://bitsquid.blogspot.com/2010/02/blob-and-i.html), [Zmeya](https://github.com/SergeyMakeev/Zmeya) + ссылки дальше).
- {%post_link 210818-inside-stl-links%} -- об альтернативных stl. Одна из фич C, унаследованная C++ -- это возможность писать программы без использования стандартной библиотеки.

`engines`
**Архитектура зависит от формата команды, платформы, развитости технологии, типа игр, и майндсета, поэтому подходы сильно разные**
[Writing Reusable Code](https://gamesfromwithin.com/writing-reusable-code) -- про паттерны *framework/layers/components* в игровых движках.
[How I Evaluate Game Engines](https://www.jeremyong.com/game%20engines/2023/09/15/how-i-evaluate-game-engines/) -- с точки зрения масштабирования.
[Jonathan Blow on why C++ is a bad language for games](https://www.youtube.com/watch?v=VglTrU5YmRw) -- вообщем-то, не C++, а о паттерне layers
[Your 1st, 2nd, 3rd, and Nth Game Engines](https://www.youtube.com/watch?v=GK7ntA7a2vk) -- о том, чем плох framework
[Write Games, Not Engines](https://geometrian.com/programming/tutorials/write-games-not-engines/) -- инди-подход
[An Anatomy of Despair: Introduction](https://gamearchitect.net/2008/04/15/an-anatomy-of-despair-introduction/) -- про выбор между low-level и abstractions (layers)

`scripting`
[Scripting language? Engine language?](https://enginearchitecture.org/downloads/reac2023_scripting_language.pdf) -- про границы между движком и игрой
[The Next Mainstream Programming Language: A Game Developer’s Perspective](https://www.st.cs.uni-saarland.de/edu/seminare/2005/advanced-fp/docs/sweeny.pdf) -- про баланс производительность/скорость разработки, надёжность, чистоту, многопоточность, развитие железа, ленивые вычисления и системы типов
[Ideas about a new programming language for games](https://www.youtube.com/watch?v=TH9VCN6UkyQ) -- Jai
[Продуктивность и производительность в новых скриптовых языках](https://www.youtube.com/watch?v=IvHGczF6Go0) -- скриптовый язык для программистов

- {%post_link 240302-unreal-script%} -- про отличия в связывании текстового и визуального языка с движком

`ecs`
дискуссии о вариантах ecs/cs и dod с точки зрения архитектуры и производительности
https://spiiin.github.io/tags/ecs/ -- набор ссылок


## Требование к языку/тулзам для разработки игр

- {% post_link 240520-cpp-in-gamedev-2 %} -- тут немного про проблематику разработки игр.

Язык для разработки игр должен быть:
`- быстрый` (для определенной части кода)
`- надёжный` (компилятор помогает находить проблемы)
`- гибкий` (для итераций, прототипов, и тюнинга геймплея -- иногда даже немного в ущерб первому требованию, ["Парето-оптимальная производительность"](https://youtu.be/IvHGczF6Go0?si=pWDCbiE2ccms_nP7&t=1395))
`- простой` (чем проще описывать предметную область -- игровую логику, тем лучше)

Требования скорости и надёжности более-менее пересекаются с общим направлением развития C++.

Хотя, кажется, насчёт `скорости`, полезное свойство языка в декларируемых zero-overhead рантайм-абстракциях, но не в абстракциях для лучшей работы с железом. Большая часть скорости получается даже не от легковесных рантайм-абстракций, а от лучшего соответствия данных и кода особенностям железа, на котором код выполняется, что достигается скорее использованием правильных библиотек, либо специфическим подходом к структурированию данных (Data oriented design).

![](240525-cpp-programmers-in-gamedev/desktop_power.png)
*картинка из прошлой статьи про C++ в геймдеве, только 3-5% производительности связано с аккуратным использованием языка*

Ну и понятно -- о скорости можно забыть в debug-билдах
[The sad state of debug performance in c++](https://vittorioromeo.info/index/blog/debug_performance_cpp.html)

Насчёт `надёжности`, местами сколько не добавляй в язык нового, из-за обратной совместимости необходима скорее дисциплина программистов. Т.е в принципе, надёжность может обеспечиваться дисциплиной в C++ ИЛИ использованием другого языка.

С `гибкостью` -- тут скорее необходимо брать другой язык, С++ для этого просто непригоден. Но так как о требованиях к гибкости редко говорят в мире C++, иногда бывает и так, что у программистов-плюсовиков просто не возникает ИДЕЙ, о том, что это приводит к ускорению разработки игр и созданию интересного геймплея.

>Меняя код запущенной игры, вы ускоряете весь процесс и проходите больше циклов в день, что, в свою очередь, повышает качество вашей игры. Раньше я использовал Scheme, Smalltalk и Python, но в целом подойдут любые языки программирования высокого уровня. Связать все воедино поможет Javascript
Jessie Schell, Геймдизайн. Как создать игру, в которую будут играть все.

*Очень* нестандартный набор с точки зрения программиста?

`Простота` тоже не является чертой C++. Количество нововведений в язык с каждой версией требует обновления знаний к новой версии стандарта.

*По разным причинам язык С++ иногда позволяет программисту сказать "I've only being doing C++ for 15 years. Can someone explain what is going on here?"*

- {%post_link 221010-simple-languages %}

Один из примеров разрастающейся сложности -- решение о разрешении использования в проекте новой версии стандарта языка. С точки зрения программиста плюсовика основным аргументом становится поддержка его компиляторами.

При этом не всегда заранее учитывается, для каждой отдельной новой фичи:
- насколько будет увеличен размер бинарника при активном использовании фичи
- время компиляции
- насколько хорошо та или иная фича в принципе продумана, и насколько хорошо реализована на уровне компиляторов ("поддерживается" -- не значит реализована оптимально)
- дополнительная семантическая/когнитивная нагрузка -- насколько в проекте станет больше различных идиом, приёмов, способов сделать что-то.
Т.е. "увеличится ли минимальное количество знаний, необходимое для того, чтобы программист игровой логики мог дописать код в произвольном месте" (ну, или в произвольном месте, отведённом для игрового кода). А также, сколько времени будет затрачено от абстрактного общего пула знаний, которые могут потребоваться игровому разработчику (вместо времени на получение дополнительных знаний по C++, он мог бы изучить что-то другое, настолько же или более полезное для разработки игр).

*иногда вообще кажется, что проще выучить язык, в котором уже хорошо реализована концепция, вводимая в стандартах C++, и только потом посмотреть, как перевести её на C++, чем изучать её на C++ сразу*

При этом с точки зрения функциональности игры в проект скорее всего не будет добавлено ничего.

*необходимый дисклеймер*
Эта заметка про программистов, и про их взаимодействие с геймдизайнерами, как **часть** специфики предметной области.

Есть и другие части, про которые тоже нельзя забывать:
`- Engineering` (как **programming integrated over time**) -- общие практика разработки. Эта часть более схожа с практиками в других областях разработки программ, хотя тоже имеет свою специфику. Ключевой литературы, посвященной именно геймдеву я не встречал, но тут либо подходит общая литература (только не забывать идиому **take everything with a pinch of salt!**), либо доклады с профильных конференций.
`- Геймдев как бизнес` -- менее связанно с непосредственно с программированием, но необходимо для представления, что такое профессиональная разработка игр. Материалы (**just a helicopter view on a problem**):
   **`Алексей Савченко - Игра как бизнес. От мечты до релиза`** -- разбор процесса создания игры, в основном про премиум-игры AA-класса. С начала и до конца. Из относительных недостатков -- высокий входной порог для понимания, не всегда легко отделить написанные кровью правила от личного опыта, мало ссылок ("изучите пайплайн производства арта у Disney")
   **`Development and Deployment of Multiplayer Online Games: from social games to MMOFPS, with stock exchanges in between`** -- MMO и сервисные игры. Не закончена. Много технической информации, немного про оперирование.
   **`Lovell Nicholas - The Pyramid of Game Design. Designing, Producing and Launching Service Games`** -- Free-to-play игры, геймдизайн и бизнес-модель.
   **`Jessie Schell - серия докладов про игровые студии`** -- [Information Flow: The Secret to Studio Structure](https://www.youtube.com/watch?v=y92-vkyHKbY), [Game Studio Leadership: You Can Do It](https://www.youtube.com/watch?v=O1zP6yJjc1o), [Game Studio Management: Making It Great](https://www.youtube.com/watch?v=-zRaFJHK0S4)

## Развитие C++
Куда двигался и двигается С++? (субъективно, не пересказ Committee's subgroups)
`- Борьба с наследием C и раннего C++` -- спрятать сырые указатели, убрать касты (больше способов передать компилятору информацию о связях типов), заменить метапрограммирование by accident на by design (меньше трюков с шаблонами), добавить больше возможностей говорить о корректности части программы. [Sean Baxter @Bloomberg: Circle Fixes Defects, Makes C++ Language Safer & More Productive](https://youtu.be/x7fxeNqSK2k?si=egaG1Vew66GVtjoT&t=308) -- C++ "bad defaults". Ориентиры -- Rust/D/Possible future C++ successor
`- Синтаксический сахар` -- добавления лямбд, deducing this, <=>, fold expressions, CTAD и прочее, сокращающее количество символов. Получается местами так себе (отчасти также из-за наследия [CppCon 2018: Timur Doumler “Can I has grammar?”](https://www.youtube.com/watch?v=tsG95Y-C14k), [Lambda Lambda Lambda](https://brevzin.github.io/c++/2020/06/18/lambda-lambda-lambda/), отчасти из-за того, что не любую синтаксическую "сладость" можно завернуть в zero-runtime overhead обёртку, в качестве примера можно пронаблюдать дискуссии про стандартизацию coroutines). Ориентиры -- Python/Ruby.
`- Возможности выразительности типов/функций` -- концепты, ranges, функциональные возможности, вычисления над типами. Последователи Alexandresku и Stepanov -- Sean Parrent, Odin Holmes, Louis Dionne/Ivan Cukic, Bartosz Milewski. [CppChat The Great Template Metaprogramming Library Debate](https://www.youtube.com/watch?v=eRFKCsysOqk) -- иногда выглядит, что каждый тянет в свою сторону, как, собственно, должно выглядеть метапрограммирование на C++. Ориентиры -- ML/Haskell/Lisp - очень разные идеи
`- Рефлексия/Compile-time evaluations` -- в принципе, то же, что и с предыдущим пунктом. [Ben Deane & Jason Turner “constexpr ALL the Things!"](https://www.youtube.com/watch?v=PJwd4JLYJJY) / [Don't constexpr All the Things - David Sankel](https://www.youtube.com/watch?v=NNU6cbG96M4) / [Reflection in C++ Next - Anton Bikineev](https://www.youtube.com/watch?v=NWIsRFDaHhs). Ориентиры -- D?. Хотя хотелось бы что-нибудь типа Haxe/Nemerle/Nim/Lisp/Smalltalk, или хотя бы Circle/LLVM.
`- Расширение std` -- Hazzard pointers, примитивы синхронизации, parallel stl, filesystem/networking/threading. Сложно, из-за большого scope С++ -- из-за необходимости поиска "наименьшего общего знаменателя" могут не приниматься доступные *почти* на любом современном железе/операционной системе вещи. [C++ Siberia 2019: Антон Полухин, C++ на практике](https://www.youtube.com/watch?v=g2iyNH2Gh1k) -- особенно интересная дискуссия в конце. Ориентиры -- Java/C#.
`- Game/Embedded/Low Latency` -- я не особо знаю идеи, пришедшие в стандарт оттуда, только общие мысли. Идеи альтернативной EASTL. DOD -- [CppCon 2018: Stoyan Nikolov “OOP Is Dead, Long Live Data-oriented Design”](https://www.youtube.com/watch?v=yy8jQgmhbAU) и [CppCon 2014 Mike Acton Data Oriented Design and C++](https://www.youtube.com/watch?v=92KFSD3ObrY). Low latency -- [What is Low Latency C++? - Timur Doumler - CppNow 2023](https://www.youtube.com/watch?v=EzmNeAhWqVs)

Уже не совсем язык, но:
`- Tooling` -- статический анализ, fuzzing, sanitazers, flamegraphs. Наверное, ещё LLVM с его API к компилятору. [CppCon 2017: Titus Winters “C++ as a "Live at Head" Language”](https://www.youtube.com/watch?v=tISy7EJQPzI)

В общем, хотя сам язык подходит для разработки игр, но развитие направлено *не совсем* в сторону упрощения решения проблем разработки игр. И не надо пытаться использовать для разработки игр только его.

## Материалы по геймдеву

*пока просто свалены в одну кучу*

`~meta`
[Gamedevs.org](https://www.gamedevs.org/) -- список презентаций и документов на различные темы в геймдеве. Почти все полезные.
[A study path for game programmer](https://github.com/miloyip/game-programmer) -- бесконечный список книг, местами для общего образования, а не необходимых каждому.
[GDC Vault](https://www.gdcvault.com/) -- огромный архив конференции, часть информации платная

`~engines`
[Game Engines with Source: Learning from the best](https://github.com/redorav/public_source_engines) -- список движков с исходниками. Как решаются возникающие в геймдеве проблемы в существующих движках. В отличие от других коллекций, здесь не все движки, которые удалось найти, а выборка приличного качества.
Блоги про разработку движков, старые, но не устаревшие. Часто содержат описание проблем и возможного пространства решений.
[Bitsquid](https://bitsquid.blogspot.com/) -- bitsquid/stingray
[Our Machinery](https://ruby0x1.github.io/machinery_blog_archive/)
[Molecular Matters](https://blog.molecular-matters.com/)
[Despair](http://gameangst.com/) + [GameArchitect](https://gamearchitect.net/category/despair-engine/)
https://solid-angle.blogspot.com/
https://diligentgraphics.com/
https://www.3dgep.com/ / render
https://engine-programming.github.io/

`~solodev`
https://floooh.github.io/
https://gist.github.com/bkaradzic (bgfx)
https://www.gingerbill.org/article/ (odin)
https://zylinski.se/
jonathan blow, http://number-none.com/product/ + разное
https://gamesfromwithin.com/category/game-tech

`~general`
https://aras-p.info/blog/ - Aras Pranckevičius, Unity
https://randygaul.github.io/
https://probablydance.com/
https://gafferongames.com/
https://journal.stuffwithstuff.com/
https://www.tomlooman.com/ - unreal
https://bronsonzgeb.com/
https://box2d.org/posts/
https://skypjack.github.io/
https://etodd.io/
https://allenchou.net/blog/
https://jobtalle.com/index.html
https://deepnight.net/tutorials/
https://caseymuratori.com/contents
https://dyn4j.org/tags#game-development
https://www.jeremyong.com/ - game dev general/graphics
https://stoyannk.wordpress.com/
https://deplinenoise.wordpress.com/
https://blog.demofox.org/
https://github.com/BobbyAnguelov/Esoterica - эксперименты Bobby Anguelov с системами анимации/ии.
mike acton
кармак

`~render (немного)`
Real-time rendering + ссылки оттуда на статьи/блоги/доклады
https://diaryofagraphicsprogrammer.blogspot.com/ - Wolfgang Angel, The Forge, пачка книг ShaderX/GPU Pro/GPU Zen
https://zeux.io/ - Arseny Kapoulkine, Roblox
https://mynameismjp.wordpress.com/ - Matt Pettineo, Sony
https://fgiesen.wordpress.com/ - Fabian “ryg” Giesen, RAD game tools
https://realtimecollisiondetection.net/blog/ Christer Ericson, Activision
http://c0de517e.blogspot.com/ - Angelo Peske, Roblox
http://eelpi.gotdns.org/ - Tom Forsyth, Valve
https://interplayoflight.wordpress.com/ - Kostas Anagnostou, Playground Games

https://x.com/SebAaltonen - Sebastian Aaltonen, Unity, Ubisoft, mobile render in hype-hype
https://x.com/mirror2mask - Natalya Tatarchuk, Activision, Unity


- {% post_link 210624-gamedev-links %} -- просто пачка разрозненных ссылок




