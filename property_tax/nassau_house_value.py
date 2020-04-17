import freshdirect.get_slot as getslot
import traceback

def house_info_extractor (driver, url):
    driver.get(url)
    fair_market_value = getslot.wait_and_find(driver, '//*[@id="infovaltab"]/div/table/tbody/tr[1]/td[2]/b')
    fair_market_value = fair_market_value.text
    property_description = getslot.wait_and_find(driver, '//*[@id="content"]/div/div[4]/div[2]/section/div/ul/li[4]')
    property_description.click()
    lot_square_footage = getslot.wait_and_find(driver, '//*[@id="procards1"]/div[1]/table/tbody/tr[5]/td')
    total_living_area = getslot.wait_and_find(driver, '//*[@id="procards1"]/div[2]/table/tbody/tr[1]/td')
    address = getslot.wait_and_find(driver, '//*[@id="right"]/section[1]/div[1]/div')
    print(fair_market_value, lot_square_footage.text, total_living_area.text, address.text)

driver = getslot.create_driver(f'https://lrv.nassaucountyny.gov/')

for lot in range(10):
    url = f'https://lrv.nassaucountyny.gov/info/02284++{lot:04d}0/'
    #print(url)
    try:
        house_info_extractor(driver, url)
    except Exception as e:
        traceback.print_exc()
        pass

