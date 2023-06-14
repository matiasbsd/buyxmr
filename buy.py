#!/usr/bin/env python3

"""
Este script realiza solicitudes a la API de AgoraDesk para obtener información sobre ofertas de compra de Monero (XMR) en
diferentes métodos de pago en Argentina. Luego muestra la información relevante de cada oferta, incluyendo el precio,
monto máximo disponible y el porcentaje de cambio en comparación con el precio actual de XMR.

Requiere las siguientes dependencias:
- requests (instalable mediante 'pip install requests')

Asegúrate de tener una conexión a Internet activa para ejecutar el script correctamente.
"""

import requests
import json

def get_offers(url):
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = json.loads(response.text)
        return data['data']['ad_list']
    else:
        print(f'Error al realizar la solicitud: {response.status_code}')
        return []

def print_offer_info(offer, xmr_price):
    offer_id = offer['data']['ad_id']
    offer_username = offer['data']['profile']['name']
    offer_price = float(offer['data']['temp_price'])
    offer_max_amount_available = offer['data'].get('max_amount_available', 'N/A')
    print(f'URL: https://localmonero.co/nojs/ad/{offer_id}')
    print(f'Precio: $ {offer_price}')
    print(f'Monto máximo: $ {offer_max_amount_available}')
    print(f'Usuario y reputación: {offer_username}')

    percentage_change = ((offer_price - xmr_price) / xmr_price) * 100
    if percentage_change > 0:
        change_type = "aumento"
    elif percentage_change < 0:
        change_type = "disminución"
    else:
        change_type = "sin cambios"

    print(f'Porcentaje de {change_type}: {round(percentage_change, 2)}%')
    print('---')

def main():
    url1 = 'https://agoradesk.com/api/v1/buy-monero-online/ARS/AR/national-bank-transfer'
    url2 = 'https://agoradesk.com/api/v1/buy-monero-online/ARS/AR/mercado-pago'

    offers1 = get_offers(url1)
    offers2 = get_offers(url2)

    def get_price(symbol):
        response = requests.get(f'https://api.binance.com/api/v3/ticker/price?symbol={symbol}')
        data = response.json()
        return float(data['price'])

    usdtars_price = get_price('USDTARS')
    xmrusdt_price = get_price('XMRUSDT')
    xmrars_price = usdtars_price * xmrusdt_price

    print('Ofertas por transferencia bancaria:')
    for offer in offers1:
        print_offer_info(offer, xmrars_price)

    print('')
    print('Ofertas por Mercado Pago:')
    for offer in offers2:
        print_offer_info(offer, xmrars_price)

    print('')
    print("El precio de XMR hoy es $ " + str(round(xmrars_price, 2)))

if __name__ == '__main__':
    main()

