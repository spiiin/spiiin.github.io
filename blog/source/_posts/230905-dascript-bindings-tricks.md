---
title: daScript - binding tricks
abbrlink: 1908536621
date: 2023-09-05 18:15:38
tags: dascript
---

Несколько примеров дополнительно к [Modules and C++ bindings](https://dascript.org/doc/reference/embedding/modules.html)

**`Привязка метода класса`**

```cpp
//структура с методами
struct MyStruct {
    int test() { return 42; }
};

//тип-обёртка, описание структуры для daScript
struct MyStructTypeAnnotation : ManagedStructureAnnotation <MyStruct> {
    MyStructTypeAnnotation(ModuleLibrary& ml) : ManagedStructureAnnotation("MyStruct", ml) {
        //тут может быть описание полей
    }
};
MAKE_TYPE_FACTORY(MyStruct, MyStruct)

//описание модуля
class Module_Tutorial02 : public Module {
public:
    Module_Tutorial02() : Module("tutorial_02") {   // module name, when used from das file
        ModuleLibrary lib;
        lib.addModule(this);
        lib.addBuiltInModule();

        //описание структуры
        addAnnotation(make_smart<MyStructTypeAnnotation>(lib));

        //регистрация метода
        using method_test = DAS_CALL_MEMBER(MyStruct::test);
        addExtern<DAS_CALL_METHOD(method_test)>(*this, lib, "mystruct_test", SideEffects::none,
            DAS_CALL_MEMBER_CPP(MyStruct::test));
    }
};
```

```dascript
//возможный вызов метода в daScript
var c: MyStruct
print("{c |> mystruct_test()}")
```

**`Привязка перегруженных и шаблонных функций с явным указанием сигнатуры`**

```cpp
int test2(int a) { return a; }

template <typename T>
T test3(T a) { return a; }

//явное указание сигнатуры функции для привязки
addExtern<int(*)(int),test2>(*this, lib, "test2", SideEffects::none, "test2");
addExtern<int(*)(int), test3>(*this, lib, "test3", SideEffects::none, "test3");
```

**`Возврат ссылки`**

```cpp
int gValue = 111;

int& getRef() { return gValue; }
inline int& getRefInline() { return gValue; }

addExtern<DAS_BIND_FUN(getRef), SimNode_ExtFuncCallRef>(*this, lib, "getRef", SideEffects::accessExternal, "getRef");
addExternTempRef<DAS_BIND_FUN(getRefInline), SimNode_ExtFuncCallRef>(*this, lib, "getRefInline", SideEffects::accessExternal, "getRefInline");
``````

```dascript
getRef() = 333
print("{getRef()}\n") //333

var v4& = getRefInline()
v4 = 444
print("{getRefInline()}\n") //444
```

**`Возврат ссылки по значению`**

```cpp
//returns a ref type by value,
addExtern<DAS_BIND_FUN(float4x4_translation), SimNode_ExtFuncCallAndCopyOrMove>(*this, lib, "translation",
        SideEffects::none, "float4x4_translation")->arg("xyz");
```

**`Привязка других типов нод AST`**
Способы привязать семантику вызова функции на стороне daScript к генерации других типов нод

```cpp
__forceinline float dot3(vec4f a, vec4f b){return v_extract_x(v_dot3_x(a, b));}
addExternEx<float(float3,float3),DAS_BIND_FUN(dot3)>(*this, lib, "dot", SideEffects::none, "dot3")->args({"x","y"});

addFunction(make_smart<BuiltInFn<SimNode_MatrixCtor<float3x3>,float3x3>>("float3x3",lib));
```

**`Хинты для аргументов`**

//TODO
```cpp
template <typename TT>
    struct registerVectorFunctions<TT> {
    //...
    addExtern<DAS_BIND_FUN(das_vector_pop<TT>)>(*mod, lib, "pop",
        SideEffects::modifyArgument, "das_vector_pop");
    //permanentArgFn
    addExtern<DAS_BIND_FUN(das_vector_clear<TT>),SimNode_ExtFuncCall,permanentArgFn>(*mod, lib, "clear",
        SideEffects::modifyArgument, "das_vector_clear");
    //explicitConstArgFn
    addExtern<DAS_BIND_FUN(das_vector_each<TT>),SimNode_ExtFuncCallAndCopyOrMove,explicitConstArgFn>(*mod, lib, "each",
        SideEffects::none, "das_vector_each");
    //temporaryArgFn
    //...
}
```

**`Симуляция walk`**

Создание своего типа-хендла, который в dascript будет обрабатываться как примитивный тип uint64

```cpp
struct MyHandle
{
    uint64_t id;
    //другие методы и свойства handle
};
MAKE_TYPE_FACTORY(MyHandle, MyHandle)

//описываем методы каста к примитивному типу и обратно
namespace das
{
    template <>
    struct cast<MyHandle>
    {
        static __forceinline MyHandle to(vec4f x) { return MyHandle{ (uint64_t)v_extract_xi64(v_cast_vec4i(x)) }; }
        static __forceinline vec4f from(MyHandle x) { return v_cast_vec4f(v_splatsi64(x.id)); }
    };
}

//описываем аннотацию типа с перегруженным методом walk
struct MyHandleAnnotation final : ManagedStructureAnnotation<MyHandle>
{
public:
    MyHandleAnnotation(ModuleLibrary& ml) : ManagedStructureAnnotation("MyHandle", ml) {}

    bool hasNonTrivialCtor() const override { return false; } //trivial type
    bool canClone() const override { return true; }

    virtual void walk(DataWalker& walker, void* data) override
    {
        if (!walker.reading)
        {
            const MyHandle* t = (MyHandle*)data;
            uint64_t eidV = t->id;
            walker.UInt64(eidV);
        }
    }

    virtual SimNode* simulateClone(das::Context& context, const das::LineInfo& at, das::SimNode* l, das::SimNode* r) const override
    {
        return GenCloneNode<MyHandle>::simulateClone(context, at, l, r);
    }
};
```

**`Симуляция итератора`**
Для кастомного контейнера можно задать прямой способ обращения к элементам (для простоты -- нешаблонная версия кода)

```cpp
//кастомный вектор из элементов MyHandle
struct MyVector
{
    std::vector<MyHandle> vec;
};
MAKE_TYPE_FACTORY(MyVector, MyVector)

//создаём вектор в C++ и делаем функцию доступа к нему из daScript
MyVector gVector = { {MyHandle{1}, MyHandle{3}, MyHandle{5}} };
auto& getArrayRef() { return gVector; }

//кастомный итератор
struct MyIterator : Iterator
{
    MyIterator(MyVector* ar) : array(ar) {}

    virtual bool first(das::Context&, char* _value) override
    {
        if (!array->vec.size())
            return false;
        iterator_type* value = (iterator_type*)_value;
        *value = array->vec.begin(); //пишем в память, выделенную в daScript под итератор
        end = array->vec.end();
        return true;
    }

    virtual bool next(das::Context&, char* _value) override
    {
        iterator_type* value = (iterator_type*)_value;
        ++(*value); //сдвигаем курсор на следующий элемент
        return *value != end;
    }

    virtual void close(das::Context& context, char* _value) override
    {
        //освобождаем итератор, по хорошему нужно еще занулить value
        context.heap->free((char*)this, sizeof(MyIterator));
    }

    MyVector* array = nullptr;
    typedef decltype(array->vec.begin()) iterator_type;
    iterator_type end;
};

//в аннотации типа вектора говорим:
//"при обращении к итератору контейнера из daScript будет создан кастомный класс итератора и вызываться его методы"
struct MyVectorAnnotation final : ManagedStructureAnnotation<MyVector, false>
{
protected:
    TypeDeclPtr vecType;
public:

    MyVectorAnnotation(das::ModuleLibrary& ml) : ManagedStructureAnnotation("MyVector", ml)
    {
        cppName = "MyVector";

        vecType = makeType<MyHandle>(ml);
        vecType->ref = true;
    }

    virtual bool isIterable() const override { return true; }

    virtual das::TypeDeclPtr makeIteratorType(const das::ExpressionPtr&) const override
    {
        return das::make_smart<das::TypeDecl>(*vecType);
    }

    //используем наш итератор для обхода
    virtual das::SimNode* simulateGetIterator(das::Context& context, const das::LineInfo& at,
        const das::ExpressionPtr& src) const override
    {
        auto rv = src->simulate(context);
        return context.code->makeNode<das::SimNode_AnyIterator<MyVector, MyIterator>>(at, rv);
    }
};

//не забываем добавить в модуль аннотации
addAnnotation(make_smart<MyHandleAnnotation>(lib));
addAnnotation(make_smart<MyVectorAnnotation>(lib));
addExtern<DAS_BIND_FUN(getArrayRef), SimNode_ExtFuncCallRef>(*this, lib, "getArrayRef",
    SideEffects::accessExternal, "getArrayRef");
```

```dascript
//теперь можно пройти по C++-контейнеру из daScript без дополнительных затрат на итерации
for v in getArrayRef()
    print("{v}\n")
```


