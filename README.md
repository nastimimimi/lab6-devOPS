# lab6-devOPS

# Модель: Автоматизоване складання розкладу занять — Генетичний алгоритм (5 семестр)

# Автор: Баранова Анастасія, група АІ-231

# ЛР5–ЛР6: Flask API + CI/CD Pipeline

## Структура проєкту
```
lab6/
├── app.py                        # Flask API (ЛР5)
├── test_app.py                   # pytest тести (ЛР6)
├── requirements.txt              # залежності
├── Dockerfile                    # контейнеризація
├── README.md
└── .github/
    └── workflows/
        └── ci.yml                # GitHub Actions pipeline
```

## CI/CD Pipeline — етапи
| Етап | Опис |
|------|------|
|  Install dependencies | `pip install -r requirements.txt` |
|  Syntax check | `python -m py_compile app.py` |
|  Run tests (pytest) | `pytest test_app.py -v` |
|  Build Docker image | `docker build -t schedule-optimizer .` |

## Запуск локально
```bash
pip install -r requirements.txt
python app.py
```

## Запуск тестів локально
```bash
pip install pytest
pytest test_app.py -v
```

## Тестовий запит
```powershell
Invoke-WebRequest -Uri "http://127.0.0.1:5000/calculate" `
  -Method POST `
  -ContentType "application/json" `
  -Body '{}'
```
