# MeetHere 接口自动化测试框架

本框架使用 `Python + pytest + requests + PyYAML`，针对 MeetHere 场馆预约系统的真实接口进行改造，不直接照搬通用 Demo。

## 为什么这样分层

```text
api_auto_framework/
|-- config/config.ini           # 环境地址、账号等可变配置
|-- core/http_client.py         # HTTP 请求和 Cookie 登录态
|-- core/case_loader.py         # YAML 读取、环境变量替换、格式校验
|-- core/assertions.py          # 可复用断言
|-- cases/smoke_cases.yaml      # 接口测试数据
|-- tests/conftest.py           # pytest fixture 和三类会话
|-- tests/test_data_driven_api.py # 参数化执行入口
`-- requirements.txt            # Python 依赖及版本
```

- 请求、数据、断言、执行相互分离，某个接口变化时不需要修改整套框架。
- `requests.Session` 自动保存普通用户和管理员登录后的 `JSESSIONID`。
- YAML 中每条用例会生成一条独立的 pytest 测试结果，失败后可直接定位用例编号。
- 配置支持环境变量覆盖，账号密码不必写死在测试代码里。

## 1. 准备环境

在项目根目录执行：

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r .\api_auto_framework\requirements.txt
```

VS Code 中按 `Ctrl+Shift+P`，选择 `Python: Select Interpreter`，再选择：

```text
.venv\Scripts\python.exe
```

## 2. 准备被测系统

启动 MySQL 和 MeetHere Spring Boot 服务，确认浏览器能访问：

```text
http://localhost:8888/login
```

默认测试账号位于 `config/config.ini`。如果实际账号不同，可以修改配置文件，也可以临时设置环境变量：

```powershell
$env:MEETHERE_USER_ID='test'
$env:MEETHERE_USER_PASSWORD='test'
$env:MEETHERE_ADMIN_ID='admin'
$env:MEETHERE_ADMIN_PASSWORD='admin'
```

## 3. 执行测试

执行当前框架全部用例：

```powershell
.\.venv\Scripts\python.exe -m pytest .\api_auto_framework\tests -v
```

只执行核心冒烟用例：

```powershell
.\.venv\Scripts\python.exe -m pytest .\api_auto_framework\tests -m smoke -v
```

按模块或优先级执行：

```powershell
.\.venv\Scripts\python.exe -m pytest .\api_auto_framework\tests -m auth -v
.\.venv\Scripts\python.exe -m pytest .\api_auto_framework\tests -m order -v
.\.venv\Scripts\python.exe -m pytest .\api_auto_framework\tests -m p0 -v
```

只检查用例能否被正常加载，不访问 MeetHere：

```powershell
.\.venv\Scripts\python.exe -m pytest .\api_auto_framework\tests --collect-only -q
```

## 4. 当前覆盖范围

- 登录页访问
- 普通用户登录及 `JSESSIONID` 校验
- 管理员登录及 `JSESSIONID` 校验
- 场馆列表查询
- 新闻列表查询
- 普通用户订单列表查询
- 管理员预约订单列表查询

## 面试表述

我参考通用接口自动化框架的分层思路，结合 MeetHere 接口返回文本、HTML 和 JSON 混合，以及使用 `JSESSIONID` 保存登录态的特点，重新封装了请求客户端、环境配置、YAML 数据驱动、pytest fixture 和通用断言。测试用例支持按模块和优先级选择执行，目前覆盖登录、场馆、新闻、用户订单和管理员订单等核心查询接口。
