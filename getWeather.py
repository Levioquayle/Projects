#! python3

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import pandas as pd
import time
import pyautogui
import pyperclip

from selenium.webdriver.support.ui import Select



def getWeather(location, begDate, endDate):


    dateRange = pd.date_range(start=begDate, end=endDate, freq='D')
    begDate1 = str(dateRange[0])
    begDate1 = begDate1[:10]
    month = begDate1[5:7]
    year = begDate1[:4]
    day = begDate1[8:10]
    print(dateRange)


    driver = webdriver.Firefox()
    driver.get(weatherURL)

    elemLocation = driver.find_element_by_css_selector('#historySearch')
    elemLocation.send_keys(location)
    time.sleep(7)
    pyautogui.press('enter')

    elemMonth = Select(driver.find_element_by_css_selector('#monthSelection'))
    elemMonth.select_by_index(int(month) -1)

    elemDay = Select(driver.find_element_by_css_selector('#daySelection'))
    elemDay.select_by_index(int(day) -1)

    elemYear = Select(driver.find_element_by_css_selector('#yearSelection'))
    elemYear.select_by_visible_text(year)
    driver.find_element_by_css_selector('#dateSubmit').click()

    time.sleep(25)
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,'tbody.ng-star-inserted:nth-child(2) > tr:nth-child(3) > td:nth-child(2)')))

    elemMeanTemp = driver.find_element_by_css_selector('tbody.ng-star-inserted:nth-child(2) > tr:nth-child(3) > td:nth-child(2)')
    elemMinTemp = driver.find_element_by_css_selector('tbody.ng-star-inserted:nth-child(2) > tr:nth-child(2) > td:nth-child(2)')
    elemMaxTemp = driver.find_element_by_css_selector('tbody.ng-star-inserted:nth-child(2) > tr:nth-child(1) > td:nth-child(2)')
    elemPrecip = driver.find_element_by_css_selector('tbody.ng-star-inserted:nth-child(4) > tr:nth-child(1) > td:nth-child(2)')
    elemMaxSustainedWind = driver.find_element_by_css_selector('tbody.ng-star-inserted:nth-child(8) > tr:nth-child(1) > td:nth-child(2)')

    precipTotal = 0
    weatherFile = open(f'C:\\Users\\levio\\MyPythonScripts\\WeatherTextFiles\\{begDate} through {endDate} at {location}.txt', 'a')
    weatherFile.write(f'                 {month}-{day}-{year}' + '\n')
    weatherFile.write(f'Average temp was {elemMeanTemp.text}' + ' F\n')
    weatherFile.write(f'Min temp was {elemMinTemp.text}' + ' F\n')
    weatherFile.write(f'Max temp was {elemMaxTemp.text}' + ' F\n')
    weatherFile.write(f'Daily precip was {elemPrecip.text}' + ' \n')
    weatherFile.write(f'Max sustained wind speed was {elemMaxSustainedWind.text}' + '\n\n\n')
    weatherFile.close()
    precipTotal += float(elemPrecip.text)
    for i in range(len(dateRange) - 1):
        time.sleep(3)
        elemDayChange = Select(driver.find_element_by_css_selector('#daySelection'))
        elemDayChange.select_by_index(int(day)+i)
        driver.find_element_by_css_selector('#dateSubmit').click()
        time.sleep(7)
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,'tbody.ng-star-inserted:nth-child(2) > tr:nth-child(3) > td:nth-child(2)')))
        newDay = int(day) + i + 1
        elemMeanTemp = driver.find_element_by_css_selector('tbody.ng-star-inserted:nth-child(2) > tr:nth-child(3) > td:nth-child(2)')
        elemMinTemp = driver.find_element_by_css_selector('tbody.ng-star-inserted:nth-child(2) > tr:nth-child(2) > td:nth-child(2)')
        elemMaxTemp = driver.find_element_by_css_selector('tbody.ng-star-inserted:nth-child(2) > tr:nth-child(1) > td:nth-child(2)')
        elemPrecip = driver.find_element_by_css_selector('tbody.ng-star-inserted:nth-child(4) > tr:nth-child(1) > td:nth-child(2)')
        elemMaxSustainedWind = driver.find_element_by_css_selector('tbody.ng-star-inserted:nth-child(8) > tr:nth-child(1) > td:nth-child(2)')
        precipTotal += float(elemPrecip.text)
        weatherFile = open(f'C:\\Users\levio\MyPythonScripts\WeatherTextFiles\{begDate} through {endDate} at {location}.txt', 'a')
        weatherFile.write(f'                 {month}-{str(newDay)}-{year}' + '\n')
        weatherFile.write(f'Average temp was {elemMeanTemp.text}' + ' F\n')
        weatherFile.write(f'Min temp was {elemMinTemp.text}' + ' F\n')
        weatherFile.write(f'Max temp was {elemMaxTemp.text}' + ' F\n')
        weatherFile.write(f'Daily precip was {elemPrecip.text}' + ' \n')
        weatherFile.write(f'Max sustained wind speed was {elemMaxSustainedWind.text}' + '\n\n\n')
        weatherFile.close()



    weatherFile = open(f'C:\\Users\levio\MyPythonScripts\WeatherTextFiles\{begDate} through {endDate} at {location}.txt', 'a')
    weatherFile.write(f'                  Total precip for date range was {precipTotal}')
    weatherFile.close()



    driver.quit()

##need to check how wunderground brings in location
#location needs to be top result


weatherURL = 'https://www.wunderground.com/history'
getWeather('KIAKLEMM8', 'June 10 2020', 'June 13 2020')
