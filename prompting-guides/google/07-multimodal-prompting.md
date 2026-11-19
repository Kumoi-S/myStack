# Gemini Multimodal Prompting

## 1. 总原则

Gemini 可以把文本、图像、音频、视频和文档作为同一请求中的输入。提示词应明确每种模态的任务，不要假设模型会自动理解文件之间的关系。

## 2. 图像

推荐说明：
- 要读取的区域、对象或字段；
- 是否需要 OCR、计数、比较或空间关系；
- 对低置信度结果如何标注；
- 是否需要引用图像中的具体证据。

示例：

```text
请读取图像中的发票表格。
只提取发票号、日期、供应商、税前金额、税额和总额。
无法辨认的字段返回 null，并在 confidence_notes 中说明原因。
不要根据常识补齐缺失值。
```

## 3. 音频

说明目标是转写、说话人区分、摘要、翻译、情绪/事件识别还是时间戳提取。不要把转写和总结混成一个没有边界的任务。

示例：

```text
先逐字转写音频，保留时间戳和说话人标签。
然后单独给出 5 条摘要。
听不清的片段标记为 [inaudible]，不要猜测。
```

## 4. 视频

指定：
- 时间范围；
- 关注的动作/对象；
- 是否需要时间戳；
- 事件顺序；
- 是否需要跨镜头/跨片段归纳。

Gemini 4 的 agentic video understanding 默认关闭；需要该能力时按当前 API 文档启用 `media_processing="agentic"`。使用前确认当前模型和 API 版本支持。

## 5. 文件和上下文

对于大型或会重复使用的文件，优先考虑 Files API 或平台支持的 Cloud Storage URI，而不是反复以内联数据上传。单文件大小、总请求大小和文件类型限制会随 Gemini API、Agent Platform、模型和传输方式变化，实施前应查看对应 API 的最新限制。

长文件建议：
- 每个文件标明名称、类型、用途；
- 提示词里说明要对哪些文件进行比较；
- 要求输出引用文件名、页码或时间戳；
- 把具体问题放在资料之后。

## 官方来源

- [Files API](https://ai.google.dev/gemini-api/docs/files)
- [Prompt design strategies](https://ai.google.dev/gemini-api/docs/prompting-strategies)
- [Get started with Gemini 4](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/start/get-started-with-gemini-4)
