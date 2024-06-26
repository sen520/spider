#### some technology about scrapy

###### before start

environment: python3

pip install -r requirement

    
###### file  

- download (orign: https://matplotlib.org/examples/index.html)
    - download file from orign

###### start

`python start.py`

`'scrapy', 'crawl', 'download'` the third `download` is the name of the spider 

if you want to save a Specific type file run like this `scrapy crawl -t csv -o data.csv`

You can choose the following types
    
- json
- jsonlines
- jl
- csv - settings.py `FEED_EXPORT_ENCODING = "gb18030"`
- xml
- marsha1
- pickle

###### settings.py

`DOWNLOAD_DELAY = 1` Visit the page every 1 seconds

- open custom cookies
    - settings.py
    ```python
  COOKIES_ENABLED = False
    ```
    - spider_file
    ```python
  custom_settings = {
    'DEFAULT_REQUEST_HEADERS': {}
  }
    ```
- download file

   `FILES_STORE` is where your file save
   
   ``` python
   ITEM_PIPELINES = {
    'scrapy_spider.pipelines.FileSpiderPipeline': 1,
    }
    ```

- save mongo
    
    
    
    ```python
    mongo = {
        # MONGODB HOST
        "MONGODB_HOST": "127.0.0.1",
        # MONGODB PORT
        "MONGODB_PORT": 27018,
        # DB NAME
        "MONGODB_DBNAME": "spider"
    }
    
    ```