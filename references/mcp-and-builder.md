# MCP execution and rectangular helper

Use the actual tools exposed by the installed `ansys-aedt-mcp`. `run_python_code` executes in a persistent Python session containing `desktop`. Verify project and Icepak design first, then obtain the app as shown in the official extension pattern:

```python
from ansys.aedt.core import get_pyaedt_app
project = desktop.active_project()
if not project or project.GetName() != "EXPECTED_PROJECT":
    raise RuntimeError("Unexpected active project")
design = desktop.active_design(project)
if not design or design.GetName() != "EXPECTED_DESIGN" or design.GetDesignType() != "Icepak":
    raise RuntimeError("Unexpected active design")
app = get_pyaedt_app(design_name=design.GetName(), desktop=desktop)
if not app or app.project_name != "EXPECTED_PROJECT" or app.design_name != "EXPECTED_DESIGN":
    raise RuntimeError("Unexpected PyAEDT attachment")
```

For an agreed rectangular model, put `scripts` on the **MCP host's** Python path, then call `build(app, body, contacts)` from `rectangular_package`. Each box is exactly `{"name": "...", "origin": [x,y,z], "size": [dx,dy,dz], "material": "..."}` with numbers in mm. `contacts` is a list of those dictionaries; include all explicitly located terminals and, if represented by a box, the pad. Derive their values from the drawing and user choices; no example values here are valid defaults. The helper checks Global CS, design type, materials, names and contact-contact box overlap; creates boxes and subtracts overlapping contacts from the body with `keep_originals=True`. It does not examine other existing geometry or the Region, resolve non-box shapes, verify real thermal properties, check interface contact, save, set up physics or roll back. Subtraction can fail or leave an invalid solid; check AEDT after every build.

Use `placements.qfn_centers` only for an explicitly symmetric centered layout. It returns side/index/XY coordinates, not pin numbering; caller determines view transformation, z, material, thickness and all dimensions. For nonuniform and dual-row layouts, generate explicit contact boxes from the drawing instead.

PyAEDT docs: https://aedt.docs.pyansys.com/version/stable/API/_autosummary/ansys.aedt.core.modeler.modeler_3d.Modeler3D.create_box.html ; https://aedt.docs.pyansys.com/version/stable/API/_autosummary/ansys.aedt.core.modeler.modeler_3d.Modeler3D.subtract.html ; https://aedt-mcp.docs.pyansys.com/version/stable/user_guide/tools_and_capabilities.html .
