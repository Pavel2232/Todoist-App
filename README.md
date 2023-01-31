# todolist_app
приложения для управления персональными и рабочими задачами.

стек (python3.9, Django, Postgres) Для начала работы скопируйте репозиторий на локальную машину: c помощью команды в терминале

https://github.com/Pavel2232/app_by_django

Откройте склонированный репозиторий в PyCharm.
активируйте poetry install 

заполнить файл .env на примере .env.example
можете использовать такие значения как:
      POSTGRES_USER: test
      POSTGRES_PASSWORD: test
      POSTGRES_DB: test
для заполнения тестовой бд.

соберите контейнер postgres командой
docker-compose up -d
или же подключитесь к своей чистой базе

накатите миграции и запустите приложение
