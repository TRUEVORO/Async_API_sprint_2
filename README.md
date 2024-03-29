# Проектная работа 5 спринта

В папке **tasks** ваша команда найдёт задачи, которые необходимо выполнить во втором спринте модуля "Сервис Async API".

Как и в прошлом спринте, мы оценили задачи в стори поинтах.

Вы можете разбить эти задачи на более маленькие, например, распределять между участниками команды не большие куски задания, а маленькие подзадачи. В таком случае не забудьте зафиксировать изменения в issues в репозитории.

**От каждого разработчика ожидается выполнение минимум 40% от общего числа стори поинтов в спринте.**

## Ссылки на спринты:

- [Async_API_sprint_1](https://github.com/TRUEVORO/Async_API_sprint_1)
- [Async_API_sprint_2](https://github.com/TRUEVORO/Async_API_sprint_2)
- [new_admin_panel_sprint_2](https://github.com/TRUEVORO/new_admin_panel_sprint_2)

## Для запуска сервисов необходимо:

### 1. Создать .env на основе .env.template
### 2. Запустить movies_admin [ссылка на второй спринт](https://github.com/TRUEVORO/new_admin_panel_sprint_2)
```
make movies_admin
```
### 3. Запустить etl и fastapi
```
make run
```

## Для запуска тестов необходимо:

### 1. Запустить тесты
```
make test
```
