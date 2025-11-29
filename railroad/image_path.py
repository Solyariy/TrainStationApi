import os
import uuid
from pathlib import Path
from django.utils.text import slugify


def path_to_media(instance, filename: str):
    filepath = f"{slugify(str(instance))}-{uuid.uuid4()}"
    filepath += Path(filename).suffix
    return os.path.join(
        "uploads",
        instance.__class__.__name__.lower(),
        filepath
    )
