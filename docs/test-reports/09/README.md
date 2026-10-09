\# API-тесты на Python и диагностика ошибок



\## Версии продукта и адреса сред



| Среда | URL | SHA | Compose-проект |

|---|---|---|---|

| client-server/fixed | http://localhost:8191 | c43590b01934caeddaa1fa2798566ede7e92d016 | mini-student-91 |

| client-server/buggy | http://localhost:8192 | 92bbb1b7287f199574ff6bad41dbcbfcdedd7711 | mini-student-92 |



\## Версии



\- Python 3.13.13

\- Pytest 8.3.5

\- Requests 2.34.2



\## Команда запуска



```powershell

$env:BASE\_URL = 'http://localhost:8191'  # или 8192

.\\.venv\\Scripts\\python.exe -m pytest tests/api -m api -vv --tb=short

