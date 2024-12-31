#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AnmiTali Archive (ATA) - Modern Terminal Archiver
Created: 2024-12-31 10:49:54 UTC
Author: AnmiTaliDev
Version: 1.0.0
License: GPL
"""

import os
import sys
import time
import struct
import hashlib
import logging
import zstandard as zstd
import click
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, BinaryIO

# Константы
MAGIC = b"ATA1"
VERSION = 1
HEADER_FORMAT = "<4sBI"  # Magic (4 bytes) + Version (1 byte) + Number of files (4 bytes)
FILE_HEADER_FORMAT = "<H8s8sQQ32s"  # name_len(2) + created(8) + modified(8) + orig_size(8) + comp_size(8) + sha256(32)
BUFFER_SIZE = 1024 * 1024  # 1MB для чтения больших файлов
COMPRESSION_METHODS = ['zstd', 'none']
DEFAULT_COMPRESSION = 'zstd'
DEFAULT_LEVEL = 3

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)

class ATAError(Exception):
    """Базовый класс для ошибок ATA"""
    pass

class ATAFormatError(ATAError):
    """Ошибка формата архива"""
    pass

class ATACompressionError(ATAError):
    """Ошибка сжатия/распаковки"""
    pass

class ATAArchive:
    def __init__(self, filename: str, compression: str = DEFAULT_COMPRESSION, level: int = DEFAULT_LEVEL, verbose: bool = False):
        self.filename = filename
        self.compression = compression
        self.level = level
        self.verbose = verbose

    def _log(self, message: str) -> None:
        """Логирование сообщений"""
        if self.verbose:
            logger.info(message)

    def _calculate_sha256(self, data: bytes) -> bytes:
        """Вычисление SHA256 хеша данных"""
        return hashlib.sha256(data).digest()

    def _compress_data(self, data: bytes) -> bytes:
        """Сжатие данных"""
        try:
            if self.compression == 'zstd':
                return zstd.ZstdCompressor(level=self.level).compress(data)
            return data
        except zstd.ZstdError as e:
            raise ATACompressionError(f"Ошибка сжатия: {e}")

    def _decompress_data(self, data: bytes) -> bytes:
        """Распаковка данных"""
        try:
            return zstd.ZstdDecompressor().decompress(data)
        except zstd.ZstdError:
            return data

    def create(self, files: List[str]) -> None:
        """Создание архива"""
        if not (valid_files := [f for f in files if os.path.exists(f)]):
            raise ATAError("Нет файлов для архивации")

        with open(self.filename, 'wb') as archive:
            self._log(f"Создание архива: {self.filename}")
            archive.write(struct.pack(HEADER_FORMAT, MAGIC, VERSION, len(valid_files)))
            
            for file_path in valid_files:
                self._log(f"Добавление: {file_path}")
                with open(file_path, 'rb') as f:
                    data = f.read()
                
                compressed = self._compress_data(data)
                name_bytes = os.path.basename(file_path).encode('utf-8')
                if len(name_bytes) > 65535:
                    raise ATAError(f"Слишком длинное имя: {file_path}")
                
                stat = os.stat(file_path)
                header = struct.pack(FILE_HEADER_FORMAT,
                    len(name_bytes),
                    int(stat.st_ctime).to_bytes(8, 'little'),
                    int(stat.st_mtime).to_bytes(8, 'little'),
                    len(data),
                    len(compressed),
                    self._calculate_sha256(data)
                )
                
                archive.write(header)
                archive.write(name_bytes)
                archive.write(compressed)

    def extract(self) -> None:
        """Извлечение архива"""
        extract_dir = os.path.splitext(self.filename)[0]
        os.makedirs(extract_dir, exist_ok=True)
        self._log(f"Извлечение в: {extract_dir}")

        with open(self.filename, 'rb') as archive:
            magic, version, num_files = struct.unpack(HEADER_FORMAT, archive.read(9))
            if magic != MAGIC or version != VERSION:
                raise ATAFormatError("Неверный формат архива")

            for _ in range(num_files):
                name_len, ctime, mtime, orig_size, comp_size, orig_sha256 = struct.unpack(FILE_HEADER_FORMAT, archive.read(66))
                filename = archive.read(name_len).decode('utf-8')
                compressed = archive.read(comp_size)
                
                self._log(f"Извлечение: {filename}")
                data = self._decompress_data(compressed)
                
                if self._calculate_sha256(data) != orig_sha256:
                    raise ATAError(f"Ошибка контрольной суммы: {filename}")
                
                out_path = os.path.join(extract_dir, filename)
                with open(out_path, 'wb') as f:
                    f.write(data)
                os.utime(out_path, (int.from_bytes(ctime, 'little'), int.from_bytes(mtime, 'little')))

    def list(self) -> None:
        """Просмотр содержимого архива"""
        with open(self.filename, 'rb') as archive:
            magic, version, num_files = struct.unpack(HEADER_FORMAT, archive.read(9))
            if magic != MAGIC or version != VERSION:
                raise ATAFormatError("Неверный формат архива")

            print(f"Файлов в архиве: {num_files}")
            for _ in range(num_files):
                name_len, ctime, mtime, orig_size, comp_size, _ = struct.unpack(FILE_HEADER_FORMAT, archive.read(66))
                filename = archive.read(name_len).decode('utf-8')
                archive.seek(comp_size, 1)
                
                if self.verbose:
                    created = datetime.fromtimestamp(int.from_bytes(ctime, 'little'))
                    modified = datetime.fromtimestamp(int.from_bytes(mtime, 'little'))
                    ratio = (1 - comp_size/orig_size) * 100 if orig_size > 0 else 0
                    print(f"{filename}:")
                    print(f"  Создан: {created}")
                    print(f"  Изменен: {modified}")
                    print(f"  Размер: {orig_size} байт")
                    print(f"  Сжатый размер: {comp_size} байт")
                    print(f"  Степень сжатия: {ratio:.1f}%")
                else:
                    print(filename)

@click.group()
def cli():
    """AnmiTali Archive - Modern Terminal Archiver"""
    pass

@cli.command()
@click.argument('archive_name')
@click.argument('files', nargs=-1, required=True)
@click.option('-c', '--compression', type=click.Choice(COMPRESSION_METHODS), default=DEFAULT_COMPRESSION)
@click.option('-l', '--level', type=int, default=DEFAULT_LEVEL)
@click.option('-v', '--verbose', is_flag=True)
def create(archive_name, files, compression, level, verbose):
    """Создать новый архив"""
    try:
        ATAArchive(archive_name, compression, level, verbose).create(files)
    except Exception as e:
        logger.error(f"Ошибка: {e}")
        sys.exit(1)

@cli.command()
@click.argument('archive_name')
@click.option('-v', '--verbose', is_flag=True)
def extract(archive_name, verbose):
    """Извлечь содержимое архива"""
    try:
        ATAArchive(archive_name, verbose=verbose).extract()
    except Exception as e:
        logger.error(f"Ошибка: {e}")
        sys.exit(1)

@cli.command()
@click.argument('archive_name')
@click.option('-v', '--verbose', is_flag=True)
def list(archive_name, verbose):
    """Показать содержимое архива"""
    try:
        ATAArchive(archive_name, verbose=verbose).list()
    except Exception as e:
        logger.error(f"Ошибка: {e}")
        sys.exit(1)

if __name__ == '__main__':
    cli()