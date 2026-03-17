import requests
import xml.etree.ElementTree as ET

OUTPUT_FILE = "news.xml"

def fetch_cnn():
    url = "https://www.cnn.com/sitemap/news.xml"
    res = requests.get(url, timeout=10)

    if res.status_code != 200:
        print("CNN 请求失败")
        return []

    try:
        root = ET.fromstring(res.text)
    except:
        print("XML 解析失败")
        return []

    items = []
    for url in root.findall("{*}url"):
        loc = url.find("{*}loc").text
        lastmod = url.find("{*}lastmod").text

        items.append({
            "title": loc.split("/")[-1],
            "link": loc,
            "pubDate": lastmod
        })
    return items

def build_rss(items):
    rss = ET.Element("rss", version="2.0")
    channel = ET.SubElement(rss, "channel")

    ET.SubElement(channel, "title").text = "CNN Latest News"

    for item in items[:20]:
        i = ET.SubElement(channel, "item")
        ET.SubElement(i, "title").text = item["title"]
        ET.SubElement(i, "link").text = item["link"]
        ET.SubElement(i, "pubDate").text = item["pubDate"]

    tree = ET.ElementTree(rss)
    tree.write(OUTPUT_FILE, encoding="utf-8", xml_declaration=True)

def main():
    items = fetch_cnn()
    build_rss(items)
    print("RSS updated")

if __name__ == "__main__":
    main()
