import json
from mutagen.easyid3 import EasyID3
from pathlib import Path
from mutagen.id3 import ID3, APIC
import configs.config as config

class Edit():
    def __init__(self, mp3Path, jsonPath):
        self.mp3Path = mp3Path
        with open(jsonPath, 'r') as f: self.data = json.load(f)
        Edit.add_art(self) # Adds an album art (image): self.data['imgPath']
        Edit.update_tags(self) # Updates the metadata depending on the json data: self.data
        
    def update_tags(self):
      audio = EasyID3(self.mp3Path)
      for key in self.data.keys():
        if key=="imgPath":
            pass;continue
        audio[key] = f"{self.data[key]}"
      audio.save(); del audio

    def add_art(self):
        imgPath = Path(self.data['imgPath'])
        audio = ID3(Path(self.mp3Path))
        with open(imgPath, "rb") as f: image_data = f.read()
        if imgPath.suffix == ".jpg": mime_type = "image/jpg"
        elif imgPath.suffix == ".png": mime_type = "image/png"
        audio.delall("APIC")
        audio.add(APIC(
            encoding=3,
            mime=mime_type,
            type=3,
            desc=imgPath.name,
            data=image_data,
        ))
        audio.save(); del audio

if __name__ == '__main__':
    Edit(config.mp3_path, config.json_data_path)
