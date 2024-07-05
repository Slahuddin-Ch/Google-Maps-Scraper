from playwright.sync_api import sync_playwright
from dataclasses import dataclass, asdict, field
import pandas as pd
import argparse

# Initialize lists to store extracted data
l1=[]
l2=[]

# Initialize variables for business information
Name = ""
Address = ""
Website = ""
Phone_Number = ""
Reviews_Count = 0
Reviews_Average = 0
Store_Shopping = ""
In_Store_Pickup = ""
Store_Delivery = ""
Place_Type = ""
Opens_At = ""
Introduction = ""

# Lists to store data for each attribute
names_list=[]
address_list=[]
website_list=[]
phones_list=[]
reviews_c_list=[]
reviews_a_list=[]
store_s_list=[]
in_store_list=[]
store_del_list=[]
place_t_list=[]
open_list=[]
intro_list=[]

# Function to extract data from a given xpath and append it to the provided list
def extract_data(xpath, data_list, page):
    if page.locator(xpath).count() > 0:
        data = page.locator(xpath).inner_text()
    else:
        data = ""
    data_list.append(data)

# Main function to perform scraping
def main():
    with sync_playwright() as p:
        # Launch the browser (adjust the path to Chrome if necessary)
        browser = p.chromium.launch(executable_path='C:\Program Files\Google\Chrome\Application\chrome.exe', headless=False)
        page = browser.new_page()

        # Navigate to Google Maps
        page.goto("https://www.google.com/maps/@32.9817464,70.1930781,3.67z?", timeout=60000)
        page.wait_for_timeout(1000)

        # Perform search on Google Maps
        page.locator('//input[@id="searchboxinput"]').fill(search_for)
        page.keyboard.press("Enter")
        page.wait_for_selector('//a[contains(@href, "https://www.google.com/maps/place")]')

        # Hover over the search results to load them
        page.hover('//a[contains(@href, "https://www.google.com/maps/place")]')

        previously_counted = 0
        while True:
            page.mouse.wheel(0, 10000)  # Scroll down to load more results
            page.wait_for_selector('//a[contains(@href, "https://www.google.com/maps/place")]')

            # Check if the required number of listings are loaded
            if (page.locator('//a[contains(@href, "https://www.google.com/maps/place")]').count() >= total):
                listings = page.locator('//a[contains(@href, "https://www.google.com/maps/place")]').all()[:total]
                listings = [listing.locator("xpath=..") for listing in listings]
                print(f"Total Found: {len(listings)}")
                break
            else:  # Avoid infinite loop by checking if the count remains the same
                if (page.locator('//a[contains(@href, "https://www.google.com/maps/place")]').count() == previously_counted):
                    listings = page.locator('//a[contains(@href, "https://www.google.com/maps/place")]').all()
                    print(f"Arrived at all available\nTotal Found: {len(listings)}")
                    break
                else:
                    previously_counted = page.locator('//a[contains(@href, "https://www.google.com/maps/place")]').count()
                    print(f"Currently Found: ", page.locator('//a[contains(@href, "https://www.google.com/maps/place")]').count())

        # Scrape data from each listing
        for listing in listings:
            listing.click()
            page.wait_for_selector('//div[@class="TIHn2 "]//h1[@class="DUwDvf lfPIob"]')

            # Define xpaths for required data fields
            name_xpath = '//div[@class="TIHn2 "]//h1[@class="DUwDvf lfPIob"]'
            address_xpath = '//button[@data-item-id="address"]//div[contains(@class, "fontBodyMedium")]'
            website_xpath = '//a[@data-item-id="authority"]//div[contains(@class, "fontBodyMedium")]'
            phone_number_xpath = '//button[contains(@data-item-id, "phone:tel:")]//div[contains(@class, "fontBodyMedium")]'
            reviews_count_xpath = '//div[@class="TIHn2 "]//div[@class="fontBodyMedium dmRWX"]//div//span//span//span[@aria-label]'
            reviews_average_xpath = '//div[@class="TIHn2 "]//div[@class="fontBodyMedium dmRWX"]//div//span[@aria-hidden]'
            info1='//div[@class="LTs0Rc"][1]'  # Store shopping
            info2='//div[@class="LTs0Rc"][2]'  # In-store pickup
            info3='//div[@class="LTs0Rc"][3]'  # Delivery
            opens_at_xpath='//button[contains(@data-item-id, "oh")]//div[contains(@class, "fontBodyMedium")]'  # Operating hours
            opens_at_xpath2='//div[@class="MkV9"]//span[@class="ZDu9vd"]//span[2]'
            place_type_xpath='//div[@class="LBgpqf"]//button[@class="DkEaL "]'  # Place type
            intro_xpath='//div[@class="WeS02d fontBodyMedium"]//div[@class="PYvSYb "]'  # Introduction

            # Extract introduction
            if page.locator(intro_xpath).count() > 0:
                Introduction = page.locator(intro_xpath).inner_text()
                intro_list.append(Introduction)
            else:
                Introduction = ""
                intro_list.append("None Found")

            # Extract review count
            if page.locator(reviews_count_xpath).count() > 0:
                temp = page.locator(reviews_count_xpath).inner_text()
                temp = temp.replace('(','').replace(')','').replace(',','')
                Reviews_Count = int(temp)
                reviews_c_list.append(Reviews_Count)
            else:
                Reviews_Count = ""
                reviews_c_list.append(Reviews_Count)

            # Extract average review rating
            if page.locator(reviews_average_xpath).count() > 0:
                temp = page.locator(reviews_average_xpath).inner_text()
                temp = temp.replace(' ','').replace(',','.')
                Reviews_Average = float(temp)
                reviews_a_list.append(Reviews_Average)
            else:
                Reviews_Average = ""
                reviews_a_list.append(Reviews_Average)

            # Extract information about store shopping, in-store pickup, and delivery
            if page.locator(info1).count() > 0:
                temp = page.locator(info1).inner_text().split('·')[1].replace("\n","")
                if 'shop' in temp:
                    Store_Shopping = temp
                    store_s_list.append("Yes")
                elif 'pickup' in temp:
                    In_Store_Pickup = temp
                    in_store_list.append("Yes")
                elif 'delivery' in temp:
                    Store_Delivery = temp
                    store_del_list.append("Yes")
            else:
                Store_Shopping = ""
                store_s_list.append("No")

            if page.locator(info2).count() > 0:
                temp = page.locator(info2).inner_text().split('·')[1].replace("\n","")
                if 'pickup' in temp:
                    In_Store_Pickup = temp
                    in_store_list.append("Yes")
                elif 'shop' in temp:
                    Store_Shopping = temp
                    store_s_list.append("Yes")
                elif 'delivery' in temp:
                    Store_Delivery = temp
                    store_del_list.append("Yes")
            else:
                In_Store_Pickup = ""
                in_store_list.append("No")

            if page.locator(info3).count() > 0:
                temp = page.locator(info3).inner_text().split('·')[1].replace("\n","")
                if 'Delivery' in temp:
                    Store_Delivery = temp
                    store_del_list.append("Yes")
                elif 'pickup' in temp:
                    In_Store_Pickup = temp
                    in_store_list.append("Yes")
                elif 'shop' in temp:
                    Store_Shopping = temp
                    store_s_list.append("Yes")
            else:
                Store_Delivery = ""
                store_del_list.append("No")

            # Extract operating hours
            if page.locator(opens_at_xpath).count() > 0:
                opens = page.locator(opens_at_xpath).inner_text().split('⋅')[1].replace("\u202f","")
                Opens_At = opens
                open_list.append(Opens_At)
            else:
                Opens_At = ""
                open_list.append(Opens_At)

            if page.locator(opens_at_xpath2).count() > 0:
                opens = page.locator(opens_at_xpath2).inner_text().split('⋅')[1].replace("\u202f","")
                Opens_At = opens
                open_list.append(Opens_At)

            # Extract other data using the helper function
            extract_data(name_xpath, names_list, page)
            extract_data(address_xpath, address_list, page)
            extract_data(website_xpath, website_list, page)
            extract_data(phone_number_xpath, phones_list, page)
            extract_data(place_type_xpath, place_t_list, page)
  
        # Create a DataFrame from the collected data
        df = pd.DataFrame(list(zip(
            names_list, website_list, intro_list, phones_list, address_list,
            reviews_c_list, reviews_a_list, store_s_list, in_store_list, 
            store_del_list, place_t_list, open_list
        )), columns = [
            'Names', 'Website', 'Introduction', 'Phone Number', 'Address', 
            'Review Count', 'Average Review Count', 'Store Shopping', 
            'In Store Pickup', 'Delivery', 'Type', 'Opens At'
        ])

        # Remove columns with a single unique value
        for column in df.columns:
            if df[column].nunique() == 1:
                df.drop(column, axis=1, inplace=True)

        # Save the DataFrame to a CSV file
        df.to_csv(r'result.csv', index = False)
        browser.close()
        print(df.head())

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--search", type=str)
    parser.add_argument("-t", "--total", type=int)
    args = parser.parse_args()

    # Set the search term and total number of listings based on user input or defaults
    search_for = args.search if args.search else "turkish stores in toronto Canada"
    total = args.total if args.total else 1

    main()
