# An Customized Site Scraper
This is a great example of web scraping using python. In this example we scraped a categories from an Australian site named [CrazyParts](https://www.crazyparts.com.au/) and extract the products information to CSV that is accepted by [Shopify](https://shopify.com).

# Libraries Used
I tried my best to make the code minimalistic using as much as system libraries.
>- `requests` - For Scraping HTML content
>- `bs4` - For extracting exact tags and classes
>- `csv` - For making csv files and operating on them
>- `psutil` - Loader animation

# How to us ?
 Just type `python3 main.py` and enter the link of any category from the given site. It willl do all the processes, returing errors peacefully.

 # Whats aim of this Repo ?
 >- Demonstrating my python and it's library using skills
 >- An Example of very well documented and well handled web scraper
 >- Teaching beginners how to write scrape website using python. 

 # What scraper extracts?
The scraper scraps :
> Title, 
> Description,
> Variants,
> Images,
> Price,
> SKU

# Installation
Run `pip install -r requirements.txt` to install all required libraries.
> In linux use `pip install -r requirements.txt --break-system-packages`.

Sometimes, some system modules might be missing , use `pip install modulename` to install them.

# Download 
For windows, you can directly [download executable directly from here](https://github.com/prabesharyal/websitesite_scraper_py_requests/tree/main/releases/v1/Site_to_CSV.exe).

# License
All tools posted publicly by [PrabeshAryal](https://github.com/prabesharyal) on github are released under MIT and GPL license and are free to use.