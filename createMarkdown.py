# import sqlite3

# def create_markdown_overview(db_path, output_file):
#     # Connect to the SQLite database
#     conn = sqlite3.connect(db_path)
#     cursor = conn.cursor()

#     # Query the articles table
#     cursor.execute("SELECT title, subtitle, text FROM articles")
#     articles = cursor.fetchall()

#     # Open the markdown file for writing
#     with open(output_file, 'w') as md_file:
#         # Write the header for the markdown file
#         md_file.write("# Articles Overview\n\n")

#         # Loop through the articles and write each one to the markdown file
#         for idx, article in enumerate(articles):
#             title, subtitle, text = article

#             # Write the article title and subtitle in markdown
#             md_file.write(f"## Article {idx + 1}: {title}\n")
#             if subtitle:
#                 md_file.write(f"### {subtitle}\n")
#             else:
#                 md_file.write("### No subtitle\n")
            
#             # Write the article text (truncated if necessary)
#             md_file.write(f"{text[:500]}...\n\n")  # Limit to first 500 characters
#             md_file.write("---\n\n")

#     # Close the database connection
#     conn.close()
#     print(f"Markdown overview saved to {output_file}")



import sqlite3
import os
from datetime import datetime

def create_markdown_overview(db_path, output_dir):
    # Get the current date in 'YYYY-MM-DD' format
    current_date = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    
    # Construct the markdown file path
    output_file = os.path.join(output_dir, f"articles_overview_{current_date}.md")
    
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Query the articles table
    cursor.execute("SELECT title, subtitle, text FROM articles")
    articles = cursor.fetchall()

    # Determine the file mode ('a' for append, 'w' for write if new file)
    file_mode = 'a' if os.path.exists(output_file) else 'w'
    
    # Open the markdown file in the appropriate mode
    with open(output_file, file_mode) as md_file:
        # If appending, check if we need to add a header for a new file
        if file_mode == 'w':
            md_file.write("# Articles Overview\n\n")

        # Loop through the articles and write each one to the markdown file
        for idx, article in enumerate(articles):
            title, subtitle, text = article
            if len(text) > 10:
                # Write the article title and subtitle in markdown
                md_file.write(f"## Article {idx + 1}: {title}\n")
                if subtitle:
                    md_file.write(f"### {subtitle}\n")
                else:
                    md_file.write("### No subtitle\n")
                
                # Write the article text (truncated if necessary)
                md_file.write(f"{text}...\n\n")  # Limit to first 500 characters
                md_file.write("---\n\n")

    # Close the database connection
    conn.close()
    print(f"Markdown overview saved to {output_file}")


# Usage example:
# create_markdown_overview("path/to/database.db", "output_directory_path")
