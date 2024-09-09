import sqlite3

def create_markdown_overview(db_path, output_file):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Query the articles table
    cursor.execute("SELECT title, subtitle, text FROM articles")
    articles = cursor.fetchall()

    # Open the markdown file for writing
    with open(output_file, 'w') as md_file:
        # Write the header for the markdown file
        md_file.write("# Articles Overview\n\n")

        # Loop through the articles and write each one to the markdown file
        for idx, article in enumerate(articles):
            title, subtitle, text = article

            # Write the article title and subtitle in markdown
            md_file.write(f"## Article {idx + 1}: {title}\n")
            if subtitle:
                md_file.write(f"### {subtitle}\n")
            else:
                md_file.write("### No subtitle\n")
            
            # Write the article text (truncated if necessary)
            md_file.write(f"{text[:500]}...\n\n")  # Limit to first 500 characters
            md_file.write("---\n\n")

    # Close the database connection
    conn.close()
    print(f"Markdown overview saved to {output_file}")


