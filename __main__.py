#!/usr/bin/env python

import aiohttp
import asyncio

import orjson
import aiosqlite
    
import logging

import random
import socket
import ssl

import logging
import datetime

import pyrogram
from pyrogram import Client, filters
from pyrogram.types import Message

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from pyrogram.enums import ParseMode

class CustomFormatter(logging.Formatter):
    def format(self, record):
        variant_id = record.__dict__.get('variant_id', None)
        
        if record.levelname == 'INFO':
            if 'is now in-stock' in record.msg:
                record.msg = f'[IN STOCK] {record.msg} [{datetime.datetime.fromtimestamp(record.created).strftime("%d/%m/%Y %H:%M")}]'
            else:
                record.msg = f'[INFO] {record.msg} [{datetime.datetime.fromtimestamp(record.created).strftime("%d/%m/%Y %H:%M")}]'
        elif record.levelname == 'ERROR':
            if 'Rate limited' in record.msg:
                record.msg = f'[RATE LIMITED] {record.msg} [{datetime.datetime.fromtimestamp(record.created).strftime("%d/%m/%Y %H:%M")}]'
            elif 'not found in the website' in record.msg:
                record.msg = f'[NOT FOUND] {record.msg} [{datetime.datetime.fromtimestamp(record.created).strftime("%d/%m/%Y %H:%M")}]'
            elif 'is out-of-stock' in record.msg:
                record.msg = f'[OUT OF STOCK] {record.msg} [{datetime.datetime.fromtimestamp(record.created).strftime("%d/%m/%Y %H:%M")}]'
            else:
                record.msg = f'[ERROR] {record.msg} [{datetime.datetime.fromtimestamp(record.created).strftime("%d/%m/%Y %H:%M")}]'

        return super().format(record)
    
custom_handler = logging.StreamHandler()
custom_handler.setFormatter(CustomFormatter())

logger = logging.getLogger()
logger.setLevel(logging.INFO)  

logger.addHandler(custom_handler)


timeout_to_wait: int = 300

variants_to_check: list[int] = [
    # PLA GALAXY
    47730388173148,
    47730388107612,
    47730388140380,
    47730388074844,
    
    # PLA Basic Refill Bundle 2 Rolls
    47513706201436,
    47513706103132,
    47513706070364,
    47513706987868,
    47513706234204,

    # PLA Silk Dual Color
    47489270841692,
    47489270808924,
    47489270776156,
    47489270874460,

    # PLA Glow
    47396823630172,
    47396823564636,
    47396823531868,
    47396823662940,
    47396823597404,

    # PLA Matte Refill Bundle 2 Rolls
    47224907727196,
    47513709511004,
    47513715867996,
    47224907759964,
    47224907792732,
    47224907661660,

    # PLA Aero
    46953506505052,
    46953506537820,

    # PLA Basic Gradient
    46901930492252,
    46901930557788,
    46901930525020,

    # PLA CMYK Lithophane Bundle
    46669434552668,
    47172230414684,

    # PLA Silk
    46636020629852,
    46636020597084,
    46636020564316,
    46636020531548,
    47301585142108,
    47301585109340,
    47301585076572,
    47301585043804,

    # PLA MARBLE
    43964050964699,
    46756997333340,

    # PLA Sparkle
    43959190946011,
    43959190913243,
    43959190880475,
    46797853032796,
    46797853163868,

    # PLA METAL
    46797850902876,
    43959185015003,
    46797851099484,
    43959185244379,
    43959185277147,

    # PLA CF
    47068316598620,
    47068316565852,
    43944001994971,
    46702306296156,
    46702306263388,
    46702306230620,
    46797856342364,

    # PLA MATTE
    42996742750427,
    47794659688796,
    47794659656028,
    47794659426652,
    47794659164508,
    42996742848731,
    42996742914267,
    42996751073499,
    42996742881499,
    42996742783195,
    42996742684891,
    42996742652123,
    42996742717659,
    42996742619355,
    42996742815963,
    42996742586587,
    43992833261787,
    46642351866204,
    46642351800668,
    46642351898972,
    46642351833436,
    43992833294555,
    46893221118300,
    43992833360091,
    46642354094428,
    46893220036956,
    46893218627932,
    46893218038108,
    46893219316060,
    47435156259164,
    43992833327323,
    46893220594012,
    43992833229019,

    # PLA BASIC
    46956986433884,
    43992830017755,
    46892984828252,
    46756980523356,
    46756980556124,
    46738546622812,
    47097922748764,
    47413030355292,
    46673378607452,
    46756980490588,
    46846865932636,
    46892982534492,
    46892985745756,
    47097923338588,
    43992829952219,
    46956529779036,
    46956524241244,
    43992829984987,
    46892983746908,
    43992829919451,
]

pyro_client: Client = Client(
    "",
    api_id=6,
    api_hash="",
    bot_token=""
)

pyrogram_ids: list[int] = [
    -12345678  # channel id
]

async def send_telegram_notification(variant_id: int, title: str, price: float, sku: str, product_type: str, url: str):

    url = f'https://eu.store.bambulab.com{url}'
    message = f"🎉 New Product Alert! 🎉\n\n" \
              f"🔹 *Product*: {title}\n" \
              f"🔹 *Price*: {price}€\n" \
              f"🔹 *SKU*: {sku}\n" \
              f"🔹 *Type*: {product_type}\n\n" \
              f"ℹ️ Variant ID: {variant_id}\n\n" \
              f"[🛒 Buy Now]({url})" 

    
    markups = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("🛒 Buy Now", url=url)
            ]
        ]
    )
    
    for pyro_id in pyrogram_ids:
        await pyro_client.send_message(pyro_id, message, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=False, reply_markup=markups)
    

async def create_product_table():
    async with aiosqlite.connect('products.db') as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS products (
                variant_id INTEGER PRIMARY KEY,
                title TEXT,
                price REAL,
                sku TEXT,
                product_type TEXT,
                in_stock INTEGER,
                notification_sent INTEGER DEFAULT 0
            )
        ''')
        await db.commit()


class BambulabResponse:
    def __init__(self, variant_id: int, status_code: int, response_json: dict) -> None:
        self.variant_id = variant_id
        self.status_code = status_code
        self.response_json = response_json

    async def parse_response(self):
        try:
            variant_id = self.response_json.get('variant_id')
            title = self.response_json.get('title')
            
            if self.status_code == 200:
                price = self.response_json.get('presentment_price')
                sku = self.response_json.get('sku')
                product_type = self.response_json.get('product_type')
                url = self.response_json.get('url')

                async with aiosqlite.connect('products.db') as db:
                    cursor = await db.execute('SELECT in_stock, notification_sent FROM products WHERE variant_id = ?', (variant_id,))
                    existing_row = await cursor.fetchone()

                    if existing_row:
                        # Product already exists in the database
                        in_stock, notification_sent = existing_row
                        if notification_sent == 0:  # Check if notification has not been sent
                            await send_telegram_notification(variant_id, title, price, sku, product_type, url)
                            await db.execute('UPDATE products SET notification_sent = 1 WHERE variant_id = ?', (variant_id,))
                            await db.commit()
                        await db.execute('''
                            UPDATE products 
                            SET title = ?, price = ?, sku = ?, product_type = ?, in_stock = ?
                            WHERE variant_id = ?
                        ''', (title, price, sku, product_type, 1, variant_id))
                        await db.commit()
                    else:
                        # Product does not exist in the database, insert it
                        await db.execute('''
                            INSERT INTO products (variant_id, title, price, sku, product_type, in_stock, notification_sent)
                            VALUES (?, ?, ?, ?, ?, ?, ?)
                        ''', (variant_id, title, price, sku, product_type, 1, 0))
                        await db.commit()

                return [variant_id, title, price, sku, product_type, url]

        except Exception as e:
            logging.error(f"Error parsing the response: {e}")


class BambulabRequests:
    def __init__(self, aiohttp_session: aiohttp.ClientSession) -> None:
        self.aiohttp_session = aiohttp_session
    
    async def handle_check_variant_response(self, response: aiohttp.ClientResponse, variant_id: int):
        match response.status:
            case 200:
                bambulab_response: BambulabResponse = BambulabResponse(variant_id, response.status, await response.json(content_type=None))
                response_data: list = await bambulab_response.parse_response()
                logging.info(f"Variant {variant_id} => {response_data[1]} is now in-stock at {response_data[2]}€")
            case 404:
                logging.error(f"Variant {variant_id} not found in the website")
            case 429:
                logging.error(f"Rate limited by the website")
            case 422:
                bambulab_response: BambulabResponse = BambulabResponse(variant_id, response.status, await response.json(content_type=None))
                response_data: list = await bambulab_response.parse_response()
                logging.error(f"Variant {variant_id} is out-of-stock")
            case _:
                logging.error(f"Unknown response status code: {response.status}")


    async def check_variant(self, variant_id: int):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:123.0) Gecko/20100101 Firefox/123.0',
            'Accept': '*/*',
            'Accept-Language': 'it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            'Origin': 'https://eu.store.bambulab.com',
            'DNT': '1',
            'Alt-Used': 'eu.store.bambulab.com',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
        }

        json_data = {
            'form_type': 'product',
            'utf8': '✓',
            'id': f'{variant_id}',
            'quantity': '1',
            'product-id': '',
        }

        async with self.aiohttp_session.post('https://eu.store.bambulab.com/cart/add.js', headers=headers, json=json_data) as response:
            await self.handle_check_variant_response(response, variant_id)

    async def check_variants(self, variant_ids: list[int]):
        tasks: list[asyncio.Task] = []
        for variant_id in variant_ids:
            tasks.append(asyncio.create_task(self.check_variant(variant_id)))
            await asyncio.sleep(2)
        await asyncio.gather(*tasks)
    
async def get_aiohttp_session(family: int = socket.AF_INET6) -> aiohttp.ClientSession:
    aiohttp_session = aiohttp.ClientSession(
        connector=aiohttp.TCPConnector(
            family=family,
            limit_per_host=0,
            force_close=True,
            enable_cleanup_closed=True,
        ),
        connector_owner=True,
        auto_decompress=True,
        timeout=aiohttp.ClientTimeout(total=10),
        skip_auto_headers=frozenset(("User-Agent", "Content-Type", "Accept-Encoding")),
    )

    return aiohttp_session

async def main():
    await create_product_table()
    await pyro_client.start()

    logging.info("Starting Bambulab Restocks Bot")
    while True:
        aiohttp_sesion: aiohttp.ClientSession = await get_aiohttp_session(family=socket.AF_INET)
        bambulab_requests = BambulabRequests(aiohttp_sesion)
        await bambulab_requests.check_variants(variants_to_check)
        await aiohttp_sesion.close()

        logging.info(f"Waiting {timeout_to_wait} seconds before relaunch the check of the variants")
        await asyncio.sleep(timeout_to_wait)

    

if __name__ == "__main__":
    asyncio.run(main())


    