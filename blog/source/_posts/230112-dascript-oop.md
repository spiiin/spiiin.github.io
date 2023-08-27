---
title: "daScript: ООП и всякое"
abbrlink: 1023396573
date: 2023-01-12 19:20:25
tags: dascript
---

# Структуры

## Структуры daScript, наследование
https://dascript.org/doc/reference/language/structs.html#struct-declaration

```cpp
struct V2
    x : float = -1.0f
    y : float

struct V3: V2
    z = 3.0f

[export]
def main
    let a : V3
    print("a = {a}\n")

    let b = V3()
    print("b = {b}\n")

    let c = [[V3 y = 2.0f]]
    print("c = {c}\n")

    let d = [[V3() y = 2.0f]]
    print("d = {d}\n")

    let e = [[V3() y = 2.0f, x = 1.0f]]
    print("e = {e}\n")

    //
    let pd = new [[V3() y = 2.0f]]
    print("pd = {pd}\n")

//Output:
a = [[ 0.000000000; 0.000000000; 0.000000000]]
b = [[ -1.000000000; 0.000000000; 3.000000000]]
c = [[ 0.000000000; 2.000000000; 0.000000000]]
d = [[ -1.000000000; 2.000000000; 3.000000000]]
e = [[ 1.000000000; 2.000000000; 3.000000000]]
pd = [[ -1.000000000; 2.000000000; 3.000000000]]
```

a,b,c,d,e - структуры, размещенные на стеке. В зависимости от способа объявления можно пропускать инициализацию полей по умолчанию -- круглые скобки в объявлении добавляют код инициализации (в порядке от родительской структуры к дочерним). Синтаксис с квадратными скобками позволяет изменить значения отдельных полей. Неинициализированные явно или по умолчанию поля инициализируются нулями -- получить в качестве значений неинициализированный мусор нельзя.

Ещё несколько примеров комбинаций синтаксиса инициализации, в первом случае создаётся структура, во втором -- массив структур, в третьем -- итератор
```cpp
    //where clause: post init function
    let f = [[V3 where $(var self) {
        self.x = 11.0f;
        self.y = 11.0f;
        self.z = 11.0f;
    }]]
    
    //array initialization, g_arr: V3[2]
    let g_arr = [[V3 
        x=1.0f, y=1.0f, z=1.0f;
        x=2.0f, y=2.0f, z=2.0f
    ]]

    //array comprehesion, h_arr : iterator<V3>
    let h_iter <- [[ for i in range(0, 10); [[V3 x=float(i), y=float(i), z=float(i)]]; where (i&1)==1 ]]
    let g_iter <- [[ for i in range(0, 10); invoke({ let fi = float(i); return [[V3 x=fi, y=fi, z=fi]]; }); where (i&1)==1 ]] // same
```

pd - указатель на структуру, размещенную в куче. Сама структура может быть инициализирована любым из перечисленных выше способов.

## Финализаторы
https://dascript.org/doc/reference/language/finalizers.html#finalizers

```cpp
    var d = [[V3() y = 2.0f]]
    print("d = {d}\n")
    delete d
    print("d = {d}\n")

    var pd = new [[V3() y = 2.0f]]
    print("pd = {pd}\n")
    unsafe { delete pd; }
    print("pd = {pd}\n")

    //Output
    d = [[ -1.000000000; 2.000000000; 3.000000000]]
    d = [[ 0.000000000; 0.000000000; 0.000000000]]
    pd = [[ -1.000000000; 2.000000000; 3.000000000]]
    pd = null
```

Финализатор по умолчанию для структуры зануляет память (в порядке от потомков к родителям, при необходимости зовёт финализаторы для членов структуры в порядке объявления). Для указателей -- после зануления полей структуры дополнительно меняет адрес указателя на null. Финализаторы для структур и классов зовутся вручную. Финализаторы не освобождают память, на которую указывает объект.

## Освобождение памяти
Модель памяти по умолчанию в daScript не подразумевает очистки памяти в ходе выполнения скрипта, за очистку отвечает хост-приложение, которое может просто освободить всю память контекста целиком -- пересоздание контекстов by design быстро и эффективно, так что такой способ предпочтительный.

Но можно настроить поведение контекста опцией `persistent_heap`:

```cpp
options persistent_heap = true

var pd = new [[V3() y = 2.0f]]
var pd2 = pd
unsafe
    print("addr(pd) = {reinterpret<uint>(pd)}\n")
    print("addr(pd2) = {reinterpret<uint>(pd2)}\n")
    delete pd
pd2.x = 33.0f
print("pd2 = {pd2}\n")

//Output
addr(pd) = 0xf1909e10
addr(pd2) = 0xf1909e10
pd2 = [[ 33.000000000; -431602080.000000000; -431602080.000000000]] //мусор
```
Я включил опцию `DAS_SANITIZER` при сборке daScript, чтобы после освобождения объектов в случае с persistent_heap память перезаписывалась мусорными значениями (0xCD, -431602080 если интерпретировать 0xCDCDCDCD как float-значение). В данном случае программа по счастливому стечению обстоятельств не упала, но благодаря санитайзеру видно, что указатель pd2 после удаления pd стал висячим -- указывает на свободную память, которая могла бы быть выделена другому объекту (объекту daScript того же контекста в случае `persistent_heap=false`, или любому другому объекту хост-приложения с `persistent_heap=true`).

Более "злобный" вариант примера:
```cpp
    var pd = new [[V3() y = 2.0f]]
    var pd2 = pd
    unsafe { delete pd; }
    var pd3 = new [[V3() x = 33.0f, y = 33.0f, z = 33.0f]]
    pd2.x = -100.0f // <----- kaboom!
    print("pd2 = {pd2}\n")
    print("pd3 = {pd3}\n")

    //Output
    pd2 = [[ -100.000000000; 33.000000000; 33.000000000]]
    pd3 = [[ -100.000000000; 33.000000000; 33.000000000]]
```
После освобождения память на которую указывали pd и pd2 была повторно отдана новому объекту, на который указывает pd3. Этот объект теперь может поменяться через указатель pd2. Должно быть понятно, насколько unsafe операция удаления -- код стал насколько же опасным (но и настолько же быстрым), как и код на языке си.

## Кастомные финализаторы

Финализатор можно переопределить, пример: финализатор для структуры V2

```cpp
def finalize(var v : V2)
    print("kill V2 {v}\n")

var d = [[ V3 x = 11.0f, y = 22.0f, z = 33.0f]]
delete d
print("d = {d}\n")

//Output
kill V2 [[ 11.000000000; 22.000000000]]
d = [[ 11.000000000; 22.000000000; 33.000000000]]
```

Вместо финализатора зануления по умолчанию вызывается функция, логгирующая поле. Также можно заметить неочевидную вещь (если думать о финализаторах как о деструкторах, но лучше не думать) -- финализаторы не зовутся в порядке от потомков к предкам, а как работают как обычные функции, daScript нашёл подходящую функцию, принимающую тип V2, и не вызвал зануления также и у поля z - т.е. финализатор родительской структуры "подошёл" к дочерней.

Более похожий на порядок вызова деструкторов в C/C++ код
{% blockquote %}
(**ещё раз, финализаторы -- это не деструкторы, они вызываются только при явном вызове оператора delete!**)
{% endblockquote %}

```cpp
def finalize(var v : V2 explicit)
    print("kill V2 {v}\n")

def finalize(var v : V3 explicit)
    finalize(cast<V2> v)
    print("kill V3 {v}\n")

[export]
def main
    var d = [[ V3 x = 11.0f, y = 22.0f, z = 33.0f]]
    delete d
    print("d = {d}\n")
//Output
kill V2 [[ 11.000000000; 22.000000000]]
kill V3 [[ 11.000000000; 22.000000000; 33.000000000]]
d = [[ 11.000000000; 22.000000000; 33.000000000]]
```

daScript не позволяет каст к дочерним типам `explicit`-аргументов.

Вместо перегрузки `finalize` можно перегрузить `def operator delete(var v : V2 explicit)` -- семантически более точно описывает, что для структур код финализатора будет вызван только в момент явного вызова оператора `delete`.

## Методы

Методы не могут быть объявлены при объявлении структур, но структуры могут хранить указатели на функции

```cpp
struct V2
    x : float
    y : float
    set = @@set

var a = V2()
a |> set(1.0f, 2.0f) //call function via pipe syntax
invoke(a.set, a, 1.0f, 2.0f)  // exactly same thing as above
a->set(1.0f, 2.0f)  // this one can call something else, if overridden in derived class.
```

Потомок может переопределить функцию

```cpp
struct V2
    x : float
    y : float
    set = @@set
struct V3: V2
    z : float
    override set = cast<auto> @@set_v3
    
def set(var thisV: V2; X, Y: float)
    with thisV
        x = X
        y = Y

def set_v3(var thisV: V3; X, Y: float)
    set(cast<V2> thisV, X, Y)
    with thisV
        z = 3.0f

[export]
def main
    var a = V3()
    a |> set_v3(1.0f, 2.0f) //non virtual call
    invoke(a.set, a, 1.0f, 2.0f)  // exactly same thing as above
    a->set(1.0f, 2.0f)  // this one can call something else, if overridden in derived class.
```
(https://github.com/GaijinEntertainment/daScript/blob/master/examples/test/unit_tests/override.das)

daScript позволяет создать две перегрузки функции set (а не определять дополнительное имя `set_v3`), принимающие V2 и V3, тогда можно переписать пример без использования дополнительного имени, с уточнением типа функции set перед кастом и последующим автоматическим приведением этого указателя к правильному типу, определённому в V2:

```cpp
struct V2
    x : float
    y : float
    set = @@<(var thisV: V2; X, Y: float):void> set
struct V3: V2
    z : float
    override set = cast<auto> @@<(var thisV: V3; X, Y: float):void> set //<------ cast
    
def set(var thisV: V2 explicit; X, Y: float)
    with thisV
        x = X
        y = Y

def set(var thisV: V3; X, Y: float)
    set(cast<V2> thisV, X, Y)
    with thisV
        z = 3.0f

[export]
def main
    var a = V3()
    a |> set(1.0f, 2.0f) //virtual call
    invoke(a.set, a, 1.0f, 2.0f)  // exactly same thing as above
    a->set(1.0f, 2.0f)
    print("{a}\n")
```
Здесь `explicit` в первом объявлении свободной функции `set` позволяет сделать некоторую магию -- несмотря на то, что эта функция "пропускает" только указатели на V2, это позволяет однозначно выделить эту функцию в приведении `set = @@<(var thisV: V2; X, Y: float):void> set` среди двух прегруженных (иначе возникла бы неоднозначность -- обе приводились бы с одинаковым приоритетом, и daScript выдавал бы ошибку). Но при этом сигнатура функции `V2'set` уже не содержит этого `explicit` (её тип выводится автоматически по правой части выражения, где явно указана сигнатура без `explicit`). Таким образом `V2'set` работает как виртуальная функция -- может принимать первым аргументом как `V2`, так и её потомков, которые не переопределили функцию.

# Классы
https://dascript.org/doc/reference/language/classes.html#classes

Классы в daScript -- это структуры "на стероидах". Немного отличий:
- Класс может быть отнаследован от структуры, но структура не может быть унаследована от класса (связано с тем, что классы могут иметь инициализаторы)
- Объявление локального класса на стеке небезопасно (требует явного unsafe)

Методы [реализованы](https://dascript.org/doc/reference/language/structs.html#structure-function-members) как указатели на функции, но с возможностью объявлять их в теле класса и переопределять с помощью ключевого слова `override` без явного каста типа метода, как было со структурами

```cpp
class V2
    x : float
    y : float
    def set(X, Y: float)
        x = X
        y = Y
class V3: V2
    z : float
    def override set(X, Y: float)
        V2`set(self, X, Y)
        z = 3.0f

[export]
def main
    var a = new V3()
    a->set(1.0f, 2.0f) //V3`set(*a, 1.0f, 2.0f)
    print("a = {a}\n")

//Output
a = [[ 0x29990d19b90; V3'__finalize/*V3'__finalize S<::V3>*/; 1.000000000; 2.000000000; V3`set/*V3`set S<::V3> Cf Cf*/; 3.000000000]]
```

Можно заметить, что имя объявленной внутри класса-функции манглится с помощью префикса-имени класса (`set -> V2'set`). Также внутри метода доступен указатель `self`, неявно передаваемый первым аргументов в методы класса.

Стоит более детально рассмотреть вывод результата.

## Порядок полей объекта в памяти
https://dascript.org/doc/reference/language/classes.html#implementation-details

Содержимое `a`:
```
a = [[
    0x29990d19b90; //указатель на rtti информацию
    V3'__finalize/*V3'__finalize S<::V3>*/;  //указатель на функцию-финализатор
    1.000000000; //x
    2.000000000; //y
    V3`set/*V3`set S<::V3> Cf Cf*/; //указатель на виртуальную функцию set
    3.000000000 //z
]]
```

Комментарии после имён функций -- замангленное имя функции и её сигнатуры (аргументы и результаты). 

{% blockquote %}
Расположение в памяти серьёзно отличается от C++ -- указатели на виртуальные функции хранятся не в отдельной таблице (vtable), а в каждом объекте класса в том порядке, в котором были объявлены функции. Это позволяет убрать один уровень индирекции при вызове функций (не нужно идти за адресом в виртуальную таблицу) и изменять адреса функций динамически для каждого отдельного объекта, но увеличивает расходы памяти на хранение указателей, и также может повлиять на выравнивание и padding между полями.
{% endblockquote %}

Тем не менее, для модификации порядка данных структур возможно написать собственный макрос, который будет хранить функции в самостоятельно сгенерированной таблице или выносить указатели на функции в конец структуры.
{%post_link 220206-dascript-macro %} -- пример макроса перестановки порядка полей при определении структур

```cpp
    unsafe
        print(
"\nsizeof(a) = {typeinfo(sizeof type<V3>)}\n
offset __rtti      = {typeinfo(offsetof<__rtti> type<V3>)} {reinterpret<uint>  addr(a.__rtti)} 
offset __finalize  = {typeinfo(offsetof<__finalize > type<V3>)} {reinterpret<uint>  addr(a.__finalize )} 
offset x           = {typeinfo(offsetof<x> type<V3>)} {reinterpret<uint>  addr(a.x)}
offset y           = {typeinfo(offsetof<y> type<V3>)} {reinterpret<uint> addr(a.y)}
offset set         = {typeinfo(offsetof<set> type<V3>)} {reinterpret<uint> addr(a.set)}
offset z           = {typeinfo(offsetof<z> type<V3>)} {reinterpret<uint> addr(a.z)}\n"
        )
Output:
sizeof(a) = 40
offset __rtti      = 0  0x4adb5f80
offset __finalize  = 8  0x4adb5f88
offset x           = 16 0x4adb5f90
offset y           = 20 0x4adb5f94
offset set1        = 24 0x4adb5f98
offset z           = 32 0x4adb5fa0
```

Существует также макрос `[cpp_layout]`, который не меняет порядок членов класса/структуры, но добавляет дополнительное правило выравнивания, как делают С/C++ -- в конце родительской структуры будет оставлено пространство для её выравнивания по максимальному выравниванию членов структуры -- например, если добавить в конце V2 поле на 4 байта `padding: uint8[4]`, то из-за выравнивания структуры в 8 байт (из-за указателей на 64-битной платформе), поле z, будет добавлено с отступом в 8 байт (без макроса daScript без проблем "встраивает" это поле сразу за 4-байтным отступом).

## Переопределение метода в экземпляре класса

Как было замеченно выше, каждый экземпляр класса/структуры хранит собственные копии указателей на функции, так что можно переопределить метод не на уровне класса-потомка, а в экземпляре класса (в пост-инициализаторе, или в любой момент после создания):
```cpp
class V2
    x : float
    y : float
    def set(X, Y: float)
        x = X
        y = Y

[export]
def main
    let fn <- @@ <| ( a : int )
        return a 

    unsafe
        //inplace init syntax
        var v_customset = [[ V2() 
            set <- @@ (var self : V2; X,Y : float) {
                self.x = X * 100.0f;
                self.y = Y * 100.0f;
            }
        ]]
        v_customset->set(1.0f, 2.0f)
        print("{v_customset.x}, {v_customset.y}\n")
        //Output: 100.000000000, 200.000000000

        //reset after construction, pipe + block syntax
        v_customset.set = @@ <| (var self : V2; X,Y : float)
            self.x = X * 200.0f
            self.y = Y * 200.0f
        print("{v_customset.x}, {v_customset.y}\n")
        //Output: 200.000000000, 400.000000000
```
*(более практичное применение этого -- паттерны типа event/callback)*

## RTTI
https://github.com/GaijinEntertainment/daScript/blob/f050f7f9a4aaaac75e454834663389c9d8ebd343/examples/test/unit_tests/reflection.das#L110

Пример вывода на экран информации о типе в runtime:

```cpp
require rtti
...
var a = new V3()
print("class_info(a): {class_info(a)}\n") 
describeStructure(*class_info(a))
//Output:
//https://dascript.org/doc/stdlib/rtti.html?highlight=rtti#StructInfo
class_info(a): [[ 0x6; V3; ; (_class|heapGC); 0x28; 0x93b8d07b5cc8cee; 0xcf51414d2d20b41e]]
struct V3
    __rtti : void?
    __finalize : function<(V2):void>
    x : float
    y : float
    set1 : function<(V2;float const;float const):void>
    z : float
```
Доступна информация о названиях и типах полей, а также мета-информация ([флаги](https://dascript.org/doc/stdlib/rtti.html?highlight=rtti#alias-structinfoflags) класс/структура, выделена на стеке/хипе, аннотации и т.п.).

Для того, чтобы передать и распознать аннотации, необходимо включить опцию `options rtti=true` (в противном случае, метаинформация о произвольных аннотациях выбрасывается после симуляции, [линк](https://github.com/GaijinEntertainment/daScript/wiki/options)). Пример:

```cpp
options rtti=true
...
class V3: V2
    [[test]] z : float
...
def describeStructure(sinfo)
    var anyAnn = false
    structure_for_each_annotation(sinfo) <| $(ann; annArgs)
        let argT = join([{for arg in annArgs; "{arg.name}{describeValue(get_annotation_argument_value(arg))}"}],",")
        print("[{ann.name}({argT})]\n")
    print("struct {sinfo.name}\n")
    for sfield in sinfo
        if sfield.annotation_arguments != null
            for arg in deref(sfield.annotation_arguments)
                print("\t[[{arg.name}]] ")
        describeVariable(sfield,"\t")
...
var a = new V3()
print("class_info(a): {class_info(a)}\n")
describeStructure(*class_info(a))

//Output:
struct V3
    __rtti : void?
    __finalize : function<(V2):void>
    x : float
    y : float
    set1 : function<(V2;float const;float const):void>
    [[test]] z : float //<-- аннотация test
```
[Полный пример](https://gist.github.com/spiiin/961974938919cc9233bacf0bb5c71cd1)

## Abstract и sealed-методы

Методы можно сделать абстрактыми, или закрытыми для переопределения

```cpp
class Test
    def abstract setX(X: int): void //необходимо явно определить сигнатуру метода -- тип аргументов и результата
    def sealed setY(Y: int)         //метод нельзя переопределить в потомках
        pass
```

## Видимость

- Из модуля экспортируются функции с аннотацией [export]

`options always_export_initializer=true` позволяет проставить аннотацию для всех инициализаторов на уровне модуля

- `private` для переменных и типов ограничивает их доступность из других модулей

```cpp
//module1.das
module module1

class private V1
    w : float

class private V2
    x : float
    y : float

class public V3: V2
    v1 : V1
    z : float = 3.0
...
//main.das
require module1
//можно звать инициализацию полей, и пост-инициализацию для V3 (также открываются поля V2), но нельзя инициализировать явно поле приватного класса V1
var a = new [[V3() x=1.0f, y=2.0f, z=3.0f]]
```

Приватными могут быть также поля и функции структур/классов

```cpp
class MyClass
    private a : int
    def private set_a(val:int)
        a = val
    def get_a
        return a
    def MyClass()
        self->set_a(42)
[export]
def main
    var f = new MyClass()
    print("f.a = {f->get_a()}\n")
```

## Инициализаторы

Инициализатор для класса -- это функция, у которой имя совпадает с именем класса. Так как классы -- надстройки над структурами, и все варианты синтаксиса иницилизации действуют и для них, то нет никакой гарантии того, что инициализатор класса будет вызван.

```cpp
class Test
    i : float
    def Test(I : float)
        i = I

def main
    var a <- new Test(33.0f)         //initializer called
    var b <- new Test()              //initializer dont called
    var c <- new [[Test() i = 2.0f]] //initializer dont called
```

## Интерфейсы
https://github.com/GaijinEntertainment/daScript/blob/eaecd72d6d44b46f5566dc4a0ce3956d5488672c/daslib/interfaces.das

Библиотека `interfaces` с помощью пары макросов позволяет реализовать паттерн интерфейса -- классы, который содержит только абстрактные методы. Макрос `implements` позволяет изобразить множественное наследование от интерфейсов.

```cpp
[interface]
class ITick
    def abstract tick (dt:float) : void

[interface]
class ILogger
    def abstract log (message : string) : void

[implements(ITick), implements(ILogger)]
class Foo
    ...
```

# Связь с C++ типами

https://github.com/GaijinEntertainment/daScript/blob/master/examples/tutorial/tutorial03.cpp#L15
Базовый пример прокидывания C++ класса в daScript. Похоже на другие скриптовые языки, создаётся класс-обёртка (`ManagedStructureAnnotation`) над типом, которая позволяет привязать и настроить отображение полей и методов структуры на тип в daScript, а также переопределить группу методов, определяющих свойства этого типа в daScript.

```cpp
struct Color {
    uint8_t r, g, b, a;
};
MAKE_TYPE_FACTORY(Color, Color);

struct ColorAnnotation : public ManagedStructureAnnotation<Color,true,true> {
    ColorAnnotation(ModuleLibrary & ml) : ManagedStructureAnnotation ("Color", ml) {
        //type fields
        addField<DAS_BIND_MANAGED_FIELD(r)>("r");
        addField<DAS_BIND_MANAGED_FIELD(g)>("g");
        addField<DAS_BIND_MANAGED_FIELD(b)>("b");
        addField<DAS_BIND_MANAGED_FIELD(a)>("a");
    }
    //type behaviour
    virtual bool isLocal() const override { return true; }
    virtual bool canCopy() const override { return true; } 
    virtual bool canMove() const override { return true; }
};

class Module_Tutorial03 : public Module {
public:
    Module_Tutorial03() : Module("tutorial_03") {
        ModuleLibrary lib;
        lib.addModule(this);
        addAnnotation(make_smart<ColorAnnotation>(lib));
    }
};
REGISTER_MODULE(Module_Tutorial03);
```

Более продвинутые [примеры](https://github.com/GaijinEntertainment/daScript/blob/master/examples/test/test_handles.cpp), также можно смотреть код [модулей](https://github.com/GaijinEntertainment/daScript/tree/master/modules).

## Наследование

Отнаследоваться от C++ типа нельзя (*ну, или я не нашёл способа сделать такой тип*).

Существует возможность передать в daScript связь родитель-потомок между C++-типами ([пример](https://github.com/borisbat/dasSFML/blob/4501a9167692180d138da4a487a42375a377db68/src/dasSFML.struct.add.inc#L134)), для upcast-приведения типов аргументов функций.

Пример организации связи между С++ и daScript-классами - [tutorial04](https://github.com/GaijinEntertainment/daScript/blob/master/examples/tutorial/tutorial04.cpp#L45).

{% nomnoml '{"style":"background-color:white;"}'%}
#fill: #eee8d5;
#.blob: fill=pink bold
[<blob> TutorialBaseClass (das)] -> [<blob>ExampleObject (das)]
[<blob> TutorialBaseClass (das)] --> [TutorialBaseClass (cpp)]
[BaseClass (cpp)] -> [BaseClassAdapter (cpp)]
[TutorialBaseClass (cpp)] -> [BaseClassAdapter (cpp)]
{% endnomnoml %}

В примере связь организуется через класс `BaseClassAdapter`, который наследуется одновременно от базового C++-класса и сгенерированного по das-коду C++-классу-адаптеру

```cpp
options remove_unused_symbols = false

//interface C++/daScript
class TutorialBaseClass
    def abstract update ( dt : float ) : void
    def abstract get_position : float3

// uncomment the section to generate C++ bindings for the TutorialBaseClass
// this code will generate tutorial04_gen.inc which contains C++ bindings

require fio
require ast
require daslib/cpp_bind
[init]
def generate_cpp_bindings
    let root = get_das_root() + "/examples/tutorial/"
    fopen(root + "tutorial04_gen.inc","wb") <| $ ( cpp_file )
        //generate c++ code from dascript rtti class information
        log_cpp_class_adapter(cpp_file, "TutorialBaseClass", typeinfo(ast_typedecl type<TutorialBaseClass>))
```

`TutorialBaseClass` - интерфейс между C++/daScript, который используется генератором C++-обёрток `log_cpp_class_adapter`, на выходе получается примерно такой C++-код:

```cpp
class TutorialBaseClass {
protected:
  enum {
    __fn_update = 0,
    __fn_get_position = 1,
  };
protected:
  static int _das_class_method_offset[2];
public:
  TutorialBaseClass ( const StructInfo * info ) {
    if ( _das_class_method_offset[0]==0 ) {
      _das_class_method_offset[__fn_update] = adapt_field_offset("update",info);
      _das_class_method_offset[__fn_get_position] = adapt_field_offset("get_position",info);
    }
  }
  ...
  static __forceinline Func get_get_position ( void * self ) {
    return getDasClassMethod(self,_das_class_method_offset[__fn_get_position]);
  }
  static __forceinline float3 invoke_get_position ( Context * __context__, Func __funcCall__, void * self ) {
    return das_invoke_function<float3>::invoke
      <void *>
        (__context__,nullptr,__funcCall__,
          self);
  }
};
int TutorialBaseClass::_das_class_method_offset[2];
```

Вызов:
```cpp
class BaseClassAdapter : public BaseClass, public TutorialBaseClass {
public:
    // in the constructor we store pointer to the original class and context
    // we also pass StructInfo of the daScript class to the generated class
    BaseClassAdapter ( char * pClass, const StructInfo * info, Context * ctx )
        : TutorialBaseClass(info), classPtr(pClass), context(ctx) { }
    ...
    virtual float3 getPosition() override {
        // we check if daScript class has 'get_position'
        if ( auto fn = get_get_position(classPtr) ) {
            // we invoke it, and return it's result
            return invoke_get_position(context, fn, classPtr);
        } else {
            return float3(0.0f);
        }
    }
protected:
    void *      classPtr;   // stored pointer to the daScript class
```

Класс не содержит особой магии, а просто хранит адреса daScript-функций и позволяет прозрачно для вызывающего C++-кода их вызывать и изменять.








