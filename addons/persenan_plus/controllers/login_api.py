# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import json


class LoginApi(http.Controller):
    @http.route('/api/login/', auth='public', methods=["POST"], csrf=False, cors="*", website=False)
    def login(self, **kw):
        # Validation
        try:
            login = kw["login"]
        except KeyError:
            return request.make_response(json.dumps({
                'status': 'failed',
                'message': '`login` is required.'
            }), headers={'Content-Type': 'application/json'})

        try:
            password = kw["password"]
        except KeyError:
            return request.make_response(json.dumps({
                'status': 'failed',
                'message': '`password` is required.'
            }), headers={'Content-Type': 'application/json'})
        try:
            db = kw["db"]

        except KeyError:
            return request.make_response(json.dumps({
                'status': 'failed',
                'message': '`db` is required.'
            }), headers={'Content-Type': 'application/json'})
        # Auth user
        http.request.session.authenticate(db, login, password)
        # Session info
        res = request.env['ir.http'].session_info()
        return request.make_response(json.dumps(res), headers={'Content-Type': 'application/json'})
