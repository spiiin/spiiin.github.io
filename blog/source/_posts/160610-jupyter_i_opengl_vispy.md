---
title: Jupyter + OpenGL = VisPy
tags:
  - 3d
  - python
  - opengl
abbrlink: 3238068701
date: 2016-06-10 15:46:00
---

Четверо программистов собрались, чтобы сделать библиотеку для визуализации BigData в браузере VisPy. По описанию, это должно быть удобное средство высокоуровнего описания сцены, но при беглом изучении мне показалось, что на текущей стадии разработки их обёртка над OpenGL под названием [gloo](http://vispy.org/gloo.html) не такая уж high-level – для её использования нужно иметь те же знания, что и при использовании OpenGL, понимать, что такое буферы данных, вершинные аттрибуты и переменные, а также фигачить шейдеры вовсю. За счёт этого её можно использовать в качестве обучения OpenGL и экспериментов с шейдерами. [Пример](https://github.com/vispy/vispy/blob/master/examples/ipynb/webgl_example_2.ipynb) ноутбука с использованием VisPy, вывод осуществляется [с помощью WebGL](https://github.com/vispy/vispy/wiki/Visualization-project). Библиотека может использовать в качестве бекэнда не только WebGL, но и PyQT, PiSide, Pyglet и другие, но мне показался интересным вывод графики прямо страницу в ноутбуке Jupyter. Получается примерно такая анимированная картинка: [![](http://ic.pics.livejournal.com/spiiin/20318251/45653/45653_300.png)](http://ic.pics.livejournal.com/spiiin/20318251/45653/45653_original.png)