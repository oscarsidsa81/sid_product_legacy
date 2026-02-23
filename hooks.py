from odoo import api, SUPERUSER_ID


def post_init_copy_legacy_to_base(cr, registry):
    """
    Post-init hook: copia valores legacy x_* a sid_*.
    - NO sobrescribe si el destino ya está informado.
    - Si el destino es Selection, intenta mapear etiqueta -> clave (si ya viene como clave, la deja).
    - Escribe en batch agrupando por valor.
    """
    env = api.Environment(cr, SUPERUSER_ID, {})
    PT = env["product.template"].sudo()

    template_map = [
        ("x_pasillo", "sid_pasillo"),
        ("x_alto", "sid_alto"),
        ("x_lado", "sid_lado"),
        ("x_largo", "sid_largo"),
    ]

    def selection_label_to_key(dst_field, value):
        selection = dst_field.selection
        if callable(selection):
            selection = selection(env)  # por robustez

        key_to_label = dict(selection or [])
        label_to_key = {label: key for key, label in key_to_label.items()}

        if value in key_to_label:
            return value
        if value in label_to_key:
            return label_to_key[value]
        return value  # desconocido: no inventamos

    for src, dst in template_map:
        if src not in PT._fields or dst not in PT._fields:
            continue

        dst_field = PT._fields[dst]

        # No machacar: solo copiar cuando dst está vacío
        records = PT.search([(src, "!=", False), (dst, "=", False)])

        buckets = {}  # val -> recordset
        for rec in records:
            val = rec[src]
            if not val:
                continue

            if dst_field.type == "selection":
                val = selection_label_to_key(dst_field, val)

            # unir recordsets correctamente
            rs = buckets.get(val)
            if rs is None:
                buckets[val] = rec
            else:
                buckets[val] = rs | rec

        for val, rs in buckets.items():
            rs.write({dst: val})