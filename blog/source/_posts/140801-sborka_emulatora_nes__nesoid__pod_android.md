---
title: Сборка эмулятора NES (NESOID) под Android
tags:
  - nes
  - hack
  - android
abbrlink: 740210792
date: 2014-08-01 17:09:00
---

В сети валяются несколько версий эмуляторов NES с открытыми исходниками.

В основном это либо едва начатые учебные проекты, либо порты написанного на C универсального эмулятора [FCE](http://www.zophar.net/nes/fce-ultra.html).

Версия под android называется Nesoid, исходники её разбросаны по интернету
<http://sourceforge.net/projects/nesoid>
<https://code.google.com/p/androidnes/source/browse/>
<https://f-droid.org/repository/browse/?fdfilter=nesoid&fdid=com.androidemu.nes>

Полные исходники, с библиотекой [Emudroid-Common](https://github.com/Pretz/Emudroid-Common), (без неё при сборке будет ругаться на нехватку файла *utils/Log.h*) и интерфейсом на Java, есть только на [f-droid](https://f-droid.org/repo/com.androidemu.nes_61_src.tar.gz), там же есть и собранный из них готовый apk, так что для старта лучше выбрать их.

Библиотеки на C собирается с помощью [Android Native SDK](https://developer.android.com/tools/sdk/ndk/index.html), после установки в папке с Nesoid достаточно набрать *ndk-build*, чтобы собрать нужные для эмулятора библиотека ***libnes***, ***libemu*** и ***libnativehelper***.

Для сборки самого эмулятора необходим [Android SDK](http://developer.android.com/sdk/index.html), с доустановленным через *SDK Manager* ***Android API 10*** (под него по умолчанию собирается эмулятор).

Сами *Build tools* лучше использовать версии > 19.0, потому что на 19.0 компилятор падает с [Buffer overflow exception](http://stackoverflow.com/questions/19727915/android-dex-gives-a-bufferoverflowexception-when-building).

 После установки всех необходимых sdk осталось установить систему сборки [Ant](http://ant.apache.org), и для него указать в файле *(PATH\_TO\_EMULATOR\_SOURCES)/local.properties* пути к sdk и ndk, например: sdk.dir=C:/android-sdk ndk.dir=C:/android-ndk-r9d
 
 Далее можно собрать эмулятор с помощью команды ant debug и установить на подключенное по usb устройство с android: ant installd
 
 После этого при открытии рома эмулятор будет падать из-за [ошибки](https://github.com/Pretz/SNesoid/issues/3) в сигнатуре метода, поэтому в файле ***common\emumedia.cpp*** стоит поправить строчку 116: - env->CallStaticIntMethod(jPeerClass, midSetSurfaceRegion, x, y, w, h); + env->CallStaticVoidMethod(jPeerClass, midSetSurfaceRegion, x, y, w, h); После этого эмулятор будет работать нормально. 
 
 Что можно добавить в эмулятор полезного? Практически любую фичу из реализованных в современной версии [fceux](http://www.fceux.com/web/version.html).
 
 Например, можно вернуть поддерживаемую в FCE опцию автоматической загрузки *ips-патчей* и *проигрывание повторений* игры. Если открыть файл **romname.nes.ips** или **romname.nes.fcm**, то эмулятор использует его, чтобы открыть игру **romname.nes** и загрузить данный файл - функция *FCEUI\_LoadGamе*.
 
 Всё, что нужно для активации данной фишки -добавить в GUI эмулятора отображение файлов нужных типов.
 
 Они описаны в файле ***(EMU\_PATH)/res/values/arrays.xml***: <string-array name="file\_chooser\_filters"> <item>.nes</item> <item>.fds</item> <item>.zip</item> <item>.ips</item> <!-- ips patches --> <item>.fcm</item> <!-- movies --> </string-array> 6. Можно также начать возвращение скриптовых возможностей.
 
 Встроить *lua* быстро не выйдет, но можно добавить свой обработчик в главный цикл эмуляции процессора **X6502**.
 
 Для этого сначала отредактировать файл ***(EMU\_PATH)/neslib/Android.mk***: #LOCAL\_CFLAGS += -DASM\_6502 #убрать директиву, которая включает код реализации главного цикла на ассемблере.
 LOCAL\_SRC\_FILES +=x6502.c #добавить код реализации главного цикла процессора на C.
 Дальше можно просто добавить в функцию X6502\_Run\_c вызов своего кода:
 ... CallInjected();
 //вызов функции обработки каждый такт процессора.
 \_PC++; switch(b1) { 
   ...
   
   Затем надо реализовать обработчик для конкретной игры и сделать распознавание конкретных игр по хэшу при открытии. 
   
   Можно для теста найти места переключения уровней в Super Mario Bros. Lua-скрипт для win версии FCEUltra:
   function logLevel()
   local logStr = string.format("Level %01X-%01X\n", memory.readbyte(0x75F)+1, memory.readbyte(0x75C)+1) 
   rint(logStr)
   end
   
   memory.registerexec(0xB8A5, logLevel) -- переключение обычных сцен
   memory.registerexec(0x845A, logLevel) -- конец мира 8.
   
   Если подключить к эмулятору [Google Play Services](http://developer.android.com/google/play-services/games.html) (про это нужна отдельная статья), то можно играть в Марио и получать ачивменты за пройденные уровни ^\_^.
   
   [![Screenshot_2014-07-31-18-43-43](http://ic.pics.livejournal.com/spiiin/20318251/38390/38390_300.png "Screenshot_2014-07-31-18-43-43")](http://ic.pics.livejournal.com/spiiin/20318251/38390/38390_original.png)
   
   Ссылка на приложение в маркете: <https://play.google.com/store/apps/details?id=com.androidemu.nesachiev>