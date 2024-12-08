import os
import cloudscraper
import json
import requests
from bs4 import BeautifulSoup
from flask_cors import CORS
import flask
from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

def product_info_url_goat(SKU):
    try:
        product_id_url = f"https://ac.cnstrc.com/search/{SKU}?c=ciojs-client-2.29.12&key=key_XT7bjdbvjgECO5d8&i=5c1db6a2-7a42-4cbd-9606-96a08face508&s=23&num_results_per_page=25&_dt=1679422941544"
        scraper = cloudscraper.create_scraper()
        request = scraper.get(product_id_url)
        json_product = json.loads(request.text)
        ID = json_product['response']['results'][0]['data']['id']
        base_url = "https://www.goat.com/web-api/v1/product_variants/buy_bar_data?productTemplateId="
        request_url = base_url + ID + "&countryCode=EU"
        scraper2 = scraper.get(request_url)
        json_product2 = json.loads(request.text)
        print("Scraped GOAT URL!")
        print(request_url)
        return request_url
    except:
        return ("https://www.goat.com/")
    

def prod_description_goat(SKU):
    try:
        request_url = product_info_url_goat(SKU)
        scraper = cloudscraper.create_scraper()
        request = scraper.get(request_url)
        print(request_url)
        print(request.text)
        output = json.loads(request.text)
        
        return output
        
    
    except:
        return ("Something went wrong, please try again later!")

#gets sizes and prices of product
def product_sizes_goat(SKU):
    try:
        request_url = product_info_url_goat(SKU)
        scraper = cloudscraper.create_scraper()
        request = scraper.get(request_url)
        output = json.loads(request.text)

        results = []
        for entry in output:
            if (entry['shoeCondition'] == "new_no_defects") and (entry['boxCondition'] == "good_condition"):
                size = entry['sizeOption']['presentation']
                try:
                    price_cents = entry['lowestPriceCents']['amount']
                except KeyError:
                    price_cents = 'OOS!'
                results.append((size, price_cents))

        results2 = []
        for entry in output:
            if (entry['shoeCondition'] == "new_no_defects") and (entry['boxCondition'] == "good_condition"):
                size = entry['sizeOption']['presentation']
                try:
                    price_cents = entry['lowestPriceCents']['amount'] / 100
                    price_euro1 = price_cents - 1
                    price_euro = str(price_euro1) + "€"
                except KeyError:
                    price_euro = 'OOS!'
                results2.append((size, price_euro))

        prices = [(size, price.replace('.0', '')) for size, price in results2]
        output_str = ""
        for element in prices:
            output_str += f"{element[0]} : {element[1]}\n"

        print("Scraped GOAT prices!")
        return output_str
    except Exception as e:
        return jsonify({
            'error': 'No product Found!',
            'details': str(e)
        }), 500


def product_img_goat(SKU):
    try:
        url = f"https://ac.cnstrc.com/search/{SKU}?c=ciojs-client-2.29.12&key=key_XT7bjdbvjgECO5d8&i=5c1db6a2-7a42-4cbd-9606-96a08face508&s=23&num_results_per_page=25&_dt=1679422941544"
        scraper = cloudscraper.create_scraper()
        request = scraper.get(url)
        json_product = json.loads(request.text)
        img = json_product['response']['results'][0]['data']['image_url']
        
        print("Scraped GOAT product picture!")
        return img
    except:
        return ("https://www.freecodecamp.org/news/content/images/2021/03/ykhg3yuzq8931--1-.png")



def product_title_goat(SKU):
    try:
        url = f"https://ac.cnstrc.com/search/{SKU}?c=ciojs-client-2.29.12&key=key_XT7bjdbvjgECO5d8&i=5c1db6a2-7a42-4cbd-9606-96a08face508&s=23&num_results_per_page=25&_dt=1679422941544"
        scraper = cloudscraper.create_scraper()
        request = scraper.get(url)
        json_product = json.loads(request.text)
        title = json_product['response']['results'][0]['value']
        print("Scraped GOAT product title!")
        return title
    except:
        return ("Title not found!")

def product_url_goat(SKU):
    try:
        base_url = "https://www.goat.com/sneakers/"
        url = f"https://ac.cnstrc.com/search/{SKU}?c=ciojs-client-2.29.12&key=key_XT7bjdbvjgECO5d8&i=5c1db6a2-7a42-4cbd-9606-96a08face508&s=23&num_results_per_page=25&_dt=1679422941544"
        scraper = cloudscraper.create_scraper()
        request = scraper.get(url)
        json_product = json.loads(request.text)
        slug = json_product['response']['results'][0]['data']['slug']
        product_url = base_url + slug
        print("Scraped GOAT product url: " + product_url)
        return product_url
    except:
        return("https://www.goat.com/")



def product_url_hypeboost(SKU):
    try:
        url = "https://hypeboost.com/en/search/shop?keyword=" + SKU

        headers = {
            "cookie": "country=eyJpdiI6ImlCRDJaRExPQkZYNTNlMmM0OWFEQVE9PSIsInZhbHVlIjoiTFRaRW01UW5wNUY2RjZnQzViWGlPYWRtYVRmbmxxMXpoRjNzODlZZUdIZmNLWjZSTFp0Q3htbTFuYUF4ZGkwVSIsIm1hYyI6IjQ0MzBlZTdkZmNhYjVhYmJhMDAzNDhlNjQ3MGU5NzQ1YThkOTk0ZDRkNzYxZGQzYzg0ODI0ZWYzZWZhODBlZGYiLCJ0YWciOiIifQ%253D%253D; currency=eyJpdiI6ImFlbkxaNHJyOHdUZlJFRlJ2dGlna0E9PSIsInZhbHVlIjoieEx2OE01VHhzOGZ1eFdsM09IVDFIZmR6R1hieHpDRDZScWoweVhqTDZjUzY2a3FFUmhQZGdPV2piaFN3OTViTCIsIm1hYyI6IjgzMTY0NDExNzljYjM1MzFmZmM5ZTBhOGY0MjU3ZWViMjA2NjBjYmUwMjg0MDFkMmUyYmJiNTVjYTUxZTk5MjMiLCJ0YWciOiIifQ%253D%253D",
            "Content-Type": "application/json"
        }

        response = requests.request("GET", url, headers=headers)

        soup = BeautifulSoup(response.content, 'html.parser')

        for a in soup.find_all('a', href=True):
            print('Scraped product url!')
            return a['href']
    except:
        return ("https://hypeboost.com/")

def stockx_url(SKU):
    try:
        url = "https://stockx.com/api/browse?_search=" + SKU

        headers = {
                'accept': 'application/json',
                'accept-encoding': 'utf-8',
                'accept-language': 'en-DE',
                'app-platform': 'Iron',
                'referer': 'https://stockx.com/en-DE',
                'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
                'x-requested-with': 'XMLHttpRequest'
            }

        request1 = requests.get(url=url, headers=headers)

        product_id = json.loads(request1.text)
        product_id_final = product_id['Products'][0]['id']

        ID = product_id_final
        url_stockX = "https://stockx.com/" + ID
        print("Scraped StockX URL: " + url_stockX)
        return url_stockX
    except:
        return ("https://stockx.com/de-de")

def restocks_url(SKU):
    try:
        base_url = 'https://restocks.net/de/shop/search?q='
        request_url = base_url + SKU + '&page=1&filters[0][range][price][gte]=1'

        r = requests.get(request_url)

        json_restocks = json.loads(r.text)
        product_url = json_restocks["data"][0]['slug']
        print('Scraped Restocks URL: ' + product_url)
        return product_url
    except:
        return ("https://restocks.net/de")


def sneakit_url(SKU):
  try:
    produkt_code = SKU
    global url
    url = f"https://sneakit.com/search/products/{produkt_code}?query={produkt_code}&page=1"
    print("Scraped Sneakit URL!", url)
    return url
  except:
    return ("https://sneakit.com/")

def sneakit_product_url(SKU):
  try:
    raw = sneakit_info(SKU)
    slug = raw['data'][0]['slug']
    p_url = "https://sneakit.com/product/" + slug
    print("Scraped Sneakit Product URL:" + p_url)
    return p_url
  except:
    return ("https://sneakit.com/")


def sneakit_info(SKU):
  try:
    scraper = cloudscraper.create_scraper()
    sneakit_url_r = sneakit_url(SKU)
    r = scraper.get(sneakit_url_r)
    global output
    output = json.loads(r.text)
    print("Scraped Sneakit info!")
    return output
  except:
    return ("error")


# SKU = "CT8012-104"  # Replace with the actual SKU value
# response = product_sizes_goat(SKU)
# print(response)




@app.route('/v1/product/prices', methods=['GET'])
def scrape_products_prices(): 
    try:
        # Combine parameters from JSON body and query parameters
       skuData= request.args.get('sku')
       if not skuData:
           return jsonify({"error": "The sku parameter is required"}), 400
       
       result= product_sizes_goat(skuData)
       
       # Return the result as JSON
       return jsonify(result) 

    except Exception as e:
        return jsonify({
            'error': 'Something went wrong!',
            'details': str(e)
        }), 500
        


@app.route('/v1/product/description', methods=['GET'])
def scrape_products_description(): 
    try:
        # Combine parameters from JSON body and query parameters
       skuData= request.args.get('sku')
       if not skuData:
           return jsonify({"error": "The sku parameter is required"}), 400
       
       result= prod_description_goat(skuData)
       
    #    print(result)
       
       # Return the result as JSON
       return jsonify(result) 

    except Exception as e:
        return jsonify({
            'error': 'Something went wrong!',
            'details': str(e)
        }), 500
        


@app.route('/', methods=['GET'])
def home_page(): 
    # Return the result as JSON
    return jsonify({"message": "This is a Goat API"})
   




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)