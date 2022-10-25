# Web Scraping Script

This repository includes all the Python code I used to gather data from a novel translation archive website. In here, you will find 5 Python files, which consists of 4 different classes and 1 main script.

 1. **logger**<br>
	 This file contains a `Logger` class which is used to keep track of warnings and errors that may or may not happen during runtime and then write it into a file called `logs.log`.
 2. **pool**<br>
	 This file has a function called `create_pool()` which will be called by `Proxer` to generate a set (a pool) of random proxies and headers. This pool will later be passed on as a parameter during the HTTP GET request so the bot will seem more like a normal user and will less likely to get blocked.
 3. **proxer**<br>
    The `Proxer` class in this file keeps track of the IP and header rotations on `main`, does the HTTP request, and then return the HTML response.
 4. **novelparser**<br>
	 Includes the `BeautifulSoup` codes to find the desired information, including maximum number of pages, titles for each page, and details for each novel.
 5. **main**<br>
     Contains a loop to fetch get the HTML response using `Proxer(). open_site()` and parse it using various functions from `NovelParser`.
