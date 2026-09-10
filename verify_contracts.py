#!/usr/bin/env python
"""契约兼容性验证脚本。

静态比对 ``alt_celery3_contract`` 中的契约声明与 ``alt_celery3``
源项目的真实 Celery 任务签名，验证二者的兼容性：

1. 任务注册名对齐：契约目录中的每个任务名都必须存在于源项目
   的 Celery 注册表中，反之亦然。
2. 参数签名对齐：契约函数的业务参数（源任务 bind=True 时剥离
   首个注入参数）与源任务的参数名称、顺序、默认值完全一致。
3. Schema 对齐：配置了 Pydantic 模型的任务，其模型字段名集合
   必须与源任务业务参数名集合一致。

用法::

    python verify_contracts.py              # 完整比对（需导入源项目）
    python verify_contracts.py --no-source  # 跳过源项目比对，仅自检

退出码：0=全部通过，1=存在不兼容项。
"""

import argparse
import inspect
import os
import sys
import tempfile
from pathlib import Path
from typing import Any, get_origin

# 将源项目加入 sys.path，以便导入其 Celery 应用
SOURCE_ROOT = Path(__file__).resolve().parent.parent / "alt_celery3"

# src 布局：未安装本包时也可直接运行本脚本
SRC_ROOT = Path(__file__).resolve().parent / "src"
for _path in (str(SRC_ROOT), str(SOURCE_ROOT)):
    if _path not in sys.path:
        sys.path.insert(0, _path)


def _annotation_name(annotation: Any) -> str:
    """把类型注解归一化为可比较的名称字符串。

    Args:
        annotation: 类型注解对象（可能是类型、字符串或 typing 结构）。

    Returns:
        归一化后的名称字符串。
    """
    if annotation is inspect.Parameter.empty:
        return ""
    if isinstance(annotation, str):
        return annotation
    origin = get_origin(annotation)
    if origin is not None:
        args = ", ".join(_annotation_name(a) for a in annotation.__args__)
        return f"{origin.__name__}[{args}]"
    return getattr(annotation, "__name__", str(annotation))


def _annotation_compatible(src: Any, contract: Any) -> bool:
    """判断源任务与契约的类型注解是否兼容。

    采用名称级别的宽松比对（跨包引用的类型以名称为准）。

    Args:
        src: 源任务参数注解。
        contract: 契约函数参数注解。

    Returns:
        兼容返回 True。
    """
    return _annotation_name(src) == _annotation_name(contract)


def check_catalog_integrity() -> list[str]:
    """自检契约包内部一致性。

    Returns:
        不一致项列表（空列表表示通过）。
    """
    from alt_celery3_contract import TASK_CATALOG, TaskName

    issues: list[str] = []
    enum_values = {t.value for t in TaskName}
    if enum_values != set(TASK_CATALOG):
        diff = enum_values ^ set(TASK_CATALOG)
        issues.append(f"TaskName 枚举与 TASK_CATALOG 键不一致: {diff}")
    for name, entry in TASK_CATALOG.items():
        if not entry.description:
            issues.append(f"{name}: 缺少 description")
        try:
            inspect.signature(entry.contract)
        except (TypeError, ValueError) as exc:
            issues.append(f"{name}: 契约函数签名不可解析: {exc}")
        func_name = entry.contract.__name__
        expected = name.rsplit(".", 1)[-1]
        if func_name != expected:
            issues.append(f"{name}: 契约函数名 {func_name} != {expected}")
    return issues


def check_source_compatibility() -> list[str]:
    """比对契约与源项目真实任务签名。

    Returns:
        不兼容项列表（空列表表示通过）。
    """
    if str(SOURCE_ROOT) not in sys.path:
        sys.path.insert(0, str(SOURCE_ROOT))
    # 源项目导入时会初始化 sclog 文件日志，将输出重定向到系统临时
    # 目录，避免在当前工作目录产生 logs/ 污染
    os.environ.setdefault("LOG_DIR", tempfile.gettempdir())
    from app import app

    from alt_celery3_contract import TASK_CATALOG

    # 未启动 worker 时 include/autodiscover 的任务模块不会自动导入，
    # 需显式触发加载后注册表才是完整的
    app.loader.import_default_modules()

    issues: list[str] = []
    registry_names = {
        n for n in app.tasks if not n.startswith("celery.")
    }
    catalog_names = set(TASK_CATALOG)
    if catalog_names - registry_names:
        issues.append(
            f"契约中的任务在源项目不存在: {catalog_names - registry_names}"
        )
    if registry_names - catalog_names:
        issues.append(
            f"源项目中存在未纳入契约的任务: {registry_names - catalog_names}"
        )

    for name, entry in TASK_CATALOG.items():
        celery_task = app.tasks.get(name)
        if celery_task is None:
            continue
        src_params = list(
            inspect.signature(celery_task.run).parameters.values()
        )
        # bind=True 的任务 run 首参数为注入的 self/task，予以剥离；
        # 注意不能使用 celery_task.bind 判断（它是 Task 绑定 app 的方法，恒为真值）
        if src_params and src_params[0].name in ("self", "task"):
            src_params = src_params[1:]
        contract_params = list(
            inspect.signature(entry.contract).parameters.values()
        )

        # 参数名 / 默认值 / 类型注解逐一对齐
        src_names = [p.name for p in src_params]
        contract_names = [p.name for p in contract_params]
        if src_names != contract_names:
            issues.append(
                f"{name}: 参数名不一致 src={src_names} contract={contract_names}"
            )
            continue
        for src, contract in zip(src_params, contract_params, strict=True):
            if src.default is not inspect.Parameter.empty:
                if src.default != contract.default:
                    issues.append(
                        f"{name}.{src.name}: 默认值不一致 "
                        f"src={src.default!r} contract={contract.default!r}"
                    )
            elif contract.default is not inspect.Parameter.empty:
                issues.append(
                    f"{name}.{src.name}: 源任务无默认值但契约有默认值"
                )
            if not _annotation_compatible(src.annotation, contract.annotation):
                issues.append(
                    f"{name}.{src.name}: 类型注解不一致 "
                    f"src={src.annotation!r} contract={contract.annotation!r}"
                )

        # Schema 字段名集合与业务参数名集合对齐
        if entry.payload_model is not None:
            schema_fields = set(entry.payload_model.model_fields)
            if schema_fields != set(src_names):
                issues.append(
                    f"{name}: Schema 字段与参数不一致 "
                    f"schema={sorted(schema_fields)} params={src_names}"
                )
    return issues


def main() -> int:
    """脚本入口：执行全部兼容性检查并输出报告。

    Returns:
        退出码：0=全部通过，1=存在不兼容项。
    """
    parser = argparse.ArgumentParser(description="alt_celery3 契约兼容性验证")
    parser.add_argument(
        "--no-source",
        action="store_true",
        help="跳过与源项目的比对，仅自检契约包内部一致性",
    )
    args = parser.parse_args()

    issues = check_catalog_integrity()
    if not args.no_source:
        issues.extend(check_source_compatibility())

    if issues:
        print(f"[FAIL] 发现 {len(issues)} 处契约不兼容项:")
        for issue in issues:
            print(f"  - {issue}")
        return 1
    print("[PASS] 契约与源任务签名完全兼容。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
