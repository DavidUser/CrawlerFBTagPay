#!/usr/bin/env python

import crawler
from webservice import webservice, CrawlerWork

def main():
    """Main function
    """
    crawler_working = CrawlerWork()
    crawler_working.daemon = True
    crawler_working.start()
    webservice.run('0.0.0.0')

if __name__ == "__main__":
    main()
