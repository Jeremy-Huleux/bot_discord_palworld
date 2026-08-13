import aiohttp
import feedparser
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator

class NewsService:
    def __init__(self, database):
        self.database = database
        self.feeds = [
            {
                "name": "Steam",
                "url": "https://store.steampowered.com/feeds/news/app/1623730/"
            }
        ]
        self.translator = GoogleTranslator(source='auto', target='fr')

    def categorize_news(self, title: str) -> str:
        title_lower = title.lower()
        patch_keywords = ["patch", "fix", "update", "v1.", "v0.", "changelog", "balance", "bug"]
        if any(kw in title_lower for kw in patch_keywords):
            return "patch_notes"
            
        event_keywords = ["event", "halloween", "sale", "drop", "tournament", "summer"]
        if any(kw in title_lower for kw in event_keywords):
            return "events"
            
        return "news"

    def extract_details(self, html_content: str):
        if not html_content:
            return "", ""
        
        soup = BeautifulSoup(html_content, "html.parser")
        
        # 1. Extraire la première image trouvée
        img_tag = soup.find("img")
        image_url = img_tag["src"] if img_tag else ""
        
        # 2. Nettoyer le texte (enlever le HTML) et garder un extrait court
        text = soup.get_text(separator=" ", strip=True)
        summary = text[:300] + "..." if len(text) > 300 else text
        
        return summary, image_url

    async def fetch_news(self):
        results = []
        async with aiohttp.ClientSession() as session:
            for feed_info in self.feeds:
                try:
                    async with session.get(feed_info["url"], timeout=aiohttp.ClientTimeout(total=15)) as response:
                        if response.status != 200:
                            continue
                        content = await response.text()
                        
                    feed = feedparser.parse(content)

                    for entry in feed.entries:
                        guid = entry.get("id", entry.get("link"))
                        if not guid or self.database.news_exists(guid):
                            continue
                            
                        raw_title = entry.get("title", "Sans titre")
                        raw_summary = entry.get("summary", entry.get("description", ""))
                        
                        # Extraction texte propre + image
                        clean_summary, image_url = self.extract_details(raw_summary)
                        
                        # Traduction
                        try:
                            title_fr = self.translator.translate(raw_title)
                            summary_fr = self.translator.translate(clean_summary) if clean_summary else ""
                        except Exception as e:
                            print(f"Erreur de traduction : {e}")
                            title_fr = raw_title
                            summary_fr = clean_summary

                        news = {
                            "guid": guid,
                            "title": title_fr,
                            "summary": summary_fr,
                            "image": image_url,
                            "url": entry.get("link", ""),
                            "published": entry.get("published", ""),
                            "source": feed_info["name"],
                            "category": self.categorize_news(raw_title) # On catégorise sur le titre original anglais
                        }
                        results.append(news)
                except Exception as error:
                    print(f"Erreur récupération {feed_info['name']} : {error}")
                    
        return results

    def mark_as_sent(self, news):
        self.database.save_news(
            guid=news["guid"],
            title=news["title"],
            url=news["url"],
            published=news["published"],
            source=news["source"]
        )
