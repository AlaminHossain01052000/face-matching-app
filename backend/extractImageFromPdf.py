from pikepdf import Pdf, Name, PdfImage
old_pdf=Pdf.open("uploads/nid.pdf")
page_1=old_pdf.pages[0]
# print(list(page_1.images.keys()))
raw_image1=page_1.images["/Im1"]
raw_image2=page_1.images["/Im2"]
raw_image3=page_1.images["/Im3"]
raw_image4=page_1.images["/Im4"]
raw_image5=page_1.images["/Im5"]
# pdf_image=PdfImage(raw_image4)
# pdf_image.extract_to(fileprefix="test2")
pdf_image=PdfImage(raw_image2)
pdf_image.extract_to(fileprefix="test5")