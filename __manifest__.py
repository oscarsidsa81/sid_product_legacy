# -*- coding: utf-8 -*-
{
    "name": "sid_product_legacy",
    "summary": "Migración de datos x_* hacia sid_* (sin redefinir Studio).",
    "version": "15.0.1.0.1",
    "category": "Inventory/Inventory",
    "author": "oscarsidsa81",
    "license": "LGPL-3",
    "depends": ["sid_product_base"],
    "data": [],
    "post_init_hook": "post_init_copy_legacy_to_base",
    "installable": True,
    "application": False,
    "auto_install": False,
}
