# alt_celery3_contract

`alt_celery3` 的**跨服务任务契约包**：通过静态扫描源项目中的全部 Celery 任务，提炼出任务注册名、入参签名、类型注解与文档，生成纯声明性质的强类型契约代码。

本包**不包含任何业务实现逻辑**——不连接数据库、不调用外部 API、不依赖 Celery，仅作为调用方（生产者）与执行方（worker）之间的类型化接口契约。

## 功能

- **`constants.py`**：`TaskName` 枚举维护全部 11 个任务的注册名字符串
- **`schemas.py`**：Pydantic v2 强类型入参模型（多参数 / 复杂任务）
- **`definitions.py`**：与源任务同名同签名的契约函数（函数体统一 `raise NotImplementedError`）
- **`catalog.py`**：`TASK_CATALOG` 全局映射（任务名 → 契约函数 + Schema + 描述）
- **`verify_contracts.py`**：基于 `inspect` 的契约与源任务签名兼容性验证脚本

## 任务清单（11 个）

| 注册名 | 入参 Schema | 说明 |
| --- | --- | --- |
| `tasks.add` | `AddPayload` | 计算两数之和 |
| `tasks.periodic_add` | `AddPayload` | 周期性加法定时任务 |
| `tasks.try_mysql` | — | MySQL 业务库连通性测试 |
| `tasks.get_one_student` | — | 查询单个学生信息 |
| `tasks.generate_many_students` | `GenerateManyStudentsPayload` | 批量生成学生信息 |
| `tasks.get_un_groups` | — | 获取高校信息（LLM） |
| `tasks.init_web_db` | — | 初始化数据库（危险操作） |
| `tasks.simu_ncee` | `SimuTaskPayload` | 模拟高考 |
| `tasks.simu_admission` | `SimuTaskPayload` | 模拟高校录取 |
| `tasks.simu_exam` | `SimuTaskPayload` | 模拟高校日常考试 |
| `tasks.simu_graduate` | `SimuTaskPayload` | 模拟本科毕业 |

## 安装

```bash
# pip（推荐 editable 模式）
pip install -e .

# conda
conda env create -f environment.yml && conda activate alt_celery3_contract
```

## 使用示例

```python
from alt_celery3_contract import TASK_CATALOG, TaskName, schemas

# 1. 枚举任务名，跨服务投递时直接引用
name = TaskName.GENERATE_MANY_STUDENTS.value   # "tasks.generate_many_students"

# 2. 用 Schema 强类型校验入参
payload = schemas.GenerateManyStudentsPayload(numbers=1_000_000)

# 3. 查询任务目录（契约函数 + Schema + 描述）
entry = TASK_CATALOG[name]
print(entry.description)          # 批量生成随机学生信息并写入 ...
print(entry.payload_model)        # <class '...GenerateManyStudentsPayload'>

# 4. 结合 celery 跨服务投递（调用方需自行配置 broker）
from celery import Celery
app = Celery(broker="redis://:pass@redis-host:6379/0")
app.send_task(name, kwargs=payload.model_dump())
```

## 兼容性验证

验证契约与源任务签名的兼容性（需能导入源项目 `../alt_celery3`）：

```bash
python verify_contracts.py            # 完整比对
python verify_contracts.py --no-source  # 仅自检契约包内部一致性
```

验证内容：任务注册名双向对齐、参数名称/顺序/默认值/类型注解一致、Schema 字段与业务参数对齐。

## 文档

文档基于 Sphinx + MyST 构建，托管配置见 `.readthedocs.yaml`，本地构建：

```bash
pip install -e .[docs]
sphinx-build -b html docs docs/_build/html
```
