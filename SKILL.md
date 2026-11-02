---
name: ti-qfn-icepak
description: Read a user-provided Texas Instruments QFN mechanical drawing and create a simplified package model and material assignments in Ansys AEDT Icepak using the PyAEDT MCP server. Use for TI QFN package outlines including VQFN, WQFN, multi-row and wettable-flank variants.
---

# TI QFN package geometry in Icepak

The user supplies a mechanical drawing. Use the drawing for the exact package as the source of geometry; package family, catalog entries and general application notes are not dimensional templates. This skill handles QFN packages. If the part is SON, DFN, QFP or another family, state the mismatch and request a suitable skill. Create the requested package geometry and materials only; do not automatically add a PCB, solder, die, thermal loads, solve setup, mesh or boundaries.

## Read the actual drawing

1. Identify the complete package drawing identifier, family, pin count, drawing number and revision; cross-check against the user's exact device. Short TI package names can correspond to different counts or variants. Read outline, section, detail and note pages visually, not PDF text alone. Distinguish package outline from example PCB layout, stencil and carrier tape/reel. Do not use land or tape dimensions as package dimensions.
2. Record the units, body dimensions, seated height and seating plane; terminal counts, widths, lengths, locations, pitches and rows; exposed pad shapes and locations; pin-1 orientation; and actual optional or wettable-flank details. Map each value to its figure/page and min, max, nominal, reference or derived status. Apply only notes belonging to that drawing; values in parentheses are reference-only where its notes say so. Do not interpret GD&T callouts as dimensions.
3. Establish +Z, XY origin, top/bottom view transform and rotation; verify pin 1 and row/terminal numbering. No assumptions that the body is square, contacts are identical, every side has the same count, all contacts are perimeter contacts, or a central pad exists. Read the drawing's numbering to determine whether a pad is numbered separately from signal terminals. Pin-count labels alone do not imply a four-way division.
4. If an image or dimension is ambiguous, unreadable, missing, contradictory or has multiple alternatives, ask for the applicable detail or variant. Use a stated nominal when available; if only limits are given, propose a midpoint as a modeling choice. Mark reference and calculated values separately. Do not infer terminal thickness from clearance, or actual construction, die size, metal composition or thermal properties from a package silhouette.

## Agree a model

Give a short plan with source and selected values, coordinate convention, materials, expected features, assumptions and omissions. Ask only for missing decisions that block the requested representation. A body envelope can be built without internal dimensions if accepted; material choice still needs to be supplied or approved.

- **Envelope:** body box, with height relative to the actual seating plane. Explicitly label as an effective external model with no individual terminals or internal thermal path.
- **External contacts:** body plus actual terminal groups and drawn pad(s). A rectangular solid approximation requires actual thickness or an accepted modeling assumption. Preserve irregular or multi-row layouts and pin-1 orientation. Use sidewall, step or dimple geometry only from the relevant drawing detail; do not assume an optional feature applies.
- **Higher detail:** create additional solids only from part-specific evidence or user-provided dimensions and materials. Use boxes, other PyAEDT primitives and Booleans as appropriate; if the geometry cannot be established, ask instead of inventing it.

Where metal occupies the body envelope, subtract the metal volumes from the body while retaining each metal solid, or partition the body without overlap. Validate the resulting shapes and interfaces. The TI note SLUA271 discusses actual board attachment and thermal paths, not package dimensions. It does not determine the user's actual solder geometry, PCB via layout or joint void fraction. When a board-level model is requested, gather the user's stackup, vias, solder, contact and boundary conditions separately. Do not turn thermal resistance or generic assembly guidance into material conductivity, or copy a note's example values to another device. Do not call an outline model a validated thermal model.

## Execute with PyAEDT MCP

- Check MCP server tools and connection; verify intended existing project and Icepak design before any edit. Confirm the working coordinate system and name collisions. Use `run_python_code` with the documented persistent `desktop`; `run_python_script` is asynchronous and requires completion/log checks. Files must exist on the MCP host. Do not close or solve the project.
- Use explicit-length-unit PyAEDT primitives and the user's approved materials. Check materials exist and inspect their actual assigned names and thermal properties. Invalid material names can fall back to a default.
- `scripts/placements.py` gives side centers for a symmetric centered group only when the actual drawing supports that layout. Side indices are not pin numbers. For irregular, two-row or unequal patterns, generate explicit box coordinates from the drawing.
- `scripts/rectangular_package.py` creates a single body box plus explicit terminal/pad boxes and subtracts intersecting metal boxes from the body, retaining them. Use only if the representation and the drawn geometry support its assumptions; the helper does not infer dimensions, map pins or detect intersections with existing solids. Read `references/mcp-and-builder.md` first. For other profiles use verified PyAEDT primitives/Booleans or request an acceptable simplification.
- Check every return and actual object/material names. Errors can leave partial geometry: report created names, inspect before retrying, and never silently delete existing work.

## Verify and report

Compare the model against the specific source and plan: body and pad bounds; Z/seating plane; every contact row, count, location, pitch, dimensions and pin-1 orientation; material assignments and physical properties; overlaps and metal/body interfaces; clearance to other geometry and Region. Use model info, numeric bounding boxes and screenshot where available; screenshot alone does not verify dimensions. Report source/revision, choices and assumptions, omitted details, created objects, checks actually performed, and confirmed save status. Do not claim build, contact physics, simulation or save without evidence.

Read `references/ti-drawings.md` for inspected examples and catalog coverage; `references/ti-assembly.md` for TI attachment guidance and its limits; `references/mcp-and-builder.md` for the PyAEDT integration and helper limitations.
