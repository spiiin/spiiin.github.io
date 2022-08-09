---
title: Внутрь STL. Ссылки
abbrlink: 1366632532
date: 2021-07-18 15:33:14
tags:
 - cpp
 - link
---

Ссылки на тему особенности реализации классов библиотеки STL и других библиотек контейнеров.

<!-- more -->

Основные источники вдохновения, когда стандартных контейнеров STL не хватает: `EASTL`, `LLVM containers`, `Folly`, `Boost`.

[EA Standard Template Library](https://github.com/electronicarts/EASTL) - альтернативная стандартная библиотека от Electonics Arts, появившаяся ещё тогда, когда стандартные реализации были сомнительного качества и развивающаяся и сейчас.
[EASTL -- Electronic Arts Standard Template Library]( http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2007/n2271.html) - описание классов, отличий от STL и принципов дизайна.
[EASTL Best Practices](https://eastl.docsforge.com/master/best-practices/#summary) - сборник советов, как пользоваться.

[LLVM Data-structures overview](https://llvm.org/devmtg/2014-04/PDFs/LightningTalks/data_structure_llvm.pdf) - доклад Marcello Maggioni о структурах данных, используемых в LLVM.
[LLVM Programmer’s Manual](https://llvm.org/docs/ProgrammersManual.html) - более детальное описание

[Folly](https://github.com/facebook/folly) - набор библиотек Facebook.
[CppCon 2016: Nicholas Ormrod “The strange details of std::string at Facebook"](https://youtu.be/kPR8h4-qZdk) - доклад про реализию `folly::String`

[Boost](https://www.boost.org/doc/) - документация к библиотекам буст.
Многое из полезных буст библиотек уже и так в STL (нужно быть очень благодарным авторам Boost за это).
[Optimizing using an exotic associative container](https://cpp-optimizations.netlify.app/boost_flatmap/) - Boost flat_map to the rescue

[Zmeya](https://github.com/SergeyMakeev/Zmeya) - библиотека stl-like контейнеров для быстрой сериализации.
[Benchmark of major hash maps implementations](https://tessil.github.io/2016/08/29/benchmark-hopscotch-map.html) - бенчмарк реализаций хеш-таблиц.

[Stlab](https://stlab.adobe.com/) - стандартные библиотеки Adobe, расширяющие функционал STL. Подход немного отличается от стандартного ООП в сторону Value Oriented Programming, много материалов на [странице](https://sean-parent.stlab.cc/papers-and-presentations/) Шона Пэрента, с отсылками к Александру Степанову. Подход периодически разбирается на конференциях, пример - [Keynote: SOLID, Revisited - Tony Van Eerd - [CppNow 2021]
](https://youtu.be/glYq-dvgby4)

Доклад `The Performance Price of Dynamic Memory in C++ - Ivica Bogosavljevic` про различные аспекты оптимизации, часто ссылается на статьи из своего блога:
{% youtuber video LC4jOs6z-ZI %}
{% endyoutuber %}
[Process polymorphic classes in lightning speed](https://johnysswlab.com/process-polymorphic-classes-in-lightning-speed/) - статья со сравнением скорости обработки полиморфных объектов. Почти все статьи в блоге посвящены оптимизации, часто касаются структур данных и контейнеров из STL.

[Polymorphic Vector](https://github.com/ibogosavljevic/johnysswlab/blob/master/2020-08-polymorphism/polymorphic_vector.h) - класс для обработки вариантов полиморфных объектов.
[stack_alloc](https://howardhinnant.github.io/stack_alloc.html) - простая реализация кастомного аллокатора для STL-контейнеров.
[Intrusive hash](https://github.com/webcoyote/coho/blob/master/Base/Hash.h) - быстрые хеш-таблицы.

[C++ Performance: Common Wisdoms and Common “Wisdoms”](http://ithare.com/c-performance-common-wisdoms-and-common-wisdoms/) - много советов про выбор `STL` и `EASTL` контейнеров.

[Classes With Many Fields - Stanisław J. Dobrowolski](https://youtu.be/35y3OrsKq8c?t=303) - по таймингу ссылки на решения для сокращения объема классов в в проектах - Chromium, Firefox, LLVM, VLC, GZDoom.

[CPP Optimizations Diary](https://cpp-optimizations.netlify.app/) - блог со статьями по оптимизации C++-кода.
[Do you actually need to use std::map?](https://cpp-optimizations.netlify.app/dont_need_map/) - сравнение производительности поиска в `std::map` и `std::vector<std::pair<KeyType, ValueType>>`.

[Shahar's C++ posts](https://shaharmike.com/cpp/) - серия постов Shahar Mike с разбором реализации некоторых STL-классов.

Книги
[Scott Meyers books](https://www.aristeia.com/books.html) - суперполезная серия `Effective`, включая немного устаревшую `Effective STL` (лучше читать с пониманием, что изменилось в C++11/14/17).
[More C++ Idioms](https://en.wikibooks.org/wiki/More_C%2B%2B_Idioms) - Набор полезных материалов и ссылок с объяснениями идиом C++, в том числе используемых в библиотеках `STL` и `Boost`.
