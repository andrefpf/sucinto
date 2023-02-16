from collections import defaultdict 

MAX_SIZE = 150
AVG_SIZE = 100

class Messages:
    def __init__(self):
        self.chats = defaultdict(list)
    
    def register(self, chat_id, first_name, username, text):
        chat_list = self.chats[chat_id]

        if len(chat_list) > MAX_SIZE:
            # removes old messages from memory
            chat_list = chat_list[-AVG_SIZE:]
    
        chat_list.append((first_name, username, text))
        self.chats[chat_id] = chat_list
    
    def retrieve(self, chat_id):
        return '\n'.join(
            f"{author} ({user}): {message}" 
            for author, user, message 
            in self.chats[chat_id]
        )

    def normalize(self, author, user, message):
        return f"{author}({user}): {message}"