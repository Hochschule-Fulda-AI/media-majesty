CATEGORIES = {
    "Digital Illustrations",
    "Photographs & Videos",
    "Ebooks, Documents & Journals",
    "Music & Audio",
}

# for validator in Items validators
ACCEPTED_FILE_EXTENSIONS = [
    "jpg", "jpeg", "png",
    "mp4", "mov", "avi",
    "mp3", "wav", "ogg", "flac",
    "pdf", "doc", "docx", "txt",
]

# for items form 
HTML_ACCEPTED_FILE_EXTENSIONS = ", ".join(list(map(lambda x: f".{x}", ACCEPTED_FILE_EXTENSIONS)))
