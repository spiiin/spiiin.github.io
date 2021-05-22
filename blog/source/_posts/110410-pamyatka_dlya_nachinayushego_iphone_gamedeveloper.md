---
title: Памятка для начинающего iphone и macosx gamedeveloper'а
tags:
  - objc
  - opengl
abbrlink: 42980
date: 2011-04-10 16:18:00
---

Cижу, изучаю маковских [юных дев](http://bash.org.ru/quote/408098) , курю маны. Небольшая памятка: 1. Компилятор и [binutils](http://www.gnu.org/software/binutils/) 

##Тулзы

**gcc + cc + g++ **- набор компиляторов, gcc вроде вызывает нужный, но иногда удобнее вызвать необходимый, чем подбирать командную строку, перекрывающую его умолчания. 

Важные параметры: 
-x передать параметр линкеру 
-Ox - уровень оптимизации с номером x, x больше -> оптимизации сильнее. Включают в себя сразу наборы из разных опций оптимизации и генерации отладочной информации. 

Стадии:
-E препроцессинг
-S ассемблерный листинг -c только компиляция, не генерировать объектный код
-Dсимвол - передать дефайн препроцессору
-Wтекст - включение предупреждений
-Werror - считать предупреждения ошибками. Для фанатиков чистоты.
-iпуть - искать заголовочные файлы в заданной папке. Может встречаться в командной строке несколько раз.
-arch тип - архитектура, под которой будет выполняться код. Можно задать сразу несколько. 

**ld** - линкер. 

-lлиб - подключить библиотеку с именем либ
-Lпуть - путь к библиотекам
-framework
-weak\_framework - подключить [фреймворк](http://developer.apple.com/library/mac/#documentation/MacOSX/Conceptual/BPFrameworks/Frameworks.html) (являющийся набором заголовочных файлов, ресурсов, библиотек). 

**ar и ranlib** - утилиты для сборки файлов в библиотеку для последующей линковки. В более широком применении - архиватор.

**nm** - просмотр информации о библиотеках и исполнимых файлах.

**strip** - вырезалка имен символов.

**arch и lipo** - позволяют управлять исполнимыми файлами, содержащими несколько архитектур (создавать и запускать разные версии). Мак под рукой поддерживает i386, x64\_86 и ppc.

**sign** - подписать файл сертификатом разработчика.

Еще бы gdc и shark упомянуть, но я ими не пользуюсь.

##Cocoa

 [Cocoa Event-Handling Guide](http://developer.apple.com/library/mac/#documentation/Cocoa/Conceptual/EventOverview/Introduction/Introduction.html#//apple_ref/doc/uid/10000060i-CH1-SW1) 

[View programming guide](http://developer.apple.com/library/mac/#documentation/Cocoa/Conceptual/CocoaViewsGuide/Introduction/Introduction.html) (часть) 

[Opengl programming guide](http://developer.apple.com/library/mac/#documentation/GraphicsImaging/Conceptual/OpenGL-MacProgGuide/opengl_drawing/opengl_drawing.html) 

<http://developer.apple.com/> - доки по NSObject, NSResponder, NSBundle, NSApplication, NSRunLoop, NSWindow, NSView, NSOpenGLView, NSTimer, NSApplicationDelegate, NSViewController 

Как создать приложение без главного nib-файла : <http://lapcatsoftware.com/blog/2007/06/10/working-without-a-nib-part-5-no-3> (правка info.plist + перегрузка NSApplication + подстановка своего класса вместо NSBundle + настройки стилей NSWindow для приема событий мыши и клавиатуры и внешнего вида) 

##Render 

Нативными для GUI являются `Cocoa` или `Carbon`. 

Cocoa лежит во фреймфорке ApplicationKit/UIKit (для macosx / iphone)
В Cocoa для рисования можно использовать Quartz или OpenGL. 

`OpenGL` представлена в виде фреймворка OpenGL, в котором содержатся библиотеки `gl, glu, glut, glx`.

Для использования OpenGL можно выбрать надстройки CGL* и NSOpenGL. Вторая состоит готовых классов-наборов установок для первой, а также частично просто дублирует классы CGL.

A drawable object can be any of the following: a Cocoa view, offscreenmemory, a full-screen graphics device, or a pixel buffer. - Смешивать отрисовку контролов из Cocoa и отрисовку OpenGL надо также аккуратно, как и в любой другой ОС. А лучше вообще не смешивать.

Полезная схема : ![opengl on mac](http://developer.apple.com/library/mac/documentation/graphicsimaging/conceptual/OpenGL-MacProgGuide/art/opengl_architecture.jpg)