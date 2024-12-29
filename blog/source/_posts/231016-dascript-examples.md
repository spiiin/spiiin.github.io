---
title: daScript - решение задачек
abbrlink: 2385889062
date: 2022-10-16 17:00:11
tags: dascript
---

Решение нескольких алгоритмических задачек на `daScript`.
<!-- more -->

Задачки со старого собеса Nokia на C++ программиста (уже закрыли офис в России), [разбор](https://twitter.com/st_1ena/status/1419689924505260032)

## Вычислить первые N простых чисел
.. и вернуть результат в качестве массива.

```dascript
def calc_primes(n: int; var a:array<int>)
    a |> clear
    a |> reserve(n)

    a |> push(2)
    if n == 1
        return
    a |> push(3)

    let gen <- generator<int>() <| $()
        var t = 6
        while true
            yield t-1
            yield t+1
            t += 6
        return false

    var iterVal: int
    while length(a) < n
        next(gen, iterVal)
        var simple = true
        for prim in a
            if iterVal % prim == 0
                simple = false
                break
            if prim * prim > iterVal
                break
        if simple
            a |> push(iterVal)

[export]
def main
    var a: array<int>
    calc_primes(1000000, a)
    print("{a[length(a)-1]}\n")
```
https://github.com/spiiin/dascript_trivial_examples/blob/main/primes/primes.das

Тривиальная версия:

- чуть более улучшенная формула перебора чисел-кандидатов (вместо всех нечётных -- t*6+/-1) + проверка границы не корнем, а квадратом.
- не совсем понял, как хочет применить решето Эратосфена в варианте на C++ сама st_1ena, если нужны первые N простых чисел, а не "все числа меньшие N", то возникает подзадача оценить минимальное натуральное число, меньше которого точно окажутся N простых чисел, что также нетривиально, или построить ленивых фильтров, что совсем нетривиально на C++, и требует оценки памяти под эти фильтры.
- вместо этого, версия решения, которая может вычислить первые N чисел в compile-time -- в предположении, что у нас есть некоторое количество памяти, для сохранения решета эратосфена, эффективнее тогда потратить всю эту память на хранение предпросчитанных первых значений, и начинать рассчёт только сверх этих предпросчитанных чисел. На языках с макросами -- предпросчёт в compile-time выполняется той же функцией, что в run-time, т.е. не требует написания дополнительного кода.
[Версия](https://github.com/spiiin/dascript_trivial_examples/blob/main/primes/primes_mix_compile_runtime.das), которая сохраняет первый числа в кеш (макрос [cached_primes (count=200)] - с параметром, сколько чисел будет предпросчитано заранее)

## Посчитать статистику слов в тексте по длине слова

Задача на то, чтобы найти в стандартной библиотеке языка нужные функциии

```dascript
require fio
require strings
require daslib/strings_boost

[export]
def main()
    var strings : array<string>
    fopen("eng_to_rus.txt","rt") <| $(f)
        if f != null
            while !feof(f)
                strings |> push <| fgets(f)

    var counter : table<int; int>
    for str in strings
        var words <- str |> split_by_chars(" .,:-\n\t()%\"'")
        for word in words
            if word != ""
                counter[length(word)] += 1   //word length
                //counter[word] += 1         //word
    
    var freq_pairs : array<tuple<int;int>>
    for k, v in keys(counter), values(counter)
        freq_pairs |> push <| [[ tuple<int;int> k, v]]
    freq_pairs |> sort($(a,b) => !(a._1 < b._1))

    for pair in freq_pairs
        print("{pair._0} : {pair._1}\n")
```
https://github.com/spiiin/dascript_trivial_examples/blob/main/sort_words_stat_by_word_len/sort_words_stat_by_word_len.das

Решение в лоб - прочитать файл построчно, разбить на символы `split_by_chars`, обновляя в словаре значения количество слов. Дальше переложить значение в список пар, который отсортировать по первому элементу, и вывести на экран.
- Можно упороться по тому, чтобы выяснять у интервьюера, какие допустимы кодировки, разделители или что есть слова, как кажется подразумевали авторы задачи, которые потом расстроились, что ни один кандидат не учёл все возможные кейсы.
- Можно сохранять данные не в словаре, а сразу в списке пар `(длина слова, частота)`, не так то и много возможных длин слов. Сортировка такого списка пар в daScript - либо с помощью явной передачи функции сортировки, либо определением [оператора <](https://github.com/GaijinEntertainment/daScript/blob/17941ef0b0199dff0db27a2bee603db1a45b69b3/examples/test/unit_tests/sort.das#L20) для своего типа.

## Удалить из односвязного списка каждый пятый элемент

Интересно посмотреть на разницу в работе с памятью между C++ и daScript

```dascript
struct ListItem
    value: int
    [[do_not_delete]] next: ListItem?

def makeDemoList
    var head =  new [[ListItem value=1]]
    var current = head
    for i in range(2, 21)
        current.next = new [[ListItem value=i]]
        current = current.next
    return head

[sideeffects]
def deleteEveryFifth(lst: ListItem?)
    var counter = 1
    var current = lst

    while current != null
        if counter++ % 4 == 0
            var toDelete = current.next
            current.next = current.next?.next
            unsafe { delete toDelete; }
        current = current.next

def printList(lst: ListItem?)
    if lst != null
        print("{lst.value} ")
        printList(lst.next)
    else
        print("\n")

[export]
def main
    var list = makeDemoList()
    printList(list)
    deleteEveryFifth(list)
    printList(list)
    //freeList //or just kill context

//Output:
// 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20
// 1 2 3 4 6 7 8 9 11 12 13 14 16 17 18 19
```

https://github.com/spiiin/dascript_trivial_examples/blob/main/delete_list_every_5/delete_every_fifth.das

- Раз мы "играем в C++", то попробуем при удалении элемента из списка сразу же звать [финализатор](https://dascript.org/doc/reference/language/finalizers.html?highlight=finalizer) для него. Финализатор по умолчанию рекурсивно зовёт финализаторы для всех полей структуры. Это поведение можно изменить, если переопределить функцию `finalize`, или если пометить поле атрибутом `[[do_not_delete]]` (так как мы вручную измененяем указатели при удалении элемента, то элемент списка не отвечает за удаление следующего элемента по ссылке next).
- С помощью `options persistent_heap = true`, можно настроить также освобождение памяти после вызова финализатора (иначе за освобождение памяти отвечает хост-программа, один из паттернов быстрой работы с памятью -- грохнуть всю выделенную в цикле работы скрипта память разом).

## Вывести максимальное число, составленное из единиц двоичного представления заданного числа

```dascript
def popcount(x)
    var temp = x
    var count = 0
    while temp != 0
        temp &= temp - 1
        count++
    return count

def maxFrom1s(x)
    let count1s = popcount(x)
    var res = 0
    for i in range(count1s)
        res++
        res<<=1
    for i in range(31 - count1s) //assume 32 bits
        res<<=1
    return res 
[export]
def main
    print("{uint(maxFrom1s(256-1))}\n")  //'0xff000000'
```
https://github.com/spiiin/dascript_trivial_examples/blob/main/max_value_from_1s/max_value_from_1s.das

Тоже без заморочек, в лоб.

В продакшен-варианте, если нужно действительно быстро, решение прокидывается в C++, где задействуются всевозможные интринсики компилятора для того, чтобы получать кол-во битов так, как умеет процессор, или другие трюки для минимизации количества инструкций (развернуть циклы, и наложить кучу масок -- [Hamming weight](https://en.wikipedia.org/wiki/Hamming_weight)).

## Вывести список всех самых длинных путей в дереве
```dascript
require daslib/functional

struct Tree
    data : int
    left, right : Tree?

var tree = new [[ Tree data = 5,
    left = new [[Tree data = 1, 
        right = new [[Tree data = 2]]
    ]],
    right = new [[Tree data = 7,
        right = new [[Tree data = 10]]
    ]]
]]

//TODO: optimize
def clone_array(a: array<int>; newData:int)
    unsafe
        var newArr <- to_array(each(a))
        newArr |> push <| newData
        return <- newArr

def each_element(var tree:Tree?; path: array<int>; depth:int; blk:lambda<(what: int; path: array<int>; depth: int):void>)
    if tree.left != null
        each_element(tree.left, clone_array(path, tree.data), depth+1, blk)
    invoke(blk, tree.data, path, depth)
    if tree.right != null
        each_element(tree.right, clone_array(path, tree.data), depth+1, blk)

[export]
def main
    let startPath: array<int>
    var globalResult : table<int; array<array<int>>>
    unsafe
        tree |> each_element(startPath, 0) <| @[[&globalResult]](value: int; path: array<int>; depth: int)
            globalResult[depth] |> push_clone <| clone_array(path, value)
    //find max depth
    let maxDepth = reduce(keys(globalResult)) <| $(left, right : int)
        return left > right ? left : right
    //print all pathes
    print("All pathes with longest depth:\n")
    for path in globalResult[maxDepth]
        print("{path}\n")

//All pathes with longest depth:
//[[ 5; 1; 2]]
//[[ 5; 7; 10]]
```
https://github.com/spiiin/dascript_trivial_examples/blob/main/all_pathes_max_depth/all_pathes_max_depth.das

Туповатое решение, с кучей лишних копирований путей.

Можно оптимайзить. Либо по памяти, разделив обход на 2 -- сначала найти максимальную глубину, затем собрать только самые длинные пути. Либо в один проход, но сохраняя не полные копии путей, а альтернативное дерево с записью глубины каждой ветви рядом с указателем на оригинальные ноды left и right, по которому можно будет восстановить пути + обновляя максимальное значение глубины каждую итерацию.
