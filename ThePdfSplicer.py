import os
import PyPDF2
from tkinter import filedialog, Tk


def select_pdf_file():
    """Opens a dialog to select a PDF file."""
    root = Tk()
    root.withdraw()  # Hide the root window
    file_selected = filedialog.askopenfilename(
        title="Select a PDF file", filetypes=[("PDF Files", "*.pdf")])
    return file_selected


def select_output_folder():
    """Opens a dialog to select an output folder."""
    root = Tk()
    root.withdraw()
    folder_selected = filedialog.askdirectory(
        title="Select a folder to save the split PDFs")
    return folder_selected


def split_pdf(pdf_path, output_folder, ranges):
    """
    Splits a PDF based on user-defined page ranges.

    :param pdf_path: Path to the input PDF file
    :param output_folder: Folder where the split PDFs will be saved
    :param ranges: List of tuples specifying (start_page, end_page) for each split
    """
    if not os.path.exists(pdf_path):
        print("❌ Error: PDF file not found.")
        return

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    with open(pdf_path, "rb") as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)

        for idx, (start, end) in enumerate(ranges, 1):
            writer = PyPDF2.PdfWriter()
            for page_num in range(start - 1, end):  # PyPDF2 uses zero-based indexing
                writer.add_page(reader.pages[page_num])

            output_pdf = os.path.join(output_folder, f"split_part_{idx}.pdf")
            with open(output_pdf, "wb") as output_file:
                writer.write(output_file)

            print(f"✅ Created: {output_pdf}")

    print("\n🎉 PDF splitting completed!")


# Select PDF and output folder
pdf_file = select_pdf_file()
output_folder = select_output_folder()

if pdf_file and output_folder:
    print("\n📄 Enter the page ranges to split (e.g., 1-3, 5-8): ")
    user_input = input("Ranges: ")

    try:
        page_ranges = [(int(start), int(end)) for start, end in (
            range_str.split("-") for range_str in user_input.split(","))]
        split_pdf(pdf_file, output_folder, page_ranges)
    except ValueError:
        print("❌ Invalid input format. Use: start-end (e.g., 1-3, 5-8)")
else:
    print("🚫 Operation cancelled.")
