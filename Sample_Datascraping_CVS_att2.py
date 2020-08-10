# -*- coding: utf-8 -*-
"""
Created on Sat Aug  8 15:24:23 2020

@author: bin_h

Data Scraping with Beautiful Soup based on Mr./Dr.? Phuc's guide with
some modifications

"""

import bs4
from urllib.request import urlopen as uReq # Import stuff from urllib library
from bs4 import BeautifulSoup as Soup # import BeautifulSoup and name it Soup

import re
def formaturl(url):
    if not re.match('(?:http|ftp|https)://', url):
        return 'http://cvs.com{}'.format(url)
    return url

#Step 1: DOWNLOAD AND PARSE 

# define the url you want to scrape
my_url = 'https://www.cvs.com/store-locator/cvs-pharmacy-locations/Colorado;jsessionid=VoD5BVVFRwudyOanePOv6Kt6w1DllckVoYTDb6WP'


# Download your url's HTML file
uClient = uReq(my_url)
# Read your HTML file from the url
page_html= uClient.read()
uClient.close() # close the big HTML file to prevent scraping explosion

#Parse the html, dissecting the code and assign meaning with BeautifulSoup
# syntax is soup(filename, type to parse)
# of course you have to define a variable to save the work after soup done parsing
page_soup = Soup(page_html, "html.parser") 



#Step 2: EXTRACT THE ELEMENT OF INTEREST FROM THE HTML FILE 
# Soup sytax: object.findAll("hmtl tag category",{"tag subcategory":"tagname"})
# remember to save the container
containers = page_soup.findAll("div", {"class":"states"})

container0 = containers[0].ul

# After look at the HTML code, find the name of the graphics 
# card you want to use inside container 
# One needs to look at the actual html code for this
# SYNTAX: object.tag.tag.tag.tag["attribute_name"]
# "]

# # Incase the previous syntax does not work, again use findAll
href_loc_all = container0.findAll("a",href=True) 
# this is the list of all hyper links of CVS location in Colorado
loc_num = len(href_loc_all)

filename = "cvs_address.csv"
f = open(filename,"w")

 #Write Header
headers = "CVS_locations"
f.write(headers)

# Extract location one by one
for ii in range(loc_num):
    href_loc_all0_raw  = href_loc_all[ii]
    href_loc_all0 = href_loc_all0_raw['href']
    # # add the http:// prepend to the url we just extracted
    loc_url0 = formaturl(href_loc_all0)

    # Extract store address from the second url
    uClient_loc0 = uReq(loc_url0)
    locpage_html = uClient_loc0.read()
    locpage_soup = Soup(locpage_html,"html.parser")
    
    add_container = locpage_soup.findAll("p",{"class":"store-address"})
    store_loc = [] 
    con_len = len(add_container)
    for jj in range(con_len) :
        store_loc = add_container[jj].text.strip()
        print(store_loc)
        f.write(store_loc + "\n")
        
f.close
# #!!!!!!!!!!! NOTE if object.div does not work use the find() filter

# #Step 3: LOOP THROUGH ALL CONTAINERS and WRITE CSV FILE
# filename = ""
# f = open(filename,"w") # write command, w for write


# #Write Header
# headers = "brand, product_name, shipping"
# f.write(headers)

# for container in containers :
#     # Graphics card name
#     GPX_brand = container.div.div.a.img["title"]
    
#     # Extract name of the card
#     title_container = container.findAll("a",{"class":"item-title"})
#     title = title_container[0].text # grab the text inside the cotainer
    
#     # Shipping 
#     shipping_container = container.findAll("li",{"class":"price-ship"})
#     ship_price = shipping_container[0].text.strip() # the strip() command removes space
    
#     print("brand: ",GPX_brand)
#     print("product_name:", title)
#     print("shipping", ship_price)
    
#     f.write(GPX_brand +"," + title + ","+ ship_price + "\n")