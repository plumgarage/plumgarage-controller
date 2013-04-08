import os.path

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

settings = {
    "persist": {
        "module": "persist.file.FilePersist",
        "dir": os.path.join(PROJECT_ROOT, "/tmp"),
    }
}
