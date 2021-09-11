import base64


with open("food.jpg", "rb") as image2string:
	converted_string = base64.b64encode(image2string.read())
print(converted_string)

with open('encode.jpg', "wb") as file:
	file.write(base64.b64decode(converted_string))
