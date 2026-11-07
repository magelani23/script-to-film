import os
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

import models, schemas
from database import engine, get_db
from ai_engine import process_script_with_ai

# ბაზის ცხრილების შექმნა
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Script-to-Film AI Backend")

# CORS-ის ჩართვა Frontend-თან დასაკავშირებლად
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/projects", response_model=schemas.ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project_and_breakdown(project_in: schemas.ProjectCreate, db: Session = Depends(get_db)):
    """
    1. იღებს სცენარს.
    2. აგზავნის AI ძრავში სცენების დასაშლელად.
    3. ინახავს პროექტს, სცენებსა და კადრებს მონაცემთა ბაზაში.
    """
    # 1. პროექტის შექმნა
    db_project = models.Project(
        title=project_in.title,
        raw_script=project_in.raw_script
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)

    # 2. AI Breakout-ის გამოძახება
    try:
        parsed_scenes = process_script_with_ai(project_in.raw_script)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI processing failed: {str(e)}")

    # 3. ბაზაში შენახვა
    for scene_data in parsed_scenes:
        db_scene = models.Scene(
            project_id=db_project.id,
            scene_number=scene_data.scene_number,
            location=scene_data.location,
            time_of_day=scene_data.time_of_day
        )
        db.add(db_scene)
        db.commit()
        db.refresh(db_scene)

        for shot_data in scene_data.shots:
            db_shot = models.Shot(
                scene_id=db_scene.id,
                shot_number=shot_data.shot_number,
                camera_angle=shot_data.camera_angle,
                action_description=shot_data.action_description,
                dialogue=shot_data.dialogue,
                image_prompt=shot_data.image_prompt,
                video_prompt=shot_data.video_prompt
            )
            db.add(db_shot)
        
        db.commit()

    db.refresh(db_project)
    return db_project


@app.get("/api/projects/{project_id}", response_model=schemas.ProjectResponse)
def get_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@app.get("/api/projects", response_model=List[schemas.ProjectResponse])
def list_projects(db: Session = Depends(get_db)):
    return db.query(models.Project).all()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

