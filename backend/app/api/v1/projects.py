from typing import Optional, List
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.core.deps import get_current_user
from app.models import User, ProjectTemplate, UserProject, UserXPLog, DailyActivity
from app.schemas.project import (
    ProjectTemplateItem,
    UserProjectResponse,
    UserProjectCreateRequest,
    UserProjectUpdateRequest
)

router = APIRouter(prefix="/projects", tags=["Projects Planner"])

@router.get("/templates", response_model=List[ProjectTemplateItem])
def list_project_templates(
    role: Optional[str] = None,
    difficulty: Optional[str] = None,
    year: Optional[int] = None,
    db: Session = Depends(get_db)
):
    query = db.query(ProjectTemplate)
    if role:
        query = query.filter(ProjectTemplate.target_role == role)
    if difficulty:
        query = query.filter(ProjectTemplate.difficulty == difficulty)

    templates = query.all()
    if year:
        templates = [t for t in templates if (not t.year_suitability or year in t.year_suitability)]

    return templates


@router.get("/templates/{template_id}", response_model=ProjectTemplateItem)
def get_template_detail(template_id: int, db: Session = Depends(get_db)):
    t = db.query(ProjectTemplate).filter(ProjectTemplate.id == template_id).first()
    if not t:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project template not found.")
    return t


@router.get("/my", response_model=List[UserProjectResponse])
def get_my_projects(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    projects = db.query(UserProject).filter(UserProject.user_id == current_user.id).all()
    return projects


@router.post("/my", response_model=UserProjectResponse)
def create_my_project(
    req: UserProjectCreateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    project = UserProject(
        user_id=current_user.id,
        template_id=req.template_id,
        title=req.title,
        status="planned",
        github_url=req.github_url,
        notes=req.notes,
        progress_percent=0,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


@router.put("/my/{project_id}", response_model=UserProjectResponse)
def update_my_project(
    project_id: int,
    req: UserProjectUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    project = db.query(UserProject).filter(
        UserProject.id == project_id,
        UserProject.user_id == current_user.id
    ).first()

    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found or not owned by you.")

    if req.status is not None:
        project.status = req.status
        # If completed, award milestone XP
        if req.status in ["completed", "submitted"]:
            ref_id = f"project_{project.id}_completed"
            existing_xp = db.query(UserXPLog).filter(
                UserXPLog.user_id == current_user.id,
                UserXPLog.action_type == "project_complete",
                UserXPLog.reference_id == ref_id
            ).first()

            if not existing_xp:
                db.add(UserXPLog(
                    user_id=current_user.id,
                    action_type="project_complete",
                    reference_id=ref_id,
                    xp_amount=100,
                    created_at=datetime.utcnow()
                ))

    if req.github_url is not None:
        project.github_url = req.github_url
    if req.notes is not None:
        project.notes = req.notes
    if req.progress_percent is not None:
        project.progress_percent = req.progress_percent

    project.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(project)
    return project


@router.delete("/my/{project_id}")
def delete_my_project(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    project = db.query(UserProject).filter(
        UserProject.id == project_id,
        UserProject.user_id == current_user.id
    ).first()

    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found.")

    db.delete(project)
    db.commit()
    return {"success": True, "message": "Project removed."}
