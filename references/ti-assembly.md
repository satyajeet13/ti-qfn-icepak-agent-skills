# TI QFN attachment and thermal context

Source: Texas Instruments [QFN and SON PCB Attachment, SLUA271C](https://www.ti.com/lit/pdf/slua271), revised December 2023. This skill handles QFN only. The application note is general board-attachment guidance; the actual mechanical drawing controls package geometry.

The note describes the heat path from an exposed pad through solder into the PCB and its copper/vias (§3.4), and describes assembly-dependent joints, stencil and potential voids (§4). Those features must not be fabricated from a generic drawing when building a package alone. Do not equate land patterns, stencil apertures, pre-reflow paste coverage, post-reflow solder geometry and package metal geometry. Obtain the actual PCB, assembly and interface information before modeling a mounted package. Suggested via and assembly values are not universal package defaults.

Reported theta-JA data depends on test-board conditions; use the actual data sheet's conditions and do not convert junction-to-ambient resistance into a bulk material conductivity. A geometry-only model with no actual die, power, board and boundary conditions does not validate thermal behavior.
