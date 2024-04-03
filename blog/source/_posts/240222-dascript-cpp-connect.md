---
title: Связь daScript классов с C++-классами
abbrlink: 2757704498
date: 2024-02-22 18:46:32
tags:
  - dascript
  - cpp
---

- {%post_link 230112-dascript-oop %} - перенёс часть про связь с C++-типами в отдельную заметку

# Связь с C++ типами

https://github.com/GaijinEntertainment/daScript/blob/master/examples/tutorial/tutorial03.cpp#L15
Базовый пример прокидывания C++ класса в daScript. Похоже на другие скриптовые языки, создаётся класс-обёртка (`ManagedStructureAnnotation`) над типом, которая позволяет привязать и настроить отображение полей и методов структуры на тип в daScript, а также переопределить группу методов, определяющих свойства этого типа в daScript.

```fsharp
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

```fsharp
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

```fsharp
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
```fsharp
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
