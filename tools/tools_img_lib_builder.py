def delete_folders(my_path):
    import os
    import os.path
    for root, dirs, files in os.walk(my_path):
        for file in files:
            os.remove(os.path.join(root, file))

def save_to_archive(src, trg):
    # importing required packages
    import os
    import shutil
    from pathlib import Path

    # defining source and destination
    # paths
    files=os.listdir(src)
    
    # iterating over all the files in
    # the source directory
    for fname in files:        
        # copying the files to the
        # destination directory
        shutil.copy2(os.path.join(src,fname), trg)

def cleanup():
    trg = "/home/linux/Bureau/Operations/Media-Vault/img_library/"

    src ="/home/linux/Bureau/Programmation/image-miner-X/archives/images/.comments"
    delete_folders("/home/linux/Bureau/Programmation/image-miner-X/archives/media/.comments/")

    src ="/home/linux/Bureau/Programmation/image-miner-X/archives/design/"
    #delete_folders("/home/linux/Bureau/Programmation/image-miner-X/archives/media/.comments")
    save_to_archive(src, trg)

    src ="/home/linux/Bureau/Programmation/image-miner-X/archives/images/"
    #delete_folders("/home/linux/Bureau/Programmation/image-miner-X/archives/media/.comments")
    save_to_archive(src, trg)

    src ="/home/linux/Bureau/Programmation/image-miner-X/archives/junk/"
    #delete_folders("/home/linux/Bureau/Programmation/image-miner-X/archives/media/.comments")
    save_to_archive(src, trg)

    src ="/home/linux/Bureau/Programmation/image-miner-X/archives/media/"
    #delete_folders("/home/linux/Bureau/Programmation/image-miner-X/archives/media/.comments")
    save_to_archive(src, trg)
