import time
from src.dataExtractor      import dataExtractor

def main():
    while True:

        data_Extractor = dataExtractor()

        data_Extractor.createContentFiles()
        data_Extractor.updateDatabase()
        data_Extractor.updateDatabaseCompany()
        data_Extractor.getWordAndUrl()
        data_Extractor.getCompanyAndUrl()
        data_Extractor.cleanDuplicates()
        data_Extractor.download_all_article_pages()
        data_Extractor.loop_all_articles()
        data_Extractor.create_markdown_overview("your_database.db", "markdown")

        sleep_time = 7200 # seconds
        time.sleep(sleep_time)

if __name__ == "__main__":
    main()
