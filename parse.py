def parse_html(html):
    import json
    from bs4 import BeautifulSoup
    
    with open("assets\\config.json") as f:
        region = json.load(f)["region"]
        
    if region == "EU":
        website_active_storms_list = ["EU-group-elemental-storms-line-0", "EU-group-elemental-storms-line-1"]
    elif region == "US":
        website_active_storms_list = ["US-group-elemental-storms-line-0", "US-group-elemental-storms-line-1"]
    else:
        print("ERROR - Unsupported region in config file!\nPlease look up if there is typo (supported configs are 'EU' and 'US').\nIf a region is unsupported, please contact the dev.")
        return -1
    
    active_storms = []
    
    # initiates bs4 to parse the html
    soup = BeautifulSoup(html, "html.parser")
    
    # narrows the search down to the dynamically generated content
    tiw_group_wrapper = soup.find_all("section", "tiw-group-wrapper")
    
    for item in tiw_group_wrapper:
        if "EU-group-elemental-storms" in str(item):
            remaining_time = item.find(class_="tiw-active").getText()
            
            for line in website_active_storms_list:
                current_storm = item.find(id=line)
                if "The Waking Shore" in str(current_storm):
                    zone = "The Waking Shore"
                elif "Ohn'ahran Plains" in str(current_storm):
                    zone  = "Ohn'ahran Plains"
                elif "The Azure Span" in str(current_storm):
                    zone = "The Azure Span"
                elif "Thaldraszus" in str(current_storm):
                    zone = "Thaldraszus"
                else:
                    zone = "Unknown"

                classes = current_storm["class"]
                for sec_class in classes:
                    if "water" in sec_class:
                        element = "Water"
                    elif "fire" in sec_class:
                        element = "Fire"
                    elif "air" in sec_class:
                        element = "Air"
                    elif "earth" in sec_class:
                        element = "Earth"
                    else:
                        element = "Unkown"
                        
                this_storm = [zone, element, remaining_time]
                active_storms.append(this_storm)
                   
    return active_storms

if __name__ == "__main__":
    parse_html("test")