import json
import time

from collections import defaultdict

from proxies.utils import upload_proxies


class ProxiesPipeline:
    def open_spider(self, spider):
        self.start_time = time.time()
        self.proxies = []
        self.output_file = open('proxies.json', 'w', encoding='utf-8')
        self.output_file.write('[\n')
        self.first = True

    def process_item(self, item, spider):
        ip = item['ip']
        port = item['port']
        proxy_string = f"{ip}:{port}"
        self.proxies.append(proxy_string)

        if not self.first:
            self.output_file.write(',\n')
        else:
            self.first = False

        json.dump(dict(item), self.output_file, ensure_ascii=False, indent=2)
        return item

    def close_spider(self, spider):
        self.output_file.write('\n]\n')
        self.output_file.close()

        spider.logger.info("Uploading the collected proxies.")

        try:
            token = spider.settings.get("PERSONAL_TOKEN")
            if not token:
                spider.logger.warning("⚠ PERSONAL_TOKEN не задан в settings.py")
                return

            result = upload_proxies(self.proxies, token)

            grouped_results = defaultdict(list)
            offset = 0
            for batch in result:
                save_id = batch.get("save_id")
                if not save_id:
                    continue

                count = batch.get("len")
                batch_proxies = self.proxies[offset:offset + count]
                grouped_results[save_id].extend(batch_proxies)
                offset += count

            with open("results.json", "w", encoding="utf-8") as out:
                json.dump(grouped_results, out, ensure_ascii=False, indent=2)

            spider.logger.info("The response was successfully saved in results.json")

            duration = int(time.time() - self.start_time)
            formatted = time.strftime('%H:%M:%S', time.gmtime(duration))
            with open("time.txt", "w") as f:
                f.write(formatted)

            spider.logger.info(f"Execution time: {formatted}")

        except Exception as e:
            spider.logger.error(f"Error when sending the proxy: {e}")
