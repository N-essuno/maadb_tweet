class Token:
    content: str
    content_type: str
    TOKEN_CONTENTS = ["word", "emoji", "emoticon", "hashtag"]

    def __init__(self, content, content_type):
        if content_type not in self.TOKEN_CONTENTS:
            raise Exception("Content type {} not allowed".format(content_type))
        self.content_type = content_type
        self.content = content

    def __str__(self):
        return "<{}, {}>".format(self.content, self.content_type)

    def __eq__(self, other):
        if isinstance(other, Token):
            return self.content == other.content and self.content_type == other.content_type
        return False

    def __hash__(self):
        return hash((self.content, self.content_type))
