def display_folium_figure(input_html, output_png="map.png"):
    """
    This function saves the folium output map in png format so that it can be 
    displayed in a GitHub page.

    Parameters
    ----------
    input_html : str
        Name of the input html. e.g., "map.html" 
    output_png : str
        Name of the output figure

    Returns
    -------
    Nothing

    Acknowledgment : code for this function is taken from psychemedia's comment in
    the folowing link.
    https://github.com/python-visualization/folium/issues/35#issuecomment-164784086
    """
    import os
    import time
    from selenium import webdriver

    delay=5
    tmpurl='file://{path}/{mapfile}'.format(path=os.getcwd(),mapfile=input_html)
    m.save(input_html)

    browser = webdriver.Firefox()
    browser.get(tmpurl)

    #Give the map tiles some time to load
    time.sleep(delay)
    browser.save_screenshot(output_png)
    browser.quit()

    return

