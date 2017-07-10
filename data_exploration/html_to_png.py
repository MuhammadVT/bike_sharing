def html_to_png(input_html, output_png="./map.png"):
    """
    This function opens the html file given to input_html, takes a screenshot of it, and saves it
    as a png file.

    Parameters
    ----------
    input_html : str
        Relative path and name of the input html file. e.g., "./map.html" 
    output_png : str
        Relative path and name of the output png file

    Returns
    -------
    Nothing
    """
    import os
    import time
    from selenium import webdriver
    from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

    # delay is needed to give enough time for browser to load input_html file
    delay=5

    # contruct the full path for input_html
    input_url='file://{path}/{mapfile}'.format(path=os.getcwd(),mapfile=input_html)

    # launch firefox
    capabilities = webdriver.DesiredCapabilities().FIREFOX
    capabilities["marionette"] = False
    #binary = FirefoxBinary("/usr/lib/firefox/firefox")
    #browser = webdriver.Firefox(firefox_binary=binary)
    browser = webdriver.Firefox()
    #browser = webdriver.Chrome()

    # open the html file in a browser
    browser.get(input_url)

    #Give the map some time to load
    time.sleep(delay)
    
    # same the screen as png
    browser.save_screenshot(output_png)

    # exit from the browser
    browser.quit()

    return

