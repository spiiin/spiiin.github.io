---
title: daScript. Brainfuck и оптимизации
abbrlink: 621874082
date: 2022-11-11 17:42:54
tags:
  - dascript
  - llvm
---

Попробовал портировать с `nim` на `daScript` [интерпретатор](https://howistart.org/posts/nim/1/) `brainfuck` кода. Брейфак предельно простой язык, и базовая реализация интерпретатора занимает полчаса, но на нём можно потренироваться в ускорении кода и продемонстрировать возможности daScript в оптимизации.

<!-- more -->

Самая первая, максимально наивная, построчно скопированная реализация:

```cpp
require strings
require fio

def run(code: string; var tape: array<uint8>; var codePos, tapePos: int&; skip: bool): bool
	while tapePos >= 0 && codePos < length(code)
		if tapePos >= length(tape) { tape |> push(uint8(0)); }

		let sym1  = code |> character_at(codePos)
		if sym1 == '['
			++codePos
			let oldPos = codePos
			while run(code, tape, codePos, tapePos, tape[tapePos] == uint8(0))
				codePos = oldPos
		elif sym1 == ']'
			return tape[tapePos] != uint8(0)
		elif !skip
			let sym  = code |> character_at(codePos)
			if sym == '+' { tape[tapePos] = uint8(int(tape[tapePos]) + 1); }
			elif sym == '-' { tape[tapePos] = uint8(int(tape[tapePos]) - 1); }
			elif sym == '>' { ++tapePos; }
			elif sym == '<' { --tapePos; }
			elif sym == '.' { print("{int(tape[tapePos]) |> to_char}"); }
			elif sym == ',' { tape[tapePos] = uint8(getchar()); }
			else { }
		++codePos
	return false

def interpret(code: string)
	let totalTime = ref_time_ticks()
	var tape: array<uint8>
	var codePos, tapePos : int
	run(code, tape, codePos, tapePos, false)
	let totalDt = double(get_time_usec(totalTime)) /1000000.0lf
	to_log(LOG_INFO, "total {totalDt} sec\n")
```

Если попытаться протестировать его на генераторе [множества Мандельброта](https://github.com/def-/nim-brainfuck/blob/master/examples/mandelbrot.b), можно заметить серьёзные проблемы со скоростью, вычисления занимают около 5 часов. Стоит попробовать его разогнать!

## Отключение проверок границ и указателей

Код на brainfuck - это простая числодробилка, ускорить которую можно, отключив все дополнительные проверки обращений к памяти.

*Как отключать проверки, мне рассказал [Борис Баткин](https://github.com/borisbat) (так как интерпретатор nim делал один основных контрибьютеров языка, то его подсказки не отменяют честности сравнения -- авторы находятся в одной "весовой категории" знания своего языка).*

В первую очередь, можно заменить функцию `charcter_at`, которая [проверяет](https://github.com/GaijinEntertainment/daScript/blob/e9f4c486848a8985e4126e0fc2d04afbc6abd883/src/builtin/module_builtin_string.cpp#L26),что индекс меньше длины строки, на `character_uat`, которая не делает этой проверки.

Также отключается проверка ссылок на null макросом `[unsafe_deref]`.

Наконец, обращение к массиву можно выполнять не через разыменование ссылки, а через обращение по указателю:

```cpp
tape: array<uint8>
tape[index] // tape[check_range(index)] //медленно

var ptape: uint8? = addr(tape[0])
ptape[index] //check_not_null(ptape)[index] //быстрее, обращение без проверок

[unsafe_deref]
ptape[index] //ptape[index] //еще быстрее, обращение без перепроверок указателя на nullptr
```

Переписанная версия кода:

```cpp
[unsafe_deref]
def run(code: uint8?; lengthOfCode:int; var tape: uint8?; var codePos, tapePos: int&; skip: bool): bool
	unsafe
		while tapePos >= 0 && codePos < lengthOfCode
			let sym1  = int(code[codePos])
			if sym1 == '['
				++codePos
				let oldPos = codePos
				while run(code, lengthOfCode, tape, codePos, tapePos, tape[tapePos] == uint8(0))
					codePos = oldPos
			elif sym1 == ']'
				return tape[tapePos] != uint8(0)
			elif !skip
				let sym  = int(code[codePos])
				if sym == '+' { tape[tapePos] = uint8(int(tape[tapePos]) + 1); }
				elif sym == '-' { tape[tapePos] = uint8(int(tape[tapePos]) - 1); }
				elif sym == '>' { ++tapePos; }
				elif sym == '<' { --tapePos; }
				elif sym == '.' { print(int(tape[tapePos]) |> to_char); }
				elif sym == ',' { tape[tapePos] = uint8(getchar()); }
				else { }
			++codePos
		return false

def interpret(code: string)
	let totalTime = ref_time_ticks()
	var tape: array<uint8>
	var codePos, tapePos : int
	tape |> resize(1000000)
	unsafe
		run(reinterpret<uint8?> code, length(code), addr(tape[0]), codePos, tapePos, false)
	let totalDt = double(get_time_usec(totalTime)) /1000000.0lf
	to_log(LOG_INFO, "total {totalDt} sec\n")
```

Такая версия интерпретатора всё ещё тормозная, но уже позволяет дождаться завершения выполнения кода:

```
e:\src\daScript\bin\Release>daScript.exe brainfuck_00.das
AAAAAAAAAAAAAAAABBBBBBBBBBBBBBBCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCDDDDDDDDDEGFFEEEEDDDDDDCCCCCCCCCBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB
AAAAAAAAAAAAAAABBBBBBBBBBBBBCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCDDDDDDDDDDEEEFGIIGFFEEEDDDDDDDDCCCCCCCCCBBBBBBBBBBBBBBBBBBBBBBBBBB
AAAAAAAAAAAAABBBBBBBBBBBBCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCDDDDDDDDDDDDEEEEFFFI KHGGGHGEDDDDDDDDDCCCCCCCCCBBBBBBBBBBBBBBBBBBBBBBB
AAAAAAAAAAAABBBBBBBBBBCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCDDDDDDDDDDDDDDEEEEEFFGHIMTKLZOGFEEDDDDDDDDDCCCCCCCCCBBBBBBBBBBBBBBBBBBBBB
AAAAAAAAAAABBBBBBBBBCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCDDDDDDDDDDDDDDEEEEEEFGGHHIKPPKIHGFFEEEDDDDDDDDDCCCCCCCCCCBBBBBBBBBBBBBBBBBB
AAAAAAAAAABBBBBBBBCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCDDDDDDDDDDDDDDDEEEEEEFFGHIJKS  X KHHGFEEEEEDDDDDDDDDCCCCCCCCCCBBBBBBBBBBBBBBBB
AAAAAAAAABBBBBBBCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCDDDDDDDDDDDDDDDEEEEEEFFGQPUVOTY   ZQL[MHFEEEEEEEDDDDDDDCCCCCCCCCCCBBBBBBBBBBBBBB
AAAAAAAABBBBBBCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCDDDDDDDDDDDDDDDEEEEEFFFFFGGHJLZ         UKHGFFEEEEEEEEDDDDDCCCCCCCCCCCCBBBBBBBBBBBB
AAAAAAABBBBBCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCDDDDDDDDDDDDDDEEEEFFFFFFGGGGHIKP           KHHGGFFFFEEEEEEDDDDDCCCCCCCCCCCBBBBBBBBBBB
AAAAAAABBBBCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCDDDDDDDDDDDDEEEEEFGGHIIHHHHHIIIJKMR        VMKJIHHHGFFFFFFGSGEDDDDCCCCCCCCCCCCBBBBBBBBB
AAAAAABBBCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCDDDDDDDDDDDEEEEEEFFGHK   MKJIJO  N R  X      YUSR PLV LHHHGGHIOJGFEDDDCCCCCCCCCCCCBBBBBBBB
AAAAABBBCCCCCCCCCCCCCCCCCCCCCCCCCCCCCDDDDDDDDEEEEEEEEEFFFFGH O    TN S                       NKJKR LLQMNHEEDDDCCCCCCCCCCCCBBBBBBB
AAAAABBCCCCCCCCCCCCCCCCCCCCCCCCCCCDDDDDDEEEEEEEEEEEEFFFFFGHHIN                                 Q     UMWGEEEDDDCCCCCCCCCCCCBBBBBB
AAAABBCCCCCCCCCCCCCCCCCCCCCCCCCDDDDEEEEEEEEEEEEEEEFFFFFFGHIJKLOT                                     [JGFFEEEDDCCCCCCCCCCCCCBBBBB
AAAABCCCCCCCCCCCCCCCCCCCCCCDDDDEEEEEEEEEEEEEEEEFFFFFFGGHYV RQU                                     QMJHGGFEEEDDDCCCCCCCCCCCCCBBBB
AAABCCCCCCCCCCCCCCCCCDDDDDDDEEFJIHFFFFFFFFFFFFFFGGGGGGHIJN                                            JHHGFEEDDDDCCCCCCCCCCCCCBBB
AAABCCCCCCCCCCCDDDDDDDDDDEEEEFFHLKHHGGGGHHMJHGGGGGGHHHIKRR                                           UQ L HFEDDDDCCCCCCCCCCCCCCBB
AABCCCCCCCCDDDDDDDDDDDEEEEEEFFFHKQMRKNJIJLVS JJKIIIIIIJLR                                               YNHFEDDDDDCCCCCCCCCCCCCBB
AABCCCCCDDDDDDDDDDDDEEEEEEEFFGGHIJKOU  O O   PR LLJJJKL                                                OIHFFEDDDDDCCCCCCCCCCCCCCB
AACCCDDDDDDDDDDDDDEEEEEEEEEFGGGHIJMR              RMLMN                                                 NTFEEDDDDDDCCCCCCCCCCCCCB
AACCDDDDDDDDDDDDEEEEEEEEEFGGGHHKONSZ                QPR                                                NJGFEEDDDDDDCCCCCCCCCCCCCC
ABCDDDDDDDDDDDEEEEEFFFFFGIPJIIJKMQ                   VX                                                 HFFEEDDDDDDCCCCCCCCCCCCCC
ACDDDDDDDDDDEFFFFFFFGGGGHIKZOOPPS                                                                      HGFEEEDDDDDDCCCCCCCCCCCCCC
ADEEEEFFFGHIGGGGGGHHHHIJJLNY                                                                        TJHGFFEEEDDDDDDDCCCCCCCCCCCCC
A                                                                                                 PLJHGGFFEEEDDDDDDDCCCCCCCCCCCCC
ADEEEEFFFGHIGGGGGGHHHHIJJLNY                                                                        TJHGFFEEEDDDDDDDCCCCCCCCCCCCC
ACDDDDDDDDDDEFFFFFFFGGGGHIKZOOPPS                                                                      HGFEEEDDDDDDCCCCCCCCCCCCCC
ABCDDDDDDDDDDDEEEEEFFFFFGIPJIIJKMQ                   VX                                                 HFFEEDDDDDDCCCCCCCCCCCCCC
AACCDDDDDDDDDDDDEEEEEEEEEFGGGHHKONSZ                QPR                                                NJGFEEDDDDDDCCCCCCCCCCCCCC
AACCCDDDDDDDDDDDDDEEEEEEEEEFGGGHIJMR              RMLMN                                                 NTFEEDDDDDDCCCCCCCCCCCCCB
AABCCCCCDDDDDDDDDDDDEEEEEEEFFGGHIJKOU  O O   PR LLJJJKL                                                OIHFFEDDDDDCCCCCCCCCCCCCCB
AABCCCCCCCCDDDDDDDDDDDEEEEEEFFFHKQMRKNJIJLVS JJKIIIIIIJLR                                               YNHFEDDDDDCCCCCCCCCCCCCBB
AAABCCCCCCCCCCCDDDDDDDDDDEEEEFFHLKHHGGGGHHMJHGGGGGGHHHIKRR                                           UQ L HFEDDDDCCCCCCCCCCCCCCBB
AAABCCCCCCCCCCCCCCCCCDDDDDDDEEFJIHFFFFFFFFFFFFFFGGGGGGHIJN                                            JHHGFEEDDDDCCCCCCCCCCCCCBBB
AAAABCCCCCCCCCCCCCCCCCCCCCCDDDDEEEEEEEEEEEEEEEEFFFFFFGGHYV RQU                                     QMJHGGFEEEDDDCCCCCCCCCCCCCBBBB
AAAABBCCCCCCCCCCCCCCCCCCCCCCCCCDDDDEEEEEEEEEEEEEEEFFFFFFGHIJKLOT                                     [JGFFEEEDDCCCCCCCCCCCCCBBBBB
AAAAABBCCCCCCCCCCCCCCCCCCCCCCCCCCCDDDDDDEEEEEEEEEEEEFFFFFGHHIN                                 Q     UMWGEEEDDDCCCCCCCCCCCCBBBBBB
AAAAABBBCCCCCCCCCCCCCCCCCCCCCCCCCCCCCDDDDDDDDEEEEEEEEEFFFFGH O    TN S                       NKJKR LLQMNHEEDDDCCCCCCCCCCCCBBBBBBB
AAAAAABBBCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCDDDDDDDDDDDEEEEEEFFGHK   MKJIJO  N R  X      YUSR PLV LHHHGGHIOJGFEDDDCCCCCCCCCCCCBBBBBBBB
AAAAAAABBBBCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCDDDDDDDDDDDDEEEEEFGGHIIHHHHHIIIJKMR        VMKJIHHHGFFFFFFGSGEDDDDCCCCCCCCCCCCBBBBBBBBB
AAAAAAABBBBBCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCDDDDDDDDDDDDDDEEEEFFFFFFGGGGHIKP           KHHGGFFFFEEEEEEDDDDDCCCCCCCCCCCBBBBBBBBBBB
AAAAAAAABBBBBBCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCDDDDDDDDDDDDDDDEEEEEFFFFFGGHJLZ         UKHGFFEEEEEEEEDDDDDCCCCCCCCCCCCBBBBBBBBBBBB
AAAAAAAAABBBBBBBCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCDDDDDDDDDDDDDDDEEEEEEFFGQPUVOTY   ZQL[MHFEEEEEEEDDDDDDDCCCCCCCCCCCBBBBBBBBBBBBBB
AAAAAAAAAABBBBBBBBCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCDDDDDDDDDDDDDDDEEEEEEFFGHIJKS  X KHHGFEEEEEDDDDDDDDDCCCCCCCCCCBBBBBBBBBBBBBBBB
AAAAAAAAAAABBBBBBBBBCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCDDDDDDDDDDDDDDEEEEEEFGGHHIKPPKIHGFFEEEDDDDDDDDDCCCCCCCCCCBBBBBBBBBBBBBBBBBB
AAAAAAAAAAAABBBBBBBBBBCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCDDDDDDDDDDDDDDEEEEEFFGHIMTKLZOGFEEDDDDDDDDDCCCCCCCCCBBBBBBBBBBBBBBBBBBBBB
AAAAAAAAAAAAABBBBBBBBBBBBCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCDDDDDDDDDDDDEEEEFFFI KHGGGHGEDDDDDDDDDCCCCCCCCCBBBBBBBBBBBBBBBBBBBBBBB
AAAAAAAAAAAAAAABBBBBBBBBBBBBCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCDDDDDDDDDDEEEFGIIGFFEEEDDDDDDDDCCCCCCCCCBBBBBBBBBBBBBBBBBBBBBBBBBB
[I] total 564.99929999999994834 sec
```

564 секунды -- в 30 раз быстрее первой версии, но всё ещё сильно медленнее интерпретатора на `nim`, который в релизной версии выполняется за 40 секунд.

## Ahead-of-Time

daScript умеет транспилироваться в C++ код, для сравнения с nim попробуем скомпилировать интерпретатор, без внесения каких-либо изменений в код.

```
daScript.exe -aot brainfuck.das brainfuck.das.cpp
```

Полученный C++-файл проще всего подсунуть в пример [tutorial02aot](https://github.com/GaijinEntertainment/daScript/blob/master/examples/tutorial/tutorial02aot.cpp), который настроен на использование AoT варианта кода. Скомпилированный файл можно запустить:

```cpp
e:\src\daScript\bin\Release>tutorial02aot.exe
[I] total 34.27342399999999856 sec
```

34 секунды -- уже быстрее, чем nim, который сам по себе достаточно быстрый!

## Just-in-Time

Можно попробовать двигаться дальше, подключив экспериментальный модуль [dasLLVM](https://github.com/borisbat/dasLLVM). Чтобы собрать его, необходимо:

- включить сборку модуля в cmake:

```
option(DAS_LLVM_DISABLED "Disable dasLLVM (llvm bindings)" OFF)
```

- собрать проект llvm, или скачать собранный (например, от [qt](https://download.qt.io/development_releases/prebuilt/libclang/)) и положить на уровень выше корневой директории проекта daScript, напрммер:

```
C:/dascript
C:/libclang
```

- сгенерировать решение и пересобрать dascript:

```
generate_msvc_2019.bat
```

Теперь можно воспользоваться аннотацией `[jit]`, чтобы код функциии интерпретатора без AoT-компиляции перед первым выполнением компилировался с помощью `llvm-c`.

```cpp
[jit,unsafe_deref]
def run(code: uint8?; lengthOfCode:int; var tape: uint8?; var codePos, tapePos: int&; skip: bool): bool
```

```
e:\src\daScript_my\bin\Release>daScript.exe brainfuck_2_jit.das
[I] total 22.66654300000000077 sec
```

22.6 секунды, еще лучше! Генерация daScript-кода в llvm-ассемблер быстрее, чем в C++ -- генератор передаёт больше полезной для оптимизации о кода, а также, возможно, задействуется сила оптимизаций LLVM.

## Метапрограммирование

Можно двигаться дальше. Вместо того, чтобы писать функцию, которая интерпретирует любой код на brainfuck, можно написать макрос, который сгенерирует код конкретной функции в compile-time, и измерить время выполнения этой функции.

Можно использовать [AstReaderMacro](https://dascript.org/doc/reference/language/macros.html#astreadermacro) -- тип макроса, который обрабатывает отдельные символы. Синтаксис вызова такого макроса:

```
% READER_MACRO_NAME ~ character_sequence %% //character_sequence будет передана на вход макросу
```

Шаблоны таких макросов можно посмотреть в модулях `json_boost` и `regex_boost`

```cpp
module brainfuck_macro shared public

def generateFunction(uniqueName, code)
    let seqStr = string(code)

    var blkArr : array<array<ExpressionPtr>>; defer_delete(blkArr)

    var blk : array<ExpressionPtr>; defer_delete(blk)
    blkArr |> emplace(blk)

    blkArr[0] |> emplace_new <| qmacro_expr( ${ var tape: array<uint8>; })
    blkArr[0] |> emplace_new <| qmacro_expr( ${ var tapePos : int; })
    blkArr[0] |> emplace_new <| qmacro_expr( ${ tape |> resize(1000000); })
    blkArr[0] |> emplace_new <| qmacro_expr( ${ var ptape = addr(tape[0]); })
    
    for sym in seqStr
        if sym == '+'   { back(blkArr) |> emplace_new <| qmacro_expr( ${ ptape[tapePos] = uint8(int(ptape[tapePos]) + 1); }); }
        elif sym == '-' { back(blkArr) |> emplace_new <| qmacro_expr( ${ ptape[tapePos] = uint8(int(ptape[tapePos]) - 1); }); }
        elif sym == '>' { back(blkArr) |> emplace_new <| qmacro_expr( ${ ++tapePos; }); } 
        elif sym == '<' { back(blkArr) |> emplace_new <| qmacro_expr( ${ --tapePos; }); }
        elif sym == '.' { back(blkArr) |> emplace_new <| qmacro_expr( ${ print(int(ptape[tapePos]) |> to_char); }); }
        elif sym == ',' { back(blkArr) |> emplace_new <| qmacro_expr( ${ ptape[tapePos] = uint8(getchar()); }); }
        elif sym == '['
            var blk1 : array<ExpressionPtr>; defer_delete(blk1)
            blkArr |> emplace(blk1)
        elif sym == ']'
            var last <- back(blkArr)
            blkArr |> pop()
            var whileExpr <- qmacro_expr <|
                while ptape[tapePos] != uint8(0)
                    $b(last)
            back(blkArr) |> emplace_new <| whileExpr
        else { }

    var fnArguments : array<VariablePtr>;
    var fn <- qmacro_function(uniqueName) <| $ ($a(fnArguments))
        unsafe
            $b(blkArr[0])
    defer_delete(fn)

    var args:array< tuple<argname:string;argvalue:RttiValue> >
    fn |> append_annotation("$", "unsafe_deref", args)
    //print(describe(fn))
    compiling_module() |> add_function(fn)

[reader_macro(name="bf")]
class private BrainfuckReader : AstReaderMacro
    def override accept( prog:ProgramPtr; mod:Module?; var expr:ExprReader?; ch:int; info:LineInfo) : bool
        append(expr.sequence, ch)
        if ends_with(expr.sequence,"%%")
            let len = length(expr.sequence)
            resize(expr.sequence,len-2)
            return false
        else
            return true
    def override visit( prog:ProgramPtr; mod:Module?; expr:smart_ptr<ExprReader>) : ExpressionPtr
        let str <- make_unique_private_name("bf`exec", expr.at)
        generateFunction(str, expr.sequence)

        var ftype <- new [[TypeDecl() at=expr.at, baseType=Type tFunction ]]
        ftype.firstType <- new [[TypeDecl() at=expr.at, baseType=Type tVoid]]
        var funcPtr <- new [[ExprAddr() at=expr.at, target:=str, funcType <- ftype]]
        return funcPtr
```

Тогда вызвать такой макрос можно так:

```cpp
require brainfuck_macro
//генерируем функцию
let func = %bf~++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++.%%
//вызываем сгенерированную функцию
invoke(func)
```

Если раскомментировать строчку `print(describe(fn))` можно посмотреть на сгенерированное тело функции.

Например:

```cpp
let func = %bf~[->+<]%%
//сгенерированный код

[unsafe_deref]
def public bf`exec_0xd_0xc
    unsafe
        var tape:array<uint8> -const                          //declare variables
        var tapePos:int -const
        resize(tape,1000000)
        var ptape:auto -const = addr(tape[0])

        while ptape[tapePos] != uint8(0)                      //[
            ptape[tapePos] = uint8(int(ptape[tapePos]) - 1)   //-
            ++tapePos                                         //>
            ptape[tapePos] = uint8(int(ptape[tapePos]) + 1)   //+
            --tapePos                                         //<]
let func = @@bf`exec_0xd_0xc //указатель на функцию
```

Для каждой функции генерируется уникальное имя, чтобы можно было создать несколько отдельных интерпретатов, и своя "лента" памяти. В дальнейшем, каждый отдельный символ brainfuck компилируется в одну или несколько ast-нод daScript, который затем могут быть просимулированы.

(Раздел `daScript` про симуляцию и устройство виртуальной машины daScript)
{% post_link 231014-vm 'Устройство интерпретаторов lua-jit и daScript' %} 

(Генерация кода с помощью [реификации выражений](https://dascript.org/doc/reference/language/reification.html))
{% post_link 220702-dascript-macro2 'daScript macro - 2' %}

Если говорить о терминологии, то brainfuck можно рассматривать как `предметно-ориентированный язык (DSL)`. Переменные состояния tape и tapePos вместе составляют `семантическую модель` этого языка, которая настраивается с помощью DSL, а затем транслируется в синтаксическое дерево на `daScript` (в терминах Мартина Фаулера из книги "Предметно-ориентированные языки программирования").

Время выполнения такой скомпилированной функции **в режиме интерпретации**:

```
e:\src\daScript_my\bin\Release>daScript.exe brainfuck.das
[I] total 29.28014399999999995 sec
```

Это немного медленнее скомпилированной JiT-версии, но уже быстрее AoT версии интерпретатора.

## Macro + JiT
Дальше будет интереснее. Наша скомпилированная версия функции представляет собой по сути развёрнутую трассированную версию исполнения кода (и занимающую больше памяти). Попробуем применить к ней макрос [jit]:

```cpp
fn |> append_annotation("$", "unsafe_deref", args)
fn |> append_annotation("$", "jit", args)
```

```
e:\src\daScript_my\bin\Release>daScript.exe brainfuck.das
[I] total 0.85775599999999996 sec
```

0.85 секунды! (плюс около секунды на само время компиляции функции). llvm jit умеет сворачивать идущие подряд повторяющиеся операторы инкремента и декремента, за счёт чего получилось ускорение в 30 раз (и соотвествующее уменьшение размера функции).

Для сравнения -- compile-time версия на nim работает ~3 секунды и тратит ~20 секунд на компиляцию (nim работает медленно в compile-time режиме).

## Оптимизации Brainfuck -> daScript AST

Получается интересная цепочка преобразования кода:

```
bf --> (bf macro) --> dascript ast --> (dascript simulate - unsafe deref macro + optimizations) --> dascript ast optimized --> (llvm macro) --> llvm native optimized code --> (execute)
```

На каждом из шагов происходят серьёзные трансформации кода, которые могут включать оптимизации. Можно рассмотреть оптимизации в обратном порядке:
- llvm -- бекэнд генерации кода оптимизирует байт-код, на этом этапе заметен эффект от сворачивания идущих подряд операций
- dascript simulate -- при симуляции ast-дерева выбираются оптимизированные частные версии нод, мелкие ноды могут "сплавляться" в более крупные, применяются кастомные макросы, трансформирующие дерево по различным правилам
- bf macro -- на данном уровне производится трансляция команд brainfuck в ноды dascript, пока без оптимизаций

Оптимизации на стадиях трансформаций llvm были сделаны библиотекой из "комплекта" языка, на стадиях преобразования daScript -- как встроенными в язык оптимизациями, так и добавленными для своего кода вручную. Можно теперь попробовать добавить пару оптимизаций на "стороне DSL", т.е. в макрос трансформации `brainfuck->daScript`.

На данном этапе первую тупую и наивную реализацию уже получилось разогнать где-то в 20000 раз, и это отличный повод разогнать ещё немного :)

Можно выбрать несколько простых паттернов brainfuck кода и попробовать распознавать их и генерить более оптимальный код для этих частных случаев:

- цепочка повторяющихся операций. Например, "+++++" можно интерпретировать не как 5 отдельных инкрементов, а как одну операцию увеличения на 5. Эту свёртку делает llvm для версии `Macro+JiT`, но если сделать её в своём макросе, то она также ускорит и обычный режим интерпретации
- паттерн [-] можно интерпретировать как очистку ячейки памяти одной операцией
- [->+<] - чуть более сложный паттерн, который часто встречается в примерах на brainfuck, "сложение двух ячеек с очисткой исходной", может быть интерпретирован как 2 команды вместо цикла
- можно продолжать обнаруживать и добавлять всё более сложные паттерны

(Приём с отслеживанием паттернов подходит, естественно, не только для brainfuck-кода, но и для любых DSL)

"Продвинутая" версия макроса, отслеживающая перечисленные паттерны

```cpp
def seachRepeats(symIt; var sym:int&; symbolToCheck)
    var count = 1
    while next(symIt, sym)
        if sym == symbolToCheck
            ++count
        else
            return count
    return count

def match_reset(data: array<int>)
    return length(data) == 3 && data[0] == '[' && data[1] == '-' && data[2] == ']'

def match_add_right_reset(data: array<int>)
    return length(data) == 6 && data[0] == '[' && data[1] == '-' && data[2] == '>' && data[3] == '+' && data[4] == '<' && data[5] == ']'

def generateFunction(uniqueName, code)
    let seqStr = string(code)

    var blkArr : array<array<ExpressionPtr>>; defer_delete(blkArr)

    var blk : array<ExpressionPtr>; defer_delete(blk)
    blkArr |> emplace(blk)

    var cyclePatternChecker:array<int>

    var initBlock <- quote() <|
        var tape: array<uint8>
        var tapePos : int
        tape |> resize(1000000)
        var ptape = addr(tape[0])
    //blkArr[0] |> emplace_new <| initBlock
    unsafe
        var _block <- reinterpret<smart_ptr<ExprBlock>>(reinterpret<smart_ptr<ExprMakeBlock>> initBlock)._block
        for blockItem in _block.list
            blkArr[0] |> emplace_new <| blockItem
    var symIt <- unsafe(each(seqStr))
    var sym : int
    var repeat = false
    var count : int = 1
    while repeat || next(symIt, sym)
        repeat = false
        if sym == '+'
            cyclePatternChecker |> push(sym)
            repeat = true
            count = seachRepeats(symIt, sym, '+')
            back(blkArr) |> emplace_new <| qmacro_expr( ${ ptape[tapePos] = uint8(int(ptape[tapePos]) + $v(count)); })
        elif sym == '-'
            cyclePatternChecker |> push(sym)
            repeat = true
            count = seachRepeats(symIt, sym, '-')
            back(blkArr) |> emplace_new <| qmacro_expr( ${ ptape[tapePos] = uint8(int(ptape[tapePos]) - $v(count)); })
        elif sym == '>'
            cyclePatternChecker |> push(sym)
            repeat = true
            count = seachRepeats(symIt, sym, '>')
            back(blkArr) |> emplace_new <| qmacro_expr( ${ tapePos +=  $v(count); })
        elif sym == '<'
            cyclePatternChecker |> push(sym)
            repeat = true
            count = seachRepeats(symIt, sym, '<')
            back(blkArr) |> emplace_new <| qmacro_expr( ${ tapePos -= $v(count); })

        elif sym == '.' { back(blkArr) |> emplace_new <| qmacro_expr( ${ print(int(ptape[tapePos]) |> to_char); }); }
        elif sym == ',' { back(blkArr) |> emplace_new <| qmacro_expr( ${ ptape[tapePos] = uint8(getchar()); }); }
        elif sym == '['
            cyclePatternChecker |> clear
            cyclePatternChecker |> push(sym)
            var blk1 : array<ExpressionPtr>; defer_delete(blk1)
            blkArr |> emplace(blk1)
        elif sym == ']'
            cyclePatternChecker |> push(sym)
            if match_reset(cyclePatternChecker)
                //match [-]
                blkArr |> pop()
                back(blkArr) |> emplace_new <| qmacro_expr( ${ ptape[tapePos] = uint8(0); })
            elif match_add_right_reset(cyclePatternChecker)
                //match [->+<]
                blkArr |> pop()
                back(blkArr) |> emplace_new <| qmacro_expr( ${ ptape[tapePos+$v(count)] = uint8(int(ptape[tapePos+$v(count)]) + int(ptape[tapePos])); })
                back(blkArr) |> emplace_new <| qmacro_expr( ${ ptape[tapePos] = uint8(0); })
            else
                //usual cycle
                var last <- back(blkArr)
                blkArr |> pop()
                var whileExpr <- qmacro_expr <|
                    while ptape[tapePos] != uint8(0)
                        $b(last)
                back(blkArr) |> emplace_new <| whileExpr

            cyclePatternChecker |> clear
        else { }

    var fnArguments : array<VariablePtr>;
    var fn <- qmacro_function(uniqueName) <| $ ($a(fnArguments))
        unsafe
            $b(blkArr[0])
    defer_delete(fn)

    var args:array< tuple<argname:string;argvalue:RttiValue> >
    fn |> append_annotation("$", "jit", args)
    fn |> append_annotation("$", "unsafe_deref", args)
    //print(describe(fn))
    compiling_module() |> add_function(fn)
```

Результат:

```
e:\src\daScript_my\bin\Release>daScript.exe brainfuck.das
[I] total 0.70142899999999999 sec
```
Еще на 17% быстрее 
*Из замеров явно стоило бы еще вынести print*

## Немного выводов

- Основа оптимизации -- написание грамотного кода на основном языке.
- Техники JiT-компиляции (особенно в сочетании с кодогенерацией или замерами hot участков) могут давать крутые результаты, в том числе превосходящие статическую компиляцию
- Организация цепочки преобразований кода в одной среде НАМНОГО удобнее, чем в разных (какой-нибудь вариант "кодоген на python" + макросы/шаблоны + код на C++" - мрак с отладкой). Особенно для более длинных цепочек.
- Нормальные макросы = нормальная отладка и скорость компиляции DSL.

[Код примеров](https://github.com/spiiin/dascript_brainfuck)

*update от 14.01.2023* 
*[Compiled and Interpreted Languages: Two Ways of Saying Tomato](https://tratt.net/laurie/blog/2023/compiled_and_interpreted_languages_two_ways_of_saying_tomato.html) - похожие замеры на rust*





