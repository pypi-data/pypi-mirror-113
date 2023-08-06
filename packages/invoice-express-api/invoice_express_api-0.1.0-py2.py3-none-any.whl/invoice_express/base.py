#!/usr/bin/python
# -*- coding: utf-8 -*-

import appier

from . import invoice

BASE_URL = "https://default.app.invoicexpress.com/"
""" The default base URL to be used when no other
base URL value is provided to the constructor """

class API(
    appier.API,
    invoice.InvoiceAPI
):

    def __init__(self, *args, **kwargs):
        appier.API.__init__(self, *args, **kwargs)
        self.base_url = appier.conf("IE_BASE_URL", BASE_URL)
        self.key = appier.conf("IE_KEY", None)
        self.base_url = kwargs.get("base_url", self.base_url)
        self.key = kwargs.get("key", self.key)

    def build(
        self,
        method,
        url,
        data = None,
        data_j = None,
        data_m = None,
        headers = None,
        params = None,
        mime = None,
        kwargs = None
    ):
        auth = kwargs.pop("auth", True)
        print(self.key)
        if auth: params["api_key"] = self.key
