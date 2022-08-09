---
title: Runtime-полиморфизм в C++
tags:
  - cpp
abbrlink: 1552834708
date: 2021-05-31 22:50:18
---
Ссылки по нестандартному способу организации полиморфизма в C++, а также материалы Шона Пэрента (Adobe) по архитектуре программ.
<!-- more -->

`Лекция про организацию неинклюзивного полиморфизма`
{% youtuber video QGcVXgEVMJg %}
{% endyoutuber %}
*"My class T inherits from nothing"*

см также - идиома ["Type Erasure"](https://en.wikibooks.org/wiki/More_C%2B%2B_Idioms/Type_Erasure)

Также может послужить небольшим туториалом по rvalue-ссылкам и обзором преимуществ использование value-семантики для перемещаемых объектов.

Доклад является часть серии **`Better Code`** ([тут](https://sean-parent.stlab.cc/papers-and-presentations/) все доклады и дополнительные статьи).

Часть из них посвящена формальному математическому подходу к построению структур данных и алгоритмов, частично базируется на книге Александра Степанова и Пола Мак-Джонса [Elements of programming](http://elementsofprogramming.com/) (в интернете можно откопать русский перевод) и заметках [Notes of Programming](http://stepanovpapers.com/notes.pdf). Но некоторые представляют интерес не только со стороны фундаментальной подготовки.

`Другие лекции и материалы Шона`
[Sean Parent - Polymorphic Task](https://youtu.be/2KGkcGtGVM4) - подход, применяемый в первой статье, для написания класса task за 10 минут.
[Language Delay](https://sean-parent.stlab.cc/presentations/2013-03-05-language-delay/language-delay.pdf) - чистый C++ позволяет использовать 0.25% производительности компьютера (объяснение, где скрыты остальные 99.75% на [видео](https://youtu.be/zULU6Hhp42w?t=938)).
![desktop-power](210531-cpp-dynamic-polymorphism/desktop_power.png)
[Sean Parent “Better Code: Relationships”](https://youtu.be/ejF6qqohp3M) - про отношения между объектами в коде. Цель - написание кода без противоречий. Объяснение идеи контрактов и концептов.
{% blockquote %}
Архитектура - это искусство проектировать и конструировать структуры
{% endblockquote %}
[How did MVC get so Fed up?]("https://stlab.cc/tips/about-mvc.html") - описание "правильного" паттерна MVC версии Smalltalk. Видео-версия объяснения проблемы - в докладе [“Better Code: Human Interface”](https://youtu.be/0WlJEz2wb8Y?t=877). Цель правильного UI - **не врать**. Другой подход к упрощению ui - парадигма *immediate gui* и [Dear ImGui](https://github.com/ocornut/imgui) как известный её представитель. Ещё цитата из доклада:
{% blockquote %}
Таксономия всего в программе - коллекции, объекты, свойства, операции, отношения.
{% endblockquote %}

`Доклад, использующий идею runtime-полиморфизма`
[Louis Dionne “Runtime Polymorphism: Back to the Basics”](https://youtu.be/gVGtNFg4ay0) - про разные способы соединения классов с их виртуальным таблицами.

`REPL-интерпретатор C++ кода`
[Cling](https://github.com/root-project/cling) - удобен для экспериментов в стиле первого доклада.

С первым днём лета, пусть ваш код код остаётся простым и надёжным!