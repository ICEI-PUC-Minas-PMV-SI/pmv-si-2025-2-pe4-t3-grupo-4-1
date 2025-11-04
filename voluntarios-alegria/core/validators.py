from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import UploadedFile

ALLOWED_EXTS = {"jpg", "jpeg", "png", "pdf"}
MAX_SIZE_MB = 5

def validate_attachment(file: UploadedFile) -> None:
    name = (file.name or "").lower()
    ext = name.rsplit(".", 1)[-1] if "." in name else ""
    if ext not in ALLOWED_EXTS:
        raise ValidationError(f"Invalid file type. Allowed: {', '.join(sorted(ALLOWED_EXTS))}")
    size_mb = file.size / (1024 * 1024)
    if size_mb > MAX_SIZE_MB:
        raise ValidationError(f"File too large. Max {MAX_SIZE_MB} MB")
