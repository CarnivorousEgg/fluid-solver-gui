# Usage Guide

## Application Overview

The Solver GUI provides a tabbed interface for configuring fluid-acoustic simulations. Each tab handles a specific aspect of the configuration.

---

## Tabs Overview

### 1. Geometry Tab
Configure mesh and boundary files.

**Fields:**
- **Coordinate file**: Node coordinates file (.crd)
- **Connectivity file**: Element connectivity (.cnn)
- **Connectivity type**: Element type (4-Node Quad, 3-Node Triangle, etc.)
- **Boundary Files**: List of boundary condition files

**Actions:**
- Click "Browse" to select files
- Click "+ Add Boundary File" to add more boundaries
- Click "✕" to remove boundary files (minimum 1 required)

---

### 2. Solver Tab
Configure solver parameters.

**Sections:**

**General Settings:**
- Simulation type: Transient or Steady
- Fluid equation: Navier-Stokes, Euler, Stokes, etc.
- Mesh equation: ALE, Prescribed, Linear Elasticity
- Acoustic equation: LPCE, Helmholtz, Wave Equation
- Dimensions: 2D or 3D

**Non-linear Iterations:**
- Min/Max iterations
- Tolerance

**Linear Solver:**
- Solver type: GMRES, BiCGSTAB, Direct
- Tolerance, max iterations, restart iterations

**Time Integration:**
- Time-step size
- Max time steps
- Temporal damping (rho infinity)
- Restart options

**Output Configuration:**
- Output file type: plt, vtk, csv
- Output start step, frequency
- Integrated output frequency
- Restart output frequency

**Acoustic NRBC Parameters:**
- Centre X, Y, Z coordinates
- Inner and outer radius

---

### 3. Physical Properties Tab
Set fluid parameters.

**Parameters:**
- Fluid density (kg/m³)
- Fluid characteristic velocity (m/s)
- Dynamic viscosity (Pa·s)
- Characteristic length (m)
- Ratio of specific heats
- Speed of sound (m/s)

**Calculator:**
- Click "Check non-dimensional numbers"
- View Reynolds and Mach numbers

---

### 4. Boundary Conditions Tab

**Initial Conditions:**
Set default values for:
- Pressure
- X, Y, Z velocity
- X, Y, Z displacement
- Psi (acoustic potential)

**Boundary Condition Tabs:**
Configure conditions for each variable:
- X-velocity, Y-velocity, Z-velocity
- X-disp, Y-disp, Z-disp  
- Acoustic-potential

**For each boundary:**
- Boundary Name/ID: File reference
- Type: None, Dirichlet, matchMeshVel (velocity), prescribed (displacement)
- Value: Boundary value
- Tag: Prescribed motion tag (for displacement with prescribed type)

**Actions:**
- Click "+ Add Boundary Condition" to add rows
- Click "✕" to remove rows
- Rows auto-number as B-1, B-2, etc.

---

### 5. Prescribed Conditions Tab
Configure prescribed motions for moving boundaries.

**For each tag:**
- **Heave**: Amplitude, Frequency, Phase
- **Pitch**: Amplitude, Frequency, Phase
- **Morph**: Amplitude, Frequency, Phase
- **Morph divisions**: Number of divisions
- **Morph position**: Position parameter
- **Leading edge X, Y**: Coordinates

**Actions:**
- Click "+ Add Prescribed Condition Tag" for more motion groups
- Each tag corresponds to tag numbers in displacement boundary conditions

---

### 6. Output Data Tab

**Time History Data (Probes):**
- Add probe file locations
- Click "+ Add Probe File"
- Enter node file paths

**Integrated Surface Forces Data:**
- Add surface output files
- Click "+ Add Surface Forces File"
- Enter boundary file paths

**Generate Output:**
- Click "Complete the pre-processing"
- Choose save location
- Generates inputFile.txt

---

## Workflow

### Basic Workflow

1. **Geometry Tab**
   - Load coordinate and connectivity files
   - Add boundary files (inlet, outlet, walls, etc.)

2. **Solver Tab**
   - Select simulation type and equations
   - Set time integration parameters
   - Configure output settings

3. **Physical Properties Tab**
   - Enter fluid properties
   - Check non-dimensional numbers

4. **Boundary Conditions Tab**
   - Set initial conditions
   - Configure boundary conditions for each variable
   - Match boundary names to geometry files

5. **Prescribed Conditions Tab** (if using moving boundaries)
   - Define motion parameters
   - Set tags matching displacement BCs

6. **Output Data Tab**
   - Add probe locations
   - Add surface output files
   - Generate input file

---

## Output File Format

The generated file follows this structure:

```
// Geometry details
crdFile = ...
cnnFile = ...
elemType = ...

// Solver details
solverType = ...
fluidEqn = ...
...

// Physical properties
fluidDens = ...
fluidVisc = ...

// Initial conditions
initPres = ...
initXVel = ...
...

// Flow boundary conditions
numberBC = ...
index = 0
type = ...
var = ...
nodes = ...
val = ...

// Mesh boundary conditions
...

// Acoustic boundary conditions
...

// Prescribed motion details
...

// Output time history details
...

// Output integrated surface details
...
```

---

## Tips

- **Save frequently**: Use File > Save or generate output file regularly
- **Boundary names**: Use descriptive names matching your mesh files
- **Tag 0**: Displacement boundaries with tag=0 are treated as Dirichlet, not prescribed
- **File paths**: Use absolute paths or paths relative to where you'll run the solver
- **Validation**: Check Reynolds/Mach numbers to verify your setup

---

## Next Steps

- [Customization Guide](CUSTOMIZATION.md) - Modify the application
- [Troubleshooting](TROUBLESHOOTING.md) - Solve common issues
