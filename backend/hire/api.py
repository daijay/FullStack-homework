from app.pagination import CustomPagination
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from hire.models import jobs_post
from hire.schemas import (CreateJobRequest, JobListResponse, JobResponse,
                          PostFilterSchema, UpdateJobRequest)
from ninja import Query, Router
from ninja.pagination import paginate
from ninja_jwt.authentication import JWTAuth

router = Router()


@router.post("/jobs", response={201: JobResponse}, auth=JWTAuth(), summary="Create a new job posting")
def create_job(request, payload: CreateJobRequest):
    job = jobs_post.objects.create(**payload.dict())
    return 201, job

@router.get("/jobs", response=list[JobListResponse], auth=JWTAuth(), summary="Retrieve a list of all job postings")
@paginate(CustomPagination)
def get_jobs(request, filters: PostFilterSchema = Query()):
    jobs = jobs_post.objects.all()
    jobs = filters.apply_filters(jobs)
    return jobs

@router.get("/jobs/{int:job_id}", response=JobResponse, auth=JWTAuth(), summary="Retrieve a single job posting by ID")
def get_job(request, job_id: int):
    job = get_object_or_404(jobs_post, job_id=job_id)
    return job

@router.put("/jobs/{int:job_id}", response=JobResponse, auth=JWTAuth(), summary="Update a job posting")
def update_job(request, job_id: int, payload: UpdateJobRequest):
    job = get_object_or_404(jobs_post, job_id=job_id)
    for attr, value in payload.dict().items():
        setattr(job, attr, value)
    job.save()
    return job

 
@router.delete(path='/jobs/{int:delete_id}/delete', auth=JWTAuth(), summary='Delete a job posting')
def delete_job(request: HttpRequest, delete_id: int) :
    jobs = get_object_or_404(jobs_post,job_id=delete_id)
    jobs.delete()
    return {"success": True}