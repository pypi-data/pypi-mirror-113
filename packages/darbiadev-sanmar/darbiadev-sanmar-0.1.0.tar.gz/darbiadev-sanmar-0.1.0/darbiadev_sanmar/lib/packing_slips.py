#!/usr/bin/env python

import xmltodict
from benedict import benedict
from suds.client import Client


def func():
    client = Client(
        url='https://ws.sanmar.com:8080/SanMarWebService/webservices/PackingSlipService?wsdl',

        retxml=True
    )

    response = client.service.GetPackingSlip(
        '1.0.0', '', '', ''
    )

    return benedict(xmltodict.parse(response.decode()))
