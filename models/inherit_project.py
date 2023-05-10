# -*- coding: utf-8 -*-

from odoo import models, fields, api


class persenan_plus(models.Model):
    _inherit = 'project.project'

    anggaran = fields.Float(string="Anggaran")
    persenan = fields.Float(string="Persenan")
    backdoor_salary = fields.Float(
        string="Gaji Sepihak", compute="_compute_backdoor_salary")
    keyholder_ids = fields.Many2many(
        'persenan_plus.keyholder', string="Pemegang Kunci")

    @api.depends('anggaran', 'persenan')
    def _compute_backdoor_salary(self):
        for record in self:
            record.backdoor_salary = record.anggaran * record.persenan / 100
