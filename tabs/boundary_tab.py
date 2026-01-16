"""
Boundary Conditions Tab Module
Handles initial conditions and boundary condition configuration.
"""

import os
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QGroupBox, QTabWidget,
    QDoubleSpinBox, QLabel, QPushButton, QLineEdit, QComboBox, QSpinBox,
    QScrollArea
)
from PySide6.QtCore import Qt


class BoundaryTab(QWidget):
    """Boundary conditions configuration tab."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_cond_widgets = {}
        self.bc_tabs = None
        self.bc_layouts = {}
        self.geometry_boundary_rows = []  # Will be set by main window
        self.init_ui()
    
    def init_ui(self):
        """Initialize the boundary conditions tab UI."""
        layout = QVBoxLayout(self)

        # === INITIAL CONDITIONS GROUP ===
        init_group = QGroupBox("Initial Conditions")
        ig_layout = QGridLayout(init_group)
        
        # Create input fields for all initial conditions
        # Change default values here (value= parameter)
        self.init_cond_widgets['pres'] = QDoubleSpinBox()
        self.init_cond_widgets['xvel'] = QDoubleSpinBox(value=1)  # Default X-velocity = 1
        self.init_cond_widgets['yvel'] = QDoubleSpinBox()
        self.init_cond_widgets['zvel'] = QDoubleSpinBox()
        self.init_cond_widgets['xdisp'] = QDoubleSpinBox()
        self.init_cond_widgets['ydisp'] = QDoubleSpinBox()
        self.init_cond_widgets['zdisp'] = QDoubleSpinBox()
        self.init_cond_widgets['psi'] = QDoubleSpinBox()
        
        ig_layout.addWidget(QLabel("Pressure"), 0, 0); ig_layout.addWidget(self.init_cond_widgets['pres'], 0, 1)
        ig_layout.addWidget(QLabel("X-velocity"), 0, 2); ig_layout.addWidget(self.init_cond_widgets['xvel'], 0, 3)
        ig_layout.addWidget(QLabel("Y-velocity"), 0, 4); ig_layout.addWidget(self.init_cond_widgets['yvel'], 0, 5)
        ig_layout.addWidget(QLabel("Z-velocity"), 0, 6); ig_layout.addWidget(self.init_cond_widgets['zvel'], 0, 7)
        ig_layout.addWidget(QLabel("X-disp"), 1, 0); ig_layout.addWidget(self.init_cond_widgets['xdisp'], 1, 1)
        ig_layout.addWidget(QLabel("Y-disp"), 1, 2); ig_layout.addWidget(self.init_cond_widgets['ydisp'], 1, 3)
        ig_layout.addWidget(QLabel("Z-disp"), 1, 4); ig_layout.addWidget(self.init_cond_widgets['zdisp'], 1, 5)
        ig_layout.addWidget(QLabel("Psi"), 1, 6); ig_layout.addWidget(self.init_cond_widgets['psi'], 1, 7)
        
        layout.addWidget(init_group)

        self.bc_tabs = QTabWidget()
        self.bc_tabs.setObjectName("subtabs")

        for name in ["X-velocity", "Y-velocity", "Z-velocity", "X-disp", "Y-disp", "Z-disp", "Acoustic-potential"]:
            w = QWidget()
            l = QVBoxLayout(w)
            
            scroll = QScrollArea()
            scroll.setWidgetResizable(True)
            scroll.setFrameShape(QScrollArea.NoFrame)
            content = QWidget()
            content_layout = QVBoxLayout(content)
            content_layout.setAlignment(Qt.AlignTop)
            scroll.setWidget(content)
            
            l.addWidget(scroll)
            
            btn_add = QPushButton("+ Add Boundary Condition")
            btn_add.setProperty("secondary", True)
            # Fix closure issue by using default arguments
            btn_add.clicked.connect(lambda checked=False, layout=content_layout, tab=name: self.add_bc_row(layout, tab))
            l.addWidget(btn_add)

            self.bc_layouts[name] = content_layout
            self.bc_tabs.addTab(w, name)
        
        layout.addWidget(self.bc_tabs)
        self.refresh_active_boundary_tab(initial=True)
    
    def add_bc_row(self, layout, tab_name, label_text=None):
        """Add a boundary condition row."""
        row_count = layout.count() + 1
        if label_text is None:
            label_text = f"B-{row_count}"
        
        w = QWidget()
        h = QHBoxLayout(w)
        h.setContentsMargins(0, 2, 0, 2)
        
        lbl = QLabel(label_text)
        lbl.setFixedWidth(40)
        lbl.setStyleSheet("font-weight:bold;")
        
        name_edit = QLineEdit()
        name_edit.setPlaceholderText("Boundary Name/ID")
        
        type_combo = QComboBox()
        # Set boundary condition types based on variable type
        if "velocity" in tab_name:
            type_combo.addItems(["None", "Dirichlet", "matchMeshVel"])
        elif "disp" in tab_name:
            type_combo.addItems(["None", "Dirichlet", "prescribed"])
        elif "Acoustic" in tab_name:
            type_combo.addItems(["None", "Dirichlet"])
        else:
            type_combo.addItems(["None", "Dirichlet", "Neumann", "Robin"])
        
        val_spin = QDoubleSpinBox(maximum=1000000)
        
        h.addWidget(lbl)
        h.addWidget(name_edit)
        h.addWidget(QLabel("Type"))
        h.addWidget(type_combo)
        h.addWidget(QLabel("Value"))
        h.addWidget(val_spin)
        
        if "disp" in tab_name:
            tag_spin = QSpinBox(value=0)
            tag_spin.setFixedWidth(60)
            h.addWidget(QLabel("Tag"))
            h.addWidget(tag_spin)

        btn_del = QPushButton("✕")
        btn_del.setProperty("danger", True)
        btn_del.clicked.connect(lambda: self.remove_generic_row(layout, w))
        h.addWidget(btn_del)

        layout.addWidget(w)
        # Refresh labels to ensure sequential numbering
        self._refresh_bc_labels(layout)

    def refresh_active_boundary_tab(self, initial=False):
        """Refresh the active boundary tab with rows matching geometry boundaries."""
        if initial:
            count = 1
        else:
            count = len(self.geometry_boundary_rows)

        idx = self.bc_tabs.currentIndex()
        name = self.bc_tabs.tabText(idx)
        target_layout = self.bc_layouts[name]
        
        while target_layout.count():
            child = target_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        for i in range(count):
            lbl = f"B-{i+1}"
            self.add_bc_row(target_layout, name, lbl)
            
            if not initial and i < len(self.geometry_boundary_rows):
                boundary_file = self.geometry_boundary_rows[i]["edit"].text()
                if boundary_file:
                    filename = os.path.splitext(os.path.basename(boundary_file))[0]
                    row_widget = target_layout.itemAt(i).widget()
                    if row_widget:
                        row_h_layout = row_widget.layout()
                        name_edit = row_h_layout.itemAt(1).widget()
                        if name_edit:
                            name_edit.setText(filename)

    def remove_generic_row(self, layout, widget):
        """Remove a row from the layout."""
        layout.removeWidget(widget)
        widget.deleteLater()
        # Refresh labels for boundary condition rows
        self._refresh_bc_labels(layout)
    
    def _refresh_bc_labels(self, layout):
        """Refresh boundary condition row labels to be sequential B-1, B-2, B-3, etc."""
        for i in range(layout.count()):
            row_widget = layout.itemAt(i).widget()
            if row_widget and row_widget.layout():
                row_h_layout = row_widget.layout()
                # First item in horizontal layout is the label
                label_widget = row_h_layout.itemAt(0).widget()
                if isinstance(label_widget, QLabel):
                    label_widget.setText(f"B-{i+1}")
    
    def set_geometry_boundary_rows(self, rows):
        """Set the geometry boundary rows reference."""
        self.geometry_boundary_rows = rows
    
    def get_initial_conditions(self):
        """Get all initial conditions data."""
        return self.init_cond_widgets
    
    def get_boundary_conditions(self):
        """Get all boundary conditions data."""
        return self.bc_layouts
