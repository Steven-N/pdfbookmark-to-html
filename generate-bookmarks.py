import os
import logging
from pathlib import Path
import argparse
import PyPDF2
from jinja2 import Environment, FileSystemLoader


def pdf_bookmarks_to_html(root_dir, output_path, output_filename):
    # Create an empty list to store the bookmark information
    raw_bookmarks = []

    # Loop through all PDF files in the directory and retrieve all bookmarks.
    for filename in os.listdir(root_dir):
        if filename.endswith(".pdf"):
            pdf_path = os.path.abspath(os.path.join(root_dir, filename))

            pdf_reader = PyPDF2.PdfReader(pdf_path, "rb")
            bookmark_info = pdf_reader.outline

            raw_bookmarks.append((pdf_path, bookmark_info))

    final_bookmarks = {}
    # Loop through all bookmarks
    # Create a dictionary with the path, bookmark title, and page number
    for pdf_path, bookmarks in raw_bookmarks:
        for bookmark in bookmarks:
            page_number = pdf_reader.get_destination_page_number(bookmark) + 1
            if pdf_path not in final_bookmarks:
                final_bookmarks[pdf_path] = []
            final_bookmarks[pdf_path].append((bookmark.title, page_number))

    # Render the HTML
    if len(final_bookmarks) > 0:
        env = Environment(loader=FileSystemLoader("."))
        template = env.get_template("bookmark_template.html")
        html = template.render(bookmarks=final_bookmarks)
        with open(f"{output_path}/{output_filename}", "w") as html_file:
            html_file.write(html)

    else:
        logging.info(f"There were no PDFs found in the {root_dir} directory.")
        os.rmdir(output_path)


def parse_arguments():
    # Create an ArgumentParser object
    parser = argparse.ArgumentParser(
        description="Extract bookmarks from PDF files and render an HTML file."
    )
    parser.add_argument(
        "--input-dir", help="The directory containing the input PDF files."
    )
    parser.add_argument("--output-dir", help="The output path.")
    parser.add_argument(
        "--output-filename",
        help="The output filename.",
        default="bookmarks.html",
        required=False,
    )

    # Parse the command line arguments
    args = parser.parse_args()

    # Define the directory where the PDF files are stored
    relative_input_pdf_dir = args.input_dir
    relative_output_pdf_dir = args.output_dir
    output_filename = args.output_filename

    # Get the absolute path of the input and output directories
    root_dir = os.path.abspath(relative_input_pdf_dir)
    output_path = os.path.abspath(relative_output_pdf_dir)

    if not os.path.exists(root_dir):
        raise RuntimeError(
            f"The directory {root_dir} does not exist. \
                Please create it and add PDF files to it."
        )

    # Create output directory
    Path(output_path).mkdir(parents=True, exist_ok=True)

    pdf_bookmarks_to_html(root_dir, output_path, output_filename)


if __name__ == "__main__":
    parse_arguments()
