---
title: daScript - binding tricks 2
abbrlink: 1528253159
date: 2024-04-03 14:35:05
tags: dascript
---

- {% post_link 230905-dascript-bindings-tricks %}

Ещё несколько примеров байндингов типов из `C++` и `daScript`.

## Standart-layout структуры

Пустой базовый класс C++:
```cpp
class MyClass
{
public:
    int hidden;
};
void printMyClass(const MyClass& a) {
    std::cout << a.hidden << std::endl;
}
```
(переменная hidden -- просто для проверок, что класс инициализирован)

Привязка его к daScript:

```cpp
struct MyClassAnnotation final : ManagedStructureAnnotation<MyClass> {
    MyClassAnnotation(ModuleLibrary& ml) : ManagedStructureAnnotation("MyClass", ml) {
    }
    void init() {
    }
};
MAKE_TYPE_FACTORY(MyClass, MyClass);
```

..и добавление в модуль

```cpp
class Module_Tutorial : public Module {
public:
    Module_Tutorial() : Module("tutorial") {   // module name, when used from das file
        ModuleLibrary lib(this);
        lib.addBuiltInModule();

        addAnnotation(make_smart<MyClassAnnotation>(lib));
        addCtorAndUsing<MyClass>(*this, lib, "MyClass", "MyClass");
        addExtern<DAS_BIND_FUN(printMyClass)>(*this, lib, "printMyClass", SideEffects::worstDefault, "printMyClass");
    }
};

REGISTER_MODULE(Module_Tutorial);

...
//где-то в регистрации модулей
NEED_MODULE(Module_Tutorial);
```

определение `ManagedStructureAnnotation` выглядит как:

```cpp
template <typename OT,
    bool canNew = is_default_constructible<OT>::value,
    bool canDelete = canNew && is_destructible<OT>::value
> struct ManagedStructureAnnotation ;
```

Это структура разбирает данные о типе `OT` с помощью `std::type_traits` и устанавливает его свойства, на основе которых daScript знает, что можно/нельзя делать с типом.

```cpp
virtual bool hasNonTrivialCtor() const override {
    return !is_trivially_constructible<OT>::value;
}
virtual bool hasNonTrivialDtor() const override {
    return !is_trivially_destructible<OT>::value;
}
virtual bool hasNonTrivialCopy() const override {
    return  !is_trivially_copyable<OT>::value
        ||  !is_trivially_copy_constructible<OT>::value;
}
virtual bool isPod() const override {
    return is_standard_layout<OT>::value && is_trivial<OT>::value;
}

virtual bool canMove() const {
    return !hasNonTrivialCopy();
}
virtual bool canCopy() const {
    return !hasNonTrivialCopy();
}
```

Пока всё тривиально, `MyClass` -- standart layout структура, не требующая дополнительной инициализации.
```dascript
//объявления на стеке
var c1 = [[MyClass]] 
var c2 = MyClass()
var c3 : MyClass
printMyClass(c1) //0

//или на хипе
var c4 = new MyClass()
printMyClass(*c4) //0

//или создание временного объекта с помощью идиомы using:
using() <| $ ( var c5: MyClass# )
    printMyClass(c5) //0
```

## Non standart layout классы

Попробуем добавить в класс что-нибудь, что потребует его инициализации:

```cpp
class MyClass
{
public:
    int hidden = 42; //инициализация члена
    std::string str; //non-stardary layout член
    MyClass(const MyClass& other) : str(other.str) {} //copy-ctor
    virtual void virtualFunction() const {} //virtual function
    //
    MyClass(const char* data): str(data) {}
    MyClass() = default
};

//...
//привязки
addCtorAndUsing<MyClass, const char*>(*this, lib, "MyClass", "MyClass")->args({ "str" });
addCtorAndUsing<MyClass, const MyClass&>(*this, lib, "MyClass", "MyClass")->args({ "other" });

using _method_100 = das::das_call_member< void(MyClass::*)() const, &MyClass::virtualFunction >;
makeExtern<DAS_CALL_METHOD(_method_100), SimNode_ExtFuncCall>(lib, "virtualFunction", "das::das_call_member< void(MyClass::*)(), &MyClass::virtualFunction >::invoke")
    ->addToModule(*this, SideEffects::worstDefault);
```

Байндинг класса при перекомпиляции "увидит", что теперь класс нетривиальный, и правильно переопределит его свойства. Теперь класс не может быть локальным, не может быть скопирован или перемещён:
```cpp
bool canCopy() const override { return false; }
bool canMove() const override { return false; }
bool isLocal() const override { return false; }
```

Соотвественно, тот же код на daScript выдаст ошибки компиляции, при попытке создать класс без инициализации:
```dascript
//можно создать класс на хипе:
var a <- new MyClass("hello heap")
printMyClass( *a ) //42

//можно создать временный объект с помощью using:
using("hello temp") <| $(var c5: MyClass explicit)
    printMyClass(c5) //42

//можно создать временный объект на стеке и передать его в качестве параметра
//(конструктор класса ничем не отличается от обычной функции)
printMyClass(MyClass("hello temp"))

//нельзя создать объект, требующий перемещения (массив из одного элемента)
printMyClass([[MyClass()]])
//нельзя переместить объект
var c1 <- MyClass()

//нельзя скопировать объект
var c1 = MyClass()
```

`daScript` достаточно консервативно определяет, что объект нельзя копировать/перемещать, вообще говоря, если у класса есть конструктор копирования, то его можно разрешить копировать, если просто явно переопределить функцию canCopy в аннотации-обёртке класса

```cpp
    bool isCopyConstructable = std::is_copy_constructible<MyClass>::value;
    bool canCopy() const override { return isCopyConstructable; }
    bool canClone() const override { return isCopyConstructable; }
    bool canMove() const override { return isCopyConstructable; }
    //но нельзя создавать локальный переменные, так как они позволяет не инициализировать класс
    bool isLocal() const override { return false; }
```
*Если можно построить объект из другого объекта, то можно и copy/clone/move?*

```dascript
//теперь можно copy/clone/move
var a <- new MyClass("hello heap")
var b = new MyClass()
*b = *a
*b := *a
*b <- *a
```

Также в unsafe блоке теперь можно делать небезопасные, но интересные штуки:
```dascript
struct Params
    a: MyClass
unsafe
    //создаём локальную переменную на стеке
    var m = MyClass("hello_local")

    //создаём контейнер неинициализированных объектов
    //  которые можно построить позже в этой памяти
    //  (аналог placement new в c++)
    var n = [[MyClass(m)]]

    //создаём структуру из неинициализированных объектов
    //( аналог stackframe)
    var s : Params
    printMyClass(s.a)
    //s.a |> virtualFunction() //пока нельзя обращаться к объекту
    s.a <- MyClass("hello_local")
    s.a |> virtualFunction() //vtable инициализирована
    printMyClass(s.a) //42
```

## Аргументы и результаты

Если попытаться привязать такую функцию:
```cpp
void functionWithClassArgument(MyClass a) { }
```
компилятор начнёт ругаться на то, что не определён шаблон `cast_arg<MyClass>::to`. daScript-функции представляют свои аргументы и результаты в виде 128-битного типа `vec4f`, так что для кастомных типов необходимо описать способ преобразования с помощью частичной специализации этого шаблона.

```cpp
template <> struct cast_arg<MyClass> {
    static __forceinline const MyClass& to(Context& ctx, SimNode* node) {
        vec4f res = node->eval(ctx);
        return *cast<MyClass*>::to(res);
    }
};
```

Другие примеры возможных способов определения преобразования:

```cpp
//если тип standart-layout и меньше 128 байт -- можно просто скопировать память
template <> struct cast_arg<const ImVec2 &> {
    static __forceinline ImVec2 to ( Context & ctx, SimNode * node ) {
        vec4f res = node->eval(ctx);
        ImVec2 v2;
        memcpy(&v2,&res,sizeof(ImVec2));
        return v2;
    }
};

//для типов-хэндлеров можно указать способ приведения хэндлера к какому-нибудь базовому типу
//  (каст указателей можно рассматривать как частный случай хэндлеров, уже определенных явно)
template <> struct cast_arg<ax::NodeEditor::NodeId> {
    static __forceinline ax::NodeEditor::NodeId to ( Context & ctx, SimNode * node ) {
        vec4f res = node->eval(ctx);
        return ax::NodeEditor::NodeId(cast<int32_t>::to(res));
    }
};
template <> struct cast_res<ax::NodeEditor::NodeId> {
    static __forceinline vec4f from ( ax::NodeEditor::NodeId node, Context * ) {
        return cast<int32_t>::from(int32_t(node.Get()));
    }
};

//для типов-прокси можно определить способ построения прокси из базового типа/извлечения базового типа
template <> struct cast_arg<const sf::String &> {
    static __forceinline sf::String to ( Context & ctx, SimNode * node ) {
        char * pstr = node->evalPtr(ctx);
        return sf::String(pstr ? pstr : "");
    }
};
template <> struct cast_res<sf::String> {
    static __forceinline vec4f from ( const sf::String & str, Context * context ) {
		auto text = context->stringHeap->allocateString(str);
        return cast<char *>::from(text);
    }
};
```

Из пары примеров выше видно, что для привязки функций, возвращающих тип в качестве результата, необходимо определить специализацию шаблона `cast_res` с функцией `from`. Это верно для standard layout структур, но для сложного класса (с созданием временного объекта на хипе, по аналогии с sf::String) daScript бросает assert:

```
addExtern(getMyClass_ExtFuncCall)::failed
  this function should be bound with addExtern<DAS_BIND_FUNC(getMyClass_ExtFuncCall), SimNode_ExtFuncCallAndCopyOrMove>
  likely cast<> is implemented for the return type, and it should not
```

говорит этот ассерт о том, что вместо того, чтобы создавать временный объект, что тормознуто, лучше использовать специальную ноду языка, которая возвращает уже созданный объект. Такое себе принуждение к оптимизации.

```cpp
class MyClass {
    MyClass getMyClass() const{ return *this; }
};

using _method_2 = das::das_call_member< MyClass(MyClass::*)() const, &MyClass::getMyClass >;

//makeExtern<DAS_CALL_METHOD(_method_2), SimNode_ExtFuncCall >(lib, "getMyClass_ExtFuncCall", "das::das_call_member< MyClass(MyClass::*)() const, &MyClass::getMyClass >::invoke")
//    ->addToModule(*this, SideEffects::worstDefault); //work with pod type, but not if type has something not trivial

makeExtern<DAS_CALL_METHOD(_method_2), SimNode_ExtFuncCallAndCopyOrMove >(lib, "getMyClass_ExtFuncCallAndCopyOrMove", "das::das_call_member< MyClass(MyClass::*)() const, &MyClass::getMyClass >::invoke")
    ->addToModule(*this, SideEffects::worstDefault);
```

Теперь в daScript можно использовать эти функции:

```dascript
functionWithClassArgument(MyClass("hello arg"))
MyClass("hello res")|> getMyClass_ExtFuncCallAndCopyOrMove()
```

## Reflection over C++

Вся эта шаблонная магия привязок генерится не руками, а генератором привязок [dasClangBind](https://github.com/GaijinEntertainment/daScript/tree/master/modules/dasClangBind/bind). Распознавание инфы о типах сделано на уровне самого кода daScript, а не генератора, чтобы сам код генератора и сгенерированный код был более простым и однообразным. Но все примеры обёрток, сделанные `dasClingBind`, сделаны для библиотек с C-интерфейсом, которые почти не требуют ручного вмешательства. Но как только дело доходит до реального C++ кода, вылезает всё и сразу. Описанные в статье приёмы позволяют побороть большую часть сложности, и нагенерировать что-нибудь серьёзное, типа привязок классов `Unreal Engine` (с небольшими доработками напильником).

Примеры привязок либ с c-интерфейсом через `dasClangBind`:
- {% post_link 220530-dascript-bindings %}
- {% post_link 220612-dascript-assimp %}

Другие подходы:
[Automatic Language Bindings](https://floooh.github.io/2020/08/23/sokol-bindgen.html) -- размышления о способах генерации привязок к языкам от автора sokol gfx (тоже c-style, с помощью clang json)
[Using C Libraries in Zig](https://medium.com/@eddo2626/lets-learn-zig-4-using-c-libraries-in-zig-5fcc3206f0dc) -- прозрачный импорт C из zig. с Си (не С++) вообще все достаточно просто
[Binding Nim to C++ std::list](https://scripter.co/binding-nim-to-c-plus-plus-std-list/) -- читерский подход в nim, без интерпретации и с транспиляцией в C++ можно просто встраивать и использовать куски плюсового кода.
[Circle](https://github.com/seanbaxter/circle) -- "бэтменский" альтернативный компилятор с встроенными compile-time фичами, включая рефлексию. Автор публикует прогресс в [твиттере](https://twitter.com/seanbax)
[cppyy: Automatic Python-C++ bindings](https://cppyy.readthedocs.io/en/latest/) -- хардкор с использованием интерактивного компилятора C++ cling, прозрачный парсинг, компиляция и генерация привязок на лету









