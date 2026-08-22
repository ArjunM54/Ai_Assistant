import easyocr

reader = easyocr.Reader(['en'])

result = reader.readtext("uploads/Screenshot(27).png")

text = ""

for item in result:

    text += item[1]

    text += "\n"
    
print(text)