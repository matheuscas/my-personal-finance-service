class ExistingTagException(Exception):
    msg = "Tag already exists"


class MissingTagException(Exception):
    msg = "Tag does not exist"
