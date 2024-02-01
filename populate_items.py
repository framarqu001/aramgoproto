import os
import requests
import json
from django.db.utils import IntegrityError

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aramgoproto.settings')

import django
django.setup()

from matchhistory.models import Item

RIOT_API_KEY = 'RGAPI-28c9c5b1-5ec6-4d05-9c94-829504571fb3'

def fetch_items_data():
    response = requests.get("https://ddragon.leagueoflegends.com/api/versions.json")
    versions = response.json()
    latest_version = versions[0]

    url = f"https://ddragon.leagueoflegends.com/cdn/{latest_version}/data/en_US/item.json"
    response = requests.get(url)
    data = response.json()
    return data['data']

def populate_items():
    items_data = fetch_items_data()
    for item_id, item_data in items_data.items():
        name = item_data['name']
        description = item_data['description']
        cost = item_data.get('gold', {}).get('total', 0)
        image_url = f"https://ddragon.leagueoflegends.com/cdn/13.5.1/img/item/{item_data['image']['full']}"

        try:
            item, created = Item.objects.update_or_create(
                item_id=item_id,
                defaults={
                    'name': name,
                    'description': description,
                    'cost': cost,
                    'image_url': image_url
                }
            )

            if created:
                print(f"Added {name} to the database.")
            else:
                print(f"Updated {name} in the database.")
        except IntegrityError:
            print(f"Skipped {name} due to duplicate name entry.")


if __name__ == '__main__':
    print("Starting item population script...")
    populate_items()
