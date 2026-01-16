"""
Solver Tab Module
Handles solver configuration including equations, iterations, and time stepping.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QGroupBox,
    QComboBox, QSpinBox, QDoubleSpinBox, QLabel, QCheckBox, QGridLayout, QScrollArea
)
from PySide6.QtCore import Qt


class SolverTab(QWidget):
    """Solver configuration tab."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.solver_widgets = {}
        self.init_ui()
    
    def init_ui(self):
        """Initialize the solver tab UI."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Create scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.NoFrame)
        
        # Create content widget
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setSpacing(15)
        
        # Two-column layout for better organization
        top_layout = QHBoxLayout()
        top_layout.setSpacing(20)
        col1 = QVBoxLayout()
        col1.setSpacing(15)
        
        # === GENERAL SETTINGS GROUP ===
        gen_group = QGroupBox("General Settings")
        gen_form = QFormLayout(gen_group)
        
        # Simulation type - add more types by extending the list
        self.solver_widgets['sim_type'] = self._combo(["Transient", "Steady"])
        
        # Fluid equation types - add/remove equations here
        self.solver_widgets['fluid_eqn'] = self._combo(["Incompressible Navier-Stokes", "Compressible NS", "Euler", "Stokes"])
        
        # Mesh equation types
        self.solver_widgets['mesh_eqn'] = self._combo(["None", "ALE", "Prescribed", "Linear Elasticity"])
        
        # Acoustic equation types - LPCE is commonly used
        self.solver_widgets['acoustic_eqn'] = self._combo(["None", "Linear Acoustics", "LPCE", "Helmholtz", "Wave Equation"])
        
        # Dimensions
        self.solver_widgets['dims'] = self._combo(["2D", "3D"])
        gen_form.addRow("Simulation type:", self.solver_widgets['sim_type'])
        gen_form.addRow("Fluid equation:", self.solver_widgets['fluid_eqn'])
        gen_form.addRow("Mesh equation:", self.solver_widgets['mesh_eqn'])
        gen_form.addRow("Acoustic equation:", self.solver_widgets['acoustic_eqn'])
        gen_form.addRow("Dimensions:", self.solver_widgets['dims'])
        col1.addWidget(gen_group)

        nl_group = QGroupBox("Non-linear Iterations")
        nl_form = QFormLayout(nl_group)
        self.solver_widgets['nl_min'] = QSpinBox(value=1)
        self.solver_widgets['nl_max'] = QSpinBox(value=10)
        self.solver_widgets['nl_tol'] = QDoubleSpinBox(value=0.0005, decimals=4)
        nl_form.addRow("Min iterations:", self.solver_widgets['nl_min'])
        nl_form.addRow("Max iterations:", self.solver_widgets['nl_max'])
        nl_form.addRow("Tolerance:", self.solver_widgets['nl_tol'])
        col1.addWidget(nl_group)
        col1.addStretch()
        
        col2 = QVBoxLayout()
        col2.setSpacing(15)
        
        lin_group = QGroupBox("Linear Solver")
        lin_form = QFormLayout(lin_group)
        self.solver_widgets['lin_solver'] = self._combo(["GMRES", "BiCGSTAB", "Direct"])
        self.solver_widgets['lin_tol'] = QDoubleSpinBox(value=0.0005, decimals=4)
        self.solver_widgets['lin_max'] = QSpinBox(value=30)
        self.solver_widgets['lin_rst'] = QSpinBox(value=30)
        lin_form.addRow("Linear solver:", self.solver_widgets['lin_solver'])
        lin_form.addRow("Tolerance:", self.solver_widgets['lin_tol'])
        lin_form.addRow("Max iterations:", self.solver_widgets['lin_max'])
        lin_form.addRow("Restart iterations:", self.solver_widgets['lin_rst'])
        col2.addWidget(lin_group)

        time_group = QGroupBox("Time Integration")
        time_form = QFormLayout(time_group)
        self.solver_widgets['time_step'] = QDoubleSpinBox(value=0.01, decimals=4, maximum=10000)
        self.solver_widgets['max_steps'] = QSpinBox(value=10, maximum=99999)
        self.solver_widgets['rho_inf'] = QDoubleSpinBox(value=0, maximum=1, decimals=4)
        time_form.addRow("Time-step size:", self.solver_widgets['time_step'])
        time_form.addRow("Max time steps:", self.solver_widgets['max_steps'])
        time_form.addRow("Temporal damping:", self.solver_widgets['rho_inf'])
        
        restart_widget = QWidget()
        r_layout = QHBoxLayout(restart_widget)
        r_layout.setContentsMargins(0,0,0,0)
        r_layout.addWidget(QLabel("Restart Options:"))
        r_layout.addWidget(QLabel("Off"))
        self.solver_widgets['restart_flag'] = QCheckBox()
        r_layout.addWidget(self.solver_widgets['restart_flag'])
        r_layout.addWidget(QLabel("On"))
        r_layout.addStretch()
        time_form.addRow(restart_widget)
        
        self.solver_widgets['restart_id'] = QSpinBox(value=20)
        time_form.addRow("Restart time-step ID:", self.solver_widgets['restart_id'])
        col2.addWidget(time_group)
        col2.addStretch()

        top_layout.addLayout(col1, 1)
        top_layout.addLayout(col2, 1)
        layout.addLayout(top_layout)

        out_group = QGroupBox("Output Configuration")
        out_grid = QGridLayout(out_group)
        out_grid.setHorizontalSpacing(15)
        out_grid.setVerticalSpacing(10)
        
        self.solver_widgets['out_type'] = self._combo(["plt", "vtk", "csv"])
        self.solver_widgets['out_type'].setCurrentText("vtk")
        self.solver_widgets['out_start'] = QSpinBox(value=5, maximum=99999)
        self.solver_widgets['out_freq'] = QSpinBox(value=1, maximum=99999)
        self.solver_widgets['int_freq'] = QSpinBox(value=1, maximum=99999)
        self.solver_widgets['rst_freq'] = QSpinBox(value=100, maximum=99999)
        
        out_grid.addWidget(QLabel("Output file type:"), 0, 0)
        out_grid.addWidget(self.solver_widgets['out_type'], 0, 1)
        out_grid.addWidget(QLabel("Output start step:"), 0, 2)
        out_grid.addWidget(self.solver_widgets['out_start'], 0, 3)
        out_grid.addWidget(QLabel("Output frequency:"), 1, 0)
        out_grid.addWidget(self.solver_widgets['out_freq'], 1, 1)
        out_grid.addWidget(QLabel("Integrated output freq:"), 1, 2)
        out_grid.addWidget(self.solver_widgets['int_freq'], 1, 3)
        out_grid.addWidget(QLabel("Restart output freq:"), 2, 2)
        out_grid.addWidget(self.solver_widgets['rst_freq'], 2, 3)

        layout.addWidget(out_group)
        
        # Acoustic NRBC Parameters
        acoustic_group = QGroupBox("Acoustic NRBC Parameters")
        acoustic_grid = QGridLayout(acoustic_group)
        acoustic_grid.setHorizontalSpacing(15)
        acoustic_grid.setVerticalSpacing(10)
        
        self.solver_widgets['acoustic_nrbc_x'] = QDoubleSpinBox(value=0.0, minimum=-1000000, maximum=1000000, decimals=2)
        self.solver_widgets['acoustic_nrbc_y'] = QDoubleSpinBox(value=0.0, minimum=-1000000, maximum=1000000, decimals=2)
        self.solver_widgets['acoustic_nrbc_z'] = QDoubleSpinBox(value=0.0, minimum=-1000000, maximum=1000000, decimals=2)
        self.solver_widgets['acoustic_nrbc_inner'] = QDoubleSpinBox(value=10, minimum=0, maximum=1000000, decimals=2)
        self.solver_widgets['acoustic_nrbc_outer'] = QDoubleSpinBox(value=15, minimum=0, maximum=1000000, decimals=2)
        
        acoustic_grid.addWidget(QLabel("Centre X:"), 0, 0)
        acoustic_grid.addWidget(self.solver_widgets['acoustic_nrbc_x'], 0, 1)
        acoustic_grid.addWidget(QLabel("Centre Y:"), 0, 2)
        acoustic_grid.addWidget(self.solver_widgets['acoustic_nrbc_y'], 0, 3)
        acoustic_grid.addWidget(QLabel("Centre Z:"), 0, 4)
        acoustic_grid.addWidget(self.solver_widgets['acoustic_nrbc_z'], 0, 5)
        acoustic_grid.addWidget(QLabel("Inner Radius:"), 1, 0)
        acoustic_grid.addWidget(self.solver_widgets['acoustic_nrbc_inner'], 1, 1)
        acoustic_grid.addWidget(QLabel("Outer Radius:"), 1, 2)
        acoustic_grid.addWidget(self.solver_widgets['acoustic_nrbc_outer'], 1, 3)
        
        layout.addWidget(acoustic_group)
        layout.addStretch()
        
        # Set content widget and add to scroll area
        scroll.setWidget(content)
        main_layout.addWidget(scroll)
    
    def _combo(self, items):
        """Create a combo box with given items."""
        c = QComboBox()
        c.addItems(items)
        return c
    
    def get_solver_data(self):
        """Get all solver configuration data."""
        return self.solver_widgets
