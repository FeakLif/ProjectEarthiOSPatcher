import os
import shutil
import zipfile
import patcher

IP = "http://100.125.132.126:8080/"

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

    # 🔍 DEBUG CHECK
    size = os.path.getsize("data/ipa.zip")
    print(f"[DEBUG] ipa.zip size: {size} bytes")

    if size < 1000000:  # less than ~1MB = definitely wrong
        print("[ERROR] Downloaded file is too small, likely not a real IPA")
        return

    print("[INFO] Extracting IPA")

    try:
        with zipfile.ZipFile("data/ipa.zip", 'r') as zip_ref:
            zip_ref.extractall("data/ipa")
    except zipfile.BadZipFile:
        print("[ERROR] File is not a valid IPA (zip). Likely bad download.")
        return

    binary_path = "./data/ipa/Payload/minecraftearthtf.app/minecraftearthtf"

    if not os.path.exists(binary_path):
        print("[ERROR] App binary not found. Structure may differ.")
        return

    if not patcher.hex_bytes_in_file(
        "68747470733A2F2F6C6F6361746F722E6D6365736572762E6E6574",
        binary_path
    ):
        print("[ERROR] File appears encrypted or unsupported")
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
