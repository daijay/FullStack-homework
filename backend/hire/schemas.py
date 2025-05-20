from datetime import date, datetime
from typing import Optional

from django.core.exceptions import ValidationError
from django.db import models
from hire.models import jobs_post
from ninja import Field, Schema


class _AuthorInfo(Schema):
    id: int = Field(examples=[1])
    username: str = Field(examples=['Alice'])
    email: str = Field(examples=['alice@exapmple.com'])

class BaseJobSchema(Schema):
    title: str = Field(examples=['Software Engineer'])
    description: str = Field(examples=['Develop and maintain software.'])
    location: str = Field(examples=['Remote'])
    salary_range: str = Field(examples=['$60,000 - $80,000'])
    P_date: datetime = Field(examples=['2025-05-16T00:00:00Z'])
    E_date: datetime = Field(examples=['2025-06-16T00:00:00Z'])
    skills: list[str] = Field(examples=[['Python', 'Django']])

class CreateJobRequest(BaseJobSchema):
    company_name: str = Field( example="Tech Company")


class UpdateJobRequest(BaseJobSchema):
    pass  # 不允許更新 company_name


class JobResponse(BaseJobSchema):
    job_id: int
    company_name: str


class JobListResponse(BaseJobSchema):
    job_id: int
    title: str
    company_name: str
    P_date: datetime
    E_date: datetime
    @staticmethod
    def resolve_posting_date(obj: jobs_post) -> str:
        return obj.P_date.strftime('%Y-%m-%dT%H:%M:%SZ')

    @staticmethod
    def resolve_expiration_date(obj: jobs_post) -> str:
        return obj.E_date.strftime('%Y-%m-%dT%H:%M:%SZ')

class PostFilterSchema(Schema):
    search: Optional[str] = Field(None, description="Search by title, description, or company name")
    status: Optional[str] = Field(None, description="Filter by status: active, expired, scheduled")
    location: Optional[str] = Field(None, description="Filter by location")
    salary_range: Optional[str] = Field(None, description="Filter by salary range")
    company_name: Optional[str] = Field(None, description="Filter by company name")
    order_by: Optional[str] = Field(None, description="Order by: posting_date or expiration_date")

    def apply_filters(self, queryset):
        # 搜尋功能
        if self.search:
            queryset = queryset.filter(
                models.Q(title__icontains=self.search) |
                models.Q(description__icontains=self.search) |
                models.Q(company_name__icontains=self.search)
            )

        # 狀態篩選
        if self.status:
            status = self.status.lower()
            current_date = date.today()
            if status == "active":
                queryset = queryset.filter(P_date__lte=current_date, E_date__gte=current_date)
            elif status == "expired":
                queryset = queryset.filter(E_date__lt=current_date)
            elif status== "scheduled":
                queryset = queryset.filter(P_date__gt=current_date)

        # 其他字段篩選
        if self.location:
            queryset = queryset.filter(location__icontains=self.location)
        if self.salary_range:
            queryset = queryset.filter(salary_range__icontains=self.salary_range)
        if self.company_name:
            queryset = queryset.filter(company_name__icontains=self.company_name)

        # 排序
        if self.order_by:
            if self.order_by == "posting_date":
                queryset = queryset.order_by("P_date")  # 確保字段名稱與模型一致
            elif self.order_by == "expiration_date":
                queryset = queryset.order_by("E_date")  # 確保字段名稱與模型一致
            else:
                raise ValidationError(f"Invalid order_by value: {self.order_by}")

        return queryset