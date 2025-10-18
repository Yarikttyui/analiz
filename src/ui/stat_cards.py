from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class StatCard(QFrame):
    def __init__(self, icon: str, title: str, value: str, parent=None):
        super().__init__(parent)
        self.icon = icon
        self.title = title
        self._setup_ui(icon, title, value)
        
    def _setup_ui(self, icon: str, title: str, value: str):
        self.setFrameShape(QFrame.Shape.StyledPanel)
        
        self.setStyleSheet("""
            QFrame {
                background-color: #1a252f;
                border-radius: 15px;
                padding: 20px;
                border: 1px solid #3a3a3a;
            }
            QLabel {
                color: #e0e0e0;
                background: transparent;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(5)
        
        icon_label = QLabel(icon)
        icon_label.setFont(QFont('Segoe UI', 14, QFont.Weight.Bold))
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setStyleSheet('color: #808080;')
        
        self.value_label = QLabel(value)
        self.value_label.setFont(QFont('Segoe UI', 28, QFont.Weight.Bold))
        self.value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        title_label = QLabel(title)
        title_label.setFont(QFont('Segoe UI', 12))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout.addWidget(icon_label)
        layout.addWidget(self.value_label)
        layout.addWidget(title_label)
        
        self.setLayout(layout)
    
    def update_value(self, value: str):
        self.value_label.setText(value)
