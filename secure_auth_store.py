import os
import base64

from kivy.utils import platform
from kivy.app import App

ANDROID = platform == "android"

if ANDROID:
    from jnius import autoclass
    from kivy.storage.jsonstore import JsonStore

    # ----------------------------------
    # Tink AEAD primitive
    # ----------------------------------
    def get_aead_primitive():
        AeadConfig = autoclass('com.google.crypto.tink.aead.AeadConfig')
        AndroidKeysetManager = autoclass(
            'com.google.crypto.tink.integration.android.AndroidKeysetManager$Builder'
        )
        AesGcmKeyTemplates = autoclass(
            'com.google.crypto.tink.aead.AesGcmKeyTemplates'
        )

        AeadConfig.register()

        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        context = PythonActivity.mActivity

        keyset_handle = (
            AndroidKeysetManager()
            .withSharedPref(context, "tink_keyset", "tink_prefs")
            .withKeyTemplate(AesGcmKeyTemplates.AES256_GCM)
            .withMasterKeyUri(
                "android-keystore://firebase_token_master_key"
            )
            .build()
            .getKeysetHandle()
        )

        return keyset_handle.getPrimitive(
            autoclass('com.google.crypto.tink.Aead')
        )

    # ----------------------------------
    # Secure Save
    # ----------------------------------
    def secure_save(token: str):
        aead = get_aead_primitive()
        encrypted = aead.encrypt(token.encode("utf-8"), None)
        encoded = base64.b64encode(encrypted).decode("utf-8")

        base = App.get_running_app().user_data_dir
        path = os.path.join(base, "vault.json")
        store = JsonStore(path)

        store.put("credentials", token=encoded)

    # ----------------------------------
    # Secure Load
    # ----------------------------------
    def secure_load():
        base = App.get_running_app().user_data_dir
        path = os.path.join(base, "vault.json")
        store = JsonStore(path)

        if not store.exists("credentials"):
            return None

        encoded = store.get("credentials")["token"]
        encrypted = base64.b64decode(encoded)

        aead = get_aead_primitive()
        decrypted = aead.decrypt(encrypted, None)
        return decrypted.decode("utf-8")

else:
    # Desktop safe stubs (NO CRASH)
    def secure_save(token):
        pass

    def secure_load():
        return None
