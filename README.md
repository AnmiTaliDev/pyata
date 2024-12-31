# PyATA - AnmiTali Archive

**Created:** 2024-12-31 10:52:44 UTC  
**Author:** AnmiTaliDev  
**Version:** 1.0.0  
**License:** GPL 3

PyATA - это современный архиватор с поддержкой сжатия, написанный на Python.

## Особенности

- Быстрое сжатие с помощью zstd
- Сохранение метаданных файлов (время создания/изменения)
- Проверка целостности через SHA256
- Удобный командный интерфейс
- Поддержка больших файлов
- Подробный режим вывода

## Установка

```bash
# Из PyPI
pip install pyata

# Из исходного кода
git clone https://github.com/AnmiTaliDev/pyata.git
cd pyata
pip install .
```

## Использование

### Создание архива

```bash
# Базовое использование
pyata create archive.ata file1.txt file2.txt

# С максимальным сжатием
pyata create archive.ata file1.txt -c zstd -l 19

# Подробный вывод
pyata create archive.ata file1.txt -v
```

### Извлечение файлов

```bash
# Извлечь все файлы
pyata extract archive.ata

# С подробным выводом
pyata extract archive.ata -v
```

### Просмотр содержимого

```bash
# Простой список файлов
pyata list archive.ata

# Подробная информация
pyata list archive.ata -v
```

## Формат архива

```
HEADER
- Magic (4 bytes): "ATA1"
- Version (1 byte)
- Number of files (4 bytes)

FILE ENTRY
- Filename length (2 bytes)
- Creation time (8 bytes)
- Modified time (8 bytes)
- Original size (8 bytes)
- Compressed size (8 bytes)
- SHA256 hash (32 bytes)
- Filename (variable)
- File data (compressed)
```

## Требования

- Python 3.6+
- zstandard
- click

## Разработка

```bash
# Установка зависимостей для разработки
pip install -e ".[dev]"

# Запуск тестов
pytest

# Сборка документации
cd docs
make html
```

## Лицензия

Распространяется под лицензией GPL 3. Смотрите файл `LICENSE` для получения подробной информации.

## Автор

AnmiTaliDev (<anmitali@anmitali.kz>)

## Участие в разработке

1. Создайте форк репозитория
2. Создайте ветку для вашей функции (`git checkout -b feature/amazing_feature`)
3. Зафиксируйте изменения (`git commit -am 'Add amazing feature'`)
4. Отправьте изменения в ваш форк (`git push origin feature/amazing_feature`)
5. Создайте Pull Request