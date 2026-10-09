\# Исследование фильтра через DevTools Network



\## Действие



Открыть http://localhost:8192 в Chrome, войти как seed-пользователь, выбрать фильтр «Новая».



\## Наблюдение



\- Метод и URL: `GET /api/tickets?status=new`

\- Код: `200`

\- X-Request-ID: создан Nginx, ответ возвращает его в header

\- Статусы объектов в Response: `new`, `active` (при активной категории D05)



\## Связь с логами



Тот же X-Request-ID находится в `docker compose -p mini-student-92 logs web`

и в `/app/logs/all.log` внутри контейнера app.



\## Сравнение с fixed



На `http://localhost:8191` тот же фильтр возвращает только `new`.



\## Вывод



Серверный ответ нарушает TICKET-05.

