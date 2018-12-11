import requests
import os
import argparse
from dotenv import load_dotenv

def create_link(long_url, token):
    payload = {
      "long_url":long_url
    }
    headers = {
        "Authorization": "Bearer {}".format(token)
    }
    host = 'https://api-ssl.bitly.com/v4/bitlinks' 
    response = requests.post(url=host, json=payload, headers=headers)
    if response.ok:
      return response.json()['id']
    else:
      return None

def get_amount_clicks(url, token):
    headers = {
        "Authorization": "Bearer {}".format(token)
    }
    host = 'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary'.format(bitlink=url) 
    params = {
      'units':''
    }
    response = requests.get(url=host, headers=headers,params = params)
    return response.json()['total_clicks']  

def is_bitlink(link, token):
  headers = {
      "Authorization": "Bearer {}".format(token)
  }
  host = 'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}'.format(bitlink=link) 
  response = requests.get(url=host, headers=headers)
  return response.ok 

def main():
  parser = argparse.ArgumentParser(
      description='Программа создает ссылку битли или показывает статистику переходов по битли ссылке.'
  )
  load_dotenv()
  parser.add_argument('link', help='Ссылка')
  args = parser.parse_args()
  link = args.link
  token = os.getenv("TOKEN")
  if is_bitlink(link, token):
    result = get_amount_clicks(link, token)
  else:
    result = create_link(link, token)
  if result is None:
    print('Введена некорректная ссылка')
  else:
    print(result)

if __name__ == '__main__':
  main()
