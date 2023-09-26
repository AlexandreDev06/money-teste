import requests

response = requests.get(
    "https://httpbin.org/get",
    proxies={
        "http": "http://968dd11a07064121908e1d9078f0dfaa:@proxy.crawlera.com:8011/",
        "https": "http://968dd11a07064121908e1d9078f0dfaa:@proxy.crawlera.com:8011/",
    },
    verify="/etc/ssl/certs/zyte-ca.crt",
)

if response.status_code == 200:
    print("Solicitação bem-sucedida!")
    print("Conteúdo da resposta:")
    print(response.text)
else:
    print("A solicitação falhou. Código de status:", response.status_code)

# curl -vx https://proxy.zyte.com:8014 -U 968dd11a07064121908e1d9078f0dfaa: --cacert zyte-ca.crt https://httpbin.org/ip
# curl https://httpbin.org/get \  -U 968dd11a07064121908e1d9078f0dfaa: \  -vx proxy.crawlera.com:8011 \  -k
