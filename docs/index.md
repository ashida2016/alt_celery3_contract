# alt_celery3_contract

`alt_celery3` 跨服务任务契约包：纯声明性质的任务注册名、强类型入参 Schema 与契约函数。

```{toctree}
:maxdepth: 2
```

## 快速开始

```python
from alt_celery3_contract import TASK_CATALOG, TaskName, schemas

entry = TASK_CATALOG[TaskName.GENERATE_MANY_STUDENTS.value]
payload = entry.payload_model(numbers=1_000_000)
```

详细使用说明见项目根目录 README.md。
