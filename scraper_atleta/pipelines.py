from scrapy.exceptions import DropItem

class DuplicatesPipeline:
    def __init__(self):
        self.links_vistos = set()

    def process_item(self, item, spider):
        # Usamos o link como identificador único
        if item['link'] in self.links_vistos:
            raise DropItem(f"Item duplicado removido: {item['titulo']}")
        else:
            self.links_vistos.add(item['link'])
            return item