---
title: Хорошие библиотеки
abbrlink: 1152347544
date: 2021-07-04 16:00:08
tags:
 - gamedev
 - dev_method
---

Очень вольный перевод идей старой, но по прежнему актуальной статьи – [Good Middleware](http://gamearchitect.net/2008/09/19/good-middleware/).
(*местами вообще не перевод, а обобщения и замечания от меня, также я иногда правил выводы и цифры от себя, так что если интересуют оригинальные рассуждения автора - читайте оригинал*)
<!-- more -->

Игровые движки используют много [middleware](https://en.wikipedia.org/wiki/Game_engine#Middleware) (библиотек или решений) – для реализации физики, рендеринга растительности, аудио, лицевой анимации, сетевого взаимодействия и различных других систем.

Во время написания движка (часто параллельно с игрой) не всегда проводится анализ используемых библиотек, но рано или поздно наступает период очистки и анализа используемых middleware-решений, чтобы определиться, какие из них использовать дальше, а от каких лучше отказаться.

Middleware-решения имеют два главных преимущества, но за них придётся заплатить:

**`- Middleware позволяет не писать собственный код, а купить его`**

Затраты на создание библиотеки фиксированы, а продавать её можно снова и снова. Таким образом команды, создающие middleware-решения могут получать доход с большого количества клиентов, и лучше специализироваться на задаче, которую решает их библиотека, чем команды, которые работают на конкретными играми. Пока вы во время разработки игры тратите время на реализацию своего решения, на рынке может появиться middleware-решение для реализации той же задачи, которое со временем будет улучшаться, в то время как вы не сможете тратить время на улучшение своего решения.

Плата же за использование чужого решения - оно никогда в точности не будет соотвествовать вашей задаче. Из этого следует, что часть чужого кода будет для вас бесполезна, так как не касается решения ваших задач. Также библиотеки пишутся для поддержки наиболее распространённых случаев. Если ваши требования отличаются от стандартных - вам лучше реализовать решение самостоятельно.
(*Иногда это будет означать не просто дописать функционал, а полностью отказаться от библиотеки*)

**`- Middleware предлагает определённую структуру кода`**

Библиотеки устанавливают определённые границы между проблемами, о которых должны беспокоиться вы, и проблемами, которые решает библиотека. В решение этих проблем вы не должны (и не можете) влезать. Пока API библиотеки хорошо документирован и достаточно стабилен – вы не должны тратить свои ментальные ресурсы на то, чтобы задумываться о том, что происходит "под капотом". По мере того, как игры становятся всё более крупными и сложными, становится невероятно полезно провести черту и сказать - "всё, что по ту сторону - не моя отвественность, и мне не о чем беспокоиться".

Очевидная плата за такой подход - вы не можете изменить то, что происходит на стороне библиотеки. Если вы решаете использовать библиотеку, вы должны смириться с тем, что теряете часть гибкости в решении проблемы, которую она решает.

Вы также должны быть готовы к тому, чтобы адаптировать архитектуру вашего движка так, чтобы она соотвествовала сторонним библиотекам, которые вы используете. Попытки поступить наоборот - рецепт для получения проблем.

## Критерии хорошего middleware

Распространённое правило выбора, брать ли middleware-решение или делать своё - "если выбранная область не ваш основной бизнес - берите готовое решение".

Исключения - делайте своё решение, если хотите лицензировать технологию, или вы хотите, что ваша игра сильно отличалась от стандартных (*желательно, чтобы вы были уверены, что в лучшую сторону* ;) ).

{% blockquote %}
Каждая игра на рынке предлагает уникальное торговое предложение - особенности, которые отличают одну игру от другой.
{% endblockquote %}

Кроме отличий, ради которых игроки будут покупать именно вашу игру, также имеются какие-то характеристики, которые не являются уникальными и совпадают с другими продающимися играми. В тех областях, в которых вы согласны по получение "среднего по рынку" результата, возможно купить готовую технологию и подстроить дизайн игры в соотвествии с ней. В той части, которую вы хотите сделать лучшей и уникальной - стоит разрабатывать свои решения. Как пишет Джоель Спольски - ["не передавайте свою основную компетенцию на аутсорс"](https://www.joelonsoftware.com/2001/10/14/in-defense-of-not-invented-here-syndrome/).

Теперь же, когде вы определились с тем, какая часть функционала игры/движка может быть реализована с помощью middleware-решений, как решить, какую из множества доступных на рынке библиотек выбрать?

Вот список критериев:

**`- Хорошая библиотека позволяет указать свои функции аллокации памяти`**
В играх часто требуются кастомные аллокаторы, и если вы их используете, вы можете попросить библиотеку использовать ваши правила работы с памятью. Стандартные примеры использования - заранее выделить большой блок памяти, чтобы избежать медленных обращений к ОС за дополнительной памятью; отладочные функции (поиск утечек); подсчёт количества потребляемой отдельной подсистемой памяти. Библиотека, которая тайно выделяет память за вашей спиной - опасное решение.

**`- Хорошая библиотека позволяет указать свои функции реализации ввода/вывода`**
Многие игры/движки хранят ассеты в упакованном формате, часто в собственном оптимизированном относительно стандартного. Библиотеки, которые не поддерживают задание кастомных функций чтения и записи не позволят хранить ресурсы в таких форматах. Современные игры могут использовать подгрузку данных на лету, для чего могут оптимизировать расположение данных так, чтобы минимизировать доступ к диску. Библиотека не должна ограничивать возможности таких оптимизаций.

**`- Хорошая библиотека позволяет расширять свой функционал`**
Ни одна библиотека не решит конкретно вашу проблему "из коробки". Но вы не должны модифицировать библиотечный код для того, чтобы подстроить его под вашу ситуацию.

Вместо этого библиотека может предлагать "точки расширения" - абстрактные интерфейсы для реализации из игры, колбеки для настройки реакций на события внутри библиотеки, специализируемые классы (например, реализация обобщённых контейнеров в STL).

Библиотека для анимаций должна давать возможность создавать собственные контроллеры анимаций, физическая библиотека - работать с вашими классами для рассчёта коллизий. Ваши объекты должны быть [объектами первого класса](https://ru.wikipedia.org/wiki/%D0%9E%D0%B1%D1%8A%D0%B5%D0%BA%D1%82_%D0%BF%D0%B5%D1%80%D0%B2%D0%BE%D0%B3%D0%BE_%D0%BA%D0%BB%D0%B0%D1%81%D1%81%D0%B0) в мире библиотеки.

**`- Хорошая библиотека избегает конфликтов имён`**
Остерегайтесь библиотек, которые безответственно используют библиотеку STL. Это работает до тех пор, пока вы не решите сменить реалзацию стандартной библиотеки или перейти на платформу без поддержки STL (*этот совет практически потерял актуальность с выходом стандарта C++ 11*).

Библиотека должна объявлять свои классы в собственном пространстве имён и засорять глобальное.

Для библиотек, активно использующих STL, стоит проверить, что классы стандартной библиотеки используются так, чтобы поддерживать кастомные аллокаторы памяти (см. первый критерий).

Также лучше, если библиотека скрывает использование классов STL внутри себя, оставляя публичный интерфейс независимым от неё.

**`- Хорошая библиотека явно говорит, какие её части можно использовать в многопоточной среде`**
Мы живём в многопоточном мире, но большинство игровых движком привязаны к главному потоку (*в 2021, спустя 13 лет после написания оригинальной статьи, ситуация не намного улучшилась =\*).

Для улучшения производительности вы должны распределять задачи по потокам. Чтобы реализовать это, вы должны быть в курсе, какие функции используемых библиотек можно вызывать параллельно из разных потоков, а какие должны дожидаться синхронизации. Хорошая библиотека, например, может создавать свои ресурсы асинхронно и возвращать управление движку.

Более продвинутый случай - библиотека может позволять указать свои примитивы синхронизации/функции для создания микро-задач, аналалогично хукам аллокаторов памяти и I/O. Статья с обсуждением такого подхода - [Good Middleware revisited](https://solid-angle.blogspot.com/2009/01/good-middleware-revisited.html).

**`- Хорошая библиотека должна вписываться в вашу схему конвейера упаковки игровых данных`**
Большинство компаний во время создания игровых ресурсов артистами экспортируют их в неэффективных форматах, и преобразуют их в оптимальный для платформы вид во время стадии упаковки/построения ресурсов в процессе сборки игры. Хорошие middleware-библиотеки, которые работают с ресурсами, должны позволять артистам экспортировать ассеты в удобном для них виде. Зачастую движок должен уметь загружать как оптимизированные, так и исходные версии ресурсов без проблем, для ускорения процесса разработки.

**`- Хорошая библиотека надёжна`**
Одно из важных преимуществ использования библиотеки - вы можете освободить мозги для решения более важных проблем, но только если вы доверяете библиотеке. Проблемные и ломающиеся библиотеки - двойное проклятие, потому что вы должны искать баги в коде, написанном посторонним программистом. Более того, исправление ошибок собственными силами требует долгосрочной поддержки, чтобы интегрировать исправления в каждую обновленную авторами версию библиотеки.
Библиотека также должна иметь стабильный API, чтобы вы не занимались повторной её интеграцией с выходом каждой новой версии.

**`- Хорошая библиотека поставляется с исходниками`**
Несмотря на предыдущий критерий, вам всё равно полезно иметь возможность посмотреть исходный код библиотеки. Это позволяет проверить данные, передаваемый на вход библиотечным функциям, и может послужить документацией. Также изредка вам всё-таки может потребоваться исправить ошибку в библиотечном коде, каким бы хорошим он не был.

## Общие критерии

Другие вопросы, позволяющие оценить качество библиотеки:
**`- Как много памяти она использует и насколько быстро работает?`**
**`- Как много усилий (изменений в вашем коде и данных) потребуется на интеграцию?`**
**`- Как она будет взаимодействовать с другими используемыми библиотеками?`**
**`- Как хорошо она поддерживается авторами и сколько стоит?`**

Ответы на эти вопросы зависят от требований к вашей игре. Усилия по переделке движка для интеграции библиотеки могут значить меньше, если вы только делаете его, а не поддерживаете десяток игр, давно находящихся на рынке. Для игр под мобильные телефоны не всегда целесообразно лицензировать Unreal Engine.

(*Автор тут приводит аргумент, что его сложновато уместить в память телефона. В 2021 уже не очень сложно, но всё равно, и сейчас проблемой может стать стоимость и условия лицензирования движка*).

Неизменные с годами правила тут следущие:
{% blockquote %}
Выбирайте использование библиотек, всегда когда это возможно, но не передавайте на аутсорс свою основную компетенцию – то, из-за чего пользователи будут играть именно в вашу игру. Выбирайте библиотеки, которые позволяют вам использовать собственные правила в отношении управления ресурсами и многозадачности.
{% endblockquote %}