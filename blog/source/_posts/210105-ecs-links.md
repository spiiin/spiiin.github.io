---
title: ECS. Ссылки
abbrlink: 381238762
date: 2021-01-05 01:09:45
tags: [gamedev, cpp, c#, link, ecs]
---

ECS - паттерн программирования, используемый в геймдеве. Основная идея - есть пул сущностей (`entities`), на которые можно добавлять компоненты (данные без логики - `components`). Сущности и компоненты читаются, модифицируются, создаются и удаляются только с помощью систем(`systems`). Подход немного отличен от традционного ООП, и от ECs (сущности разбиваются на  компоненты - логика хранится как в классах-сущностях, так и в компонентах), так что требует ознакомления и практики перед использованием
<!-- more -->

## История и примеры практического применения в больших играх

`Dungeon Siege` - [A Data-Driven Game Object System
](https://www.gamedevs.org/uploads/data-driven-game-object-system.pdf)
`Operation Flashpoint 2`
`GrexEngine` (движок для mmo-rpg) - [Cерия статей](http://t-machine.org/index.php/2007/09/03/entity-systems-are-the-future-of-mmog-development-part-1/), и ссылка ещё на одну презу из dungeon siege
`World of Tanks Blitz` - [Создание World of Tanks Blitz на базе собственного движка DAVA](https://habr.com/ru/company/wargaming/blog/245321/)
`Wooga` (немецкая студия, разрабатывает казуалки) - для матч-3 и стратегии. Ссылки на видео в следующем разделе.
`Overwatch` - Ссылка на видео в следующем разделе (в комментариях к ютуб лекции ещё несколько разработчиков игр отписывались, например `Mercenaries 2`)
`Minecraft` - Использует библиотеку [entt](https://minecraft.net/en-us/attribution/).

## Видео презентации
`Entitas - Entity System Architecture with Unity - Unite Europe 2015.`
Доклад от Макса Закса и Саймона Шмидта о библиотеке Entitas для Unity - идеи, и как совмещать объектами Unity.
{% youtuber video 1wvMXur19M4 %}
{% endyoutuber %}

`Unite Europe 2016 - ECS architecture with Unity by example`
От них же, практическое применение библиотеки Entitas для решения конкретной задачи, создания интерфейса в стиле Clash Royale.
{% youtuber video lNTaC-JWmdI %}
{% endyoutuber %}

`Кирилл Надеждин (Kumo Kairo) - ECS в разработке игр — хорошая архитектура приложений для всех`
Обзор entitas и ссылки на другие примеры использования ECS в играх, на русском. Примеры проблем, которые приводят к тому, чтобы перейти на ECS.
{% youtuber video pp5sYybOidg %}
{% endyoutuber %}

`Wargaming.net: Архитектура современных 3D движков (DevGAMM Minsk 2014)`
Архитектура современных 3D движков, Виталий Бородовский, Technical Director WoT Blitz
{% youtuber video 1zLqgQ_-F84 %}
{% endyoutuber %}

`Overwatch Gameplay Architecture and Netcode`
Разбирается внутренняя ECS близзрад. Cамая объёмная и сложная для понимания презентация, тут на 0.75 лучше смотреть. Почему пришли к применению ECS, с какими проблемами сталкивались и как их решали. Обзор после 3х лет использования такой архитектуры на практике.
{% youtuber video W3aieHjyNvw %}
{% endyoutuber %}

`itCppCon19 - ECS back and forth (Michele Caini)`
Обзор внутреннего устройства ECS на C++ - разбор двух типов архитектур - на основе "архетипов" и "разреженных множеств". Можно также почитать в ECS-FAQ (ссылка в следующем разделе)
{% youtuber video WB5bRKKGRUk %}
{% endyoutuber %}

`Game Engine Entity/Object Models`
Game Engine Entity/Object Models, Bobby Anguelov. Обзор различных архитектур, плюсы и минусы подходов EC и ECS в различных движках
{% youtuber video jjEsB611kxs %}
{% endyoutuber %}

## Обзоры библиотек
[Entity Component System FAQ](https://github.com/SanderMertens/ecs-faq ) - общий обзор подхода, терминология, список библиотек, примеры применения в продакшене.
[Entity-Component-Systems Benchmark](https://github.com/abeimler/ecs_benchmark) - бенчмарк различных библиотек
[EnTT](https://github.com/skypjack/entt) - production-ready c++ библиотека, используемая в `Minecraft`, с примерами использования (самый простой - [pacman](https://github.com/Kerndog73/EnTT-Pacman)), [документацией](https://github.com/skypjack/entt/wiki/EnTT-in-Action) и [блогом](https://skypjack.github.io/tags/#entt)
[flecs](https://github.com/SanderMertens/flecs) - c/c++ библиотека с большим количеством [примеров](https://github.com/SanderMertens/flecs/tree/master/examples) и функционала (есть модули для сериализации, рефлексии, продвинутое api для обращения с сущностями). [Мануал](https://github.com/SanderMertens/flecs/blob/master/docs/Manual.md)
[Entitas](https://github.com/sschmid/Entitas-CSharp) - библиотека на C# для использования с Unity (порты на другие языки можно не смотреть. Возможно, стоит смотреть сразу штатный ECS для Unity - Unity DOTS.

## Ссылки

[Обсуждение на gamedev.ru](https://gamedev.ru/code/forum/?id=198194&m=3785006#m8) - пост с большой коллекцией ссылок
[Entity Systems Wiki](http://entity-systems.wikidot.com/) - вики с терминологией, ссылками, список библиотек для разных языков.
[Artemis](http://gamadu.com/artemis/) - академическая реализация ECS на Java, посмотреть как задумано.

## Data-oriented Design (DoD)
Теория, если сходу не очень понятны идеи ECS.
[Data-Oriented Design](https://www.dataorienteddesign.com/dodbook/) - фундаментальная книжка по DoD от Richard Fabian
[Data Oriented Design Resources](https://github.com/dbartolini/data-oriented-design) - список материалов по DOD
[Data-Oriented Design (или почему, используя ООП, вы, возможно, стреляете себе в ногу)](https://habr.com/ru/post/472052/) - перевод статьи Noel Llopis
[Data-Oriented Design - Links and Thoughts](https://asawicki.info/news_1422_data-oriented_design_-_links_and_thoughts.html) - коллекция ссылок на статьи, многие gamedev-related.
[DOD в Battlefield](https://media.contentapi.ea.com/content/dam/eacom/frostbite/files/introduction-to-data-oriented-design.pdf) - исследование прироста скорости от правильного расположения структур в памяти, полезные ссылки в конце доклада
[Stoyan Nikolov “OOP Is Dead, Long Live Data-oriented Design”](https://www.youtube.com/watch?v=yy8jQgmhbAU) - видео доклада Стояна Николова с примером разницы подходов к решению практической задачи - OOP vs DoD.

Примеры библиотек, спроектированных с применением подхода data-oriented design:
[Dear ImGui](https://github.com/ocornut/imgui)
[bgfx](https://github.com/bkaradzic/bgfx)

**update 2023.11.03**
Еще пара ссылок по замерам производительности:

["Clean" Code, Horrible Performance](https://www.youtube.com/watch?v=tD5NrevFtbU) -- доклад от Casey Muratory, замеры на простых примерах Shape/Square/Circle
`Practical Optimizations` -- Jason Booth, замеры производительности и некоторые приёмы организации кода, связанные с DoD. 
{% youtuber video NAVbI1HIzCE %}
{% endyoutuber %}

Важные идеи:
**`Optimization is DESIGN time problem`**
**`Performance is a feature`**
