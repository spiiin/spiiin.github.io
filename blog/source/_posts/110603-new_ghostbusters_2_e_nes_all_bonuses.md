---
title: 'New Ghostbusters 2 (E) [NES] All bonuses'
tags:
  - nes
  - games
  - hack
abbrlink: 51050
date: 2011-06-03 19:47:00
---

##Особенности игры: 
 
 Движок использует для описания логики интерпретатор игровых скриптов, содержащий примерно 25 основных команд и еще 25 дополнительных (среди которых есть циклы, условные и безусловные перехода, команды записи значений по адресам).
 
 Теперь я понимаю, почему скриптовые языки получаются именно в 5-10 раз медленнее нативных ^\_^.
 
 Записи о призраках и комнатах состоят из перемешанного набора команд интерпретатора скриптов и данных. 
 
 В игре есть бонусы - мешки с деньгами, за которые начисляется по 3000 очков, но появляются они настолько редко, что за прохождение можно найти не более пары, и то если повезет. Но из кода комнаты можно вытащить команду записи условия появления бонуса. Она состоит из записи указателя на цепочку байт, заканчивающуюся нулём, соответствующую набору типов призраков, которых нужно отловить в заданном порядке для получения мешка. Естественно, что случайно наткнуться на нужный порядок практически нереально.
 
  Я подозреваю, что стал вообще первым из игроков после самих разработчиков, собравшим все возможные спрятанные мешки.
  
Видео:
{% youtuber video L90WP3TiEhI %}
{% endyoutuber %}
  
Цепочки призраков:
```
Stage 1-1. Running Ghost, Slimer, Slimer.
Stage 1-3. Running Ghost, Fast slimer, Invisible Chainsaw Ghost, Slimer.
Stage 1-7. Slimmer with carts, Debris-throwing Slimer, Fast slimer x 3, Debris-throwing Slimer x 2.
Stage 2-5. Jackhammer worker x 2, Mine Car worker, Jackhammer worker x 2, Hammer worker.
Stage 2-6. Mine Car worker, Jackhammer worker, Hammer worker, Mine Car worker, Jackhammer worker, Hammer worker.
Stage 2-7. Mine Car worker x 2, Pick workers
Stage 2-8. Hammer worker, Pick workers, Hammer worker, Mine Car worker.
Stage 2-9. Hammer worker, Pick workers, Jackhammer worker, Mine Car worker.
Stage 3-3. Imp x 3, Blob x 2.
Stage 3-6. Blob x 2, Ninja with sword..
Stage 3-9. Ninja with shureken x 2, Blob.
Stage 3-13. Blob, Fly imp x 3, Blob.
Stage 3-15. Blob, Fly imp x 6, Imp.
Stage 4-6. Fast Debris-throwing Slimer x 3, River Creature x 2, Fast Debris-throwing Slimer.
Stage 4-9. Stand Debris-throwing Slimer x 4, Rotating Creature x 4.
Stage 4-10. River Creature, Rotating Creature, River Creature, Rotating Creature, River Creature x 2, Rotating Creature x 2.
Stage 4-11. River Creature, Rotating Creature x 2, Fast Debris-throwing Slimer, River Creature, Rotating Creature, Fast Debris-throwing Slimer, Rotating Creature.
Stage 5-11. Wall Slime, Chainsaw Ghost, Wall Slime x 3, Chainsaw Ghost x 2.
Stage 5-12. Slimer x 2, Wall Slime x 4, Running Ghost x 2.
```