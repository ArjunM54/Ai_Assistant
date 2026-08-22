from reader.pdf_reader import read_pdf

text = read_pdf("uploads/computer_networks.pdf")
print(len(text))
