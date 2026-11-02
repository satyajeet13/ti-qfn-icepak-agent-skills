# Texas Instruments QFN drawing references

The supplied catalog https://www.ti.com/packaging/docs/searchtipackages.tsp?packageName=QFN listed 405 options when checked on 2026-11-01, but its complete result table was not accessible to this research session. This is not an exhaustive catalog or a claim that all drawings were inspected. The following example drawing pages were inspected visually; always use the user's actual part drawing.

- [RTW0024B WQFN, qfnd062](https://www.ti.com/lit/pdf/qfnd062): 24 perimeter terminals, an exposed pad labeled 25, and a separate example board layout. Verify whether the count refers to signal terminals or includes the pad in each actual document.
- [RAK0009A WQFN-HR, mpqf742e](https://www.ti.com/lit/pdf/mpqf742e): irregular terminal features and an optional side-wall wettable-flank detail. Verify whether the selected physical package has that option. Do not assume a symmetric 4-side layout.
- [RZW0020A WQFN-HR, mpqf714](https://www.ti.com/lit/pdf/mpqf714): distinct terminal groups and dimensions. Its separate example board layout is not a source of package terminal dimensions.
- [RUB 24-terminal QFN, mpqf211](https://www.ti.com/lit/pdf/mpqf211): earlier mechanical drawing format; the outline is graphical and plain-text extraction may miss it.

Selected TI drawings state that parenthesized dimensions are for reference; check the notes on the drawing actually supplied. TI catalog data may contain missing or zero pitch and short package codes may recur across pin counts. Do not treat missing/zero catalog entries or marketing descriptions as drawing geometry. Catalog descriptions, carrier pack dimensions and PCB land patterns are not replacements for a package outline.
