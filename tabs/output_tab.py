"""
Output Tab Module
Handles output configuration for time history and surface forces data.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox,
    QLineEdit, QPushButton, QFileDialog
)


class OutputTab(QWidget):
    """Output data configuration tab."""
    
    def __init__(self, parent=None, save_callback=None):
        super().__init__(parent)
        self.probe_layout = None
        self.surf_layout = None
        self.save_callback = save_callback
        self.init_ui()
    
    def init_ui(self):
        """Initialize the output tab UI."""
        layout = QVBoxLayout(self)
        
        probe_group = QGroupBox("Time History Data (Probes)")
        pg_layout = QVBoxLayout(probe_group)
        self.probe_layout = QVBoxLayout()
        
        btn_add_probe = QPushButton("+ Add Probe File")
        btn_add_probe.setProperty("secondary", True)
        btn_add_probe.clicked.connect(lambda: self.add_output_row(self.probe_layout, "Probe file"))
        
        pg_layout.addLayout(self.probe_layout)
        pg_layout.addWidget(btn_add_probe)
        
        surf_group = QGroupBox("Integrated Surface Forces Data")
        sg_layout = QVBoxLayout(surf_group)
        self.surf_layout = QVBoxLayout()
        
        btn_add_surf = QPushButton("+ Add Surface Forces File")
        btn_add_surf.setProperty("secondary", True)
        btn_add_surf.clicked.connect(lambda: self.add_output_row(self.surf_layout, "Surface file"))

        sg_layout.addLayout(self.surf_layout)
        sg_layout.addWidget(btn_add_surf)

        layout.addWidget(probe_group)
        layout.addWidget(surf_group)
        
        btn_run = QPushButton("Complete the pre-processing")
        btn_run.setMinimumHeight(50)
        btn_run.setStyleSheet("font-size: 12pt; margin-top: 20px;")
        layout.addWidget(btn_run)
        layout.addStretch()

        self.add_output_row(self.probe_layout, "Probe file")
        self.add_output_row(self.surf_layout, "Surface file")

        if self.save_callback:
            btn_run.clicked.connect(self.save_callback)
    
    def add_output_row(self, layout, placeholder):
        """Add an output file row."""
        w = QWidget()
        h = QHBoxLayout(w)
        h.setContentsMargins(0, 2, 0, 2)
        
        edit = QLineEdit()
        edit.setPlaceholderText(placeholder)
        
        btn = QPushButton("Browse")
        btn.setProperty("secondary", True)
        btn.clicked.connect(lambda: self._browse_file(edit))
        
        btn_del = QPushButton("✕")
        btn_del.setProperty("danger", True)
        btn_del.clicked.connect(lambda: self.remove_generic_row(layout, w))
        
        h.addWidget(edit)
        h.addWidget(btn)
        h.addWidget(btn_del)
        
        layout.addWidget(w)
    
    def remove_generic_row(self, layout, widget):
        """Remove a row from the layout."""
        layout.removeWidget(widget)
        widget.deleteLater()
    
    def _browse_file(self, edit):
        """Open file browser dialog."""
        path, _ = QFileDialog.getOpenFileName(self, "Select File")
        if path:
            edit.setText(path)
    
    def get_probe_layout(self):
        """Get the probe layout."""
        return self.probe_layout
    
    def get_surf_layout(self):
        """Get the surface layout."""
        return self.surf_layout
