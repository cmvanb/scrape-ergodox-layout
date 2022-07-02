# ------------------------------------------------------------------------------
# scrape.py
#
# Scrape an ergodox layout from the ZSA ergodox layout website.
# Because the print button isn't good enough.
# ------------------------------------------------------------------------------

# Constants
URL_PREFIX = 'https://configure.zsa.io/ergodox-ez/layouts/'
URL_TEMPLATE = 'https://configure.zsa.io/ergodox-ez/layouts/{0}/latest'
URL_EXAMPLE = URL_TEMPLATE.format('XXXXX')
PAGE_LOAD_TIMEOUT = 10

# Argument parsing and validation
def main():
    import argparse
    import validators

    try:
        parser = argparse.ArgumentParser(description='Scrape ZSA ergodox layout')
        parser.add_argument('url', help='The URL for your layout. Must look like: \'{0}\'. Append /X to select layer.'.format(URL_EXAMPLE))

        args = parser.parse_args()

        if not validators.url(args.url):
            raise Exception('URL provided is malformed.')

        # TODO: Use regex to validate the full URL
        if (len(args.url) < len(URL_EXAMPLE)
            or not args.url.startswith(URL_PREFIX)):
            raise Exception('URL must look like: \'{0}\''.format(URL_EXAMPLE))

        scrape(args.url)

        print('Scrape complete.')

    except Exception as ex:
        print('Error: {0}'.format(ex))

# Program
def scrape(url):
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait

    print('Scraping...')

    try:
        opts = webdriver.FirefoxOptions()
        opts.add_argument('--headless')
        opts.add_argument('--enable-javascript')

        browser = webdriver.Firefox(options=opts)

        browser.get(url)

        print('Waiting for page to load...')

        element = WebDriverWait(browser, timeout=PAGE_LOAD_TIMEOUT).until(lambda b: b.find_element(By.CLASS_NAME, 'frame'))

        # TODO: Modify CSS.
        # TODO: Take a screenshot.

        print(element.get_attribute('innerHTML'))

    finally:
        try:
            browser.close()
        except Exception as ex:
            print('Error: {0}'.format(ex))

# Entry point
if __name__ == '__main__':
    main()
