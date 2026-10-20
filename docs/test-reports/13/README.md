\# Автоматизация UI на Playwright



\## Версия продукта и параметры среды



| Параметр | Значение |

|---|---|

| Ветка продукта | `client-server/fixed` |

| Архитектура / состояние | `client-server` / `fixed` |

| Контракт | 1.0.0 |

| Git SHA продукта | c43590b01934caeddaa1fa2798566ede7e92d016 |

| Адрес UI | http://localhost:8231 |

| PostgreSQL | 127.0.0.1:55571 |

| Compose-проект | mini-student-131 |

| Браузер | Chromium (Playwright chromium 1208, Chrome for Testing 145.0.7632.6) |

| Viewport | desktop 1440×900, compact 390×844 |

| Ветка тестов | practice/13-ui-playwright |



\## Сценарии и требования



| ID | Требование | Действие UI | Ожидание |

|---|---|---|---|

| P13-UI-01 | UI-01, TICKET-03 | вход и создание заявки | сообщение, карточка, строка списка и API согласованы |

| P13-UI-02 | UI-02, TICKET-03 | открыть карточку и выбрать high | карточка и строка списка показывают high без reload |



\## Граница API-подготовки и UI-проверки



\- API создаёт уникального пользователя и заявку-предусловие через `PreparedUser.register` и `PreparedUser.create\_ticket`.

\- UI проверяет само действие и наблюдаемое состояние (карточка, строка таблицы, сообщение).

\- API-проверка в конце подтверждает сохранение данных через `PreparedUser.get\_ticket`.



\## Структура Page Object



\- `LoginPage` — heading, email, password, submit + методы `open`, `login`.

\- `TicketsPage` — heading, table, status\_message, форма, карточка + методы `ticket\_row`, `create\_ticket`, `open\_ticket`, `change\_priority`, `selected\_title`, `selected\_priority`, `row\_priority`.

\- `PreparedUser` — API-регистрация, токен, создание заявки, `get\_ticket`, `cleanup`.

\- Тест — сценарий и assertions.



\## Выбор инструмента



Выбран \*\*Playwright\*\*: auto-wait, встроенные трейсы, браузерные контексты.

\- \*\*Selenium WebDriver\*\* — зрелая экосистема, но синхронизация вручную.

\- \*\*Cypress\*\* — удобен для JS/TS, ограничен по браузерам.

\- \*\*Appium\*\* — для мобильных, здесь не нужен.



Page Object используется обычный, без Selenium Page Factory. Page Factory не нужен Playwright.



\## Карта устойчивых локаторов



| Элемент | Локатор |

|---|---|

| Заголовок входа | `get\_by\_role("heading", name="Вход в систему")` |

| Email | `get\_by\_label("Email", exact=True)` |

| Пароль | `get\_by\_label("Пароль", exact=True)` |

| Войти | `get\_by\_role("button", name="Войти", exact=True)` |

| Таблица заявок | `get\_by\_role("table", name="Список заявок")` |

| Сообщение результата | `get\_by\_role("status")` |

| Заголовок новой заявки | `get\_by\_label("Заголовок новой заявки")` |

| Приоритет новой заявки | `get\_by\_label("Приоритет новой заявки")` |

| Создать заявку | `get\_by\_role("button", name="Создать заявку", exact=True)` |

| Карточка заявки | `get\_by\_role("complementary", name="Карточка заявки")` |

| Строка заявки | `get\_by\_test\_id("ticket-<uuid>")` |

| Приоритет в строке | `row.get\_by\_test\_id("ticket-priority")` |

| Заголовок в карточке | `card.get\_by\_label("Заголовок заявки")` |

| Приоритет в карточке | `card.get\_by\_label("Приоритет заявки")` |

| Сохранить изменения | `card.get\_by\_role("button", name="Сохранить изменения", exact=True)` |



\## Ожидания и синхронизация



\- `goto` → `expect(login.heading).to\_be\_visible()`

\- submit → `expect(tickets.heading)` и `expect(tickets.table).to\_be\_visible()`

\- создание → `expect(status\_message).to\_have\_text("Заявка создана")`

\- открытие → `expect(card).to\_be\_visible()` и `to\_have\_value(title)`

\- сохранение → `expect(status\_message).to\_have\_text("Изменения сохранены")` и `expect(row\_priority).to\_have\_text("Высокий")`



\## Сценарий создания заявки



1\. Регистрация пользователя через API (`PreparedUser.register`).

2\. UI: открыть адрес, войти.

3\. UI: заполнить заголовок и приоритет, нажать «Создать заявку».

4\. Проверить сообщение, карточку, строку списка.

5\. API: `GET /tickets/{id}` подтверждает title/priority/status.

6\. Cleanup: `DELETE /tickets/{id}` для всех заявок пользователя.



\## Сценарий обновления приоритета



1\. API: создать пользователя и заявку с `priority=low`.

2\. UI: войти, найти строку по `ticket-<uuid>`, открыть карточку.

3\. UI: изменить приоритет на `high`, сохранить.

4\. Проверить сообщение, приоритет в карточке, приоритет в строке.

5\. API: `GET /tickets/{id}` возвращает `priority=high`.

6\. Cleanup: `DELETE /tickets/{id}`.



\## Desktop- и compact-результаты



| Сценарий | Desktop | Compact |

|---|---|---|

| Создание заявки | PASSED | PASSED |

| Синхронизация приоритета | PASSED | PASSED |



\## Повторный запуск и очистка данных



\- Каждый запуск создаёт уникального пользователя (`p13-<uuid>@example.test`).

\- Каждый сценарий создаёт новую заявку с уникальным title.

\- Cleanup удаляет все заявки пользователя через API.

\- Повторный запуск дал тот же результат: 4 passed.



\## Screenshot и trace при падении



Флаги: `--screenshot=only-on-failure`, `--tracing=retain-on-failure`, `--output=artifacts/practice-13`.



В текущем прогоне падений нет, артефакты не созданы. При реальном падении:

\- `trace.zip` — открыть через `playwright show-trace`,

\- `screenshot.png` — последний кадр.



\## Итоговый вывод и остаточные риски



\- 4 из 4 UI-тестов прошли на `client-server/fixed` в обоих viewport.

\- API-подготовка изолирована от UI-действий.

\- Локаторы через роли и `data-testid` устойчивы к изменению вёрстки.

\- Остаточные риски: не проверены состояния active/closed в UI, нет кросс-браузерных запусков (только chromium), UI-тесты не покрывают вход оператора.

