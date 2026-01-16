"""
Main entry point for the Fluid-Acoustic Solver GUI application.

This application provides a graphical interface for configuring fluid-acoustic
solver simulations with moving boundaries.

Modular structure:
- Styling is centralized in utils/styles.py
- Helper functions are in utils/helpers.py
- Tab modules are in tabs/ directory
- Each tab is a separate module for easy customization

See README.md for usage instructions.
"""

import sys
import os
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QFileDialog, QTabWidget
)
from PySide6.QtCore import Qt

from utils.styles import get_stylesheet
from tabs.geometry_tab import GeometryTab
from tabs.solver_tab import SolverTab
from tabs.physical_tab import PhysicalTab
from tabs.boundary_tab import BoundaryTab
from tabs.prescribed_tab import PrescribedTab
from tabs.output_tab import OutputTab


class SolverGUI(QWidget):
    """
    Main application window for the Fluid-Acoustic Solver GUI.
    
    This class assembles all modular tab components and handles file generation.
    """
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fluid-Acoustic Solver for Moving Boundaries")
        
        # Apply centralized stylesheet
        self.setStyleSheet(get_stylesheet())
        
        # Set minimum size to ensure visibility
        self.setMinimumSize(1200, 800)

        # Initialize tabs
        self.geometry_tab = GeometryTab(self)
        self.solver_tab = SolverTab(self)
        self.physical_tab = PhysicalTab(self)
        self.boundary_tab = BoundaryTab(self)
        self.prescribed_tab = PrescribedTab(self)
        self.output_tab = OutputTab(self, save_callback=self.save_input_file)
        
        # Link boundary tab to geometry tab for boundary row synchronization
        self.boundary_tab.set_geometry_boundary_rows(self.geometry_tab.boundary_rows)
        
        self.init_ui()

    def init_ui(self):
        """
        Initialize the main user interface.
        
        Creates the main layout with:
        - Title bar
        - Tab widget with 6 tabs
        """
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(10)

        # Title label
        title = QLabel("Fluid-Acoustic Solver for Moving Boundaries")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)

        # Tab widget containing all configuration tabs
        self.tabs = QTabWidget()
        
        # Add all modular tabs
        self.tabs.addTab(self.geometry_tab, "Geometry")
        self.tabs.addTab(self.solver_tab, "Solver")
        self.tabs.addTab(self.physical_tab, "Physical properties")
        self.tabs.addTab(self.boundary_tab, "Boundary conditions")
        self.tabs.addTab(self.prescribed_tab, "Prescribed conditions")
        self.tabs.addTab(self.output_tab, "Output data")
        
        main_layout.addWidget(self.tabs)
        
        # Maximize window after UI is built
        self.showMaximized()
    
    def save_input_file(self):
        """Generate and save the solver input file."""
        path, _ = QFileDialog.getSaveFileName(self, "Save Input File", "inputFile.txt", "Text Files (*.txt);;All Files (*)")
        if not path:
            return

        try:
            with open(path, 'w') as f:
                f.write("// Input file for solver\n\n")

                # Geometry
                f.write("// Geometry details\n")
                f.write(f"crdFile = {self.geometry_tab.get_coord_file()}\n")
                f.write(f"cnnFile = {self.geometry_tab.get_conn_file()}\n")
                elem_map = {"4-Node Quadrilateral": "4NodeQuad", "3-Node Triangle": "3NodeTri", "6-Node Triangle": "6NodeTri"}
                f.write(f"elemType = {elem_map.get(self.geometry_tab.get_conn_type(), '4NodeQuad')}\n\n")

                # Solver
                solver_widgets = self.solver_tab.get_solver_data()
                f.write("// Solver details\n")
                f.write(f"solverType = {solver_widgets['sim_type'].currentText().lower()}\n")
                fluid_eqn_map = {"Incompressible Navier-Stokes": "navierStokes", "Compressible NS": "compressibleNS", "Euler": "euler", "Stokes": "stokes"}
                f.write(f"fluidEqn = {fluid_eqn_map.get(solver_widgets['fluid_eqn'].currentText(), 'navierStokes')}\n")
                mesh_eqn_map = {"None": "none", "ALE": "ale", "Prescribed": "linearElasticPrescribed", "Linear Elasticity": "linearElastic"}
                f.write(f"meshEqn = {mesh_eqn_map.get(solver_widgets['mesh_eqn'].currentText(), 'linearElasticPrescribed')}\n")
                acoustic_eqn_map = {"None": "none", "Linear Acoustics": "linearAcoustics", "LPCE": "lpce", "Helmholtz": "helmholtz", "Wave Equation": "waveEquation"}
                f.write(f"acousticEqn = {acoustic_eqn_map.get(solver_widgets['acoustic_eqn'].currentText(), 'none')}\n")
                f.write(f"nDims = {solver_widgets['dims'].currentText().replace('D', '')}\n")
                f.write(f"nonLinearIterMin = {solver_widgets['nl_min'].value()}\n")
                f.write(f"nonLinearIterMax = {solver_widgets['nl_max'].value()}\n")
                f.write(f"nonLinearTolerance = {solver_widgets['nl_tol'].value():.6e}\n")
                f.write(f"timeStepSize = {solver_widgets['time_step'].value():.6e}\n")
                f.write(f"maxTimeSteps = {solver_widgets['max_steps'].value()}\n")
                f.write(f"rhoInfinity = {solver_widgets['rho_inf'].value():.6e}\n")
                f.write(f"linearSolver = {solver_widgets['lin_solver'].currentText().lower()}\n")
                f.write(f"linearSolverTol = {solver_widgets['lin_tol'].value():.6e}\n")
                f.write(f"linearSolverIterMax = {solver_widgets['lin_max'].value()}\n")
                f.write(f"linearSolverRstIter = {solver_widgets['lin_rst'].value()}\n")
                f.write(f"restartFlag = {1 if solver_widgets['restart_flag'].isChecked() else 0}\n")
                f.write(f"restartTsId = {solver_widgets['restart_id'].value()}\n")
                f.write(f"restartOutFreq = {solver_widgets['rst_freq'].value()}\n")
                f.write(f"outputFileType = {solver_widgets['out_type'].currentText()}\n")
                f.write(f"outputStartTimeStep = {solver_widgets['out_start'].value()}\n")
                f.write(f"outFreq = {solver_widgets['out_freq'].value()}\n")
                f.write(f"intOutFreq = {solver_widgets['int_freq'].value()}\n")
                f.write(f"acousticNRBCCentreX = {solver_widgets['acoustic_nrbc_x'].value()}\n")
                f.write(f"acousticNRBCCentreY = {solver_widgets['acoustic_nrbc_y'].value()}\n")
                f.write(f"acousticNRBCCentreZ = {solver_widgets['acoustic_nrbc_z'].value()}\n")
                f.write(f"acousticNRBCInnerRadius = {int(solver_widgets['acoustic_nrbc_inner'].value())}\n")
                f.write(f"acousticNRBCOuterRadius = {int(solver_widgets['acoustic_nrbc_outer'].value())}\n\n")

                # Fluid properties
                phys_inputs = self.physical_tab.get_physical_data()
                f.write("// Fluid properties\n")
                f.write(f"fluidDens = {phys_inputs['rho'].value():.6e}\n")
                f.write(f"fluidVisc = {phys_inputs['mu'].value():.6e}\n")
                f.write(f"fluidGamma = {phys_inputs['gamma'].value()}\n")
                f.write(f"fluidSpeedOfSound = {int(phys_inputs['a'].value())}\n\n")

                # Initial conditions
                init_cond_widgets = self.boundary_tab.get_initial_conditions()
                f.write("// Initial conditions\n")
                f.write(f"initPres = {init_cond_widgets['pres'].value():.6e}\n")
                f.write(f"initXVel = {init_cond_widgets['xvel'].value():.6e}\n")
                f.write(f"initYVel = {init_cond_widgets['yvel'].value():.6e}\n")
                f.write(f"initZVel = {init_cond_widgets['zvel'].value():.6e}\n")
                f.write(f"initXDisp = {init_cond_widgets['xdisp'].value():.6e}\n")
                f.write(f"initYDisp = {init_cond_widgets['ydisp'].value():.6e}\n")
                f.write(f"initZDisp = {init_cond_widgets['zdisp'].value():.6e}\n")
                f.write(f"initPsi = {init_cond_widgets['psi'].value():.6e}\n\n")

                # Boundary conditions
                flow_bcs = []
                mesh_bcs = []
                acoustic_bcs = []
                var_map = {"X-velocity": "xVelocity", "Y-velocity": "yVelocity", "Z-velocity": "zVelocity",
                          "X-disp": "xDisp", "Y-disp": "yDisp", "Z-disp": "zDisp", "Acoustic-potential": "acousticPotential"}

                bc_layouts = self.boundary_tab.get_boundary_conditions()
                for tab_name, layout in bc_layouts.items():
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
                prescribed_tag_rows = self.prescribed_tab.get_prescribed_tags()
                f.write("// Prescribed motion details\n")
                f.write(f"numberBC = {len(prescribed_tag_rows)}\n")
                for i, group in enumerate(prescribed_tag_rows):
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
                probe_layout = self.output_tab.get_probe_layout()
                f.write("// Output time history details\n")
                probe_rows = []
                for i in range(probe_layout.count()):
                    w = probe_layout.itemAt(i).widget()
                    if w:
                        txt = w.layout().itemAt(0).widget().text()
                        if txt: probe_rows.append(txt)
                
                f.write(f"numberFiles = {len(probe_rows)}\n")
                for i, txt in enumerate(probe_rows):
                    f.write(f"tag = {i+1}\n")
                    f.write(f"nodes = {txt}\n")
                f.write("\n")

                # Output integrated surface
                surf_layout = self.output_tab.get_surf_layout()
                f.write("// Output integrated surface details\n")
                surf_rows = []
                for i in range(surf_layout.count()):
                    w = surf_layout.itemAt(i).widget()
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


def main():
    """
    Main application entry point.
    
    Creates and displays the SolverGUI window.
    """
    app = QApplication(sys.argv)
    
    # Create main window
    window = SolverGUI()
    window.show()
    
    # Start event loop
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
