"""
Physical Properties Tab Module
Handles fluid parameters and non-dimensional number calculations.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QGridLayout, QGroupBox,
    QDoubleSpinBox, QLabel, QPushButton, QLineEdit
)
from PySide6.QtCore import Qt


class PhysicalTab(QWidget):
    """Physical properties configuration tab."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.phys_inputs = {}
        self.lbl_reynolds = None
        self.lbl_mach = None
        self.init_ui()
    
    def init_ui(self):
        """Initialize the physical properties tab UI."""
        layout = QVBoxLayout(self)
        
        group = QGroupBox("Fluid Parameters")
        grid = QGridLayout(group)
        grid.setVerticalSpacing(15)
        
        # Helper function to add parameter inputs
        def add_param(label, key, val, row, col):
            """Add a labeled parameter input field."""
            w = QDoubleSpinBox(value=val, maximum=1000000, decimals=4)
            self.phys_inputs[key] = w
            grid.addWidget(QLabel(label), row, col)
            grid.addWidget(w, row, col+1)

        # Fluid properties - change default values here
        add_param("Fluid density:", "rho", 1000, 0, 0)         # kg/m³
        add_param("Fluid characteristic velocity:", "U", 1, 0, 2)  # m/s
        add_param("Fluid dynamic viscosity:", "mu", 0.9091, 1, 0)  # Pa·s
        add_param("Fluid characteristic length:", "L", 1, 1, 2)    # m
        add_param("Fluid ratio of specific heats:", "gamma", 1.4, 2, 0)  # dimensionless
        add_param("Speed of sound:", "a", 340, 3, 0)              # m/s

        layout.addWidget(group)

        calc_container = QWidget()
        calc_layout = QVBoxLayout(calc_container)
        calc_layout.setAlignment(Qt.AlignCenter)
        
        btn_check = QPushButton("Check non-dimensional numbers")
        btn_check.setFixedWidth(250)
        btn_check.clicked.connect(self.calculate_nondim)
        
        self.lbl_reynolds = QLineEdit("0")
        self.lbl_reynolds.setReadOnly(True)
        self.lbl_reynolds.setFixedWidth(100)
        
        self.lbl_mach = QLineEdit("0")
        self.lbl_mach.setReadOnly(True)
        self.lbl_mach.setFixedWidth(100)

        res_layout = QGridLayout()
        res_layout.addWidget(QLabel("Reynolds number"), 0, 0, Qt.AlignRight)
        res_layout.addWidget(self.lbl_reynolds, 0, 1, Qt.AlignLeft)
        res_layout.addWidget(QLabel("Mach number"), 1, 0, Qt.AlignRight)
        res_layout.addWidget(self.lbl_mach, 1, 1, Qt.AlignLeft)

        calc_layout.addSpacing(20)
        calc_layout.addWidget(btn_check)
        calc_layout.addSpacing(10)
        calc_layout.addLayout(res_layout)

        layout.addWidget(calc_container)
        layout.addStretch()
    
    def calculate_nondim(self):
        """Calculate Reynolds and Mach numbers."""
        try:
            rho = self.phys_inputs['rho'].value()
            mu = self.phys_inputs['mu'].value()
            U = self.phys_inputs['U'].value()
            L = self.phys_inputs['L'].value()
            a = self.phys_inputs['a'].value()

            if mu != 0:
                re = (rho * U * L) / mu
                self.lbl_reynolds.setText(f"{re:.2f}")
            else:
                self.lbl_reynolds.setText("Inf")

            if a != 0:
                ma = U / a
                self.lbl_mach.setText(f"{ma:.4f}")
            else:
                self.lbl_mach.setText("Inf")

        except Exception as e:
            print(f"Error calculating: {e}")
    
    def get_physical_data(self):
        """Get all physical properties data."""
        return self.phys_inputs
