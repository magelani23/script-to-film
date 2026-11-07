from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    raw_script = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    scenes = relationship("Scene", back_populates="project", cascade="all, delete-orphan")


class Scene(Base):
    __tablename__ = "scenes"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    scene_number = Column(Integer)
    location = Column(String)
    time_of_day = Column(String)

    project = relationship("Project", back_populates="scenes")
    shots = relationship("Shot", back_populates="scene", cascade="all, delete-orphan")


class Shot(Base):
    __tablename__ = "shots"

    id = Column(Integer, primary_key=True, index=True)
    scene_id = Column(Integer, ForeignKey("scenes.id"))
    shot_number = Column(Integer)
    camera_angle = Column(String)
    action_description = Column(Text)
    dialogue = Column(Text, nullable=True)
    image_prompt = Column(Text)
    video_prompt = Column(Text)
    generated_image_url = Column(String, nullable=True)
    generated_video_url = Column(String, nullable=True)

    scene = relationship("Scene", back_populates="shots")
