#!/usr/bin/env python

import xmltodict
from benedict import benedict
from suds.client import Client


def get_packing_slip(
        username: str,
        password: str,
        license_plate: str
):
    client = Client(
        url='https://ws.sanmar.com:8080/SanMarWebService/webservices/PackingSlipService?wsdl',

        retxml=True
    )

    response = client.service.GetPackingSlip(
        '1.0.0', username, password, license_plate
    )

    return benedict(xmltodict.parse(response.decode()))
