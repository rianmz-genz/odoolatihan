# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import json
import math


class OknumApi(http.Controller):
    # create oknum
    @http.route('/api/oknum/create', auth='user', method=['POST'], csrf=False, cors="*", website=False)
    def createOknum(self, **kw):
        # validate column
        try:
            name = kw['name']
        except KeyError:
            return request.make_response(json.dumps({
                'status': 'failed',
                'message': '`name` is required.'
            }), headers={'Content-Type': 'application/json'})

        try:
            jabatan = kw['jabatan']
        except KeyError:
            return request.make_response(json.dumps({
                'status': 'failed',
                'message': '`jabatan` is required.'
            }), headers={'Content-Type': 'application/json'})

        try:
            domisili = kw['domisili']
        except KeyError:
            return request.make_response(json.dumps({
                'status': 'failed',
                'message': '`domisili` is required.'
            }), headers={'Content-Type': 'application/json'})

        # operasional
        Oknum = request.env['persenan_plus.oknum'].sudo()

        newOknum = Oknum.create({
            'name': name,
            'jabatan': jabatan,
            'domisili': domisili,
        })

        # response api
        return request.make_response(json.dumps({
            'status': 'success',
            'message': 'berhasil menambahkan oknum.',
            'data': {
                'name': newOknum.name,
                'jabatan': newOknum.jabatan,
                'domisili': newOknum.domisili,
            }
        }), headers={'Content-Type': 'application/json'})

    # get one oknum
    @http.route('/api/oknum/<int:id>', auth='user', method=['GET'], csrf=False, cors="*", website=False)
    def getOknumById(self, id, **kw):
        # validate
        Oknum = request.env['persenan_plus.oknum'].sudo()

        existingOknum = Oknum.search([("id", '=', id)])

        if (len(existingOknum) < 1):
            return request.make_response(json.dumps({
                'status': 'failed',
                'message': 'data tidak ditemukan',
            }), headers={'Content-Type': 'application/json'})

        return request.make_response(json.dumps({
            'status': 'success',
            'message': 'data ditemukan',
            'data': {
                'nama': existingOknum.name,
                'jabatan': existingOknum.jabatan,
                'domisili': existingOknum.domisili
            },
        }), headers={'Content-Type': 'application/json'})

     # update oknum
    @http.route('/api/oknum/update/<int:id>', auth='user', methods=['PUT'], csrf=False, cors="*", website=False)
    def updateOknum(self, id, **kw):
        # operasional
        Oknum = request.env['persenan_plus.oknum'].sudo()

        # cari data oknum dengan id tertentu
        oknum = Oknum.browse(id)
        if not oknum:
            return request.make_response(json.dumps({
                'status': 'failed',
                'message': 'Oknum tidak ditemukan.'
            }), headers={'Content-Type': 'application/json'})

        # update data oknum
        try:
            if 'name' in kw:
                oknum.name = kw['name']
            if 'jabatan' in kw:
                oknum.jabatan = kw['jabatan']
            if 'domisili' in kw:
                oknum.domisili = kw['domisili']
        except Exception as e:
            return request.make_response(json.dumps({
                'status': 'failed',
                'message': str(e)
            }), headers={'Content-Type': 'application/json'})

        # response api
        return request.make_response(json.dumps({
            'status': 'success',
            'message': 'Berhasil mengupdate oknum.',
            'data': {
                'name': oknum.name,
                'jabatan': oknum.jabatan,
                'domisili': oknum.domisili,
            }
        }), headers={'Content-Type': 'application/json'})

    # delete oknum
    @http.route('/api/oknum/delete/<int:id>', auth='user', methods=['DELETE'], csrf=False, cors="*", website=False)
    def deleteOknum(self, id, **kw):
        # operasional
        Oknum = request.env['persenan_plus.oknum'].sudo()

        # cari data oknum dengan id tertentu
        oknum = Oknum.browse(id)
        if not oknum:
            return request.make_response(json.dumps({
                'status': 'failed',
                'message': 'Oknum tidak ditemukan.'
            }), headers={'Content-Type': 'application/json'})

        # hapus data oknum
        try:
            oknum.unlink()
        except Exception as e:
            return request.make_response(json.dumps({
                'status': 'failed',
                'message': str(e)
            }), headers={'Content-Type': 'application/json'})

        # response api
        return request.make_response(json.dumps({
            'status': 'success',
            'message': 'Berhasil menghapus oknum.',
        }), headers={'Content-Type': 'application/json'})

    # get all oknum
    @http.route('/api/oknum', auth='user', methods=['POST'], csrf=False, cors="*", website=False)
    def getAllOknum(self, **kw):
        # operasional
        Oknum = request.env['persenan_plus.oknum'].sudo()

        # ambil parameter halaman dan ukuran halaman
        page = int(kw.get('page', 1))
        limit = int(kw.get('limit', 10))
        field = kw.get('field', 'id')
        orderBy = kw.get('orderBy', 'asc')

        # hitung offset
        offset = (page - 1) * limit

        # buat domain filter
        domain = []

        # tambahkan filter berdasarkan field jika ada
        if 'name' in kw:
            domain.append(('name', 'ilike', kw['name']))
        if 'jabatan' in kw:
            domain.append(('jabatan', 'ilike', kw['jabatan']))
        if 'domisili' in kw:
            domain.append(('domisili', 'ilike', kw['domisili']))

        # ambil data oknum dengan paginasi dan filter
        oknums = Oknum.search(
            domain, offset=offset, limit=limit, order=field + ' ' + orderBy)

        # hitung jumlah total halaman
        total_count = Oknum.search_count(domain)

        total_pages = math.ceil(total_count / limit)

        # response api
        response_data = []
        for oknum in oknums:
            response_data.append({
                'id': oknum.id,
                'name': oknum.name,
                'jabatan': oknum.jabatan,
                'domisili': oknum.domisili,
            })

        return request.make_response(json.dumps({
            'status': 'success',
            'message': 'berhasil mendapatkan semua data oknum',
            'data': response_data,
            'meta': {
                'page': page,
                'limit': limit,
                'total_pages': total_pages
            }
        }), headers={'Content-Type': 'application/json'})
