import requests, os
from bs4 import BeautifulSoup
import csv

from modules.loader import Loader

def extract_html(link):
    resp = requests.get(link,allow_redirects=False)
    if resp.status_code == 200:
        this_has_cont = resp.text
        soup = BeautifulSoup(this_has_cont, "html.parser")
        return soup
    else :
        return False


def get_required_stuffs(soup_element):
    all_products_in_page = soup_element.find_all("a", class_="product-image fadein")

    try:
        pages_existence = soup_element.find("div", class_="pages").find_all("a")
        flag = True
        page_links = [pages["href"] for pages in pages_existence]
    except AttributeError as e:
        flag = False
        page_links = []

    just_products_links_in_this_page = [
        linkypinky["href"] for linkypinky in all_products_in_page
    ]
    return just_products_links_in_this_page, flag, page_links


def extract_from_product_page(product_page):
    scraped_html = requests.get(product_page).text
    soup_elem_for_product = BeautifulSoup(scraped_html, "html.parser")
    try :
        product_category = (
        soup_elem_for_product.find("div", class_="breadcrumbs")
        .find("ul")
        .text.split("\n")
    )
    except Exception as e:
        product_category = ['','Home', '']
    shortened = soup_elem_for_product.find("div", class_="product-view")

    try :
        title = shortened.find("div", class_="product-title").find("h1").text
    except Exception as e:
        title = ""

    try :
        description = shortened.find("div", class_="details-container").text
    except Exception as e:
        description = ""

    try :
        sku = shortened.find("p", class_="pro_sku").find("span").text
    except Exception as e:
        sku = ""

    try:
        variations = [
            swtach_image["title"]
            for swtach_image in shortened.find(
                "div", class_="swatchesContainer"
            ).find_all("a")
        ]
    except AttributeError:
        variations = []
    # images
    try:
        images_links = shortened.find_all("a", class_="cloud-zoom-gallery")
        extracted_images = [image["href"] for image in images_links]
        # all_images =
        #     print(pages["href"])
    except AttributeError as e:
        extracted_images = []
        # print("Can't find other pages")

    try :
        price = float(
        shortened.find("div", class_="retail-price").find("span", "price").text[1:]
    )
    except Exception as e:
        price = 0.0

    try :
        package_contents = shortened.find("p", class_="product_number").find("span").text
    except Exception as e:
        package_contents = ''

    return (
        product_category,
        title,
        description,
        variations,
        price,
        package_contents,
        extracted_images,
        sku,
    )

# ALL_PAGES_LINK = []
# def extract_more_pages(link):
#     hehe = extract_html(link)


def a_main(give_a_link):
    filename = give_a_link.split("/")[-1].split(".")[0]
    filename = filename + ".csv"
    # The `filename` variable is being used to generate the name of the CSV file that will be created
    # based on the input link provided by the user. It extracts the last part of the URL after
    # splitting it by '/' and '.' to create a unique filename for the CSV file.
    os.makedirs("CSVs") if not os.path.exists(os.path.join(os.getcwd(),'CSVs')) else None
    filename = os.path.join(os.getcwd(),'CSVs',filename)
    saved_as = filename
    print("%50s"%"Checking Link ...")
    soup = extract_html(give_a_link)
    if soup == False:
        print("%50s"%"Incorrect Link or some Network Issue Occurred ! \n\n Try again!")
        return None
    print("%50s"%"Starting to extract ...")
    product_links, has_other, pages_links = get_required_stuffs(soup)
    if has_other:
        print("%50s"%"Found Multiple Pages, So Extracting Them too :)")
        c = 2
        with Loader("%50s"%"Extracting Page :   ","%50s"%"Extracted All {} Pages of This Category".format(str(c))):
            old_product_size = len(product_links)-1
            while True:
                new_product_size = len(product_links)
                if new_product_size == old_product_size:
                    break
                old_product_size = new_product_size
                print(str(c-2),end='', flush=True)
                soup_sub = extract_html(give_a_link + "?p=" + str(c))
                if soup_sub!= False:
                    more_product_links = get_required_stuffs(soup_sub)[0]
                    product_links.extend(more_product_links)
                    product_links = list(set(product_links))
                else:
                    break
                c += 1

        # print("%50s" % f"Extracted Product Links from {str(c)} pages")

    total_products = len(product_links)
    print("%50s" % f"Total Product Links : {str(total_products)}")
    with Loader("%50s"%"Extrating Information of Product :   ","%30s"%"Extracted Product Details of all {} products".format(str(total_products))):
        for index, each_product in enumerate(product_links):
            try:
                print(f"{str(index+1)}/{str(total_products)}",end='', flush=True)
                (
                    product_category,
                    title,
                    description,
                    variations,
                    price,
                    package_contents,
                    extracted_images,
                    sku,
                ) = extract_from_product_page(each_product)
                product_category = product_category = [
                    value for value in reversed(product_category) if value.strip()
                ][0]
                # product_category = "> ".join(product_category)

                if index == 0:
                    headers = [
                        "Handle",
                        "Title",
                        "Body (HTML)",
                        "Vendor",
                        "Product Category",
                        "Type",
                        "Tags",
                        "Published",
                        "Option1 Name",
                        "Option1 Value",
                        "Option2 Name",
                        "Option2 Value",
                        "Option3 Name",
                        "Option3 Value",
                        "Variant SKU",
                        "Variant Grams",
                        "Variant Inventory Tracker",
                        "Variant Inventory Qty",
                        "Variant Inventory Policy",
                        "Variant Fulfillment Service",
                        "Variant Price",
                        "Variant Compare At Price",
                        "Variant Requires Shipping",
                        "Variant Taxable",
                        "Variant Barcode",
                        "Image Src",
                        "Image Position",
                        "Image Alt Text",
                        "Gift Card",
                        "SEO Title",
                        "SEO Description",
                        "Google Shopping / Google Product Category",
                        "Google Shopping / Gender",
                        "Google Shopping / Age Group",
                        "Google Shopping / MPN",
                        "Google Shopping / AdWords Grouping",
                        "Google Shopping / AdWords Labels",
                        "Google Shopping / Condition",
                        "Google Shopping / Custom Product",
                        "Google Shopping / Custom Label 0",
                        "Google Shopping / Custom Label 1",
                        "Google Shopping / Custom Label 2",
                        "Google Shopping / Custom Label 3",
                        "Google Shopping / Custom Label 4",
                        "Variant Image",
                        "Variant Weight Unit",
                        "Variant Tax Code",
                        "Cost per item",
                        "Price / International",
                        "Compare At Price / International",
                        "Status",
                    ]
                    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow(headers)

                values = [
                "",
                title[:69],
                "",
                title.split(" ")[0],
                product_category,
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                sku,
                "",
                "",
                "",
                "",
                False,
                price,
                "",
                "",
                "",
                "",
                extracted_images[0],
                "",
                title[:69],
                "",
                title[:69],
                description[:319].replace("\n", ""),
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                extracted_images[0],
                "",
                "",
                price,
                "",
                "",
                "active",
            ]
                values[8] = f"Variant {variations[0]}" if len(variations) > 0 else ""
                values[9] = variations[0] if len(variations) > 0 else ""
                values[10] = f"Variant {variations[1]}" if len(variations) > 1 else ""
                values[11] = variations[1] if len(variations) > 1 else ""
                values[12] = f"Variant {variations[2]}" if len(variations) > 2 else ""
                values[13] = variations[2] if len(variations) > 2 else ""

                with open(filename, "a", newline="", encoding="utf-8") as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(values)

                if len(extracted_images)>1:
                    for images in extracted_images[1:]:
                        for index,hmmm in enumerate(values):
                            values[index] = ""
                        values[25] = images  
                        with open(filename, "a", newline="", encoding="utf-8") as csvfile:
                            writer = csv.writer(csvfile)
                            writer.writerow(values)
            except Exception as e:
                print("Error extracting", end='')
                print(f"{str(index+1)}/{str(total_products)}", flush=True)
    return saved_as

while True:
    enter = input("%50s"%"Enter link to Turn into CSV or press 'q' or 'exit' or 'no' to quit : \n")
    if (
        enter.lower() == "q"
        or enter.lower() == "no"
        or enter.lower() == "n"
        or enter.lower() == "exit"
    ):
        exit(0)
    else :
        try:
            FILE = a_main(enter)
            if FILE != None:
                print("%50s"%"Your CSV File is exported as : "+FILE)
            else:
                print("%50s"%"Some Known Error")
        except Exception:
            print("%50s" % "Some Unknown Error occurred!")
        print("\n\n")
