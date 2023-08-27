---
title: daScript tiny renderer port
abbrlink: 3563373441
date: 2022-12-25 16:02:28
tags:
  - dascript
  - opengl
  - 3d
---

Портировал первые несколько примеров [Tiny renderer or how OpenGL works: software rendering in 500 lines of code](https://github.com/ssloy/tinyrenderer/wiki) софт-рендера с C++ на daScript. Механически и неоптимально, но близко к коду оригинального туториала, для желающих потренироваться в базовых алгоритмах растеризации на daScript.
https://github.com/spiiin/dascript_soft_render

Растеризация отрезков, wireframe
![](221225-dascript-soft-render/1.png)
Растеризация треугольников line sweeping, flat shading, отсечение задних граней
![](221225-dascript-soft-render/2.png)
Z-буфер, наложение текстурных координат
![](221225-dascript-soft-render/3.png)
Перспективная проекция
![](221225-dascript-soft-render/4.png)
Камера, Gouraud shading
![](221225-dascript-soft-render/5.png)
Коррекция перспективных искажений текстурных координат, растеризация треугольника проверкой барицентрических координат точки, пиксельный и вершинный шейдеры
![](221225-dascript-soft-render/6.png)

В оригинале есть ещё детальный разбор матриц (model, view, projection), наложение карты нормалей, тени и ambient occlusion. Но, мне кажется где-то с этого уровня можно продолжать разбираться с графикой уже с помощью графического API.

