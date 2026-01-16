"""
Fluid-Acoustic Solver GUI Application
======================================

This application provides a graphical interface for configuring fluid-acoustic
solver simulations with moving boundaries.

CUSTOMIZATION GUIDE:
-------------------
1. COLORS & STYLING: See the setStyleSheet() section in __init__() (around line 50)
2. DEFAULT VALUES: Search for QSpinBox(value=...) or QDoubleSpinBox(value=...)
3. TAB NAMES: See self.tabs.addTab() calls in init_ui() (around line 100)
4. WINDOW SIZE: See showMaximized() in __init__() (around line 25)
5. BUTTON LABELS: Search for QPushButton("text") throughout the file

ARCHITECTURE:
------------
- SolverGUI: Main window class containing all UI components
- create_*_tab(): Methods that build each tab's UI
- save_input_file(): Generates the output configuration file
- add_*_row(): Methods that add dynamic rows to lists

For detailed build instructions, see README.md
"""

import sys
import os
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QComboBox,
    QVBoxLayout, QHBoxLayout, QFileDialog, QTabWidget, QFormLayout, QSpinBox,
    QDoubleSpinBox, QSizePolicy, QGroupBox, QGridLayout,
    QScrollArea, QCheckBox
)
from PySide6.QtCore import Qt


class SolverGUI(QWidget):
    """
    Main application window for the Fluid-Acoustic Solver GUI.
    
    This class manages all UI components and data for the solver configuration.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fluid-Acoustic Solver for Moving Boundaries")
        # Open maximized by default to ensure all controls are visible
        self.showMaximized()

        # ============================================================
        # APPLICATION STYLING - Customize colors and appearance here
        # ============================================================
        # Background color: #f7f9fc
        # Primary button color: #3b82f6
        # Font: 'Segoe UI' (Windows) - change to 'Arial' or 'Helvetica' for other systems
        self.setStyleSheet("""
        QWidget { background: #f7f9fc; color: #222; font-family: 'Segoe UI', sans-serif; font-size: 11pt; }
        QLabel#title { font-size: 20pt; font-weight: 700; color: #1e3a8a; padding: 10px; }
        QGroupBox { font-weight: 600; border: 1px solid #cbd5e1; border-radius: 8px; background: #ffffff; margin-top: 24px; padding-top: 25px; padding-bottom: 15px; }
        QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 5px; }
        QLineEdit, QComboBox, QDoubleSpinBox, QSpinBox { min-height: 30px; max-height: 30px; padding: 4px; border: 1px solid #cbd5e1; border-radius: 4px; background: white; }
        QLineEdit:focus, QComboBox:focus, QSpinBox:focus { border: 1px solid #3b82f6; }
        QPushButton { min-height: 32px; background-color: #3b82f6; color: white; border-radius: 6px; font-weight: 600; padding: 0 15px; border: none; }
        QPushButton:hover { background-color: #2563eb; }
        QPushButton:pressed { background-color: #1d4ed8; }
        QPushButton[secondary='true'] { background-color: #eff6ff; color: #1e40af; border: 1px solid #bfdbfe; }
        QPushButton[secondary='true']:hover { background-color: #dbeafe; }
        QPushButton[danger='true'] { background-color: transparent; color: #ef4444; font-weight: bold; font-size: 14pt; min-width: 30px; }
        QPushButton[danger='true']:hover { background-color: #fee2e2; border-radius: 4px; }
        QTabWidget::pane { border: 0; }
        QTabBar::tab { background: #e2e8f0; padding: 8px 20px; margin-right: 2px; border-top-left-radius: 6px; border-top-right-radius: 6px; color: #64748b; }
        QTabBar::tab:selected { background: #3b82f6; color: white; font-weight: bold; }
        QTabBar::tab:hover:!selected { background: #cbd5e1; }
        """)

        # ============================================================
        # DATA STORAGE
        # ============================================================
        # These lists and dictionaries store the dynamic UI elements and their values
        self.geometry_boundary_rows = []  # Stores boundary file rows in Geometry tab
        self.prescribed_tag_rows = []      # Stores prescribed motion condition groups
        self.phys_inputs = {}              # Physical properties input widgets
        self.solver_widgets = {}           # Solver configuration widgets
        self.init_cond_widgets = {}        # Initial condition widgets

        self.init_ui()

    def init_ui(self):
        """
        Initialize the main user interface.
        
        Creates the main layout with:
        - Title bar
        - Tab widget with 6 tabs
        
        To add a new tab: self.tabs.addTab(self.create_my_tab(), "Tab Name")
        """
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(10)

        # Title label - change text here to modify the header
        title = QLabel("Fluid-Acoustic Solver for Moving Boundaries")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)

        # Tab widget containing all configuration tabs
        self.tabs = QTabWidget()
        # Add tabs here - order determines display order
        self.tabs.addTab(self.create_geometry_tab(), "Geometry")
        self.tabs.addTab(self.create_solver_tab(), "Solver")
        self.tabs.addTab(self.create_physical_tab(), "Physical properties")
        self.tabs.addTab(self.create_boundary_tab(), "Boundary conditions")
        self.tabs.addTab(self.create_prescribed_tab(), "Prescribed conditions")
        self.tabs.addTab(self.create_output_tab(), "Output data")
        
        main_layout.addWidget(self.tabs)

    def create_geometry_tab(self):
        """
        Create the Geometry configuration tab.
        
        Contains:
        - Mesh Configuration: Coordinate and connectivity files
        - Boundary Files: Dynamic list of boundary condition files
        
        Customization:
        - Change file type labels: Modify QLabel text
        - Change dropdown options: Modify conn_type.addItems() list
        """
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # === MESH CONFIGURATION GROUP ===
        file_group = QGroupBox("Mesh Configuration")
        grid = QGridLayout(file_group)
        
        # Coordinate file input
        self.coord_edit = QLineEdit()
        btn_coord = QPushButton("Browse")
        btn_coord.setProperty("secondary", True)
        btn_coord.clicked.connect(lambda: self._browse_file(self.coord_edit))
        
        # Connectivity file input
        self.conn_edit = QLineEdit()
        btn_conn = QPushButton("Browse")
        btn_conn.setProperty("secondary", True)
        btn_conn.clicked.connect(lambda: self._browse_file(self.conn_edit))

        # Connectivity type dropdown - add/remove options here
        self.conn_type = QComboBox()
        self.conn_type.addItems(["4-Node Quadrilateral", "3-Node Triangle", "6-Node Triangle"])
        
        grid.addWidget(QLabel("Coordinate file:"), 0, 0)
        grid.addWidget(self.coord_edit, 0, 1)
        grid.addWidget(btn_coord, 0, 2)
        grid.addWidget(QLabel("Connectivity file:"), 1, 0)
        grid.addWidget(self.conn_edit, 1, 1)
        grid.addWidget(btn_conn, 1, 2)
        grid.addWidget(QLabel("Connectivity type:"), 2, 0)
        grid.addWidget(self.conn_type, 2, 1)
        
        layout.addWidget(file_group)

        self.boundary_group = QGroupBox("Boundary Files")
        bg_layout = QVBoxLayout(self.boundary_group)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.NoFrame)
        scroll.setStyleSheet("background: transparent;")
        
        self.geom_scroll_widget = QWidget()
        self.geom_scroll_layout = QVBoxLayout(self.geom_scroll_widget)
        self.geom_scroll_layout.setAlignment(Qt.AlignTop)
        scroll.setWidget(self.geom_scroll_widget)

        self.btn_add_geom_bound = QPushButton("+ Add Boundary File")
        self.btn_add_geom_bound.setProperty("secondary", True)
        self.btn_add_geom_bound.clicked.connect(self.add_geometry_row)

        bg_layout.addWidget(scroll)
        bg_layout.addWidget(self.btn_add_geom_bound)
        
        layout.addWidget(self.boundary_group)
        self.add_geometry_row()
        
        return tab

    def add_geometry_row(self):
        row_idx = len(self.geometry_boundary_rows) + 1
        row_widget = QWidget()
        row_layout = QHBoxLayout(row_widget)
        row_layout.setContentsMargins(0, 0, 0, 0)

        lbl = QLabel(f"B-{row_idx}")
        lbl.setFixedWidth(40)
        lbl.setStyleSheet("font-weight: bold;")
        
        edit = QLineEdit()
        edit.setPlaceholderText(f"Select file for Boundary {row_idx}...")
        
        btn_browse = QPushButton("Browse")
        btn_browse.setProperty("secondary", True)
        btn_browse.clicked.connect(lambda: self._browse_file(edit))
        
        btn_del = QPushButton("✕")
        btn_del.setProperty("danger", True)
        btn_del.clicked.connect(lambda: self.remove_geometry_row(row_widget))

        row_layout.addWidget(lbl)
        row_layout.addWidget(edit)
        row_layout.addWidget(btn_browse)
        row_layout.addWidget(btn_del)
        
        self.geom_scroll_layout.addWidget(row_widget)
        self.geometry_boundary_rows.append({"widget": row_widget, "label": lbl, "edit": edit, "btn_del": btn_del})
        self._refresh_geom_ui()

    def remove_geometry_row(self, widget):
        if len(self.geometry_boundary_rows) <= 1: return
        
        for i, row in enumerate(self.geometry_boundary_rows):
            if row["widget"] == widget:
                self.geometry_boundary_rows.pop(i)
                break
        
        self.geom_scroll_layout.removeWidget(widget)
        widget.deleteLater()
        self._refresh_geom_ui()

    def _refresh_geom_ui(self):
        show_del = len(self.geometry_boundary_rows) > 1
        for i, row in enumerate(self.geometry_boundary_rows):
            idx = i + 1
            row["label"].setText(f"B-{idx}")
            row["edit"].setPlaceholderText(f"Select file for Boundary {idx}...")
            row["btn_del"].setVisible(show_del)

    def create_solver_tab(self):
        """
        Create the Solver configuration tab.
        
        Contains four main sections:
        1. General Settings: Simulation type, equations, dimensions
        2. Non-linear Iterations: Iteration limits and tolerance
        3. Linear Solver: Solver type and parameters
        4. Time Integration: Time stepping and restart options
        5. Output Configuration: File format and frequencies
        6. Acoustic NRBC Parameters: Non-reflecting boundary conditions
        
        Customization:
        - Add equation types: Modify self._combo() lists
        - Change default values: Modify value= parameters in QSpinBox/QDoubleSpinBox
        - Add new settings: Add rows with gen_form.addRow()
        """
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Two-column layout for better organization
        top_layout = QHBoxLayout()
        col1 = QVBoxLayout()
        
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
        
        col2 = QVBoxLayout()
        
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

        top_layout.addLayout(col1)
        top_layout.addLayout(col2)
        layout.addLayout(top_layout)

        out_group = QGroupBox("Output Configuration")
        out_grid = QGridLayout(out_group)
        
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
        return tab

    def create_physical_tab(self):
        """
        Create the Physical Properties tab.
        
        Contains:
        - Fluid parameters (density, viscosity, etc.)
        - Non-dimensional number calculator
        
        Customization:
        - Add parameters: Call add_param() with new label, key, default value, row, col
        - Change defaults: Modify the value parameter in add_param() calls
        """
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
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
        
        self.lbl_reynolds = QLineEdit("0"); self.lbl_reynolds.setReadOnly(True); self.lbl_reynolds.setFixedWidth(100)
        self.lbl_mach = QLineEdit("0"); self.lbl_mach.setReadOnly(True); self.lbl_mach.setFixedWidth(100)

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
        return tab

    def calculate_nondim(self):
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

    def create_boundary_tab(self):
        """
        Create the Boundary Conditions tab.
        
        Contains:
        - Initial Conditions: Default values for all variables
        - Boundary Condition Tabs: X/Y/Z velocity, X/Y/Z displacement, Acoustic potential
        
        Customization:
        - Add variables: Add new entries to the loop that creates tabs
        - Change initial defaults: Modify value= in QDoubleSpinBox() calls
        - Add tabs: Append to the list in the for loop
        """
        tab = QWidget()
        layout = QVBoxLayout(tab)

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
        self.bc_layouts = {}

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
        
        return tab

    def add_bc_row(self, layout, tab_name, label_text=None):
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

    def create_prescribed_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
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
        return tab

    def add_prescribed_tag(self):
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

    def create_output_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
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

        btn_run.clicked.connect(self.save_input_file)
        return tab

    def add_output_row(self, layout, placeholder):
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

    def _browse_file(self, edit):
        path, _ = QFileDialog.getOpenFileName(self, "Select File")
        if path:
            edit.setText(path)
    
    def _combo(self, items):
        c = QComboBox()
        c.addItems(items)
        return c

    def save_input_file(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save Input File", "inputFile.txt", "Text Files (*.txt);;All Files (*)")
        if not path:
            return

        try:
            with open(path, 'w') as f:
                f.write("// Input file for solver\n\n")

                # Geometry
                f.write("// Geometry details\n")
                f.write(f"crdFile = {self.coord_edit.text()}\n")
                f.write(f"cnnFile = {self.conn_edit.text()}\n")
                elem_map = {"4-Node Quadrilateral": "4NodeQuad", "3-Node Triangle": "3NodeTri", "6-Node Triangle": "6NodeTri"}
                f.write(f"elemType = {elem_map.get(self.conn_type.currentText(), '4NodeQuad')}\n\n")

                # Solver
                f.write("// Solver details\n")
                f.write(f"solverType = {self.solver_widgets['sim_type'].currentText().lower()}\n")
                fluid_eqn_map = {"Incompressible Navier-Stokes": "navierStokes", "Compressible NS": "compressibleNS", "Euler": "euler", "Stokes": "stokes"}
                f.write(f"fluidEqn = {fluid_eqn_map.get(self.solver_widgets['fluid_eqn'].currentText(), 'navierStokes')}\n")
                mesh_eqn_map = {"None": "none", "ALE": "ale", "Prescribed": "linearElasticPrescribed", "Linear Elasticity": "linearElastic"}
                f.write(f"meshEqn = {mesh_eqn_map.get(self.solver_widgets['mesh_eqn'].currentText(), 'linearElasticPrescribed')}\n")
                acoustic_eqn_map = {"None": "none", "Linear Acoustics": "linearAcoustics", "LPCE": "lpce", "Helmholtz": "helmholtz", "Wave Equation": "waveEquation"}
                f.write(f"acousticEqn = {acoustic_eqn_map.get(self.solver_widgets['acoustic_eqn'].currentText(), 'none')}\n")
                f.write(f"nDims = {self.solver_widgets['dims'].currentText().replace('D', '')}\n")
                f.write(f"nonLinearIterMin = {self.solver_widgets['nl_min'].value()}\n")
                f.write(f"nonLinearIterMax = {self.solver_widgets['nl_max'].value()}\n")
                f.write(f"nonLinearTolerance = {self.solver_widgets['nl_tol'].value():.6e}\n")
                f.write(f"timeStepSize = {self.solver_widgets['time_step'].value():.6e}\n")
                f.write(f"maxTimeSteps = {self.solver_widgets['max_steps'].value()}\n")
                f.write(f"rhoInfinity = {self.solver_widgets['rho_inf'].value():.6e}\n")
                f.write(f"linearSolver = {self.solver_widgets['lin_solver'].currentText().lower()}\n")
                f.write(f"linearSolverTol = {self.solver_widgets['lin_tol'].value():.6e}\n")
                f.write(f"linearSolverIterMax = {self.solver_widgets['lin_max'].value()}\n")
                f.write(f"linearSolverRstIter = {self.solver_widgets['lin_rst'].value()}\n")
                f.write(f"restartFlag = {1 if self.solver_widgets['restart_flag'].isChecked() else 0}\n")
                f.write(f"restartTsId = {self.solver_widgets['restart_id'].value()}\n")
                f.write(f"restartOutFreq = {self.solver_widgets['rst_freq'].value()}\n")
                f.write(f"outputFileType = {self.solver_widgets['out_type'].currentText()}\n")
                f.write(f"outputStartTimeStep = {self.solver_widgets['out_start'].value()}\n")
                f.write(f"outFreq = {self.solver_widgets['out_freq'].value()}\n")
                f.write(f"intOutFreq = {self.solver_widgets['int_freq'].value()}\n")
                f.write(f"acousticNRBCCentreX = {self.solver_widgets['acoustic_nrbc_x'].value()}\n")
                f.write(f"acousticNRBCCentreY = {self.solver_widgets['acoustic_nrbc_y'].value()}\n")
                f.write(f"acousticNRBCCentreZ = {self.solver_widgets['acoustic_nrbc_z'].value()}\n")
                f.write(f"acousticNRBCInnerRadius = {int(self.solver_widgets['acoustic_nrbc_inner'].value())}\n")
                f.write(f"acousticNRBCOuterRadius = {int(self.solver_widgets['acoustic_nrbc_outer'].value())}\n\n")

                # Fluid properties
                f.write("// Fluid properties\n")
                f.write(f"fluidDens = {self.phys_inputs['rho'].value():.6e}\n")
                f.write(f"fluidVisc = {self.phys_inputs['mu'].value():.6e}\n")
                f.write(f"fluidGamma = {self.phys_inputs['gamma'].value()}\n")
                f.write(f"fluidSpeedOfSound = {int(self.phys_inputs['a'].value())}\n\n")

                # Initial conditions
                f.write("// Initial conditions\n")
                f.write(f"initPres = {self.init_cond_widgets['pres'].value():.6e}\n")
                f.write(f"initXVel = {self.init_cond_widgets['xvel'].value():.6e}\n")
                f.write(f"initYVel = {self.init_cond_widgets['yvel'].value():.6e}\n")
                f.write(f"initZVel = {self.init_cond_widgets['zvel'].value():.6e}\n")
                f.write(f"initXDisp = {self.init_cond_widgets['xdisp'].value():.6e}\n")
                f.write(f"initYDisp = {self.init_cond_widgets['ydisp'].value():.6e}\n")
                f.write(f"initZDisp = {self.init_cond_widgets['zdisp'].value():.6e}\n")
                f.write(f"initPsi = {self.init_cond_widgets['psi'].value():.6e}\n\n")

                # Boundary conditions
                flow_bcs = []
                mesh_bcs = []
                acoustic_bcs = []
                var_map = {"X-velocity": "xVelocity", "Y-velocity": "yVelocity", "Z-velocity": "zVelocity",
                          "X-disp": "xDisp", "Y-disp": "yDisp", "Z-disp": "zDisp", "Acoustic-potential": "acousticPotential"}

                for tab_name, layout in self.bc_layouts.items():
                    var_name = var_map.get(tab_name)
                    is_disp = "disp" in var_name.lower()
                    is_acoustic = "Acoustic" in tab_name
                    
                    for i in range(layout.count()):
                        row_widget = layout.itemAt(i).widget()
                        if not row_widget: continue
                        
                        row_h_layout = row_widget.layout()
                        bc_data = {}
                        bc_data['var'] = var_name
                        bc_data['nodes'] = row_h_layout.itemAt(1).widget().text()
                        type_combo = row_h_layout.itemAt(3).widget()
                        type_text = type_combo.currentText().lower()
                        
                        if type_text == "none": continue
                        
                        bc_data['type'] = type_text
                        bc_data['val'] = row_h_layout.itemAt(5).widget().value()
                        
                        if is_disp:
                            bc_data['tag'] = row_h_layout.itemAt(7).widget().value()
                            mesh_bcs.append(bc_data)
                        elif is_acoustic:
                            acoustic_bcs.append(bc_data)
                        else:
                            flow_bcs.append(bc_data)

                # Write Flow BCs
                f.write("// Flow boundary conditions\n")
                f.write(f"numberBC = {len(flow_bcs)}\n")
                for i, bc in enumerate(flow_bcs):
                    f.write(f"index = {i}\n")
                    f.write(f"type = {bc['type']}\n")
                    f.write(f"var = {bc['var']}\n")
                    f.write(f"nodes = {bc['nodes']}\n")
                    if bc['type'] != 'matchmeshvel':
                         f.write(f"val = {bc['val']}\n")
                f.write("\n")

                # Write Mesh BCs (skip tag 0)
                mesh_bcs_filtered = [bc for bc in mesh_bcs if bc.get('tag', 0) != 0 or bc['type'] != 'prescribed']
                f.write("// Mesh boundary conditions\n")
                f.write(f"numberBC = {len(mesh_bcs_filtered)}\n")
                for i, bc in enumerate(mesh_bcs_filtered):
                    f.write(f"index = {i}\n")
                    final_type = 'prescribed' if bc.get('tag', 0) > 0 else bc['type']
                    f.write(f"type = {final_type}\n")
                    f.write(f"var = {bc['var']}\n")
                    f.write(f"nodes = {bc['nodes']}\n")
                    if final_type == 'prescribed':
                        f.write(f"tag = {bc['tag']}\n")
                    else:
                        f.write(f"val = {bc['val']}\n")
                f.write("\n")
                
                # Write Acoustic BCs
                f.write("// Acoustic boundary conditions\n")
                f.write(f"numberBC = {len(acoustic_bcs)}\n")
                for i, bc in enumerate(acoustic_bcs):
                    f.write(f"index = {i}\n")
                    f.write(f"type = {bc['type']}\n")
                    f.write(f"var = {bc['var']}\n")
                    f.write(f"nodes = {bc['nodes']}\n")
                    f.write(f"val = {bc['val']}\n")
                f.write("\n")

                # Prescribed motion
                f.write("// Prescribed motion details\n")
                f.write(f"numberBC = {len(self.prescribed_tag_rows)}\n")
                for i, group in enumerate(self.prescribed_tag_rows):
                    vbox = group.layout()
                    grid = vbox.itemAt(0).layout()
                    extra_grid = vbox.itemAt(2).layout()
                    
                    def get_val(gl, r, c):
                        return gl.itemAtPosition(r, c).widget().value()

                    f.write(f"tag = {i+1}\n")
                    f.write(f"heaveAmp = {get_val(grid, 0, 1)}\n")
                    f.write(f"heaveFreq = {get_val(grid, 0, 3)}\n")
                    f.write(f"heavePhase = {int(get_val(grid, 0, 5))}\n")
                    f.write(f"pitchAmp = {int(get_val(grid, 1, 1))}\n")
                    f.write(f"pitchFreq = {get_val(grid, 1, 3)}\n")
                    f.write(f"pitchPhase = {int(get_val(grid, 1, 5))}\n")
                    f.write("pitchAxisX = 0\n")
                    f.write("pitchAxisY = 0\n")
                    f.write(f"morphAmp = {int(get_val(grid, 2, 1))}\n")
                    f.write(f"morphFreq = {get_val(grid, 2, 3)}\n")
                    f.write(f"morphPhase = {int(get_val(grid, 2, 5))}\n")
                    f.write(f"morphPos = {int(get_val(extra_grid, 0, 3))}\n")
                    f.write(f"morphDiv = {int(get_val(extra_grid, 0, 1))}\n")
                    f.write(f"LEPosX = {int(get_val(extra_grid, 1, 1))}\n")
                    f.write(f"LEPosY = {int(get_val(extra_grid, 1, 3))}\n")
                    f.write("chordLength = 1\n")
                f.write("\n")

                # Output time history
                f.write("// Output time history details\n")
                probe_rows = []
                for i in range(self.probe_layout.count()):
                    w = self.probe_layout.itemAt(i).widget()
                    if w:
                        txt = w.layout().itemAt(0).widget().text()
                        if txt: probe_rows.append(txt)
                
                f.write(f"numberFiles = {len(probe_rows)}\n")
                for i, txt in enumerate(probe_rows):
                    f.write(f"tag = {i+1}\n")
                    f.write(f"nodes = {txt}\n")
                f.write("\n")

                # Output integrated surface
                f.write("// Output integrated surface details\n")
                surf_rows = []
                for i in range(self.surf_layout.count()):
                    w = self.surf_layout.itemAt(i).widget()
                    if w:
                        txt = w.layout().itemAt(0).widget().text()
                        if txt: surf_rows.append(txt)

                f.write(f"numberFiles = {len(surf_rows)}\n")
                for i, txt in enumerate(surf_rows):
                    f.write(f"tag = {i+1}\n")
                    f.write(f"nodes = {txt}\n")

                f.write("\n// End of input file\n")

        except Exception as e:
            print(f"Error saving file: {e}")
            import traceback
            traceback.print_exc()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = SolverGUI()
    gui.show()
    sys.exit(app.exec())
