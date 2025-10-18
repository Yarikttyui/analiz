from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QTableWidget, QTableWidgetItem, QFileDialog, 
                             QLabel, QLineEdit, QHeaderView, QProgressBar)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor

from ..core.analyzer import FileAnalyzer
from ..ui.buttons import ModernButton
from ..ui.stat_cards import StatCard
from ..utils.constants import *
from ..utils.file_utils import format_size, validate_path


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.analyzer_thread = None
        self._init_ui()
        
    def _init_ui(self):
        self.setWindowTitle(WINDOW_TITLE)
        self.setMinimumSize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)
        
        self.setStyleSheet(APP_STYLE)
        
        self._create_header(main_layout)
        self._create_input_section(main_layout)
        self._create_buttons(main_layout)
        self._create_progress_bar(main_layout)
        self._create_stat_cards(main_layout)
        self._create_table(main_layout)
        
        central_widget.setLayout(main_layout)
        self.statusBar().setStyleSheet(STATUS_BAR_STYLE)
    
    def _create_header(self, parent_layout):
        header_layout = QVBoxLayout()
        
        title = QLabel(APP_TITLE)
        title.setFont(QFont('Segoe UI', 32, QFont.Weight.Bold))
        title.setStyleSheet('color: #e0e0e0;')
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        subtitle = QLabel(APP_SUBTITLE)
        subtitle.setFont(QFont('Segoe UI', 14))
        subtitle.setStyleSheet('color: #a0a0a0;')
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        parent_layout.addLayout(header_layout)
    
    def _create_input_section(self, parent_layout):
        input_layout = QVBoxLayout()
        
        path_label = QLabel(PATH_LABEL)
        path_label.setFont(QFont('Segoe UI', 12, QFont.Weight.Bold))
        path_label.setStyleSheet('color: #e0e0e0;')
        
        self.path_input = QLineEdit()
        self.path_input.setPlaceholderText(PATH_PLACEHOLDER)
        self.path_input.setFont(QFont('Segoe UI', 12))
        
        input_layout.addWidget(path_label)
        input_layout.addWidget(self.path_input)
        parent_layout.addLayout(input_layout)
    
    def _create_buttons(self, parent_layout):
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)
        self.btn_select_folder = ModernButton(
            'Выбрать папку', 
            *BUTTON_COLORS['folder']
        )
        self.btn_select_folder.clicked.connect(self._select_folder)
        
        self.btn_select_file = ModernButton(
            'Выбрать файл',
            *BUTTON_COLORS['file']
        )
        self.btn_select_file.clicked.connect(self._select_file)
        
        self.btn_analyze = ModernButton(
            'Анализировать',
            *BUTTON_COLORS['analyze']
        )
        self.btn_analyze.clicked.connect(self._analyze_path)
        
        self.btn_clear = ModernButton(
            'Очистить',
            *BUTTON_COLORS['clear']
        )
        self.btn_clear.clicked.connect(self._clear_results)
        
        buttons_layout.addWidget(self.btn_select_folder)
        buttons_layout.addWidget(self.btn_select_file)
        buttons_layout.addWidget(self.btn_analyze)
        buttons_layout.addWidget(self.btn_clear)
        buttons_layout.addStretch()
        
        parent_layout.addLayout(buttons_layout)
    
    def _create_progress_bar(self, parent_layout):
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setFont(QFont('Segoe UI', 10, QFont.Weight.Bold))
        parent_layout.addWidget(self.progress_bar)
    
    def _create_stat_cards(self, parent_layout):
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(20)
        
        self.stat_files = StatCard('ФАЙЛЫ', 'Всего файлов', '0')
        self.stat_size = StatCard('РАЗМЕР', 'Общий размер', '0 Б')
        self.stat_largest = StatCard('МАКС', 'Самый большой', '0 Б')
        
        stats_layout.addWidget(self.stat_files)
        stats_layout.addWidget(self.stat_size)
        stats_layout.addWidget(self.stat_largest)
        
        parent_layout.addLayout(stats_layout)
    
    def _create_table(self, parent_layout):
        self.table = QTableWidget()
        self.table.setColumnCount(len(TABLE_HEADERS))
        self.table.setHorizontalHeaderLabels(TABLE_HEADERS)
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(0, TABLE_ICON_COLUMN_WIDTH)
        
        self.table.setAlternatingRowColors(False)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setFont(QFont('Segoe UI', 10))
        
        parent_layout.addWidget(self.table, 1)
    
    def _select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, 'Выберите папку')
        if folder:
            self.path_input.setText(folder)
    
    def _select_file(self):
        file, _ = QFileDialog.getOpenFileName(self, 'Выберите файл')
        if file:
            self.path_input.setText(file)
    
    def _analyze_path(self):
        import os
        path = self.path_input.text().strip()
        is_valid, error_msg = validate_path(path)
        if not is_valid:
            self._show_message(MSG_PATH_EMPTY if not path else MSG_PATH_NOT_EXISTS)
            return
        
        self.table.setRowCount(0)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self._set_buttons_enabled(False)
        is_folder = os.path.isdir(path)
        self.analyzer_thread = FileAnalyzer(path, is_folder)
        self.analyzer_thread.progress.connect(self._update_progress)
        self.analyzer_thread.file_found.connect(self._add_file_to_table)
        self.analyzer_thread.finished.connect(self._analysis_finished)
        self.analyzer_thread.error.connect(self._handle_error)
        self.analyzer_thread.start()
        
        self._show_message(MSG_ANALYZING)
    
    def _update_progress(self, value: int):
        self.progress_bar.setValue(value)
    
    def _add_file_to_table(self, file_info: dict):
        row = self.table.rowCount()
        self.table.insertRow(row)
        
        icon_item = QTableWidgetItem(file_info['icon'])
        icon_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_item.setFont(QFont('Consolas', 9, QFont.Weight.Bold))
        self.table.setItem(row, 0, icon_item)
        
        name_item = QTableWidgetItem(file_info['name'])
        self.table.setItem(row, 1, name_item)
        
        size_item = QTableWidgetItem(file_info['size_formatted'])
        self.table.setItem(row, 2, size_item)
        
        percent_item = QTableWidgetItem('')
        self.table.setItem(row, 3, percent_item)
        path_item = QTableWidgetItem(file_info['path'])
        path_item.setForeground(QColor('#808080'))
        self.table.setItem(row, 4, path_item)
        
        self.table.setRowHeight(row, TABLE_ROW_HEIGHT)
    
    def _analysis_finished(self, result: dict):
        self.progress_bar.setVisible(False)
        self._set_buttons_enabled(True)
        total_files = result['total_files']
        total_size = result['total_size']
        
        self.stat_files.update_value(str(total_files))
        self.stat_size.update_value(format_size(total_size))
        
        if result['files']:
            largest = result['files'][0]['size_formatted']
            self.stat_largest.update_value(largest)
            
            for row in range(self.table.rowCount()):
                if row < len(result['files']):
                    file_size = result['files'][row]['size']
                    percent = (file_size / total_size * 100) if total_size > 0 else 0
                    percent_item = self.table.item(row, 3)
                    percent_item.setText(f'{percent:.2f}%')
        else:
            self.stat_largest.update_value('0 Б')
        
        self._show_message(MSG_ANALYSIS_COMPLETE.format(total_files))
    
    def _handle_error(self, error_msg: str):
        self.progress_bar.setVisible(False)
        self._set_buttons_enabled(True)
        self._show_message(MSG_ERROR.format(error_msg))
    
    def _clear_results(self):
        self.table.setRowCount(0)
        self.path_input.clear()
        self.stat_files.update_value('0')
        self.stat_size.update_value('0 Б')
        self.stat_largest.update_value('0 Б')
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(False)
        self.statusBar().clearMessage()
    
    def _set_buttons_enabled(self, enabled: bool):
        self.btn_select_folder.setEnabled(enabled)
        self.btn_select_file.setEnabled(enabled)
        self.btn_analyze.setEnabled(enabled)
        self.btn_clear.setEnabled(enabled)
    
    def _show_message(self, message: str):
        self.statusBar().showMessage(message, 5000)
