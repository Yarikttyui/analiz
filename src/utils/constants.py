BUTTON_COLORS = {
    'folder': ('#2c3e50', '#34495e'),
    'file': ('#2c3e50', '#34495e'),
    'analyze': ('#1a252f', '#2c3e50'),
    'clear': ('#4a4a4a', '#5a5a5a'),
}
WINDOW_MIN_WIDTH = 1200
WINDOW_MIN_HEIGHT = 800
TABLE_ICON_COLUMN_WIDTH = 80
TABLE_ROW_HEIGHT = 50

APP_STYLE = """
    QMainWindow {
        background-color: #1a1a1a;
    }
    QWidget {
        background-color: #2d2d2d;
        border-radius: 10px;
        color: #e0e0e0;
    }
    QLineEdit {
        padding: 15px;
        border: 2px solid #404040;
        border-radius: 10px;
        font-size: 14px;
        background-color: #3a3a3a;
        color: #e0e0e0;
    }
    QLineEdit:focus {
        border: 2px solid #4a4a4a;
    }
    QTableWidget {
        border: none;
        border-radius: 10px;
        background-color: #2d2d2d;
        gridline-color: #404040;
        color: #e0e0e0;
        alternate-background-color: #2d2d2d;
    }
    QTableWidget::item {
        padding: 10px;
        color: #e0e0e0;
        background-color: #2d2d2d;
    }
    QTableWidget::item:selected {
        background-color: #3a3a3a;
        color: #ffffff;
    }
    QHeaderView::section {
        background-color: #1a252f;
        color: #e0e0e0;
        padding: 12px;
        border: none;
        font-weight: bold;
        font-size: 13px;
    }
    QLabel {
        background: transparent;
        color: #e0e0e0;
    }
    QProgressBar {
        border: 2px solid #404040;
        border-radius: 10px;
        text-align: center;
        background-color: #3a3a3a;
        color: #e0e0e0;
    }
    QProgressBar::chunk {
        background-color: #2c3e50;
        border-radius: 8px;
    }
"""

STATUS_BAR_STYLE = """
    QStatusBar {
        background-color: #2d2d2d;
        color: #e0e0e0;
        font-weight: bold;
        font-size: 12px;
    }
"""

WINDOW_TITLE = 'Проверка размера файлов'
APP_TITLE = 'Проверка размера файлов'
APP_SUBTITLE = 'Анализатор файлов'
PATH_LABEL = 'Путь к файлу или папке:'
PATH_PLACEHOLDER = 'Например: C:\\Users\\Desktop\\Documents'

TABLE_HEADERS = ['Тип', 'Имя файла', 'Размер', 'Процент', 'Путь']
MSG_PATH_EMPTY = 'Введите путь к файлу или папке'
MSG_PATH_NOT_EXISTS = 'Путь не существует'
MSG_ANALYZING = 'Анализируем файлы...'
MSG_ANALYSIS_COMPLETE = 'Анализ завершен! Найдено файлов: {}'
MSG_ERROR = 'Ошибка: {}'
