SEED_NUM = 10

CATEGORIES = {
    "Digital Illustrations",
    "Photographs & Videos",
    "Ebooks, Documents & Journals",
    "Music & Audio",
}

# for validator in Items validators
ACCEPTED_FILE_EXTENSIONS = [
    "jpg",
    "jpeg",
    "png",
    "mp4",
    "mov",
    "avi",
    "mp3",
    "wav",
    "ogg",
    "flac",
    "pdf",
    "doc",
    "docx",
    "txt",
]

ACCEPTED_FILE_MIME_TYPES = [
    "image/jpeg",
    "image/png",
    "video/mp4",
    "video/quicktime",
    "video/x-msvideo",
    "audio/mpeg",
    "audio/wav",
    "audio/ogg",
    "audio/flac",
    "application/pdf",
    "application/msword",
    "text/plain",
]

# for items form
HTML_ACCEPTED_FILE_EXTENSIONS = ", ".join([f".{x}" for x in ACCEPTED_FILE_EXTENSIONS])
