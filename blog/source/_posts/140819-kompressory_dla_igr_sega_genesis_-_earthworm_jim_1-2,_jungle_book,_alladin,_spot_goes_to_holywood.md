---
title: >-
  Компрессоры для игр Sega Genesis - Earthworm Jim 1-2, Jungle Book, Alladin,
  Spot Goes To Holywood
tags:
  - sega
  - hack
abbrlink: 1604429615
date: 2014-08-19 19:05:00
---
В продолжение [поста](http://spiiin.livejournal.com/76109.html).

Нашёл редактор уровней для игры Earth Worm Jim - [EWJ2edit](https://www.youtube.com/watch?v=itIvzBWZcY8), со ссылкой на скачивание.

Редактор поставляется в сыром виде, по сути в нём есть только работа с тайловой картой (как в [CadEditor](http://spiiin.livejournal.com/79971.html)'е), для получения этой тайловой карты необходимо "обработать напильником" ром - выдрать из оперативной памяти видеоданные и данные тайловой карты и макроблоков (или извлечь их с помощью архиватора).

**RNC\_ProPack.** Интересно, что в мануале к редактору было описано как извлечь архивы из игры с помощью утилит [RNC\_ProPack](http://aminet.net/package/util/pack/RNC_ProPack), а также упоминалось, что архиватор подходит для ещё нескольких игр (Alladin, Jungle Book).

Решил проверить, в каких играх используется данный тип архивов. В наборе RNC\_ProPack есть код распаковки под платформы SNES, Mips, M68000 (Sega и Amiga), Lynx, IBM PC, GameBoy. Для данного поста я проверял сеговские игры, для них существуют 4 версии исходников - 2 вариации метода, полный и компактный. Сверив их, можно написать небольшой кусочек кода, который присутствует во в разных версиях и скомпилировать его ассемблером [asm68k](http://elektropage.ru/publ/programmy_dlja_romkhakinga/asm_disasm_etc/asm68k_assembler_dlja_m68000/39-1-0-141):
``` 
BUFSIZE EQU 16*8*3 lea -BUFSIZE(sp),sp #захватывает нестандартную константу.
move.l sp,a2 #и несколько байт вокруг неё. 
addq.w #4,a0
```

```
ASM68K.EXE /p путь_к_asm,путь_к_bin
```
После этого можно проверить собранный файл в [онлайн-дизассемблере](http://www.onlinedisassembler.com/odaweb/#view/tab-assembly/offset/00000000) (в поле ***Arch*** выставить *m68k:68000*, в поле ***Endian*** оставить *Default*, в поле с бинарными данными вставить содержимое полученного бинарного файла - его можно скопировать открыв его в любом шестнадцатеричном редакторе).

Дальше можно прогнать поиск бинарного куска кода по всем файлам из набора *GoodGen*. Дополнительно можно отсечь случайно найденные игры, проверив, содержится ли в роме сигнатура архива из букв "**RNC**" и повторно провести поиск больших кусков кода, чтобы разделить игры на используемые внутри них версии компрессора/декомпрессора.

Результаты (игры, в которых используется одна из версии компрессора/декомпрессора RNC\_**ProPack**):

**Версия EarthWorm Jim Method 1, сигнатура 4FEFFE80244F47E800117800181B5344.**
```
asterix and the power of the gods
blockbuster world game championship II
bugs bunny in double trouble
duffy duck in hollywood
disney's alladin
earth worm jim
earth worm jim 2
incredible hulk
judge dredd - the movie
jungle book
mary shelley's frankenstein
mortal kombat
mortal kombat 2
ncaa college football
no escape
pagemaster
primal rage
second samurai
sceleton crew
spirou
spot goes of hollywood
street racer
striker
tinhead
tintin au tibet 2. 
```
**Версия EarthWorm Jim Method 2, сигнатура 4FEFFE80244F5848610000EC47E8000A**.
```
3 ninjas kick back
addams family values
asterix and the great rescue
asterix and the power of the gods
bubba n stix
bugs bunny in double trouble
huricanes
incredible
hulk
disney's alladin
earth worm jim
earth worm jim 2
incredible hulk
jungle book
last action hero
mortal kombat
mortal kombat 2
primal rage
spirou
spot goes of hollywood
terminator 2
judgement day
tintin au tibet 3
```

**Версия Pitfall : The Mayan Adventure, cигнатура 4FEFFE80244F6100016C72000C80524E**
```
pitfall - the mayan adventure
adventures of mighty max
brutal - paws of fury
chaos engine
chuck II - son of chuck
frank tomas big hurt baseball
humans
itchy and scratchy game
kick off 3
marsupilami
rise of the robots
soldiers of fortune 4
```

**Версия Toy Story, сигнатура 4FEFFE80244F6100016C7200B0BC524E**
```
toy story
bram stoker's draсula
family feud
mickey mania timeless adventures of mickey mouse
lemmings 2 - the tribes
puggsy
sonic 3d blast
```

Напоследок, добавил редактор EWJ2Edit и RNC\_ProPack в папку с [сега-компрессорами](https://www.dropbox.com/sh/mn6sanuwtu0gbac/AACBbu3_HlnpyI-3MjeGooxwa).