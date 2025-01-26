import os
import requests
from urllib.parse import urljoin, quote
from bs4 import BeautifulSoup

# URL của trang web bạn muốn cào
url = "https://www.facebook.com/"

# Gửi yêu cầu HTTP để tải trang
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Lấy HTML của trang
html_content = soup.prettify()

# Lấy các liên kết đến file CSS và JS
css_files = soup.find_all('link', {'rel': 'stylesheet'})
js_files = soup.find_all('script', {'src': True})

# Lưu lại HTML vào file
with open("page.html", "w", encoding="utf-8") as f:
    f.write(html_content)

# Lưu CSS và JS vào thư mục riêng biệt
css_folder = "css_files"
js_folder = "js_files"
os.makedirs(css_folder, exist_ok=True)
os.makedirs(js_folder, exist_ok=True)

# Tải các file CSS
for css in css_files:
    css_href = css.get('href')
    if css_href:
        # Mã hóa các ký tự đặc biệt trong URL
        safe_css_name = quote(css_href, safe='')

        css_url = urljoin(url, css_href)
        css_response = requests.get(css_url)
        with open(os.path.join(css_folder, safe_css_name), "wb") as f:
            f.write(css_response.content)

# Tải các file JS
for js in js_files:
    js_src = js.get('src')
    if js_src:
        # Mã hóa các ký tự đặc biệt trong URL
        safe_js_name = quote(js_src, safe='')

        js_url = urljoin(url, js_src)
        js_response = requests.get(js_url)
        with open(os.path.join(js_folder, safe_js_name), "wb") as f:
            f.write(js_response.content)

print("Đã tải xong HTML, CSS và JS.")
