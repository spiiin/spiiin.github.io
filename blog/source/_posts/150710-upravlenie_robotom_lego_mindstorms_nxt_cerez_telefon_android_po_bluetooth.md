---
title: Управление роботом Lego Mindstorms NXT через телефон Android по Bluetooth
tags:
  - lego
  - hardware
abbrlink: 1516237476
date: 2015-07-10 01:31:00
---
После посещения [Geek Picnic](http://geek-picnic.me/geek-picnic-2015-spb) решился собрать из лего что-нибудь полезное и управлять этим с телефона

Среди [существующих программ](https://play.google.com/store/search?q=mindstorms&c=apps) для Lego Mindstorms большинство умеют лишь управлять моторами. Не нашлось таких, которые умеют читать состояние сенсоров, менять схему управления роботом на свою (например, управлять через USB-джойстик) или превратить телефон в центр управления роботами (запускать и удалять загруженные в них программы).

Поэтому решил разобраться, как написать свою (в итоге, пока у меня тоже только управление моторами и запуск программ по имени, зато своё ^\_^).

Для установки соединения можно использовать шаблон [отсюда](http://stackoverflow.com/questions/4969053/bluetooth-connection-between-android-and-lego-mindstorm-nxt).

После установки Bluetooth-соединения NXT-кирпичу можно начинать слать команды (они описаны в [доке LEGO MINDSTORMS NXT Direct commands](http://joanna.iwr.uni-heidelberg.de/projects/NXT_DAME/data/nxt_direct_command.pdf), но весьма поверхностно, подробнее про управление моторами есть [здесь](http://www.robotappstore.com/Knowledge-Base/-How-to-Control-Lego-NXT-Motors/81.html), для понимания параметров всех команд лучше изучить ещё мануал по программированию роботов на каком-нибудь языке из списка [отсюда](http://spiiin.livejournal.com/78887.html)).

Отправка команд выглядит примерно так:

```csharp
//слегка модифицированный класс BTConnect из примера по ссылке
BTConnect btConnect = new BTConnect();
//присоединяемся к NXT-блоку
btConnect.connectToNXTs();
//Запуск моторов, подключенных к портам B и C в полную силу без дополнительных опций
byte[]command1 = new byte[] { 0x0C, 0x00, 0x00, 0x04, (byte)0x01, (byte)100, 0x01, 0x00, 0x00, 0x20, 0x00, 0x00, 0x00, 0x00 };
byte[]command2 = new byte[] { 0x0C, 0x00, 0x00, 0x04, (byte)0x02, (byte)100, 0x01, 0x00, 0x00, 0x20, 0x00, 0x00, 0x00, 0x00 };
btConnect.writeMessage(command1);
btConnect.writeMessage(command2);
/* 
... Робот продолжает условно "ехать вперёд" (зависит от того, как он собран, конечно).
*/
//Остановка всех моторов
byte[]command3 = new byte[] { 0x0C, 0x00, 0x00, 0x04, (byte)0xFF, 0, 0x01, 0x00, 0x00, 0x20, 0x00, 0x00, 0x00, 0x00 };
btConnect.writeMessage(command3);
```

Дальше сел собирать такого робота (инструкция по сборке есть в [книжке автора](http://www.amazon.com/gp/product/1593272111/ref=as_li_ss_tl?ie=UTF8&tag=valkmindstorm-20&linkCode=as2&camp=1789&creative=390957&creativeASIN=1593272111)):  
https://www.youtube.com/watch?v=c2MUd5O6aWc

... и завис за этим на всю ночь. После сборки оказалось, что `The Snatcher` (хочется назвать его за манеру действий по-русски в честь перевода фильма Snatch от Гоблина) хватает своей рукой выше положенного уровня и робота пришлось ещё час отлаживать, в ходе чего выяснилось, что я просто неправильно прикрепил руку к вездеходу.

В демонстрационной программе от автора он находит и поднимает ближайший предмет и произносит его цвет.

На практике, часто пытается ухватиться за ногу или кровать, перевернуть и разбросать тестовые предметы по комнате.

Чётко умеет воровать крышки с флаконов. Поэтому тестовая программа запускается редко, вместо этого при некоторой сноровке с помощью дистанционного управления можно притащить к себе подходящие по форме клешни предметы весом грамм в 150.

Приведённый в книге для примера циллиндр из картона по форме удивительно напоминает стопку. Проверил на практике — наполненную жидкостью стопку робот почти гарантированно не проливает и доносит.

Так что лучше всего этот робот пригоден для того, чтобы приносить алкоголь. Чувствую себя [изобретателем Гэллегером](http://www.lib.ru/KUTTNER/gelleger.txt), построившим себе робота для открывания банок с пивом.