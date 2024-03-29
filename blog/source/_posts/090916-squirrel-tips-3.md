---
title: Squirrel tips - 3
date: 2009-09-16 09:27:00
tags: squirell
abbrlink: 43997
---

`Squirrel` простой, как 5 копеек, язык. Но документации по нему очень мало. Официальный [мануал](http://squirrel-lang.org/doc/squirrel2.html), и полупустые [вики](http://wiki.squirrel-lang.org/default.aspx/SquirrelWiki/SquirrelWiki.html) и [форум](http://squirrel-lang.org/forums/default.aspx) - все, что удалось найти (ну и исходный текст, если его считать за документацию). Поэтому я себе и пишу такие типсы о том, что не указано явно в доках.  
  
  
Есть вот в нем такой "спецэффект", в принципе, логичный, но о котором следует помнить - если в классе имеется слот-значение, то инициализировать его можно прямо в теле класса, а не в конструкторе, все экземпляры получат копию этого слота. А если так сделать со слотом-ссылкой, то все экземпляры получат по копии этой ссылки, указывающей на один и тот же созданный объект. Поэтому слоты-ссылки стоит инициализировать в конструкторе. На примере:  
  
```js
class A 
{
  val = "hello"              //числа, строковые константы и члены перечислений - значения
}
 
a1 <- A()
a2 <- A()
a2.val = " world!"            //a2.val изменилось, a1.val не изменилось
print (a1.val + a2.val);
 
 
class B
{
  wrong = {val = "hello"}            // ссылочный тип, если создать здесь экземпляр таблицы, она будет "шариться" всеми экземплярами
  right = null                       // не спешим создавать таблицу
  constructor()
  {
    right = {val = "hello"}          // создаем свою копию таблицы для каждого экземпляра класса
  }
}
 
b1 <- B()
b2 <- B()
print (b1.wrong == b2.wrong)         //true,  ссылки указывают на одну и ту же таблицу
print (b1.right == b2.right)         //false, у каждого объекта своя таблица
 
b2.wrong.val = " world!"             //b1.wrong.val ссылается сюда же... 
b2.right.val = " world!"
print (b1.wrong.val + b2.wrong.val)  //не вышло :(
print (b1.right.val + b2.right.val)  //ура!
```
  

Ну и еще штука, основанная на разнице между значениями и ссылками. Свободные переменные, переданные в функцию, вычисляются в момент определения функции. Т.е. если передать переменную-значение, то создастся ее копия и связи с исходной переменной не будет:  

```js
 a <- 10 function f () : (a) { print(a) } a = 5 f(); //выведет 10  
```

Если все же нужно передать значение в функцию, можно завернуть его в класс или таблицу и воспользоваться одним из двух способов связи - передать таблицу как свободную переменную (как было описано выше) или привязать ее как окружение для функции. Второй способ основан на том, что функция когда встречает неизвестное ей имя переменной, она ищет его в таблице this. Эту таблицу можно заменить на свою, используя функцию bindenv. Разница между двумя способами заключается в том, что в первом случае ссылка на таблицу копируется в скрытую переменную, а во втором используется слабая ссылка на таблицу. Это означает, что во втором случае когда исходная таблица будет удалена, функция перестанет работать! На примере:  
  
```js
t <- { a = "vaaar!" }                           //кладем нужную переменную в таблицу
 
f1  <- function () : (t)  { print (t.a) }   
f2  <- function () { print(a) }.bindenv(t)      //эта строка эквивалентна такой записи : function f2 ()  { print (a) }
                                                //                                       f2 = f2.binenv(t)
 
f1()                                            //vaaar!
f2()                                            //vaaar!
t.a = "nyaaa!"                                  //теперь попробуем так
f1()                                            //nyaaa!
f2()                                            //nyaaa!
delete t                                        //и вот так
f1()                                            //nyaaa!
f2()                                            //упс, сломалось, t больше не существует и f2 теперь ищет переменную a в глобальном пространстве имен
```
  
В `Squirrel`'е для таблицы можно указать родителя, в котором будут искаться слоты, если их нету в самой таблице. Такой родитель будет называется делегатом. За счет этого таблицы становятся похожи на классы. Отличия состоят только в том, что таблицы нельзя инстанциировать, в них нельзя не будут работать метаметоды (но в таблицах-делегатах будут) и для них можно сменить делегата-родителя в любой момент. Еще я сильно пытался сделать что-то похожее на множественное наследование, которого в языке нету.  

```js
class A { a = 1 }                             //классический способ определения для классов
a <- {a = 1}                                  //и таблиц
 
B <- class { b = 2}                           //синтаксический сахарок
b <- { b = 2 }
 
C <- class extends B { c = 3 }                //наследование
с <- delegate b : { c = 3 }                   //и делегирование
 
d <- delegate a : delegate b :
  delegate c : {d = 4}                        //интерпретатор пропускает и такое, но настоящим делегатом будет только первый из списка, это видимо ошибка парсера
E <- class extends class {e1 = 10}  {e2 = 11} //а вот подставить определение класса в том месте, где требуется его имя можно 
e <- delegate delegate delegate 
     {z = 3 } : a  : {x = 1}  : {}            //и определить таблицу тоже - цепочки делегатов выглядят прикольно =(^_^)=
```
   
Можно, собственно вообще вместо наследования просто перекидывать в класс нужные слоты от какого-нибудь объекта, в том числе и задаваемого на лету, "[подмешивая](http://ru.wikipedia.org/wiki/Mixin)" его свойства:  
  
```js
function mixin (clas, mix)
{
  foreach (slot,val in mix)
    clas[slot] <- val
}
 
class A {}
mixin (A , {f = function() print ("hello") } )
A.f();   //print "hello"
```
  
Если еще отслеживать список имен добавленных методов, можно даже "отмешать" свойства обратно, единственное ограничение - делать это можно только до первого создания экземпляра класса, зато таблицы можно модифицировать как душе угодно.