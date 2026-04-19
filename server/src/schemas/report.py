from pydantic import BaseModel
from typing import List

class ModuleStat(BaseModel):
    module_name: str
    average_score: int
    completion_rate: int

class CourseReportResponse(BaseModel):
    overall_average: int
    total_students: int
    common_gaps: List[str]
    module_stats: List[ModuleStat]
