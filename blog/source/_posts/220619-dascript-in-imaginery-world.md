---
title: daScript in imaginery world
abbrlink: 1160489034
date: 2022-06-19 11:48:24
tags:
  - dascript
---

Мой собственный способ измерить выразительность и скорость языка -- решить на нём "задачу Джеймса Бонда младшего", выдуманную головоломку из игры на NES `James Bond Jr` ([видео](https://youtu.be/Kzu_cGHFqM8?t=1290)). Несмотря на игрушечность задачи, кажется, это неплохой тест нового языка. Это веселее, чем реализовывать абстрактный поиск в ширину/глубину. Задачу решаю с небольшими алгоритмическими оптимизациями, но без оптимизаций по мелочам (скорее, наоборот, массив чисел специально копируется, как решена первая версия задачи на питоне, чтобы решения были сравнивыми, чтобы симулировать "код новичка" на языка и посмотреть, как язык справляется с этим копированием).

Сразу выводы про `daScript` для тех, кому не особенно интересны подробности реализации:

-- Выразительность языка ОЧЕНЬ похожа на `Python`. Более того, я фактически просто переписал своё решение на `Python` 13-летней давности построчно, с парой изменений.
-- `daScript` по скорости **в режиме интерпретации** находится в одной лиге с компилируемыми языками (!!!). Код по скорости сопоставим с версией на `Nim` (чуть быстрее "наивной" **скомпилированной** версии, и раза в 1.5-2 медленнее оптимизированной).
-- В режиме `Ahead-of-Time` компиляции `daScript` обгоняет `nim` (который вообще показывает достаточно хорошие результаты в нормальных бенчмарках с другими языками).

<!-- more -->
Заметки
1 - {% post_link 090601-python-in-imaginary-world '(2009) Python in imaginary world' %} 
2 - {% post_link 150223-scala_in_imaginary_world '(2015) Scala in imaginary world' %}
3 - {% post_link 210504-nim-in-imaginery-world '(2021) Nim in imaginary world' %} 
Исходники
https://github.com/spiiin/james_bond_jr_problem

## Подготовка

Сборка автономного интерпретатора - проект `daScript` (можно в cmake поотключать дополнительные библиотеки типа `glfw`, ненужные для интерпретатора)
```
option(DAS_XXX_MODULE_DISABLED "Disable any unneeded modules" OFF)
```
Также не забывать собрать Release-версию. Теперь можно запускать скрипты из командной строки:
```
daScript.exe james_bond_jr.das
```

## Решение

{% spoiler gist %}
{% gist 3bd63cd5271b277f5bc87f670b0ab967 james_bond_jr_dascript.das %}
{% endspoiler %}

Отличия в синтаксис от `Python`:

**` - Отсутствует присваивание кортежей`**
Из-за чего нельзя написать сдвиг в массиве как в `python`:
```
n[0+plus],n[1+plus],n[2+plus],n[3+plus] = n[3+plus],n[0+plus],n[1+plus],n[2+plus]
```
и приходится писать отдельную функцию сдвига

**` - Нельзя сравнить два массива с помощью оператора проверки равенства`**
Что логично из-за неопределенности поведения такого оператора (сравнивать ли содержимое или указатели). Из-за этого используется самописная функция `same`:
```dascript
def same(var a,b: int[16])
    for ai, bi in a, b
        if ai != bi
            return false
    return true
```

**`- Поддержка именованных именованных кортежей без необходимости использовать отдельный класс`**
`Python` позволяет использовать [именованные кортежи](https://docs.python.org/3.6/library/collections.html?highlight=namedtuple#collections.namedtuple) вместо обычных там, где не хочется заводить структуру. В `daScript` возможность именовать поля кортежа встроена в язык:
```dascript
typedef FieldPathInfo = tuple<field:int[16]; fieldFrom:int[16];  rate:int>
var a = [[FieldPathInfo val, vert, rate(val)]]
```

**` - Ошибки вывода типа в генериках иногда напоминают вывод ошибок в шаблонов C++`**
https://github.com/GaijinEntertainment/daScript/issues/309

**`- Нет встроенного аналога list из Python и DoubleLinkedList из Nim`**
Вместо этого кортежи хранятся в классе `array`, представляющем собой динамический массив. Для того, чтобы избежать лишнего копирования данных при сортировке, память под кортежи выделяется на стеке:
```dascript
//медленный вариант
var open: array<FieldPathInfo>
open |> push <| [[FieldPathInfo source, rate(source), zeros]] //хранение в массиве объектов
//более быстрый вариант
var open: array<FieldPathInfo?>
open |> push <| new [[FieldPathInfo source, zeros, rate(source)]] //хранение в массиве ссылок на объекта на хипе
```

Также можно отметить, что объекты на хипе выделяются в соседних областях памяти, аллокатор контекста по умолчанию выделяет память из предвыделенного линейного блока:
```dascript
 for i in range(16)
    var xxx = new [[FieldPathInfo val, vert, rate(val)]]
    unsafe
        print("addr={reinterpret<void?> xxx}\n")

//output:
addr=0x28b1bb582f0
addr=0x28b1bb58380
addr=0x28b1bb58410
addr=0x28b1bb584a0
addr=0x28b1bb58530
...
```

Так что, в теории, разница в скорости в выделении объектов на стеке и в куче для `daScript` должна быть небольшой, и хранение узлов в массиве должно дать даже небольшой прирост скорости из-за локальности хранения узлов в памяти, по отношению к способу хранения в списке.

За исключением перечисленных отличий, код "переведён" построчно с Python версии (с "бонусной" проверкой ошибок типизации интерпретатором). В такой форме при интерпретации он уже работает лишь чуть медленнее скомпилированной версии на `Nim`.

## Ahead-of-Time компиляция

`daScript` можно настроить, чтобы вместо интерпретации он генерировал C++-код, выполняющий те же действия. В репозитория проекта есть [пример](https://github.com/GaijinEntertainment/daScript/blob/master/examples/tutorial/CMakeLists.txt#L36) настройки `cmake` для автоматической генерации AoT-версии кода.
Можно проделать этот этап вручную:
```
daScript.exe -aot james_bond_jr.das james_bond_jr.das.cpp
```

Полученный C++ файл можно скомпилировать (можно просто добавить его в один из туториалов), и теперь при выполнении скрипта `james_bond_jr.das`, вместо интерпретации, будут выполнены скомпилированные версии функций. В таком режиме скрипт обгоняет разогнанную `nim` версию решения. Выводы в начале.

![jbjr](220619-dascript-in-imaginery-world/jbjr.gif)

## Ещё быстрее!

Пара оптимизаций, чтобы сделать программу ешё быстрее.

**`[[unsafe_deref]]`**
аннотация для функций, которая "инлайнит" обращения по указателям.
Код из [ast_simulate](https://github.com/GaijinEntertainment/daScript/blob/a0fcdfdbf134d3dfb8055c9218c6e57ff4ae925b/src/ast/ast_simulate.cpp#L1023):
```cpp
    SimNode * ExprPtr2Ref::simulate (Context & context) const {
        if ( unsafeDeref ) {
            //симуляция выполнения ноды
            return subexpr->simulate(context);
        } else {
            //создание ноды для более поздней симуляции
            return context.code->makeNode<SimNode_Ptr2Ref>(at,subexpr->simulate(context));
        }
    }
```

**`Векторизация!`**
В daScript есть встроенные векторные типы int4 и float4, и описание поля логичнее переделать на их использование:
```dascript
//typedef Field = int[16]
typedef Field = int4[4]
```
Тогда горизонтальные сдвиги можно описать так:
```dascript
def right(var v:Field; line: int)
    var ans = v
    ans[line] = ans[line].yzwx
    return <- ans

def left(var v:Field; line: int)
    var ans = v
    ans[line] = ans[line].wxyz
    return <- ans
```

Что 1) короче 2) очень быстро

Можно измерить скорость выполнения обычной и оптимизированной версии встроенным профайлером:
```
profile(20, "JamesBondUsual") <|
        for i in range(100)
            var dif <- extract(search())
```

Получился прирост скорости ещё на 25% ( 0.4 -> 0.3 миллисекунд за 100 запусков).
Код быстрой версии:

{% spoiler gist %}
{% gist 5aba216fdf4aa70984c112cd4c6496df james_bond_jr_fast.das %}
{% endspoiler %}
