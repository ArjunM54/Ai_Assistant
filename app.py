from test_items.responses import get_response

print("===================================")
print("      Welcome to My AI Chatbot")
print("===================================")

while True:

    user = input("\nYou : ")

    if user.lower() == "bye":
        print("Bot : Goodbye! Have a nice day.")
        break

    response = get_response(user)

    print("Bot :", response)