---
title: Selenium WebDriver
tags:
  - dev
  - c#
  - python
abbrlink: 61719
date: 2017-02-19 22:36:00
---

Нашёл замечательную библиотеку [Selenium](http://www.seleniumhq.org/projects/webdriver/) по управлению браузерами, как headless (Phantom-JS/HTMLUnit), так и "настоящими" (Firefox/Chrome/IE/Safari и ещё десяток third-party драйверов для браузеров на любой вкус) локально или удалённо. Позволяет "нажимать" на элементы, ожидать результатов асинхронных запросов по условию, выполнять JavaScript в контексте DOM-страницы и вообще почти любые фишки, которые умеет браузер. Когда-то юзал для выполнения простых JavaScript на странице [Greasemonkey](https://addons.mozilla.org/ru/firefox/addon/greasemonkey/), а для парсинга сайтов [mechanize](https://github.com/jjlee/mechanize) (уже мертва, приходится [дописывать нужные фичи самому](http://spiiin.livejournal.com/93137.html)), теперь с этим проектом можно пойти намного дальше и наавтоматизировать всякого на Python или C# (а также Ruby, Java или JavaScript).