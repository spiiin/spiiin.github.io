---
title: daScript macro - 2
tags: dascript
abbrlink: 4046309382
date: 2022-07-02 18:11:26
---

Еще немного про способы кодогенерации в макросах.

В {% post_link 220206-dascript-macro 'предыдущей заметке про макросы' %} описывались способы сгенерировать код выражений на языке.

Можно строить выражения с помощью ручной генерации абстрактного синтаксического дерева. Например, код для генерации выражения `let a = 40 + 2`:
```fsharp

var expr40 <- new [[ExprConstInt() value=40]]                               //40
var expr2 <- new [[ExprConstInt() value=2]]                                //2
var exprPlus <- new [[ExprOp2() op:="+", left := expr40, right := expr2]]  //40+2

var exprLet <- new [[ExprLet()]]                                           //let
exprLet_aSize.variables |> emplace_new() <| new [[Variable()    
    name := "a",                                                            //a
    _type <- new [[TypeDecl() baseType=Type tInt]],
    init <- exprPlus                                                        //=40+2
]]
```

Генерировать большие функции с использованием ExprXXX-кирпичиков утомительно, поэтому можно использовать макрос `quote`, который трансформирует переданное в него выражение в синтаксическое дерево этого выражения:

```fsharp
var exprLet <- quote <|
    let a = 40 + 2
print(describe(exprLet))
//output:
let  /*unused*/ a:auto const = (40 + 2);
```

В случае, если какую-либо часть выражения нужно сделать изменяемой, можно воспользовать макросом `apply_template`:

```fsharp
require daslib/templates
require daslib/templates_boost

var exprLet <- quote <|
    let VARIABLE_NAME = OP1 + OP2                                         //шаблон выражения
var exprLet_rules : Template                                              //правила переписывания выражения
exprLet_rules |> renameVariable("VARIABLE_NAME", "a")                     //замена одного имени на другое
exprLet_rules |> replaceVariable("OP1", new [[ExprConstInt() value=40]])  //замена одного выражения на другое
exprLet_rules |> replaceVariable("OP2", new [[ExprConstInt() value=2]]) 
apply_template(exprLet_rules, exprLet.at, exprLet)
```

Недавно в язык была добавлена фича по упрощению генерации правил переписываний выражений -- [expression reification](https://dascript.org/doc/reference/language/reification.html?highlight=reification) ([аналогичная фича из haxe](https://haxe.org/manual/macro-reification-expression.html)).
Её можно описать как DSL для задания правил переписывания выражений в шаблонах. Теперь генерацию того же самого выражения можно описать так:
```fsharp
let variableName = "a"
let op1 = 40
let op2 = 2
var exprLet <-qmacro <|
    let $i(variableName) = $v(op1) + $v(op2)
```
В таком виде строчка шаблона всё ещё остаётся похожим на сам код, который будет сгенерирован этим шаблоном, а не на синтаксическое дерево или таблицу с описанием правил. Пример на все поддерживаемые правила реификации выражений - [reification.das](https://github.com/GaijinEntertainment/daScript/blob/fe8868308a44d7ad57d823205dc183993f428d40/examples/test/misc/reification.das).

Переписанная кодо-генерированная функция инициализации структуры с использованием реификации получается где-то вдвое короче и проще:

```fsharp
def generateStructureInitFunction(var st:StructurePtr; ptrsTypeIndexes:array<int>&)
    let ptrFieldsLen = ptrsTypeIndexes |> length
    var blk : array<ExpressionPtr>; defer_delete(blk)

    //-------------------------
    //memblock.a`count = aCount

    for i in range(0, ptrFieldsLen)
        let argumentName = "{st.fields[ptrsTypeIndexes[i]].name}`count"
        blk |> emplace_new <| qmacro_expr(
            ${memblock.$f(argumentName) = $i(argumentName);}
        )

    //-------------------------
    //let aSize = typeinfo(sizeof *memblock.a) * aCount

    for i in range(0, ptrFieldsLen)
        let argumentName = "{st.fields[ptrsTypeIndexes[i]].name}"
        let argumentNameSize = "{argumentName}Size"
        let argumentNameCount = "{argumentName}`count"
        blk |> emplace_new <| qmacro_expr(
            ${let $i(argumentNameSize) = typeinfo(sizeof *memblock.$f(argumentName)) * $i(argumentNameCount);}
        )
    
    //-------------------------
    //memblock.mem |> resize(aSize + bSize + cSize)

    var sumArgumentsArray: array<ExpressionPtr>
    let zero = 0;
    sumArgumentsArray |> emplace<| qmacro_expr(${$v(zero);})
    for i in range(0, ptrFieldsLen) 
        let argumentName = "{st.fields[ptrsTypeIndexes[i]].name}"
        let nameSize := "{argumentName}Size"
        sumArgumentsArray |> emplace <| qmacro_expr(${$i(nameSize);})
    unsafe
        var sumExpr <- reduce(each(sumArgumentsArray), @@makeSumExpr)
        blk |> emplace_new <| qmacro_expr(
            ${memblock.mem |> resize($e(sumExpr));}
        )

    //-------------------------
    //memblock.a = reinterpret<int?> addr(memblock.mem[0])

    for i in range(0, ptrFieldsLen)
        let argumentName = "{st.fields[ptrsTypeIndexes[i]].name}"
        unsafe
            var exprStartAddress <- reduce_while(each(sumArgumentsArray), @@makeSumExpr,  @(e:ExpressionPtr; counter:int):bool => counter <= i)
            var subtype := st.fields[ptrsTypeIndexes[i]]._type
            var exprAssign <- qmacro_expr <|
                unsafe{ memblock.$f(argumentName) = reinterpret<$t(subtype)> addr(memblock.mem[$e(exprStartAddress)]); }
            blk |> emplace_new(exprAssign)
    //-------------------------

    //function signature
    var fnArguments : array<VariablePtr>;
    unsafe
        fnArguments |> emplace_new <| new [[Variable() at=st.at, name:= "memblock", _type <- new [[TypeDecl() baseType=Type tStructure, structType=addr(*st)]]]]
    var structT <- typeinfo(ast_typedecl type<int>)
    for i in range(0, ptrFieldsLen)
        let argumentName = "{st.fields[ptrsTypeIndexes[i]].name}`count"
        fnArguments |> emplace_new <| new [[Variable() at=st.at, name:= argumentName,  _type := intAstType]]
    var fn <- qmacro_function("init`struct`{st.name}") <| $ ($a(fnArguments))
        $b(blk)
    defer_delete(fn)
    compiling_module() |> add_function(fn)
```

Макрос `qmacro_expr` позволяет вставить сгенерированное выражение в текущий блок, а не генерировать новый блок. 
`reduce` - функция из стандартной библиотеки [functional](https://github.com/GaijinEntertainment/daScript/blob/fdc48d4d4cfc46f08f0ca2fd8938a05896b973a6/daslib/functional.das), позволяющая произвольным образом свернуть массив выражений с помощью функтора.
`reduce_while` -- её дописанная версия, позволяющая задать предикат остановки свёртки выражения по условию.
`qmacro_function` -- макрос для генерации сигнатуры функции и её определения

Получившаяся функция инициализации аналогична той, которая генерировалась в предыдущей заметке:
```fsharp
struct Vec2
    x, y : float

[memblock, dump_fields]
struct Memblock
    a: int?
    b: float?
    c: int?
    d: Vec2?

//output:
---gen_text--------------
// [modifyArgument]
[privateFunction]def init`struct`Memblock ( var memblock : Memblock; var a`count : int; var b`count : int; var c`count : int; var d`count : int )
        memblock.a`count = a`count
        memblock.b`count = b`count
        memblock.c`count = c`count
        memblock.d`count = d`count
        var aSize : int const = (a`count * 4)
        var bSize : int const = (b`count * 4)
        var cSize : int const = (c`count * 4)
        var dSize : int const = (d`count * 8)
        __::builtin`resize(memblock.mem,((((aSize + 0) + bSize) + cSize) + dSize))
        memblock.a = reinterpret<int?> addr(memblock.mem[0])
        memblock.b = reinterpret<float?> addr(memblock.mem[(aSize + 0)])
        memblock.c = reinterpret<int?> addr(memblock.mem[((aSize + 0) + bSize)])
        memblock.d = reinterpret<Vec2?> addr(memblock.mem[(((aSize + 0) + bSize) + cSize)])
```

[Код примера](https://github.com/spiiin/dascript_macro_tutorial/tree/master/memblock_2)
