# Аналитика Данных - Wow-like система мониторинга данных

**Автор:** Жизнев Вадим Евгеньевич
**Группа:** Б9123-09.03.04

---

## Структура базы данных

### Таблица `players`

| Поле | Тип | Описание |
|------|-----|----------|
| `id` | bigint | Автоматическое приращение |
| `name` | varchar | Имя игрока |
| `guild` | varchar | Гильдия |
| `pvp_rating` | float | PvP рейтинг |

### Таблица `game_events`

| Поле | Тип | Описание |
|------|-----|----------|
| `id` | bigint | Автоматическое приращение |
| `player_id` | bigint | ID игрока (FK на players.id) |
| `points` | integer | Очки за событие |
| `item_rarity` | varchar | Редкость предмета (Common, Rare, Epic) |
| `created_at` | timestamptz | Время события |

---

## Как запустить

Не забудьте скачать Docker или Podman, а так же task для удобства

### 1. Настройка переменных окружения

Создайте файл `.env` в корне проекта на основе `.env.example`:

```env
POSTGRESQL_DATABASE=main_db
POSTGRESQL_USERNAME=wow_user
POSTGRESQL_PASSWORD=wow_pass

REDASH_DATABASE_URL=postgresql://wow_user:wow_pass@postgres:5432/main_db
REDASH_REDIS_URL=redis://redis:6379
REDASH_COOKIE_SECRET=very_secret
```

### 3. Запуск сервисов

Используйте Task runner для удобства:

```bash
# Запуск всех сервисов кроме jupyter
task up-without-jupyter

# Или запуск всех
task up-all

# Или только jupyter (после запуска остальных)
task up-jupyter
```

Или напрямую Docker Compose:

```bash
docker-compose -f jocker-compose.yml up
```

### 4. Доступ

- **Redash**: http://localhost:80 через nginx
- **Jupyter Notebook**: http://localhost:8888 (если запущен) либо через vscode подключить kernel, так же есть возможность локально через uv sync
- **PostgreSQL**: localhost:5432

### 5. Аналитика в Jupyter

Откройте `analytics.ipynb` в Jupyter. Код подключается к БД и строит графики.

---

## Визуализации в Redash

![Скриншот 1](./screenshots/screenshot1.jpg)
![Скриншот 2](./screenshots/screenshot2.jpg)
![Скриншот 3](./screenshots/screenshot3.jpg)
![Скриншот 4](./screenshots/screenshot4.jpg)

---

## Структура проекта

- `src/generator/` - генератор данных
- `analytics.ipynb` - Jupyter notebook для анализа
- `jocker-compose.yml` - Docker Compose конфиг
- `Taskfile.yml` - Задачи для запуска
- `Dockerfile` - Образ для Jupyter
