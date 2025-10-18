import os
from PyQt6.QtCore import QThread, pyqtSignal
from ..utils.file_utils import get_file_info


class FileAnalyzer(QThread):
    progress = pyqtSignal(int)
    file_found = pyqtSignal(dict)
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)
    
    def __init__(self, path: str, is_folder: bool = True):
        super().__init__()
        self.path = path
        self.is_folder = is_folder
        self.files_data = []
        self.total_size = 0
        self._is_cancelled = False
        
    def run(self):
        try:
            if self.is_folder:
                self._analyze_folder()
            else:
                self._analyze_file()
        except Exception as e:
            self.error.emit(f'Ошибка анализа: {str(e)}')
            
    def cancel(self):
        self._is_cancelled = True
    
    def _analyze_file(self):
        info = get_file_info(self.path)
        if info:
            self.files_data.append(info)
            self.total_size = info['size']
            self.file_found.emit(info)
        self._emit_results()
    
    def _analyze_folder(self):
        all_files = self._collect_files()
        
        if self._is_cancelled:
            return
        
        total_files = len(all_files)
        if total_files == 0:
            self._emit_results()
            return
        
        for idx, file_path in enumerate(all_files):
            if self._is_cancelled:
                break
                
            info = get_file_info(file_path)
            if info:
                self.files_data.append(info)
                self.total_size += info['size']
                self.file_found.emit(info)
                
            progress_percent = int((idx + 1) / total_files * 100)
            self.progress.emit(progress_percent)
        
        self.files_data.sort(key=lambda x: x['size'], reverse=True)
        self._emit_results()
    
    def _collect_files(self) -> list:
        all_files = []
        try:
            for root, dirs, files in os.walk(self.path):
                if self._is_cancelled:
                    break
                for file in files:
                    file_path = os.path.join(root, file)
                    all_files.append(file_path)
        except (PermissionError, OSError) as e:
            self.error.emit(f'Ошибка доступа: {str(e)}')
        return all_files
    
    def _emit_results(self):
        self.finished.emit({
            'files': self.files_data,
            'total_size': self.total_size,
            'total_files': len(self.files_data)
        })
