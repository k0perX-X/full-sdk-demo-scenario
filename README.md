# Full SDK Demo Scenario

Пример отдельного подпроекта сценария для оркестратора.

Цель:
- показать минимальную структуру внешнего git-репозитория сценария
- продемонстрировать весь актуальный публичный API `orchestrator-sdk`
- дать готовый `algorithm_path` для регистрации сценария в оркестраторе

## Структура

```text
full-sdk-demo-scenario/
├── README.md
├── requirements.txt
└── scenario.py
```

## Как использовать

1. Установить SDK:

```bash
pip install -r requirements.txt
```

Для локальной разработки внутри монорепозитория можно временно заменить строку в `requirements.txt` на:

```text
-e ../../sdk
```

2. Зарегистрировать сценарий в оркестраторе:

- `git_url`:
  URL git-репозитория, в котором лежит этот подпроект
- `version`:
  ветка или тег, который должен checkout'ить worker
- `algorithm_path`:
  `scenario.py`

3. Передать во входных данных сценария, например:

```json
{
  "task_description": "hello from scenario",
  "child_prompt": "child hello world",
  "cancel_prompt": "cancel me"
}
```

## Что показывает пример

- `sdk.log(...)`
- `sdk.generate(...)`
- `sdk.create_request(...)`
- `sdk.get_request_status(...)`
- `sdk.wait_for_completion(...)`
- `sdk.cancel_request(...)`
- `sdk.emit_metric(...)`
