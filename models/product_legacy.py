from odoo import fields, models

class ProductTemplate(models.Model):
    _inherit = "product.template"

    x_pasillo = fields.Selection(string="Pasillo (legacy)")
    x_alto = fields.Selection(string="Alto (legacy)")
    x_lado = fields.Selection(string="Lado (legacy)")
    x_largo = fields.Selection(string="Largo (legacy)")

class ProductProduct(models.Model):
    _inherit = "product.product"

    x_pasillo = fields.Selection(string="Pasillo (legacy)")
    x_forecast_madrid = fields.Float(string="Forecast Madrid (legacy)")
