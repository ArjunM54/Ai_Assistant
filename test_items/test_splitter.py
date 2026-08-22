from reader.pdf_reader import read_pdf
from test_items.text_splitter import split_text

text = read_pdf("uploads/computer_networks.pdf")

chunks = split_text(text)

print("Total Chunks:", len(chunks))

print()

for i, chunk in enumerate(chunks):

    print(f"\n------ Chunk {i+1} ------\n")

    print(chunks[i])

"""print(len(chunks))

print(chunks[0][:100])"""