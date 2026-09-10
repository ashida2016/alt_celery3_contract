"""任务契约函数模块。

每个契约函数与 alt_celery3 中的 Celery 任务同名、同签名
（bind=True 任务已剥离首个注入参数），仅保留声明性质的定义，
函数体统一抛出 ``NotImplementedError``。

契约函数不包含任何业务实现逻辑，仅作为跨服务调用的类型化接口：
调用方通过 ``TASK_CATALOG`` / ``TaskName`` 定位任务名，
通过 ``schemas`` 校验入参后，使用 ``send_task`` 投递到消息队列。
"""

from typing import Any


def add(x: int, y: int) -> int:
    """计算两数之和。

    Args:
        x: 加数。
        y: 被加数。

    Returns:
        两数之和。

    Raises:
        NotImplementedError: 契约函数不包含实现。
    """
    raise NotImplementedError


def periodic_add(x: int, y: int) -> int:
    """周期性加法定时任务（由 celery beat 周期调度）。

    Args:
        x: 加数。
        y: 被加数。

    Returns:
        两数之和。

    Raises:
        NotImplementedError: 契约函数不包含实现。
    """
    raise NotImplementedError


def try_mysql() -> dict:
    """测试 MySQL 业务库（web_db）连通性。

    Returns:
        连通性测试结果字典。

    Raises:
        NotImplementedError: 契约函数不包含实现。
    """
    raise NotImplementedError


def get_one_student(student_id: int) -> dict:
    """按主键查询单个学生信息。

    Args:
        student_id: 学生记录主键 id（students 表）。

    Returns:
        查询结果字典。

    Raises:
        NotImplementedError: 契约函数不包含实现。
    """
    raise NotImplementedError


def generate_many_students(
    numbers: int,
    birthday_min: str = "2000-01-01",
    birthday_max: str = "2010-12-31",
    chunk_size: int = 50_000,
    max_workers: int = 8,
) -> dict:
    """批量生成随机学生信息并写入 web_db.students 表。

    Args:
        numbers: 要生成的学生总人数。
        birthday_min: 出生年月日最小值（YYYY-MM-DD）。
        birthday_max: 出生年月日最大值（YYYY-MM-DD）。
        chunk_size: 单块人数上限（默认 50000）。
        max_workers: 并发线程数（默认 8）。

    Returns:
        执行摘要（inserted、elapsed_seconds 等）。

    Raises:
        NotImplementedError: 契约函数不包含实现。
    """
    raise NotImplementedError


def get_un_groups(count: int = 5) -> list[dict[str, Any]]:
    """自动获取指定数量的高校信息（含专业组），查重后入库。

    Args:
        count: 要获取的高校数量（默认 5）。

    Returns:
        标准的 JSON 对象（高校信息数组）。

    Raises:
        NotImplementedError: 契约函数不包含实现。
    """
    raise NotImplementedError


def init_web_db(confirm: bool = False) -> dict:
    """初始化数据库：重建 web_db / log_db 及用户，并创建业务表。

    危险操作：会删除旧的 web_db / log_db 与用户，
    必须显式传入 ``confirm=True`` 才会执行。

    Args:
        confirm: 危险操作确认开关，必须为 True。

    Returns:
        执行摘要（重建的库、表列表等）。

    Raises:
        NotImplementedError: 契约函数不包含实现。
    """
    raise NotImplementedError


def simu_ncee(
    year: int, chunk_size: int = 50_000, max_workers: int = 8
) -> dict:
    """模拟指定年份的高考，完成后学生状态 0→10（已高考未入学）。

    Args:
        year: 高考年份。
        chunk_size: ID 窗口大小（默认 50000）。
        max_workers: 并发线程数（默认 8）。

    Returns:
        执行摘要（simulated：登记成绩人数）。

    Raises:
        NotImplementedError: 契约函数不包含实现。
    """
    raise NotImplementedError


def simu_admission(
    year: int, chunk_size: int = 50_000, max_workers: int = 8
) -> dict:
    """模拟指定年份的高校录取，完成后学生状态 10→20（在读）。

    Args:
        year: 高考年份。
        chunk_size: ID 窗口大小（默认 50000）。
        max_workers: 并发线程数（默认 8）。

    Returns:
        执行摘要（admitted、band_stats 等）。

    Raises:
        NotImplementedError: 契约函数不包含实现。
    """
    raise NotImplementedError


def simu_exam(year: int, chunk_size: int = 50_000, max_workers: int = 8) -> dict:
    """模拟指定学年的高校日常考试（避开寒暑假月份）。

    Args:
        year: 学年起始年份。
        chunk_size: ID 窗口大小（默认 50000）。
        max_workers: 并发线程数（默认 8）。

    Returns:
        执行摘要（recorded：登记成绩行数）。

    Raises:
        NotImplementedError: 契约函数不包含实现。
    """
    raise NotImplementedError


def simu_graduate(
    year: int, chunk_size: int = 50_000, max_workers: int = 8
) -> dict:
    """模拟指定年份的本科毕业，完成后学生状态 20→30（已毕业）。

    Args:
        year: 毕业年份。
        chunk_size: ID 窗口大小（默认 50000）。
        max_workers: 并发线程数（默认 8）。

    Returns:
        执行摘要（graduated、no_score 等）。

    Raises:
        NotImplementedError: 契约函数不包含实现。
    """
    raise NotImplementedError
