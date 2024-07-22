import os
from typing import List
from fastapi import APIRouter, File, HTTPException, Depends, UploadFile
from fastapi.responses import FileResponse, JSONResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.project import ProjectCreate
from app.repositories import project_repository
from app.config import settings
from app.models.asset import Asset


project_router = APIRouter()


@project_router.post("/", status_code=201)
def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    if not project.name.strip():
        raise HTTPException(status_code=400, detail="Project title is required")

    db_project = project_repository.create_project(db=db, project=project)
    return {
        "status": "success",
        "message": "Project created successfully",
        "data": db_project,
    }


@project_router.get("/")
def get_projects(db: Session = Depends(get_db)):
    projects = project_repository.get_projects(db=db)

    return {
        "status": "success",
        "message": "Projects successfully returned",
        "data": [
            {
                "id": project.id,
                "name": project.name,
                "description": project.description,
                "created_at": project.created_at.isoformat(),
                "updated_at": project.updated_at.isoformat(),
            }
            for project in projects
        ],
    }


@project_router.get("/{id}")
def get_project(id: int, db: Session = Depends(get_db)):
    project = project_repository.get_project(db=db, project_id=id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")

    return {
        "status": "success",
        "message": "Projects successfully returned",
        "data": {
            "id": project.id,
            "name": project.name,
            "description": project.description,
            "created_at": project.created_at.isoformat(),
            "updated_at": project.updated_at.isoformat(),
        },
    }


@project_router.get("/{id}/assets")
def get_assets(id: int, db: Session = Depends(get_db)):
    assets = project_repository.get_assets(db=db, project_id=id)
    return {
        "status": "success",
        "message": "Projects successfully returned",
        "data": [
            {
                "id": asset.id,
                "filename": asset.filename,
                "created_at": asset.created_at.isoformat(),
                "updated_at": asset.updated_at.isoformat(),
            }
            for asset in assets
        ],
    }


@project_router.post("/{id}/assets")
async def upload_files(
    id: int, files: List[UploadFile] = File(...), db: Session = Depends(get_db)
):
    try:
        project = project_repository.get_project(db=db, project_id=id)
        if project is None:
            raise HTTPException(status_code=400, detail="Project not found")

        # Ensure the upload directory exists
        os.makedirs(os.path.join(settings.upload_dir, str(id)), exist_ok=True)

        for file in files:
            # Check if the uploaded file is a PDF
            if file.content_type != "application/pdf":
                raise HTTPException(
                    status_code=400, detail=f"The file {file.filename} is not a PDF"
                )

            # Generate a secure filename
            filename = file.filename.replace(" ", "_")
            filepath = os.path.join(settings.upload_dir, str(id), filename)

            # Save the uploaded file
            with open(filepath, "wb") as buffer:
                buffer.write(await file.read())

            # Save the file info in the database
            new_asset = Asset(
                filename=filename,
                path=filepath,
                project_id=id,
            )

            db.add(new_asset)

        db.commit()

        return JSONResponse(content="Successfully uploaded the files")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Failed to upload files")


@project_router.get("/{id}/assets/{asset_id}")
async def get_file(asset_id: int, db: Session = Depends(get_db)):
    try:
        asset = project_repository.get_asset(db, asset_id)

        if asset is None:
            raise HTTPException(
                status_code=404, detail="File not found in the database"
            )

        filepath = asset.path

        # Check if the file exists
        if not os.path.isfile(filepath):
            raise HTTPException(status_code=404, detail="File not found on server")

        # Return the file
        return FileResponse(
            filepath, media_type="application/pdf", filename=asset.filename
        )

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Failed to retrieve file")


@project_router.get("/{id}/processes")
def get_processes(id: int, db: Session = Depends(get_db)):
    project = project_repository.get_project(db=db, project_id=id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")

    processes = project_repository.get_processes(db=db, project_id=id)
    return {
        "status": "success",
        "message": "Processes successfully returned",
        "data": [
            {
                "id": process.id,
                "type": process.type,
                "status": process.status,
                "project_id": f"{process.project_id}",
                "started_at": process.started_at.isoformat(),
                "completed_at": process.completed_at.isoformat(),
                "created_at": process.created_at.isoformat(),
                "updated_at": process.updated_at.isoformat(),
            }
            for process in processes
        ],
    }
