---
title: daScript - мелочи
abbrlink: 1728452067
date: 2023-03-05 20:25:54
tags: [dascript]
---

Научился читать грамматику для bison, нашёл несколько новых для себя мелочей синтаксиса [daScript](https://github.com/GaijinEntertainment/daScript/blob/master/src/parser/ds_parser.ypp).
<!-- more -->

**`1. assume`**
Аналог `#define` в си, текстовая подстановка выражений. Со всеми ее минусами.

```dascript
var a = "global_string"

[export]
def main
    assume x = a //not capture global var a, but only text name
    var a = "local string"
    x = "changed string" //change local, but not global a!
    print("{a}\n")
    print("{::a}\n")
//changed string
//global_string
```

**`2. =>`**

Символ стрелки используется для записи коротких блоков/лямбд/безымянных функций:

```dascript
def radd(var ext:int&; b:block<(var arg:int&):int>):int
    return invoke(b,ext)
def radd(var ext:int&; b:lambda<(var arg:int&):int>):int
    return invoke(b,ext)
def radd(var ext:int&; b:function<(var arg:int&):int>):int
    return invoke(b,ext)

[export]
def main
    var x = 0
    radd(x, $(a) => a++) 
    radd(x, @(a) => a++)
    radd(x, @@(a) => a++) 
    print("{x}\n")
    //Output: 3
```

А также для записи создания кортежей и таблиц:

```dascript
    var x <- [[auto 1=>"one"]] //работает также в массивах [[auto 1=>"one"; 2=>"two"]]
    print("{x} {typeinfo(typename x)}\n")
    //[[ 1; one]] tuple<int;string> - кортеж
    var y <- {{ 1=>"one"}}
    print("{y} {typeinfo(typename y)}\n")
    //[[ 1 : one]] table<int;string> - таблица
```

**`3. auto для инициализации`**

auto при инициализации может выводить тип массивов (статических и динамических) и кортежей. Для структур -- не может

```dascript
def printType(a) { print("{typeinfo(typename a)}\n"); }
printType([[auto 1=>2]]) //tuple<int;int> const
printType([[auto 1,2]])  //tuple<int;int> const
printType([[auto 1;2]])  //int const[2]
printType([{auto 1;2}])  //array<int> const
```

**`4. сокращенная запись при обьявлении переменных ссылочных типов`**
```dascript
let a = 1
let ar& = a //let ar: int& = a
```

**`5. if после выражений`**
Условие может стоять после определённых выражений (с опциональной веткой else):

```dascript
def fun
    print("1") if true else print("2")  //expr if
    while true
        break if true else continue //break if
        continue if false //continue if
    return <- generator<int>() <| $() 
        for t in range(0,10)
            yield t if true //yield if
        return false if true //return if
```

**`6. aka`**
Синоним для имени переменной (как намного менее "злобный" вариант `assume`)
```dascript
var a aka b: int
b = 1
print("{a}\n") //1
```

**`7. expect`**

Ключевое слово для тестового фреймворка [dasTest](https://borisbat.github.io/dascf-blog/2023/02/25/wake-up-and-test-the-damn-thing/)
```dascript
expect 10003:1, 20000:1
//ожидается по одной ошибке компилятора типа 10003 и 20000 (незакрытая кавычка и неожиданный конец файла)
[export]
def test
    print("ok
```
Для запуска теста нужно вызвать скрипт [dastest](https://github.com/GaijinEntertainment/daScript/tree/master/dastest) и передает в параметре `test` имя скрипт для тестирования (или директории с группой скриптов):
```
daScript dastest.das -- --test my_test.das
```

**`8. named arguments`**

Функцию можно вызвать с [явными именами](https://dascript.org/doc/reference/language/functions.html?highlight=named#named-arguments-function-call) аргументов.

```dascript
def foo(a:int=13; b: int)
    return a + b
foo([b = 2])  // same as foo(13, 2)
```

Также можно скомбинировать первые неименованные аргументы, или вызов через пайп:

```dascript
def func(a:int; b=1; c=2)
  pass

func([a=0, c=2]    //ok
func(0, [c=2])   //error
0 |> func([c=2]) //error
```
[Больше примеров](https://github.com/GaijinEntertainment/daScript/blob/master/tests/language/named_call.das). Логика выбора -- именованные аргументы применяются после неименованных и могут "перекрывать" их.

**`9. with`**

[with](https://dascript.org/doc/reference/language/classes.html?highlight=class#implementation-details) позволяет внутри блока обращаться к полям структуры без явного указания её имени:

```dascript
struct S
    a, b: int

var s = [[S a=1, b=2]]
with s
    print("{a}, {b}\n") //s.a, s.b
```

