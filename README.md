#Микросервис для intrealt.com

## Содержание
- [Установка](#установка)
- [Использование](#использование)

## Установка
1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/Gretsir12/jp-property.git
   cd jp-property
   ```

2. Создайте виртуальное окружение python и установите все нужные бибилотеки
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    pip install -r req.txt
    ```

3. Создайте базу данных (перед этим убедитесь что у вас установлен MongoDB compass) На первый запуск потребуется около 20 минут
    ```bash
    python refresh.py
    ```

4. Запустите приложение
    ```bash
    uvicorn main:app --reload
    ```

  ## Использование
  1. если вам надо обновить базу данныхЖ
  ```bash 
  python refresh.py
  ```

  2. Запуск приложения
  ```bash 
  uvicorn main:app --reload
  ```

  3. Получение XML фида

Фид выдается в "/feed" по адресу вашего бекенда (если вы тестируете локально, то адрес вам выведут в терминал при запуске приложения)