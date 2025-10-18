from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class ModernButton(QPushButton):
    def __init__(self, text: str, color_start: str, color_end: str, parent=None):
        super().__init__(text, parent)
        self.color_start = color_start
        self.color_end = color_end
        self._setup_style()
        
    def _setup_style(self):
        self.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {self.color_start}, stop:1 {self.color_end});
                color: white;
                border: none;
                border-radius: 12px;
                padding: 15px 30px;
                font-size: 14px;
                font-weight: bold;
                min-width: 150px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {self.color_end}, stop:1 {self.color_start});
            }}
            QPushButton:pressed {{
                padding: 16px 29px 14px 31px;
            }}
            QPushButton:disabled {{
                background: #cccccc;
                color: #666666;
            }}
        """)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFont(QFont('Segoe UI', 10, QFont.Weight.Bold))
