#!/usr/bin/env python3
import time, os, sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

PF_HOST = os.environ.get("PFSENSE_HOST", "https://10.10.0.2")
USER = os.environ.get("PFSENSE_USER", "admin")
PASS = os.environ["PFSENSE_PASS"]  # set via environment, never hardcode
OUTDIR = sys.argv[1] if len(sys.argv) > 1 else "/root/IceAlexaSecure/docs/images"
os.makedirs(OUTDIR, exist_ok=True)

opts = Options()
opts.add_argument("--headless=new")
opts.add_argument("--no-sandbox")
opts.add_argument("--disable-dev-shm-usage")
opts.add_argument("--ignore-certificate-errors")
opts.add_argument("--window-size=1600,1400")
opts.binary_location = "/usr/bin/chromium"

service = Service(executable_path="/usr/bin/chromedriver")
driver = webdriver.Chrome(service=service, options=opts)

def shot(path_suffix, name, wait=2.0, full=True):
    driver.get(f"{PF_HOST}/{path_suffix}")
    time.sleep(wait)
    if full:
        h = driver.execute_script("return document.body.scrollHeight")
        driver.set_window_size(1600, max(1400, h))
        time.sleep(0.3)
    driver.save_screenshot(f"{OUTDIR}/{name}.png")
    print("saved", name)

try:
    driver.get(f"{PF_HOST}/index.php")
    time.sleep(2)
    user_el = driver.find_element(By.NAME, "usernamefld")
    pass_el = driver.find_element(By.NAME, "passwordfld")
    user_el.send_keys(USER)
    pass_el.send_keys(PASS)
    driver.find_element(By.NAME, "login").click()
    time.sleep(3)

    shot("interfaces_assign.php", "01-interfaces-assign")
    shot("interfaces.php?if=opt3", "02-interface-opt3-config")
    shot("firewall_rules.php?if=opt3", "03-firewall-rules-opt3")
    shot("services_dhcp.php?if=opt3", "04-dhcp-opt3")
    shot("status_interfaces.php", "05-status-interfaces")
finally:
    driver.quit()
