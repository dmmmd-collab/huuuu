import cloudscraper
import time
import os
from art import text2art
from colorama import Fore, Style, init
import json
import random
import sys
import asyncio
from concurrent.futures import ThreadPoolExecutor
import urllib.parse
import logging

init(autoreset=True)

# Thiết lập logging: Chỉ ghi lỗi vào x_error.txt, không hiển thị log trên console
logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('x_error.txt', mode='a', encoding='utf-8'),
        logging.NullHandler()  # Không hiển thị log trên console
    ]
)

USER_AGENTS = [
    "Mozilla/5.0 (Linux; Android 11; Pixel3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/902.25 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 13; Pixel5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/957.34 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Samsung11) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/831.43 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; Xiaomi6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.9829.263 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU iPad OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; Xiaomi1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.7410.646 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; Xiaomi11) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.9587.633 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; Xiaomi18) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6694.428 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; Pixel17) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.8847.492 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Xiaomi1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/874.19 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Xiaomi17) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.5001.174 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 12; SM-A125F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 10; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.20 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPad; CPU OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPad; CPU OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 11; Redmi Note 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.20 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 11; SM-A125F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; Vivo Y20) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPad; CPU OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 10; Mi 11 Lite) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 10; OPPO A74) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 13; Mi 11 Lite) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.20 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPad; CPU OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 13; Pixel 6 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 12; Mi 11 Lite) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 12; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.20 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPad; CPU OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPad; CPU OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 10; SM-A125F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; Pixel 6 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; Vivo Y20) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 10; Mi 11 Lite) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; Redmi Note 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 11; Redmi Note 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; SM-A125F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPad; CPU OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 11; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPad; CPU OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPad; CPU OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 12; Mi 11 Lite) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Mi 11 Lite) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.20 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 12; OPPO A74) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 14; Vivo Y20) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 12; OPPO A74) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 10; SM-A125F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 14; Mi 11 Lite) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; OPPO A74) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; Vivo Y20) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 11; Redmi Note 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 11; Redmi Note 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 11; Pixel 6 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 14; Mi 11 Lite) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 13; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPad; CPU OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPad; CPU OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 12; Redmi Note 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; Mi 11 Lite) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; OPPO A74) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.20 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; SM-A125F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPad; CPU OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 12; OPPO A74) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 11; Redmi Note 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 10; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 11; Vivo Y20) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; Mi 11 Lite) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 14; Pixel 6 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 13; SM-A125F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 11; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 11; Vivo Y20) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; Pixel 6 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 10; SM-A125F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.20 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; Redmi Note 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; OPPO A74) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 10; SM-A125F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 11; Pixel 6 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPad; CPU OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPad; CPU OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; SM-A125F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Pixel 6 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 13; SM-A125F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.20 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 12; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; Pixel 6 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 13; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 10; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Redmi Note 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPad; CPU OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 14; Vivo Y20) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.20 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; Pixel 6 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPad; CPU OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 13; OPPO A74) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPad; CPU OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 12; OPPO A74) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.20 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPad; CPU OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 14; Pixel 6 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 11; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 10; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; SM-A125F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.20 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 11; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPad; CPU OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 14; Vivo Y20) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPad; CPU OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPad; CPU OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 12; Mi 11 Lite) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; SM-A125F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 13; Pixel 6 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 10; SM-A125F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 13; Pixel 6 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 13; Redmi Note 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 12; SM-A125F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 10; Pixel 6 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; SM-A125F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPad; CPU OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; Pixel 6 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Vivo Y20) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.20 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; SM-A125F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.20 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 10; Vivo Y20) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 10; SM-A125F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 12; SM-A125F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPad; CPU OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 13; SM-A125F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; Pixel 6 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; Redmi Note 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 10; SM-A125F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.20 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; OPPO A74) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.20 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 13; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 10; OPPO A74) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 12; Redmi Note 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 13; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPad; CPU OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 10; Redmi Note 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; Pixel 6 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; Pixel 6 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.20 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 10; Pixel 6 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; Redmi Note 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; OPPO A74) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; OPPO A74) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 14; Mi 11 Lite) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; Mi 11 Lite) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.20 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 12; SM-A125F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPad; CPU OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 13; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; Vivo Y20) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPad; CPU OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 11; Redmi Note 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 13; Redmi Note 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.20 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 11; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 14; Mi 11 Lite) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 12; Pixel 6 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 14; Vivo Y20) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 13; Pixel 6 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 12; Pixel 6 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 11; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 13; Mi 11 Lite) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPad; CPU OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 12; Mi 11 Lite) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; Redmi Note 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; Pixel 6 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 10; SM-A125F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; Redmi Note 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 11; Pixel 6 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.20 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; Vivo Y20) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; Vivo Y20) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.20 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 11; SM-A125F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.20 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; OPPO A74) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 11; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 11; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.20 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 12; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPad; CPU OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 12; SM-A125F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 12; Vivo Y20) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.20 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 12; Mi 11 Lite) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Mi 11 Lite) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 13; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; Mi 11 Lite) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; Redmi Note 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPad; CPU OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; SM-A125F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 12; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 13; Mi 11 Lite) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; Redmi Note 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 13; OPPO A74) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 13; Vivo Y20) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 13; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 10; SM-A125F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPad; CPU OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 10; Redmi Note 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.20 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPad; CPU OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; Redmi Note 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPad; CPU OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 11; Vivo Y20) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 13; Pixel 6 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 11; Mi 11 Lite) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 14; Mi 11 Lite) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.20 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 13; Samsung3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/815.33 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; Pixel12) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5019.321 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU iPad OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 13_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; Samsung3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.8832.313 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU iPad OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; Samsung18) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/977.22 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_8 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 12; Xiaomi5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.7748.583 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; Pixel1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.9206.396 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Samsung12) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/983.43 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; Pixel4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/853.30 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; Xiaomi18) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.7111.231 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU iPad OS 15_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; Xiaomi3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.8258.647 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU iPad OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU iPad OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 11; Pixel2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/700.45 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; Samsung10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/659.20 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU iPad OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 12; Pixel10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.8576.872 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU iPad OS 15_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_8 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; Xiaomi17) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/849.15 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; Samsung3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/919.18 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 13_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; Samsung12) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/945.35 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU iPad OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 12; Pixel16) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/681.21 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU iPad OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU iPad OS 15_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU iPad OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; Xiaomi8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/811.43 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU iPad OS 15_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU iPad OS 15_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU iPad OS 15_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 13_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 12; Xiaomi3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/797.10 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Samsung16) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/622.14 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU iPad OS 15_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 12; Pixel11) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.5869.160 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU iPad OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU iPad OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 12; Xiaomi16) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6926.809 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU iPad OS 15_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU iPad OS 15_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 13_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; Samsung8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.6308.734 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 13_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 13; Pixel7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.5770.188 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; Xiaomi7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/972.11 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU iPad OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 13; Pixel10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/738.22 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; Samsung8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6129.474 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Xiaomi6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.7810.187 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Samsung5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/825.50 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU iPad OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 12; Samsung14) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/715.25 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 12; Samsung19) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/887.29 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Pixel7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.9811.655 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; Xiaomi3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.6539.684 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; Xiaomi18) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.8273.481 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Xiaomi20) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/717.28 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU iPad OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; Xiaomi7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.8511.709 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Pixel9) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5124.311 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; Samsung4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.8757.173 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU iPad OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; Samsung7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/874.8 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; Samsung8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.7494.328 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; Pixel11) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/970.22 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Xiaomi17) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/963.37 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Samsung16) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/969.6 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU iPad OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU iPad OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 12; Samsung10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/673.30 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; Xiaomi13) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/776.32 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Xiaomi5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/752.49 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU iPad OS 15_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 12; Xiaomi19) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/906.21 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU iPad OS 15_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_8 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 12; Xiaomi4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/728.23 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; Samsung19) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.7614.643 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 13; Pixel12) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.7227.638 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU iPad OS 15_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU iPad OS 15_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU iPad OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 11; Pixel8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/844.40 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; Pixel1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.6084.946 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_8 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; Samsung11) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.7683.489 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Pixel9) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/921.20 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; Xiaomi9) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/671.8 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 13; Pixel12) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/891.9 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Xiaomi6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/652.26 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_8 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 13; Pixel14) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/917.30 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; Samsung9) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6044.249 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 13; Samsung2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.6638.543 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU iPad OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU iPad OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU iPad OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; Samsung16) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/793.42 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; Pixel4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.8913.388 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; Xiaomi1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.8241.681 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; Pixel15) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.5237.423 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; Pixel18) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.5915.842 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; Pixel17) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.9051.968 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Pixel11) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.9551.899 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; Samsung12) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/799.19 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; Pixel20) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.7799.792 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; Xiaomi16) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/841.45 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_8 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU iPad OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU iPad OS 15_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 13; Xiaomi17) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.5298.936 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; Xiaomi17) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/639.36 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; Pixel3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6057.807 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU iPad OS 15_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; Pixel20) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/785.47 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU iPad OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_8 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 12; Xiaomi1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/639.30 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; Pixel1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.7178.873 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 13_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU iPad OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU iPad OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; Xiaomi16) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/842.4 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU iPad OS 15_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU iPad OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU iPad OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 13; Samsung19) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/937.43 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; Samsung20) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.7112.922 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Xiaomi4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.6672.223 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; Xiaomi11) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.7117.907 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; Xiaomi18) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6834.985 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; Xiaomi20) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/856.17 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU iPad OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU iPad OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 12; Samsung5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.7830.686 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Samsung1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/741.10 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU iPad OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU iPad OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 12; Xiaomi17) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.7286.446 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; Pixel19) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/760.37 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; Xiaomi11) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.7426.739 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU iPad OS 15_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; Samsung4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6874.865 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; Xiaomi9) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/998.38 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_8 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 12; Samsung19) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.5425.166 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; Samsung1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/771.1 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 13_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 11; Pixel11) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/893.8 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; Pixel20) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.8237.231 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Pixel11) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.6487.792 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU iPad OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 12; Pixel3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/904.4 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU iPad OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 13; Pixel4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/602.34 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU iPad OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 12; Pixel11) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5005.427 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_8 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_8 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU iPad OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 12; Pixel6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.5586.807 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Xiaomi14) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/626.4 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Samsung2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.9778.512 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU iPad OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU iPad OS 15_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; Xiaomi9) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/727.36 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; Pixel12) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.7318.996 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Samsung17) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/867.35 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; Pixel18) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.5471.232 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; Xiaomi16) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.8131.381 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 13_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; Xiaomi5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/724.19 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 11; Pixel16) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.9710.307 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU iPad OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 13; Samsung18) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/951.23 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU iPad OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU iPad OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; Samsung3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/967.21 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Xiaomi6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/677.23 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU iPad OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU iPad OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; Pixel18) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/612.30 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; Xiaomi5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/922.12 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; Xiaomi10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.7008.660 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; Samsung1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/998.2 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 13; Xiaomi3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/925.43 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Pixel9) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/967.45 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU iPad OS 15_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU iPad OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU iPad OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; Samsung9) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.9880.876 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU iPad OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU iPad OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; Xiaomi20) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.5974.593 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU iPad OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 13_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 13; Samsung20) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/612.48 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU iPad OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; Samsung15) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.7564.497 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Samsung13) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/811.25 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; Pixel12) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/845.45 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 13_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; Samsung6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.7532.763 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU iPad OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; Xiaomi2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.5907.536 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; Pixel12) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/806.35 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU iPad OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 13; Xiaomi14) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/887.30 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 13; Samsung7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.8165.834 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Pixel10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.9252.196 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; Samsung20) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/997.21 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU iPad OS 15_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 13; Xiaomi10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.9771.619 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU iPad OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU iPad OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU iPad OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; Samsung4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/829.2 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Xiaomi13) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/904.43 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU iPad OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_8 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU iPad OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU iPad OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU iPad OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU iPad OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; Pixel20) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.9538.336 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU iPad OS 15_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 11; Pixel8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/829.21 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; Pixel2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/847.38 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Xiaomi11) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/875.48 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; Xiaomi20) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/670.7 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Pixel8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/789.36 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU iPad OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU iPad OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 11; Pixel6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/875.9 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; Xiaomi16) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/852.47 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; Pixel6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5438.383 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Samsung20) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6709.300 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; Xiaomi10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.6489.495 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; Samsung10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/810.24 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; Pixel1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.7538.345 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; Pixel2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/872.30 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; Samsung7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.5104.328 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 13_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_8 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 13; Xiaomi11) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/696.29 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; Xiaomi17) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/788.48 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_8 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; Xiaomi15) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/602.1 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; Samsung1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/927.50 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Xiaomi9) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/761.49 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Samsung3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.6654.839 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; Samsung2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/972.28 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU iPad OS 15_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 12; Pixel14) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.8785.573 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU iPad OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; Pixel18) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.8948.813 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; Xiaomi5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/681.3 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; Pixel2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.7980.497 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 13_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU iPad OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 12; Samsung5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/714.6 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; Pixel2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.5474.858 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; Xiaomi15) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/942.37 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Samsung5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/752.34 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU iPad OS 15_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; Pixel13) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.6599.254 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Samsung12) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/881.37 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; Samsung12) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.9541.881 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU iPad OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 13_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; Samsung17) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/664.28 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU iPad OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 12; Samsung3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.9323.828 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; Pixel15) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.5463.347 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 12; Pixel16) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/868.28 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; Samsung14) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/709.16 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 13; Samsung2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/981.20 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU iPad OS 15_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 11; Pixel7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.5873.497 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU iPad OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; Xiaomi17) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.8966.647 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; Xiaomi4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/765.37 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU iPad OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; Samsung6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.7268.891 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Xiaomi11) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.6891.275 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; Samsung20) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/697.5 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Xiaomi10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/893.39 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Samsung16) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6274.293 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Xiaomi10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5645.280 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Xiaomi6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/652.44 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Samsung5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/702.17 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; Samsung5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/720.4 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; Pixel18) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/857.32 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; Samsung8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/760.13 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; Pixel19) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/886.17 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; Xiaomi18) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.5292.445 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Xiaomi8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/763.38 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; Samsung8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/663.34 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Pixel19) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/851.34 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Xiaomi5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/898.21 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Samsung2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.8090.669 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Samsung5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.8045.244 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU iPad OS 15_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 13; Samsung5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.6197.978 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; Xiaomi17) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/786.21 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU iPad OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 13_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 12; Pixel3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6395.947 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; Pixel4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.9494.112 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; Samsung10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/643.19 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; Pixel14) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.7721.856 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Samsung4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/884.36 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; Samsung1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.6223.268 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; Xiaomi17) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/975.35 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU iPad OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 12; Pixel18) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.8681.696 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; Samsung16) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/933.1 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU iPad OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; Xiaomi11) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.8119.856 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU iPad OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 12; Pixel4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/761.31 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU iPad OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU iPad OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 12; Pixel6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.5408.109 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Pixel11) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.5352.970 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU iPad OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU iPad OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 12; Pixel8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/812.6 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; Xiaomi8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/899.41 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Samsung18) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/792.17 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Xiaomi12) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5366.732 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Samsung20) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/658.44 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; Xiaomi9) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.5581.462 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; Samsung1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/993.6 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU iPad OS 15_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 13; Samsung2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/679.39 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_8 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; Xiaomi6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/769.16 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Pixel4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.9589.899 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; Xiaomi5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.9342.166 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Pixel10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/738.17 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU iPad OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; Pixel3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/702.13 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; Xiaomi17) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/966.36 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU iPad OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; Xiaomi12) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.8384.533 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; Xiaomi17) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/893.7 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; Xiaomi7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/750.38 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU iPad OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 12; Pixel10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.8950.120 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; Samsung3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/924.25 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; Pixel18) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/719.25 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; Xiaomi1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/942.16 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; Pixel12) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.8817.241 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; Samsung19) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/891.41 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Pixel20) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.5099.342 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU iPad OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 11; Pixel5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/788.39 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; Xiaomi3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/897.28 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; Xiaomi11) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.6332.547 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; Pixel5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.6357.230 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Pixel7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/738.4 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Xiaomi8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/857.14 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU iPad OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 12; Xiaomi20) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.8574.352 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Samsung14) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/844.19 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU iPad OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 12; Samsung8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.6690.378 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; Pixel13) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.8801.262 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 13_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 12; Xiaomi13) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/820.26 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; Pixel19) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.7407.228 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; Pixel15) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.8726.501 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU iPad OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; Pixel9) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.8250.816 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; Samsung18) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/942.13 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU iPad OS 15_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 13; Pixel10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/753.6 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; Samsung17) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/990.49 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU iPad OS 15_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 12; Xiaomi5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.8623.346 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Xiaomi14) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6590.690 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; Pixel12) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.6766.613 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Samsung10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/898.12 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU iPad OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 11; Pixel2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.6049.680 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; Samsung8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/719.27 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Xiaomi9) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/944.1 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU iPad OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU iPad OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU iPad OS 15_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU iPad OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; Samsung6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.6481.731 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Samsung14) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6409.913 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Samsung20) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.8367.320 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; Pixel5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/911.36 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; Samsung12) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.5183.358 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; Pixel19) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5369.272 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; Pixel10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.6772.633 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU iPad OS 15_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU iPad OS 15_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 11; Pixel14) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/671.28 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU iPad OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; Samsung12) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.5721.527 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU iPad OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 11; Pixel18) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/804.41 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; Samsung8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.9229.750 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; Pixel8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/947.19 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Xiaomi20) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/696.5 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Samsung12) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/923.29 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU iPad OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU iPad OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 13; Pixel4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.8128.153 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 13_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU iPad OS 15_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU iPad OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; Xiaomi3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/754.2 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU iPad OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 11; Pixel20) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/613.9 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; Samsung18) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/717.2 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_8 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; Xiaomi13) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/693.4 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU iPad OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 12; Samsung7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/749.16 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU iPad OS 15_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 12; Samsung18) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/907.37 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; Xiaomi18) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.7177.396 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU iPad OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU iPad OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU iPad OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 13_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU iPad OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 12; Pixel18) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.8460.284 Mobile Safari/537.36",
]

DEFAULT_HEADERS = {
    'Accept-Language': 'vi,en-US;q=0.9,en;q=0.8',
    'Referer': 'https://app.golike.net/',
    'Sec-Ch-Ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': "Windows",
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'T': 'VFZSamQwOUVSVEpQVkVFd1RrRTlQUT09',
    'Content-Type': 'application/json;charset=utf-8'
}

class ToolUI:
    @staticmethod
    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def typing_effect(text, color=Fore.WHITE, delay=0.01):
        for char in text:
            print(f"{color}{Style.BRIGHT}{char}{Style.RESET_ALL}", end='', flush=True)
            time.sleep(delay)
        print()

    @staticmethod
    def print_banner():
        ToolUI.clear_screen()
        banner = text2art("Golike X", font="small")
        print(f"{Fore.CYAN}{Style.BRIGHT}{banner}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}╔════════════════════════════════════════════════════╗{Style.RESET_ALL}")
        ToolUI.typing_effect("║ Tool By: BVTOOL         Version: 1.0          ║", Fore.GREEN, 0.015)
        ToolUI.typing_effect("║ Zalo: https://zalo.me/g/bhbotm174                  ║", Fore.GREEN, 0.015)
        ToolUI.typing_effect("║ ADMIN: PHUOCAN                              ║", Fore.GREEN, 0.015)
        print(f"{Fore.YELLOW}╚════════════════════════════════════════════════════╝{Style.RESET_ALL}")
        print()

    @staticmethod
    def display_account_info(user_data):
        ToolUI.print_banner()
        ToolUI.typing_effect("THÔNG TIN TÀI KHOẢN GOLIKE", Fore.CYAN, 0.015)
        print(f"{Fore.MAGENTA}╭{'─' * 50}╮{Style.RESET_ALL}")
        ToolUI.typing_effect(f"│ Tên tài khoản : {user_data['username']:<36} │", Fore.GREEN, 0.01)
        ToolUI.typing_effect(f"│ Số dư hiện tại: {user_data['coin']:,} VNĐ{' ' * (35-len(str(f'{user_data['coin']:,}')))} │", Fore.YELLOW, 0.01)
        ToolUI.typing_effect(f"│ ID người dùng : {user_data['id']:<36} │", Fore.GREEN, 0.01)
        print(f"{Fore.MAGENTA}╰{'─' * 50}╯{Style.RESET_ALL}")
        print()

    @staticmethod
    def display_twitter_accounts(accounts, user_data):
        ToolUI.print_banner()
        ToolUI.typing_effect(f"DANH SÁCH TÀI KHOẢN TWITTER (X) - CHỦ: {user_data['username']}", Fore.CYAN, 0.015)
        print(f"{Fore.GREEN}╭{'─' * 40}╮{Style.RESET_ALL}")
        ToolUI.typing_effect(f"│ Tổng số dư    : {user_data['coin']:,} VNĐ{' ' * (23-len(str(f'{user_data['coin']:,}')))} │", Fore.YELLOW, 0.01)
        ToolUI.typing_effect(f"│ ID người dùng : {user_data['id']}{' ' * (25-len(str(user_data['id'])))} │", Fore.YELLOW, 0.01)
        print(f"{Fore.GREEN}╰{'─' * 40}╯{Style.RESET_ALL}")
        print()

        print(f"{Fore.BLUE}╔════╦{'═' * 22}╦{'═' * 15}╦{'═' * 12}╗{Style.RESET_ALL}")
        ToolUI.typing_effect(f"║ STT ║ TÀI KHOẢN TWITTER      ║ ID TÀI KHOẢN ║ TRẠNG THÁI ║", Fore.YELLOW, 0.01)
        print(f"{Fore.BLUE}╠════╬{'═' * 22}╬{'═' * 15}╬{'═' * 12}╣{Style.RESET_ALL}")

        for i, acc in enumerate(accounts['data'], 1):
            screen_name = acc['screen_name']
            account_id = acc.get('id', 'N/A')
            display_name = (screen_name[:18] + '...') if len(screen_name) > 18 else screen_name.ljust(18)
            display_id = (str(account_id)[:12] + '...') if len(str(account_id)) > 12 else str(account_id).ljust(12)
            status = "Hoạt động"
            
            ToolUI.typing_effect(f"║ {str(i).rjust(2)}{' ' * 2} ║ @{display_name:<19} ║ {display_id:<13} ║ {status.center(10)} ║", Fore.GREEN, 0.01)
            
            if i < len(accounts['data']):
                print(f"{Fore.BLUE}├────┼{'─' * 22}┼{'─' * 15}┼{'─' * 12}┤{Style.RESET_ALL}")

        print(f"{Fore.BLUE}╚════╩{'═' * 22}╩{'═' * 15}╩{'═' * 12}╝{Style.RESET_ALL}")
        ToolUI.typing_effect(f"➤ Tổng cộng: {len(accounts['data'])} tài khoản Twitter (X)", Fore.YELLOW, 0.01)
        print()

    @staticmethod
    def input_prompt(prompt, options=None, clear_after=True):
        ToolUI.typing_effect(f"✦ {prompt.upper()} ✦", Fore.GREEN, 0.015)
        print(f"{Fore.GREEN}╭{'─' * 40}╮{Style.RESET_ALL}")
        if options:
            for i, opt in enumerate(options, 1):
                ToolUI.typing_effect(f"│ {i}. {opt:<36} │", Fore.YELLOW, 0.01)
        else:
            ToolUI.typing_effect(f"│ {prompt:<38} │", Fore.GREEN, 0.01)
        print(f"{Fore.GREEN}╰{'─' * 40}╯{Style.RESET_ALL}")
        value = input(f"{Fore.WHITE}➤ {Style.RESET_ALL}")
        if clear_after:
            ToolUI.clear_screen()
            ToolUI.print_banner()
        return value

    @staticmethod
    def input_proxy_prompt():
        ToolUI.clear_screen()
        ToolUI.print_banner()
        prompt = "SỬ DỤNG PROXY? (Y/N)".center(40)
        print(f"{Fore.CYAN}╔{'═' * 42}╗{Style.RESET_ALL}")
        ToolUI.typing_effect(f"║{prompt}║", Fore.CYAN, 0.015)
        print(f"{Fore.CYAN}╚{'═' * 42}╝{Style.RESET_ALL}")
        value = input(f"{Fore.WHITE}➤ Nhập (y/n): {Style.RESET_ALL}")
        return value

    @staticmethod
    def display_task_runner(delay, account_name, proxy=None):
        ToolUI.clear_screen()
        print("Lưu Ý: Tool Này Đừng Treo Đêm!")
        ToolUI.typing_effect(f"TRÌNH XỬ LÝ NHIỆM VỤ - TK: {account_name}", Fore.CYAN, 0.015)
        print(f"{Fore.GREEN}╭{'─' * 50}╮{Style.RESET_ALL}")
        ToolUI.typing_effect(f"│ Chế độ       : Chạy liên tục{' ' * 28} │", Fore.YELLOW, 0.01)
        ToolUI.typing_effect(f"│ Thời gian chờ: {delay} giây{' ' * (34-len(str(delay)))} │", Fore.YELLOW, 0.01)
        ToolUI.typing_effect(f"│ Proxy       : {proxy if proxy else 'Không sử dụng'}{' ' * (34-(len(proxy if proxy else 'Không sử dụng')))} │", Fore.YELLOW, 0.01)
        print(f"{Fore.GREEN}╰{'─' * 50}╯{Style.RESET_ALL}")
        ToolUI.typing_effect("✦ TRẠNG THÁI NHIỆM VỤ ✦", Fore.MAGENTA, 0.015)
        print(f"{Fore.MAGENTA}{'═' * 50}{Style.RESET_ALL}")

    @staticmethod
    def display_earning(count, timestamp, job_type, amount, total):
        colors = [Fore.GREEN, Fore.CYAN, Fore.YELLOW]
        border_color = random.choice(colors)
        print(f"{border_color}╔{'─' * 44}╗{Style.RESET_ALL}")
        ToolUI.typing_effect(f"║ [{count:03d}] {timestamp} ✔ {job_type:<10} +{amount:,} VNĐ{' ' * (6-len(str(amount)))}║", Fore.YELLOW, 0.01)
        ToolUI.typing_effect(f"║ Tổng thu nhập: {total:,} VNĐ{' ' * (28-len(str(f'{total:,}')))} ║", Fore.YELLOW, 0.01)
        print(f"{border_color}╚{'─' * 44}╝{Style.RESET_ALL}")

    @staticmethod
    def display_multi_account_status(accounts_status):
        ToolUI.clear_screen()
        ToolUI.typing_effect("TRÌNH XỬ LÝ ĐA TÀI KHOẢN TWITTER (X)", Fore.CYAN, 0.015)
        print(f"{Fore.GREEN}╔════╦{'═' * 22}╦{'═' * 12}╦{'═' * 12}╦{'═' * 15}╗{Style.RESET_ALL}")
        ToolUI.typing_effect(f"║ STT ║ TÀI KHOẢN TWITTER      ║ NHIỆM VỤ ║ THU NHẬP ║ TRẠNG THÁI   ║", Fore.YELLOW, 0.01)
        print(f"{Fore.GREEN}╠════╬{'═' * 22}╬{'═' * 12}╬{'═' * 12}╬{'═' * 15}╣{Style.RESET_ALL}")
        
        for i, status in enumerate(accounts_status, 1):
            display_name = (status['name'][:18] + '...') if len(status['name']) > 18 else status['name'].ljust(18)
            job_count = str(status['jobs']).rjust(5)
            earnings = f"{status['earnings']:,} VNĐ".ljust(10)
            state = status['status'].center(13)
            color = Fore.GREEN if status['status'] == 'Running' else Fore.RED
            
            ToolUI.typing_effect(f"║ {str(i).rjust(2)}{' ' * 2} ║ @{display_name:<19} ║ {job_count:<10} ║ {earnings:<11} ║ {state:<13} ║", color, 0.01)
            
            if i < len(accounts_status):
                print(f"{Fore.BLUE}├────┼{'─' * 22}┼{'─' * 12}┼{'═' * 12}┼{'═' * 15}┤{Style.RESET_ALL}")
        
        print(f"{Fore.BLUE}╚════╩{'═' * 22}╩{'═' * 12}╩{'═' * 12}╩{'═' * 15}╝{Style.RESET_ALL}")
        ToolUI.typing_effect(f"➤ Tổng tài khoản hoạt động: {len([s for s in accounts_status if s['status'] == 'Running'])}", Fore.YELLOW, 0.01)

class TwitterBot:
    def __init__(self):
        self.proxy_list = []
        self.current_proxy = None
        self.auth_file = 'user.txt'
        self.proxy_file = 'proxies.txt'
        self.user_agent = random.choice(USER_AGENTS)
        self.headers = DEFAULT_HEADERS.copy()
        self.headers['User-Agent'] = self.user_agent
        self.accounts_status = []
        self.retry_count = 0
        self.max_retries = 5
        self.tasks_per_session = 30
        self.rest_duration = 300
        self.scraper = None  # Initialize scraper as None

    def load_proxies(self):
        """Load proxies from proxies.txt and support both ip:port and ip:port:username:password formats."""
        self.proxy_list = []
        if os.path.isfile(self.proxy_file):
            with open(self.proxy_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        # Validate proxy format
                        parts = line.split(':')
                        if len(parts) in [2, 4]:
                            self.proxy_list.append(line)
                        else:
                            logging.error(f"Invalid proxy format: {line}")
            ToolUI.typing_effect(f"✓ Đã tải {len(self.proxy_list)} proxy từ file {self.proxy_file}", Fore.GREEN, 0.01)
        return len(self.proxy_list) > 0

    def get_random_proxy(self):
        """Return a proxy dictionary in the format required by cloudscraper."""
        if not self.proxy_list:
            return None
        proxy_str = random.choice(self.proxy_list)
        parts = proxy_str.split(':')
        
        if len(parts) == 2:
            # Format: ip:port
            ip, port = parts
            proxy_dict = {
                'http': f'http://{ip}:{port}',
                'https': f'http://{ip}:{port}'
            }
        elif len(parts) == 4:
            # Format: ip:port:username:password
            ip, port, username, password = parts
            proxy_dict = {
                'http': f'http://{username}:{password}@{ip}:{port}',
                'https': f'http://{username}:{password}@{ip}:{port}'
            }
        else:
            logging.error(f"Invalid proxy format: {proxy_str}")
            return None
        
        return proxy_dict

    def create_scraper(self):
        """Create a cloudscraper instance with or without a proxy."""
        proxy = self.get_random_proxy()
        try:
            if proxy:
                print(f"{Fore.BLUE}┌{'─' * 50}┐{Style.RESET_ALL}")
                ToolUI.typing_effect(f"│ Sử dụng proxy: {proxy['http']:<33} │", Fore.BLUE, 0.01)
                print(f"{Fore.BLUE}└{'─' * 50}┘{Style.RESET_ALL}")
                self.current_proxy = proxy['http']
                # Create scraper with proxy
                scraper = cloudscraper.create_scraper()
                scraper.proxies = proxy  # Set proxies after initialization
                return scraper
            else:
                self.current_proxy = None
                return cloudscraper.create_scraper()
        except Exception as e:
            logging.error(f"Error creating scraper with proxy {proxy}: {str(e)}")
            ToolUI.typing_effect(f"✗ Lỗi khởi tạo scraper với proxy: {str(e)}", Fore.RED, 0.01)
            self.current_proxy = None
            return cloudscraper.create_scraper()  # Fallback to no proxy

    def load_or_create_auth(self):
        ToolUI.clear_screen()
        ToolUI.print_banner()
        ToolUI.typing_effect("QUẢN LÝ AUTHORIZATION", Fore.CYAN, 0.015)
        print(f"{Fore.YELLOW}╭{'─' * 50}╮{Style.RESET_ALL}")
        if os.path.isfile(self.auth_file):
            with open(self.auth_file, 'r') as f:
                old_auth = f.read().strip()
            temp_headers = self.headers.copy()
            temp_headers['Authorization'] = old_auth
            username = "Không xác định (auth lỗi)"
            try:
                self.scraper = self.create_scraper()
                response = self.scraper.get('https://gateway.golike.net/api/users/me', headers=temp_headers, timeout=10)
                data = response.json()
                if data.get('status') == 200:
                    username = data['data']['username']
            except Exception as e:
                logging.error(f"Error checking existing auth: {str(e)}")
            
            ToolUI.typing_effect(f"│ Đã tìm thấy Authorization cũ{' ' * 21} │", Fore.GREEN, 0.01)
            print(f"{Fore.YELLOW}├{'─' * 50}┤{Style.RESET_ALL}")
            ToolUI.typing_effect(f"│ Tài khoản Golike: {username:<28} │", Fore.WHITE, 0.01)
            print(f"{Fore.YELLOW}╰{'─' * 50}╯{Style.RESET_ALL}")
            print()
            choice = ToolUI.input_prompt("Sử dụng auth này? (y/n)", None, True)
            if choice.lower() == 'y':
                self.headers['Authorization'] = old_auth
                return
        ToolUI.typing_effect(f"│ Vui lòng nhập Authorization mới{' ' * 17} │", Fore.GREEN, 0.01)
        print(f"{Fore.YELLOW}╰{'─' * 50}╯{Style.RESET_ALL}")
        print()
        auth = ToolUI.input_prompt("Nhập Authorization Golike", None, True)
        with open(self.auth_file, 'w') as f:
            f.write(auth)
        self.headers['Authorization'] = auth

    def get_random_headers(self):
        headers = self.headers.copy()
        headers['User-Agent'] = random.choice(USER_AGENTS)
        return headers

    async def check_login(self):
        retries = 3
        for attempt in range(retries):
            try:
                self.scraper = self.create_scraper()
                headers = self.get_random_headers()
                response = self.scraper.get('https://gateway.golike.net/api/users/me', headers=headers, timeout=10)
                data = response.json()
                if data.get('status') == 200:
                    return data['data']
                else:
                    ToolUI.typing_effect(f"✗ Lỗi đăng nhập (Lần {attempt + 1}/{retries})", Fore.RED, 0.01)
                    logging.error(f"Login error (Attempt {attempt + 1}/{retries}): {data.get('message', 'Unknown error')}")
                    time.sleep(5)
            except Exception as e:
                ToolUI.typing_effect(f"✗ Lỗi kết nối: {str(e)} (Lần {attempt + 1}/{retries})", Fore.RED, 0.01)
                logging.error(f"Connection error (Attempt {attempt + 1}/{retries}): {str(e)}")
                time.sleep(5)
        ToolUI.typing_effect(f"✗ Đăng nhập thất bại sau {retries} lần thử", Fore.RED, 0.01)
        logging.error(f"Login failed after {retries} attempts")
        return None

    async def get_twitter_accounts(self):
        retries = 3
        for attempt in range(retries):
            try:
                self.scraper = self.create_scraper()
                headers = self.get_random_headers()
                response = self.scraper.get('https://gateway.golike.net/api/twitter-account', headers=headers, timeout=10)
                data = response.json()
                if data.get('status') == 200:
                    return data
                ToolUI.typing_effect(f"✗ Lỗi lấy tài khoản Twitter (Lần {attempt + 1}/{retries})", Fore.RED, 0.01)
                logging.error(f"Error fetching Twitter accounts (Attempt {attempt + 1}/{retries}): {data.get('message', 'Unknown error')}")
                time.sleep(5)
            except Exception as e:
                ToolUI.typing_effect(f"✗ Lỗi kết nối: {str(e)} (Lần {attempt + 1}/{retries})", Fore.RED, 0.01)
                logging.error(f"Connection error fetching Twitter accounts (Attempt {attempt + 1}/{retries}): {str(e)}")
                time.sleep(5)
        ToolUI.typing_effect(f"✗ Không lấy được danh sách tài khoản Twitter sau {retries} lần thử", Fore.RED, 0.01)
        logging.error(f"Failed to fetch Twitter accounts after {retries} attempts")
        return None

    async def process_jobs(self, account_id, delay, account_name, multi_mode=False, status=None):
        job_url = f'https://gateway.golike.net/api/advertising/publishers/twitter/jobs?account_id={account_id}'
        
        total_earned = 0
        success_count = 0
        error_report_counter = 0
        session_count = 0
        
        if not multi_mode:
            ToolUI.display_task_runner(delay, account_name, self.current_proxy)
        
        while True if not multi_mode else status['status'] == 'Running':
            if success_count > 0 and success_count % self.tasks_per_session == 0:
                if not multi_mode:
                    ToolUI.typing_effect(f"Nghỉ {self.rest_duration} giây sau {self.tasks_per_session} nhiệm vụ...", Fore.YELLOW, 0.01)
                await asyncio.sleep(self.rest_duration)
                session_count += 1
                self.scraper = self.create_scraper()
                if not multi_mode:
                    ToolUI.display_task_runner(delay, account_name, self.current_proxy)
            
            retry_attempts = 0
            max_attempts = 3
            
            while retry_attempts < max_attempts:
                try:
                    headers = self.get_random_headers()
                    if not multi_mode:
                        ToolUI.typing_effect("➤ Đang lấy nhiệm vụ...", Fore.YELLOW, 0.01)
                    job_response = self.scraper.get(job_url, headers=headers, timeout=10)
                    job_data = job_response.json()
                    
                    if job_data['status'] != 200:
                        if not multi_mode:
                            ToolUI.typing_effect(f"✗ Lỗi lấy nhiệm vụ: {job_data.get('message', 'Không xác định')}", Fore.RED, 0.01)
                        logging.error(f"Error fetching job: {job_data.get('message', 'Unknown error')}")
                        if job_data['status'] == 400 and self.retry_count < self.max_retries:
                            self.retry_count += 1
                            if not multi_mode:
                                ToolUI.typing_effect(f"➤ Thử lại lần {self.retry_count}/{self.max_retries}...", Fore.YELLOW, 0.01)
                            await asyncio.sleep(5 * self.retry_count)
                            continue
                        await asyncio.sleep(15)
                        continue

                    self.retry_count = 0
                    job_type = job_data['data']['type']
                    ads_id = job_data['data']['id']
                    object_id = job_data['data']['object_id']

                    await asyncio.sleep(delay)
                    complete_response = await self.complete_job(ads_id, account_id, job_type)
                    
                    if complete_response and complete_response.get('success'):
                        prices = complete_response['data']['prices']
                        total_earned += prices
                        success_count += 1
                        error_report_counter += 1
                        
                        if multi_mode:
                            status['earnings'] += prices
                            status['jobs'] += 1
                        else:
                            timestamp = time.strftime("%H:%M:%S")
                            ToolUI.display_earning(success_count, timestamp, job_type.upper(), prices, total_earned)
                        
                        if error_report_counter >= 5:
                            await self.skip_job(ads_id, account_id, object_id, job_type)
                            error_report_counter = 0
                            if not multi_mode:
                                ToolUI.typing_effect("↷ Tự động báo lỗi sau 5 nhiệm vụ thành công", Fore.YELLOW, 0.01)
                    else:
                        await self.skip_job(ads_id, account_id, object_id, job_type)
                    
                    await asyncio.sleep(delay)
                    break
                
                except Exception as e:
                    retry_attempts += 1
                    if retry_attempts < max_attempts:
                        if not multi_mode:
                            ToolUI.typing_effect(f"✗ Lỗi: {str(e)}. Thử lại lần {retry_attempts}/{max_attempts} sau 5s...", Fore.RED, 0.01)
                        logging.error(f"Error processing job (Attempt {retry_attempts}/{max_attempts}): {str(e)}")
                        await asyncio.sleep(5)
                    else:
                        if not multi_mode:
                            ToolUI.typing_effect(f"✗ Đã thử {max_attempts} lần, không thể tiếp tục.", Fore.RED, 0.01)
                        logging.error(f"Failed to process job after {max_attempts} attempts: {str(e)}")
                        if multi_mode:
                            status['status'] = f"Error: Failed after {max_attempts} retries"
                        return

    async def complete_job(self, ads_id, account_id, job_type):
        url = 'https://gateway.golike.net/api/advertising/publishers/twitter/complete-jobs'
        payload = {
            'ads_id': str(ads_id),
            'account_id': str(account_id),
            'async': 'true',
            'type': job_type
        }
        retries = 3
        for attempt in range(retries):
            try:
                headers = self.get_random_headers()
                response = self.scraper.post(url, headers=headers, json=payload, timeout=10)
                return response.json()
            except Exception as e:
                ToolUI.typing_effect(f"✗ Lỗi hoàn thành nhiệm vụ: {str(e)} (Lần {attempt + 1}/{retries})", Fore.RED, 0.01)
                logging.error(f"Error completing job (Attempt {attempt + 1}/{retries}): {str(e)}")
                time.sleep(5)
        ToolUI.typing_effect(f"✗ Không thể hoàn thành nhiệm vụ sau {retries} lần thử", Fore.RED, 0.01)
        logging.error(f"Failed to complete job after {retries} attempts")
        return None

    async def skip_job(self, ads_id, account_id, object_id, job_type):
        url = 'https://gateway.golike.net/api/advertising/publishers/twitter/skip-jobs'
        params = {
            'ads_id': ads_id,
            'account_id': account_id,
            'object_id': object_id,
            'async': 'true',
            'type': job_type
        }
        retries = 3
        for attempt in range(retries):
            try:
                headers = self.get_random_headers()
                response = self.scraper.post(url, headers=headers, params=params, timeout=10)
                data = response.json()
                if data.get('status') == 200:
                    ToolUI.typing_effect(f"↷ Đã bỏ qua job: {data.get('message')}", Fore.YELLOW, 0.01)
                break
            except Exception as e:
                ToolUI.typing_effect(f"✗ Lỗi bỏ qua job: {str(e)} (Lần {attempt + 1}/{retries})", Fore.RED, 0.01)
                logging.error(f"Error skipping job (Attempt {attempt + 1}/{retries}): {str(e)}")
                time.sleep(5)

    async def process_account(self, account, delay, semaphore):
        async with semaphore:
            account_id = account['id']
            account_name = account['screen_name']
            status = {
                'name': account_name,
                'jobs': 0,
                'earnings': 0,
                'status': 'Running'
            }
            self.accounts_status.append(status)
            
            try:
                await self.process_jobs(account_id, delay, account_name, multi_mode=True, status=status)
            except Exception as e:
                logging.error(f"Unexpected error processing account {account_name}: {str(e)}")
                status['status'] = 'Error: Unexpected'

    async def run_multi_accounts(self, accounts, delay, max_concurrent=5):
        semaphore = asyncio.Semaphore(max_concurrent)
        tasks = [self.process_account(account, delay, semaphore) for account in accounts['data']]
        
        async def status_updater():
            while True:
                ToolUI.display_multi_account_status(self.accounts_status)
                await asyncio.sleep(2)

        await asyncio.gather(*tasks, status_updater())

async def main():
    bot = TwitterBot()
    
    # Hiển thị khởi động đơn giản bằng typing_effect
    ToolUI.clear_screen()
    ToolUI.typing_effect("GOLIKE BOT - KHỞI ĐỘNG", Fore.YELLOW, 0.015)
    ToolUI.typing_effect("Đang kết nối hệ thống...", Fore.GREEN, 0.01)
    time.sleep(1)
    
    # Load proxies với giao diện đẹp hơn
    use_proxy = ToolUI.input_proxy_prompt()
    if use_proxy.lower() == 'y':
        if not bot.load_proxies():
            ToolUI.typing_effect("⚠ Không tìm thấy file proxies.txt hoặc file rỗng", Fore.YELLOW, 0.01)
            proxy_input = ToolUI.input_prompt("Nhập proxy (ip:port hoặc ip:port:username:password) hoặc để trống để tiếp tục không dùng proxy")
            if proxy_input:
                bot.proxy_list = [proxy_input]
    
    bot.load_or_create_auth()
    ToolUI.typing_effect("Đang kiểm tra đăng nhập...", Fore.CYAN, 0.015)
    user_data = await bot.check_login()
    
    if user_data:
        ToolUI.display_account_info(user_data)
        accounts = await bot.get_twitter_accounts()
        if accounts and 'data' in accounts:
            ToolUI.display_twitter_accounts(accounts, user_data)
            
            mode = ToolUI.input_prompt("Chọn chế độ", ["Đơn", "Nhiều"])
            delay = int(ToolUI.input_prompt("Nhập thời gian delay (giây)"))
            rest_input = ToolUI.input_prompt("Nhập thời gian nghỉ sau 30 nhiệm vụ (giây) [Enter để dùng 300]")
            rest_duration = int(rest_input) if rest_input.strip() else 300
            bot.rest_duration = rest_duration if rest_duration > 0 else 300
            
            if mode == '1':
                acc_choice = int(ToolUI.input_prompt(f"Chọn tài khoản (1-{len(accounts['data'])})"))
                account_name = accounts['data'][acc_choice-1]['screen_name']
                await bot.process_jobs(accounts['data'][acc_choice-1]['id'], delay, account_name)
            elif mode == '2':
                max_concurrent = int(ToolUI.input_prompt(f"Số tài khoản chạy cùng lúc (max {len(accounts['data'])})"))
                max_concurrent = min(max_concurrent, len(accounts['data']))
                await bot.run_multi_accounts(accounts, delay, max_concurrent)
            else:
                ToolUI.typing_effect("✗ Chế độ không hợp lệ!", Fore.RED, 0.01)
        else:
            ToolUI.typing_effect("✗ Không lấy được danh sách tài khoản Twitter", Fore.RED, 0.01)
    else:
        ToolUI.typing_effect("✗ ĐĂNG NHẬP THẤT BẠI", Fore.RED, 0.01)
        if os.path.exists(bot.auth_file):
            os.remove(bot.auth_file)

if __name__ == "__main__":
    asyncio.run(main())