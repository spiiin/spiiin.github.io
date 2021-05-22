---
title: 'Уровни Jungle Book [NES]. Часть 2'
tags:
  - nes
  - hack
abbrlink: 21742
date: 2011-10-20 01:14:00
---

**Шаг 0x0A.** 

Остается последний шаг, чтобы связать результаты анализа снизу (от экрана к набору) и сверху (от набора к экрану) - понять, как адреса из предэкрана + смещение попадают в экран . Так как для этого копирования используется адресация через нулевую страницу, точку остановки поставить нельзя, поэтому можно только поставить ее на запись в экран и просто искать в окрестностях чтение из предэкрана .

```asm
ROM:840F JSR sub_856B ; Копирование 4х адресов в зону предэкран-вторичные индексы
ROM:840F ; х циклически проходит диапазон (00-03)
ROM:8412 LDA byte_A5
ROM:8414 EOR #3
ROM:8416 TAX
ROM:8417 LSR A
ROM:8418 STA byte_A9
ROM:841A
ROM:841A LDY #0
ROM:841C LDA ($A3),Y ; индекс относительно базового адреса из предэкрана
ROM:841E TAY
ROM:841F PHA
ROM:8420 BMI loc_8427
ROM:8422 LDA ($83),Y ; отсюда мы считываем индекс начала цепочки
ROM:8424 JMP loc_8429
ROM:8427 ; ---------------------------------------------------------------------------
ROM:8427
ROM:8427 LDA ($85),Y
ROM:8429
ROM:8429 TAY
ROM:842A BPL loc_843B
ROM:842C LDA ($95),Y ; используем считанный индекс, чтобы взять тайл из набора
ROM:842E STA $40B,X
ROM:8431 LDA ($99),Y
ROM:8433 STA $40C,X
ROM:8436 LDA ($71),Y
ROM:8438 JMP loc_8447
ROM:843B ; ---------------------------------------------------------------------------
ROM:843B
ROM:843B LDA ($93),Y
ROM:843D STA $40B,X
ROM:8440 LDA ($97),Y
ROM:8442 STA $40C,X
ROM:8445 LDA ($6F),Y
ROM:8447
ROM:8447 AND #3
ROM:8449 TAY
ROM:844A LDA $8B16,Y
ROM:844D LDY byte_A9
ROM:844F STA $455,Y
ROM:8452 INC byte_A9
ROM:8454 PLA
ROM:8455 TAY
ROM:8456 BMI loc_845D
ROM:8458 LDA ($87),Y
ROM:845A JMP loc_845F
ROM:845D ; ---------------------------------------------------------------------------
ROM:845D
ROM:845D LDA ($89),Y
ROM:845F
ROM:845F TAY
ROM:8460 BPL loc_8471 ; что-то типа записи в столбик, из которого будет перенос в видеопамять
ROM:8462 LDA ($95),Y
ROM:8464 STA $40D,X
ROM:8467 LDA ($99),Y
ROM:8469 STA $40E,X
ROM:846C LDA ($71),Y
ROM:846E JMP loc_847D
ROM:8471 ; ---------------------------------------------------------------------------
ROM:8471
ROM:8471 LDA ($93),Y ; что-то типа записи в столбик, из которого будет перенос в видеопамять
ROM:8473 STA $40D,X
ROM:8476 LDA ($97),Y
ROM:8478 STA $40E,X
ROM:847B LDA ($6F),Y
ROM:847D
ROM:847D AND #3
ROM:847F TAY
ROM:8480 LDA $8B16,Y
ROM:8483 LDY byte_A9
ROM:8485 STA $455,Y
ROM:8488 INC byte_A9
ROM:848A INX
ROM:848B INX
ROM:848C INX
ROM:848D INX
ROM:848E DEC byte_3F0 ; кол-во повторов считывания
ROM:8491 BMI loc_84BE ; выход из копирования столбца
ROM:8493 LDA xcoord ; x-координата столбца
ROM:8496 INC xcoord
ROM:8499 CMP #2
ROM:849B BCS loc_84A1
ROM:849D LDA #0
ROM:849F BEQ loc_84B0
ROM:84A1
ROM:84A1 BIT byte_12
ROM:84A3 BPL loc_84AD
ROM:84A5 LDA xcoord
ROM:84A8 CMP byte_36F
ROM:84AB BCS loc_84C1
ROM:84AD
ROM:84AD LDA xshift_cycle60
ROM:84B0
ROM:84B0 CLC
ROM:84B1 ADC byte_A3
ROM:84B3 STA byte_A3
ROM:84B5 LDA byte_A4
ROM:84B7 ADC #0
ROM:84B9 STA byte_A4
ROM:84BB JMP loc_841A ; повтор загрузки
```

Этот кусок кода и есть функция- комбинатор . Она показывает связь между предэкраном и экраном . Новые важные переменные здесь `$366 (x_shift_cycle)` - насколько сдвигаться за один шаг цикла считывания, похоже на разницу между строками, то есть ширину всего уровня; 
`xcoord` - число повторов выборки, постоянно равно 5, от есть считывается по 4 тайла 5 раз = 20 раз - один столбец на экране. `$A2-$A3` - пара ячеек, в которых написан изначальный индекс, от которого проводится измерение. 

Разбираться откуда он берется пока не обязательно, можно посмотреть первый попавшийся и начать написание функции-комбинатора, которая будет делать то же самое, что и приведенный выше кусок кода на ассемблере.
 
**Шаг 0x0B.**
 
Реализация комбинатора на питоне: 
```python
 def get4Lines(begin,end, levelSet, a3a4, step, vertCount):
  cycleBegin = begin
  cycleEnd   = end
  a3a4ind = begin/4
  line4 = []
  for x in xrange(cycleBegin,cycleEnd):
    if x%4==0:
      a3a4ind += 1
    b83,b85,b87,b89 = getLevelSetForCycle(levelSet, b8x_inds,(x+2)%4)
    b93,b95,b97,b99 = getLevelSetForCycle(levelSet, b9x_inds,(x+2)%4)
    line4.extend(makeLine(a3a4, a3a4ind, b83,b85,b87,b89, b93,b95,b97,b99, step, vertCount))
  return line4
 
 
def makeLine(a3a4, a3a4BaseInd, b83,b85,b87,b89, b93,b95,b97,b99, step, vertCount):
  a3a4ind = a3a4BaseInd
  lines = []
  for globalRepeat in xrange(vertCount): ##5(screen size)
    predInd = a3a4[a3a4ind]
    ind2a,ind2b = -1,-1
    if predInd<128:
      ind2a = b83[predInd]
      ind2b = b87[predInd]
    else:
      ind2a = b85[predInd]
      ind2b = b89[predInd]
 
    res = [-1]*4
    if ind2a<128:
      res[0],res[1] = b93[ind2a], b97[ind2a]
    else:
      res[0],res[1] = b95[ind2a], b99[ind2a]
    if ind2b<128:
      res[2],res[3] = b93[ind2b], b97[ind2b]
    else:
      res[2],res[3] = b95[ind2b], b99[ind2b]
    lines.extend(res)
    a3a4ind+=step
  return lines
 
b8x_inds = [[5,5,4,4], [7,7,6,6], [9,9,8,8], [11,11,10,10]]
b9x_inds = [[12,13,12,13], [14,15,14,15], [16,17,16,17], [18,19,18,19]]
def getLevelSetForCycle(levelSet,indsConst,loop):
  inds = map (lambda v: v[loop], indsConst)
  return map (lambda i: levelSet[i], inds)
```

Набор данных можно выхватить прямо из дампа памяти: 

```python
def prepareBinary(binaryDump, addrBegin, addrLen, outName):
f = open(binaryDump,"rb")
byt = f.read()
f.close()
bb = byt[addrBegin:addrBegin+addrLen]
f =open(outName,"wb")
f.write(bb)
f.close()
```

Дальше можно проверить отрисовку и убедиться, нарисовалась полоса уровня высотой в 20 клеток.
 
**Шаг 0x0C.**
 
Экспериментируя с параметрами `A2A3` и значением `vertCount` можно получать разные срезы уровня, например, такой:
[![](http://pics.livejournal.com/spiiin/pic/0001xwst)](http://pics.livejournal.com/spiiin/pic/0001xwst/)

По нему можно прикинуть, откуда начинается мусор, и как конец уровня связан с началом по высоте и вычислить правильное значение `A2A3` соответствуюшее началу уровня (и в итоге заметить, что оно на 1 меньше, чем адрес в `$47-$48` (это первое значение из набора ), то есть равно первому значению и набора - 1).

Также можно обратить внимание, что рядом с шириной уровня ($366) в ячейке $367 лежит и его ширина).

Тогда можно вывести полную схему работы комбинатора:
[![](http://pics.livejournal.com/spiiin/pic/0001y71x/s640x480)](http://pics.livejournal.com/spiiin/pic/0001y71x/)

и написать универсальную функцию рисования:

```python
def makeJob (binaryName, spritesName, addr, baseAddrSet, w,h, levelNo):
  tempName1 = binaryName+".a2a3."+str(levelNo)+".bin"
 
  imNameTable = Image.open(spritesName)
  nameSize = imNameTable.size
  nameTable = [imNameTable.crop((x,y,x+8,y+8)) for y,x in itertools.product(xrange(0,nameSize[1],8),xrange(0,nameSize[0],8))]
  sprites = map (lambda im: PpuSprite(im),nameTable) 
 
  prepareBinary(binaryName, addr, 0x2000, tempName1)
  a3a4 = parseBinData256(tempName1)
 
  prepareBinaries(binaryName, baseAddrSet)
  levelSet = map(loadLevelSetElement, baseAddrSet)
  ll = get4Lines(0,w*4, levelSet, a3a4, w,h)
  drawLevelFromData(ll, sprites,(w*4,h*4),True).show()
```

(уровень определяется - дампом памяти, набором адресов, размерами (ширина и высота) и картой тайлов).

Этой функцией можно нарисовать любой уровень:
Уровень 1. 
[![1](http://pics.livejournal.com/spiiin/pic/0001zdhq/s640x480)](http://pics.livejournal.com/spiiin/pic/0001zdhq/)
Уровень 2.
[![2](http://pics.livejournal.com/spiiin/pic/00020r8e/s640x480)](http://pics.livejournal.com/spiiin/pic/00020r8e/)
Уровень 3.
[![3](http://pics.livejournal.com/spiiin/pic/0002115d/s640x480)](http://pics.livejournal.com/spiiin/pic/0002115d/)
Уровень 4.
[![4](http://pics.livejournal.com/spiiin/pic/000228yk/s640x480)](http://pics.livejournal.com/spiiin/pic/000228yk/)
Уровень 5.
[![5](http://pics.livejournal.com/spiiin/pic/00023f84/s640x480)](http://pics.livejournal.com/spiiin/pic/00023f84/)
Уровень 6.
[![6](http://pics.livejournal.com/spiiin/pic/00024g9r/s640x480)](http://pics.livejournal.com/spiiin/pic/00024g9r/)
Уровень 7.
[![7](http://pics.livejournal.com/spiiin/pic/00025e0b/s640x480)](http://pics.livejournal.com/spiiin/pic/00025e0b/)
Уровень 8.
[![8](http://pics.livejournal.com/spiiin/pic/00026hc9/s640x480)](http://pics.livejournal.com/spiiin/pic/00026hc9/)
Уровень 9.
[![9](http://pics.livejournal.com/spiiin/pic/000277fy/s640x480)](http://pics.livejournal.com/spiiin/pic/000277fy/)
Уровень 10. [![10](http://pics.livejournal.com/spiiin/pic/00028s1z/s640x480)](http://pics.livejournal.com/spiiin/pic/00028s1z/)
[Код скрипта](http://pastebin.com/e4qedf4X) (использовался больше в интерактивном режиме)

 *//Если что-то долго ломать, то оно сломается.*
 
 **Конец**