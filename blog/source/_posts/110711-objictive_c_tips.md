---
title: Objictive С tips
tags:
  - iphone
  - objc
abbrlink: 43611
date: 2011-07-11 20:40:00
---

**1. Смешивание языков.** 

Objective-C код совместим с сишным кодом, но не всегда совместим с С++.

Также существует язык Objective-C++, который позволяет более-менее свободно смешивать C++/Objective-C код. Компилятор gcc по умолчанию считает файлы с расширением .m содержащими код на Objective-C, а файлы с расширением .mm - код на языка Objictive-C++, но ему можно явно указать язык с помощью ключа -x В универсальных заголовочных файлах определить, в какой язык включается файл, можно, проверяя наличие макросимволов \_\_OBJC\_\_ или \_\_cplusplus. 

Чтобы вызывать Objective-C код из языка С++, удобнее всего сделать обычный С++-класс-обертку, содержащий членом указатель на класс Objective-C, так как наследование от него невозможно. 

Если возможности создать класс нет (Objective-C, в отличие от Objective-C++, не дает возможности создавать C++-классы), то проще всего заворачивать вызовы в глобальные функции, и звать их из С++. При этом такие функции, как и обычные сишные, в С++ коде надо объявлять в блоке extern "C", так как компилятор манглит их имена по правилам языка си. Проще это всё показать примером:  

```objc
//h-файл (общий заголовок)
 class ObjClassWrapper
 {
   ObjClass * objClass1;
   ObjClassWrapper(); { [[objClass1 alloc] init]; }
   ~ObjClassWrapper(); { [objClass1 dealloc]; }
   void method1(); { [objClass1 method1]; }
 };
 
 //mm-файл (язык Objective-C++)
 @interface ObjClass
 @end
 
 @implementation ObjClass
 -(void) method1
 {
   NSLog("Method1");
 }
 @end
 
 ObjClassWrapper::ObjClassWrapper() { [[objClass1 alloc] init]; }
 ObjClassWrapper::~ObjClassWrapper() { [objClass1 dealloc]; }
 void ObjClassWrapper::method1(); { [objClass1 method1]; }
 
 //m-файл (язык Objective-C)
 @implementation StaticObjClass
 +(void) method2
 {
   NSLog("Method2");
 }
 @end
 
 void method2() { [StaticObjClassObjClass method2]; }
 
 //c++-файл
 #include <universalHeader.h>   //объявляем класс-обертку
 extern "C" { void method2(); } //объявляем метод-обертку
 
 ObjClassWrapper w; w.method1();  //зовем код на Objective-C
 method2();
 ```

Про смешивание языков и вызов кода на С++ из языка Objective-C есть статья <http://touchdev.ru/documents/963>

**2. True/Yes**

Всегда интересно ([раз](http://stackoverflow.com/questions/615702/is-there-a-difference-between-yes-no-true-false-and-true-false-in-objective-c) [два](http://stackoverflow.com/questions/541289/objective-c-bool-vs-boo) [три](http://stackoverflow.com/questions/6420987/why-does-objective-c-use-yes-no-macro-convention-instead-of-true-false)), нафига разные ключевые слова?

[Главное, чтобы помещалось](http://wasm.ru/article.php?article=1022005)

**3. Динамический Objective-C**

**3.1**
Так как Objective-C является динамической веткой развития языка С++, то проверка наличия методов у экземляров выполняется только во время запуска приложения.

Методы среды выполнения, позволяющие динамически оперировать классами и методами классов, находятся в библиотеке `libobjc.A.dylib`, которая подключается к любой программе.

С помощью них можно, например, сделать подмену одного класса другим во всех местах, в которых будет обращения к оригинальному классу:  

```
[[MyBundle class] poseAsClass:[NSBundle class]]; //заменяем класс бандла своим, переопределяя его стандартное поведение.
```

**3.2**
Однако такой метод уже признан apple устаревшим и вместо него можно подменять отдельные методы класса при помощи `class_getInstanceMethod` и свойства `method_imp` у селекторов класса. 

Описание интересного трика с подменой метода :
<http://www.cocoadev.com/index.pl?MethodSwizzling>

**3.3**
Помимо этого в самих классах также можно перегрузить служебные методы, используемые средой выполнения, например, присвоив новый класс свойству isa, проверяющему, какому классу принадлежит объект. Члены класса таким способом поменять нельзя, зато можно полностью сменить интерфейс.

```
obj->isa = [MyClass class];
```

**3.4**
Или можно перегрузить методы `forwardInvocation:` и `methodSignatureForSelector:` проверяющие само наличие метода у объекта
[ссылка](http://developer.apple.com/library/mac/documentation/Cocoa/Reference/Foundation/Classes/NSObject_Class/Reference/Reference.html#//apple_ref/occ/instm/NSObject/forwardInvocation:)

**3.5**
Ну и в самом языке есть возможность расширения существующих классов, вплоть до базового `NSObject`'а, используя категории
[ссылка](http://developer.apple.com/library/mac/#documentation/Cocoa/Conceptual/ObjectiveC/Chapters/ocCategories.html#//apple_ref/doc/uid/TP30001163-CH20-SW1)