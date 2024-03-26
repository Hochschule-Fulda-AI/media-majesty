SEED_NUM = 5

CATEGORIES = {
    "Digital Illustrations & Photographs",
    "Videos & Animations",
    "Music & Audio",
    "Documents & Journals & Books",
}

# for validator in Items validators
ACCEPTED_FILE_EXTENSIONS = [
    "jpg",
    "jpeg",
    "png",
    "mp4",
    "mkv",
    "webm",
    "mp3",
    "wav",
    "ogg",
    "flac",
    "opus",
    "pdf",
    "doc",
    "txt",
]

ACCEPTED_FILE_MIME_TYPES = [
    "image/jpeg",
    "image/png",
    "video/mp4",
    "video/x-matroska",
    "video/webm",
    "audio/webm",
    "audio/mpeg",
    "audio/wav",
    "audio/ogg",
    "audio/flac",
    "audio/opus",
    "application/pdf",
    "application/msword",
    "text/plain",
]

# for items form
HTML_ACCEPTED_FILE_EXTENSIONS = ", ".join([f".{x}" for x in ACCEPTED_FILE_EXTENSIONS])
