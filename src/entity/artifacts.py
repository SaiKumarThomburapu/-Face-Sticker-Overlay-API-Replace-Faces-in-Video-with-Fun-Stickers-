from dataclasses import dataclass
from typing import Dict, List
      
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
    frame: any # any to avoid PIL import issue
    
    
    



