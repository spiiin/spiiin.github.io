---
abbrlink: 16778
title: Шейдеры для NES игр
date: 2018-04-21 14:57:00
tags: [lua, nes]
---

Продолжаю изучать возможности lua-скриптов в эмуляторе Mesen. 

Функции [getScreenBuffer/setScreenBuffer](https://www.mesen.ca/docs/apireference/drawing.html#getscreenbuffer) позволяют каждый кадр (или чаще) модифицировать содержимое экранного буфера. Так можно добавлять простые шейдеры постэффектов (да и сложные тоже). 

[Скрипт](https://github.com/spiiin/CadEditor/blob/master/Stuff/nes_lua/mesen_modifyScreen.lua) с эффектами красного экрана, мерцания, черезстрочного вывода и построчного "двоения экрана". 

Возможны также и более сложные эффекты (размытие движения, дождик, выделение контуров и т.п.), правда, не сильно удобно писать такое на Lua.

{% youtuber video 04KOJmRYwko %}
{% endyoutuber %}