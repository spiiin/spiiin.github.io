---
title: "daScript: C++ auto-bindings, assimp"
abbrlink: 500729544
date: 2022-06-12 15:41:20
tags:
 - 3d
 - dascript
---

Продолжение предыдущего поста с генерацией модулей daScript к С++-библиотекам с помощью автоматического генератора `dasBind`.
{% post_link 220530-dascript-bindings 'daScript: C++ auto-bindings, msgpack' %}

На этот раз чуть более сложный случай с библиотекой [assimp](https://github.com/assimp/assimp), которая позволяет загружать 3d-модели в различных форматах. Для начала -- собираем библиотеку из исходников. Я бы рекомендовал версию 4.1.0, как стабильную, в более новых сломаны некоторые настройки постпроцессинга загруженных мешей.

Привязки assimp к другим языкам в основном репозитории малость заброшены, так что попутно починим и их.

##Python

Самый простой случай -- достаточно поправить синтаксические отличия между Python 2 и 3. 

##DotNet, open3mod

Живёт [тут](https://github.com/acgessler/open3mod), необходимо:
- Собрать библиотеку assimp в DLL, переименовать в Assimp32.dll или Assimp64.dll.
- Собрать библиотеку AssimNet.dll с классами обёртками.
- Собрать проект `AssimpNet.Interop.Generator`, который нужен, чтобы [пропатчить](https://github.com/acgessler/open3mod/blob/master/libs/assimp-net/AssimpNet.Interop.Generator/Program.cs#L34) IL-код из AssimpNet размерами типов, полученных из PDB файла. Для этой техники используется библиотека [Mono.Cecil](https://www.mono-project.com/docs/tools+libraries/libraries/Mono.Cecil/).
- Пропатчить библиотеку (данный шаг прописан в PostBuild-степ в решении, но лучше убедиться, что он корректно отработал)
- Собрать и запустить open3Mod - просмотрщик, в котором можно проверить работоспособность библиотеки.

##daScript

Автоматический генератор привязок `dasBind` не работает с C++ template-кодом, но все заголовочные файлы `assimp` поддерживают также c-интерфейс. Однако без некоторой "доработки напильником" воспользоваться этим интерфейсом не удастся, так как, несмотря на то, что генератору привязок можно указать, чтобы он парсил заголовочные файлы как c-код, возникают ошибки двойного определения типов при использования этих же хидеров в C++ коде самого проекта, который будет использовать эти привязки. Причины такого поведения -- попытка различать, какой из интерфейсов использовать с помощью макроса ` __cplusplus`, который всегда определён в C++ коде (`exrern "C"` его не отключает).

Однако можно пойти на хитрость, и просто заменить во всех исходниках макрос ` __cplusplus` на какой-нибудь кастомный, который не будет определен в коде, чтобы как `dasBind`, так и использующий сгенерированный C++-модуль `dasAssimp`, "увидели" именно сишный интерфейс к библиотеке.

```python
#replace_cplusplus_to_custom.py
#Script for replace __cplusplus text to some other build directive (__CUSTOM_CPP_DEFINE)

import os

HEADERS_PATH = "."

for fname in os.listdir(HEADERS_PATH):
	if os.path.isfile(os.path.join(HEADERS_PATH, fname)) and os.path.splitext(fname)[1] != ".py":
		print("Proccessing", fname)
		with open(fname, "rt") as f:
			lines = f.readlines()
		newlines = []
		for line in lines:
			newlines.append(line.replace("__cplusplus", "__CUSTOM_CPP_DEFINE"))
		with open(fname, "wt") as f:
			f.writelines(newlines)
```

Ну и дальше, аналогично инструкции в предыдущем посте:

```python
class AssimpGen : CppGenBind
    override func_to_stdout = false
    unique_functions : table<string; bool>

    def AssimpGen
        bind_root = "{get_das_root()}/modules/dasAssimp/src"
        bind_module = "assimp"
        bind_das_module = "assimp"
        let pfn = "assimp/include_all_import.h"
        //# тут пользуемся сгенерированными сишными заголовочными файлами
        let pfp = "{get_das_root()}/modules/dasAssimp/assimp/include_c/" 

        let args <- [{string
            "-xc++-header";
            "-std=c++1z";
            "-I{get_full_file_name(pfp)}";
            "-DSWIG"
        }]
```

и дописываем функцию преобразования `dasString` в `std::string`, чтобы генератор привязок мог понять, как с ней работать


```c++
const char* das_aiString_to_string(aiString* string) {
	return string->data;
}

void Module_assimp::initMain() {
	addExtern<DAS_BIND_FUN(das_aiString_to_string)>(*this, lib, "assimp_str",
		SideEffects::worstDefault, "das_aiString_to_string");
}
```

После генерации модуля можно попробовать им воспользоваться (предварительно не забыть прилинковать к проекту lib файлы от библиотеки `assimp` и сделать доступным путь к собранный dll, если ассимп был собран как динамическая библиотека):

```python
require assimp
require strings
require daslib/defer

def printNodesHierarchy(depth:int; var node:aiNode?&)
    unsafe
        print("{repeat("-",depth)}{assimp_str(addr(node.mName))}\n")
        for i in range(0, int(node.mNumChildren))
            printNodesHierarchy(depth+1, node.mChildren[i])

[export]
def main
    unsafe
        let path = "character.dae"
        var scene = aiImportFile(path, 8u)
        defer <|
            scene |> aiReleaseImport
        
        var mesh = scene.mMeshes
        print("Meshes: {int(scene.mNumMeshes)}\n")
        print("Vertices:{int(mesh[0].mNumVertices)}\n")
        print("Faces:{int(mesh[0].mNumFaces)}\n")

        var rootNode = scene.mRootNode
        print("Node hierarchy:\n")
        printNodesHierarchy(1, rootNode)
```

Данный код загружает модель из файла `character.dae`, и печатает иерархию костей скелета в этой модели:
```
Meshes: 1
Vertices:14487
Faces:4829
Node hierarchy:
-character.dae
--root
---M_spine_1_joint
----M_spine_2_joint
-----M_spine_3_joint
------M_spine_4_joint
------M_spine_5_joint
-------L_shoulder_joint
--------L_arm_1_joint
---------L_arm_2_joint
...
-------R_leg_4_joint
--------R_leg_5_joint
------R_leg_2_twist_1_joint
-------R_leg_2_twist_2_joint
-----R_leg_1_twist_1_joint
------R_leg_1_twist_2_joint
--body_geo
```

[Сырой код модуля](https://github.com/spiiin/dasClangBind_modules/tree/main/dasAssimp), когда-нибудь надо будет причесать




 
