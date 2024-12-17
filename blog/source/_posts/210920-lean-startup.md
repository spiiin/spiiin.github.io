---
title: Метод Lean Startup
abbrlink: 2486671624
date: 2021-09-20 01:02:21
tags:
  - dev_method
  - gamedesign
  - книги
---

Выдержки из книг Эрика Риса `Lean Startup` и Стива Бланка `Четыре шага к озарению` с комментариями.

В русском варианте она называется `Бизнес с нуля: Lean startup`, что сбивает с толку. В книге разбираются случаи как запуска нового бизнеса, так и создания нового продукта в рамках существующих компаний. Кроме того, книга не про *Стартапы* (у этого слова уже давно образовалось самостоятельное значение в русском языке), а про *Запуск новых продуктов*. Так что корректнее было бы перевести название как `Способ экономного запуска новых продуктов`. С таким переводом читатели скорее заинтересуются методикой, которая может быть адаптирована для различных типов проектов. Например, Николас Ловелл в книге `The Pyramid of Game-Design` описывает использование элементов методологии в разработке игр.
<!-- more -->

##Любая игра -- инновация
{% blockquote ries %}
Почти все, с кем мне приходится общаться, считают, что по крайней мере в их отрасли проекты терпят неудачу по серьезным причинам: они всегда рискованны, состояние рынка непредсказуемо, а сотрудники крупных компаний не могут похвастаться творческими способностями. Некоторые полагают, что если мы просто будем действовать не спеша, с большей тщательностью, то сможем избежать многих неудач, реализуя меньше проектов, но делая это более качественно.
{% endblockquote %}

Ага, геймдев -- экстремально hit-driven отрасль разработки, в которой нормальным считается успех 1-2 проектов из 10. `Supercell`, которые являются эталоном и лучшими, запустили 4 успешных проекта, закрыли 13 на этапе софт-ланча, и неизвестно сколько ещё на более ранних непубличных этапах.

Для игры на ранней стадии разработки не всегда понятно, где же обнаружится фан, и какой она станет в итоге. Некоторые примеры серьёзной трансформации жанров игр в ходе прототипирования я собирал в заметке о прототипировании игр (раздел `Путь от прототипа к результату`) - {% post_link 210808-prototyping 'Прототипирование в геймдеве' %}

(Кроме трансформации жанра естественно происходит и трансформация аудитории игры)

Игры на рынке не могут быть просто более дешёвой версией другой качественной игры, как это могло бы быть с другими типами товаров, поэтому любая игра -- это инновация, со своим уникальным рыночным предложением(`Unique Selling Point`). Тайнан Сильвестр в книге `Гейм-дизайн. Рецепты успеха лучших игр` использует для описания уникального предложения концепцию **`Кривая ценности`**. Примеры относительного сравнения нескольких игр
![usp](210920-lean-startup/usp_small.png)

Смысл графика кривой ценности -- AAA-игры должны обладать несколькими уникальными особенностями, чтобы выделяться на фоне других по их совокупности, в то время как инди-игры могут сосредоточиться на чём-то одном, проигрывая по другим параметрам. Тем не менее, любая игра делает предположение о том, нужно ли что-то игрокам (например, "Чокнутая креативность", за счёт которой популярна `Garry's Mod`).

Задача бережливого запуска -- найти способ проверить гипотезу о том, настолько ли нужно игрокам то, в чём игра будет лучше других, как это ожидают разработчики, до окончания полного цикла разработки и вывода игры на рынок.

##Minimum awesome product
{% blockquote %}
Другие считают, что есть люди, обладающие врожденным даром понимать, что нужно делать, а что - нет. Если нам удастся найти достаточно таких магов и волшебников, это решит все наши проблемы. Но такой подход мог бы быть оправдан разве что в XIX веке, когда о современном менеджменте еще никто не слышал. Мир меняется все быстрее, и такие древние подходы давно потеряли эффективность. При этом вина за неудачу проекта и провал бизнеса часто возлагается на высшее руководство, от которого ждут невозможного.
{% endblockquote %}

Есть такое, менеджеры хотят найти супер-таланты, если что-то не получилось - виноват продюссер, суперчеловек, который должен нутром чувствовать, как надо всё делать.

{% blockquote %}
Многие опасаются, что конкуренты, особенно крупные корпорации, украдут идею стартапа. Но если бы хорошую идею было так легко украсть! Ведь это и есть одна из основных проблем стартапов: почти невозможно добиться того, чтобы вашу идею, компанию или продукт заметил хоть кто-нибудь, а тем более конкуренты. Иногда предпринимателям, которые этого боятся, я даю такое задание: возьмите какую-нибудь свою идею (например, одну из ваших последних разработок), выясните, как зовут продукт-менеджера какой-нибудь крупной корпорации из той сферы, к которой относится ваша идея, и попытайтесь заставить эту компанию украсть ее. Позвоните этому менеджеру, напишите ему письмо, отправьте пресс-релиз - давайте, попробуйте!
{% endblockquote %}

У каждой второй компании есть *сверхсекретный прототип игры*, которые нельзя показывать никому, особенно игрокам, пока их официально не анонсируют (например, чтобы не склонировали по быстрому китайцы)

{% blockquote %}
Но если конкуренты смогут опередить стартап, как только увидят его идею, он обречен. Создавать команду, чтобы реализовать новую идею, нужно лишь в том случае, если вы уверены, что сможете пройти цикл обратной связи «создать-оценить-научиться» быстрее всех остальных. Если это так, не имеет значения, что знают о вашей идее конкуренты. А если нет, значит, у стартапа есть очень серьезные проблемы, и секретность их не решит. И стартовое преимущество, полученное за счет работы в режиме секретности, вдали от клиентов, едва ли тут поможет. Единственный путь к победе - учиться быстрее всех.
{% endblockquote %}

Идея метода -- не создавать большой и дорогой продукт, а попробовать продавать клиентам полуготовый, просто чтобы понять, нужен ли он им вообще в задуманном виде, или же какие-то первоначальные предпосылки были ошибочными и их нужно менять.

>Чаще всего предприниматели сначала создают продукт, а потом проверяют, как отреагируют на него клиенты. Но я предлагаю поступать как раз наоборот и таким образом избегать ненужных трат.

Рис -- автор широко известной сейчас концепции **`Minimum valuable product`** (MVP) -- продукт, который уже можно продать пользователям для того, чтобы понять, нужен ли он им. Этим продуктом может быть вообще не программа, а просто форма предзаказа на сайте, группа в соцсети или кампания на Kickstarter.

{% blockquote %}
Да, иногда клиенты считают, что MVP- продукт недостаточного качества. Если так, это нужно использовать для того, чтобы понять, какие опции важны для клиентов. Такой подход гораздо результативнее, чем теоретические размышления о стратегиях, потому что он дает прочные эмпирические основания для создания будущих продуктов.

Будьте готовы к тому, что MVP может принести дурные вести. 
В отличие от традиционного тестирования концепции или опытных образцов, MVP предназначен для того, чтобы проверить весь спектр вопросов, а не только те из них, что связаны с дизайном или технологиями.
{% endblockquote %}

Применительно к геймдеву, пара замечаний от Ловелла:

Часто компании бояться выпустить игру прохого качества. Некоторые запускают тестовые игры под другим брендом. Такой способ позволяет без шумного запуска проводить исследования на небольших группах игроков без риска привлечь лишнее внимание, которое не нужно проектам на этапе исследований.

Программисты часто плохо понимают концепцию MVP, не так, как дизайнеры или бизнес, поэтому Ловелл [выделяет](https://www.gamesbrief.com/2014/04/make-a-minimum-awesome-product/) отдельные прототипы:
**`Minimum Feasible Product`** -- техно-демо, прототип того, что команда может реализовать задуманное.
**`Minimum Desirable Product`** -- минимальный продукт, в который захотят поиграть пользователи.
**`Minimum Viable Product`** -- минимальный продукт, который продаётся для проверки того, рентабельно ли делать игру.
В сумме необходимо получить **`Minimum Awesome Product`**, который можно тестировать и развивать.

{% blockquote %}
Если мы не знаем, кто наш клиент, мы не знаем, что такое качество.
{% endblockquote %}

##Что такое качество

{% blockquote %}
Концепция бережливого производства определяет ценность как создание преимуществ для клиента, а все остальное - затраты. Если речь идет о сфере производства, клиента не волнует, как сделан продукт, - ему нужно, чтобы он как следует работал. Но стартап еще не знает, кто его клиент и что для него ценно. Это одно из проявлений той самой неопределенности, с которой постоянно сталкиваются стартапы. 

Но все наши действия, не помогавшие нам учиться, приводили к потерям. Так можно ли было учиться, не тратя столько усилий? Конечно, можно.
{% endblockquote %}

Звучит, как будто Рис нашёл очевидное простое решение. На самом деле вроде и очевидное, но не простое -- изучать клиентов итеративно вместе с итерациями развития продукта.

{% blockquote %}
Вот мысль, не дававшая мне спать по ночам: нужно ли нам было тратить время и силы на разработку ненужной фичи? Что, если бы мы выяснили, насколько некорректны наши предположения, вообще не создавая продукт? Например, предложили бы клиентам испытать продукт исключительно на основании его возможных опций, еще до того, как приступить к созданию полной версии?
Все эти терзавшие меня мысли не имели отношения к моим должностным обязанностям. Я был руководителем отдела разработки и должен был обеспечивать своевременное создание качественных продуктов и опций. Но если многие из этих опций - пустая трата времени, то что мне оставалось делать? Как избежать этих трат?
{% endblockquote %}

Угу, программисты программируют, дизайнеры дизайнят, артисты создают красивый арт -- все делают всё хорошо, что же может пойти не так?

{% blockquote %}
Но теперь мое взаимодействие с пользователями изменилось. Внезапно у меня возникли вопросы, на которые нужно было срочно ответить: почему клиенты не реагируют на «совершенствование» продукта? Почему все наши усилия ни к чему не приводят?

Во время встречи я задал членам команды простой вопрос, который всегда задаю основателям стартапа: «Становится ли ваш продукт лучше?» Они всегда отвечают: «Да». Тогда я спрашиваю: «Откуда вы об этом знаете»? 
И каждый раз получаю один и тот же ответ: «Ну, мы занимаемся разработкой и в этом месяце ввели множество изменений, нам кажется, что нашим клиентам они понравятся, и наши общие показатели в этом месяце улучшились. Должно быть, мы на верном пути». И еще важнее: как мы узнаем, что правильно понимаем и интерпретируем эти изменения?
{% endblockquote %}

Нет инструментов для измерений -- нет никакой точной информации, станет ли игрокам нравиться играть больше, или нет. Более того, неправильные измерения могут являться `метриками тщеславия`, улучшающим настроение разработчиков, но не популярность игры у игроков.

{% blockquote %}
Инженеры, дизайнеры и маркетологи - мастера оптимизации. Скажем, специалисты по директ-маркетингу проводят сплит-тестирование, чтобы выяснить мнение потребителей о ценности нового продукта. Они отправляют разные предложения двум одинаковым группам клиентов, а потом оценивают различия в реакции этих двух групп. Инженеры, конечно же, умеют повышать производительность продукта, а дизайнеры делают его удобным в использовании. Все эти действия в стабильной традиционной организации дают постепенные преимущества при постепенных усилиях. 
До тех пор, пока мы хорошо выполняем план, наш труд приносит результат. Однако в случае со стартапом такие инструменты совершенствования продукта не работают. Если вы создаете ненужный продукт, его оптимизация или маркетинг ни к чему не приведут
{% endblockquote %}

##Опасность создания хорошего ненужного продукта

{% blockquote Алан Купер, "Психбольница в руках пациентов" %}
Неприятная особенность нежелания разбираться в причинах неудач заключается в том, что все участники молча признают невозможность спрогнозировать успех, считая, что в индустрии высоких технологий все зависит лишь от удачи и случая. Это явление, в свою очередь, положило начало подходу к инвестированию, которое инвесторы называют spray-and-pray («стреляй куда придется и молись, чтобы попало»): небольшие суммы денежных средств вкладываются во множество предприятий, а затем остается лишь надеяться на то, что хотя бы одно из них окажется успешным.
{% endblockquote %}

Дороже разработки программ может быть только разработка плохих программ

{% blockquote %}
Главный вопрос нашего времени не в том, можно ли это сделать, а в том, нужно ли. Мы переживаем необычный исторический момент: наше будущее процветание зависит от коллективного воображения человечества. 

«Конечно же, нет ничего более бесполезного, чем эффективно делать то, что вообще делать не нужно». 
{% endblockquote %}

##Где искать знания о клиентах?

**`Постоянно собирать с помощью экспериментов`**

[Just Enough Research / Erika Hall - UX Salon 2016](https://youtu.be/5WtB5FRn-Sc)
- Если хотите знать, кто в действительности владеет знаниями о клиентах в вашей организации - это не кто-то на высоком посту, а часто люди из службы поддержки.
- Никогда не просите людей что-то предсказать. Вы не заработаете денег если поймёте, что люди считают о себе, вы заработаете их если поймёте что люди реально делают.
- Поставьте вопросы -> соберите данные для ответа на ваши вопросы -> проанализируйте данные
- Data->Meaning->Useful insights

**`Поставить вопросы, собрать данные от клиентов, понять смысл собранных данных, затем, возможно, получить инсайты`**

**`Генти Генбуцу`** - "Иди и посмотри сам".
{% blockquote blank %}
In a startup no facts exist inside the building, only opinions. для стартапа в офисе не существует никаких фактов, только мнения.

Нельзя решить проблему, если ты её не понимаешь, а чтобы понять, нужно её увидеть. Недопустимо полагать что-то само собой разумеющимся или полагаться на рассказы других. Стив Бланк уже много лет убеждает предпринимателей в том, что информацию, которую нужно собрать о клиентах, рынках, поставщиках и каналах сбыта, можно найти только «на улице». Так что вставайте из-за стола и отправляйтесь знакомиться с ними! 
{% endblockquote %}

[Метод пяти почему](https://en.wikipedia.org/wiki/Five_whys) - кроме устранения очевидной неисправности находить её первопричину.

[Карта эмпатии](https://netology.ru/blog/karty-empatii-v-marketinge) -- способ описать накопленные знания о клиентах, используемый маркетологами.

Алан Купер в `Психбольница в руках пациентов` предлагает немного похожий [метод персон](https://habr.com/ru/post/248063/), больше ориентированный на дизайнеров/проектировщиков, описывающий взаимодействия и сценарии использования клиентами продукта.

##Проблемы традиционного планирования

{% blockquote %}
Одна из причин - в «сокрушительном обаянии» хорошего плана, основательной стратегии и всесторонних исследований рынка. Прежде они служили надежными индикаторами вероятности успеха, и потому очень соблазнительно применять их к стартапам. Но это не срабатывает, потому что стартапы действуют в условиях почти что полной неопределенности. Еще не известно, кто их клиенты или каким должен быть их продукт.

Планирование и прогнозирование точны только тогда, когда они основаны на долгой, стабильной истории деятельности и только в относительно стабильной окружающей среде. А у стартапов нет ни того, ни другого.

Предприниматели и инвесторы видят: традиционные методы менеджмента не в состоянии решить эту проблему. И зачастую они пускают все на самотек и действуют по принципу «просто сделай это». Согласно этому принципу, если управлять процессом сложно, то лучшая стратегия - хаос. К сожалению, мой личный опыт свидетельствует о том, что это тоже не работает.
{% endblockquote %}

"Просто сделай это (хорошую игру), и игроки придут" -- игра слов с [мотто фильма](https://ru.wikipedia.org/wiki/%D0%9F%D0%BE%D0%BB%D0%B5_%D0%B5%D0%B3%D0%BE_%D0%BC%D0%B5%D1%87%D1%82%D1%8B), к сожалению почти никогда не работает в реальном мире на тесном рынке.

{% blockquote %}
Проблема многих планов не в том, что они упускают из виду важные стратегические принципы, но в том, что факты, на которых основаны эти планы, не соответствуют действительности. К сожалению, это невозможно обнаружить в теории - такие промахи можно заметить только в процессе взаимодействия продукта и пользователей.
{% endblockquote %}

{% blockquote blank%}
Что бы вы сделали по-другому, если бы знали, что только одна из десяти попыток создания нового продукта приводит к рождению прибыльного бизнеса? Стали бы вы продолжать вести дела так же, как сейчас, неделя за неделей, год за годом? Вы, вероятно, удивитесь, но факты таковы, что и крупные, и небольшие компании, и огромные корпорации, и новорожденные стартапы проваливают девять из десяти попыток запуска нового продукта. Для этого не обязательно прожечь миллиарды долларов, продвигая новинку на рынок, где покупатели вовсе не ждут ее.
{% endblockquote %}
Мотивирующее предисловие из книги Стива Бланка.

[Стратегия New Lanchester](https://studref.com/417544/ekonomika/strategiya_lanchester) - военная стратегия, используемая и для прикидок в бизнесе. Чтобы конкурировать с монополией/дуополией, нужно тратить на маркетинг в 3 раза больше ресурсов, чем лидер.

##Развитие знаний о клиентах

{% blockquote blank%}
Развитие понимания клиентов это процесс, параллельный развитию продукта. Мы не отказываемся от видения продукта на каждом шаге экспериментов, но делаем всё возможное, чтобы подтвердить и уточнить его.
{% endblockquote %}

Отсюда Бланк делает вывод об удобстве использования Agile-методологии разработки -- в короткие итерации цикла разработки удобно вставить пустые "слоты", в которые будет вставлена информация, полученная в ходе параллельного процесса изучения клиентов.

{% blockquote %}
Разница между победителями и проигравшими проста. Когда топ-менеджмент компании с самого начала выходит из офиса и много и часто общается с потребителями, развитие продукта завершается успехом. Когда судьба продукта отдается полностью в руки департаментов по продажам и маркетингу, которые не вовлечены напрямую собственно в процесс разработки нового продукта, компанию ждет поражение. Здесь нет ничего сложного. В настоящее время большинство компаний предпочитают сосредоточиться на деятельности, не выходя из офиса, чтобы обеспечить представление своего нового продукта рынку.

Вывод очевиден: внимание к мнению будущих покупателей, умение выйти из офиса и исследовать потенциальных потребителей и рынок до того, как окончательно выбрать свой путь и определить характеристики продукта, — вот константа, которая определяет разницу между победителями и побежденными, вот в чем заключается идея процесса развития потребителей.
{% endblockquote %}

Ошибки в стандартной схеме "разработки продукта": `концепция/посев-->разработка-->альфа/бета тест-->запуск/первая поставка`:

- Название "модель разработки продукта" - не описывает "не-разработочные" процессы: маркетинг, продажи, найм, обретение клиентов, финансирование.
- Где потребители? Причина неудач - не в развитии нового продукта, а в развитии клиентов и рынков. Недостаточное количество потребителей и отсутствие выверенной финансовой модели.
- Зацикленность на дате получения первой версии продукта покупателем. В действительности факт запуска не означает, что компания понимает своих клиентов и знает, как следует подавать и продавать им продукт.
- Акцент на исполнении плана в ущерб процессам обучения и изучения
- Отсутствие значимых ориентиров для отделов маркетинга, продаж и развития бизнеса
- Использование схемы разработки продукта для измерения продаж
- Использование методологии разработки продукта для измерения успеха маркетинга
- Преждевременное масштабирование
- Смертельная спираль: цена ошибок при запуске продукта.
- Не все стартапы одинаковы (могут сегментировать существующий рынок или создавать новый)
- Нереалистичные ожидания

{% blockquote %}
Однако, даже если нам удалось поднять маркетологов из-за столов и отправить «в поля», карты все равно крапленые и честного выигрыша не получится. Посмотрите на схему разработки продукта. Когда маркетологи могут выяснить, работают ли на самом деле позиционирование, «ажиотаж» и создание спроса? После даты начала продаж первым клиентам. Неумолимый марш к этой дате не предполагает итеративного цикла, который бы говорил: «Если наши предположения неверны, возможно, мы должны попробовать что-то другое».

Информация и данные о потребителях собираются постепенно, шаг за шагом. Иногда эти шаги могут повести вас в неправильном направлении или заманить в тупик. Вы будете искать неправильных клиентов, не понимая мотивации потребителей и степени важности различных характеристик продукта. Именно способность учиться на своих ошибках отличает успешный стартап от тех, что исчезли без следа.
{% endblockquote %}

##Кросс-функциональные команды

{% blockquote %}
При благоприятных экономических условиях компания может позволить две или три итерации вокруг неудачного запуска продукта или плохих показателей продаж. В более жесткие времена инвесторы менее щедры и считают каждую копейку, прежде чем профинансировать очередной транш.
{% endblockquote %}

Совпадает с моими ощущениями по количеству выдаваемых попыток исправить что-то крупными переделками при "традиционной" разработке.

{% blockquote %}
Предприниматель - это должность. Предпринимательство может стать для новаторов хорошим способом развития карьеры в крупных организациях. Тогда менеджерам, способным возглавлять команды и работать по системе «экономичный стартап», не придется покидать компанию, чтобы самореализоваться, или пытаться вписаться в жесткую иерархию традиционных функциональных подразделений. Вместо этого на их визитных карточках будет написано: «Такой-то. Предприниматель». И все. Такие менеджеры могут отчитываться перед руководством, используя систему учета инноваций, и получать вознаграждение в соответствии с достигнутыми результатами. 
{% endblockquote %}

А также решает проблемы некоторых разработчиков игр, сталкивающихся с недостатком творческой реализации и желанием делать свои инди-проекты по вечерам.

{% blockquote %}
Если мы начнем определять продуктивность команды не как успешное выполнение узкофункциональных обязанностей - в сфере маркетинга, продаж или разработки продукта, а как получение фактических данных, возникнут проблемы. Как мы уже говорили, функциональные специалисты привыкли оценивать свою эффективность в соответствии с тем, сколько времени они тратят на работу. Например, программисты считают, что весь день должны писать коды. Именно поэтому традиционная рабочая атмосфера их так раздражает, ведь им все время приходится отвлекаться: встречи, кросс-функциональные задачи и бесконечные совещания с начальством - все это снижает эффективность. 

Однако эффективность отдельных специалистов не является целью «Экономичного стартапа». Вместо этого нужно создавать кросс-функциональные команды, позволяющие получать подтверждение фактами. Многие методы - действенные показатели, непрерывное развертывание и полный цикл обратной связи «создать-оценить-научиться» - предназначены для того, чтобы побуждать команду оптимизировать отдельные функции. Не так важно, как быстро мы можем создать продукт. Не так важно, как быстро мы можем его оценить. Важнее всего то, как быстро мы можем пройти весь цикл.
{% endblockquote %}
Как хочет работать программист полный рабочий день:
![kot](210920-lean-startup/kot.gif)

{% blockquote %}
Инновации всегда начинаются с видения. Важнее всего то, что происходит дальше. Как мы видели, команды инноваций часто начинают заниматься «пантомимой успеха» и вместо того, чтобы проверять элементы своего видения с помощью настоящих экспериментов, обращают внимание лишь на то, что позволяет подтвердить свою правоту. Или, что еще хуже, они работают «тайно», пытаясь создать зону, свободную от данных, где можно «экспериментировать, не получая никакой обратной связи от потребителей и без всякой ответственности. Каждый раз, когда такая команда пытается продемонстрировать кому-то причинно-следственные связи, рисуя красивые графики общих показателей, она занимается псевдонаукой. Как узнать, что эти причинно-следственные связи соответствуют реальности? Каждый раз, когда команда пытается использовать «желание учиться» в качестве оправдания, она также занимается псевдонаукой. Если в одном цикле итерации мы чему-то научились, давайте подтвердим эти данные в следующем цикле. Только создав модель поведения потребителей, а затем подтвердив, что мы способны использовать наш продукт или сервис, чтобы менять это поведение, можно выяснить, насколько обосновано наше видение.
{% endblockquote %}

[Отзывы пользователей изменили культуру и игровой дизайн Rovio](https://www.businessthink.unsw.edu.au/articles/Angry-Birds-fly-high-again-with-data-analytics) - статья про то, как сбор данных о клиентах изменил культуру и организацию компании Rovio.

##Переход на методы Lean Startup

"Песочница" инноваций:
{% blockquote %}
Работать в «песочнице» инноваций - все равно что тренировать мышцы. Сначала команда проводит небольшие эксперименты. Возможно, первые из них не дадут ничего для обучения и окажутся не слишком успешными. 
Но со временем команда будет работать все лучше и лучше и в итоге благодаря подходу небольших партий и действенным показателям начнет получать постоянную обратную связь. При этом обучение будет все более эффективным.

Я обучаю других своей системе уже много лет и постоянно сталкиваюсь с тем, что переход к концепции подтверждения фактами сначала вызывает отторжение и только потом люди начинают видеть, в чем заключается ее суть. Дело в том, что проблемы, вызванные старой системой, часто бывают неосязаемыми, а проблемы новой системы слишком очевидны. Но тут нужно знать теорию. Если все понимают, что временное снижение продуктивности в переходном периоде неизбежно, то этим процессом можно активно управлять.
{% endblockquote %}

Кривая жизненного цикла, поиск ранних клиентов:
{% blockquote %}
Новый продукт последовательно принимается 5 категориями - техноэнтузиасты, провидцы, прагматики, консерваторы, скептики.
Форма рынка - гауссова кривая, причём между провидцами и массовым рынком - пропасть (мелкие пропасти также и между другими группами.
{% endblockquote %}

Признаки раннеевангелиста (находятся на 4-5 стадиях)
- Имеет проблему
- Осознаёт наличие проблемы
- Активно ищут решение
- Состряпал решение на коленке
- Имеет или может привлечь средства

{% blockquote %}
Задача развития потребителей — это сделать так, чтобы знания компании о клиентах шли в ногу с разработкой продукта, а также обеспечить уверенность в том, что у продукта, когда он появится на рынке, будут платежеспособные покупатели. идентифицировать ключевую группу провидцев, определить их потребности и убедиться, решает ваш продукт проблему, которую нужно и за которую они готовы заплатить, или нет.
{% endblockquote %}

##Пивот

[Пивот](https://ru.wikipedia.org/wiki/%D0%9F%D0%B8%D0%B2%D0%BE%D1%82) (вираж?).

Стартап должен иметь возможность "разворота", если собранные данные о клиентах показывают такую необходимость. Нашли что-то неожиданное, что любят клиенты -- этим стоит попробовать воспользоваться. Также, если не удаётся обнаружить клиентов, стоит попробовать что-то радикально новое. Успешность обучения и виражей определяется тем, что каждая итерация проходит быстрее предыдущей -- приближает к конечной цели нахождения своих клиентов и работы с ними.

{% blockquote %}
Чрезвычайно важен сдвиг в сознании. Если это первый продукт, который производит стартап, ваша главная задача, идя навстречу потребителям, — не собрать пожелания в отношении характеристик и расширить их набор впоследствии, а найти потребителей на продукт, который вы уже создаете. Только в том случае, если ваше решение не устраивает никаких потребителей, познакомьте группу разработки продукта с дополнительными пожеланиями клиентов.
{% endblockquote %}

##Темпы роста 

{% blockquote %}
Темпы роста зависят прежде всего от трех показателей: прибыльности каждого клиента, стоимости привлечения новых клиентов и количества повторных покупок, совершенных существующими клиентами. Чем выше эти цифры, тем быстрее будет расти компания и тем более прибыльной она будет. Это и есть драйверы модели роста компании. По контрасту у компании, которая знакомит между собой покупателей и продавцов, например у еВау, - другая модель роста. Ее успех зависит в первую очередь от сетевых эффектов, повышающих ее популярность и среди покупателей, и среди продавцов.
{% endblockquote %}

Три механизма роста - `оплаченный, вирусный, липкий`.
В отношении жизнеспособного роста действует одно простое правило: Новые клиенты приходят благодаря действиям клиентов, которые пришли раньше. Клиенты, которые пришли раньше, содействуют жизнеспособному росту четырьмя способами:
- Сарафанное радио
- Побочный эффект использования продукта. "Вирусность" продукта (facebook, paypal)
- Затраты на рекламу (затраты на рекламу оплачиваются с доходов, полученных от предыдущих пользователей)
- Повторные покупки или повторное обращение (подписки и сменные/расходуемые компоненты - от электрических лампочек до кристаллов в играх)

{% blockquote %}
Если у нас есть продукт, популярный среди ранних последователей, теоретически его разработку можно остановить. Рост будет продолжаться до тех пор, пока этот первоначальный рынок не исчерпает себя. Затем он замедлится или даже полностью остановится. Проблема в том, что такое  замедление может длиться месяцами или даже годами. 

Некоторые неудачливые компании опрометчиво следуют привычной стратегии. Они используют «показатели тщеславия» и традиционную систему отчетности, и им кажется, что они делают успехи, когда видят, что их показатели растут. Они ошибочно полагают, что улучшают продукт, хотя на самом деле изменение его опций не оказывает никакого влияния на поведение потребителей. Рост происходит только благодаря механизму, который эффективно работает и привлекает новых клиентов, а не благодаря усовершенствованиям в разработке продукта. Поэтому, когда рост внезапно замедляется, начинается кризис. Та же проблема возникает у крупных компаний. Их прошлые успехи были основаны на точно настроенном механизме роста. Если он замедляется или перестает работать, а у компании нет новых инновационных проектов, способных обеспечить новые источники роста, возникает кризисная ситуация. И это может произойти с компанией любого размера. Поэтому нужно одновременно настраивать механизм роста и развивать новые источники роста на тот случай, когда этот механизм перестанет работать.
{% endblockquote %}
