# Luxonis-interview

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