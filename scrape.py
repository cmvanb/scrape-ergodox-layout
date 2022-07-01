
URL_PREFIX = 'https://configure.zsa.io/ergodox-ez/layouts/'

def main():
    import argparse
    import validators

    try:
        parser = argparse.ArgumentParser(description='Scape ZSA ergodox layout')
        parser.add_argument('url', help='The URL for your layout. Must begin with: \'{0}\''.format(URL_PREFIX))

        args = parser.parse_args()

        if not validators.url(args.url):
            raise Exception('URL provided is malformed.')

        if (len(args.url) < len(URL_PREFIX)
            or not args.url.startswith(URL_PREFIX)):
            raise Exception('URL must begin with: \'{0}\''.format(URL_PREFIX))

        scrape(args.url)

        print('success')
        print(vars(args))

    except Exception as ex:
        print('error: {0}'.format(ex))

def scrape(url):
    # from selenium import webdriver
    #
    # browser = webdriver.Firefox()

    raise Exception('Not implemented.')

# ------------------------------------------------------------------------------
# Entry point
# ------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
