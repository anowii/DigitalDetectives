import os
def send_iso(fileName): #vet ej om denna behövs eller kan köras direkt via TSK
    print("Test")
    return 0

def send_csv(fileName):  #vet ej om denna behövs eller kan köras direkt via OLLAMA
    print(fileName)
    return 0

def forward_message_llm(message): #Will forward message to the llm + append whatever is needed
    print(f"Message received: {message}")
    return 0


def is_valid_disk_image(disk_image):
    """
    Checks if a given disk image path is valid by verifying its file extension.
    Returns True if the file extension is valid, False otherwise.
    """
    valid_extensions =[".img",  ".iso", ".vdi", ".vmdk", ".vhd", ".dmg",
                       ".qcow2"] # Add more file types
    _,ext = os.path.splitext(disk_image)
    if ext.lower() not in valid_extensions:
        return False

    return True