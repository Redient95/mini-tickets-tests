\# Результат client-server/buggy



\## Координаты среды



\- Ветка: `client-server/buggy`

\- Git SHA: `92bbb1b7287f199574ff6bad41dbcbfcdedd7711`

\- BASE\_URL: `http://localhost:8192`

\- PostgreSQL: `localhost:55532`

\- Compose-проект: `mini-student-92`

\- LAB\_DEFECTS: `all`



\## Команда запуска



```powershell

$env:BASE\_URL = 'http://localhost:8192'

.\\.venv\\Scripts\\python.exe -m pytest tests/api -m api -vv --tb=short `

&#x20;   --junitxml=docs/test-reports/09/buggy-junit.xml

