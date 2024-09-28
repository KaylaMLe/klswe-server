from math import floor
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from io import BytesIO
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextBox, LTTextLine, LTChar, Rect

def extract_bboxes(input_pdf_path: str) -> list[list[tuple[int, int, int]]]:
	positions = [
		[
			square_bbox(character.bbox)
			for element in page_layout
			if isinstance(element, (LTTextBox, LTTextLine)) # for each text line and group of text lines
			for text_line in element
			if isinstance(text_line, LTTextLine) # only necessary for LTTextBox
			for character in text_line
			if isinstance(character, LTChar) and character.get_text() == '◻'
		]
		for page_layout in extract_pages(input_pdf_path)
	]
	return positions

# outputs the bottom left corner and the side length of a square in the center of the bounding box
def square_bbox(bbox: Rect) -> tuple[int, int, int]:
	x0, y0, x1, y1 = bbox
	side = floor(x1 - x0) # round down because the bbox is larger than the square
	padding = (y1 - y0 - side) / 2 # vertical padding to center the square

	return (round(x0), round(y0 + padding), side)

def add_checkboxes_to_pdf(input_pdf_path, output_pdf_path):
	# extract positions of '◻' using pdfminer.six
	bboxes = extract_bboxes(input_pdf_path)
	
	# use PyPDF2 to read the original PDF
	pdf_reader = PdfReader(input_pdf_path)
	num_pages = len(pdf_reader.pages)
	
	# create a new PDF using ReportLab
	packet = BytesIO()
	can = canvas.Canvas(packet, pagesize=letter)

	for page_num in range(num_pages):
		# for each checkbox on this page
		for i in range(len(bboxes[page_num])):
			x, y, side = bboxes[page_num][i]
			name = f"checkbox_{page_num}_{i}"
			can.acroForm.checkbox(
				name=name,
				x=x,
				y=y,
				size=side,
				borderStyle="solid",
				borderWidth=3,
				fillColor=colors.white,
				fieldFlags="",
			)
		# save the current page and start a new one
		can.showPage()

	can.save()

	# merge the new checkboxes with the original PDF
	packet.seek(0)
	new_pdf = PdfReader(packet)
	output_pdf = PdfWriter()

	# rebuild the PDF by merging each page
	for page_num in range(num_pages):
		original_page = pdf_reader.pages[page_num]
		new_page = new_pdf.pages[page_num]
		
		original_page.merge_page(new_page)
		output_pdf.add_page(original_page)

	# Save the final PDF
	with open(output_pdf_path, "wb") as output_file:
		output_pdf.write(output_file)
