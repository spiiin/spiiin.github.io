---
title: daScript AoT
tags: dascript
abbrlink: 368621422
date: 2024-06-06 23:44:37
---

## Ahead-of-Time

Пример сборки с поддержкой Ahead-of-Time скриптов.

**`Сборка tutorial02_dasAot`**

Программа компилирует скрипты на daScript, но полученное дерево симуляции не выполняет, а отдаёт в [visitor](https://github.com/GaijinEntertainment/daScript/blob/master/src/ast/ast_aot_cpp.cpp#L3943), который генерирует c++-код, строящий аналогичное дерево симуляции (без парсинга, и компиляции). `tutorial02_dasAot` -- пример кастомной утилиты генерации, в которой можно, например, дописать необходимые игре префиксы/постфиксы вроде путей к заголовочным файлам, инициализации или обёртки в неймспейсы. Собранный по умолчанию `daScript` с ключом `-aot` также может сгенерировать из das-файла соотвествующий ему c++-файл.

**`Генерация из скриптов cpp-файлов`**

Проект `tutorial02_dasAotStub` -- шаг генерации. Вручную может быть вызван как 

```
tutorial02_dasAot.exe -aot tutorial02.das tutorial02_dasAotStub_tutorial02.das.cpp
```

В настроенном через cmake проекте сгенерированный файл попадает в папку `\daScript\examples\tutorial\_aot_generated\tutorial02_dasAotStub_tutorial02.das.cpp`

**`Сборка игры с подключенной AoT-версией кода`**

Следующий шаг -- сборки хост-приложения с подключенной к нему AoT-версией кода (`tutorial02aot`).

```cpp
int main( int, char * [] ) {
    //стандартный код инициализации/компиляция/запуска скриптов daScript
    policies.aot = true; //политика aot
    auto program = compileDaScript(getDasRoot() + TUTORIAL_NAME, fAccess, tout, dummyLibGroup, policies);
}
```

При этом к программе прилинкован код файла `tutorial02_dasAotStub_tutorial02.das.cpp`. По коду в нём можно понять, что будет происходить внутри виртуальной машины daScript:

```cpp
//aotLib - таблица заполняется ссылками на "скомпилированное" дерево симуляции функций.
// можно предположить, что в виртуальной машине daScript перед выполнением функции рассчитывается её хеш,
// и если он совпадает, то вызывается Ahead-of-Time версия. В случае изменения хеша -- вызывается новая функция
// (ну или точнее, выбор происходит на стадии построения дерева симуляции программы, 
// ссылки на ноды-вызовы функций заменяются на aot-ноды)
static void registerAotFunctions ( AotLibrary & aotLib ) {
	// test_f5d22a771e42aa43
	aotLib[0x217a567e6e416cd0] = [&](Context & ctx){
		return ctx.code->makeNode<SimNode_Aot<void (*) ( Context * __context__ ),&test_f5d22a771e42aa43>>();
	};
	// [[ init script ]]
	aotLib[0xd9e9b0755c21f011] = [&](Context & ctx){
		ctx.aotInitScript = ctx.code->makeNode<SimNode_Aot<void (*)(Context *, bool),&__init_script>>();
		return ctx.aotInitScript;
	};
	resolveTypeInfoAnnotations();
};

//глобальная переменная -- intrusive list, регистрирующий функции и хранящий ссылки на другие списки инициализации aot-функций
AotListBase impl(registerAotFunctions);
```

**`Проверка`**
В скрипт `tutorial2.das` можно добавить опцию `options log_aot=true`, чтобы в output проверить, что скрипт использует AoT версию функции
```
test AOT=0x217a567e6e416cd0  <----- AoT!
this tutorial utilizes basic builin module with constant and function
sq2 = 1.414213538 // expecting sqrt(2), 1.41421
a   = 2   // expecting var a initialized with 2
xma = 3.000000000 // expecting 3
```

(можно отключить aot -- `policies.aot = false;`)
