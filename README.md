№ Лабораторная работа № 3
# Tech_Prog_lab2_3
client serser application, using json to transfer data, to save and to load state.
## Вариант 8
* Почта  - myslim2000@ya.ru
* Группа - 6408

## Задание
  Кооперативная игра “Удалённая стыковка”. В игру играют два игрока:  один  на  земле,  другой  на  корабле,  стыкующемся  с космической станцией в точке лагранжа L1. Оператор на земле получает  положение  и  вращение  корабля,  лётчик  не  знает положения, но может управлять кораблём и получать сообщения от  оператора.  Информация  распространяется  с  задержкой. Игроки выигрывают при совершении успешной стыковки.
  Добавьте в свой предыдущий проект возможность сохранения состояния в виде периодического сохранения, либо в виде функций импорта и экспорта. Выбранный формат для сериализации должен иметь  схему.  В  проекте обязателенкод  валидирующийданные. Валидация должна производитьсялибо в программе при импортеданных,   либо   в   юнит-тестах,   проверяющих   корректность сохранения состояния.

## Запуск
Чтобы поиграть в игру необходмо запусить 3 скрипта  
* `server.py` - сервер приложения  
* `main.py` - командный центр полетов, где есть данные о летящей ракете  
* `nuclear_launch.py` - ракета с пилотом))

## Описание работы
Пилот( сторона запустившая `nuclear_launch.py`) должен вводить изменения скорости(по оси Х, оси У и вращения) в панель при помощи стрелок у поля с цифрами.  
Эти данные отправляются на сервер. Ракета не может разогнаться сразу, то есть скорость меняется с течением времени не так уж быстро(настраивается в файле `parametr.py`)  
Раз в несколько секунд обновляются данные о скорости и положении у диспетчера полетов (сторона запустившая  `main.py`) 
Стороны могут обмениваться сообщениями. При этом из-за экономии на обородовании, передача идет с небольшой задержкой(настраивается в файле `parametr.py`).
Цель игры достичь точки указанной у диспетчера ракетой, которой управляет пилот посредством комуникации между пилотом и диспетчером.  
Игра считается выигранной если кораблю пришел в необходимую точку и его скорость на тот момент равна нулю по всем составляющим(X, Y и вращение)

В интерфейсе у пилота и пункта управления есть кнопки меню, отвечающие за сохранение игры на сервере. В меню `Игра` имеются 2 кнопки: `Сохранить` и `Загрузить`.  
При сохранении и загрузке игра приостанваливается и продолжается либо загруженная игра(при успешной загрузке), либо текущая(при сохранении или какой-то ошибке).
На сервере только 1 сохранение, так что использовать надо его разумно!

В файле `parametr.py` можно менять
* максимальное изменнеие скорости за промежуток времени
* сам промежуток обновления
* границы случайно гененрирующихся начальных скоростей и положений
* задержку сообщений от командного пункта

## О содержании кода
На сервере имеется поток который по прошествии промежутка обновления изменяет скорость и текущаю координату.  
Скорость за 1 период обновления может измениться на ограниченную величину, значение которой прописно для каждой из скоростей в `parametr.py`
Так же на сервере под каждого клиента выделяется свой поток для получения сообщений.  

Остальные клиенты - так же имеют поток для получения асинхронных сообщений от сервера и главный поток приложения.  

Для обмена сообщениями используется класс `Message` расположенный в файле `model.py`, который для передачи по сокетам сериализуется json технологией.

