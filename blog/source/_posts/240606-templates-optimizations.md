---
title: Template optimizations
abbrlink: 4074204396
date: 2024-06-06 20:17:56
tags: cpp
---

Редкая тема -- ускорение compile-time вычислений.

[code::dive 2017 – Odin Holmes – The fastest template metaprogramming in the West](https://www.youtube.com/watch?v=ZpVPexZHYrQ) -- основные идеи
[C++Now 2017: Odin Holmes "Type Based Template Metaprogramming is Not Dead"](https://www.youtube.com/watch?v=EtU4RDCCsiU) -- использование в библиотеках
[CppCon 2019: Mateusz Pusz “Rethinking the Way We Do Templates in C++”](https://www.youtube.com/watch?v=oNBnYhLxlTU)
https://odinthenerd.blogspot.com/p/index.html - блог автора, статьи с примерами

`Rule of chiel`, список операций по времени с точки зрения компилятора:
- дорогое - SFINAE, инстанцирование функции, ~100-500x
- чуть менее дорогое - инстанциирование типа, под капотом у компилятора зовёт аллокацию, ~100x
- среднее - вызов алиаса, ~5x
- добавление параметра типа, ~5x
- добавление параметра в alias вызов, +1x
- повторный поиск уже запомненного созданного типа - 0x

Основная идея -- отделять типы от алгоритмов, чтобы не создавать новые на каждый вызов алгоритма.

На основе замеров, идиомы:
- alias conditional
- recursive alias
- composition with continuations
- fast tracking

[alias conditional](https://odinthenerd.blogspot.com/2017/03/start-simple-with-conditional-why.html)

```cpp
template<bool>
struct my_if {
	template<typename T, typename F> //`alias template`
	using t = F;
};

template<>
struct my_if<true> {
	template<typename T, typename F>
	using t = T;
};

template<bool B, class T, class F>
using result = my_if<B>::template t<T,F>;

//using
using result1 = typename my_if<true>::template t<int,bool>;
using result2 = typename my_if<true>::template t<float,char>; //reuse my_if<true>

другой быстрый вариант с template variable:

```cpp
template <class T, class U>
inline constexpr bool is_same = false;

template<class T>
inline constexpr bool is_same<T,T> = true;
```

[recursive alias](https://odinthenerd.blogspot.com/2017/03/recursive-alias-pattern-why-kvasirmpl.html)

```cpp
template<unsigned>
struct loop;

template<>
struct loop<0> {  //stop
    template<template<typename...> class F, typename T>
    using f = T;
};

template<>
struct loop<1> {  //keep going
    template<template<typename...> class F, typename T, typename U, typename...Ts>
    using f = typename loop<(sizeof...(Ts) > 0)>::template f<F,F<T,U>,Ts...>;
};

//using
template<int I>
struct int_ {
 static constexpr int value = I;
};

template<typename T, typename U>
using add = int_<(T::value + U::value)>;

using result = typename loop<1>::template f<add, int_<1>, int_<3>, int_<4>, int_<5>, int_<6>>;
```

Не создаётся новый тип на каждый шаг алгоритма, переиспользуется уже существующий -- разница на 2 порядка. Алгоритм `loop<(sizeof...(Ts) > 0)>` и тип `f<add, int_<1>, int_<3>, int_<4>, int_<5>, int_<6>>;` разделены.

[composition with continuations](https://odinthenerd.blogspot.com/2017/03/zero-const-composition-with.html)

```cpp
//С - continuation
template<typename C>
struct join {
    template<typename...Ts>
    using f = join_impl<C, Ts...>;
};

template<typename F, typename C>
struct transform {
    template<typename...Ts>
    using f = ucall<C, typename F::template f<Ts>...>;
};

//using
using result = ucall< 
    flatten< 
        filter<predicate, 
            sort<less, 
                remove_adjacent< is_same,
                    fold_left<predicate>>>>>, 
    Ts...>;
```

Элементы не собираются/разбираются в списки, а передаются по одному через композицию функций-продолжений ([tacit programming](https://en.wikipedia.org/wiki/Tacit_programming)/point free style, pipe) - сильно быстрее + чуть менее вырвиглазный синтакс.

[fast tracking](https://odinthenerd.blogspot.com/2017/03/fast-tracking-why-kvasirmpl-is-faster.html)

Кроме терминальной ветки и обработки следующего элемента дописываются ещё несколько веток обработки сразу серии элементов (у автора pow(2) до 256).

```cpp
constexpr unsigned next_fold_track(unsigned size){
    return size > 10 ? 2 : size > 0 ? 1 : 0;
}

template<unsigned>
struct fold_left_impl;

template<>
struct fold_left_impl<0> {  //stop
    template<template<typename...> class F, typename T>
    using f = T;
};

template<>
struct fold_left_impl<1> {  //keep going
    template<template<typename...> class F, typename T, typename U, typename...Ts>
    using f = typename fold_left_impl<next_fold_track(sizeof...(Ts))>::template f< 
        F,F<T,U>,Ts...>;
};

template<>
struct fold_left_impl<2> {  //keep going
    template<template<typename...> class F, typename T0, typename T1, typename T2,
    typename T3, typename T4, typename T5, typename T6, typename T7, typename T8, 
    typename T9, typename T10, typename...Ts>
    using f = typename fold_left_impl<
        next_fold_track(sizeof...(Ts))>::template f<F,
        F<F<F<F<F<F<F<F<F<F<T0,T1>,T2>,T3>,T4>,T5>,T6>,T7>,T8>,T9>,T10>,Ts...>;
};

template<typename F, typename C = identity>
struct fold_left{
    template<typename...Ts>
    using f = typename C::template f<
        typename fold_left<next_fold_track(sizeof...(Ts))>::template f<
        F::template f, Ts...>;
};
```

