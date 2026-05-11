# GPT API 配置说明（Windows + IntelliJ IDEA）

本文档说明如何把本工具切换为调用 OpenAI 官方 GPT API。当前代码读取环境变量，不需要把密钥写入 Python 文件。

## 1. 配置项含义

| 配置项 | 必填 | 示例 | 说明 |
| --- | --- | --- | --- |
| `AI_API_KEY` | 是 | `sk-...` | OpenAI API Key。请只放在环境变量或 IDEA Run Configuration 中，不要提交到 Git。 |
| `AI_API_BASE_URL` | 是 | `https://api.openai.com/v1` | OpenAI 官方 API 的基础地址。代码会自动请求 `${AI_API_BASE_URL}/chat/completions`。 |
| `AI_MODEL` | 是 | `gpt-4o-mini` | 使用的 GPT 模型。可按预算和质量需求改为 `gpt-4o`、`gpt-4.1` 等可用模型。 |
| `AI_TIMEOUT_SECONDS` | 否 | `120` | API 请求超时时间，默认 120 秒。论文 chunk 较长时可以调大。 |

## 2. `.env.example` 推荐写法

项目根目录的 `.env.example` 可以保持如下格式：

```env
# OpenAI official GPT API settings
# Copy these values into IntelliJ IDEA Run Configuration > Environment variables.
# Do not commit real secrets.
AI_API_KEY=replace-with-your-openai-api-key
AI_API_BASE_URL=https://api.openai.com/v1
AI_MODEL=gpt-4o-mini
AI_TIMEOUT_SECONDS=120
```

> 注意：当前程序不会自动读取 `.env` 文件；它读取的是系统环境变量或 IDEA Run Configuration 中配置的环境变量。

## 3. Windows PowerShell 临时配置

如果你想先在 PowerShell 里测试：

```powershell
$env:AI_API_KEY="你的 OpenAI API Key"
$env:AI_API_BASE_URL="https://api.openai.com/v1"
$env:AI_MODEL="gpt-4o-mini"
$env:AI_TIMEOUT_SECONDS="120"
```

然后运行：

```powershell
python -m paper_style_ai.cli --help
```

## 4. IntelliJ IDEA 中配置 GPT API

在 IDEA 中进入：

```text
Run → Edit Configurations... → 选择你的 Python 配置 → Environment variables
```

添加以下变量：

```text
AI_API_KEY=你的 OpenAI API Key
AI_API_BASE_URL=https://api.openai.com/v1
AI_MODEL=gpt-4o-mini
AI_TIMEOUT_SECONDS=120
```

如果 IDEA 要求写成一行，使用分号分隔：

```text
AI_API_KEY=你的 OpenAI API Key;AI_API_BASE_URL=https://api.openai.com/v1;AI_MODEL=gpt-4o-mini;AI_TIMEOUT_SECONDS=120
```

## 5. 推荐模型选择

- `gpt-4o-mini`：成本较低，适合先用 `--limit-chunks 5` 测试 PDF 读取、chunk 切分和模板生成。
- `gpt-4o`：质量更高，适合正式润色或重要论文段落。
- 其他 GPT 模型：只要你的 OpenAI 账号可用，就可以把 `AI_MODEL` 改成对应模型名。

## 6. 安全提醒

- 不要把真实 API Key 写入 `config.py`。
- 不要把真实 API Key 写入 README。
- 不要提交 `.env` 文件。
- 如果 API Key 泄露，应立刻在 OpenAI 控制台撤销并重新生成。
