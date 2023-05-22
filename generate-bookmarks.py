import os
import logging
import glob
from pathlib import Path
import argparse
import pypdf
from jinja2 import Environment, FileSystemLoader

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def pdf_bookmarks_to_html(root_dir, output_dir, filename, verbose_logging):
    # Create an empty list to store the bookmark information
    raw_bookmarks = []

    # Loop through all PDF files in the directory and retrieve all bookmarks.
    # for filename in os.listdir(root_dir):
    for filename in glob.iglob(f"{root_dir}/**/*.pdf", recursive=True):
        if filename.endswith(".pdf"):
            logging.info(f"Reading PDF - {filename}")
            pdf_path = os.path.abspath(os.path.join(root_dir, filename))

            try:
                pdf_reader = pypdf.PdfReader(pdf_path, "rb")
                bookmark_info = pdf_reader.outline
            except Exception as e:
                logging.error(f"Error reading PDF - {filename} - error: {e}")
                continue
            raw_bookmarks.append((pdf_path, bookmark_info))

    final_bookmarks = {}
    # Loop through all bookmarks
    # Create a dictionary with the path, bookmark title, and page number
    for pdf_path, bookmarks in raw_bookmarks:
        for bookmark in bookmarks:
            try:
                page_number = pdf_reader.get_destination_page_number(bookmark) + 1
                if pdf_path not in final_bookmarks:
                    final_bookmarks[pdf_path] = []
                final_bookmarks[pdf_path].append((bookmark.title, page_number))
                if verbose_logging:
                    logging.info(f"Parsing bookmark {bookmark.title}")
            except Exception as e:
                logging.error(f"Error reading bookmark - error: {e}")
                continue

    # Render the HTML
    if len(final_bookmarks) > 0:
        env = Environment(loader=FileSystemLoader("."))
        template = env.get_template("bookmark_template.html")
        html = template.render(bookmarks=final_bookmarks)
        with open(f"{output_dir}/output.html", "w", encoding="utf-8") as html_file:
            html_file.write(html)

    else:
        logging.error(f"There were no PDFs found in the {root_dir} directory.")


def parse_arguments():
    # Create an ArgumentParser object
    parser = argparse.ArgumentParser(
        description="Extract bookmarks from PDF files and render an HTML file."
    )
    parser.add_argument(
        "--input-dir", help="The directory containing the input PDF files."
    )
    parser.add_argument(
        "--verbose", help="Enable verbose logging", action="store_true"
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
    output_path = args.output_dir

    if not os.path.exists(root_dir):
        raise RuntimeError(
            f"The directory {root_dir} does not exist. \
                Please create it and add PDF files to it."
        )

    # Create output directory
    Path(output_path).mkdir(parents=True, exist_ok=True)

    pdf_bookmarks_to_html(root_dir, output_path, output_filename, args.verbose)


if __name__ == "__main__":
    parse_arguments()
