import os


def format_size(size_bytes: int) -> str:
    for unit in ['Б', 'КБ', 'МБ', 'ГБ', 'ТБ']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} ПБ"


def get_file_icon(extension: str) -> str:
    icons = {
        '.pdf': 'ДОК', '.doc': 'ДОК', '.docx': 'ДОК', '.odt': 'ДОК',
        '.txt': 'ТЕКСТ', '.log': 'ЛОГ', '.md': 'МД', '.rtf': 'РТФ',
        '.xls': 'ТБЛ', '.xlsx': 'ТБЛ', '.csv': 'ЦСВ', '.ods': 'ТБЛ',
        '.jpg': 'ФОТО', '.jpeg': 'ФОТО', '.png': 'ФОТО', '.gif': 'ГИФ', 
        '.bmp': 'ФОТО', '.svg': 'СВГ', '.ico': 'ИКО', '.webp': 'ФОТО',
        '.mp4': 'ВИДЕО', '.avi': 'ВИДЕО', '.mov': 'ВИДЕО', '.mkv': 'ВИДЕО', 
        '.wmv': 'ВИДЕО', '.flv': 'ВИДЕО', '.webm': 'ВИДЕО', '.m4v': 'ВИДЕО',
        '.mp3': 'АУДИО', '.wav': 'АУДИО', '.flac': 'АУДИО', '.aac': 'АУДИО', 
        '.ogg': 'АУДИО', '.wma': 'АУДИО', '.m4a': 'АУДИО',
        '.zip': 'АРХИВ', '.rar': 'АРХИВ', '.7z': 'АРХИВ', '.tar': 'АРХИВ', 
        '.gz': 'АРХИВ', '.bz2': 'АРХИВ', '.xz': 'АРХИВ', '.iso': 'ОБРАЗ',
        '.exe': 'ПРОГ', '.msi': 'ПРОГ', '.dll': 'ДЛЛ', '.app': 'ПРИЛ', 
        '.deb': 'ПАК', '.rpm': 'ПАК',
        '.py': 'ПИТОН', '.js': 'ДЖС', '.ts': 'ТС', '.html': 'ХТМЛ', 
        '.css': 'ЦСС', '.scss': 'СЦСС', '.java': 'ДЖАВА', '.cpp': 'СПП', 
        '.c': 'СИ', '.cs': 'ШАРП', '.php': 'ПХП', '.rb': 'РБ',
        '.go': 'ГО', '.rs': 'РАСТ', '.swift': 'СВИФТ', '.kt': 'КОТЛИН', 
        '.json': 'ДЖСОН', '.xml': 'ИКСМЛ', '.yaml': 'ЯМЛ', '.yml': 'ЯМЛ',
        '.db': 'БД', '.sql': 'СКЛ', '.sqlite': 'БД', '.mdb': 'БД',
        '.ttf': 'ШРИФТ', '.otf': 'ШРИФТ', '.woff': 'ШРИФТ',
        '.ppt': 'ПРЕЗ', '.pptx': 'ПРЕЗ', '.odp': 'ПРЕЗ',
    }
    return icons.get(extension.lower(), 'ФАЙЛ')


def get_file_info(file_path: str) -> dict:
    try:
        size = os.path.getsize(file_path)
        name = os.path.basename(file_path)
        extension = os.path.splitext(name)[1] or 'без расширения'
        
        return {
            'name': name,
            'size': size,
            'size_formatted': format_size(size),
            'path': file_path,
            'extension': extension,
            'icon': get_file_icon(extension)
        }
    except (OSError, PermissionError):
        return None


def validate_path(path: str) -> tuple[bool, str]:
    if not path:
        return False, 'Путь не указан'
    if not os.path.exists(path):
        return False, 'Путь не существует'
    return True, ''
