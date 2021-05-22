---
title: windows command multiline
tags: codespell
abbrlink: 26294
date: 2010-11-01 11:03:00
---

В коммандных файлах windows можно делать списки из нескольких строк с помощью символа "^": 

```
set m=^
1 ^
2 ^
3
for %%f in (%m%) do ^
echo %%f
```