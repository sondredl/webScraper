import time
from datetime import datetime
from src.dataExtractor      import dataExtractor
from src.dbCleaner          import databaseCleaner
from src.databaseHandler import DbHandler
from src.getStockValue import aksjer24

def main():
    while True:

        database_handler = DbHandler()
        data_Extractor = dataExtractor()
        data_Cleaner = databaseCleaner()
        m_stock = aksjer24()

        # data_Extractor.download_web_pages() # downloads news pages
        # data_Extractor.updateDatabase("temp.db")     # get articles from news pages and store url to database searc_word
        # data_Extractor.getWordAndUrl("temp.db")      # filter articles in word_and_url to get the ones with search word hits
        # data_Extractor.getCompanyAndUrl("temp.db")   # filter articles in word_and_url to get the ones with search word hits

        # data_Extractor.cleanDuplicates("temp.db")
        # data_Extractor.download_all_article_pages("temp.db") # downloads articles from word_and_url to file
        # data_Extractor.loop_all_articles("temp.db", "raw_articles")
        # database_handler.clean_duplicates_in_column("temp.db", "Articles", "url")
        # database_handler.clean_duplicates_in_column("temp.db", "Articles", "title")

        # data_Extractor.create_markdown_overview("temp.db", "markdown")
        # data_Extractor.m_dbCleaner.delete_folder_contents("articles")
        # data_Extractor.m_dbCleaner.delete_folder_contents("htmlFiles")
        # data_Extractor.m_dbCleaner.set_last_time_run()
        # data_Cleaner.delete_all_content_in_table("temp.db", "raw_articles")

        # m_stock.download_web_pages("e24aksjer", "https://e24.no/bors")
        # m_stock.get_content()
        m_stock.download_web_pages("e24aksjer", "https://e24.no/bors/aksjer")
        m_stock.get_content_2()
        data_Extractor.cleanDuplicateRows("temp.db", "Stock_index")
        data_Extractor.delete_rows_with_null_value("temp.db", "Stock_index", "value")

        print()
        print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        print(f"time: {time.time()}")

        sleep_time = 7200 # seconds
        time.sleep(sleep_time)

if __name__ == "__main__":
    main()
