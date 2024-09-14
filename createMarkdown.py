import sqlite3
import os
from datetime import datetime
import textwrap

def create_markdown_overview(db_path, output_dir, date_time, last_run_int):
    # Get the current date in 'YYYY-MM-DD' format
    # last_date_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    
    # Construct the markdown file path
    output_file = os.path.join(output_dir, f"articles_overview_{date_time}.md")
    
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Query the articles table
    cursor.execute("""SELECT timestamp, title, subtitle, text, timestamp_int 
                   FROM articles
                   WHERE timestamp_int > ? """, (last_run_int,))
    articles = cursor.fetchall()
    print(f"last_date_time {last_run_int}")
    # print(f"last_time_run {last_date_time}")
    print(f"number of articles to be used {len(articles)}")

    # Determine the file mode ('a' for append, 'w' for write if new file)
    file_mode = 'a' if os.path.exists(output_file) else 'w'
    
    # Open the markdown file in the appropriate mode
    with open(output_file, file_mode) as md_file:
        # If appending, check if we need to add a header for a new file
        if file_mode == 'w':
            md_file.write("# Articles Overview\n\n")

        # Loop through the articles and write each one to the markdown file
        for index, article in enumerate(articles):
            timestamp, title, subtitle, text, timestamp_int = article
            # if len(text) > 10 :
            if len(text) > 10 and timestamp_int > last_run_int:
                # Write the article title and subtitle in markdown
                md_file.write(f"## Article {index + 1}: {title}\n")
                if subtitle:
                    md_file.write(f"### {subtitle}\n")
                else:
                    md_file.write("### No subtitle\n")
                
                # Write the article text (truncated if necessary)
                md_file.write(f"{text}...\n\n")  # Limit to first 500 characters
                md_file.write("---\n\n")
            else:
                print("no new articles, will not make new file")

    # Close the database connection
    conn.close()
    print(f"Markdown overview saved to {output_file}")
    format_markdown_file(output_file)

def format_markdown_file(file_path, max_width=120):
    # Open the input markdown file and read its content
    with open(file_path, 'r') as md_file:
        content = md_file.read()

    # Split the content into lines for more granular control
    lines = content.splitlines()

    formatted_lines = []
    for line in lines:
        # Add a newline before `###` headers and list items that don't start with a `#`
        if line.__contains__('###') :
            # Ensure the previous line isn't a header or list
            if len(formatted_lines) > 0 and not formatted_lines[-1].startswith('#'):
                formatted_lines.append('\n')  # Add a blank line

        # Add the line itself to the formatted list
        formatted_lines.append(line)

    # Join the lines back into paragraphs for wrapping
    content = '\n'.join(formatted_lines)

    # Split the content into paragraphs by double newlines
    paragraphs = content.split('\n\n')

    # Wrap each paragraph to the specified width
    formatted_paragraphs = []
    for paragraph in paragraphs:
        # Handle code blocks and lists (you may want to skip wrapping these)
        if paragraph.startswith("```") or paragraph.startswith("- ") or paragraph.startswith("* "):
            formatted_paragraphs.append(paragraph)
        else:
            # Wrap lines to the max_width
            wrapped = textwrap.fill(paragraph, width=max_width)
            formatted_paragraphs.append(wrapped)

    # Join the formatted paragraphs back with double newlines
    formatted_content = '\n\n'.join(formatted_paragraphs)

    # Write the formatted content back to the same file or a new file
    with open(file_path, 'w') as md_file:
        md_file.write(formatted_content)

    print(f"File '{file_path}' has been formatted with a max width of {max_width} characters.")

# Example usage
# format_markdown_file('myFile.md', max_width=120)

