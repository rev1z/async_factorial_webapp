# async_factorial_webapp
Пример веб-приложения на aiohttp, с фоновым процессом для вычисления факториала.
Фоновый процесс пишет в результат вычисления в stdout.
При запросе, отдаётся текущее значения факториала, на момент запроса, из stdout фонового процесса.

Используется:

    python 3.6+
    asyncio
    subprocess
    aiohttp
    aiohttp-jinja2
    jinja2

запуск в виртуальном окружении:

    python3.6 -m venv env
    source env/bin/activate
    pip install -r requirements.txt
    python main.py
 
в докере:

    docker-compose up --build
    
У этого метода есть проблемы с производительностью,
по сравнению с запуском в виртуальном окружении.
запрос к фоновому процессу очень долгий, если сравнивать с запуском в виртуальном окружении.

   
Я пока в поиске решения.
Есть мнение что subprocess и докер нужно как-то,по-особому, дружить.


