from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def _selection_from_db(self, field_name):
        fld = self.env["ir.model.fields"].sudo().search([
            ("model", "=", self._name),
            ("name", "=", field_name),
        ], limit=1)
        if not fld:
            return []
        sels = self.env["ir.model.fields.selection"].sudo().search(
            [("field_id", "=", fld.id)],
            order="sequence, id",
        )
        return [(s.value, s.name) for s in sels]

    @api.model
    def _sel_x_pasillo(self):
        return self._selection_from_db("x_pasillo")

    @api.model
    def _sel_x_alto(self):
        return self._selection_from_db("x_alto")

    @api.model
    def _sel_x_lado(self):
        return self._selection_from_db("x_lado")

    @api.model
    def _sel_x_largo(self):
        return self._selection_from_db("x_largo")

    x_pasillo = fields.Selection(selection="_sel_x_pasillo", string="Pasillo (legacy)")
    x_alto = fields.Selection(selection="_sel_x_alto", string="Alto (legacy)")
    x_lado = fields.Selection(selection="_sel_x_lado", string="Lado (legacy)")
    x_largo = fields.Selection(selection="_sel_x_largo", string="Largo (legacy)")


class ProductProduct(models.Model):
    _inherit = "product.product"

    def _selection_from_db(self, field_name):
        fld = self.env["ir.model.fields"].sudo().search([
            ("model", "=", self._name),
            ("name", "=", field_name),
        ], limit=1)
        if not fld:
            return []
        sels = self.env["ir.model.fields.selection"].sudo().search(
            [("field_id", "=", fld.id)],
            order="sequence, id",
        )
        return [(s.value, s.name) for s in sels]

    @api.model
    def _sel_x_pasillo(self):
        return self._selection_from_db("x_pasillo")

    x_pasillo = fields.Selection(selection="_sel_x_pasillo", string="Pasillo (legacy)")
    x_forecast_madrid = fields.Float(string="Forecast Madrid (legacy)")
