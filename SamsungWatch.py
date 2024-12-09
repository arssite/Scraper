import asyncio
import json
from playwright.async_api import async_playwright

async def scrape_amazon_product(url: str) -> dict:
    async with async_playwright() as p:
        browser = await p.webkit.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        
        try:
            await page.goto(url, timeout=60000)
            await page.wait_for_selector('span#productTitle', timeout=30000)

            # Extract product title
            title = await page.inner_text('span#productTitle.a-size-large.product-title-word-break')
            # Extract product price
            price = await page.inner_text('span.a-price-whole')

            product_details = {
                "title": title.strip(),
                "price": price.strip() if price else "Price not available"
            }

            return product_details

        except Exception as e:
            print(f"Error occurred while scraping {url}: {e}")
            return {"title": "Error", "price": "Error"}

        finally:
            await browser.close()

if __name__ == "__main__":
    product_url = "https://www.amazon.com/SAMSUNG-Bluetooth-Smartwatch-Personalized-Advanced/dp/B0C797946T/ref=sr_1_14?sr=8-14"
    product_info = asyncio.run(scrape_amazon_product(product_url))
    
    # Save to JSON file
    with open('output.json', 'w', encoding='utf-8') as f:
        json.dump(product_info, f, indent=4, ensure_ascii=False)

    print("Scraped data:", product_info)
