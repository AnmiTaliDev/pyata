# -*- coding: utf-8 -*-

"""
AnmiTali Archive (ATA) - Modern Terminal Archiver
Created: 2024-12-31 10:51:42 UTC
Author: AnmiTaliDev
Version: 1.0.0
License: GPL

A modern terminal archiver with compression support.
"""

from .ata import ATAArchive, ATAError, ATAFormatError, ATACompressionError
from .ata import cli, create, extract, list

__version__ = "1.0.0"
__author__ = "AnmiTaliDev"
__email__ = "anmitali@anmitali.kz"
__license__ = "GPL"
__created__ = "2024-12-31 10:51:42 UTC"

__all__ = [
    'ATAArchive',
    'ATAError',
    'ATAFormatError',
    'ATACompressionError',
    'cli',
    'create',
    'extract',
    'list',
]

# Основные команды
COMMANDS = {
    'create': 'Создать новый архив',
    'extract': 'Извлечь содержимое архива',
    'list': 'Показать содержимое архива'
}

# Поддерживаемые методы сжатия
COMPRESSION_METHODS = ['zstd', 'none']

# Значения по умолчанию
DEFAULT_COMPRESSION = 'zstd'
DEFAULT_LEVEL = 3

# Формат архива
ARCHIVE_VERSION = 1
ARCHIVE_EXTENSION = '.ata'