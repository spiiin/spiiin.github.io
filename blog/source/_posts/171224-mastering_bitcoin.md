---
title: Mastering Bitcoin
tags:
  - крипто
  - python
  - книги
abbrlink: 2409821993
date: 2017-12-24 18:15:00
---
Дочитал [Mastering Bitcoin](https://www.bitcoinbook.info/), в книжке рассказывается как о базовых концепциях самой известной криптовалюты, так и о программах/библиотеках для работы с ней.

Всё это описывается детально, виден "скелет" всего, что происходит внутри системы. Описано, как с помощью простого скрипта на Python собрать, подписать и отправить транзакцию со своего адреса, имея только приватный ключ от него.  
   
Низкоуровневые подробности интересны будут только для разработки своих приложений, но разобраться в функционировании системы будет полезно любым программистам, из-за хайпа вокруг биткоинов многих интересует только их текущий курс к доллару =\  
  
 Забавляет, что в качестве примеров часто приводятся цифры, которые по текущему курсу подходят скорее не для оплаты чашки кофе, а для покупки кофейни.  
  
В качестве упражнения попробовал повторить исследования хакера по [поиску кладов в блокчейне](https://spiiin.dreamwidth.org/113215.html). Адреса всех неизрасходованных выходов транзакций блокчейна (UTXO) можно получить из полного узла, или, если лень его качать, то их периодически выкладывают [тут](https://bitcointalk.org/index.php?topic=267618.100) (~20 млн адресов в данный момент).  
  
Получается примерно такой код:  
<https://gist.github.com/spiiin/f929da13d7f4c2ee31365f59ac22bb02>  
  
Забавно, что по [первому же адресу](https://blockchain.info/address/1Q7f2rL2irjpvsKVys5W2cmKJYss82rNCy) из примера удалось обнаружить немного реальных денег (574 сатоши, уже забрали из этого кошелька).