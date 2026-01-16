"""
Geometry Tab Module
==================

Handles geometry configuration including mesh files and boundary files.

Customization:
- Change connectivity types: Modify CONNECTIVITY_TYPES list
- Add more file inputs: Add rows in create_mesh_config()
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QComboBox, QGroupBox, QGridLayout, QScrollArea
)
from PySide6.QtCore import Qt

from utils.helpers import browse_file


# Configuration constants - edit these to customize options
CONNECTIVITY_TYPES = [
    "4-Node Quadrilateral",
    "3-Node Triangle", 
    "6-Node Triangle"
]


class GeometryTab(QWidget):
    """
    Geometry configuration tab.
    
    Manages:
    - Coordinate file selection
    - Connectivity file selection  
    - Element type selection
    - Dynamic boundary file list
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_app = parent
        self.boundary_rows = []
        self.init_ui()
    
    def init_ui(self):
        """Initialize the geometry tab UI."""
        layout = QVBoxLayout(self)
        
        # Mesh Configuration Section
        layout.addWidget(self.create_mesh_config())
        
        # Boundary Files Section
        layout.addWidget(self.create_boundary_files())
    
    def create_mesh_config(self):
        """
        Create the mesh configuration group.
        
        Returns:
            QGroupBox: Mesh configuration widget
        """
        group = QGroupBox("Mesh Configuration")
        grid = QGridLayout(group)
        
        # Coordinate file input
        self.coord_edit = QLineEdit()
        btn_coord = QPushButton("Browse")
        btn_coord.setProperty("secondary", True)
        btn_coord.clicked.connect(lambda: browse_file(self, self.coord_edit))
        
        # Connectivity file input
        self.conn_edit = QLineEdit()
        btn_conn = QPushButton("Browse")
        btn_conn.setProperty("secondary", True)
        btn_conn.clicked.connect(lambda: browse_file(self, self.conn_edit))
        
        # Connectivity type dropdown
        self.conn_type = QComboBox()
        self.conn_type.addItems(CONNECTIVITY_TYPES)
        
        # Layout
        grid.addWidget(QLabel("Coordinate file:"), 0, 0)
        grid.addWidget(self.coord_edit, 0, 1)
        grid.addWidget(btn_coord, 0, 2)
        grid.addWidget(QLabel("Connectivity file:"), 1, 0)
        grid.addWidget(self.conn_edit, 1, 1)
        grid.addWidget(btn_conn, 1, 2)
        grid.addWidget(QLabel("Connectivity type:"), 2, 0)
        grid.addWidget(self.conn_type, 2, 1)
        
        return group
    
    def create_boundary_files(self):
        """
        Create the boundary files group with scrollable list.
        
        Returns:
            QGroupBox: Boundary files widget
        """
        group = QGroupBox("Boundary Files")
        layout = QVBoxLayout(group)
        
        # Scrollable area for boundary rows
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.NoFrame)
        scroll.setStyleSheet("background: transparent;")
        
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_layout.setAlignment(Qt.AlignTop)
        scroll.setWidget(self.scroll_widget)
        
        # Add boundary file button
        btn_add = QPushButton("+ Add Boundary File")
        btn_add.setProperty("secondary", True)
        btn_add.clicked.connect(self.add_boundary_row)
        
        layout.addWidget(scroll)
        layout.addWidget(btn_add)
        
        # Add initial row
        self.add_boundary_row()
        
        return group
    
    def add_boundary_row(self):
        """Add a new boundary file row."""
        row_idx = len(self.boundary_rows) + 1
        row_widget = QWidget()
        row_layout = QHBoxLayout(row_widget)
        row_layout.setContentsMargins(0, 0, 0, 0)
        
        # Label
        lbl = QLabel(f"B-{row_idx}")
        lbl.setFixedWidth(40)
        lbl.setStyleSheet("font-weight: bold;")
        
        # File path input
        edit = QLineEdit()
        edit.setPlaceholderText(f"Select file for Boundary {row_idx}...")
        
        # Browse button
        btn_browse = QPushButton("Browse")
        btn_browse.setProperty("secondary", True)
        btn_browse.clicked.connect(lambda: browse_file(self, edit))
        
        # Delete button
        btn_del = QPushButton("✕")
        btn_del.setProperty("danger", True)
        btn_del.clicked.connect(lambda: self.remove_boundary_row(row_widget))
        
        # Add widgets to layout
        row_layout.addWidget(lbl)
        row_layout.addWidget(edit)
        row_layout.addWidget(btn_browse)
        row_layout.addWidget(btn_del)
        
        self.scroll_layout.addWidget(row_widget)
        self.boundary_rows.append({
            "widget": row_widget,
            "label": lbl,
            "edit": edit,
            "btn_del": btn_del
        })
        
        self.refresh_ui()
    
    def remove_boundary_row(self, widget):
        """
        Remove a boundary file row.
        
        Args:
            widget: The row widget to remove
        """
        if len(self.boundary_rows) <= 1:
            return  # Keep at least one row
        
        # Find and remove the row
        for i, row in enumerate(self.boundary_rows):
            if row["widget"] == widget:
                self.boundary_rows.pop(i)
                break
        
        self.scroll_layout.removeWidget(widget)
        widget.deleteLater()
        self.refresh_ui()
    
    def refresh_ui(self):
        """Refresh row labels and delete button visibility."""
        show_del = len(self.boundary_rows) > 1
        
        for i, row in enumerate(self.boundary_rows):
            idx = i + 1
            row["label"].setText(f"B-{idx}")
            row["edit"].setPlaceholderText(f"Select file for Boundary {idx}...")
            row["btn_del"].setVisible(show_del)
    
    def get_boundary_rows(self):
        """
        Get all boundary file rows.
        
        Returns:
            list: List of boundary row dictionaries
        """
        return self.boundary_rows
    
    def get_coord_file(self):
        """Get coordinate file path."""
        return self.coord_edit.text()
    
    def get_conn_file(self):
        """Get connectivity file path."""
        return self.conn_edit.text()
    
    def get_conn_type(self):
        """Get connectivity type."""
        return self.conn_type.currentText()
