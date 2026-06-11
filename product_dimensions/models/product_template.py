# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
import logging

_logger = logging.getLogger(__name__)
class ProductTemplate(models.Model):
    _inherit = "product.template"

    dimensional_uom_id = fields.Many2one(
        "uom.uom",
        "Dimensional UoM",
        related="product_variant_ids.dimensional_uom_id",
        help="UoM for length, height, width",
        readonly=False,
    )
    volume = fields.Float(
        'Volume',
        digits='Volume',
        compute='_compute_volume',
        inverse='_inverse_volume',
        store=True
    )

    product_height = fields.Float(
        inverse="_inverse_dimensions",
        store=True
    )
    product_length = fields.Float(
        inverse="_inverse_dimensions",
        store=True
    )
    product_width = fields.Float(
        inverse="_inverse_dimensions",
        store=True
    )

    @api.model
    def _calc_volume(self, product_length, product_height, product_width, uom_id):
        volume = 0
        if product_length and product_height and product_width and uom_id:
            length_m = self.convert_to_meters(product_length, uom_id)
            height_m = self.convert_to_meters(product_height, uom_id)
            width_m = self.convert_to_meters(product_width, uom_id)
            volume = length_m * height_m * width_m

        return volume

    @api.depends(
        "product_length", "product_height", "product_width", "dimensional_uom_id"
    )
    def _compute_volume(self):
        for template in self:
            template.volume = template._calc_volume(
                template.product_length,
                template.product_height,
                template.product_width,
                template.dimensional_uom_id,
            )

    def convert_to_meters(self, measure, dimensional_uom):
        uom_meters = self.env.ref("uom.product_uom_meter")

        return dimensional_uom._compute_quantity(
            qty=measure,
            to_unit=uom_meters,
            round=False,
        )

    def _prepare_variant_values(self, combination):
        """
        As variant is created inside template create() method and as
        template fields values are flushed after _create_variant_ids(),
        we catch the variant values preparation to update them
        """
        res = super()._prepare_variant_values(combination)
        if self.product_length:
            res.update({"product_length": self.product_length})
        if self.product_height:
            res.update({"product_height": self.product_height})
        if self.product_width:
            res.update({"product_width": self.product_width})
        return res

    def _inverse_dimensions(self):
        for template in self:
            _logger.info("Inverse")
            _logger.info(template.product_variant_ids)
            template.product_variant_ids.write({
                'product_height': template.product_height,
                'product_length': template.product_length,
                'product_width': template.product_width,
            })

    def _inverse_volume(self):
        for template in self:
            _logger.info("Inverse variant, volume")
            template.product_variant_ids.write({
                'volume': template.volume
            })