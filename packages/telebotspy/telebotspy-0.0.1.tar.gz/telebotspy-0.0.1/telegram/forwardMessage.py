class ForwardMessage():
    def __init__(self,
                chat_id,
                from_chat_id,
                message_id,
                disable_notification = None):
        self.chat_id = chat_id
        self.from_chat_id = from_chat_id
        self.message_id = message_id
        self.disable_notification = disable_notification