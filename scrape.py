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
PAGE_LOAD_TIMEOUT = 10 # Seconds
OUTPUT_FILENAME = 'layout.png'
TARGET_ELEMENT = 'ergodox'
EXTRA_HEIGHT = 20 # Pixels

# Argument parsing and validation
def main():
    import argparse
    import validators

    try:
        parser = argparse.ArgumentParser(description='Scrape ZSA ergodox layout')
        parser.add_argument('url', help='The URL for your layout. Must look like: \'{0}\'. Append /X to select layer.'.format(URL_EXAMPLE))
        parser.add_argument('--hide-logo', action='store_true', help='Hide the EZ logo.')
        parser.add_argument('--hide-none-icon', action='store_true', help='Hide the \'none\' icon.')
        parser.add_argument('--hide-mod-color', action='store_true', help='Hide the colored background on modifer keys.')

        args = parser.parse_args()

        if not validators.url(args.url):
            raise Exception('URL provided is malformed.')

        # TODO: Use regex to validate the full URL
        if (len(args.url) < len(URL_EXAMPLE)
            or not args.url.startswith(URL_PREFIX)):
            raise Exception('URL must look like: \'{0}\''.format(URL_EXAMPLE))

    except Exception as ex:
        print('Error: {0}'.format(ex))

    scrape(args)

# Program
def scrape(args):
    import os
    import time
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait

    url = args.url
    hide_logo = args.hide_logo
    hide_none_icon = args.hide_none_icon
    hide_mod_color = args.hide_mod_color

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

        if hide_logo:
            logo = browser.find_element(By.XPATH, '//div[@class=\'ergodox\']/div[@class=\'logo\']')
            browser.execute_script('arguments[0].style.visibility = \'hidden\';', logo)
            time.sleep(0.5)

        if hide_none_icon:
            browser.execute_script('document.styleSheets[1].insertRule(".icon-none:before { content: none !important; border: 2px solid red; }")')
            time.sleep(0.5)

        if hide_mod_color:
            # TODO: Implement.
            time.sleep(0.5)

        # input('press ENTER to continue')

        screenshot(browser, element)

    finally:
        try:
            browser.close()
        except Exception as ex:
            raise Exception from ex

# Save image of element to disk
def screenshot(browser, element):
    import os
    from PIL import Image

    try:
        temp_filename = 'temp.png'

        browser.save_screenshot(temp_filename)

        x0 = (int)(element.location['x'])
        y0 = (int)(element.location['y'])
        x1 = (int)(x0 + element.size['width'])
        # Extra height is added because the visual element extends outside the
        # element's reported borders.
        y1 = (int)(y0 + element.size['height'] + EXTRA_HEIGHT)

        image = Image.open(temp_filename)
        image = image.crop((x0, y0, x1, y1))
        image = image.save(OUTPUT_FILENAME)

        os.remove(temp_filename)

        # TODO: Include path.
        print('Image saved to: {0}'.format(OUTPUT_FILENAME))

    except Exception as ex:
        raise Exception from ex

# Entry point
if __name__ == '__main__':
    main()
