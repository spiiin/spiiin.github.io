---
title: "daScript: обобщенное программирование"
abbrlink: 2629978232
date: 2023-01-21 23:33:14
tags: dascript
---

Обобщенное программирование -- одна из серых, но важных и интересных сторон daScript. "Серость" темы связана с тем, что, во-первых, система типов не очень детально описана в документации, во-вторых -- в рассуждениях о типизации можно от практики быстро уйти в дебри академических терминов, в-третьих, тема плохо укладывается в голову C++-программисту.

Поддержка обобщенного программирования в языке, если "на пальцах" -- совокупность способов вызывать одну функцию для разных типов.

## Перегрузка функций

Перегруженные функции (ad-hoc полиморфизм) -- простейший способ определить функцию для двух различных типов

```cpp
def func(a : int)
    print("{a}\n")
def func(a : float)
    print("{a}\n")
[export]
def main
    func(1)
    func(1.0f)
```

**`Константность`**

Напечатаем тип параметра-аргумента:
```cpp
def func(a : int)
    print("{typeinfo(typename a)}\n")
//Output:
int const
```

По умолчанию к типу был добавлен спецификатор `const`, который не позволяет поменять значение аргумента. Его можно убрать, добавив ключевое слово `var`:
```cpp
def func(var a: int)
    print("{typeinfo(typename a)}\n")
//Output
int
```

При выборе перегрузки, константная и неконстантная версия, в отличие от C++, не имеют приоритета друг перед другом и при нахождении двух вариантов функции `daScript` выдаст ошибку ([Правила выбора функции](https://dascript.org/doc/reference/language/functions.html#function-overloading)). 
```cpp
var a: int
func(a)
//Output
30304: too many matching functions or generics func
candidates:
        func ( a : int const ) : void at generics.das:3:4 //принимает int и int const
        func ( a : int -const ) : void at generics.das:9:4 //-const читается как "удалить у типа спецификатор const"
```

Для того, чтобы daScript различил функции, можно добавить [спецификатор типа](https://dascript.org/doc/reference/language/generic_programming.html#type-contracts-and-type-operations) `== const` ("константность аргумента должна совпадать).
```cpp
def func(a : int ==const)
    print("{typeinfo(typename a)}\n")

def func(var a : int ==const)
    print("{typeinfo(typename a)}\n")

[export]
def main
    var a: int
    func(a)
    func(1)
//Output:
int ==const
int const ==const
```

**`Ссылки`**

В предыдущем примере аргумент передавался по значению, поэтому даже `var int` не позволяет изменить переданную переменную (меняется **значение аргумента**, а не оригинальная переменная). Возможно передать аргумент по ссылке:
```cpp
def func(var a : int&)
    a = 42

[export]
def main
    var a: int
    func(a)
    print("{a}\n")
//Output: 42
```

** Все непримитивные типы передаются по ссылке, независимо от того, был ли описан аргумент со спецификатором `&` или без него. **

```cpp
struct A
    a : int

def func(var arg : A)
    arg.a = 42
    print("{typeinfo(typename arg)}\n")

[export]
def main
    var a : A
    func(a)
    print("{a}\n")
//Output
A
[[ 42]]
```
*(причём можно описать 2 перегруженные функции с аргуметами типа A и A&, несмотря на то, что для структур семантически это будет идентичная запись)*

При этом, как и с константностью, компилятор не различает приоритета перегрузки функций с аргументом-ссылкой и значением, и выдаёт ошибку неоднозначности разрешения перегрузки.

```cpp
def func(var a: int)
    pass
def func(var a : int&)
    pass

[export]
def main
    func(1) //ok
    var a: int
    func(a) //30304: too many matching functions or generics func
            //candidates:
            //func ( a : int -const ) : void at generics.das:1:4
            //func ( a : int& -const ) : void at generics.das:3:4
```

**`Контракты`**

Макросы работают раньше разрешения перегрузки, что позволяет реализовать паттерн [contracts](https://github.com/GaijinEntertainment/daScript/blob/e7992b384dad13c1a201f9eee1c6a6ae1e0cf8b8/daslib/contracts.das) -- произвольную функцию, которая предварительно проверяет тип аргументов:

```cpp
require daslib/contracts

[!expect_ref(arg)]
def func(var arg : int)
    print("{typeinfo(typename arg)}\n")

[expect_ref(arg)]
def func(var arg : int&)
    print("{typeinfo(typename arg)}\n")

[export]
def main
    var a: int
    func(a)
    func(1)
//Output:
int //must be int&
int
```
https://github.com/GaijinEntertainment/daScript/blob/master/examples/test/misc/contracts_example.das
*вывод typeinfo, кажется, содержит [баг](https://github.com/GaijinEntertainment/daScript/issues/393)*

**`Временные ссылки`**

Кроме обычных ссылок в daScript есть временные ссылки, которые позволяют работать с объектами из C++-кода внутри блоков. Временная ссылка доступна только внутри блока, и не может быть сохранена вне его (но может быть передана в другую функцию, принимающую временные объекты).

Рассмотрим для примера C++ тип `Color` из [туториала к daScript](https://github.com/GaijinEntertainment/daScript/blob/master/examples/tutorial/tutorial03.cpp#L15). Для него создаётся daScript-обёртка, в которую можно добавить декларацию конструктора и инициализатора с помощью паттерна `using` -- в этом случае можно создать временную ссылку на тип, которая будет доступна только внутри блока: 

```cpp
//cpp
Module_Tutorial03() : Module("tutorial_03") {   // module name, when used from das file
    ModuleLibrary lib;
    ...
    addCtorAndUsing<Color>(*this, lib, "Color", "Color");
}
//das

require tutorial_03

def printColor(c : Color) //same as Color& as c is struct
    print("{typeinfo(typename c)}\n")

def printColor(c : Color#)
    print("{typeinfo(typename c)}\n")

[export]
def test
    let c = [[Color]]
    printColor(c)
    using() <| $(var c_temp : Color#)
        printColor(c_temp)
//Output
tutorial_03::Color const
tutorial_03::Color const#
```
**Если тип нельзя [скопировать или переместить](https://github.com/GaijinEntertainment/daScript/commit/9521fdba38c4f5ea422450c6b4979cc2808f58ef), то `using` не будет не будет создавать временный тип -- аргумент и так не сможет покинуть блок**

Чаще всего нет необходимости в раздельной обработке обычных и временных ссылок, в этом случае можно добавить к типу аргумента спецификатор `implicit`:

```cpp
def printColor(c:Color implicit)
    print("{typeinfo(typename c)}\n")
//Output
tutorial_03::Color const implicit
tutorial_03::Color const implicit
```

Небольшое отличие в том, как будет трактоваться аргумент:
```cpp
def printColor(c:Color implicit)    // accepts Color and Color#, a will be treated as Color
def printColor(c:Color# implicit)   // accepts Color and Color#, a will be treated as Color#
```


**`Указатели`**

Как и в C++, указатели -- это ссылки, которые могут указывать на `null`, также имеют чуть другую семантику, что позволяет уже без шаманства иметь перегрузки для значения и указателя.

```cpp
require daslib/safe_addr

def func(var a: int)
    print("{typeinfo(typename a)}\n")

def func(var a: int?)
    print("{typeinfo(typename a)}\n")

[export]
def main
    var a: int
    var a_ptr: int? = safe_addr(a)
    func(a)
    func(a_ptr)
//Output
int
int?
```

**`Приведение базовых типов`**

Базовые типы не приводятся друг другу неявно, требуется явный вызов конструктора типа (*Explicit is better than implicit*).

```cpp
def func(a : int) {}
def func(a : float) {}
def func(a : int4) {}
def func(a : bool) {}
def func(a : uint) {}
def func(a : int64) {}

[export]
def main
    func(1) //int
    func(float(1)); func(1.0f) //float
    func(int4(1)) //int4
    func(true) //bool
    func(uint(1)); func(1u); func(0x1) //uint
    func(int64(1)); func(1l) //int64
```


**`Приведение классов/структур`**

Для типов, поддерживающих наследование, неявно выполняется приведение указателей и ссылок от дочернего к родительскомму типу ([LSP](https://en.wikipedia.org/wiki/Liskov_substitution_principle)).

```cpp
struct A 
    a : int

struct B : A
    b : int

def func(a : A)
    print("{typeinfo(typename a)}\n")

[export]
def main
    var a : A
    var b : B
    func(a)
    func(b)
//Output:
A const
A const
```

Приведение типов структур (`cast/upcast/reinterpret`):
```cpp
    var a : A
    var b : B

    var refA : A& = a
    var refB : B& = b

    //downcast, safe
    refA = cast<A&> refB 
    //upcase, unsafe
    unsafe
        refB = upcast<B&> refA
    //reinterpret cast, VERY unsafe, can cast any
    unsafe
        refA = reinterpret<A&>(1) //will crash
```

**При выборе перегрузки функции выбирается та, для которой нужно выполнить наименьшее количество преобразований (при равном количестве daScript выдаст ошибку неоднозначности выбора)**

```cpp
struct A 
    a : int

struct B : A
    b: int

def func(var a : A?)
    print("a: {typeinfo(typename a)}\n")

def func(var b : B?)
    print("b: {typeinfo(typename b)}\n")

def func4(var a,b,c,d: A?)
    print("AAAA\n")

def func4(var a,b,c: A?; var d: B?)
    print("AAAB\n")

def func4(var a,b : A?; var c: B?; var d: A?)
    print("AABA\n")

def func4(var a,b,c,d: B?)
    print("BBBB\n")

[export]
def main
    //simple cases
    var refA = new A()
    func(refA) //a: A?
    var refB = new B()
    func(refB) //b: B?
    var refAB = cast<A?> new B()
    func(refAB) //a: A?

    //advanced cases
    func4(refA, refA, refA, refA) //shortest LSP to AAAA = 0
    func4(refA, refA, refA, refB) //shortest LSP to AAAB = 0
    //func4(refA, refA, refB, refB) //shortest LSP to AAAB/AABA = 1, conflict error
    func4(refA, refB, refB, refA) //shortest LSP to AABA = 1
    func4(refB, refB, refB, refB) //shortest LSP to BBBB = 0
```

**`explicit`**

Для того, чтобы отключить LSP приведение типа аргумента, можно добавить ключевое слово `explicit`. Так 

```cpp
struct A 
    a : int

struct B : A
    b : int

def func(var a : A explicit)
    print("{typeinfo(typename a)}\n")

[export]
def main
    var a : A
    var b : B
    func(a)   //A
    //func(b) //invalid argument a (0). expecting A explicit -const, passing B& -const

```

**`Приведение generic-типов`**

В документации не описана работа с generic-типами (и не дано общее определение для них, также пока отсутствует возможность создания своих типов), но поиском по коду находятся такие встроенные типы (исключая те, которые связаны с оператором typeinfo и кастами):

```
Функциональные объекты:
block
function
lambda

Коллекции:
array
table<key>
table<key, value>

iterator
generator
smart_ptr
tuple
variant
```

Для таких типов, возможно явное LSP-приведение для типов их аргументов (`ковариантность`). Пример для функций:

```cpp
struct A 
    a : int

struct B : A
    b : int

def func1(var a : A)
    print("a\n")

def func2(var b : B)
    print("b\n")

def highOrder(func: function<(var a:A):void>)
    invoke(func, [[B]])

[export]
def main
    highOrder(@@func1)
    highOrder(cast<function<(var a:A):void>> @@func2) //возможно привести тип function<(var b:B):void> к function<(var a:A):void>
```

## Generic-функции

Вернёмся к самому первому примеру -- если мы хотим написать функцию, семантически одинаково обрабатывающую различные типы (например, выводящую значение типа с помощью функции `print`) для типов. Чтобы не реализовывать её для каждого нового типа, в языках программирования используется понятие generic-функций, которые могут производить конкретные функции для новых типов автоматически.

[Обзор реализаций в языках](https://habr.com/ru/company/piter/blog/656377/).

Шаблонные функции в C++ производят код конкретных функций на уровне текста, который отдаётся компилятору (если не ошибаюсь, компилятор visual studio в этом плане действительно генерирует полные копии, не остлеживаю возможных повторов, чтобы иметь больше простора для частных оптимизаций функции под конкретные типы, а clang чуть раньше начинает отслеживать потенциально идентичные реализации для экономии памяти).

Другой возможный вариант реализации в Java -- "изображать" generic на высоком уровне для контроля типов, но оставлять одну реализацию (все объекты передаются по ссылке, добавляется overhead при работе с value-типами по боксингу/анбоксингу в обёртку).

Третий путь из C# -- добавить поддержку generic-функций в виртуальную машину, в этом случае возможна комбинированная реализация -- value-типы получают свои сгенерированные копии функций, а reference-типы -- общую функцию. Также возможно инстанцировать новые версии функций в runtime. daScript близок к такому типу реализации generic-функций.

**`Автоматический вывод типов`**

Если не указан тип аргумента функции, daScript выводит его автоматически, пример функции id принимающей аргумент любого типа и возвращающий его:

```cpp
options log=true, optimize=false

struct S1
    a: int
struct S2
    a: int

def id(T)
    return T

[export]
def main
    let a = id(1)
    let b = id(1.0f)
    let c = id([[S1]])
    let d = id([[S2]])
//Output

def `id ( T:int const explicit ) : int const
        return T

def `id ( T:float const explicit ) : float const
        return T

def `id ( T:S1 const explicit ) : S1 const
        return T

def `id ( T:S2 const explicit ) : S2 const
        return T

def public main
        let a:int const = __::`id(1)
        let b:float const = __::`id(1f)
        let c:S1 const = __::`id([[S1 ]])
        let d:S2 const = __::`id([[S2 ]])
```

По выводу текста сгенерированной программы понятна реализация. Символы подчёркивания перед именем функции `__::id` означают "взять реализацию функции только из текущего модуля" ([линк](https://dascript.org/doc/reference/language/modules.html#module-function-visibility)), идея будет рассмотрена далее.

Большая часть фич, связанных с generic-функциями, связана с тем, чтобы так или иначе задать или использовать информацию о типах.

**`auto`**

Определение для id более развернуто выглядит так:
```cpp
def id(a:auto): auto
    return a
```

Такая форма синтаксиса позволяет задать для каждого из выводимых типов псевдоним, который можно использовать для сравнения типа или получения rtti информации. Несколько примеров:

```cpp
//print typename
def func(a : auto(T))
    print("{typeinfo(typename type<T>)}\n")

//generic sum, a and b must be same type
def sum(a, b : auto(T))
    return a + b
```

**`Использование типа в качестве аргумента`**

Можно передать информацию о типе в качестве аргумента шаблона, как обычный `auto` аргумент.

```cpp
//generic linear interpolation between int types via cast to float type
def lerpi(a, b : auto(IntType); part : float; tempCastType : auto(CastType))
    return IntType(CastType(a) + CastType(b - a) * part)
print("{lerpi(int2(0, 0), int2(4, 4), 0.5f, type<float2>)}\n") // (2,2)
print("{lerpi(int3(1, 2, 3), int3(2, 4, 7), 0.5f, type<float3>)}\n") // (1,3,5)
```

Для того, чтобы тип не передавался в runtime, существует макрос [template](https://github.com/GaijinEntertainment/daScript/blob/master/daslib/templates.das#L41), который в compile-time убирает такие аргументы.

**`Шаблоны для auto`**

Различные формы [ограчений](https://dascript.org/doc/reference/language/generic_programming.html#type-contracts-and-type-operations) для типов аргументов auto. Примеры из доки

```cpp
def foo( a : auto&)           // accepts any type, passed by reference
def foo( a : auto[])          // accepts static array of any type of any size
def foo( a : array<auto -const>)  // matches any array, with non-const elements
//some tests
def foo(a: tuple<auto; auto; auto>) //tuple of 3 elements, any type
def foo(a: function<(a : auto) : auto>) //any function with 1 argument
def foo(a: table<int; auto>) //any tables with int keys
```

Еще раз приведу [ссылку](https://dascript.org/doc/reference/language/functions.html#function-overloading) на правила выбора функций при наличии нескольких специализаций и перегрузок.

**`Контракты`**

Так же, как и к аргументам обычным функциям, к аргументам generic-функциям могут быть применены контракты, позволяющие в более общем виде описать ограничения для типа аргумента. Именно c generic-функциями видна вся мощь контрактов.

```cpp
require daslib/contracts

//accept any functions
[expect_any_function(a)]
def foo(a: auto(T))
    print("{typeinfo(typename type<T>)}\n")

//accept any tuples
[expect_any_tuple(a)]
def bar(a:auto(T))
    print("{typeinfo(typename type<T>)}\n")

[export]
def main
    foo(@@(a : int) => a)                       //function<(a:int const):int const> const
    foo(@@(a : int; b: float) => "hello world") //function<(a:int const;b:float const):string const> const
    bar([[auto 1 ,2.0f, "test"]])               //tuple<int;float;string> const
    bar([[auto 1, 1]])                          //tuple<int;int> const
```

Контракты для одного аргумента могут комбинироваться с помощью операторов !, &&, || и ^^

```cpp
require daslib/contracts

[expect_any_function(arg) || expect_any_tuple(arg)]
def func_or_tuple(var arg : auto)
    print("{typeinfo(typename arg)}\n")

//expect_any_array разрешает любые массивы, expect_dim - статические массивы
[expect_any_array(arg) && !expect_dim(arg)]
def array_and_notdim(var arg : auto)
    print("{typeinfo(typename arg)}\n")

[export]
def main
    func_or_tuple(@@(a : int) => a)
    func_or_tuple([[auto 1, 2.0, "3"]])

    array_and_notdim([{ int[] 1;2;3 }]) //array<int> allowed
    //array_and_notdim([[ int[] 1;2;3 ]]) //int4[2] not allowed
```

**`Сумма типов`**

Еще один способ задать ограничения для типа -- перечислить разрешенные типы через символ `|` ([options](https://dascript.org/doc/reference/language/generic_programming.html#options) в доках):

```cpp
def foo(var a : int | float | string) //accept int or float or string
def foo(var a : array<int | float>) //array of int of array of float
def foo(a : function<(a : auto) : auto> | function<(a, b : auto) : auto>) //accept any function with 1 or 2 arguments
def foo (a : Bar explicit | Foo)   // accept exactly Bar or anything inherited from Foo
def foo (a : Foo | #) //accept Foo and Foo#, looks like this short syntax only works with #
```

Порядок проверки соответствия опций -- слева направо:

```cpp
def foo(var a : auto | int&) { a = 84; }
def bar(var a : int& | auto) { a = 42; }

[export]
def main
    var a: int
    foo(a) // match foo(auto)
    print("{a}\n") // a == 0
    bar(a) // match bar(int&)
    print("{a}\n") // a == 42
```

**`static_if`**

Проверка наличия методов или полей структуры выполняется в момент инстанцирования generic-функции

```cpp
struct S
    a : int

def foo(var s)
    s.a = 42 //not check if s has field

[export]
def main
    var s : S
    foo(s) //ok
```

Ошибка возникнет только в момент инстанциирования `foo` со структурой, не имеющей поля `a`. Проверить наличие полей или другую информацию о типе в время компиляции можно с помощью оператора `static_if`:

```cpp
struct S
    a : int
struct T
    a : float4

def foo(var s)
    static_if typeinfo(has_field<a> s) && (typeinfo(typename s.a) == typeinfo(typename type<int -const>))
        s.a = 42

var s : S
foo(s) //ok
var t: T
foo(t) //also ok, but do nothing
```

**`Вызываемые макросы`**

Более сложные конструкции вроде "вызвать конструктор того же типа, что и поле структуры `s.a` можно выразить с помощью макросов

```cpp
//generics macro
module generics_macro shared private

[call_macro(name="convert_to")]  // convert_to(convertType, arg)
class ApplyMacro : AstCallMacro
    //! convert_to("float4", 42) -> float4(42)
    def override visit ( prog:ProgramPtr; mod:Module?; var expr:smart_ptr<ExprCallMacro> ) : ExpressionPtr
        var exprConstStr <- unsafe(reinterpret< smart_ptr<ast::ExprConstString>&> expr.arguments[0])
        var call <- new [[ExprCall() name:=exprConstStr.value, at=expr.at]]
        emplace_new(call.arguments, clone_expression(expr.arguments[1]))
        return <- call

//
require generics_macro

def foo(var s)
    static_if typeinfo(has_field<a> s)
        static_if typeinfo(has_field<a> s)
            static_if typeinfo(typename s.a) == typeinfo(typename type<int -const>)
                s.a = 42
            else
                s.a = convert_to(typeinfo(typename s.a), 42) // --> s.a = float4(42)

var t : T
foo(t)
print("{t}\n")

//Output:
[[ 42,42,42,42]]

```

**`[generic]`**

daScript распознаёт обычные или generic-функции по синтаксису, но можно также явно обозначить функцию как generic:

```cpp
options log=true

[generic]
def func()
    print("hello")

[export]
def main
    func()

//Output:

def private `func
        print("hello",__context__)

// [modify_external]
[export]
def public main
        __::`func()
```

В таком случае вызов `func` будет преобразован в `__::`func` - вызов версии функции только из текущего модуля. Это используется в [некоторых функциях](https://github.com/GaijinEntertainment/daScript/blob/87ab585fc3704896bff3eea71ab87e29f772be94/src/builtin/fio.das#L10) стандартной библиотеки daslib, потому что если компилятор знает, что функция находится в том же модуле, что и вызывающий код, то может её оптимизировать -- при AoT-компиляции генериуется не полноценный вызов через ABI (который может вести в другой не-AoT daScript модуль), а прямой вызов, что быстрее.

**`[instance_function]`**

С помощью макроса `[instance_function]` можно попросить явно специализировать generic-функцию с определенными типами:

```cpp
require daslib/instance_function

def func(a : auto(TT))
    print("{typeinfo(typename a )}\n")

[instance_function(func, TT = "int const")]
def print_int(a) {}

[export]
def main
    print_int(1)
```

**`Видимость модулей`**

Для generic функций, которые подразумевают переопределение для новых кастомных типов в других модулях, необходимо добавлять префикс `_::` или `__::`, чтобы обозначить, что функций должна искаться в том модуле, который её вызывает.

```cpp
//module1.das
[export]
def call_func(a)
    _::func(a) //func will be declared somewhere later

//main.das
require module1

struct S
    a: int

def func(s: S)
    print("{s}\n")

call_func(s) //module1::call_func will see and call main::func()
```

`__::` -- подразумевает возможность определения функции только в том же модуле, что и вызывающий код (main)
`_::` -- допускает определение как в том же модуле, что и вызывающий код, так и в других модулях (main, module1 или другие модули)




