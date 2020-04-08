import requests
import base64
from PIL import Image
from io import BytesIO

resp = requests.get('http://192.168.43.85:7500/api/v1/solarpanel?latitude=-6.21151&longitude=106.74293')
data = resp.json()
encoded_data = data['BestRoofPlacement']

im = Image.open(BytesIO(base64.b64decode(encoded_data)))
im.save('image_result.png','PNG')