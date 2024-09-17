import time
from src.dataExtractor      import dataExtractor

def main():
    while True:

        data_Extractor = dataExtractor()

        # data_Extractor.download_web_pages() # downloads news pages
        data_Extractor.updateDatabase("temp.db")     # get articles from news pages and store url to database searc_word
        data_Extractor.getWordAndUrl("temp.db")      # filter articles in word_and_url to get the ones with search word hits
        data_Extractor.getCompanyAndUrl("temp.db")   # filter articles in word_and_url to get the ones with search word hits

        # data_Extractor.cleanDuplicates("temp.db")
        data_Extractor.download_all_article_pages("temp.db") # downloads articles from word_and_url to file
        data_Extractor.loop_all_articles("temp.db", "articles/")
        data_Extractor.create_markdown_overview("temp.db", "markdown")
        # data_Extractor.m_dbCleaner.delete_folder_contents("articles")
        # data_Extractor.m_dbCleaner.delete_folder_contents("htmlFiles")
        # data_Extractor.m_dbCleaner.set_last_time_run()

        sleep_time = 7200 # seconds
        time.sleep(sleep_time)

if __name__ == "__main__":
    main()
