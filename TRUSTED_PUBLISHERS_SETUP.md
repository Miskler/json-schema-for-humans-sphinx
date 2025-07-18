# Настройка Trusted Publishers для PyPI

## Что такое Trusted Publishers?

Trusted Publishers - это современный и безопасный способ публикации пакетов на PyPI без использования API токенов. Вместо хранения секретных токенов в GitHub, PyPI доверяет определенным GitHub Actions workflows.

## Преимущества над API токенами:

1. **Безопасность**: Нет секретных токенов для хранения и управления
2. **Автоматизация**: Настройка один раз, работает всегда
3. **Аудит**: Лучшая отслеживаемость публикаций
4. **Отзывчивость**: Легко отозвать доступ при необходимости

## Настройка Trusted Publishers

### 1. Настройка на PyPI

1. Зайдите на [pypi.org](https://pypi.org) и войдите в свой аккаунт
2. Перейдите в раздел "Publishing" в настройках вашего проекта
3. Нажмите "Add a new pending publisher"
4. Заполните следующие поля:
   - **PyPI Project Name**: `jsoncrack-for-sphinx`
   - **Owner**: `miskler` (ваш GitHub username)
   - **Repository name**: `json-schema-for-humans-sphinx`
   - **Workflow filename**: `publish.yml`
   - **Environment name**: `release` (опционально)

### 2. Настройка на Test PyPI (опционально)

Если хотите также использовать Test PyPI:

1. Зайдите на [test.pypi.org](https://test.pypi.org)
2. Повторите те же шаги для тестового окружения
3. Используйте Environment name: `test`

### 3. Проверка workflow

Ваш workflow уже настроен для использования Trusted Publishers:

```yaml
# Trust publishers permissions
permissions:
  id-token: write
  contents: read

- name: Publish to PyPI
  uses: pypa/gh-action-pypi-publish@release/v1
```

## Использование

### Автоматическая публикация при релизе

1. Создайте release в GitHub
2. Workflow автоматически соберет и опубликует пакет на PyPI

### Ручная публикация

1. Перейдите в Actions в вашем репозитории
2. Выберите "Publish to PyPI" workflow
3. Нажмите "Run workflow"
4. Выберите окружение: `release` или `test`
5. Нажмите "Run workflow"

## Безопасность

- Не нужно создавать или хранить API токены
- PyPI автоматически верифицирует, что публикация происходит из правильного репозитория
- Все публикации автоматически привязаны к конкретному коммиту и пользователю

## Что было удалено

- ❌ Dependabot (автоматические обновления зависимостей)
- ❌ Секретные токены (`PYPI_API_TOKEN`, `TEST_PYPI_API_TOKEN`)
- ❌ Ручная конфигурация twine с токенами

## Что добавлено

- ✅ Trusted Publishers конфигурация
- ✅ Современный pypa/gh-action-pypi-publish action
- ✅ Правильные permissions для id-token
