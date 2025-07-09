from pydantic import BaseModel
from typing import List

class FaceReplaceRequest(BaseModel):
    selected_indices: List[int]
