from odoo import api, SUPERUSER_ID


def post_init_copy_legacy_to_base(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})

    PT = env["product.template"].sudo()
    Opt = env["sid.location.option"].sudo()

    mapping = [
        ("x_pasillo", "sid_pasillo", "pasillo"),
        ("x_alto",    "sid_alto",    "alto"),
        ("x_lado",    "sid_lado",    "lado"),
        ("x_largo",   "sid_largo",   "largo"),
    ]

    for src, dst, ltype in mapping:
        if src not in PT._fields or dst not in PT._fields:
            continue

        # solo rellenar si destino vacío
        records = PT.search([(src, "!=", False), (dst, "=", False)])

        # prefetch de valores distintos
        values = {rec[src] for rec in records if rec[src]}
        if not values:
            continue

        # index por code (y por name por si acaso)
        opts = Opt.search([("location_type", "=", ltype), ("code", "in", list(values))])
        by_code = {o.code: o.id for o in opts}
        # fallback: si viniera etiqueta en legacy
        opts2 = Opt.search([("location_type", "=", ltype), ("name", "in", list(values))])
        by_name = {o.name: o.id for o in opts2}

        for rec in records:
            v = rec[src]
            opt_id = by_code.get(v) or by_name.get(v)
            if opt_id:
                rec.write({dst: opt_id})