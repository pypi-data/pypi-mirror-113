import requests
from bs4 import BeautifulSoup

def _get_infos(web_item, actual_version):
    version, __ = web_item.a.string.split('-')
    actual_version_on_web = version.replace(' ', '').removeprefix("Python")

    if actual_version != actual_version_on_web:
        download_list = web_item.ul.find_all("li")
        for link in download_list:
            #return only tarball links
            if link.a.string == "Gzipped source tarball":
                return {actual_version_on_web: link.a['href']}


def update_releases(dev_version, last_stable_version) -> dict:
    try:
        page = requests.get('https://www.python.org/downloads/source/')
        soup = BeautifulSoup(page.text, 'html.parser')
    except Exception:
        return
    
    lists = soup.find_all("div", class_="column")
    stables = lists[0].ul.find_all("li", recursive=False)
    #First ul.li in pre-releases column
    dev = lists[1].ul.li

    respost = {
        "new_dev": {},
        "new_stables": {}
    }

    new_dev = _get_infos(dev, dev_version)
    respost['new_dev'] = new_dev if new_dev else {}

    for web_item in stables:
        new_stable = _get_infos(web_item, last_stable_version)
        if new_stable:
            respost['new_stables'].update(new_stable)
        else:
            #If not found a new_stable, indicates the end
            break;

    return respost
