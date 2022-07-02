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
FILENAME = 'layout.png'
TARGET_ELEMENT = 'ergodox'
EXTRA_HEIGHT = 20

# Argument parsing and validation
def main():
    import argparse
    import validators

    try:
        parser = argparse.ArgumentParser(description='Scrape ZSA ergodox layout')
        parser.add_argument('url', help='The URL for your layout. Must look like: \'{0}\'. Append /X to select layer.'.format(URL_EXAMPLE))
        parser.add_argument('--hide-logo', action='store_true', help='Hide the EZ logo.')

        args = parser.parse_args()

        if not validators.url(args.url):
            raise Exception('URL provided is malformed.')

        # TODO: Use regex to validate the full URL
        if (len(args.url) < len(URL_EXAMPLE)
            or not args.url.startswith(URL_PREFIX)):
            raise Exception('URL must look like: \'{0}\''.format(URL_EXAMPLE))

        scrape(args.url, args.hide_logo)

    except Exception as ex:
        print('Error: {0}'.format(ex))

# Program
def scrape(url, hide_logo):
    import os
    import time
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait

    try:
        # NOTE: Using this sad hack because the --width and --height arguments
        # don't work in headless mode on Firefox.
        os.environ['MOZ_HEADLESS_WIDTH'] = '1920'
        os.environ['MOZ_HEADLESS_HEIGHT'] = '1080'

        opts = webdriver.FirefoxOptions()
        opts.add_argument('--headless')
        opts.add_argument('--enable-javascript')

        browser = webdriver.Firefox(options=opts)
        browser.maximize_window()

        browser.get(url)

        print('Waiting for page to load...')

        element = WebDriverWait(browser, timeout=PAGE_LOAD_TIMEOUT).until(lambda b: b.find_element(By.CLASS_NAME, TARGET_ELEMENT))

        # Selenium scrolls down for some reason.
        browser.execute_script('window.scrollTo(0, 0)')
        time.sleep(0.5)

        # TODO: Modify CSS for cleaner image.

        if hide_logo:
            logo = browser.find_element(By.CLASS_NAME, 'logo')
            # browser.execute_script('arguments[0].style.visibility = \'hidden\';', logo)
            # This change is reflected in the print output, but not in the saved image. Maddening.
            browser.execute_script('arguments[0].style.border = \'2px solid red\';', logo)
            time.sleep(0.5)
            print(logo.value_of_css_property('border'))

        screenshot(browser, element)

        # print(element.get_attribute('innerHTML'))

    finally:
        try:
            browser.close()
        except Exception as ex:
            print('Error: {0}'.format(ex))

# Save image of element to disk
def screenshot(browser, element):
    from PIL import Image

    try:
        location = element.location
        size = element.size

        browser.save_screenshot('full.png')

        x0 = (int)(location['x'])
        y0 = (int)(location['y'])
        x1 = (int)(x0 + size['width'])
        # Extra height is needed because the visual element extends outside the
        # element's reported borders.
        y1 = (int)(y0 + size['height'] + EXTRA_HEIGHT)

        print('{0}, {1}, {2}, {3}'.format(x0, y0, x1, y1))

        image = Image.open('full.png')
        image = image.crop((x0, y0, x1, y1))
        image = image.save(FILENAME)

        # TODO: Include path.
        print('Image saved to: {0}'.format(FILENAME))

    except Exception as ex:
        print('Error: {0}'.format(ex))

# Entry point
if __name__ == '__main__':
    main()
