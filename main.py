import time
from src.dataExtractor      import dataExtractor

def main():
    while True:

        data_Extractor = dataExtractor()

        # data_Extractor.download_web_pages()         # downloads news pages
        # data_Extractor.updateDatabase()             # get articles from news pages and store url to database searc_word
        # data_Extractor.getWordAndUrl()              # filter articles in word_and_url to get the ones with search word hits
        # data_Extractor.getCompanyAndUrl()           # filter articles in word_and_url to get the ones with search word hits

        data_Extractor.cleanDuplicates("temp.db")
        data_Extractor.download_all_article_pages("temp.db")
        data_Extractor.loop_all_articles("your_database.db", "articles/")
        data_Extractor.create_markdown_overview("your_database.db", "markdown")
        data_Extractor.m_dbCleaner.delete_folder_contents("articles")
        data_Extractor.m_dbCleaner.delete_folder_contents("htmlFiles")
        # data_Extractor.m_dbCleaner.set_last_time_run()

        sleep_time = 7200 # seconds
        time.sleep(sleep_time)

if __name__ == "__main__":
    main()
