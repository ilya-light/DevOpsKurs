# DevOps docker-compose project

Проект поднимает ровно два сервиса:

- `app` — демонстрационное Flask-приложение из `https://github.com/moevm/devops-examples/tree/main/EXAMPLE_APP`;
- `tester` — контейнер для запуска тестов. PID 1 в контейнере — `python -m http.server 3000`, сервер стартует из `/workspace`.

## Что реализовано

1. Сборка обоих контейнеров из локальных Dockerfile:
   - `Dockerfile_app`
   - `Dockerfile_tester`
2. Базовый образ: `ubuntu:22.04`.
3. Зависимости apt и pip указаны с версиями.
4. Приложение скачивается из репозитория при сборке, затем файлы `EXAMPLE_APP` копируются в контейнер.
5. Исправления приложения оформлены patch-файлом: `patches/example_app.patch`.
6. Проверка HTML-бьютификации через `css-html-prettify`.
7. Статический анализ через `pylint`, включен только свой критерий: запрещено имя переменной, совпадающее с именем из `FORBIDDEN_VARIABLE_NAME`.
8. Интеграционные тесты через `requests`: проверяются HTTP-коды возврата.
9. SSH-доступ в `tester` по публичному ключу.
10. Логи каждого этапа пишутся одновременно:
    - в stdout/stderr контейнера, чтобы их было видно через `docker-compose logs tester`;
    - в отдельный файл в `/workspace/logs`.
11. Публичный порт веб-приложения передается через `.env`.
12. На оба контейнера задано ограничение памяти `510m`: `100 + 41 * 10 МБ`.

## Подготовка

Скопируйте пример env-файла:

```bash
cp .env.example .env
```

Положите существующий публичный ключ для SSH-доступа в `tester`:

```bash
cp ~/.ssh/id_ed25519.pub ssh/authorized_keys
```

Если у вас другой ключ, укажите путь к нему вместо `~/.ssh/id_ed25519.pub`.

## Сборка

```bash
docker-compose build
```

## Запуск контейнеров

```bash
docker-compose up -d
```

Проверить, что веб-приложение доступно на публичном порту из `.env`:

```bash
curl -i http://127.0.0.1:8080/
```

## Запуск всех тестов

```bash
docker-compose exec tester bash /workspace/tests/scripts/run_all.sh
```

## Запуск отдельных этапов

HTML-бьютификация:

```bash
docker-compose exec tester bash /workspace/tests/scripts/run_beautify.sh
```

Статический анализ с кастомным правилом pylint:

```bash
docker-compose exec tester bash /workspace/tests/scripts/run_lint.sh
```

Интеграционные тесты кодов возврата:

```bash
docker-compose exec tester bash /workspace/tests/scripts/run_integration.sh
```

## Проверка логов

Логи через docker-compose:

```bash
docker-compose logs tester
```

Файлы логов внутри tester:

```bash
docker-compose exec tester ls -la /workspace/logs
docker-compose exec tester cat /workspace/logs/01_beautify_html.log
docker-compose exec tester cat /workspace/logs/02_pylint_custom.log
docker-compose exec tester cat /workspace/logs/03_integration_status_codes.log
```

## SSH в tester

Порт задается в `.env` переменной `TESTER_SSH_PUBLIC_PORT`.

```bash
ssh -i ~/.ssh/id_ed25519 -p 2222 tester@127.0.0.1
```

## Изменение публичного порта app

В `.env` поменяйте:

```env
WEB_PUBLIC_PORT=8081
```

Затем пересоздайте контейнеры:

```bash
docker-compose up -d --force-recreate
```

После этого приложение будет доступно так:

```bash
curl -i http://127.0.0.1:8081/
```

## Как проверить кастомный pylint-критерий

По умолчанию запрещено имя переменной `ivan`:

```env
FORBIDDEN_VARIABLE_NAME=ivan
```

Можно указать несколько вариантов через запятую:

```env
FORBIDDEN_VARIABLE_NAME=ivan,иван
```

Для демонстрации ошибки создайте временный файл внутри tester:

```bash
docker-compose exec tester bash -lc 'echo "ivan = 1" > /workspace/app/bad_name_demo.py'
docker-compose exec tester bash /workspace/tests/scripts/run_lint.sh
```

После проверки удалите временный файл:

```bash
docker-compose exec tester rm /workspace/app/bad_name_demo.py
```

## Остановка

```bash
docker-compose down -v
```
