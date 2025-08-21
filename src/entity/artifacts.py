from dataclasses import dataclass
from typing import Dict, List, Any
from PIL import Image
import numpy as np
      
@dataclass
class AudioMergerArtifact:
    final_output_path:str
    
@dataclass
class ClustererArtifact:
    clustered:Dict[int, List[Dict[str, Any]]]

@dataclass
class FaceExtractorArtifact:
    all_faces:List[Dict[str, Any]]
    
@dataclass
class StickerOverlayArtifact:
    frame:Image.Image
    
    
    



