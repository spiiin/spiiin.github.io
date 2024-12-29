---
title: Профилирование размера программы
tags:
  - cpp
  - dev_method
  - link
abbrlink: 1465137776
date: 2024-05-15 23:49:45
---

Старый, но местами по прежнему актуальный цикл статей от авторов Despair Engine (F.E.A.R. 3) ([An Anatomy of Despair: Introduction](https://gamearchitect.net/2008/04/15/an-anatomy-of-despair-introduction/))

Автор выделяет 2 школы писателей игровых движков.

**`Low-level Faction`** - работающие с ранними консолями типа PS1 и DreamCast, работающие close to metal, избегая лишних абстракций и ориентирующиеся больше на тюнинг кода игры, а не движка. Майк Актон с его "**Software isn't platofrm, hardware is platform!**" как представитель этой школы. `Halo` как пример.

**`Abstraction Faction`** - автор приводит сюда Epic с их "отдадим 10% производительности за 50% ускорения в создании контекта" из доклада Тима Суини, и их блюпринты (хотя не совсем корректно считать такие небольшие отступления прямо согласием использовать абстракции, достаточно посмотреть на разницу их рендера для ios и android, **hardware definitively is platform!**). `Gear of War` как пример игры.

*Выбор фракции частично зависит не от идеологии разработчиков, а от волн развития технологий -- на ранних стадиях на платформах может не быть нормальной стандартной библиотеки, или нестандартное железо, а на поздних -- можно позволить себе занять свободные ресурсы системы*

*Код у представителей обеих факций ОЧЕНЬ разный, но обвешать абстракциями low-level код сильно проще, чем выбросить abstraction, когда ими обмазано всё. Сложно вытащить клоунов из набитой ими машины, лучше их туда не пускать - [ссылка](https://youtu.be/p65Yt20pw0g?t=112)*


Сам движок `Despair` использовал шаблоны, контейнеры stl и куски boost. Отчасти последствие такого выбора -- в блоге его коллеги, треть которого посвящена тому, как сделать, чтобы бинарник хоть как-то вмещался в память. Цикл статей полезен и сейчас, для таких же апологетов абстракций.

![](240515-binary-size/barbar_small.png)
*если я заплатил за телефон с 4 гигабайтами оперативки, то моя программа должна использовать все 4*

>Very few programmers, in my experience, really think about what the compiler and linker are doing with the code they write.  They design their code in C++, they write their code in C++, and of course they debug their code in C++.  Their view of the programs they write begins and ends at that level, which is certainly understandable since there is more than enough to worry about in C++ alone.

http://gameangst.com/?p=226 Minimizing Code Bloat: Template Overspecialization
http://gameangst.com/?p=212 Minimizing Code Bloat: Excessive Inlining
http://gameangst.com/?p=222 Minimizing Code Bloat: Static Allocations
http://gameangst.com/?p=224 Minimizing Code Bloat: Incorrect Inlining
http://gameangst.com/?p=246 Minimizing Code Bloat: Redundant Template Instantiation (extern templates)

Чуть более поздние исследования и тулзы:
https://aras-p.info/projSizer.html - лид-программист Unity
https://github.com/MolecularMatters/raw_pdb - от авторов мертвого уже движка [Molecule Engine](https://blog.molecular-matters.com/) (блог местами тоже хорош)

https://github.com/google/bloaty - гугловая мерялка (dwarf, экспериментально exe и wasm)
https://github.com/microsoft/SizeBench - и microsoft (по pdb)
https://github.com/surma/wasmphobia - wasm build size viewer as flamegraph ({% post_link 210814-flamegraphs %} -- вообще везде хороши)