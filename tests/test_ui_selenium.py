from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

def test_home_page_ui():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    
    driver.get("http://localhost:5000")
    
    assert "WattWise" in driver.title  

    # Test the presence of a form or button
    assert driver.find_element(By.ID, "submit-btn")
    
    # Fill and submit a form
    driver.find_element(By.NAME, "name").send_keys("Test User")
    driver.find_element(By.NAME, "email").send_keys("test@example.com")
    driver.find_element(By.ID, "submit-btn").click()

    time.sleep(1)  # wait for redirect
    assert "Assessment" in driver.page_source

    driver.quit()
