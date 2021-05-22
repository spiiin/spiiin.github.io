---
title: scala_vk_get_pictures
tags:
  - vk
  - scala
abbrlink: 1798415512
date: 2015-03-24 03:34:00
---

Продолжаю сравнивать Scala и Python на небольших прикладных задачках.

На этот раз переписал [старый скрипт](http://spiiin.livejournal.com/2023.html) для выгрузки всех фотографий из альбома Вконтакта.

Небольшие отличия в задаче - 5 лет назад у VK не было api, поэтому url картинок получался парсингом страницы, сейчас обычным запросом к api.

[Старый код на python](https://gist.github.com/spiiin/ce2c43808d2d09fda361): 136 строк
[Новый код на scala](https://gist.github.com/spiiin/53312ac444f73497f645): 36 строк 

```scala
var token: String = ""
  implicit def string2xml(v: String) = XML.loadString(v)

  override def main(args: Array[String]): Unit = {
    implicit val threadPool = ExecutionContext.fromExecutor(Executors.newFixedThreadPool(4))
    val cmdName = "../../vkAuthorizeToOutput/vkAuthorize.exe"
    token = (cmdName.!!).replace("\r\n", "")
    val photosAns = getPhotos("OWNER_ID", "ALBUM_ID")
    val photo_1280 = extractBigPhotos(photosAns)
    val fut = photo_1280.zipWithIndex.map {
      case (url, i) => Future { println(i + " " + url); saveToFile(url, f"C:/users/USERS/desktop/test/$i%03d.jpg") }
    }
    Await.result(Future.sequence(fut), 30 seconds)
    println("END")
  }

  def getPhotos(ownerId: String, album_id: String) = executeCommand("photos.get", token, ("owner_id" -> ownerId), ("album_id" -> album_id))
  def extractBigPhotos(xml: String) = (xml \\ "photo").map(v => (v \ "src_xxbig").text)
  def saveToFile(url: String, filename: String) = new URL(url) #> new File(filename) !!
  def executeCommand(cmd: String, accessToken: String, params: (String, String)*) = {
    val fmt = s"https://api.vkontakte.ru/method/$cmd.xml?access_token=$accessToken" + params.map { case (k, v) => k + "=" + v }.mkString("&", "&", "")
    Source.fromURL(fmt).mkString
```

Implicits-параметры функций как-то сильно настораживают.

За счёт него можно парой строк включить/выключить многопоточность - у конструктора класса Future есть неявный параметр ExecutorContext, и если его опустить, то что именно передастся в конструктор будет зависеть от того, какой именно неявный объект будет находится в области видимости: 

```scala
import ExecutionContext.Implicits.global //так импортируется  объект implicit lazy val global: ExecutionContextExecutor
implicit val threadPool = ExecutionContext.fromExecutor(Executors.newFixedThreadPool(4)) //так создаётся свой пул потоков
Future { println(i + " " + url); saveToFile(url, f"test/$i%03d.jpg") } //эти объявления повлияют на эту строку (в которой нет никакого упоминания ExecutionContext вообще!)
//лучше всё время указывать неявный параметр явно:
Future { println(i + " " + url); saveToFile(url, f"test/$i%03d.jpg") }(threadPool) //теперь видно, что между создаваемым объектов и местом его выполнения есть связь
```

Скала не перестаёт удивлять своей идиоматичностью - для каждой подзадачи находится несколько вариантов решения, часто однострочных.