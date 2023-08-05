# -*- coding: utf-8 -*-
import json
import logging
import xmltodict

from zeep import Client, xsd
from zeep.helpers import serialize_object

from bluexpress.settings import api_settings

logger = logging.getLogger(__name__)


class BluexpressHandler:
    """
        Handler to send shipping payload to Bluexpress.
    """
    def __init__(self, issue_wsdl=api_settings.BLUEXPRESS['ISSUE_WSDL'],
                 token_id=api_settings.BLUEXPRESS['TOKEN_ID'],
                 user_cod=api_settings.BLUEXPRESS['USER_COD']):

        self.issue_wsdl = issue_wsdl
        self.token_id = token_id
        self.user_cod = user_cod
        self.header = self._headers(self.token_id, self.user_cod)

    def _headers(self, token, code_user):
        header = xsd.Element(
            '{http://ws.cl.bluex.cl/}requestHeader',
            xsd.ComplexType([
                xsd.Element('idToken', xsd.String()),
                xsd.Element('codigoUsuario', xsd.String()),
            ])
        )
        return header(idToken=token, codigoUsuario=code_user)

    def get_shipping_label(self, shipping_id):
        raise NotImplementedError(
            'get_shipping_label is not a method implemented for BluexpressHandler')

    def get_default_payload(self, instance):
        """
            This method generates by default all the necessary data with
            an appropriate structure for Bluexpress courier.
        """

        try:
            address = instance.address

            lista_items = [
                {
                    'codigoUnidadMasa': 'KG',
                    'codigoUnidadLongitud': 'CM',
                    'masa': 10,
                    'largo': 10,
                    'ancho': 10,
                    'alto': 10,
                }
            ]

            payload = {
                'cuentaCliente': api_settings.SENDER['ACCOUNT_CLIENT'],
                'nombreEmbalador': api_settings.SENDER['NAME'],
                'codigoPaisEmbalador': api_settings.SENDER['COUNTRY_CODE'],
                'codigoRegionEmbalador': api_settings.SENDER['REGION_CODE'],
                'codigoComunaEmbalador': api_settings.SENDER['COMMUNE_CODE'],
                'codigoLocalidadOrigen': api_settings.SENDER['LOCATION_CODE'],
                'direccionCompletaEmbalador': '{} {} {} {}'.format(
                    api_settings.SENDER['STREET'],
                    api_settings.SENDER['NUMBER'],
                    api_settings.SENDER['FLOOR'],
                    api_settings.SENDER['DPTO'],
                ),
                'direccionPisoEmbalador':  xsd.SkipValue,
                'direccionDeptoEmbalador':  xsd.SkipValue,
                'prefijoTelefonoEmbalador':  xsd.SkipValue,
                'numeroTelefonoEmbalador': api_settings.SENDER['PHONE_NUMBER'],
                'anexoTelefonoEmbalador':  xsd.SkipValue,
                'nombreDestinatario': instance.customer_full_name,
                'codigoPaisDestinatario': api_settings.DESTINATARY['COUNTRY_CODE'],
                'codigoRegionDestinatario': address.commune.region.code,
                'codigoComunaDestinatario': address.commune.zone_code,
                'codigoLocalidadDestino': address.commune.locations.first().code,
                'direccionCompletaDestinatario': address.full_address,
                'direccionPisoDestinatario': xsd.SkipValue,
                'direccionDeptoDestinatario': xsd.SkipValue,
                'prefijoTelefonoDestinatario': '',
                'numeroTelefonoDestinatario': instance.customer_phone.replace('56', ''),
                'anexoTelefonoDestinatario': xsd.SkipValue,
                'valorDeclarado': '0',
                'codigoProducto': api_settings.BLUEXPRESS['PRODUCT_CODE'],
                'codigoMoneda': api_settings.BLUEXPRESS['CURRENCY_CODE'],
                'codigoEmpresa': api_settings.BLUEXPRESS['COMPANY_CODE'],
                'codigoTipoServicio': api_settings.BLUEXPRESS['SERVICE_TYPE_CODE'],
                'codigoPersona': api_settings.SENDER['PERSON_CODE'],
                'codigoFamiliaProducto': api_settings.BLUEXPRESS['PRODUCT_FAMILY_CODE'],
                'observaciones': '',
                'centroCosto': xsd.SkipValue,
                'switchNotificar': 'false',
                'codigoAgencia': '0',
                'listaEmisionEmbalajesCrearReq': {
                    'emisionEmbalajeCrearReq': lista_items
                },
                'listaNumerosReferenciaCrearReq': {
                    'numeroReferencia': instance.id,
                },
                'listaEmisionMercanciasPeligrosas': xsd.SkipValue,
                'listaDocumentosDevolucionCrearReq': xsd.SkipValue,
                'listaCobrosContraEntregaCrearReq': xsd.SkipValue
            }

            logger.debug(payload)
            return payload
        except Exception as error:
            logger.error(error)
            raise Exception(error) from error

    def create_shipping(self, data):
        """
            This method generate a Bluexpress shipping.
            If the get_default_payload method returns data, send it here,
            otherwise, generate your own payload.

            Additionally data was added to the response:
                tracking_number -> number to track the shipment.
        """
        logger.debug(data)

        client = Client(self.issue_wsdl)
        client.set_ns_prefix('ws', 'http://ws.bluex.cl/')

        try:
            zeep_response = client.service.emitir(
                codigoFormatoImpresion=3,
                ordenServicio=data,
                _soapheaders=[self.header]
            )

            response = dict(serialize_object(zeep_response))
            response.update({'tracking_number': response['nroFolio']})

            logger.debug(response)
            return response
        except Exception as error:
            logger.error(error)
            return False

    def get_tracking(self, identifier):
        """
            This method obtain a detail a shipping of Bluexpress.
        """
        raise NotImplementedError(
            'get_tracking is not a method implemented for BluexpressHandler')

    def get_events(self, raw_data):
        """
            This method obtain array events.
            structure:
            {
                'carrier_tracking_number': int.
                'tracking_data': xml string.
            }
            return [{}, {}, ...]
        """
        json_data = self._parse_xml_to_json(raw_data.get('tracking_data'))
        punctures = self._get_value_by_key(json_data ,'pinchazo')

        if isinstance(punctures, list):
            events = [
                {
                    'city': prick.get('nombrePosta'),
                    'state': prick.get('codigoPosta'),
                    'description': f"{prick.get('codigoTipo')} - {prick.get('nombreTipo')}",
                    'date': prick.get('fecha'),
                } for prick in punctures
            ]

        else:
            events = [
                {
                    'city': punctures.get('nombrePosta'),
                    'state': punctures.get('codigoPosta'),
                    'description': f"{punctures.get('codigoTipo')} - {punctures.get('nombreTipo')}",
                    'date': punctures.get('fecha'),
                }
            ]

        return events

    def get_status(self, raw_data):
        """
            This method returns the status of the order and "is_delivered".
            structure:
            {
                'carrier_tracking_number': int.
                'tracking_data': xml string.
            }

            response: ('Entregado', True)
        """
        json_data = self._parse_xml_to_json(raw_data.get('tracking_data'))
        macrostates = self._get_value_by_key(json_data , 'macroestado')
        is_delivered = False

        if isinstance(macrostates, list):
            status = [macrostate.get('nombre') for macrostate in macrostates if macrostate.get('nombre')]

            if status:
                status = status[-1]

        else:
            status = macrostate.get('nombre')

        if not status:
            status = 'Sin estado'

        elif status == 'Entregado':
            is_delivered = True

        return status, is_delivered

    def _parse_xml_to_json(self, tracking_data):
        """
            Parse xml string to json.
        """

        parse = xmltodict.parse(tracking_data)
        return json.loads(json.dumps(parse))

    def _get_value_by_key(self, json_data, search_key):
        """
            Extract value from key.
        """

        for key, value in json_data.items():
            if key == search_key:
                return value
            elif isinstance(value, dict):
                returned_value = self._get_value_by_key(value, search_key)
                if returned_value:
                    return returned_value
