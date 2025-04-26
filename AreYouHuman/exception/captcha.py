class MissingDirectoryError(Exception):
    """An exception that is raised when the emojis directory is missing."""
    def __init__(self, message="The \"emojis\" directory is missing."):
        super().__init__(message)
