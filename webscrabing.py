import pandas as pd
import requests
from bs4 import BeautifulSoup
import time

# Ask user how many products to scrape
num_items = int(input("Enter the number of MI mobile models to scrape: "))

# Base URL template
base_url = "https://www.flipkart.com/search?q=mi+mobiles&sid=tyy,4io&page={}"

# Lists to store data
name = []
price = []
rate = []
image = []
link = []

page = 1

print("\nScraping in progress...")

# Loop through pages until enough items are collected
while len(name) < num_items:
    url = base_url.format(page)
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract product containers
    products = soup.find_all('div', class_='tUxRFH')  # Updated wrapper class

    if not products:
        print("No more products found or Flipkart structure changed.")
        break

    for product in products:
        # Name
        n = product.find('div', class_='KzDlHZ')
        # Price
        p = product.find('div', class_='Nx9bqj _4b5DiR')
        # Rating
        r = product.find('div', class_='XQDdHH')
        # Image
        img = product.find('img', class_='DByuf4')
        # Link
        a = product.find('a', class_='CGtC98')

        if None in (n, p, r, img, a):
            continue  # Skip incomplete products

        name.append(n.get_text())
        price.append(p.get_text())
        rate.append(r.get_text())
        image.append(img['src'])
        link.append("https://www.flipkart.com" + a['href'])

        if len(name) >= num_items:
            break

    page += 1
    time.sleep(1)  # Be polite and avoid being blocked

# Create DataFrame
df = pd.DataFrame({
    "Names": name[:num_items],
    "Prices": price[:num_items],
    "Rating": rate[:num_items],
    "Images": image[:num_items],
    "Links": link[:num_items]
})

# Save to CSV
df.to_csv("Mobiles.csv", index=False)
print(f"\n✅ Scraped {len(df)} MI mobile(s) and saved to 'Mobiles.csv'")
