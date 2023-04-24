class RecordMissingIdException(Exception):
    msg = "record's id is missing. Can' update a records without it"


class RecordNotFoundException(Exception):
    msg = "record's not found"
