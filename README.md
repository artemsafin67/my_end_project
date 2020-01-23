Добрый день! Меня зовут Артём и я сделал игру Тетрис.
Для начала, если кто-то не знает или подзабыл правила, я кратко их расскажу.
•	Цель игры – набрать как можно больше очков
•	За каждое заполнение строки фигурами, игрок получает очки
•	Когда игрок не может поставить фигуру, то есть она находится на верхней строке – он проигрывает

Немного о использованных технологиях
Основными библиотеками, без которых бы я не написал Тетрис были pygame (для отрисовки интерфейса и основого игрового процесса), socket (для возможности отправки и получения данных с сервера) и threading (для возможности одновременного получения данных с сервера и игрового процесса. Иными словами, для использования многопоточности)

Ну а теперь перейдем к структуре программы. При запуске приложения пользователь попадает в меню. Отсюда он может запустить однопользовательскую игру, сетевую игру для двоих или попасть в настройки. 

В настройках пользователь может включить или выключить звуковые эффекты, изменить своё имя и зарегистрировать его на сервере (это необходимо для игры по сети). 
Нажав на кнопку “новая игра” мы запускаем обычную однопользовательскую игру.  На экране показывается полезная информация, такая как рекорд, текущий счёт и уровень сложности.
Аналогично, нажав на кнопку “игра по сети” мы попадаем в меню выбора соперника. Надо вбить имя игрока и нажать на галочку. Если игрок нас пригласил до этого, мы сразу же попадаем в игру. В противном случае, мы ожидаем ответа от нашего соперника.

Что же можно доработать?
Во-первых, очевидно, надо поработать над дизайном, чтобы пользователю было приятнее играть.
Во-вторых, можно улучшить удобство при подключении для сетевой игры (например, добавить отображение текущих приглашений)
В-третьих, для того чтобы игроку было комфортнее, хорошо было бы добавить больше персонализации (например, выбор темы)

Немного о клавишах для управления игрой:
a - поворот влево на 90 градусов
s - поворот вправо на 90 градусов
стрелка влево - сдвиг фигуры влево
стрелка вправо - сдвиг фигуры вправо
стрелка вниз - опускает фигуру вниз
