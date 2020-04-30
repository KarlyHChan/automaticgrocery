import freshdirect.get_slot as getslot
import traceback

def find_error_no_property(driver):
    element = getslot.wait_and_find(driver, '//*[@id="content"]/div/div[3]/div', wait_time=.5)
    element = element.text
    if element == """×
Error! No Properties Found""":
        return True
    return False

def house_info_extractor (driver, url, f = None):
    driver.get(url)
    if find_error_no_property(driver):
        return
    fair_market_value = getslot.wait_and_find(driver, '//*[@id="infovaltab"]/div/table/tbody/tr[1]/td[2]/b')
    fair_market_value = fair_market_value.text
    property_description = getslot.wait_and_find(driver, '//*[@id="content"]/div/div[4]/div[2]/section/div/ul/li[4]')
    property_description.click()
    lot_square_footage = getslot.wait_and_find(driver, '//*[@id="procards1"]/div[1]/table/tbody/tr[5]/td')
    total_living_area = getslot.wait_and_find(driver, '//*[@id="procards1"]/div[2]/table/tbody/tr[1]/td')
    address = getslot.wait_and_find(driver, '//*[@id="right"]/section[1]/div[1]/div')
    clean_fmv= fair_market_value.replace(',', '').replace('$', '')
    fmv_float = float(clean_fmv)
    float_area = float(total_living_area.text)
    unit_fair_market_value = fmv_float/float_area
    if f is not None:
        f.write(f'{unit_fair_market_value}, {fair_market_value}, {lot_square_footage.text}, {total_living_area.text}, {address.text}\n')
        f.flush()
    print(unit_fair_market_value, fair_market_value, lot_square_footage.text, total_living_area.text, address.text)

driver = getslot.create_driver(f'https://lrv.nassaucountyny.gov/')

f = open('output.txt', "a+t")
for block in range(295, 1000):
    print(f"block = {block}")
    f.write(f"block = {block}")
    if block == 284:
        continue

    for lot in range(1, 1000):
        url = f'https://lrv.nassaucountyny.gov/info/02{block:03d}++{lot:04d}0/'
        #print(url)
        try:
            house_info_extractor(driver, url, f)
        except Exception as e:
            traceback.print_exc()
            pass

f.close()