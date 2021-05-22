---
title: Cad Editor 3.0 (Universal NES and SEGA level editor).
tags:
  - nes
  - sega
  - gba
  - hack
abbrlink: 2166282811
date: 2014-06-06 16:29:00
---
[Семестровый пост про CadEditor.](http://spiiin.livejournal.com/73681.html)
[![cad_editor_v30](http://ic.pics.livejournal.com/spiiin/20318251/38067/38067_300.png "cad_editor_v30")](http://ic.pics.livejournal.com/spiiin/20318251/38067/38067_original.png)

Добавил в редактор конфиги игр на Sega/GBA (*Contra Hards Corps, Lost Vikings, Tiny Toon Buster's Hidden Adventure, Quack Shot, Zombies Ate My Neighbors, Final Fantasy Tactics Advance*)

общие принципы построения уровней из тайлов такие же, разве что часто требуются внешние компрессор-декомпрессор из внутриигровых архивов.

Разобрал с десяток систем хранения списков игровых объектов (*Tale Spin, Little Mermaid, Ninja Cat, Tiny Toon Adventures, Chip & Dale 2, Flintstones 1 & 2, Tom & Jerry, New Ghostbusters 2, Jungle Book, Zombies Ate My Neignborns*), вдобавок к тем, что уже были разобраны. В них тоже много общих идей, прослеживаются два типа устройства систем – с равными по длине списками и с переменными по длине (часто со встроенной системой команд). У объекта имеется тип (иногда может быть несколько разных списков с разными форматами), координаты на экране (либо одномерные, либо двумерные) и, часто, несколько байт дополнительных данных (подтип, кол-во жизней, радиус появления и т.п.).

Из улучшений редактора:
- Нормальный интерфейс главного окна.
- Возможность работать с двумя реальными слоями и произвольным количеством виртуальных.
- Подредактор виртуальных макроблоков (структур), для составления и расставления по карте блоков произвольного размеры и формы.

[Cписок поддерживаемых игр](https://github.com/spiiin/CadEditor/blob/master/CadEditor/cad_editor_supported_games.txt)
(8 игр полностью и ещё 33 в режиме редактора картинками).

[Ссылка на редактор](https://github.com/spiiin/CadEditor/blob/master/Release/cad_editor_v30.zip?raw=true)