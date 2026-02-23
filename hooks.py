from odoo import api, SUPERUSER_ID


def post_init_copy_legacy_to_base(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})

    PT = env["product.template"].sudo()

    # Template
    template_map = [
        ("x_pasillo", "sid_pasillo"),
        ("x_alto", "sid_alto"),
        ("x_lado", "sid_lado"),
        ("x_largo", "sid_largo"),
    ]

    for src, dst in template_map:
        if src in PT._fields and dst in PT._fields:
            records = PT.search([(src, "!=", False)])
            for rec in records:
                if rec[src] and rec[dst] != rec[src]:
                    rec.write({dst: rec[src]})
