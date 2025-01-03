---
title: Рандомные мысли про функциональные языки программирования
abbrlink: 3007069853
date: 2024-12-18 23:26:03
tags:
  - dev_method
  - fsharp
---

Решил поучаствовать в [AdventOfCode](https://adventofcode.com/2024) на [F#](https://github.com/spiiin/advent_of_code) ([лидерборд](https://adventofcode.com/2024/leaderboard/private/view/393584)). Не помню откуда, но знаю синтаксис ML (кажется когда-то на F# 2.0 смотрел), так что только немного прочитал про язык в общем, и поставил себе условие не скатываться в `let mutable x`, а писать в функциональном стиле. Немного заметок по ходу.

<!-- toc -->

## Деревья из данных и кода

Программист смотрит на код как на текст, но тулзам и компиляторам удобнее иметь более высокоуровневое представление. Для них программа -- это дерево выражений (AST). AST можно рассматривать как `model` в MVC, тогда как её текст - это `view/controller`.

При этом, если программист пишет программы, которые обрабатывают код  (плагины к ide/компилятору, кодогенераторы, синтаксические макросы, парсеры) -- то он должен знать не только синтаксис своего языка, но и работать с его синтаксическим деревом (если и программа, и код, который она обрабатывает на одном языке).

**Такая работа будет проще, если:**
- синтаксис программы удобно проецировать на генерируемый AST (код программы можно мысленно легко отобразить на дерево, и обратно). То есть синтаксис является не только вопросом вкуса, но и способом уменьшить ментальные усилия при программировании
- язык предлагает удобное представления для кода обработки деревьев (в основном -- что умеет и как расширяется pattern matching)
- язык предлагает средства трансформации своего собственного представления из одного в другое (цитирование, синтаксические макросы), чтобы изменять собсвенный синтаксический view.

["What next?"](https://graydon.livejournal.com/256533.html) - автор rust об идеях в языках программирования. *Open implementations* -- дизайн языка с предпосылкой о том, чтобы компилятор (или программист) был в любой момент "на связи" с программой ведёт к определённой эстетике языка, оказывает давление (в сторону программируемости) на синтаксис, систему типов, модель компиляции (*проще, единообразнее, программируемо*)

[Bicameral, Not Homoiconic](https://parentheticallyspeaking.org/articles/bicameral-not-homoiconic/) -- о Lispy-языках и идее `Syntax is a view`. Языки могут разделять *философию синтаксиса*, но отличаться в деталях.

*S-выражения удобны для представления синтаксического дерева, но не всегда удобны для человека. Имхо, философия синтаксиса ML намного приятнее. Хотя некоторые не любят ни скобок, ни значащих отступов. Но синтаксис -- это только "фронтэнд" языка, "бекэнд" -- это то, как компилятор/интерпретатор может обрабатывать построенное синтаксическое дерево. От синтаксиса эта не зависит почти никак*.

[21 compilers and 3 orders of magnitude in 60 minutes](https://d22yoqkt46k26p.cloudfront.net/graydon/talks/CompilerTalk-2019.pdf) - ML designed as implementation language for symbolic logic (expression-tree wrangling) system

Данные тоже удобно представлять как дерево (`json/xml/yaml/toml/cue/etc`) -- узлы могут быть атомами, либо деревьями данных. Форматы для описания данных обычно не предполагают описания правил интерпретации этих данных.

Но эволюция систем, которые используют описания данных в таких упрощенных форматах,  приводит их к тому, чтобы начать хранить внутри данных код. Причины могут быть разными:
- уменьшение избыточности описания (в качестве примера подойдут всякие текстовые template-движки, или какие-нибудь системы анимации типа [Nodezator](https://youtu.be/GlQJvuU7Z_8?si=iKBr9m4ELN0id2wC&t=1498)) 
- необходимость задания связей между различными частями одного описания, или с внешними данными/кодом (валидации значений, взаимо-зависимости, реактивная связь с внешним источником, пользовательские типы объектов с уникальными правилами конфигурации)
- желание описать поведение данных во времени
- необходимость сложной конфигурации с помощью данных (например xml в ant или spring)

Причём выбор способа представления такого кода внутри данных -- сложная задача. С одной стороны, не хочется опускаться до описания кода строками (ведь почти точно нужен не какой-то посторонний код, а обрабатывающий эти данные). С другой стороны, добавлять полноценный ast для кода внутри данных выглядит овер-инжинирингом. В итоге создаются упрощенные микроязыки, которые постоянно требуют расширения. 

*В качестве примера можно погуглить недоумение обнаруживающих, что в WPF XAML отсутствует оператор `not`*

[Ideas for a Programming Language Part 3: No Shadow Worlds](https://probablydance.com/2015/02/16/ideas-for-a-programming-language-part-3-no-shadow-worlds/) -- микроязыки как теневые разрастающиеся миры

Хорошие примеры "данных с внедрённым кодом" -- `табличные редакторы и SQL`.

## Списки из данных и кода
Код трансформации списков часто можно разделить на две части:
- как обрабатывается элемент списка,
- как соединяются обработанные коллекции вместе.

*код который на императивном языке выглядел бы линейно, тут разделяется на 2 части, соединение коллекций друг с другом -- оригами-программирование. При этом если встречается линейный код, обёрнутый в вычислительное выражение, то скорее всего между строк спрятано что-то монадное, и вычисления будут далеко нелинейными*

Синтаксис может либо способствовать визуальному/мысленному отделению этих потоков друг от друга, либо мешать.

[Ideas for a Programming Language Part 4: Reactive Programming](https://probablydance.com/2015/06/16/ideas-for-a-programming-language-part-4-reactive-programming/) - о синтаксисе для обработки списков.

```cpp
std::transform(vec.begin(), vec.end(), std::back_inserter(ovec), [](int a){ return a + 5; });
ovec.erase(std::remove_if(ovec.begin(), ovec.end(), [](int a){ return a > 10; }), ovec.end());
//сложно визуально отделить поток преобразований элемента (a -> a+5) и (a -> a>10) от потока транформаций
```

- {% post_link 220731-iterators %} - этот же синтаксический узор встречается не только в обработке списков, но и любых коллекций

В ML-синтаксисе без лишних скобок выглядит так:
```dascript
let ovec = 
	vec
	|> List.map (fun a -> a + 5) //or ((+) 5)
	|> List.filter (fun a -> a <= 10) //or (>=) 10)
//or |> List.choose (fun a -> if a + 5 <= 10 then Some(a + 5) else None)
//or |> List.collect (fun a -> if a + 5 <= 10 then [a + 5] else [])
```
Здесь легче отделить отделить поток оригами-функций для коллекций `map |> filter` от функций преобразования элемента. 
[Transducers by Rich Hickey](https://www.youtube.com/watch?v=6mTbuzafcII) - Рич Хики от том, что имя коллекции (`List.`) перед именами функций в принципе можно было бы и выбросить.

*В таком стиле необходимо отлично ориентироваться в наборе этих оригами-функций, поиск нужного иногда напоминает поиск подходящего кусочка пазла. Причём подходить могут несколько, но подобрать сходу какие именно, сложно. Порой даже забываешь, что Хиндли-Милнер твои друзья. Но в принципе, доверить поиск соединителей можно ИИ, главное, не забыть, что кроме соответвия типов, функции могут отличаться по поведению и выбрать из нескольких предложенных подходящую по поведению.*

[Functional Programming Is Not Popular Because It Is Weird](https://probablydance.com/2016/02/27/functional-programming-is-not-popular-because-it-is-weird/)

Из плюсов такого подхода -- часть вычислений можно распараллелить просто добавив в поток "оригами-функций" распараллеливание
```dascript
let more =
	sortedPaths
	|> PSeq.withDegreeOfParallelism Environment.ProcessorCount //обрабатываем параллельно
	|> PSeq.collect (fun path ->
		moves
		|> Seq.map (fun move -> path.Extend(move, endState, rate))
		|> Seq.filter filterPath
	)
	|> Seq.toList
```

[Vectorized Interpreters](http://venge.net/graydon/talks/VectorizedInterpretersTalk-2023-05-12.pdf) -- про векторизированные интерпретаторы, в которых можно избежать прыжков между вызывающим/вызываемым кодом. Происходит сначала настройка путей выполнения кода, а затем вызов вычисления всего построенного выражения в нейтивном коде (в качестве примеров -- `Numpy/R/Matlab`).
   
*настройка gpu на cpu перед запуском вычислений -- это тоже векторизированный интерпретатор*

*еще один отбитый вариант синтаксиса, берущий худшее из обоих миров (не видно ни 2 столбцов, ни императивности в теле лямбд) -- записывать все операторы в строку: `ovec =: (>. 10&<) @: (5&+)"0 vec`*

## Черепашки и синтонность
[Learnable Programming - Designing a programming system for understanding program](https://worrydream.com/LearnableProgramming/) - статья Виктора Брата о том, как проектировать системы так, чтобы можно было понимать написанные в них программы. Традиционно относится к обучению программированию, но полезно для любых систем.

*Брат и сам по себе крут, и часто ссылается на Алана Кея и Сеймура Пайперта*
>Maybe we don't need a silver bullet. We just need to take off our blindfolds to see where we're firing.

В статье приводится рекомендация книги [Seymour Papert's "Mindstorms"](https://worrydream.com/refs/Papert_1980_-_Mindstorms,_1st_ed.pdf), с описанием того, как проектировался и работает язык LOGO, и знаменитая черепашья графика в нём. Важное свойство черепашки -- **`синтонность`** другим объектам.

"Если не знаешь, как нарисовать с помощью черепашки круг, представь себя черепашкой". Даже ребёнок знает, как ходить по кругу, но не задумывается об алгоритме. Кроме того, более взрослый программист может не ходить по кругу, а моделировать работу черепашки с помощью листа бумаги и ручки. Компьютерная черепашка синтонна телу, или физическому роботу, который умеет выполнять те же команды. Но кроме этого она также синтонна математическому объекту, абстракции, с помощью которой можно понять принципы и приёмы программирования (аргументы, рекурсия, отладка), или дифференциальное исчисление. Черепашка позволяет развивать эмпанию так, чтобы было проще осваивать сложные концепции.

**В широком смысле, все доступные нам способы познания -- это разделение объекта на части+пересборка, и эмпатия (имперсонификация)** -- [теория категорий 1.1: Мотивация и философия](https://youtu.be/I8LbkfSSR58?si=OVQEC_tWjknqgALI&t=2085)
*(и эти навыки не обязательно коррелируют с умением решать логические задачки)*

Проблема функциональных языков в том, что у них нет своей черепашки, развивающей нужную интуицию ([1](https://byorgey.wordpress.com/2009/01/12/abstraction-intuition-and-the-monad-tutorial-fallacy/), [2](https://fsharpforfunandprofit.com/posts/why-i-wont-be-writing-a-monad-tutorial/)) - [Programming and Tacit Knowledge](https://mbuffett.com/posts/all-tacit-knowledge/) Наиболее полезная абстракция, кажется -- **`железнодорожные пути и паровозики с вагонами, в которых лежат данные`**.

## Про код как способ расширения существующих систем

Текстовый редактор может обращаться к структурам в AST, за данными для подсветки, рефакторинга или структурного редактирования. Если это нужно для интерактивного редактирования (т.е. всегда), то удобнее изменения дерева, а не строить его заново.

[Tree-sitter - a new parsing system for programming tools](https://youtu.be/Jes3bD6P0To?si=0G4Ugppx-qcp9w6B&t=957) by Max Brunsfeld - структурное выделение текста в редакторе.

Компилятор может иметь хуки для встраивания своих вычислений, чтобы (в порядке от простого к продвинутому):
- генерировать код -- templates в С++
- изменять код произвольным образом -- синтаксические макросы
- производить произвольные вычисления - [Jai](https://youtu.be/UTqZNujQOlA?si=37vNnAEI2fE13hBZ&t=4755) или [Type Providers](https://learn.microsoft.com/en-us/dotnet/fsharp/tutorials/type-providers/) в F#.

Если язык не проектировался с целью делать что-то во время компиляции, то встроить в него позже что-нибудь сложнее генерации кода будет сложно (и то, иногда парсинг кода проще сделать внешним препроцессором).

Метаинформация в коде может быть адресована не IDE/компилятору, а среде, в которой он будет выполняться -- какие-нибудь [аннотации](https://docs.godotengine.org/en/stable/tutorials/scripting/c_sharp/c_sharp_differences.html#onready-annotation)  для редактора в Godot или Unity. Это вроде не требуют особого синтаксиса, кроме конвенций об именах (которые вообще-то по хорошему тоже нужно заставить проверять компилятор, а не внешний скрипт, или хуже, run-time среду).
 
 Ну и, собственно, среда выполнения может уметь собирать из рантайм объектов, построенных с помощью этой метаинформации, другие составные объекты. Для построения помощью встроить скриптовый или визуальный язык (`Dataflow/Block/Event tables`), отличающийся от исходного языка. Или можно тащить в рантайм компилятор основого языка, если он не монструозный.
 
- {%post_link 240704-visual-languages%}
- {%post_link 240520-cpp-in-gamedev-2%} -- раздел про волны развития технологий. Более зрелый язык обрастает тулзами с способами связи его с внешними системами предметной области.
