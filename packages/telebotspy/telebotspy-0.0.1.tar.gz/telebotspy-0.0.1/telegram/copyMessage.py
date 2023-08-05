class CopyMessage():
    def __init__(self,
                chat_id,
                from_chat_id,
                message_id,
                caption = None,
                parse_mode = None,
                caption_entities = None,
                disable_notification = None,
                reply_to_message_id = None,
                allow_sending_without_reply = None,
                reply_markup = None):
        
        self.chat_id = chat_id
        self.from_chat_id = from_chat_id
        self.message_id = message_id
        self.caption = caption
        self.parse_mode = parse_mode
        self.caption_entities = caption_entities
        self.disable_notification = disable_notification
        self.reply_to_message_id = reply_to_message_id
        self.allow_sending_without_reply = allow_sending_without_reply
        self.reply_markup = reply_markup