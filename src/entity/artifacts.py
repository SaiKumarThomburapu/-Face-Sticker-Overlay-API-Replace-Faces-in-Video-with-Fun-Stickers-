from dataclasses import dataclass
from typing import Dict, List
from PIL import Image
      
@dataclass
class AudioMergerArtifact:
    final_output_path:str
    
@dataclass
class ClustererArtifact:
    clustered:Dict

@dataclass
class FaceExtractorArtifact:
    all_faces:List
    
@dataclass
class StickerOverlayArtifact:
    frame:Image.Image
    
    
    



