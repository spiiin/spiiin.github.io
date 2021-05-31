---
title: Battletoads - Nightmare
tags:
  - nes
  - hack
abbrlink: 5060
date: 2009-09-03 23:46:00
---
Чего-то я приболел... И не спится чего-то.
В больную голову лезут больные идеи. 

Вот, например, японцы оказались [обделены](http://community.livejournal.com/ru_oldgames/144383.html) ловушками в Battletoads.

Решил поправить положение.
Взял [WinMerge](http://winmerge.org/) и дизассемблер [6502d](http://www.zophar.net/utilities/nesdev/6502d-disassembler.html), начал сравнивать японскую версию с английской и с русским переводом от [Magic Team](http://magicteam.net/index.htm), чтобы видно было, где отличия в графике, а где - в коде. 

Но почему-то версии отличаются слишком сильно. Пришлось сменить инструменты и взять [ArtMoney](http://www.artmoney.ru/rus.htm) и искать значение, отвечающее за скорость в гонках, тупым отсевом адресов типа "уменьшилось/увеличилось". Зато найденный адрес используется как коэффициент скорости во всех гонках, так что одним махом можно усложнить пол-игры.

Мои экперименты с гонками на 3-м этапе:
{% youtuber video JheDS1MF_DU %}
{% endyoutuber %}

Интересны моменты, когда жаба начинает падать в непрорисовавшийся провал и касается трамплина только в самый последний момент.

Еще в одном эпизоде наш болид должны обгонять какие-то чудики на ракетах и сбрасывать препятствия, но на такой скорости они просто не успевают угнаться за жабой =)

Когда вылечусь и если будет немного свободного времени, попробую еще поискать интересные адреса.