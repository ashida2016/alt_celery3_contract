"""任务注册名常量模块。"""

from enum import StrEnum


class TaskName(StrEnum):
    """alt_celery3 全部 Celery 任务的注册名枚举。

    枚举值为任务的全局注册名字符串，可直接用于
    ``app.send_task(name=...)`` 或 ``celery_app.send_task`` 跨服务调用。
    """

    ADD = "tasks.add"
    PERIODIC_ADD = "tasks.periodic_add"
    TRY_MYSQL = "tasks.try_mysql"
    GET_ONE_STUDENT = "tasks.get_one_student"
    GENERATE_MANY_STUDENTS = "tasks.generate_many_students"
    GET_UN_GROUPS = "tasks.get_un_groups"
    INIT_WEB_DB = "tasks.init_web_db"
    SIMU_NCEE = "tasks.simu_ncee"
    SIMU_ADMISSION = "tasks.simu_admission"
    SIMU_EXAM = "tasks.simu_exam"
    SIMU_GRADUATE = "tasks.simu_graduate"
