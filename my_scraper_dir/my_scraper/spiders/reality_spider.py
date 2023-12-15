import scrapy
from my_scraper_dir.my_scraper.items import RealityItem
# from ..items import RealityItem


class RealitySpider(scrapy.Spider):
    name = "reality"
    base_url = 'https://www.sreality.cz/api/en/v2/estates'
    start_urls = [f'{base_url}?category_main_cb=1&category_type_cb=1&page=1&per_page=20&tms=1702632648401']

    def __init__(self, max_flats: int, database_info: dict):
        """
        Initialize the spider that scrapes the real estate website:
        https://www.sreality.cz/en/search/for-sale/apartments.

        :param max_flats: maximum number of books to collect
        :param database_info: dictionary with the information about the database (format: {"hostname": "hostname",
                                                                                            "username": "username",
                                                                                            "password": "password",
                                                                                            "database": "database"})
        """
        super(RealitySpider, self).__init__()
        # Set the counter of the collected flats to 0 (TODO: use internal counter if possible)
        self.counter = 0

        # Save the info about the database (It is used in pipelines.py)
        self.database_info = database_info

        # Set the maximum number of flat offers to collect
        self.max_flats = max_flats

        # Define the current page
        self.current_page = 1

    def parse(self, response):
        # Create the item to store the information
        item = RealityItem()

        # Parse the JSON response
        data = response.json()

        # The data are a dictionary with the following keys:
        #   - keys: ['meta_description', 'result_size', '_embedded', 'filterLabels', 'title', 'filter', '_links',
        #            'locality', 'locality_dativ', 'logged_in', 'per_page', 'category_instrumental', 'page',
        #            'filterLabels2']
        # The key '_embedded' contains the information about the flats we are interested in. It is a dictionary with
        # the following keys:
        #   - keys: ['estates', 'is_saved', 'not_precise_location_count']
        # The key 'estates' contains the information about the flats we are interested in. It is a list of dictionaries
        # with the following keys:
        #   - keys: ['labelsReleased', 'has_panorama', 'labels', 'is_auction', 'labelsAll', 'seo', 'exclusively_at_rk',
        #   'category', 'has_floor_plan', '_embedded', 'paid_logo', 'locality', 'has_video', 'advert_images_count',
        #   'new', 'auctionPrice', 'type', 'hash_id', 'attractive_offer', 'price', 'price_czk', '_links', 'rus', 'name',
        #   'region_tip', 'gps', 'has_matterport_url'])
        # We are interested in the keys "name" and "_links"
        # The key '_links' contains the information about the links to the next page and the images. It is a dictionary
        # with the following keys:
        #   - keys: ['dynamicDown', 'dynamicUp', 'iterator', 'self', 'images', 'image_middle2'])
        # We are interested in the key "images" which is a list of dictionaries (each dictionary belongs to one image)
        # with the following keys:
        #   - keys: ['href']
        # We are interested in the key "href" which contains the link to the image

        # Get the information from the website
        for flat in data['_embedded']['estates']:
            # Check if the maximum number of flats has been reached
            if self.counter >= self.max_flats:
                break

            # Fill the item with the information
            item["name"] = flat["name"]
            item["image_url"] = flat["_links"]["images"][0]["href"]

            # Yield the information
            yield item

            # Increment the counter
            self.counter += 1

        # Check if the maximum number of flats has been reached
        if self.counter < self.max_flats:
            # Increment the current page
            self.current_page += 1

            # Check if there are more pages and follow the next page link
            next_page = f"https://www.sreality.cz/api/en/v2/estates?category_main_cb=1&category_type_cb=1&" \
                        f"page={self.current_page}&per_page=20&tms=1702632648401"

            # Follow the next page link (Note: if the next page does not exist, the spider will stop -> it is not necessary
            # to check if the next page exists)
            yield scrapy.Request(url=next_page, callback=self.parse)

