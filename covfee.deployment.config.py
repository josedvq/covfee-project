from project_env import (
    get_env_bool,
    get_env_int,
    get_env_optional,
    get_env_path,
    get_env_str,
)

HOST = get_env_str("COVFEE_HOST", "localhost")
PORT = get_env_int("COVFEE_PUBLIC_PORT", 5000)
COVFEE_SECRET_KEY = get_env_str("COVFEE_SECRET_KEY", "change-me")
ADMIN_USERNAME = get_env_str("COVFEE_ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = get_env_str("COVFEE_ADMIN_PASSWORD", "change-me")
MEDIA_SERVER = get_env_bool("COVFEE_MEDIA_SERVER", True)

media_url = get_env_optional("COVFEE_MEDIA_URL")
if media_url:
    MEDIA_URL = media_url

ssl_key_file = get_env_path("COVFEE_SSL_KEY_FILE")
ssl_cert_file = get_env_path("COVFEE_SSL_CERT_FILE")
if ssl_key_file and ssl_cert_file:
    SSL_KEY_FILE = ssl_key_file
    SSL_CERT_FILE = ssl_cert_file
