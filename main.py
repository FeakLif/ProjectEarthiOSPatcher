import os
import shutil
import zipfile
import patcher

# 🔥 hardcoded IP
IP = "172.29.148.159:8080"

def cleanup():
    if os.path.exists('data'):
        shutil.rmtree('data')

def main():
    print(f"[INFO] Using IP: {IP}")

    if not os.path.exists("ipa.ipa"):
        print("[ERROR] ipa.ipa not found")
        return

    os.makedirs("data", exist_ok=True)

    shutil.copyfile("ipa.ipa", "data/ipa.zip")

    print("[INFO] Extracting IPA")
    with zipfile.ZipFile("data/ipa.zip", 'r') as zip_ref:
        zip_ref.extractall("data/ipa")

    binary_path = "./data/ipa/Payload/minecraftearthtf.app/minecraftearthtf"

    if not patcher.hex_bytes_in_file(
        "68747470733A2F2F6C6F6361746F722E6D6365736572762E6E6574",
        binary_path
    ):
        print("[ERROR] File appears encrypted")
        cleanup()
        return

    print("[INFO] Patching...")

    patcher.patch_app_name()
    patcher.remove_drm()
    patcher.remove_useless_files()
    patcher.patch_ip(IP)
    patcher.patch_sunset_time()

    print("[INFO] Repacking IPA")
    patcher.zip_folder_contents("data/ipa/", "patched.ipa")

    print("[SUCCESS] patched.ipa ready")

    cleanup()

if __name__ == "__main__":
    main()
