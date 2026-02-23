from odoo import api, SUPERUSER_ID


def post_init_copy_legacy_to_base(cr, registry):
    """
    Post-init hook: copia valores legacy x_* a los campos sid_* del módulo base.
    - NO sobrescribe si el destino ya está informado.
    - Si el destino es Selection, intenta mapear etiqueta -> clave (y deja la clave tal cual si ya viene como clave).
    - Escribe en batch para rendimiento.
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
        """
        Para fields.Selection:
        - si value coincide con una etiqueta, devuelve su clave.
        - si ya coincide con una clave, lo devuelve tal cual.
        - si no coincide con nada, devuelve el valor tal cual (no inventa).
        """
        # selection puede ser callable; en post_init solemos tenerlo ya materializado,
        # pero por robustez lo soportamos si fuera callable.
        selection = dst_field.selection
        if callable(selection):
            selection = selection(env)

        # selection: [(key, label), ...]
        key_to_label = dict(selection or [])
        label_to_key = {label: key for key, label in key_to_label.items()}

        if value in key_to_label:
            return value  # ya es clave
        if value in label_to_key:
            return label_to_key[value]  # venía como etiqueta
        return value  # desconocido: no tocamos (lo validará ORM si procede)

    for src, dst in template_map:
        if src not in PT._fields or dst not in PT._fields:
            continue

        dst_field = PT._fields[dst]

        # Solo los que tienen src informado y dst vacío: no machacamos
        domain = [(src, "!=", False), (dst, "=", False)]
        records = PT.search(domain)

        # batch write: agrupamos por valor destino final
        bucket = {}  # mapped_value -> recordset
        for rec in records:
            val = rec[src]
            if not val:
                continue

            # Si destino es selection, intentamos convertir etiqueta->clave
            if dst_field.type == "selection":
                val = selection_label_to_key(dst_field, val)

            bucket.setdefault(val, PT.browse()). |= rec

        for val, rs in bucket.items():
            if rs:
                rs.write({dst: val})