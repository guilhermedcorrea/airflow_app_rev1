from airflow.providers.http.operators.http import SimpleHttpOperator
from pendulum import datetime, duration
from airflow.decorators import dag, task, task_group
from airflow.utils.task_group import TaskGroup
import pendulum
import json
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.expected_conditions import visibility_of_element_located, \
    invisibility_of_element_located, title_contains, title_is
import os
from typing import Any, Dict,List
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from pathlib import Path
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
from seleniumwire import webdriver
from selenium.common.exceptions import NoSuchElementException


PROXY = "<HOST:PORT>"
webdriver.DesiredCapabilities.FIREFOX['proxy'] = {
"httpProxy": PROXY,
"ftpProxy": PROXY,
"sslProxy": PROXY,
"proxyType": "MANUAL",

}

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--disable-infobars")
options.add_argument("--no-proxy-server")
options.add_argument("--safebrowsing-disable-download-protection")
options.add_argument("safebrowsing-disable-extension-blacklist")
options.add_argument('--disable-gpu')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--allow-running-insecure-content')
options.add_argument('--ignore-certificate-errors')
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument('--no-sandbox')
options.add_argument('--ignore-certificate-errors-spki-list')
options.add_argument('--ignore-ssl-errors')


service = Service()

def check_exists_by_xpath(*args, **kwargs) -> bool:
    try:
        webdriver.find_element(*args)
    except NoSuchElementException:
        return False
    return True


class CheckelementClass(object):
 
  def __init__(self, locator, css_class) -> None:
    self.locator = locator
    self.css_class = css_class

  def __call__(self, driver) -> Any:
    element = driver.find_element(*self.locator)  
    if self.css_class in element.get_attribute("class"):
        return element
    else:
        return False


#wait = WebDriverWait(driver, 10)
#element = wait.until(CheckelementClass((By.ID, 'myNewInput'), "myCSSClass"))


@dag(schedule=None, start_date=pendulum.datetime(2023, 7, 1, tz="UTC"), catchup=False)
def spider_vinculo_tim():
    global driver
    driver = webdriver.Chrome(options=options)
    driver.get("https://pacportal.timbrasil.com.br")
    driver.maximize_window()
    

    def login_user() -> Any:
    
        try:
            
            username = WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="USERNAME"]')))
            username.send_keys("T3696103")

            password = WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="PASSWORD"]')))
            password.send_keys("018334")
            
        except Exception as e:
            print(e)
       
        try:
            token = WebDriverWait(driver, 30).until(
                        EC.presence_of_element_located((By.XPATH, '//*[@id="PASSWORD"]')))
            token.send_keys("018334")
        except Exception as e:
            
            print(e)
                
        except Exception as e:
            print("Error", e)
        
        try:
            button = WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.ID, "btnSubmit")) )
            button.click()
        except Exception as e:
            print("Error", e)
                
        time.sleep(5)

    def pesquisa_cliente() -> None:
        #from .controllers.querys_akiva_database import get_user_infos

        try:
            if WebDriverWait(driver, 15).until(
                        EC.presence_of_element_located((By.ID, "2_c_err"))):
                
                driver.find_element(
                    By.XPATH, '//*[@id="s_S_A2_div"]/form/div/span/div[3]/div/div/table/tbody/tr[3]/td[3]/div/input')
                
            else:
                driver.refresh()
                
                WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((
                            By.XPATH, '//*[@id="s_S_A2_div"]/form/div/span/div[3]/div/div/table/tbody/tr[3]/td[3]/div/input')))
                                
        except Exception as e:
            print("Error",e)
            
            
        referencia_usuario = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((
                            By.XPATH, '//*[@id="s_S_A2_div"]/form/div/span/div[3]/div/div/table/tbody/tr[3]/td[3]/div/input')))
        #user_ref = get_user_infos()
        #print(user_ref)
        #referencia_usuario.send_keys("000000000000000")
        
     
    pesquisa_cliente(login_user())  
        
spider_vinculo_tim()






