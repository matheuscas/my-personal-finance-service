class RecordMissingIdException(Exception):
    msg = "records's id is missing. Can' update a records without it"


class RecordNotFoundException(Exception):
    msg = "records's not found"
