from flask import Flask, request, jsonify
from lxml import html
import requests

app = Flask(__name__)

@app.route('/scrape', methods=['POST'])
def scrape():
    data = request.get_json()
    videourl = data.get('videourl')

    if videourl:
        url = f"https://10downloader.com/download?v={videourl}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            tree = html.fromstring(response.content)
            
            image_link = tree.xpath('/html/body/div/div/div/div[1]/img/@src')[0]
            href_link = tree.xpath('/html/body/div/div/div/div[2]/div[2]/table[1]/tbody/tr[1]/td[4]/a/@href')[0]
            text_title = tree.xpath('/html/body/div/div/div/div[1]/span[contains(@class, "title")]/text()')[0]

            result = {
                'image_link': image_link,
                'href_link': href_link,
                'text_title': text_title
            }

            return jsonify(result)
        else:
            return jsonify({'error': 'Failed to fetch the page'}), 500
    else:
        return jsonify({'error': 'Video URL is missing'}), 400

if __name__ == '__main__':
    app.run(debug=True)