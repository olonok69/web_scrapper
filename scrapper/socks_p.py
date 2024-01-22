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
