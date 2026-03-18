import requests
import xml.etree.ElementTree as ET

OUTPUT_FILE = "news.xml"

def fetch_all_cnn():
    urls = [
        "https://www.cnn.com/sitemap/news.xml",
        "https://www.cnn.com/sitemap/article.xml",
        "https://www.cnn.com/sitemap/live-story.xml"
    ]

    all_items = []

    for sitemap in urls:
        try:
            res = requests.get(sitemap, timeout=10)
            root = ET.fromstring(res.text)

            for url in root.findall("{*}url"):
                loc = url.find("{*}loc").text
                lastmod = url.find("{*}lastmod").text

                all_items.append({
                    "title": loc.split("/")[-1],
                    "link": loc,
                    "pubDate": lastmod
                })
        except:
            continue

    return all_items

def build_rss(items):
    rss = ET.Element("rss", version="2.0")
    channel = ET.SubElement(rss, "channel")

    ET.SubElement(channel, "title").text = "CNN Latest News"

    for item in items[:20]:  # 只取最新20条
        i = ET.SubElement(channel, "item")
        ET.SubElement(i, "title").text = item["title"]
        ET.SubElement(i, "link").text = item["link"]
        ET.SubElement(i, "pubDate").text = item["pubDate"]

    tree = ET.ElementTree(rss)
    tree.write(OUTPUT_FILE, encoding="utf-8", xml_declaration=True)

def main():
    items = fetch_all_cnn()
    build_rss(items)
    print("RSS 已生成：news.xml")

if __name__ == "__main__":
    main()
