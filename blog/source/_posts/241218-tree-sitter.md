---
title: Tree sitter
abbrlink: 433986896
date: 2024-12-18 01:12:09
tags: link
---

[Tree-sitter](https://tree-sitter.github.io/tree-sitter/) -- библиотека на rust, в которой можно с помощью javascript описать грамматику любого языка. Она скомпилится в парсер на C и привязки к ещё пачке языков.

Кроме большого количества [парсеров](https://github.com/tree-sitter/tree-sitter/wiki/List-of-parsers) для разных языков имеет lisp-like язык запросов к AST-дереву.

С ним можно [поиграться](https://tree-sitter.github.io/tree-sitter/playground) онлайн -- подсвечивает в реальном времени блоки кода, соотвествующие описанным ast-запросам.

Может использоваться для очень умной подсветки (включая файлы на нескольких языках, вроде встроенных языков), умного грепания кода (для [рефактора](https://ast-grep.github.io/playground.html), составления Table of Contents кода на github, [структурного редактирования](https://youtu.be/Jes3bD6P0To?si=_B6gsDe71TqMhBTC&t=980) или [копилотирования](https://github.com/Aider-AI/grep-ast) с ИИ).

Вообще выглядит как будто им можно попробовать генерировать байндинги с сишного кода вместо clang-а (или с других форматов описания)