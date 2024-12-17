---
title: Заметки о языках программирования
tags:
 - dev_method
 - longread
abbrlink: 2297379949
date: 2021-05-26 18:57:06
---

Заметки о языках программирования
<!-- more -->

#Императивные языки

##Си
Хороший старт для изучения C или программирования вообще - книжка **`Кернига и Ритчи "Язык программирования Си"`** (TCPL).

*После прочтения её обнаружил, что курс программирования на C++ в моём университете был на 80% взят из этой книги (и оставшие 20% - краткий рассказ про классы*

Информации по современному си не очень много, но найти-таки можно:
[Modern C for C++ Peeps](https://floooh.github.io/2019/09/27/modern-c-for-cpp-peeps.html)
[One year of C](https://floooh.github.io/2018/06/02/one-year-of-c.html)
[Modern C and What We Can Learn From It - Luca Sas](https://youtu.be/QpAhX-gsHMs) - паттерны современного Си.

##Ortodox C++
[Orthodox C++](https://gist.github.com/bkaradzic/2e39896bc7d8c34e042b) - подход к использованию C++, с использованием небольшого подмножества языка, улучшающего Cи, но с отказом от современных фич, усложняющих понимание кода. Основная цель - упростить понимание написанного кода и исключить скрытые от программиста неочевидные эффекты.
[Not so modern C++](https://www.polymonster.co.uk/blog/not-so-modern-cpp) - статья Alex Dixon о выборе практичных частей C++.
[Safety](https://solid-angle.blogspot.com/2009/09/safety.html) - статья из блога Solid Angle.

##Zig
[Zig](https://ziglang.org/) - язык, который пытается исправить недостатки Си не надстройкой сверху, а изменением и удалением фич. Основные идеи (с сайта) - исключить скрытые эффекты, выделения памяти и макросы. Из добавлений - улучшение обработки ошибок, вычислений времени компиляции, что интересно - имеет в комплекте небольшой быстрый компилятор Си и систему сборки. Выглядит как небольшая и аккуратная альтернатива Си для тех, кому нужен Си вместо C++.
[Zig: A programming language designed for robustness, optimality, and clarity –  Andrew Kelley
](https://youtu.be/Z4oYSByyRak)
[The Road to Zig 1.0 - Andrew Kelley
](https://youtu.be/Gv2I7qTux7g)

##Jai
Разрабатываемый автором игр Braid и The Witness язык программирования для игр. Доступных компиляторов пока нет, основные идеи изложены в цикле видео:
[Jonathan Blow - A Programming Language for Games](https://www.youtube.com/watch?v=TH9VCN6UkyQ&list=PLmV5I2fxaiCKfxMBrNsU1kgKJXD3PkyxO&ab_channel=JonathanBlowJonathanBlow).
Короткое резюме по основным фичам (также много интересного про `C++`):
[The Jai Programming Language and What Can We Learn From It - Luca Sas [ACCU 2019]](https://youtu.be/roLD9-TA06Q)
[Jon Blow's Design decisions on creating Jai a new language for game programmers](https://youtu.be/uZgbKrDEzAs)

В языке много решений проблем, специфических для разработки игр. Навскидку, фичи - рефлексия, Data-oriented-design паттерны, выполнение кода и и кеширование результатов в compile-time, удобство рефакторинга (похожие синтаксические формы для анонимных-функций, блоков кода и методов), возможности по настройке расположения объектов в памяти, кастомные аллокаторы, стандартная библиотека в стиле SDL. Выглядит вкусно, хотелось бы увидеть в действии.

#Отступление 1. Эффективность языка

Что мы вообще ожидаем от языков программирования и почему пользуемся теми или иными?
Я немного касался этой темы в заметке {% post_link 210205-ten-years-gamedev '10 лет в геймдеве' %} в разделах **`"Языки программирования"`** и **`"Культура разработки"`**, а также в заметке {% post_link 210504-nim-in-imaginery-world 'Nim in imaginary world' %} в разделе **`Критерии выбора языка`**.

С помощью программирования мы решаем определённые задачи, и выбор языка в первую очередь в первую очередь состоит в том, насколько эффективно он позволяет решать определённый класс задач. Языки общего назначения позволяют решать широкий спектр задач, но в решении некоторых одни оказываются эффективнее других по какому-либо критерию.

{% blockquote %}
Эффективность языка в решении задач - главный технический критерий языка программирования
{% endblockquote %}


Языки, перечисленные выше, выбирают таким критерием `скорость работы конечной программы` - дизайн этих языков построен так, чтобы в ходе решения программист мог оценить, какой по быстродействию код получится на выходе. Примеры задач, для которых этот критерий является важным:
- построение систем, которые должны работать без задержек
- выполнение на компьютерах с ограниченными ресурсами
- задачи, в которых требуется максимальное быстродействие

С другой стороны, под эффективностью часто подразумевают `скорость решения задачи на выбранном языке`. Этот критерий во многих категориях задач перевешивает эффективность работы самой программы, поэтому ради того, чтобы решить задачу быстро, быстродействием программы пренебрегают в пользу абстракций более высокого уровня, а также "защиты от дурака" со стороны компилятора.

В этом случае критерием эффективности является простота использования языка. Важно не то, как много фич поддерживается языком, а то, насколько хорошо компилятор понимает, что мы хотим ему сказать. Чем больше он может сделать за нас – тем лучше. Любое усложнение языка/компилятора должно в конечном счёте увеличивать производительность программиста/команды.

Ещё один важный критерий эффективности (точнее, совокупность критериев) - `"поддерживаемость" языка`. Я понимаю под этим общую распространённость и доступность - в какой форме осуществляется поддержка компилятора и тулзов к нему (IDE, отладчики, системы сборки, менеджеры зависимостей etc), как часто язык меняется, как легко найти в интернете решение типичных проблем, и насколько сложно найти других программистов, которые готовы и способны изучить язык и писать на нём код. Это важно для любых языков, которые претендуют на то, чтобы быть востребованными в профессиональной разработке.

Из-за этого критерия часто для решения задач могут быть выбраны язык, программы на которых получаются медленными и пишутся долго, но которые хорошо поддерживаются - являются стандартом в индустрии, или за которыми стоят большие корпорации, и которые любят учить разработчики, чтобы много зарабатывать (*не буду показывать пальцем на такие языки*).

#Отступление 2. Масштабируемость

Главным критерием выбора языка для создания на нём больших систем является `возможность писать масштабируемые программы`. А в программировании рано или поздно любая система становится большой.

Важность этого критерия сложно описать в паре абзацев, и под этой эффективностью можно понимать очень многое. Например, можно перечислить:
- Поддерживаемые парадигмы программирования
- Способы для разделения частей программы (классы, модули)
- Спектр задач, которые можно решать с помощью одного языка
- Платформа (доступность библиотек, способ взаимодействия между частями системы)
- Совместимость системы созданной на языке, с различными аппаратными платформами и с другими системами (в том числе, на других языках)

В конечном счёте, язык должен помочь справится с двумя видами сложности, возникающими при масштабируемости программы:
- "Сложность в ширину" - растущий объем кода, который нужно разделять на независимые части
- "Сложность в высоту" - поддержка абстракций более высокого семантического уровня

Императивные языки, перечисленные выше, относятся к языкам среднего уровня, в которых можно проследить, какой код получается на выходе.

Высокоуровневые языки я бы разделил на две категории по тому, какой вид сложности они хотят сделать простым.

Одна из причин успеха "объектно-ориентированных языков" (`C++`, `Java`, `C#`, когда-то `Delphi`) - это их способ борьбы со "сложностью в ширину". Концепции, которые применяются в них для борьбы с этой сложностью, похожие, из-за чего программисты часто не видят особой разницы между этими языками и способны быстро изучать похожие новые языки.

Не сильно отличаются и другие языки из этой группы, которые берут на себя роль либо "склеивающих языков" ([Сценарии: высокоуровневое программирование для XXI века](https://www.osp.ru/os/1998/03/179470) - важная статья, описывающая такое применение, скриптовые - `Python`, `Perl`, `Tcl`, `JavaScript`), либо "языков управления частями программы" (`Python`, `Lua`, `Squirell`), жертвуя эффективностью ради некоторого повышения "сложности в высоту" - возможности отойти дальше от уровня железа.

Видео, которое достаточно просто и понятно объясняет, почему все языки программирования из Top-10 рейтингов - ООП-языки - **`Why Isn't Functional Programming the Norm? – Richard Feldman`** (несмотря на название, оно про причины популярности языков и не касается функционального программирования):
{% youtuber video QyJZzq0v7Z4 %}
{% endyoutuber %}

Из-за того, что дизайн этих языков сосредоточен вокруг решения проблемы уменьшения "сложности в ширину", встаёт вопрос о том, как они решают проблему роста "сложности в глубину", возникающей в ходе дальнейшей эволюции систем. Один из найденных путей - `создание вокруг языка стандартной платформы`, которая является нижним уровнем абстракции сама по себе (т.е. "прячет" от программиста решение низкоуровневых проблем и даёт большой набор библиотек для решения стандартных задач).

Цена такого подхода решения проблемы - языки работающие над платформой становятся уже немного менее "общего назначения" за счёт зависимости от своей платформ.

Примеры - самые известные и популярные - `.Net`, `Java` (общего назначения, над которыми сверху строились специальные новые языки), сильно уступающие по популярности платформы для Smalltalk типа `Pharo`. "Развёрнутый" случай - платформы, выстроенные над языком для решения более-менее конкретной задачи, вроде `Jupyter` для Python, `Rails` для Ruby, `Otp` для Erlang. Слитые вместе язык и платформа для ещё более конкретных целей - языки типа `Matemathica` или `J`.

Я не вижу особого смысла писать про какие-то из этих языков, потому что они мейнстримные и так у всех на слуху, а информации по них в интернете хватает. Остановлюсь только немного на C++, так как использую его в работе над играми, а затем перейду к менее известным языкам, которые пытаются решать проблему возрастания сложности "в высоту".

#С++
C++ - язык с богатой историей, выросший из C. Начальная история языка описана самим автором в книге **`"Дизайн и эволюция C++"`**. Книга сложная для чтения и бесполезная с точки зрения изучения языка, интересна именно с точки зрения того, в каких условиях находился Бьярн Страуструп в то время, когда проектировал первую версию языка.

Бьярн пользовался языком C, и решал проблему "сложности в ширину", добавив в C классы, чтобы с помощью них решить проблему масштабируемости. Инкапсуляция в языке решает проблему роста сложности в ширину, а наследование и полиморфизм - в глубину. История с ООП и классами хорошо освещается в видео **`Why Isn't Functional Programming the Norm?`**, которое было приведено в предыдущем разделе.

Отдельный интерес представляет постановка задачи сохранения максимальной обратной совместимости с C - как улучшить язык, не ломая то, что уже построено с помощью подмножества этого языка. Многие программисты сталкиваются с такой проблемой при улучшении своих фреймворков, движков, инструментов, и эта книга - одна из немногих, где описывается подход к решению аналогичных проблем на уровне проектирования языка программирования. Один из принципов добавления новых возможностей в C++ после создания `C with Classes` - делать так, чтобы получалось не медленнее, чем в C, потому что иначе программисты на C не будут этим пользоваться.

Также в книге много обсуждений того, как могли бы выглядеть различными варианты синтаксиса и ограничений, и почему был выбран именно тот вариант, который существует в C++. Важным требованием было использование существующего компоновщика C, т.е. C++ строился как платформа над C, чтобы получить возможность использования уже созданных инструментов (это требование всё равно накрылось с добавлением шаблонов - нормальные реализации требуют знаний о других единицах компиляции).

Кстати, отдельный вопрос, тоже связанный с языками программирования - почему получилось так, что на языке C было написано много кода? Детальный ответ есть в книге Эрика Раймонда **`"Философия программирования под Unix"`** – C был языком Unix, а Unix была операционной системой раннего интернета, и именно вокруг Unix образовалась хакерская субкультура и концепция свободного программного обеспечения. Отсюда видна ещё одна важная функция языка:
{% blockquote %}
Умение программировать на правильном языке означает причастность к сообществу/субкультуре программистов
{% endblockquote %}

(*я так когда-то чтобы понимать о чём пишут русскоязычные "функциональные" программисты в ЖЖ на начальном уровне изучил ocaml и haskell*)

Другая интересная тема из книги - создание и формат работы комитета C++, после которых удивляешься, как вообще язык движется вперёд, настолько это бюрократическая и политическая структура. При этом язык пытается учитывать интересы очень широкого круга программистов, использующих его.

Ещё один принцип дизайна – не добавлять фичи в язык без тщательного обдумывания, под девизом "Помни о [Vasa](https://ru.wikipedia.org/wiki/%D0%92%D0%B0%D0%B7%D0%B0_(%D0%BA%D0%BE%D1%80%D0%B0%D0%B1%D0%BB%D1%8C))" (которым Страуструп стращает всех [до сих пор](https://www.stroustrup.com/P0977-remember-the-vasa.pdf)). Хотя глядя на новые стандарты и все возможные правила и исключения, язык стоило бы назвать Vasa – C++ выглядит языком, который нужно продолжать изучать постоянно и бесконечно. Поэтому вместо добавления чего-то в ядро языка, это предлагается добавлять в сторонние библиотеки.

Тем не менее, C++ можно использовать, зная только некоторые его подмножества, спасибо ему хотя бы за это. Также С++ - это язык, на котором можно написать кроссплатформенный игровой движок, который с относительно небольшими усилиями будет почти одинаково работать под iOS/android/консоли/windows/mac/unix.

#Отступление 3. Масштабируемость вверх

Рост сложности "в ширину" мешает программистам работать над частями системы параллельно, и архитектуры, направленные на то, чтобы снизить эту сложность, "изолируют" подсистемы друг от друга. Хорошая книга про поиск способов борьбы с этой сложностью - **`"Мифический человеко-месяц"`** Фредерика Брукса.

Проблема роста сложности "в глубину" пока не особо волнует рядовых разработчиков, хотя способы справится с ней исследуются давно. Одно из её проявлений - ощущение того, что решение задач на "обычных" языках выглядит громоздко, требует написание большого количества повторяющегося кода, а подсистемы в большом количестве повторяют один и тот же функционал. 
[Система STEPS](https://www.computerra.ru/183817/steps/) - статьи об исследовании под руководством [Алана Кея](https://ru.wikipedia.org/wiki/%D0%9A%D1%8D%D0%B9,_%D0%90%D0%BB%D0%B0%D0%BD_%D0%9A%D1%91%D1%80%D1%82%D0%B8%D1%81), целью которого является поиск методов написать операционную систему на порядки меньшую по количеству строк кода, чем существующие.

Что интересно, исследования таких методов проводились ещё в 50х – рекурсивное описание языков, на которых пишутся более сложные языки, на которых пишутся ещё более сложные языки. В  **`"Руководстве пользователя Lisp 1.5"`** уже на 13-й странице в качестве примера даётся небольшая программа, которая является интерпретатором Лиспа на Лиспе (это скорее "фрактальный рост сложности") – это книга также вполне может быть первым учебником по программированию.

Способы создания новых языков, соответствующих предметной области - это либо отдельные утилиты для создания ["маленьких языков"](https://comp590-19s.github.io/), либо языки с системой макросов для расширения, сужения или изменения собственного синтаксиса, либо платформы для создания языков.

Классификация и терминология приводятся в книге Мартина Фаулера **`"Предметно-ориентированные языки программирования"`**.

[Метапрограммирование: какое оно есть и каким должно быть](https://habr.com/ru/post/258667/) - небольшая статья с обзором возможностей макросов в разных языках.

#DSL

Примеры способов описания Domain Specific Languages без циклического "повышения" сложности языков.

`Лексические и текстовые макросы`
Иногда для кодогенерации достаточно обычной текстовой подстановки в шаблоны (templating engine, [сравнение движков для подстановки](https://en.wikipedia.org/wiki/Comparison_of_code_generation_tools)). Пример практического использования - статья [Как мы делали нашу маленькую Unity с нуля](
https://habr.com/ru/company/playrix/blog/467827/), раздел `генератор кода` (парсинг размеченного файла, и замена в нём текста по шаблону на другой текста) или `макросы QT`.

Примеры DSL, не связанные с компьютером - [нотация вращения кубика Рубика](https://alg.cubing.net/) (интерпретатор - человек, семантическая модель - кубик Рубика), [жонглёрская нотация - siteswap](https://jugglinglab.org/anim?423) (кстати, возможно один из авторов - [Клод Шеннон](https://ru.wikipedia.org/wiki/%D0%A8%D0%B5%D0%BD%D0%BD%D0%BE%D0%BD,_%D0%9A%D0%BB%D0%BE%D0%B4)).

`Hexo`, `Jekyll`, и другие статические генераторы сайтов, хороший пример использования множества DSL, используют набор языков и надстроек над ними для генерации сайта - html, js, css, markdown, hexo nunjacks, sass + можно подключить свой парсер на javascript).

`mermaid`, `dot` и другие языки описания графов.

`JavaScript` как язык преобразований над DOM.

`Ruby on Rails` - пример использования языка, синтаксис которого достаточно гибкий, чтобы выглядеть как DSL без непосредственного написания DSL.

`Cmake` и другие декларативные системы сборки

#Языки для создания языков
Большинство языков поддерживают различные парадигмы, из-за чего многие программисты видят в новых изучаемых языках только ту часть, которую они знали до этого - *"На любом языке можно написать фортрановскую программу"*

*Языки программирования можно разделить по разным критериям: императивные, прикладные, логические, проблемно-ориентированные, и т.д. Но возникает ощущение, что все они представляют собой либо «агглютинацию (сочетания) свойств», либо «кристаллизацию стиля». COBOL, PL/1, Ada, и т.д., принадлежат к первому типу, а LISP, APL и Smalltalk – ко второму. Алан Кей*

##Генераторы анализаторов
`Lex/Yack`, `Antlr` и подобные утилиты служат генерации анализаторов грамматик языков. Парсер на выходе выдаёт абстрактное синтаксическое дерево, которое может быть обработано компилятором, или другим анализатором этого дерева. Если нужен свой микроязык или отличный от стандартных формат данных, с которым не может справится элементарное разбиение на лексемы из языка программирования - то можно попробовать.
*Я один раз в жизни возился с таким самописным генератором шейдеров из самописного языка в hlsl и glsl и помню, что разобраться в этом было достаточно сложно*

##Meta Programming System
[Jetbrains MPS](https://www.jetbrains.com/mps/) - система для создания языков. В отличие от генераторов анализаторов, на выходе получается не голое абстрактное дерево, а язык, полностью интегрированный с продвинутой средой разработки.
[Языково-ориентированное программирование: следующая парадигма](https://rsdn.org/article/philosophy/LOP.xml) - статья от Сергея Дмитриева, автора системы и концепции.
[Language Workbenches: The Killer-App for Domain Specific Languages?](https://martinfowler.com/articles/languageWorkbench.html) - Мартин Фаулер про Language Oriented Programming.

##Nemerle
[Nemerle](http://nemerle.org) - язык с мощными макросами, позволяющий изменять синтаксис и использовать расширение синтаксиса как библиотеки. Фичи Nemerle постепенно перетекают в C#.
[Серия статей на русском](https://rsdn.org/summary/3766.xml).
Изначально был написан под .Net, что являлось как плюсом для быстрой разработки компилятора, так и минусом. В процессе разработки был создан фреймворк для разработки языков N2, позже переименованный в [Nitra](https://github.com/rsdn/nitra). В дальнейшем автор хотел описать через Nitra C# и другие языки, в том числе создать на ней новую версию Nemerle. Проект масштабный, перешёл от разработки по фану к JetBrains, а затем снова вернулся к фанатской разработки одним человеком, к сожалению.
[CLRium #3: Язык программирования Nemerle (Влад Чистяков)](https://youtu.be/HSPivYkQ2t4)
[CLRium #3: Nitra. Средство создания языков программирования и не только (Влад Чистяков)](https://youtu.be/O693I7Yk4GY).

##Nim
[Nim](https://nim-lang.org/) - ещё один язык с макросами позволяющими строить и модифицировать AST во время компиляции программы.
Мои заметки про Nim:
{% post_link 210504-nim-in-imaginery-world 'Nim in imaginery world' %} (особенности языка и выполнения кода во время компиляции)
{% post_link 210521-nim-vk-get-pictures 'Nim vk-get-pictures' %} (в конце ссылки на примеры DSL на языке)
[C++ as Assembly 2.0 - Hello Nim - Viktor Kirilov - code::dive 2019
](https://youtu.be/8SoJR3sCaR4) - доклад про возможности Nim от Виктора Кирилова (ещё один интересный [доклад про hot-code reload](https://youtu.be/7WgCt0Wooeo) от него).
Основные тезисы доклада, что даёт метапрограммирование в `Nim`:
- Более высокий уровень уровень zero-cost абстракций:
 - помогает использовать паттерны
 - помогает увеличить читаемость и поддерживаемость кода
- Помогает строить DSL-и
 - DSL для HMTL
 - DSL для построения интерфейсов к библиотекам GUI и биндингов
- Ручное написание сериализации/десериализации в прошлом
 - интерация по полям структур во время компиляции - больше нельзя что-нибудь пропустить
- Не нужно 3rd-party движков для кодогенерации на уровне макросов или текста

##Racket
[Racket](https://racket-lang.org/) - язык семейства Lisp/Scheme. Позволяет создавать свои языки, в том числе и не лиспоподобные.
[Beautiful Racket](https://beautifulracket.com/) - книга про создание на Racket языков.
[Зачем ЯОП? Зачем Racket?](https://habr.com/ru/post/445822/) - перевод эссе из книги, со ссылками на примеры реализованных DSL.
[Современная игра для NES, написанная на Lisp-подобном языке](https://habr.com/ru/post/467125/) - DSL [CO2](https://gitlab.com/nebogeo/co2) для генерации NES-кода на Racket
[Lambda World 2019 - Language-Oriented Programming with Racket - Matthias Felleisen](https://youtu.be/z8Pz4bJV3Tk) - использование Racket для создания группы DSL для работы с видео.
[RacketCon 2013: Dan Liebgold - Racket on the Playstation 3? It's Not What you Think!](https://youtu.be/oSmqbnhHp1c) - доклад от Naughty Dog про создание языка для описания структур данных, генерирующего код десериализации, а также описание сериализаванных данных на этом языке для игры 
[Adventures in Data Compilation Uncharted: Drake’s Fortune](https://ubm-twvideo01.s3.amazonaws.com/o1/vault/gdc08/slides/S6636i1.pdf) - Ещё один старый доклад Naughty Dog про их Data Compiler (Naughty Dog вообще [большие экспериментаторы](https://en.m.wikipedia.org/wiki/Game_Oriented_Assembly_Lisp) с [лиспом в продакшене](https://all-things-andy-gavin.com/2011/03/12/making-crash-bandicoot-gool-part-9/)).

Пример кода описания данных из книги **`"Игровой движок. Программирование и внутреннее устройство"`** Джейсона Грегори (лид программист Naughty Dog):
```lisp
simple-animation.scm

;;тип
(deftype simple-animation()
	(name string)
	(speed float :default 1.0)
	(fade-in-seconds float :default 0.25)
	(fade-out-seconds float :default 0.25)
)

;;экземпляры
(define-export anim-walk
	(new simple-animation
		:name "walk"
		:speed 1.0
	)
)

(define-export anim-walk-fast
	(new simple-animation
		:name "walk"
		:speed 2.0
	)
)

(define-export anim-jump
	(new simple-animation
		:name "jump"
		:fade-in-seconds 0.1
		:fade-out-seconds 0.1
	)
)
```
```cpp
//генерируемый по схеме c++ код
struct SimpleAnimation {
  const char* name
  float speed;
  float fadeInSeconds;
  float fadeOutSeconds;
}

//использование
void loadFunction() {
	SimpleAnimation* pWalkAnim = LookupAnimation<SimpleAnimation*>(stringHash("anim-walk"));
}
```