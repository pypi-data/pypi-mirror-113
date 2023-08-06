#!/usr/bin/python
# -*- coding: utf-8 -*-

class InvoiceAPI(object):

    def list_invoices(self, *args, **kwargs):
        url = self.base_url + "invoices.json"
        contents = self.get(url, **kwargs)
        return contents

    def get_invoice(self, id):
        url = self.base_url + "invoices/%s.json" % id
        contents = self.get(url)
        return contents
