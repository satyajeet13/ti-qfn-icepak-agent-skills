"""Small, unit-agnostic placement helpers. Values must share one length unit.

These functions return coordinates; they do not create or modify AEDT objects.
Use only if the drawing's actual layout matches the stated assumptions.
"""
import math


def _number(value, name, positive=False):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(f"{name} must be a finite number")
    if positive and value <= 0:
        raise ValueError(f"{name} must be positive")
    return float(value)


def qfn_centers(body_x, body_y, count_x, count_y, pitch_x, pitch_y, inset_x, inset_y):
    """Return (side, index, x, y) for centered, symmetric side arrays.

    Origin is body center. count_x is contacts on EACH horizontal side, count_y
    is contacts on EACH vertical side. inset_x/y measure edge to contact CENTER;
    they must be derived from the chosen terminal representation and drawing.
    side indices increase with x for south/north, y for west/east. They are NOT
    pin numbers. Top/bottom view, pin numbering, z, and contact size are caller's
    responsibility. No corner-pad or staggered layouts are supported.
    """
    bx, by = _number(body_x, 'body_x', True), _number(body_y, 'body_y', True)
    px, py = _number(pitch_x, 'pitch_x', True), _number(pitch_y, 'pitch_y', True)
    ix, iy = _number(inset_x, 'inset_x'), _number(inset_y, 'inset_y')
    if any(type(n) is not int or n <= 0 for n in (count_x, count_y)):
        raise ValueError('contact counts must be positive integers')
    if not 0 <= ix < bx / 2 or not 0 <= iy < by / 2:
        raise ValueError('insets must lie between edge and center')
    if (count_x - 1) * px >= bx or (count_y - 1) * py >= by:
        raise ValueError('contact centers extend beyond body')
    result = []
    for side, y in [('south', -by / 2 + iy), ('north', by / 2 - iy)]:
        for i in range(count_x):
            result.append((side, i, (i - (count_x - 1) / 2) * px, y))
    for side, x in [('west', -bx / 2 + ix), ('east', bx / 2 - ix)]:
        for i in range(count_y):
            result.append((side, i, x, (i - (count_y - 1) / 2) * py))
    return result


