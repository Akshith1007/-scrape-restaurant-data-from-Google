import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

# Set up Selenium WebDriver
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run browser in headless mode
driver = webdriver.Chrome(options=chrome_options)

def scrape_restaurant_info(query, num_pages=5):
    restaurant_data = []
    base_url = f"https://www.google.com/search?q={query}&start="

    try:
        # Loop through pages of search results
        for page in range(num_pages):
            print(f"Scraping page {page + 1}...")
            driver.get(base_url + str(page * 10))  # Google shows 10 results per page

            # Allow the page to load
            time.sleep(3)

            # Find restaurant elements in search results
            restaurants = driver.find_elements(By.CSS_SELECTOR, '.VwiC3b')
            ratings = driver.find_elements(By.CSS_SELECTOR, '.r0bn4c.rQMQod')
            addresses = driver.find_elements(By.CSS_SELECTOR, '.BNeawe.iBp4i.AP7Wnd')
            phone_numbers = driver.find_elements(By.CSS_SELECTOR, '.BNeawe.s3v9rd.AP7Wnd')  # Look for phone numbers

            # Loop through each result and extract information
            for i in range(len(restaurants)):
                name = restaurants[i].text.strip() if i < len(restaurants) else 'N/A'
                rating = ratings[i].text.strip() if i < len(ratings) else 'N/A'
                address = addresses[i].text.strip() if i < len(addresses) else 'N/A'
                phone_number = phone_numbers[i].text.strip() if i < len(phone_numbers) else 'N/A'

                # Append data for the current restaurant
                restaurant_data.append([name, rating, phone_number, address])

            # Wait for a while before loading the next page to avoid being blocked
            time.sleep(3)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

    return restaurant_data

# Save data to CSV
def save_to_csv(data, filename='restaurants.csv'):
    if data:
        headers = ['Restaurant Name', 'Rating', 'Phone Number', 'Address']
        # Creating DataFrame for neat formatting
        df = pd.DataFrame(data, columns=headers)
        
        # Sort the data (optional, sorting by restaurant name for neatness)
        df = df.sort_values(by='Restaurant Name').reset_index(drop=True)
        
        # Save the DataFrame to CSV
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"Data saved to {filename}")
    else:
        print("No data to save.")

# Main function
if __name__ == "__main__":
    search_query = "restaurants in New York"  # Change to your desired location
    num_pages = 5  # Number of pages to scrape
    restaurant_info = scrape_restaurant_info(search_query, num_pages)
    
    if restaurant_info:
        save_to_csv(restaurant_info)
    else:
        print("No data to save.")
