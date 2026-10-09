\# Результат client-server/fixed



\## Координаты среды



\- Ветка: `client-server/fixed`

\- Git SHA: `c43590b01934caeddaa1fa2798566ede7e92d016`

\- BASE\_URL: `http://localhost:8191`

\- PostgreSQL: `localhost:55531`

\- Compose-проект: `mini-student-91`



\## Версии



\- Python: 3.13.13

\- Pytest: 8.3.5

\- Requests: 2.34.2



\## Команда запуска



```powershell

$env:BASE\_URL = 'http://localhost:8191'

.\\.venv\\Scripts\\python.exe -m pytest tests/api -m api -vv --tb=short `

&#x20;   --junitxml=docs/test-reports/09/fixed-junit.xml

