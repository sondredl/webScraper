import time
from src.dbCleaner          import databaseCleaner
from src.databaseHandler    import DbHandler
from src.dataExtractor      import dataExtractor

# table_name = "WordAndUrl"
# column_name = "href"
# date_column = "timestamp"

# articlesTable_name = "Articles"
# title_column_name = "title"

def main():

    db_handler = DbHandler()
    data_Extractor = dataExtractor()
    db_cleaner = databaseCleaner()

    db_handler.set_last_time_run()

    while True:

        data_Extractor.createContentFiles()

        db_handler.create_database_and_tables()

        data_Extractor.updateDatabase()
        data_Extractor.updateDatabaseCompany()
        data_Extractor.getWordAndUrl()
        data_Extractor.getCompanyAndUrl()
        

        db_handler.cleanDuplicates("WordAndUrl", "href",  "timestamp")
        db_handler.cleanDuplicates("Articles",    "title", "timestamp")
        
        db_cleaner.reorganize_ids(db_handler.database_path, "WordAndUrl")
        db_handler.clean_last_update("WordAndUrl")

        data_Extractor.download_all_article_pages(db_handler)
        data_Extractor.loop_all_articles()

        db_cleaner.evaluateArticlesTable(db_handler.get_last_time_run())

        last_run_int = db_handler.get_last_time_run_int()
        date_time = db_handler.get_last_time_run()

        data_Extractor.create_markdown_overview("your_database.db", "markdown", date_time, last_run_int)

        db_cleaner.delete_folder_contents("articles")
        db_cleaner.delete_folder_contents("htmlFiles")
        db_handler.set_last_time_run()

        sleep_time = 7200 # seconds
        time.sleep(sleep_time)

if __name__ == "__main__":
    main()
