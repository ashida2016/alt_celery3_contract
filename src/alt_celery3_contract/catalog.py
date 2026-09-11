"""任务目录模块。

``TASK_CATALOG`` 将任务注册名映射到对应的契约函数与入参 Schema，
是跨服务调用方的唯一检索入口。
"""

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from pydantic import BaseModel

from alt_celery3_contract import definitions, schemas
from alt_celery3_contract.constants import TaskName


@dataclass(frozen=True)
class TaskCatalogEntry:
    """单条任务目录条目。

    Attributes:
        name: 任务注册名字符串。
        contract: 同名的契约函数（仅签名声明）。
        payload_model: 入参 Pydantic 模型；单参数任务为 None。
        description: 任务接口描述（源自任务 Docstring）。
    """

    name: str
    contract: Callable[..., Any]
    payload_model: type[BaseModel] | None
    description: str


#: 全局任务目录：任务注册名 → 目录条目
TASK_CATALOG: dict[str, TaskCatalogEntry] = {
    TaskName.ADD.value: TaskCatalogEntry(
        name=TaskName.ADD.value,
        contract=definitions.add,
        payload_model=schemas.AddPayload,
        description="计算两数之和。",
    ),
    TaskName.PERIODIC_ADD.value: TaskCatalogEntry(
        name=TaskName.PERIODIC_ADD.value,
        contract=definitions.periodic_add,
        payload_model=schemas.AddPayload,
        description="周期性加法定时任务（由 celery beat 周期调度）。",
    ),
    TaskName.TRY_MYSQL.value: TaskCatalogEntry(
        name=TaskName.TRY_MYSQL.value,
        contract=definitions.try_mysql,
        payload_model=None,
        description="测试 MySQL 业务库（web_db）连通性。",
    ),
    TaskName.GET_ONE_STUDENT.value: TaskCatalogEntry(
        name=TaskName.GET_ONE_STUDENT.value,
        contract=definitions.get_one_student,
        payload_model=None,
        description="按主键查询单个学生信息。",
    ),
    TaskName.GENERATE_MANY_STUDENTS.value: TaskCatalogEntry(
        name=TaskName.GENERATE_MANY_STUDENTS.value,
        contract=definitions.generate_many_students,
        payload_model=schemas.GenerateManyStudentsPayload,
        description="批量生成随机学生信息并写入 web_db.students 表。",
    ),
    TaskName.GET_UN_GROUPS.value: TaskCatalogEntry(
        name=TaskName.GET_UN_GROUPS.value,
        contract=definitions.get_un_groups,
        payload_model=None,
        description="自动获取指定数量的高校信息（含专业组），查重后入库。",
    ),
    TaskName.INIT_WEB_DB.value: TaskCatalogEntry(
        name=TaskName.INIT_WEB_DB.value,
        contract=definitions.init_web_db,
        payload_model=None,
        description="初始化数据库：重建 web_db / log_db 及用户，并创建业务表。",
    ),
    TaskName.SIMU_NCEE.value: TaskCatalogEntry(
        name=TaskName.SIMU_NCEE.value,
        contract=definitions.simu_ncee,
        payload_model=schemas.SimuTaskPayload,
        description="模拟指定年份的高考，完成后学生状态 0→10（已高考未入学）。",
    ),
    TaskName.SIMU_ADMISSION.value: TaskCatalogEntry(
        name=TaskName.SIMU_ADMISSION.value,
        contract=definitions.simu_admission,
        payload_model=schemas.SimuTaskPayload,
        description="模拟指定年份的高校录取，完成后学生状态 10→20（在读）。",
    ),
    TaskName.SIMU_EXAM.value: TaskCatalogEntry(
        name=TaskName.SIMU_EXAM.value,
        contract=definitions.simu_exam,
        payload_model=schemas.SimuTaskPayload,
        description="模拟指定学年的高校日常考试（避开寒暑假月份）。",
    ),
    TaskName.SIMU_GRADUATE.value: TaskCatalogEntry(
        name=TaskName.SIMU_GRADUATE.value,
        contract=definitions.simu_graduate,
        payload_model=schemas.SimuTaskPayload,
        description="模拟指定年份的本科毕业，完成后学生状态 20→30（已毕业）。",
    ),
    TaskName.SIMU_SCHOOL_YEAR.value: TaskCatalogEntry(
        name=TaskName.SIMU_SCHOOL_YEAR.value,
        contract=definitions.simu_school_year,
        payload_model=schemas.SimuSchoolYearPayload,
        description="模拟学年例行操作：依次编排高考/录取/日常考试/毕业四个任务。",
    ),
}

__all__ = ["TASK_CATALOG", "TaskCatalogEntry"]
