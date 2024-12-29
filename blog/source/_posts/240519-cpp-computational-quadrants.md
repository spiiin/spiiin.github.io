---
title: C++ computational quadrants
abbrlink: 2220953486
date: 2024-05-19 22:11:42
tags: cpp
---

- {% post_link 230319-cpp-templates-links %} -- ссылки по метапрограммированию в C++


Увидел в доках [boost.hana](https://boostorg.github.io/hana/) разделение типов вычислений в C++ на 4 типа (я не понимаю, как Louis Dionne сложил их в квадранты). Ну и, соответственно, внутри C++ существует 4 языка для того, чтобы описывать эти типы вычислений.

**`1. Runtime computations`** -- "usual computations". Примитивы для таких вычислений -- рантайм контейнеры, функции и алгоритмы (std как пример базового фреймворка)

```cpp
auto f = [](int i) -> std::string {
  return std::to_string(i * i);
};
 
std::vector<int> ints{1, 2, 3, 4};
std::transform(ints.begin(), ints.end(), std::back_inserter(strings), f);
```

**`2. Constexpr computations`** -- constexpr вычисления компилятором. Синтаксис для таких вычислений поддерживается максимально похожим на C++. Можно воспринимать их, как код для отдельной ограниченной платформы (компилятора), которая не поддерживает выделение памяти или исключения. ([Sprout](https://github.com/bolero-MURAKAMI/Sprout) -- пример библиотеки контейнеров, функций и алгоритмов для таких вычислений)

```cpp
constexpr int factorial(int n) {
  return n == 0 ? 1 : n * factorial(n - 1);
}
 
template <typename T, std::size_t N, typename F>
  constexpr std::array<std::invoke_result_t<F, T>, N>
transform(std::array<T, N> array, F f) {
  // ...
}
 
constexpr std::array<int, 4> ints{{1, 2, 3, 4}};
constexpr std::array<int, 4> facts = transform(ints, factorial);
```

**`3. Heterogeneous computations`** -- гетерогенные вычисления. Работа с суммами  и произведениями типов(`std::variant/std::tuple/std::any`). [Boost.Fusion](https://www.boost.org/doc/libs/1_80_0/libs/fusion/doc/html/) как пример библиотеки.

```cpp
auto to_string = [](auto t) {
  std::stringstream ss;
  ss << t;
  return ss.str();
};
 
fusion::vector<int, std::string, float> seq{1, "abc", 3.4f};
fusion::vector<std::string, std::string, std::string>
  strings = fusion::transform(seq, to_string);
```

**`4. Type-level computations`** -- вычисления над типами. [Boost.MPL](https://www.boost.org/doc/libs/1_85_0/libs/mpl/doc/index.html) как пример библиотеки

```cpp
template <typename T>
struct add_const_pointer {
  using type = T const*;
};
 
using types = mpl::vector<int, char, float, void>;
using pointers = mpl::transform<types, add_const_pointer<mpl::_1>>::type;
```

## Оптимизации

[C++Now 2017: Odin Holmes "Type Based Template Metaprogramming is Not Dead"](https://youtu.be/EtU4RDCCsiU?si=xZPfpHsV06l5B1gz&t=570) -- доклад про оптимизацию вычислений над типами (`Rule of Chiel`). Для compile-time вычислений таким заморачиваются редко, нужно хорошо представлять себе, что приблизительно должен сделать под капотом компилятор, раскрывая тот или иной шаблонный код. Без такого представления время компиляции и размер выходного кода становятся непредсказумыми (точнее, предсказумо большими).

[Explicit template instantiation - when is it used?](https://stackoverflow.com/questions/2351148/explicit-template-instantiation-when-is-it-used) -- явная специализация шаблонов как приём оптимизации.

- {% post_link 240515-binary-size %} -- замеры и оптимизации размера бинарника (борьба с кодом шаблонов и инлайнгом).

## Общее

[Don't constexpr All the Things - David Sankel CppNow 2021](https://www.youtube.com/watch?v=NNU6cbG96M4) -- обзор ограничений constexpr computations. И идеи по замене ограниченного языка constexpr на полноценный язык времени компиляции равный языку времени выполнения (не C++).

[Matt Calabrese, Zachary Laine: Instantiations Must Go!](https://github.com/boostcon/2010_presentations/raw/master/mon/instantiations_must_go.pdf) -- слайды про то, как трансформировать синтаксис type-level computations в Heterogeneous computations (на 1 внутренний язык в c++ меньше), основная идея Boost.Hana.

[Exploring the design space of metaprogramming and reflection](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/p0633r0.pdf) -- варианты дизайна рефлексии в C++ через Type syntax/Heterogeneous value/Homogeneous value syntax (2,3 и 4 "квадранты")
[Reflection in C++ Next - Anton Bikineev - Meeting C++ 2017](https://youtu.be/NWIsRFDaHhs?si=kwX_viciHp91AwK0&t=850) -- тайминг доклада с примерами реализаций этими способами

[The next big Thing - Andrei Alexandrescu - Meeting C++ 2018 Opening Keynote](https://youtu.be/tcyb1lpEHm0?si=PgwOTQ-cc_LkpIv5&t=2367) -- (тайминг) Александреску рассказывает про интроспецию с видом человека, который её придумал. В его терминологии это генерация произвольного кода во время компиляции. Input - чтение любого кода (в proposals), processing - выполнение любого кода в compile-time (wip), output - генерация любого кода (отсутствует совсем).

## За пределами C++

- {% post_link 240330-dascript-macro3 %} -- работа с AST языка, как базовый способ метапрограммирования без создания [теневых миров](https://probablydance.com/2015/02/16/ideas-for-a-programming-language-part-3-no-shadow-worlds/)
- {% post_link 221010-simple-languages %} -- маленькие языки проще и для работы с ними на мета-уровне

[Clang/LibTooling AST Notes](https://ikrima.dev/dev-notes/clang/clang-libtooling-ast/) -- интерфейсы к Clang для работы с AST. Метапрограммирование не "на C++", а "с использованием C++", без ожидания принятия стандартов, их имплементации, и миграции библиотек.







