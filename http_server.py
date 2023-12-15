from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer


class ServerHandler(SimpleHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        super().__init__(request=request, client_address=client_address, server=server)
        self.titles = []
        self.image_urls = []
        self.keep_running = True

    def do_GET(self) -> None:
        """
        Handle GET requests.

        :return: None
        """
        # List the provided titles and image URLs
        items_html = self.list_items()

        # Generate the HTML frame
        html_start, html_end = self.generate_html_frame()

        # Combine the HTML frame with the items HTML
        response = f"{html_start}{items_html}{html_end}"

        # Send the response
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(response.encode('utf-8'))

    def set_titles_and_image_urls(self, titles: list, image_urls: list) -> None:
        """
        Set the titles and image URLs to be displayed in the HTML.

        :param titles: list of titles (strings)
        :param image_urls: list of image URLs (strings)
        :return: None
        """
        self.titles = titles
        self.image_urls = image_urls

    def list_items(self) -> str:
        """
        Generate the HTML for the list of items.

        :return: item part of the HTML (string)
        """
        items = ""
        for title, image_url in zip(self.titles, self.image_urls):
            item_html = f"""
                         <div class="item">
                             <h2>{title}</h2>
                             <img src="{image_url}" alt="{title}">
                         </div>
                         """
            items += item_html
        return items

    @staticmethod
    def generate_html_frame() -> tuple:
        """
        Generate the HTML frame. Specifically, the HTML head and body tags.

        :return: tuple of strings (html_start, html_end)
        """
        html_start = """
                    <!DOCTYPE html>
                    <html lang="en">
                    <head>
                        <meta charset="UTF-8">
                        <meta name="viewport" content="width=device-width, initial-scale=1.0">
                        <title>Simple HTTP Server</title>
                    </head>
                    <body>
                        <h1>Interview Result</h1>
                        <div class="items">
                    """

        html_end = """
                   </div>
                   </body>
                   </html>
                   """

        return html_start, html_end


def send_data_to_http(ip: str, port: int, image_urls: list, titles: list) -> None:
    """
    Run the server.

    :param ip: IP address (str)
    :param port: port number (int)
    :param image_urls: image URLs (list of str)
    :param titles: titles (list of str)
    :return: None
    """
    # Get the server handler
    handler = ServerHandler

    # Set the titles and image URLs
    handler.set_titles_and_image_urls(handler, titles, image_urls)

    # Run the server
    keep_running = True
    with TCPServer((ip, port), handler) as httpd:
        print(f"Serving on http://{ip}:{port}")
        while keep_running:
            httpd.handle_request()
