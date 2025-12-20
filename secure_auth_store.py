import os
import json

from kivy.utils import platform
from kivy.app import App

ANDROID = platform == "android"


# -----------------------------
# SAFE PATH (AFTER build())
# -----------------------------
def _auth_file_path():
    app = App.get_running_app()
    if not app:
        return None

    base = app.user_data_dir
    auth_dir = os.path.join(base, "auth")
    os.makedirs(auth_dir, exist_ok=True)
    return os.path.join(auth_dir, "auth.bin")


# ==========================================================
# ANDROID — Android Keystore (NO EXTRA LIBS)
# ==========================================================
if ANDROID:
    from jnius import autoclass

    KeyStore = autoclass("java.security.KeyStore")
    KeyGenerator = autoclass("javax.crypto.KeyGenerator")
    Cipher = autoclass("javax.crypto.Cipher")
    Base64 = autoclass("android.util.Base64")
    GCMParameterSpec = autoclass("javax.crypto.spec.GCMParameterSpec")
    KeyProperties = autoclass("android.security.keystore.KeyProperties")
    KeyGenParameterSpecBuilder = autoclass(
        "android.security.keystore.KeyGenParameterSpec$Builder"
    )

    KEY_ALIAS = "weather_tether_auth"
    ANDROID_KEYSTORE = "AndroidKeyStore"
    AES_MODE = "AES/GCM/NoPadding"

    def _get_or_create_key():
        ks = KeyStore.getInstance(ANDROID_KEYSTORE)
        ks.load(None)

        if ks.containsAlias(KEY_ALIAS):
            return ks.getKey(KEY_ALIAS, None)

        kg = KeyGenerator.getInstance(
            KeyProperties.KEY_ALGORITHM_AES, ANDROID_KEYSTORE
        )

        spec = (
            KeyGenParameterSpecBuilder(
                KEY_ALIAS,
                KeyProperties.PURPOSE_ENCRYPT | KeyProperties.PURPOSE_DECRYPT,
            )
            .setBlockModes([KeyProperties.BLOCK_MODE_GCM])
            .setEncryptionPaddings([KeyProperties.ENCRYPTION_PADDING_NONE])
            .setKeySize(256)
            .build()
        )

        kg.init(spec)
        kg.generateKey()
        return ks.getKey(KEY_ALIAS, None)

    def _encrypt(data: bytes) -> str:
        key = _get_or_create_key()
        cipher = Cipher.getInstance(AES_MODE)
        cipher.init(Cipher.ENCRYPT_MODE, key)
        encrypted = cipher.doFinal(data)
        iv = cipher.getIV()
        combined = iv + encrypted
        return Base64.encodeToString(combined, Base64.NO_WRAP)

    def _decrypt(data: str) -> bytes:
        raw = Base64.decode(data, Base64.NO_WRAP)
        iv, encrypted = raw[:12], raw[12:]
        key = _get_or_create_key()
        cipher = Cipher.getInstance(AES_MODE)
        spec = GCMParameterSpec(128, iv)
        cipher.init(Cipher.DECRYPT_MODE, key, spec)
        return cipher.doFinal(encrypted)


# ==========================================================
# DESKTOP — Keyring + Fernet
# ==========================================================
else:
    import keyring
    from cryptography.fernet import Fernet

    SERVICE = "weather_tether"
    KEY_NAME = "auth_key"

    def _get_key():
        key = keyring.get_password(SERVICE, KEY_NAME)
        if key:
            return key.encode()

        new_key = Fernet.generate_key()
        keyring.set_password(SERVICE, KEY_NAME, new_key.decode())
        return new_key

    def _encrypt(data: bytes) -> str:
        return Fernet(_get_key()).encrypt(data).decode()

    def _decrypt(data: str) -> bytes:
        return Fernet(_get_key()).decrypt(data.encode())


# ==========================================================
# PUBLIC API
# ==========================================================
def save_auth(email: str, refresh_token: str):
    path = _auth_file_path()
    if not path:
        return

    payload = {
        "email": email,
        "refresh_token": refresh_token,
    }

    encrypted = _encrypt(json.dumps(payload).encode())
    with open(path, "w") as f:
        f.write(encrypted)


def load_auth():
    path = _auth_file_path()
    if not path or not os.path.exists(path):
        return None

    try:
        with open(path, "r") as f:
            encrypted = f.read()
        raw = _decrypt(encrypted)
        return json.loads(raw.decode())
    except Exception:
        return None


def clear_auth():
    path = _auth_file_path()
    if path and os.path.exists(path):
        os.remove(path)

