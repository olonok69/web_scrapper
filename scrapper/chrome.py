# vim test.py
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from src.utils import _get_search_url
import requests

PROXY = "socks5://127.0.0.1:9050"
RULES = "MAP * ~NOTFOUND , EXCLUDE 127.0.0.1"
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument(f"--proxy-server={PROXY}")
options.add_argument(f"--host-resolver-rules={RULES}")
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), options=options
)


query = "agreement"
url = _get_search_url(query)

print(url)
import requests

session = requests.session()
session.proxies = {}
r = session.get("http://httpbin.org/ip")
print(r.text)


session.proxies["http"] = "socks5h://localhost:9050"
session.proxies["https"] = "socks5h://localhost:9050"
headers = {}
headers["User-agent"] = "HotJava/1.1.2 FCS"
r = session.get("http://httpbin.org/ip")

print(r.text)
r = session.get("https://httpbin.org/user-agent", headers=headers)
print(r.text)

r = session.get(url, headers=headers)

print(r.text)
