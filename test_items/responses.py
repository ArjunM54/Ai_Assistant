def get_response(user):

    user = user.lower()

    if "hi" in user or "hello" in user or "hey" in user:
        return "Hello Sir! How can I help you?"

    elif "name" in user:
        return "My name is Gima."

    elif "who made you" in user or "creator" in user:
        return "I was created by Arjun."

    elif "good morning" in user:
        return "Good Morning ,how can I help you buddy.!"
    
    elif "good afternoon" in user:
        return "Good afternoon ,how can I help you today.!"
    
    elif "good night" in user:
        return "Haa good night,have a sweet dreams💕!"

    elif "thank" in user or "thx" in user:
        return "You're Welcome!"

    elif "how are you" in user:
        return "I'm doing great!"
    
    elif "who are you" in user:
        return "I'm a Ai chatbot."

    elif "python" in user:
        return "Python is a powerful programming language."

    elif "ai" in user:
        return "AI means Artificial Intelligence."
    
    elif "college" in user:
        return "I don't know your college yet."

    elif "java" in user:
        return "Java is an object-oriented programming language."
    
    elif "can you predict" in user:
        return "I can't predict that."
    
    elif "what is your work" in user:
        return "My work is to answer your questions."

    elif "weather" in user:
        return "I cannot check live weather yet."

    elif "time" in user:
        return "I cannot tell the current time yet."
    
    elif "how to make you" in user or "i want to make a chatbot":
        return "That is a huge process, I can't answer."

    elif "joke" in user:
        return "Why do programmers prefer dark mode? Because light attracts bugs!"
    
    elif "java" in user:
        return "Java is an object-oriented language."

    elif "python" in user:
        return "Python is easy to learn."

    elif "machine learning" in user:
        return "Machine Learning is a branch of AI."

    elif "bye" in user:
        return "Goodbye!"

    else:
        return "Sorry, I don't understand."
    