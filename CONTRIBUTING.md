# 贡献指南

感谢你对 Kiro Proxy 的关注！

## 项目结构

请先阅读 [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) 了解项目组织。

## 开发环境

```bash
# 克隆项目
git clone https://github.com/petehsu/KiroProxy.git
cd KiroProxy

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 运行
python run.py
```

## 代码规范

### Python 风格

- 遵循 PEP 8
- 使用类型提示（Type Hints）
- 函数和类添加文档字符串

### 模块组织

- 核心逻辑 → `kiro_proxy/core/`
- API 处理 → `kiro_proxy/handlers/`
- 工具脚本 → `scripts/`
- 文档 → `docs/`

### 提交信息

使用清晰的提交信息：

```
feat: 添加新功能
fix: 修复 bug
docs: 更新文档
refactor: 重构代码
test: 添加测试
chore: 构建/工具相关
```

## 添加新功能

1. **创建分支**
   ```bash
   git checkout -b feature/your-feature
   ```

2. **开发功能**
   - 在合适的模块中添加代码
   - 更新相关文档
   - 添加必要的注释

3. **测试**
   ```bash
   # 手动测试
   python run.py
   
   # 检查服务
   python scripts/check_service.py
   ```

4. **提交**
   ```bash
   git add .
   git commit -m "feat: 添加 XXX 功能"
   git push origin feature/your-feature
   ```

5. **创建 Pull Request**

## 报告问题

在 GitHub Issues 中报告问题时，请包含：

- 操作系统和版本
- Python 版本
- 错误信息和日志
- 复现步骤

## 文档

- 用户文档 → `docs/`
- 内置帮助 → `kiro_proxy/docs/zh/` 和 `kiro_proxy/docs/en/`
- API 文档 → README.md

更新功能时请同步更新文档。

## 测试

目前项目主要依赖手动测试：

1. 启动服务
2. 测试各个 API 端点
3. 测试 Web UI
4. 测试客户端集成（Claude Code, Codex CLI 等）

## 发布流程

1. 更新版本号（`kiro_proxy/main.py`）
2. 更新 README 和 CHANGELOG
3. 构建可执行文件：`python build.py`
4. 创建 GitHub Release
5. 上传构建产物

## 许可证

本项目采用 MIT 许可证。贡献代码即表示同意以相同许可证发布。

## 联系方式

- GitHub Issues: 报告问题和建议
- Pull Requests: 提交代码贡献

感谢你的贡献！🎉
