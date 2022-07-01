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

        print('success')
        print(vars(args))

    except Exception as ex:
        print('error: {0}'.format(ex))

# Program
def scrape(url):
    # from selenium import webdriver
    #
    # browser = webdriver.Firefox()

    raise Exception('Not implemented.')

# Entry point
if __name__ == '__main__':
    main()
