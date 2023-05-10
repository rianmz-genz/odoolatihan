# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Keyholder(models.Model):
    _name = 'persenan_plus.keyholder'
    _description = "persenan_plus.keyholder"

    nama = fields.Char(string='Nama')
    posisi_id = fields.Many2one(
        'persenan_plus.keyholder_position', string="Posisi")
    bagian_persen = fields.Float(
        string='Bagian Persen')
    jumlah_bagian = fields.Float(
        string='Jumlah Bagian')
    project_ids = fields.Many2many(
        'project.project', string='Project')

    @api.depends('bagian_persen')
    def _compute_jumlah_bagian(self):
        for record in self:
            record.jumlah_bagian = record.project_ids.backdoor_salary * record.bagian_persen / 100
