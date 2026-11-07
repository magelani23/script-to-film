from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ShotBase(BaseModel):
    shot_number: int
    camera_angle: str
    action_description: str
    dialogue: Optional[str] = None
    image_prompt: str
    video_prompt: str

class ShotCreate(ShotBase):
    pass

class ShotResponse(ShotBase):
    id: int
    generated_image_url: Optional[str] = None
    generated_video_url: Optional[str] = None

    class Config:
        from_attributes = True

class SceneBase(BaseModel):
    scene_number: int
    location: str
    time_of_day: str

class SceneCreate(SceneBase):
    shots: List[ShotCreate]

class SceneResponse(SceneBase):
    id: int
    shots: List[ShotResponse]

    class Config:
        from_attributes = True

class ProjectCreate(BaseModel):
    title: str
    raw_script: str

class ProjectResponse(BaseModel):
    id: int
    title: str
    raw_script: str
    created_at: datetime
    scenes: List[SceneResponse] = []

    class Config:
        from_attributes = True

