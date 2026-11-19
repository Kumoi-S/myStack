# 怎样给模型写提示词

假设你把一份草稿交给同事，说“检查一下，改得对客户友好一点”。他需要知道客户在等什么、哪些话已经对客户承诺过，以及你要一封可直接发送的邮件，还是只要修改意见。给 Gemini、Claude、GPT 写提示词时，也可以从这几件会改变成品的事写起。

## 写清要交付什么

把用途写进任务。让模型“作为资深分析师分析这份调查”，它可以合理地交出一份涵盖全部问题的报告。换成“产品负责人明天要决定先改哪个注册步骤。用这份调查推荐一个步骤，引用两条直接涉及它的反馈，并说明最可能改变建议的一个未知因素”，它就知道怎样取舍。指定角色时，写出这个人要做的决定、面对的读者以及交付物。 [Google 提示词策略](https://ai.google.dev/gemini-api/docs/prompting-strategies) · [Claude 通用提示词指南](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)

对推理任务，先写结果必须满足的条件，把方法留给模型。只有某个步骤本身决定答案是否可用，或需要人工核对时，再指定这一步。比较两份报价，可以写“分别算出购买 240 件的含税总价，列出换算用的包装规格”；做创意命名，则可以写“给三个读音容易区分、电话里能听清的名字”。后者通常用不上“逐步解释你的全部思路”。 [Google 推理提示词指南](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/thinking/prompting-guide) · [OpenAI 推理提示词指南](https://developers.openai.com/api/docs/guides/reasoning-best-practices)

## 告诉模型每份材料怎么用

长材料可以逐份写上名称、日期和适用对象，最后放具体问题。尤其要说明样稿的作用。把去年给客户的邮件和今年的合同一起交给模型，旧邮件里的金额、称呼和措辞看起来都像可以照搬的内容。下面这段中文示例把选择交代清楚了。 [Google 提示词策略](https://ai.google.dev/gemini-api/docs/prompting-strategies) · [Claude 通用提示词指南](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)

> 材料 A 是今年的合同，用来核对续约价格和生效日。材料 B 是去年给同一客户的邮件，沿用其中的称呼和句子长度。请起草今年的续约邮件。先找到 A 中支持价格和日期的条款。正文只放客户用得到的信息，把条款编号放在给我看的稿后备注里。

配图或录像时，也可以说明各自能证明什么。例如“用字幕找出演示者声称修好了哪个问题，再看随后的画面是否展示了操作结果。给出时间点；画面在结果出现前切走，就写‘这一段只拍到了操作’”。这样读者能分清说过什么、实际展示过什么。 [Google 思考与验证](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/thinking/prompting-guide) · [Gemini 多模态提示词整理](google/07-multimodal-prompting.md)

### 用两个相近的例子教会模型何时改变答案

分类、抽取和编辑任务常常只在边界处出错。挑两个只差一项关键信息的例子，让模型看到这项信息怎样改变答案。若示例的行数、标题或客套话只是碰巧一样，也值得删掉，以免被当成格式要求。 [Google 提示词策略](https://ai.google.dev/gemini-api/docs/prompting-strategies) · [OpenAI 提示词指南](https://developers.openai.com/api/docs/guides/prompt-engineering)

| 客户原话 | 希望模型记录的结果 |
|---|---|
| “周五下午我有空，你们定好了告诉我。” | 客户周五下午有空，会议时间待确认。 |
| “周五下午三点就这么定，我会参加。” | 客户已确认周五下午三点参会。 |

这对例子教的是“同意具体安排才算确认”。如果真正的任务是分类，还可以把问题直接写成“从‘已确认、仅提供可用时间、信息不足’中选一项”。问题形式本身就能减少多余解释。

## 写给实际读者

“自然、专业、友好”同时适用于朋友、同事和陌生客户，具体写出来却差很多。告诉模型对方知道什么、在担心什么，以及双方平时如何说话。下面是一个虚构的客服场景，示范怎样把这些信息放进提示词。 [GPT 写作风格指南](https://developers.openai.com/api/docs/guides/latest-model?model=gpt-6.2-astra) · [Claude 的交接与报告写法](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-2)

> 林女士上午传过两次文件，页面都报错了。我们刚刚查到两份都已收到，保留第一份即可。她问“我还要再传一次吗？”请直接回她，沿用她说的“上传”。先回答要不要再传，再解释页面为什么让她以为失败。我们还没查清报错原因，这一点照实说。

一条可直接发送的回复是：“林女士，您不用再上传了。您上午传的两份文件我们都收到了，会保留第一份。页面当时显示失败，具体原因我们还在查。”如果只给“安抚客户”的要求，模型容易写出礼貌却无用的“感谢您的耐心与理解”，甚至自行承诺解决时间。

改别人已有的文字时，还要交代哪些地方可以动。例如：“只把价格和生效日更新成新合同的内容。保留她原来的称呼和告别语。原句更新后仍通顺，就沿用原句。”写交接报告时，读者又换了，可以写“接班人没看过我们的聊天。第一段写哪个订单出了什么事、现在要他决定什么。提到内部简称时用他在订单页看到的名称”。 [OpenAI 写作与编辑指南](https://developers.openai.com/api/docs/guides/latest-model?model=gpt-6.2-astra) · [Claude 通用提示词指南](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)

## 指定怎么核对，发现错误就改稿

“再仔细检查一下”没有告诉模型到哪里寻找反证。检查事实时，要求它回到能证明那句话的来源。检查数字时，让它核对单位、分母和舍入。检查代码时，指定用户能触发的入口、原来出错的输入和应当看到的结果。最终只报告做过的检查。 [Google 推理提示词指南](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/thinking/prompting-guide) · [GPT-6 测试与验证指南](https://developers.openai.com/api/docs/guides/latest-model?model=gpt-6-astra)

例如草稿写“投诉下降了 5%”，原表写“投诉率从 20% 降到 15%”。提示词可写：“逐句核对稿里的数量、比例和变化幅度。先确认表里量的是什么，再重算差值。直接改正正文，稿后只列有实质影响的修改。”成稿应写“投诉率从 20% 降至 15%，下降了 5 个百分点”。如果要报告相对降幅，则是 25%。现有材料只给了投诉率，无法据此确定投诉件数是否减少。

对于需要实际执行的工作，写出停止条件。例如：“先用原来失败的输入从导出页面下载并打开文件，再跑受影响模块的已有测试。若共用的导出逻辑也改了，补查另一个调用入口。无法打开页面时，说清哪些检查完成了、页面下载还有待确认。”这比要求“保证万无一失”更能让读者判断证据够不够。 [GPT-6 的 Testing and verification](https://developers.openai.com/api/docs/guides/latest-model?model=gpt-6-astra)

## 让多步工作做到交付

让模型知道你要建议、草稿还是实际修改。“看看怎么改”适合征求意见；如果你想拿到改好的文件，直接写“请修改这三个文件，并检查三处链接都指向新入口”。一项决定需要人确认时，可明确在确认前能做哪些事。 [Google 的智能体提示词指南](https://docs.cloud.google.com/gemini/docs/discover/engineer-agentic-prompts) · [GPT-6 关于主动完成任务的指南](https://developers.openai.com/api/docs/guides/latest-model?model=gpt-6-astra)

> 把旧帮助页迁到新版。路径和按钮名先从当前页面查；稿件的小标题可以自行决定。两个版本的退款期限冲突时，把两处原文和拟采用的版本列给我。等待我确认期间继续改其他小节。交付时给我完整草稿和仍需确认的句子，我来决定是否发布。

长任务可以再补两句：“一次查询结果为空时，换用材料里的旧名称再找。查到新的限制、完成可查看的草稿、或确实卡住时再更新进度。”如果工作环境支持委派，还可以指定“不同地区的附件可以独立核对，汇总时由你检查是否用了同一版条款”。这样的指令给模型可执行的下一步，也让最后签字的人知道责任落在哪里。 [Claude Fable 5.2](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-2) · [GPT-6 的 Subagent delegation](https://developers.openai.com/api/docs/guides/latest-model?model=gpt-6-astra)

## 按型号调整提示词

### GPT-6 和 GPT-6.1

**小型代码改动可以给 GPT-6 Astra 写明何时结束验证。** OpenAI 提到，它有时会为一个小改动扩展测试范围。可以写：“修复后运行复现用例和项目规定的检查。通过后即可交付。出现新失败、又改了代码，或仍有具体疑点时，再补相应测试。”若项目里已经有详细规则，也要检查模型会读到的文件，清除与当前任务冲突的过期要求。 [Using GPT-6](https://developers.openai.com/api/docs/guides/latest-model?model=gpt-6-astra)

GPT-6 Astra 的回答也容易写得详细、格式多。如果读者只问一个问题，可以写：“直接用一段话回答。说清这对我的订单有什么影响。需要我在两种做法之间选择时，再分别列出选项。”需要多人协作时则可显式指明哪几项互不依赖，官方指南提到 Astra 的默认委派可能少于某些工作流的预期。 [Using GPT-6](https://developers.openai.com/api/docs/guides/latest-model?model=gpt-6-astra)

GPT-6.1 Sol 和 Terra 与 GPT-6 共用家族指南，上面的测试和格式倾向是该页对 **GPT-6 Astra** 的描述。对于 Terra，官方型号选择指南举的是基于材料写简明文字、完成有明确结果的视觉操作等用途。例如给两张工单截图，可以写“按工单编号配对，只列状态发生变化的工单，把数量和仍待处理的编号写成一段交班消息”。 [GPT-6 家族指南](https://developers.openai.com/api/docs/guides/latest-model?model=gpt-6-astra) · [OpenAI 型号选择指南](https://developers.openai.com/api/docs/guides/model-selection)

### GPT-6.2

**希望 GPT-6.2 Astra 说得更有人情味，先检查旧 prompt 里反复出现的“简短”。** OpenAI 说 Astra 默认比前代更直接。写给受影响的人时，可以明确允许它多说一句对方需要的背景：“和熟悉情况的同事说话。客户已经为这件事来回跑过两趟，先答他明天还要不要来，再说明我们会替他办哪一步。用他邮件里的称呼。能连起来说的两句话就放在同一段。”讲清处境和实际帮助，通常比要求“提高亲和力”更容易落实到字句。 [Using GPT-6.2](https://developers.openai.com/api/docs/guides/latest-model?model=gpt-6.2-astra)

做前端时，“用户友好”还涉及界面取舍。可以附截图并说明借鉴哪一处：“沿用参考图的字号层级和两栏布局。主按钮写‘下载账单’。空列表时告诉用户怎样生成第一张账单。请实际渲染页面，对照参考图检查按钮在小屏上能否看全。”这些是对一次设计任务的具体要求。OpenAI 的型号指南建议给视觉参考、明确排版方向，并把界面文字留给真正需要的信息和操作。 [GPT-6.2 的 Frontend design](https://developers.openai.com/api/docs/guides/latest-model?model=gpt-6.2-astra)

### Claude Fable 5.2

**把“要它花多少精力”和“你想读多少字”分开。** Anthropic 指出，Fable 5.2 在 low、medium 下做多步任务更容易停在中途。可以补“核对完一份附件就继续下一份；所有附件都核对完，或剩余项确实缺材料时，再交结果”。high 是默认档，高档下简单问题也常先思考。官方测试里，medium 及以上加一句“直接回答”也没消除思考。思考程度对最终回复长度影响很小；要短报告，可以直接写“给负责人两句话，保留结论和需要他做的决定”。 [Prompting Claude Fable 5.2](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-2)

代码归属也会改变改动范围。Anthropic 在小型编码任务里发现，告诉 Fable“这个代码库由你维护”会让它更愿意合并重复逻辑，也更可能加上未要求的改动。给别人的项目补一个小错误时，直接说明要修的入口和需要保留的行为，省去“把整个项目当成你自己的”这句。对于确实交给它维护的模块，可以要求它列出连带修改，方便对照实际改动审阅。 [Fable 5.2 的 Say who owns the code](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-2)

较高档位也会影响委派。在一种已鼓励委派的编码环境里，Anthropic 见过 xhigh 和 max 下的 Fable 找子代理复核自己的工作。如果这在你的小任务里频繁出现，先检查项目里是否写过“每次都找人复核”。遇到相反的问题，例如代理每步都停下请示，也应查旧笔记里有没有一次性留下的“永远不要重试”。把例外写回它真正适用的动作。 [Fable 5.2 的委派与审批指南](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-2)

### Claude Opus 5.5

Opus 5.5 默认用 medium。Anthropic 建议在 low 下需要快速回应时试一句“请直接作答”，并检查缩短思考后准确率是否还能接受。在高档下回复太慢时，优先重新选择适合任务的思考程度。读复杂图表时，可以把精力引向有用的工作：“核对左右两张图的单位和纵轴起点。刻度太小时，放大对应区域再读数。标出哪一项差异只是比例尺造成的。”需要放大或测量时，工作环境也得提供相应能力。 [Prompting Claude Opus 5.5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5-5)

Opus 有时会汇报进度并结束当前一轮，无人值守时尤其容易被误当作交付。续作消息要带上仍欠的工作，例如“北区已核对。继续核对南区订单和总表，最后检查两区合计是否等于总表。南区数据若尚未收到，告诉我缺哪个月”。读者回到对话时，一眼就能看懂已经完成什么、为什么还要继续。 [Opus 5.5 的 Unattended agentic runs](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5-5)

### Gemini 4 系列和 Gemini 3.8 Flash

给 Gemini 4 Neon、Hydrogen、Carbon 和 Argon 写长材料任务时，都可以采用 Google 的通用写法：分清材料用途，把具体问题放在资料之后，指出要从哪一段文字或画面取证。迁移时留意思考深度的默认值，Neon、Hydrogen 默认 HIGH，Carbon、Argon 默认 MEDIUM。要保持报告的长短和形式，仍要在提示词里交代读者及交付物，例如“给剪辑师三个可定位的片段，每条只写时间范围和要保留的镜头”。 [Google 提示词策略](https://ai.google.dev/gemini-api/docs/prompting-strategies) · [Gemini 4 家族指南](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/start/get-started-with-gemini-4)

Gemini 3.8 Flash 的指南用视频工作解释了思考程度的选择。假设材料是同一段培训录像和转写稿，下面三问需要查的东西并不一样。 [Gemini 3.8 Flash 开发者指南](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/guides/gemini-3-8-flash)

| 你要做的工作 | 可以这样问 |
|---|---|
| 在已有转写稿中检索，适合先试 LOW | “从转写稿找出第一次提到‘手动复位’的时间点和原句。” |
| 一般视频问答或片段检索，可从默认 MEDIUM 开始 | “找出讲师示范复位的片段，写出起止时间，以及学员要按的两个键。” |
| 长视频跨段推断或快速动作辨认，可试 HIGH | “比较开头的错误示范与结尾的正确示范。逐段定位手离开按钮的时刻，说明两次操作的先后顺序差在哪儿。遮挡处标明看不清。” |

## 修改已有提示词

拿一次真实的坏回答定位要改的句子。例如模型总写“我可以继续为你核对”，翻回提示词，发现原句是“每完成一项就总结并等待确认”。可以直接换成“每完成一项就记下结论并继续，只有两份价格表冲突才请我定夺”。重跑一个材料齐全的旧任务，看它是否能做完；再跑一个价格确实冲突的任务，看它是否把问题留给了你。换型号时也用同一对输入，才能判断旧句子今天是否还有必要。 [Google 提示词迭代策略](https://ai.google.dev/gemini-api/docs/prompting-strategies) · [OpenAI 评测指南](https://developers.openai.com/api/docs/guides/evaluation-best-practices)
