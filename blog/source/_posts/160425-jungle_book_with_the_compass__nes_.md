---
title: 'Jungle Book With The Compass [NES]'
tags:
  - nes
  - hack
abbrlink: 1474905038
date: 2016-04-25 14:44:00
---
После просмотра фильма Jungle Book решил вернуться к ромхак-анализу игр этой серии.

Существует несколько различных портов Jungle Book для разных консолей, выпущенных одной и той же командой разработчиков.

Версии для PC и Sega практически идентичны, Snes версия обладает схожей графикой, но полностью другими уровнями, а NES и GameBoy – очень похожими по структуре уровнями, но отличаются по используемому физическому движку и графике.

Для примера карты уровней для NES и SMD версии (можно сравнить позиции деревьев).
[![](http://ic.pics.livejournal.com/spiiin/20318251/43301/43301_600.png)](http://ic.pics.livejournal.com/spiiin/20318251/43301/43301_original.png)

Однако при всей схожести сеговская версия проходится легко и приятно, а NES-версия – хардкорный ад, как будто разработчики намерянно решили усложнить игру в разы.

Смотрите сами:

Во-первых, физический движок на NES написан так, чтобы усложнить жизнь игроку – медленно летящие снаряды, вроде осколков ореха наносят урон не один раз, а 4-5, что отбирает почти всё здоровье, попасть на врага сверху очень сложно, нужно чётко знать область повреждения, чтобы не промахнуться по ней (в сега версии можно хоть ударить врага снизу, игра всё равно вытолкнет Маугли наверх и нанесёт урон врагу), вдобавок иногда Маугли просто промахивается мимо лианы, пролетая сквозь неё.

Дальше – на наклонной поверхности или после бега в NES версии Маугли начинает не останавливается сразу, а пробуксовывает вперёд, что часто приводит к незапланированным падениям. Ещё он умеет прыгать двумя способами, с места и с разбега, в обеих версиях, но в сеге отличия заключаются только в анимации прыжка, на NES же уровни построенны так, что иногда требуется прыгнуть только конкретным типом прыжка, иначе не хватит длины или высоты полёта.

Особенно это ощущается в уровне Falling Ruins, целиком состоящем из падающих под весом Маугли платформ. Во-вторых, в версии на SMD кристалы, необходимые для окончания уровня, чаще всего лежат на видном месте и для прохождения нужно найти не все из них, а только (8/10/12 из 15 в зависимости от выбранной сложности), причём можно найти компас, который показывает, где лежит ближайший кристал.

В NES, соответственно, некоторые кристалы спрятаны в секретных нычках, которые ещё нужно найти, иногда даже совершив "прыжок веры" вслепую, причём какую бы сложность вы ни выбрали, придётся собирать все кристалы.

Часто приходится отыскивать по всему уровню последний лучше всего спрятанный кристал в условиях, когда кончается время (для справедливости отмечу, что в GameBoy версии всё ещё сложнее, в ней кристалы часто спрятаны внутри врагов, и для их отыскания приходится устраивать уничтожение всех животных, встреченных на пути в поисках драгоценностей).

В-третьих, Балу. В мультфильме есть эпизод, в котором он обучает Маугли жизни в джунглях и поёт песню/

Уровень The River в игре про этот момент. В Sega версии Маугли доходит до Балу со стороны реки, рядом три камня, Балу бросает фрукты, их надо ловить, если упасть в речку, бонус закончится, и начнётся следующий уровень. В NES же Балу просто пытается утопить Маугли, и его нужно победить. Друг называется... Чтобы хоть немного облегчить NES-версию, я написал Lua-скрипт для эмулятора FCEUX, который добавляет в игру компас, который, как и в Sega-версии показывает направление к ближайшему ещё не собранному кристалу.

<https://gist.github.com/spiiin/14acca27ded1989f86622eaa3ad1b515>

Так что можно перепройти игру, не путаясь в лабиринтах из лиан: 
https://www.youtube.com/watch?v=_SVjgF7rcbs