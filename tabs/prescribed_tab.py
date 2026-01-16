"""
Prescribed Conditions Tab Module
Handles prescribed motion conditions for moving boundaries.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QGroupBox,
    QDoubleSpinBox, QLabel, QPushButton, QSpinBox, QScrollArea
)
from PySide6.QtCore import Qt


class PrescribedTab(QWidget):
    """Prescribed conditions configuration tab."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.prescribed_tag_rows = []
        self.prescribed_container = None
        self.prescribed_layout = None
        self.init_ui()
    
    def init_ui(self):
        """Initialize the prescribed conditions tab UI."""
        layout = QVBoxLayout(self)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.NoFrame)
        
        self.prescribed_container = QWidget()
        self.prescribed_container.setStyleSheet("background: #f7f9fc;")
        
        self.prescribed_layout = QVBoxLayout(self.prescribed_container)
        self.prescribed_layout.setAlignment(Qt.AlignTop)
        self.prescribed_layout.setContentsMargins(10, 10, 10, 10)
        self.prescribed_layout.setSpacing(20)

        scroll.setWidget(self.prescribed_container)
        
        btn_add_tag = QPushButton("+ Add Prescribed Condition Tag")
        btn_add_tag.clicked.connect(self.add_prescribed_tag)
        
        layout.addWidget(scroll)
        layout.addWidget(btn_add_tag)
        
        self.add_prescribed_tag()
    
    def add_prescribed_tag(self):
        """Add a new prescribed condition tag group."""
        tag_id = len(self.prescribed_tag_rows) + 1
        
        group = QGroupBox(f"Prescribed Condition Tag {tag_id}")
        group_layout = QVBoxLayout(group)
        
        grid = QGridLayout()
        grid.setHorizontalSpacing(20)
        grid.setVerticalSpacing(12)
        grid.setColumnStretch(1, 1)
        grid.setColumnStretch(3, 1)
        grid.setColumnStretch(5, 1)

        def add_row_data(row, name, v1, v2, v3):
            grid.addWidget(QLabel(f"{name} amplitude"), row, 0)
            grid.addWidget(QDoubleSpinBox(value=v1, maximum=10000), row, 1)
            grid.addWidget(QLabel(f"{name} frequency"), row, 2)
            grid.addWidget(QDoubleSpinBox(value=v2, maximum=10000), row, 3)
            grid.addWidget(QLabel(f"{name} phase"), row, 4)
            grid.addWidget(QDoubleSpinBox(value=v3, maximum=10000), row, 5)

        add_row_data(0, "Heave", 1.00, 0.20, 90.00)
        add_row_data(1, "Pitch", 30.00, 0.20, 0.00)
        add_row_data(2, "Morph", 20.00, 0.20, 0.00)

        extra_grid = QGridLayout()
        extra_grid.setHorizontalSpacing(20)
        extra_grid.setColumnStretch(1, 1)
        extra_grid.setColumnStretch(3, 1)
        extra_grid.setColumnStretch(5, 1)
        
        extra_grid.addWidget(QLabel("Morph divisions"), 0, 0)
        extra_grid.addWidget(QSpinBox(value=99), 0, 1)
        extra_grid.addWidget(QLabel("Morph position"), 0, 2)
        extra_grid.addWidget(QDoubleSpinBox(value=0.00), 0, 3)
        extra_grid.addWidget(QLabel("Leading edge X"), 1, 0)
        extra_grid.addWidget(QDoubleSpinBox(value=0.00), 1, 1)
        extra_grid.addWidget(QLabel("Leading edge Y"), 1, 2)
        extra_grid.addWidget(QDoubleSpinBox(value=0.00), 1, 3)

        group_layout.addLayout(grid)
        group_layout.addSpacing(15)
        group_layout.addLayout(extra_grid)
        
        self.prescribed_layout.addWidget(group)
        self.prescribed_tag_rows.append(group)
    
    def get_prescribed_tags(self):
        """Get all prescribed condition tag data."""
        return self.prescribed_tag_rows
