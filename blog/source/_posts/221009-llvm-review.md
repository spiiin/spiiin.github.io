---
title: LLVM - обзор
tags:
    - cpp 
    - dev
    - dascript
    - llvm
abbrlink: 315556844
date: 2022-10-09 16:41:32
---

Попытка очень бегло пройтись по тому, что можно найти в LLVM.
<!-- more -->

## Инфраструктура для авторов языков программирования

LLVM - это огромный проект. Чаще всего, когда говорят о нём - имеют ввиду возможность написать только фронтэнд для какого-нибудь языка - из языка в биткод llvm. Дальше автоматом можно получить следующие стадии трансформации: из `ir llvm -> оптимизации различные ->mir под конкретные платформы -> бинарный код под платформы`.

Биткод может быть представлен в 3х формах: текстовый псевдоассемблер, бинарный формат, и in-memory api, с помощью которого можно нагенерить всё с помощью кода, в том числе сделать jit-компилятор.

В теории, jit быстрее статической компиляции, потому что:
- может задействовать динамические данные о том, какой код "горячее" (статическому компилятору тоже можно передать эту инфу, полученную уже после запуска приложения, при повторной компиляции/линковке)
- может инлайнить больше, чем статический - например, библиотечные функции, которые иначе нельзя
- может подстроиться под особенностью архитектуры или ос

Java vm, .net или js-двики чаще всего jit так или иначе делают, быстрые версии интерпретаторов тоже. Jit-компиляция большая отдельная тема.
[dasLLVM](https://github.com/borisbat/dasLLVM) -- пример jit-компиляции из [daScript](https://spiiin.github.io/tags/dascript/) на LLVM, пока на начальной стадии.

Если хочется погрузиться в теорию компиляции, можно читать что-нибудь типа:
- Learn LLVM 12
- Классическую "Компиляторы: принципы, технологии и инструменты"
- [Crafting Interpreters](http://craftinginterpreters.com/)

Последняя интересна тем, что нацелена на практику, от автора `Game Programming Patterns`, а также нескольких скриптовых языков: [wren](https://wren.io/), [magpie](https://magpie-lang.org/). В его блоге также много [статей](https://journal.stuffwithstuff.com/category/language/) об устройстве языков программирования. В третьей части много продвинутого материала об оптимизации вызовов функций, замыканий и методам ускорения интерпретатора байт кода.

Несколько нестандартных применений:
- [Statically Recompiling NES Games into Native Executables with LLVM and Go](https://andrewkelley.me/post/jamulator.html) - попытка перекомпилировать байт-код для NES в LLVM-биткод, без эмуляции от автора языка `Zig`, не очень успешная, так как в NES ассемблере очень много трюков, которые требуют реальной эмуляции особенностей железа (синхронизация с процессором, прыжки в середину инструкции, самомодифицирующийся код).
- "Компиляция данных" -- создание микроязыков для того, чтобы добавить возможность "положить" в игровые ресурсы код.

[2019 LLVM Developers’ Meeting: J. Paquette & F. Hahn “Getting Started With LLVM: Basics”](https://www.youtube.com/watch?v=3QQuhL-dSys) -- доклад про IR LLVM
[Writing an LLVM Pass](https://llvm.org/docs/WritingAnLLVMPass.html) -- как написать свой проход LLVM

## Clang - фронтэнд компилятор C++

Отдельный проект -- фронтэнд для С++ (а также С и  Objective C/C++) - `clang`. Собственно, у него есть несколько ключей, чтобы получать промежуточные представления кода, но это тоже прикладным разработчикам не особо надо чаще всего. Один из вариантов его использования - написание своих проходов при компиляции. Cобирается плагин в dll/dylib/a и компилятору clang ключом передаётся, чтобы он дёргал функции-колбека из этого плагина при каждой компиляции кода.

Apple в xcode clang не совсем из стандартной репы собирала, поэтому он у них с такими плагинами не работает, но в принципе пересобрав самому из исходников можно и им под ios код генерить. Вот ["hello world"](https://railsware.com/blog/creation-and-using-clang-plugin-with-xcode/) с плагинами. Таким способом можно решать что-то типа "хочу, чтобы если в лямбду кто-то захватил this неявно, то компиляция крешилась с сообщением, потому что в половине случаев автор забыл проверить время жизни this и упадёт в рантайме" (или другие правила, обычно написанные кровью в code convention проекта, которые невозможно выразить семантикой C++).

Так редко кто делает, но вот примеры проектов с набором плагинов, дополнительно проверяющих код:
[libreoffice](https://github.com/LibreOffice/core/tree/master/compilerplugins/clang)
[chrome](https://chromium.googlesource.com/chromium/src.git/+/master/docs/clang.md#using-plugins) + [Статья](https://ehsanakhgari.org/blog/2015-12-07/c-static-analysis-using-clang/)
[firefox](https://hg.mozilla.org/mozilla-central/file/tip/build/clang-plugin/)

Более основательный туториал про то, как писать плагины, и что с их помощью можно делать
[https://github.com/banach-space/llvm-tutor](https://github.com/banach-space/llvm-tutor)

## API для работы с Clang

Особенность компилятора Clang -- он предоставляет несколько API для того, чтобы можно было получать информацию о коде программы.

К примеру, можно пропарсить заголовочный файлы и автоматом нагенерить привязок к другим языкам. Из особенностей - не очень быстро работает (поэтому некоторые предпочитают велосипедить свои парсеры, передавая мета-информацию комментариями), и не очень хорошо работает с сложным шаблонным кодом. Но в целом можно целиком какую-нибудь либу привязать им к другому языку с небольшим количеством ручной работы.

Один из интерфейсов - `libclang`, библиотека на C++, к которой есть привязки на других языках.

Примеры использования **`генерации привязок`**:
{% post_link 220530-dascript-bindings 'daScript: C++ auto-bindings, msgpack' %} -- генерация из daScript привязок к `msgpack`
{% post_link 220612-dascript-assimp 'daScript: C++ auto-bindings, assimp' %} -- генерация из daScript привязок к `assimp`, без написания кода (почти)
(с помощью [dasClangBind](https://github.com/GaijinEntertainment/daScript/tree/master/modules/dasClangBind))
[Automatic Language Bindings](https://floooh.github.io/2020/08/23/sokol-bindgen.html) -- генерация из Python привязок к `solol` для различных языков (zig/nim/odin)

**`Интерактивное получение данных из кода`**
[Cling](https://root.cern/cling/) - интерактивная комплиляция С++ кода, для использования с инструментами типа `Jupyter`
[cppyy](https://cppyy.readthedocs.io/en/latest/examples.html) - привязка cling к python, работает в том числе и под windows

**`Написание тулзов для IDE`**
[ycmd](https://github.com/def-/ycmd) - сервер автодополнения кода для различных IDE
[StructLayout](https://marketplace.visualstudio.com/items?itemName=RamonViladomat.StructLayout) - расширение для VS code, которое может показать то, как компилятор будет размещать структуру в памяти (надо помнить, что libclang, который использует это расширение, должен быть той же версии, что и сам компилятор, который будет генерировать код).

Можно также решать всякие задачи вроде "отсортировать функции по количеству байт и напечатать 10 самых больших".

**`Туториалы, как научиться пользоваться`**
[Understanding the Clang AST](https://jonasdevlieghere.com/understanding-the-clang-ast/) - 3 API для работы с AST в clang
[Introduction to the Clang AST](https://clang.llvm.org/docs/IntroductionToTheClangAST.html) - ссылки на диаграммы классов AST, во что трансформируется код на C++
[How to write RecursiveASTVisitor based ASTFrontendActions](https://clang.llvm.org/docs/RAVFrontendAction.html) - пример того, как сделать свой визитор для AST
[Tutorial for building tools using LibTooling and LibASTMatchers](https://clang.llvm.org/docs/LibASTMatchersTutorial.html) - использование других интерфейсов для написания визиторов
[The Clang AST - a Tutorial](https://www.youtube.com/watch?v=VqCkCDFLSsc) - доклад всё про то же
[Emitting Diagnostics in Clang](http://www.goldsborough.me/c++/clang/llvm/tools/2017/02/24/00-00-06-emitting_diagnostics_and_fixithints_in_clang_tools/) -- вывод своих сообщений об ошибках

В каком-то смысле, интерфейс для того, чтобы иметь доступ к AST языка, необходим из-за того, что этого не умеет сам C++ - шаблоны умеют заставить компилятор произвести эффекты, но не имеют доступа к самому коду. В языках вроде `daScript` аналогичную плагинам компилятора работы могут выполнять макросы.
[Пример](https://github.com/GaijinEntertainment/daScript/blob/master/daslib/jobque_boost.das#L142) макроса в daScript, применяемого к замыканию и выполняющего дополнительную работу, если в замыкание передаются примитивы синхронизации `Channel` или `Job`.
{% post_link 220206-dascript-macro 'daScript macro' %} -- пример генерации AST daScript из кода
{% post_link 220702-dascript-macro2 'daScript macro - 2' %} -- пример работы с DSL, упрощающим написание AST

Также, для Clang, чтобы упростить работу с C++ AST, существует DSL для составления запросов - **`clang query`**
[2019 EuroLLVM Developers’ Meeting: S. Kelly “The Future of AST Matcher-based Refactoring](https://www.youtube.com/watch?v=yqi8U8Q0h2g) - использование запросов clang query для визуальной работы с кодом, расширение godbolt + интерфейс к qt контролам
[Extending clang-tidy in the Present and in the Future - Stephen Kelly](https://www.youtube.com/watch?v=38tYYrnfNrs) - и для модификации кода/рефакторинга

Ещё один способ использования -- глубже изучить, как устроена какая-либо абстракция в языке
[CppCon 2016: Gor Nishanov “C++ Coroutines: Under the covers"](https://www.youtube.com/watch?v=8C8NnE1Dg4A) -- реализация корутин в новом стандарте C++
[LLVM Language Reference Manual](https://llvm.org/docs/LangRef.html) - справка по псевдо-ассемблеру LLVM

## Исходный код и архитектура LLVM
[Глава в книге "Архитектура приложений с открытым исходным кодом"](http://rus-linux.net/MyLDP/BOOKS/Architecture-Open-Source-Applications/Vol-1/llvm.html)
[A Tourist’s Guide to the LLVM Source Code](https://blog.regehr.org/archives/1453) - обзор исходников
[Обзор используемых структур данных](https://llvm.org/docs/ProgrammersManual.html) + [Ещё один](https://llvm.org/devmtg/2014-04/PDFs/LightningTalks/data_structure_llvm.pdf)

## LLDB
Отладчик, также использующий инфраструктуру llvm. Одна из интересных возможностей -- наличие [python api](https://lldb.llvm.org/python_reference/).

Пример использования API:
{% post_link 210615-cpp-objects-memory-layout-2 'Расположение объектов C++ в памяти. Часть 2' %} -- рекурсивный обход структур, для запроса из отладчика выравнивания их в памяти, с отображением "дырок"

## Общие ссылки
https://llvm.org/devmtg/ + https://www.youtube.com/c/LLVMPROJ/playlists
https://blog.llvm.org/


