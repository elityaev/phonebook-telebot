# phonebook-telebot

### Описание

Телеграм бот - телефонный справочник поддерживающий следующие 
операции:
 * создание контакта (имя, фамилия, номер телефона);
 
https://user-images.githubusercontent.com/92791325/224549207-24c41d4a-93d1-4627-8352-96399c1d415c.mp4
 
 * показ всех имеющихся записей;
 * при выборе записи из общего списка открывается 
карточка контакта в которой указаны все телефоны, 
принадлежащие контакту, а также кнопки с выбором действия:
    * добавить номер телефона;
    * удалить контакт;
    * возможно редактирование характеристики контакта при 
    нажатии на соответствующую кнопку(имя, фамилия, один из 
    номеров);
 
 https://user-images.githubusercontent.com/92791325/224549593-31507c94-9fe2-4672-9e18-5e358e5589d1.mp4
    
 * поиск записи по имени или фамилии.

### Технологии

* Python
* pyTelegramBotAPI

### Запуск

1. Клонировать проект, создать и активировать виртуальное окружение, установить
зависимости

Для Windows:

```shell
git clone git@github.com:elityaev/phonebook-telebot.git
cd phonebook-telebot
python -m venv venv
venv/Scripts/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```
Для Linux:

```shell
git clone git@github.com:elityaev/phonebook-telebot.git
cd phonebook-telebot
python3 -m venv venv
source venv/bin/activat
python -m pip install --upgrade pip
pip install -r requirements.txt
```

2. Cкопировать файл .env.example и назвать его .env, указать значение вашего
TELEGRAM_TOKEN 
([создание телеграм бота и получение токена](https://t.me/botfather))
3. Запустить бота 
```shell
python bot.py
```
4. Активировать бота командой `/start`

Автор
Литяев Евгений
