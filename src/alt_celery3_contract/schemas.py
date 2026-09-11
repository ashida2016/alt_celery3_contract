"""任务入参 Pydantic Schema 模块。

仅为多参数或逻辑较复杂的任务定义强类型入参模型；
单参数任务的入参直接使用契约函数签名中的基础类型。
"""

from pydantic import BaseModel, Field

_DATE_PATTERN = r"^\d{4}-\d{2}-\d{2}$"


class AddPayload(BaseModel):
    """加法任务入参（tasks.add / tasks.periodic_add 共用）。

    Attributes:
        x: 加数。
        y: 被加数。
    """

    x: int = Field(description="加数")
    y: int = Field(description="被加数")


class GenerateManyStudentsPayload(BaseModel):
    """批量生成学生任务入参（tasks.generate_many_students）。

    Attributes:
        numbers: 要生成的学生总人数。
        birthday_min: 出生年月日最小值（YYYY-MM-DD）。
        birthday_max: 出生年月日最大值（YYYY-MM-DD）。
        chunk_size: 单块人数上限。
        max_workers: 并发线程数。
    """

    numbers: int = Field(gt=0, description="要生成的学生总人数")
    birthday_min: str = Field(
        default="2000-01-01",
        pattern=_DATE_PATTERN,
        description="出生年月日最小值（YYYY-MM-DD）",
    )
    birthday_max: str = Field(
        default="2010-12-31",
        pattern=_DATE_PATTERN,
        description="出生年月日最大值（YYYY-MM-DD）",
    )
    chunk_size: int = Field(
        default=50_000, gt=0, description="单块人数上限"
    )
    max_workers: int = Field(
        default=8, ge=1, le=32, description="并发线程数"
    )


class SimuTaskPayload(BaseModel):
    """业务模拟任务入参（tasks.simu_* 四个任务共用）。

    Attributes:
        year: 业务年份（高考年份 / 学年起始年 / 毕业年份）。
        chunk_size: ID 窗口大小。
        max_workers: 并发线程数。
    """

    year: int = Field(description="业务年份")
    chunk_size: int = Field(
        default=50_000, gt=0, description="ID 窗口大小"
    )
    max_workers: int = Field(
        default=8, ge=1, le=32, description="并发线程数"
    )


class SimuSchoolYearPayload(BaseModel):
    """学年例行操作编排任务入参（tasks.simu_school_year）。

    Attributes:
        year: 学年起始年份（编排 ncee/admission/exam 用 year，
            graduate 用 year+3）。
        stage_timeout: 单个阶段等待结果的最长秒数。
        chunk_size: ID 窗口大小。
        max_workers: 并发线程数。
    """

    year: int = Field(description="学年起始年份")
    stage_timeout: float = Field(
        default=600.0, gt=0, description="单个阶段等待结果的最长秒数"
    )
    chunk_size: int = Field(
        default=50_000, gt=0, description="ID 窗口大小"
    )
    max_workers: int = Field(
        default=8, ge=1, le=32, description="并发线程数"
    )
