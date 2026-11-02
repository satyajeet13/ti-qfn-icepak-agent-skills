"""Create one box body and explicit box contacts in an existing Icepak app.

Coordinates and dimensions are finite numbers in millimetres in Global CS.
No defaults are supplied for geometry, materials, positioning, or thickness.
This is a small execution helper, not a drawing parser or full package model.
"""
import math
import re


def _vector(v, label, positive=False):
    if not isinstance(v, (list, tuple)) or len(v) != 3:
        raise ValueError(f'{label} must have three numbers')
    if any(isinstance(x, bool) or not isinstance(x, (int, float)) or not math.isfinite(x) for x in v):
        raise ValueError(f'{label} must contain finite numbers')
    if positive and any(x <= 0 for x in v):
        raise ValueError(f'{label} must be positive')
    return [float(x) for x in v]


def _box(v):
    if not isinstance(v, dict) or set(v) != {'name', 'origin', 'size', 'material'}:
        raise ValueError('Each box requires name, origin, size, and material')
    name, material = v['name'], v['material']
    if not isinstance(name, str) or not re.fullmatch(r'[A-Za-z][A-Za-z0-9_]*', name):
        raise ValueError('Use ASCII letters, digits and underscores for object names')
    if not isinstance(material, str) or not material.strip():
        raise ValueError('Material name is required')
    origin, size = _vector(v['origin'], 'origin'), _vector(v['size'], 'size', True)
    upper = [a + b for a, b in zip(origin, size)]
    if not all(math.isfinite(x) for x in upper):
        raise ValueError('Coordinate overflow')
    return {'name': name, 'origin': origin, 'size': size, 'material': material, 'upper': upper}


def _overlap(a, b):
    return all(a['origin'][i] < b['upper'][i] and b['origin'][i] < a['upper'][i] for i in range(3))


def build(app, body, contacts):
    """Create explicit rectangular solids, subtracting contacts from body.

    body and each contact are dicts with name, origin, size, material. The body
    is one box; contacts may overlap it but may not overlap each other. Contacts
    outside the body are not subtracted. No existing geometry checks except name
    collisions. Does not save, set up physics or delete/rollback on failure.
    Returns created names. Caller must verify geometry and interfaces in AEDT.
    """
    b = _box(body)
    if not isinstance(contacts, list):
        raise ValueError('contacts must be a list')
    cs = [_box(v) for v in contacts]
    boxes = [b] + cs
    names = [v['name'].lower() for v in boxes]
    if len(names) != len(set(names)):
        raise ValueError('Duplicate object names')
    for i, a in enumerate(cs):
        for other in cs[i + 1:]:
            if _overlap(a, other):
                raise ValueError(f"Contacts overlap: {a['name']} and {other['name']}")
    if getattr(app, 'design_type', None) != 'Icepak':
        raise ValueError('Expected Icepak app')
    if str(app.modeler.get_working_coordinate_system()).lower() != 'global':
        raise ValueError('Expected Global working coordinate system')
    present = {str(n).lower() for n in app.modeler.object_names}
    if any(n in present for n in names):
        raise ValueError('Object name collision in active design')
    for material in sorted({v['material'] for v in boxes}):
        if not app.materials.exists_material(material):
            raise ValueError('Material unavailable: ' + material)
    created = []
    try:
        for item in boxes:
            to_mm = lambda x: f'{x:.17g}mm'
            obj = app.modeler.create_box([to_mm(x) for x in item['origin']],
                                         [to_mm(x) for x in item['size']],
                                         name=item['name'], material=item['material'])
            if not obj:
                raise RuntimeError('create_box failed: ' + item['name'])
            created.append(str(obj.name))
            if obj.name != item['name'] or str(obj.material_name).strip('"').lower() != item['material'].lower():
                raise RuntimeError('Unexpected name or material on ' + item['name'])
        cutters = [c['name'] for c in cs if _overlap(b, c)]
        if cutters and not app.modeler.subtract(b['name'], cutters, keep_originals=True):
            raise RuntimeError('Body subtraction failed')
    except Exception as exc:
        raise RuntimeError(f'Build failed; created so far: {created!r}. Inspect for further partial objects. {exc}') from exc
    return {'created': created, 'subtracted_from_body': [c['name'] for c in cs if _overlap(b, c)],
            'saved': False, 'note': 'Verify actual solids, dimensions, materials and interfaces in AEDT.'}
