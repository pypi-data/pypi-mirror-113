class SendMessage():
    def __init__(chat_id, 
                text, 
                parse_mode = None,
                entities = None,
                disable_web_page_preview = None,
                disable_notification = None,
                reply_to_message_id = None,
                allow_sending_without_reply = None,
                reply_markup = None):
        self.text = text
        self.chat_id = chat_id
        self.parse_mode = parse_mode
        self.entities = entities
        self.disable_web_page_preview = disable_web_page_preview
        self.disable_notification = disable_notification
        self.reply_to_message_id = reply_to_message_id
        self.allow_sending_without_reply = allow_sending_without_reply
        self.reply_markup = reply_markup