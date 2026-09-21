# MeetHere 场馆预约系统测试与自动化实践

本仓库保留原作者的 Spring Boot + MySQL 项目与历史，在此基础上开展测试学习和接口自动化适配。原作者说明在本文下方；原始报告、视频和 Java 测试不代表本 fork 作者独立完成。

## 本 fork 的新增工作

- `pytest_tests/`：第一版 Python 接口回归脚本。
- `api_auto_framework/`：requests.Session、Cookie 登录态、pytest fixture、YAML 参数化和模块/优先级标记。
- 场馆页面及订单、留言视图对象的兼容性和空值处理调整。
- AI 辅助编写部分代码；实现与测试局限见下文，不宣称生产交付或量化提效。

## 运行

Java 项目使用 JDK 8、Maven 和 MySQL。先阅读原始 SQL，在独立的本地测试库导入。该历史数据可能缺少关联场馆，需检查数据完整性；不要导入生产库。

数据库配置通过 `MEETHERE_DB_URL`、`MEETHERE_DB_USER`、`MEETHERE_DB_PASSWORD` 环境变量提供。URL默认指向本地meethere_db，密码无内置值。IDEA运行配置中填写实际值后启动 `com.meethere.MeetHereApplication`，访问 `http://localhost:8888/login`。

Python使用3.10或更新版本（本地验证版本3.13）：

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r api_auto_framework/requirements.txt
.\.venv\Scripts\python.exe -m pytest api_auto_framework/tests --collect-only -q
.\.venv\Scripts\python.exe -m pytest api_auto_framework/tests -m smoke -v
```

实际执行前设置 `MEETHERE_USER_ID`、`MEETHERE_USER_PASSWORD`、`MEETHERE_ADMIN_ID`、`MEETHERE_ADMIN_PASSWORD`。测试目录里的test/admin值仅为历史演示默认值，应使用隔离测试账号。

## 验证范围与限制

新版包含7条参数化用例。历史上只完成收集及服务不可达时的跳过验证，不能据此声称业务通过。旧版曾记录17 passed、3 skipped，冒烟6 passed，结果仅适用于当时环境。

已知限制：当前场馆接口返回分页对象，YAML中仍以list断言，需要修正后实测；登录前置异常可能被跳过；查询结构断言尚未充分覆盖业务字段。暂无已验证的JMeter性能报告或70%提效数据。发布不代表这些问题已修复。

Skill配套实验独立维护于 `https://github.com/damengkai/ai-testcase-skill`（仓库创建后可访问）。

## 原作者说明

# SoftwareTesting-MeetHere
软件测试学期项目MeetHere场馆预约电子商务网站<br>
项目运行入口：SoftwareTesting-MeetHere/src/main/java/come/meethereMeetHereApplication.java<br>
MySQL数据库创建脚本：meethere_db.sql<br>
# 代码说明
前端代码在SoftwareTesting-MeetHere/src/main/resources/templates中<br>
后端代码在SoftwareTesting-MeetHere/src/main/java/come/meethere中<br>
# 测试脚本
所有的测试代码都在SoftwareTesting-MeetHere/src/test/java/come/meethere中<br>
controller单元测试代码在SoftwareTesting-MeetHere/src/test/java/come/meethere/controller中<br>
service单元测试代码在SoftwareTesting-MeetHere/src/test/java/come/meethere/service/impl中<br>
集成测试代码在SoftwareTesting-MeetHere/src/test/java/come/meethere/IntegrationTest中<br>
系统功能测试代码在SoftwareTesting-MeetHere/src/test/java/come/meethere/SystemFunctionTesting中<br>
# 项目文档
所有报告及展示PPT和系统Demo演示视频都在根目录下
### 文档清单：
《MeetHere Demo》<br>
《MeetHere展示PPT》<br>
《覆盖度报告》<br>
《静态分析报告》<br>
《系统测试计划》<br>
《系统测试报告》<br>
《缺陷报告单》<br>
《性能测试计划》<br>
《性能测试报告》<br>
# 人员分工
项目经理：徐赞博<br>
项目成员：郭晓康<br>
### 分工：
后端开发、单元测试、接口测试：郭晓康<br>
前端开发、代码静态分析、系统测试、性能测试：徐赞博<br>
