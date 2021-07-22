from copy import Error
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# Create a Chrome window
chrome = webdriver.Chrome("C:\chromedriver_win32\chromedriver")
chrome.maximize_window()

#I declare the page i am looking for
chrome.get("https://rl.insider.gg/es/pc/cristiano_infinite")

txt = open("ItemsRocketLeague.txt", "r+")
content = txt.readlines()

inventory = {}
priceUpdate = {}
linesIndex = {}
index = 0

#Load the inventory from the txt file
for line in content:
    linesIndex.__setitem__(line, index)
    if (("Plano" not in line and "cr mandar md" not in line and "Mister Monsoon" not in line and "varios colores" not in line) and ("[H]" in line)):
        line = line.replace("[H] ", "").split(" [W] ")
        inventory.__setitem__(line[0], int(line[1].replace("cr\n", "")))
        print(line[0] +" => "+ (line[1].replace("cr\n", "")))
    index += 1

for item in inventory:
    #Take the search input in the page
    time.sleep(5)
    try:
        searchInput = chrome.find_element_by_xpath("//input[@id='itemSearch']")
        #Clean it
        searchInput.clear()
    except Error:
        print(Error)

    origineItem = item
    item = item.lower()
    itemWords = item.split()
    redoItem = item

    if ("color" in itemWords):
        redoItem = redoItem.replace(" color", "")
    print(redoItem)
    searchInput.send_keys(redoItem)
    #Type what you are looking for
    searchInput.send_keys(Keys.ENTER)
    time.sleep(5)
    itemPrice = chrome.find_element_by_xpath("//h1[@id='itemSummaryPrice']").get_attribute("innerHTML")
    itemPrice = itemPrice.split(" - ")
    minPrice = itemPrice[0]
    maxPrice = itemPrice[1]

    print("Precio minimo: "+minPrice)
    print("Precio maximo: "+maxPrice)
    print(inventory[origineItem])

    if ("k" in itemPrice[1]):
        minPrice = int(float(itemPrice[0]) * 1000)
        maxPrice = int(float(itemPrice[1].replace(" k", "")) * 1000)
        
    if (inventory[origineItem] < int(minPrice) or inventory[origineItem] > int(maxPrice)):
        print("Precio desactualizado. Precio en el .txt: "+str(inventory[origineItem])+". Rango de precio actual: "+ str(minPrice)+" - "+ str(maxPrice)+".")
        newPrice = int((int(maxPrice) - int(minPrice)) / 2 + int(minPrice))
        print("Nuevo precio recomendado: "+str(newPrice))
        # priceUpdate [vieja linea, nueva linea]  
        priceUpdate.__setitem__("[H] "+origineItem+" [W] "+str(inventory[origineItem])+"cr", "[H] "+origineItem+" [W] "+str(newPrice)+"cr")

newContent = ""
count = 0
for line in content:
    if (line.replace("\n", "") in priceUpdate.keys()):
        newContent += priceUpdate[line.replace("\n", "")]+"\n"
    else:
        if (count == 0):
            line = ""
        newContent += line
txt.close()
txt = open("ItemsRocketLeague.txt", "w")
txt.write(newContent)
txt.close()