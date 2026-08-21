from pathlib import Path


SENSITIVE_FILENAMES = {
    "passwords.txt",
    "password.txt",
    "credentials.json",
    "credential.json",
    "secrets.json",
    "secret.json",
    ".env",
    ".env.local",
    ".env.production",
    "tokens.json",
    "token.json",
    "id_rsa",
    "id_ed25519",
}


def is_sensitive_path(path):
    filename = Path(path).name.lower()

    return filename in SENSITIVE_FILENAMES