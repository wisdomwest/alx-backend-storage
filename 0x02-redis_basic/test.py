#!/usr/bin/env python3

from web import count_requests, get_page

# Decorate the get_page function with the count_requests decorator
get_page = count_requests(get_page)

def test_caching():
    # Access the same URL twice
    html1 = get_page('http://slowwly.robertomurray.co.uk/delay/1000/url/http://www.google.co.uk')
    html2 = get_page('http://slowwly.robertomurray.co.uk/delay/1000/url/http://www.google.co.uk')

    # Ensure that the second request returns the cached HTML content
    assert html1 == html2, "Cached content should be returned for the same URL within the expiration time"

if __name__ == "__main__":
    test_caching()
    print("Caching test passed.")

