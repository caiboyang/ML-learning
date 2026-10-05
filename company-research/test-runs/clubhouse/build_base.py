"""Fresh Clubhouse test run of the company-research skill (PR head 4885886). Writes research.json."""
import json, sys

ACC = "2026-10-02"
E = []
def ev(i, title, nature, date, url, support, limitation, locator="正文"):
    E.append(dict(id=i, title=title, nature=nature, date=date, locator=locator, url=url, support=support, limitation=limitation))

ev("e-check", "Clubhouse 博客：Check 1, 2, 3... Is this thing on?", "公司原始披露", "2020-07-11",
   "https://joinclubhouse.ghost.io/check-1-2-3/",
   "开发三个多月、只给朋友试用；有意慢慢放人，理由是不让产品崩、保持社区多样；当时只有两名全职员工。",
   "创始人自述的意图，不说明慢放量带来的效果。")
ev("e-welcome", "Clubhouse 博客：Welcoming More Voices（B 轮公告）", "公司原始披露", "2021-01-24",
   "https://joinclubhouse.ghost.io/welcoming-more-voices/",
   "两位创始人十年都在做社交产品、多次失败；2019 年秋合伙，在音频方向多次迭代后于 2020-03 上线；过去一周约 200 万人来过；计划做 Android 和创作者支持。",
   "“来过”的定义和去重方式未说明；不是留存数据。")
ev("e-highlight", "TechCrunch：Pinterest 收购 Highlight 团队", "媒体报道", "2016-07-14",
   "https://techcrunch.com/2016/07/14/pinterest-acquires-the-team-behind-highlight-and-shorts/",
   "Davison 的前一个产品 Highlight 靠附近的人起量，后来没有成为日常工具；报道认为它受限于身边人的密度。",
   "这是记者对 Highlight 的评价，用来说明创始人经历，不是对 Clubhouse 的直接证据。")
ev("e-wiki", "Wikipedia：Clubhouse (app)", "二手汇编（只作线索）", f"{ACC} 访问",
   "https://en.wikipedia.org/wiki/Clubhouse_(app)",
   "前身为播客方向的 Talkshow（2019 年秋）；2020-05 a16z 领投 1200 万美元 A 轮；2020-12 约 60 万注册用户；邀请码曾在 eBay 卖到 400 美元。",
   "百科条目，底层多为付费墙报道（Bloomberg、NYT），本次未逐一读到原文；只用于时间线，不用于关键数字。",
   "History 一节")
ev("e-musk", "CNBC：Musk 在 Clubhouse 上对话 Robinhood CEO", "媒体报道", "2021-02-01",
   "https://www.cnbc.com/2021/02/01/elon-musk-on-clubhouse-robinhood-ceo-explains-trading-restrictions.html",
   "2021-02-01 Musk 进入 Clubhouse 房间，与 Robinhood CEO 对话。",
   "只证明事件发生，不提供带来的下载或留存。")
ev("e-tc8m", "TechCrunch：Clubhouse 全球下载超过 800 万", "媒体转述第三方测量", "2021-02-18",
   "https://techcrunch.com/2021/02/18/report-social-audio-app-clubhouse-has-topped-8-million-global-downloads/",
   "App Annie 估算：2021-02-01 累计约 350 万，02-16 约 810 万；报道把增长归因于 Musk、扎克伯格等名人露面；仍是邀请制。",
   "下载为第三方估算；名人归因是报道判断，不是因果测量。")
ev("e-bi", "Business Insider：Clubhouse 的增长与内容治理问题", "媒体转述公司口径", "2021-03-20",
   "https://www.businessinsider.com/clubhouses-growth-raises-troubling-questions-over-spread-of-misinformation-2021-3",
   "公司 2 月下旬称每周活跃用户超过 1000 万；App Annie 估算 3 月 1 日累计下载约 1140 万。",
   "周活为公司口径，活跃定义未公开；之后公司没有再公布周活。")
ev("e-sensor", "Sensor Tower：社交音频应用增长", "第三方原始测量", "2021-04",
   "https://sensortower.com/blog/social-audio-apps-growth",
   "Clubhouse 全球月安装估算：2021-01 约 240 万，02 约 960 万，03 约 270 万（比 2 月下降 72%）。",
   "安装量估算衡量新增，不追踪同一批人是否留下。", "Breakout Hits")
ev("e-9to5", "9to5Mac：Clubhouse 4 月下载跌到约 90 万", "媒体转述第三方测量", "2021-05-03",
   "https://9to5mac.com/2021/05/03/clubhouse-downloads-plummet-to-900000-in-april-as-competition-grows/",
   "转述 Sensor Tower：2021-04 全球下载约 92.2 万。",
   "二手转述；5 月才见报，不能算作 4 月决策时公开可知的信息。")
ev("e-creator", "Clubhouse 博客：Creator First 加速计划", "公司原始披露", "2021-03",
   "https://joinclubhouse.ghost.io/creator-first-accelerator/",
   "给创作者寄设备、帮做内容和推广、发月度津贴、对接品牌；申请截至 2021-03-31。",
   "只有计划内容，没有入选人数、津贴金额和创作者后续是否持续开房。")
ev("e-pay", "Clubhouse 博客：Introducing Payments", "公司原始披露", "2021-04-05",
   "https://joinclubhouse.ghost.io/introducing-payments/",
   "第一个变现功能是用户给创作者打赏，100% 归创作者，平台不抽成；收款资格分批开放。",
   "说明 2021 年的收入设计，不说明打赏规模。")
ev("e-verge", "The Verge：Twitter 曾讨论以约 40 亿美元收购 Clubhouse", "媒体转述", "2021-04-07",
   "https://www.theverge.com/2021/4/7/22372510/twitter-clubhouse-acquire-four-billion-spaces-audio",
   "转述 Bloomberg：Twitter 与 Clubhouse 讨论过约 40 亿美元收购，谈判已停滞，原因不明。",
   "二手转述，谁先接触、为何停滞都不清楚；Davison 2022 年拒绝评论。")
ev("e-seriesc", "Clubhouse 博客：Growing a Global Community（C 轮公告）", "公司原始披露", "2021-04-18",
   "https://joinclubhouse.ghost.io/growing-a-global-community/",
   "宣布 C 轮（a16z 领投，DST、Tiger 等跟投）；“今年团队已扩大到原来的四倍”；承认增长超过了早期推荐算法的能力，资金重点投向发现和创作者。",
   "估值未在公告中写明；“四倍”是已发生的扩张，不是计划。")
ev("e-open", "Clubhouse 博客：Opening Day", "公司原始披露", "2021-07-21",
   "https://joinclubhouse.ghost.io/opening-day/",
   "取消等待名单，向所有人开放；半年内团队 8 人→58 人，每日房间 5 万→50 万；5 月中上线 Android 后新增 1000 万人；平均每位听众每天超过 1 小时；邀请分批、每周迎新和周日 Town Hall 是早期做法。",
   "公司自报，未审计；“平均每天超过 1 小时”只覆盖仍在使用的人，不是全体新增的留存。")
ev("e-replays", "Clubhouse 博客：Introducing Replays", "公司原始披露", "2021 年秋（博文未标日期）",
   "https://joinclubhouse.ghost.io/clubhouse-replays-room-recording/",
   "公开房间可以回放、剪辑、下载源文件，并显示总收听人数。",
   "上线时间据 Wikipedia 转引路透社为 2021-09 至 10；没有回放使用数据。")
ev("e-houses", "TechCrunch：Clubhouse 测试私密社区 Houses", "媒体报道", "2022-08-04",
   "https://techcrunch.com/2022/08/04/clubhouse-beta-testing-private-houses/",
   "Houses 是只给熟人的私密走廊，成员提名朋友加入，有固定见面时间。",
   "功能上线，不说明使用量和留存变化。")
ev("e-davison", "TechCrunch：Davison 谈热潮及其后果", "媒体转述创始人原话", "2022-10-27",
   "https://techcrunch.com/2022/10/27/clubhouses-paul-davison-on-twitter-the-impact-of-hype-and-what-happened/",
   "Davison：曾有两个月“疯狂、不可持续的”月增 10 倍；服务到处崩；热潮中加入的人“体验很差……找不到好房间”；公司从没请名人入驻；现在私密房间占比更大；拒绝透露日活。",
   "创始人事后解释，可能有自我辩护；没有给出任何留存数字。")
ev("e-cnbc23", "CNBC：疫情把 Clubhouse 推到 40 亿美元估值", "媒体报道", "2023-04-27",
   "https://www.cnbc.com/2023/04/27/clubhouse-layoffs-app-reached-4-billion-valuation-during-pandemic.html",
   "估值 2020 年中约 1 亿→2021-01 约 10 亿→2021-04 约 40 亿美元；“在收入模式建立之前增长就已停滞”；Davison 2021 年底对 Bloomberg 说“长得太快了”；按 LinkedIn 约 200 名员工。",
   "估值为报道口径；员工数来自 LinkedIn；“太快”一语为转引。")
ev("e-email", "Clubhouse 博客：创始人致员工信", "公司原始披露", "2023-04-27",
   "https://joinclubhouse.ghost.io/april-27-2023/",
   "裁员超过一半；疫情后很多人更难在 Clubhouse 上找到朋友，也难把长对话塞进日常；团队太大、协调慢；公司仍有数年资金，不是因为缺钱裁员。",
   "管理层自述，问题描述可信但没有数据；裁员原因可能不止信中所写。")
ev("e-chats", "Clubhouse 博客：the new clubhouse（推出 Chats）", "公司原始披露", "2023-09-06",
   "https://joinclubhouse.ghost.io/the-new-clubhouse/",
   "改成更像消息应用：Chats 是只给好友的异步语音群聊，目标是“即使你在 Clubhouse 上朋友不多、时间不多”也能用；保留直播房间。",
   "产品意图，不是效果证明。")
ev("e-plus", "Clubhouse 帮助中心：Clubhouse Plus Features", "公司原始披露", "2025-10-22 创建",
   "https://support.clubhouse.com/hc/en-us/articles/45818422930835-Clubhouse-Plus-Features",
   "Plus 订阅：匿名收听、看谁访问过主页等功能，在设置里开通。",
   "没有订阅人数、价格披露和续费率；网页有反爬，本次经帮助中心公开接口读取。")
ev("e-rewards", "Clubhouse 帮助中心：Rewards FAQ and Policies", "公司原始披露", "2025-12-13 创建",
   "https://support.clubhouse.com/hc/en-us/articles/47352574166035-Rewards-FAQ-and-Policies",
   "用户用真钱在应用内买 Coins，给发言人送付费表情；平台按贡献发放 Gold，满足条件可经 Stripe 提现。",
   "用户花的钱、平台留存部分、发给创作者的部分都未披露。")
ev("e-subfaq", "Clubhouse 帮助中心：订阅 FAQ", "公司原始披露", "2025-10-22 创建",
   "https://support.clubhouse.com/hc/en-us/articles/45818798443411-FAQ",
   "订阅可经应用内、App Store、Google Play 购买和取消，退款走渠道方。",
   "证明收费渠道存在，不证明收入规模。")
ev("e-home", "Clubhouse 官网", "公司原始披露", f"{ACC} 访问", "https://www.clubhouse.com/",
   "官网仍在运营，提供下载入口。", "不说明活跃规模。")
ev("e-spaces-beta", "TechCrunch：Twitter Spaces 开始内测", "媒体报道", "2020-12-17",
   "https://techcrunch.com/2020/12/17/twitter-launches-its-voice-based-spaces-social-networking-feature-into-beta-testing/",
   "Twitter 2020-12 开始内测语音房 Spaces。", "内测范围小，不说明使用量。")
ev("e-spaces-600", "Twitter 博客：Spaces is here（网页存档）", "公司原始披露", "2021-05-03",
   "https://web.archive.org/web/20240503102030/https://blog.twitter.com/en_us/topics/product/2021/spaces-is-here",
   "向粉丝 600 以上的账号开放主持，理由是这些账号已有听众、更可能有好的主持体验。",
   "原网址有反爬，经网页存档读取；不说明使用和留存。")
ev("e-stage", "Discord 博客：Stage Discovery", "公司原始披露", "2021-06-01",
   "https://discord.com/blog/discover-the-next-great-community-in-stage-discovery",
   "Discord 2021-03 在服务器里推出 Stage 语音舞台，6 月试点跨社区的公开发现。", "试点规模和效果未披露。")
ev("e-stage-end", "Discord 博客：What’s Next for Communities", "公司原始披露", "2021-10-01",
   "https://discord.com/blog/whats-next-for-communities-at-discord",
   "近百万个社区开过 Stage，每月数十万个社区办语音活动；10-04 关闭公开发现，继续投入社区内的 Stage。",
   "累计和月度社区数，不是同批留存；关闭发现的原因是公司表述。", "Focusing on the Future of Communities")
ev("e-greenroom", "TheWrap：Spotify 推出 Greenroom", "媒体报道", "2021-06-16",
   "https://www.thewrap.com/spotify-just-launched-its-clubhouse-rival-greenroom/",
   "Spotify 收购体育语音应用 Locker Room 后改版为 Greenroom，作为独立应用上线。", "不说明使用量。")
ev("e-spotify-end", "TechCrunch：Spotify 关闭 Spotify Live", "媒体转述公司声明", "2023-04-03",
   "https://techcrunch.com/2023/04/03/spotify-is-shutting-down-its-live-audio-app-spotify-live/",
   "Spotify 关闭由 Greenroom 改名的 Spotify Live：作为独立应用“不再合理”，继续在主应用里试艺人“听歌派对”。",
   "公司声明，没有给出用户数。")
ev("e-fb", "MacRumors：Facebook 推出 Live Audio Rooms", "媒体报道", "2021-06-22",
   "https://www.macrumors.com/2021/06/22/facebook-clubhouse-competitor-launches/",
   "Facebook 2021-06 在美国推出语音房，先开放给部分公众人物和群组。", "本次未查到其后续使用或关闭的原始材料。")
ev("e-hp-up", "TechCrunch：Houseparty 一个月 5000 万注册", "媒体转述公司口径", "2020-04-15",
   "https://techcrunch.com/2020/04/15/houseparty-reports-50m-sign-ups-in-past-month-amid-covid-19-lockdowns/",
   "疫情封城期间 Houseparty 一个月 5000 万注册，部分市场约为平时 70 倍。", "注册不是活跃；不能和安装量直接比。")
ev("e-hp-end", "TechCrunch：Epic 关闭 Houseparty", "媒体报道", "2021-09-09",
   "https://techcrunch.com/2021/09/09/epic-games-to-shut-down-houseparty-in-october-including-the-video-chat-fortnite-mode-feature/",
   "Epic 2019 年约 3500 万美元收购 Houseparty，2021-10 关闭，团队转做 Epic 内的社交功能。",
   "关闭也受母公司战略影响，不能单独证明用户留不住。")

R = []
def rec(i, section, role, kind, title, text, status, limitation, evs, company="clubhouse", related=None, **extra):
    r = dict(id=i, companyId=company, section=section, kind=kind, role=role, status=status, title=title, text=text,
             limitation=limitation, evidenceIds=evs, relatedIds=related or [])
    r.update(extra); R.append(r)

# 01 执行结论
rec("verdict", "exec", "judgment", "inference",
    "注意力被证明了，回来的理由没有被证明",
    "Clubhouse 在 2021 年初几周内吸引上千万人，靠的是疫情里的空闲时间、名人房间和稀缺的邀请码，这三样都会消退；产品本身的规律是人越多越难找到好房间，热潮里进来的人大多没留下。2025 年才开始收费，规模未公开。",
    "核心判断", "没有公开的同批留存；“大多没留下”来自创始人对热潮期新用户体验的描述和下载的断崖式回落，是推断。",
    ["e-bi", "e-sensor", "e-davison", "e-email", "e-plus", "e-rewards"], related=["p-activation", "p-revisit", "dec-scale"])
rec("m-wau", "exec", "metric", "fact", "周活跃用户（峰值）", "2021 年 2 月下旬公司口径。", "公司口径",
    "活跃定义未公开；此后公司不再公布周活，后续走势只能看下载估算。", ["e-bi", "e-welcome"],
    metric=dict(value="1000 万+", unit="人／周", basis="2021-02 下旬公司所说；一个月前（2021-01）为约 200 万人／周"))
rec("m-installs", "exec", "metric", "fact", "月安装量：峰值后两个月", "同一测量方，相邻月份。", "第三方估算",
    "安装衡量新增，不等于用户流失；4 月数字为二手转述。", ["e-sensor", "e-9to5"],
    metric=dict(value="960 万 → 92 万", unit="全球月安装", basis="Sensor Tower：2021-02 → 2021-04，降约 90%"))
rec("m-revenue", "exec", "metric", "fact", "公司收入", "2021 年的打赏全部给创作者；2025 年起有 Plus 订阅和 Coins。", "未公开",
    "不能填零：收费机制存在，只是金额没有披露。", ["e-pay", "e-plus", "e-rewards", "e-cnbc23"],
    metric=dict(value="未公开", unit="收入", basis="2021–2024 没有平台收入设计；2025 起有订阅和 Coins，金额未披露"))

# 02 现状：证明命题（消费社交）
def proof(i, prop, state, evidence, gap, nxt, evs, limitation):
    rec(i, "status", "proof", "inference", prop, evidence, state, limitation, evs,
        proof=dict(proposition=prop, state=state, evidence=evidence, gap=gap, next=nxt))
proof("p-activation", "激活：新用户第一次就找到值得留下的房间", "反证",
      "CEO 2022 年承认：热潮里加入的人“体验很差”，服务到处崩，之后几个月新人“找不到好房间”。",
      "没有新用户首日找到房间的比例。", "按加入月份查首日进房、发言、关注人数。", ["e-davison"],
      "创始人事后说法；对核心早期用户（Opening Day 说平均每天超 1 小时）不成立。")
proof("p-cohort", "同批留存：同一批人几个月后还在", "未证明",
      "从未公开。月安装 2→4 月降约 90% 只说明新增变少，不说明老用户走了多少。",
      "没有任何批次的 D30/D90。", "查 2021-01、02、05（Android）三批用户的 30/90 天活跃。", ["e-sensor", "e-9to5"],
      "下载回落和留存是两件事，这里只能写“未证明”。")
proof("p-revisit", "回访：用户会在日常生活里反复回来", "反证",
      "2023 年创始人信：疫情后很多人更难在 Clubhouse 上找到朋友，也难把长对话塞进日常。这正是实时房间赖以回访的两个条件。",
      "没有活跃天数分布。", "查每周活跃天数和回访间隔，分疫情前后。", ["e-email"],
      "管理层定性描述，没有数字；但出自公司自己，方向可信。")
proof("p-content", "内容沉淀：一场对话结束后留下可复用的东西", "未证明",
      "高峰期房间结束即消失；回放和剪辑到 2021 年秋才上线，已在下载回落之后。",
      "没有回放收听量。", "查回放和剪辑带来的再次进房。", ["e-replays", "e-sensor"],
      "功能上线时间清楚，效果没有数据。")
proof("p-creator", "创作者留存：主持人在没有补贴时也持续开房", "未证明",
      "供给靠补贴拉起：Creator First 发设备、津贴、帮推广；打赏 100% 给创作者。没有任何主持人持续开房的数据。",
      "入选人数、津贴金额、主持人留存都未公开。", "查补贴结束后主持人连续开房的比例。", ["e-creator", "e-pay"],
      "补贴存在不代表供给不可持续，只是无法证明。")
proof("p-monetize", "变现：有可持续的收入来源", "有信号",
      "2021–2024 年平台没有收入设计（打赏全给创作者，报道称收入模式建立前增长就停了）；2025 年起有 Plus 订阅和用真钱买的 Coins。",
      "订阅人数、Coins 流水、平台分成都未公开。", "查 Plus 价格与订阅量、Coins 年流水与提现比例。", ["e-pay", "e-cnbc23", "e-plus", "e-rewards", "e-subfaq"],
      "只证明收费机制存在；收入能否覆盖成本完全未知。")

# 03 产品
rec("a-products", "products", "asset", "fact", "产品形态：三年换了三次", "按上线时间排列；每次都在回应同一个问题。", "时期与证据分列",
    "使用量全部未公开，只能比较设计意图。", ["e-check", "e-open", "e-replays", "e-houses", "e-chats", "e-plus", "e-rewards"],
    fields=[
        {"label": "2020-03 公开直播房间", "value": "进房当听众、举手上台；唯一有规模证据的形态（周活千万级只发生在这个阶段）。"},
        {"label": "2021-07 Backchannel 私信", "value": "上线一周 9000 万条私信（公司自报）；第一次让关系在房间之外延续。"},
        {"label": "2021 秋 回放与剪辑", "value": "让一场对话留下可复用的内容；上线时下载已回落。"},
        {"label": "2022-08 Houses 私密社区", "value": "熟人提名加入、固定见面时间，从公开广场退回小圈子。"},
        {"label": "2023-09 Chats 异步语音群聊", "value": "不要求同时在线，明确面向“朋友不多、时间不多”的用户。"},
        {"label": "2025 Plus 订阅、Coins 付费表情", "value": "第一批平台收入来源；规模未披露。"}])
rec("a-portfolio", "products", "judgment", "inference", "组合判断：后面每一次改版都在修“凑不齐人”",
    "公开房间要求对的人同时在线；Houses 用熟人圈降低找人的成本，Chats 干脆取消同时在线。方向越来越像消息应用，离当初让它爆红的公开舞台越来越远。",
    "研究者判断", "改版动机来自公司公告；改版是否奏效没有数据。", ["e-houses", "e-chats", "e-email"], related=["p-revisit"])

# 04 渠道
rec("a-channels", "channels", "asset", "inference", "获客渠道：几乎零成本，但都不归公司控制", "按作用分；贡献占比全部未公开。", "研究者整理",
    "没有任何渠道的归因数据；作用判断来自报道和创始人说法。", ["e-wiki", "e-tc8m", "e-davison", "e-open", "e-check"],
    fields=[
        {"label": "邀请制｜主渠道", "value": "每人有限邀请，沿通讯录扩散；稀缺制造了向往（邀请码曾在 eBay 卖到 400 美元）。2021-07 取消后，这个渠道的稀缺价值随之消失。"},
        {"label": "名人房间｜放大器", "value": "Musk、扎克伯格露面后两周下载从 350 万到 810 万；公司说从没请名人来，所以也无法复制。"},
        {"label": "国家级邀请链｜放大器", "value": "日本、德国等多国 App Store 第一，德国有播客主在 Telegram 群里组织邀请链。"},
        {"label": "神秘感｜放大器", "value": "创始人不回应媒体，热度由外界叙事推动（Davison 2022 年自述）。"},
        {"label": "开放注册与 Android｜覆盖", "value": "2021-05 至 07 打开，新增 1000 万人（公司自报），但已没有稀缺和名人效应加持。"}])

# 05 起步资产
rec("a-assets", "assets-map", "asset", "inference", "起步资产：大多是借来的，会过期", "按能否持续补充区分。", "研究者判断",
    "资产作用是解释，不是测量；投资人网络对早期用户的贡献没有数字。", ["e-welcome", "e-highlight", "e-wiki", "e-cnbc23", "e-email"],
    fields=[
        {"label": "疫情空闲时间｜外部、会过期", "value": "实时语音要求大家同时有空；2023 年创始人信说疫情后这一条件消失了。"},
        {"label": "名人与硅谷投资人圈｜借来的", "value": "早期用户集中在科技投资圈，a16z 2020 年在内测期就投了约 1 亿美元估值；名人露面带来峰值，但不受公司控制。"},
        {"label": "邀请稀缺｜一次性", "value": "只在封闭期有效，开放即用完。"},
        {"label": "创始人经验｜持续", "value": "两人十年都在做社交产品；Davison 的 Highlight 也是靠“身边有对的人”才有用，后来就卡在密度上——同一个难题在 Clubhouse 重现。"},
        {"label": "融资｜持续但买不到留存", "value": "三轮估值 1 亿→10 亿→40 亿美元，2023 年仍有数年资金；钱能扩团队和服务器，解决不了凑不齐人。"}])
# 06 团队
rec("team", "team-map", "team", "fact", "两位创始人，团队跟着热度涨、跟着回落砍", "人数：2（2020-07）→ 8（2021-01）→ 58（2021-07）→ 约 200（2023-04，LinkedIn）→ 裁员过半。", "公开信息",
    "内部分工、股权和每人投入都未公开；约 200 人为 LinkedIn 口径。", ["e-check", "e-open", "e-cnbc23", "e-email", "e-welcome", "e-highlight"],
    people=[
        {"name": "Paul Davison", "role": "联合创始人、CEO", "background": "做过附近社交应用 Highlight，团队 2016 年被 Pinterest 收购",
         "responsibility": "对外代表公司（采访、公告署名）；内部具体分工未公开", "commitment": "全职；持股未公开", "evidenceIds": ["e-highlight", "e-davison"]},
        {"name": "Rohan Seth", "role": "联合创始人", "background": "多年做社交产品（帮朋友在城市里找到彼此的应用）；公开履历本次未逐一核实",
         "responsibility": "与 Davison 联名发布公司决定；内部具体分工未公开", "commitment": "全职；持股未公开", "evidenceIds": ["e-welcome", "e-email"]}])

# 07 自身 0→1 路径
def step(i, stage, title, action, result, mechanism, evs, limitation, kind="inference"):
    rec(i, "path", "step", kind, title, action, "时间与证据分列", limitation, evs, stage=stage,
        fields=[{"label": "动作", "value": action}, {"label": "结果", "value": result}, {"label": "机制判断", "value": mechanism, "kind": "inference"}])
rec("path-verdict", "path", "judgment", "inference", "借圈子起步，借名人引爆，按峰值扩张，再花三年修补",
    "前一年克制有效：小圈子、慢放人、创始人每周在场。2021 年 2 月名人带来的峰值之后，公司在新增已经下滑时按峰值融资和扩编；此后的产品改版都在补“凑不齐人”这一课。",
    "研究者判断", "顺序清楚，因果需要同批留存才能确认。", ["e-check", "e-tc8m", "e-sensor", "e-seriesc", "e-email"])
step("s1", "2019 秋–2020-03", "01 从播客方向转到实时语音",
     "以播客方向的 Talkshow 起步，在音频方向反复迭代后改成实时语音房 Clubhouse。", "2020-03 上线，只给朋友试用。",
     "把“录好再发”换成“现在一起聊”，价值来自同时在场。", ["e-welcome", "e-wiki"], "Talkshow 细节只有百科转述。")
step("s2", "2020-03–05", "02 在硅谷投资圈里内测，拿到 a16z",
     "早期用户集中在科技投资人和创业者；2020-05 a16z 在内测期投资。", "约 1 亿美元估值；2020-12 约 60 万注册用户。",
     "第一批用户自带话题和关注度，让小圈子一开始就有好房间。", ["e-wiki", "e-cnbc23"], "早期用户构成来自报道，没有官方统计。")
step("s3", "2020-07–2021-01", "03 有意慢放人，创始人每周在场",
     "邀请分批放人，每周三迎新、周日 Town Hall；两名全职员工。", "2021-01 一周约 200 万人来过。",
     "控制涌入速度让新人进来时房间质量还在。", ["e-check", "e-open", "e-welcome"], "慢放量的效果没有对照。")
step("s4", "2021-02", "04 名人引爆",
     "02-01 Musk 进房，扎克伯格等相继露面；多国 App Store 第一。", "两周下载 350 万→810 万；2 月下旬周活 1000 万+；服务到处崩。",
     "放大器不受控：峰值来得比基础设施和推荐能力快。", ["e-musk", "e-tc8m", "e-bi", "e-davison"], "名人对下载的贡献是报道归因。")
step("s5", "2021-03–04", "05 先把钱给供给侧",
     "Creator First 发设备和津贴，打赏全部归创作者。", "主持人留存未公开；平台没有收入。",
     "在没有证明自然供给能持续时，用补贴买供给，收入问题往后推。", ["e-creator", "e-pay"], "补贴规模未公开。")
step("s6", "2021-04", "06 在新增下滑时按峰值扩张",
     "完成 C 轮（报道估值约 40 亿美元），团队当年已扩大四倍；此前 Twitter 收购谈判停滞。", "同期月安装 2 月 960 万→3 月 270 万→4 月 92 万。",
     "扩张依据是峰值和估值，不是回访数据。", ["e-seriesc", "e-cnbc23", "e-verge", "e-sensor", "e-9to5"], "公司内部当时掌握的留存数据未知。")
step("s7", "2021-05–07", "07 开放注册、上线 Android",
     "5 月 Android，7 月取消等待名单。", "新增 1000 万人；团队 58 人；每日房间 50 万。",
     "稀缺用完，覆盖变大，但新人面对的是更难找好房间的产品。", ["e-open"], "新增为公司自报；留存未知。")
step("s8", "2020-12–2021-06", "08 大平台同时复制",
     "Twitter Spaces（2020-12 内测，2021-05 开放给 600 粉以上）、Discord Stage（2021-03）、Facebook 语音房和 Spotify Greenroom（2021-06）。", "同一形式在一个季度内被四家平台推出。",
     "形式本身没有壁垒；有现成关系网的平台一抄就能铺开。", ["e-spaces-beta", "e-spaces-600", "e-stage", "e-fb", "e-greenroom"], "复制与 Clubhouse 用户流失之间没有直接数据。")
step("s9", "2021 秋–2023-09", "09 从公开广场退回熟人圈",
     "回放剪辑（2021 秋）、私密 Houses（2022-08）、裁员过半（2023-04）、异步 Chats（2023-09）。", "使用效果全部未公开。",
     "公司自己承认问题在“找朋友”和“没时间”，对症但晚了两年。", ["e-replays", "e-houses", "e-email", "e-chats"], "改版效果无数据。")
step("s10", "2025", "10 开始收费", "推出 Plus 订阅和 Coins 付费表情。", "金额未公开。",
     "上线五年后才建立平台收入。", ["e-plus", "e-rewards", "e-subfaq"], "只证明机制存在。", kind="fact")

# 08 增长回路
rec("c-loop", "loop", "loop", "inference", "回路靠外部燃料转，核心那条边是反的",
    "正常的社交网络里人越多越好找到想聊的人；Clubhouse 里人越多，走廊越乱，好房间越难找。名人和稀缺邀请停下后，回路就转不动。",
    "研究者判断", "边的状态来自创始人说法和功能时间线，没有回路级数据。", ["e-davison", "e-email", "e-tc8m", "e-creator", "e-replays"],
    edges=[
        {"from": "邀请码", "to": "朋友加入", "mechanism": "有限邀请沿通讯录扩散，稀缺增加吸引力", "status": "有信号；开放注册后失效", "evidenceIds": ["e-wiki", "e-open"]},
        {"from": "名人房间", "to": "大量新用户", "mechanism": "想“碰到”名人的好奇心", "status": "已观察（2021-02）；不受公司控制", "evidenceIds": ["e-tc8m", "e-davison"]},
        {"from": "更多用户", "to": "更好的房间", "mechanism": "规模本应带来更多好话题", "status": "反证：CEO 说新人找不到好房间", "evidenceIds": ["e-davison", "e-seriesc"]},
        {"from": "听众", "to": "主持人", "mechanism": "听众上台、开自己的房间", "status": "未证明；供给靠补贴", "evidenceIds": ["e-creator"]},
        {"from": "一场对话", "to": "下次回来的理由", "mechanism": "关系或内容留下来", "status": "未证明；回放、私信、Houses 都是后补", "evidenceIds": ["e-open", "e-replays", "e-houses"]},
        {"from": "朋友同时在线", "to": "日常回访", "mechanism": "实时房间需要对的人同时有空", "status": "反证：疫情后变难（创始人信）", "evidenceIds": ["e-email"]}])

# 09 关键决策
def decision(i, title, text, d, evs, limitation):
    rec(i, "decisions", "decision", "inference", title, text, "复盘判断", limitation, evs, decision=d)
rec("dec-verdict", "decisions", "judgment", "inference", "最贵的一次选择是 2021 年 4 月按峰值扩张",
    "慢放人的决定让早期社区质量高；按峰值扩张和开放注册都发生在新增已经下滑、大平台已经开抄之后；转向熟人和异步方向对症，但晚了两年。",
    "研究者判断", "备选路径是研究者构造；公司当时掌握的内部数据未知。", ["e-check", "e-seriesc", "e-sensor", "e-email"])
decision("dec-slow", "2020：坚持邀请制、慢放人", "早期最对的一个选择：先保证新人进来有好房间。", dict(
    period="2020-03 至 2021-01", context="两名全职员工，服务器和社区规则都没准备好。",
    knownThen="创始人公开写明：不想一夜之间 10 倍增长，要保持社区多样、产品不崩。",
    options="实际：邀请制分批放人。备选（研究者构造）：尽早公开注册。",
    chosen="分批邀请，配每周迎新和 Town Hall。", outcome="社区质量带来口碑；邀请码有了二手市场；2021-01 一周约 200 万人。",
    tradeoff="增长慢，用户圈层窄（偏科技投资圈）。", assessment="这一步是对的：先保证新人进来有好房间，再放人。",
    falsifier="如果早期批次的留存并不比后来批次高，说明慢放量没有起作用。"), ["e-check", "e-open", "e-welcome", "e-wiki"],
    "早期批次留存没有公开，判断依据是口碑和增长，属于推断。")
decision("dec-scale", "2021-04：按峰值融资扩张", "扩张依据是峰值和估值，不是回访数据。", dict(
    period="2021-04", context="2 月峰值后服务到处崩，推荐算法跟不上；Twitter 收购谈判停滞。",
    knownThen="公司自己有下载和活跃数据（2→3 月安装降 72% 是第三方估算，公开时间不晚于 4 月）；Twitter Spaces 已在内测。",
    options="实际：C 轮约 40 亿美元估值、继续扩编。备选一（报道）：接受收购。备选二（研究者构造）：先修发现和新人体验，看回访再扩。",
    chosen="完成 C 轮，团队当年已扩到四倍，钱投向发现和创作者。",
    outcome="4 月安装 92 万；7 月 58 人，2023 年约 200 人后裁掉一半；Davison 2021 年底说“长得太快了”。",
    tradeoff="放弃了被收购的机会；组织规模先于回访证据。",
    assessment="扩张按的是峰值和估值，不是回访数据；创始人事后也承认太快。",
    falsifier="如果 2021 年 2–4 月进来的批次 90 天留存与早期批次相当，说明问题不在扩张节奏。"),
    ["e-seriesc", "e-sensor", "e-verge", "e-open", "e-cnbc23", "e-davison"], "“太快”是转引；裁员与扩张之间没有直接因果证明。")
decision("dec-open", "2021-05 至 07：Android 加开放注册", "开放带来一次新增，时机落在大平台铺开之后。", dict(
    period="2021-05 至 07", context="新增已从峰值回落约 90%；Spaces 刚向 600 粉以上账号开放。",
    knownThen="公开可知：Twitter、Discord 已上线同类功能，Facebook、Spotify 在路上。",
    options="实际：同时开放。备选（研究者构造）：保留邀请制，先在核心圈做深回访。",
    chosen="5 月 Android，7 月取消等待名单。", outcome="新增 1000 万人（公司自报）；之后没有再公布增长数据。",
    tradeoff="稀缺用完；新人体验问题被放大。", assessment="开放带来一次新增，但没有证据显示这批人留下来；时机落在大平台铺开之后。",
    falsifier="Android 批次的 30/90 天留存不低于 iOS 早期批次。"), ["e-open", "e-spaces-600", "e-stage"], "开放后的留存完全未公开。")
decision("dec-reset", "2023：裁员过半，转向熟人异步语音", "诊断对症，但晚了两年。", dict(
    period="2023-04 至 09", context="疫情后找朋友、挤时间都变难；团队协调慢。",
    knownThen="创始人信写明了需求变化；公司仍有数年资金。",
    options="实际：裁员并推出 Chats。备选（研究者构造）：维持公开房间、加强推荐；出售或关停。",
    chosen="裁员超过一半，推出异步 Chats，保留直播。", outcome="2025 年推出订阅和 Coins；使用数据未公开。",
    tradeoff="放弃公开广场的规模叙事。", assessment="诊断对症（同时在线太难），但比 2021 年的信号晚了两年。",
    falsifier="Chats 用户的周活跃天数明显高于只用直播房间的用户。"), ["e-email", "e-chats", "e-plus"], "效果没有数据。")

# 10 衰退诊断
rec("dx", "decline", "judgment", "inference", "主因是产品回路和需求消退，竞争只是加速",
    "三种解释都有证据，按现有证据排序：产品回路 ≈ 需求消退 > 竞争复制。依据是：竞争对手的独立语音应用自己也没撑住，说明是这种形式的需求在缩小，而不只是用户被抢走。",
    "有条件的排序", "没有同批留存和用户去向数据，排序可能被推翻。", ["e-davison", "e-email", "e-spotify-end", "e-stage-end", "e-hp-end"],
    fields=[
        {"label": "产品回路", "value": "CEO 承认热潮期新人找不到好房间；人越多越乱。证据：创始人原话。"},
        {"label": "需求消退", "value": "创始人信：疫情后朋友难凑齐、长对话难塞进日常。证据：公司自述。"},
        {"label": "竞争复制", "value": "Spaces 等一个季度内铺开；但 Spotify 的独立应用 2023 年关闭，Discord 也关了公开发现，只保留社区里的 Stage。复制者没有把这种形式做大。"},
        {"label": "会推翻排序的证据", "value": "若用户去向数据显示大量活跃用户转去 Spaces 继续高频使用，竞争应排第一。"}])

# 11 借鉴顺序
rec("transfer-order", "transfer", "transfer", "recommendation", "学它前一年的克制，不学 2021 年的扩张",
    "给做社交或内容产品的人：顺序是“小圈子密度 → 新人首日能找到好房间 → 回访证据 → 再补贴供给、再扩张”。Clubhouse 实际是先扩张、再补贴、最后回头修回访。",
    "迁移建议", "来自单一案例和四家对照，换成付费或企业产品时要重新判断。", ["e-check", "e-davison", "e-email", "e-stage-end"],
    fields=[
        {"label": "现在复制", "value": "邀请分批放人、创始人每周在场（迎新、Town Hall）；把“新人第一天是否找到好房间”当成第一指标。"},
        {"label": "以后复制", "value": "开放注册、扩团队：等同批 30/90 天回访稳定后再做。"},
        {"label": "谨慎借鉴", "value": "名人带来的峰值：不花钱但不受控，来之前先备好服务器和推荐能力。创作者补贴：先看有没有不靠补贴的主持人。"},
        {"label": "暂不复制", "value": "按峰值下载和估值决定团队规模。"}])

# 12 下一步调查
rec("next-plan", "next", "action", "recommendation", "下一步调查：先补留存和收入", "研究者的取证计划，不是给公司的排期。", "调查计划",
    "多数关键数据只有公司掌握，公开渠道可能拿不到。", ["e-bi", "e-plus", "e-rewards"],
    milestones=[
        {"period": "第一轮", "action": "找第三方应用数据（日活、留存曲线）和 2022–2026 年的公开采访", "owner": "研究 Agent", "observe": "是否有按批次的留存或日活趋势", "decision": "找不到就保留“未证明”，不用下载代替留存"},
        {"period": "第二轮", "action": "核对 Plus 价格、订阅量线索和 Coins 规则变化", "owner": "研究 Agent", "observe": "收入规模的数量级", "decision": "没有数量级证据就不判断能否盈利"},
        {"period": "第三轮", "action": "按新证据重排衰退诊断三种解释", "owner": "研究 Agent", "observe": "用户去向、Chats 使用", "decision": "若出现用户转去 Spaces 的证据，竞争上调"}])
rec("data-needs", "next", "contract", "recommendation", "需要的数据与口径", "外部研究拿不到内部记录，这里列清楚要什么、为什么要。", "数据约定",
    "这些字段公司从未公开，可能长期缺失。", ["e-bi", "e-sensor"],
    fields=[
        {"label": "同批留存", "value": "按加入月份（2021-01、02、05）的 30/90 天活跃；区分 iOS 与 Android。"},
        {"label": "首日激活", "value": "新用户首日进房、发言、关注人数。"},
        {"label": "主持人留存", "value": "补贴结束后主持人连续开房比例。"},
        {"label": "收入", "value": "Plus 订阅量与价格、Coins 年流水、提现给创作者的比例。"}])
rec("q-user", "next", "question", "recommendation", "给使用者的问题", "如果你借鉴 Clubhouse 是为了自己的社区或产品：你现在能直接组织的是哪一群人？最近一批新人里，有多少人在一周内回来过第二次？", "待回答",
    "没有回答时按“理解机制”交付，不替用户假设资源。", ["e-check"],
    fields=[{"label": "影响", "value": "决定借鉴顺序从“建小圈子”还是从“修首日体验”开始。"}])

# 13 横向对照
def profile(i, company, fields, evs, limitation):
    rec(i, "peers", "profile", "fact", f"{dict(spaces='Twitter Spaces', stage='Discord Stage', greenroom='Spotify Greenroom', houseparty='Houseparty')[company]} 档案",
        "比较起点和结果，不比功能。", "公开信息", limitation, evs, company=company, fields=fields)
profile("pf-spaces", "spaces", [
    {"label": "起点资产", "value": "Twitter 的关注关系和时间线入口"},
    {"label": "第一批用户", "value": "内测用户，2021-05 起所有 600 粉以上账号"},
    {"label": "结果", "value": "一个季度内铺开，至今仍是 X 的功能；独立使用数据未公开"},
    {"label": "启示", "value": "有现成听众的人才能开出好房间——这正是 Clubhouse 新人缺的"}], ["e-spaces-beta", "e-spaces-600"], "没有 Spaces 使用量和留存数据。")
profile("pf-stage", "stage", [
    {"label": "起点资产", "value": "已有的服务器社区和成员关系"},
    {"label": "第一批用户", "value": "各服务器的管理员和成员"},
    {"label": "结果", "value": "近百万社区开过 Stage；跨社区的公开发现半年后关闭"},
    {"label": "启示", "value": "语音舞台放进常回来的社区能留下，放进陌生人广场留不住"}], ["e-stage", "e-stage-end"], "社区数是累计和月度，不是同批留存。")
profile("pf-greenroom", "greenroom", [
    {"label": "起点资产", "value": "Spotify 的品牌和播客创作者；收购来的体育语音应用"},
    {"label": "第一批用户", "value": "Locker Room 老用户和受邀创作者"},
    {"label": "结果", "value": "独立应用，2022 改名 Spotify Live，2023 年关闭"},
    {"label": "启示", "value": "大平台的分发也救不了一个需要单独打开的实时语音应用"}], ["e-greenroom", "e-spotify-end"], "没有用户数；关闭原因是公司表述。")
profile("pf-houseparty", "houseparty", [
    {"label": "起点资产", "value": "已有的视频群聊产品，2019 年被 Epic 收购"},
    {"label": "第一批用户", "value": "疫情封城时的年轻用户（一个月 5000 万注册）"},
    {"label": "结果", "value": "2021-10 关闭，团队并入 Epic"},
    {"label": "启示", "value": "同样借疫情时机爆发，窗口过去后没有找到日常理由"}], ["e-hp-up", "e-hp-end"], "关闭也受 Epic 战略影响。")
rec("cmp-verdict", "peers", "judgment", "inference", "同一种直播语音，放进已有关系里才留得下",
    "Spaces 借关注关系一铺就开，Discord 把它放进已有社区保留下来；需要用户单独打开的独立应用——Greenroom、Houseparty——都关了。Clubhouse 是独立应用，所以它后来要自己去建熟人圈。",
    "研究者判断", "四家的留存都没有公开数据；结论依据是存续与关闭。", ["e-spaces-600", "e-stage-end", "e-spotify-end", "e-hp-end"], company=None)
rec("cmp-matrix", "peers", "comparison", "inference", "起点资产与结局", "同字段比较。", "研究者整理",
    "结局受母公司战略影响，不能只用产品解释。", ["e-spaces-600", "e-stage-end", "e-spotify-end", "e-hp-end"], company=None,
    comparisonIds=["pf-spaces", "pf-stage", "pf-greenroom", "pf-houseparty"], columns=["起点资产", "第一批用户", "结果", "启示"])
for c, title, text, evs in [
    ("spaces", "Spaces：把主持权先给有听众的人", "只向 600 粉以上账号开放主持，理由是他们已有听众。", ["e-spaces-600"]),
    ("stage", "Stage：留在社区里，砍掉公开发现", "近百万社区用过，公开发现试点半年后关闭。", ["e-stage-end"]),
    ("greenroom", "Greenroom：收购改版，两年后关闭", "独立应用“不再合理”，转到主应用里试听歌派对。", ["e-spotify-end"]),
    ("houseparty", "Houseparty：疫情爆发，窗口后关闭", "一个月 5000 万注册，2021-10 关闭。", ["e-hp-up", "e-hp-end"])]:
    rec(f"{c}-key", "peers", "step", "fact", title, text, "关键动作", "单一动作，不代表完整路径。", evs, company=c, stage="2020–2023",
        fields=[{"label": "动作", "value": text}])
rec("tradeoff", "path", "tradeoff", "inference", "取舍：推迟收入，换增长和供给", "2021 年打赏全给创作者、不做广告和订阅；收入到 2025 年才出现。公开材料里没有公司说明不做收入的理由，这里是研究者从动作推出的取舍。",
    "研究者推断", "可能也有其他原因（例如先做规模再变现的融资逻辑），公开资料没有说明。", ["e-pay", "e-cnbc23", "e-plus"])

sections = [
    ("exec", "执行结论", "verdict", ["verdict", "m-revenue"],
     "Clubhouse 证明了实时语音房能在几周内吸引上千万人，没有证明人们会每天回来。",
     "最大的缺口是同批留存和收入金额；两者公司都没公开。", ["e-bi", "e-sensor", "e-davison", "e-plus"]),
    ("status", "Clubhouse 现状：证明到哪一步", "verdict", ["p-activation", "p-cohort", "p-revisit", "p-content", "p-creator", "p-monetize"],
     "注意力已证明，习惯被反证：激活和回访都有创始人自己的反面说法，变现 2025 年才有信号。",
     "六个命题没有一个达到“已证明”；最硬的证据恰恰是两条反证。", ["e-davison", "e-email", "e-plus"]),
    ("products", "产品形态演变", "assets", ["a-products", "a-portfolio"],
     "三年换了三次形态，都在解决同一个问题：凑不齐想聊的人。",
     "只有最初的公开房间有规模证据；后面的改版方向对，效果未知。", ["e-houses", "e-chats"]),
    ("channels", "获客渠道", "assets", ["a-channels"],
     "增长几乎零成本，但靠的是稀缺和名人，两样都不归公司控制。",
     "开放注册后没有留下任何一个公司能持续加码的渠道。", ["e-tc8m", "e-open"]),
    ("assets-map", "起步资产", "assets", ["a-assets"],
     "起步资产大多是借来的，会过期；创始人在前一个产品里已经撞过“密度”这堵墙。",
     "能持续的只有经验和资金，而它们解决不了“对的人同时在线”。", ["e-highlight", "e-email"]),
    ("team-map", "团队与组织规模", "assets", ["team"],
     "团队规模跟着热度走：半年从 8 人到 58 人，两年后约 200 人再砍一半。",
     "组织按峰值扩张，是 2021 年最贵的一个决定的直接体现。", ["e-open", "e-cnbc23"]),
    ("path", "自身 0→1 路径", "assets", ["path-verdict", "s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8", "s9", "s10"],
     "借圈子起步，借名人引爆，在新增下滑时按峰值扩张，再花三年修补。",
     "前一年的克制是对的；从第 6 步开始，扩张跑在了回访证据前面。", ["e-check", "e-sensor", "e-seriesc"]),
    ("loop", "增长回路", "assets", ["c-loop"],
     "回路靠外部燃料转，“人越多房间越好”这条边是反的。",
     "这更像一条要不断补充名人和新用户的直线，不是飞轮。", ["e-davison"]),
    ("decisions", "关键决策复盘", "decisions", ["dec-verdict", "dec-slow", "dec-scale", "dec-open", "dec-reset"],
     "最贵的一次是 2021 年 4 月按峰值扩张；最对的一次是 2020 年慢放人。",
     "后两次选择都比信号晚一步：开放在大平台铺开之后，转向在需求消退两年之后。", ["e-check", "e-seriesc", "e-email"]),
    ("decline", "衰退诊断", "decisions", ["dx"],
     "主因是产品回路和需求消退，竞争只是加速。",
     "复制者的独立应用自己也没撑住，说明是这种形式的需求在缩小。", ["e-spotify-end", "e-stage-end"]),
    ("transfer", "借鉴顺序", "choices", ["transfer-order"],
     "学它前一年的克制，不学 2021 年的扩张。",
     "先证明新人第一天能找到好房间、一周后会回来，再谈开放和补贴。", ["e-check", "e-davison"]),
    ("next", "下一步调查", "validation", ["next-plan", "data-needs", "q-user"],
     "公开资料拿不到留存和收入，下一步先补这两项。",
     "拿到同批留存后，“激活”和“回访”的反证可能升级为直接数据，也可能被推翻。", ["e-bi", "e-plus"]),
    ("peers", "横向对照", "paths", ["cmp-verdict", "cmp-matrix"],
     "同一种直播语音，放进已有关系里才留得下。",
     "独立应用都关了；Clubhouse 活下来的方式是自己去建熟人圈。", ["e-spaces-600", "e-stage-end", "e-spotify-end", "e-hp-end"]),
]
S = [dict(id=i, title=t, part=p, overviewIds=o, thesis=th, conclusion=co, evidenceIds=e) for i, t, p, o, th, co, e in sections]

topics = [
    dict(id="audit", title="数据核验", parentSectionId="status", verdictId="verdict", argument=["指标口径", "序列", "证明边界"],
         modules=[
             dict(id="au-metrics", title="01 每个数字是谁说的", recordIds=["m-wau", "m-installs", "m-revenue"],
                  thesis="周活是公司口径，下载是第三方估算，收入从未披露。", conclusion="三种口径不能互相换算。"),
             dict(id="au-series", title="02 下载与周活怎么变", recordIds=["ser-installs", "ser-wau"],
                  thesis="2 月同时是下载峰值和周活峰值，之后公司不再公布周活。", conclusion="能看到爆发和回落，看不到留存。"),
             dict(id="au-proof", title="03 六个命题各证明到哪", recordIds=["p-activation", "p-cohort", "p-revisit", "p-content", "p-creator", "p-monetize"],
                  thesis="两条反证都来自创始人自己。", conclusion="同批留存是决定性缺口。")]),
    dict(id="path-detail", title="自身路径拆解", parentSectionId="path", verdictId="path-verdict", argument=["互补资产", "首次交付", "取舍", "回路与迁移"],
         modules=[
             dict(id="pd-assets", title="01 互补起点资产", recordIds=["a-assets", "team"],
                  thesis="投资人圈提供第一批好房间，疫情提供同时在线的时间。", conclusion="两样都会过期。"),
             dict(id="pd-first", title="02 首次交付与验证", recordIds=["s2", "s3", "dec-slow"],
                  thesis="靠慢放人和创始人在场保证新人进来有好房间。", conclusion="这是 Clubhouse 唯一被验证有效的增长方式。"),
             dict(id="pd-tradeoff", title="03 取舍", recordIds=["tradeoff", "s5", "dec-scale"],
                  thesis="推迟收入、补贴供给、按峰值扩张。", conclusion="三个取舍都押注规模会自己带来留存。"),
             dict(id="pd-loop", title="04 回路与迁移", recordIds=["c-loop", "transfer-order"],
                  thesis="核心边是反的，所以要先修密度再放量。", conclusion="可迁移的是前一年的顺序。")]),
    dict(id="comparisons", title="四家对标", parentSectionId="peers", verdictId="cmp-verdict", argument=["已有关系", "社区内", "独立应用", "时机型"],
         modules=[
             dict(id="cp-spaces", title="01 Twitter Spaces", recordIds=["pf-spaces", "spaces-key"], thesis="关注关系就是现成的听众。", conclusion="分发解决了新人没听众的问题。"),
             dict(id="cp-stage", title="02 Discord Stage", recordIds=["pf-stage", "stage-key"], thesis="社区内留下，公开发现关闭。", conclusion="陌生人广场是最难的场景。"),
             dict(id="cp-greenroom", title="03 Spotify Greenroom", recordIds=["pf-greenroom", "greenroom-key"], thesis="大平台做独立应用也关了。", conclusion="需求在缩小，不只是被抢。"),
             dict(id="cp-houseparty", title="04 Houseparty", recordIds=["pf-houseparty", "houseparty-key"], thesis="同样借疫情爆发。", conclusion="时机资产会过期。")]),
]
rec("ser-installs", "status", "series", "fact", "全球月安装（第三方估算）", "Sensor Tower 估算；4 月为媒体转述。", "第三方估算",
    "衡量新增，不追踪同一批人。", ["e-sensor", "e-9to5"],
    series=dict(unit="万次／月", definition="Clubhouse 全球月安装估算", points=[
        dict(period="2021-01", value=240, basis="Sensor Tower", evidenceIds=["e-sensor"]),
        dict(period="2021-02", value=960, basis="Sensor Tower", evidenceIds=["e-sensor"]),
        dict(period="2021-03", value=270, basis="Sensor Tower", evidenceIds=["e-sensor"]),
        dict(period="2021-04", value=92.2, basis="Sensor Tower，经 9to5Mac 转述", evidenceIds=["e-9to5"]),
        dict(period="2021-05 以后", value=None, basis="同一测量方", evidenceIds=["e-sensor"], missingReason="本次没有找到同一测量方的后续月度公开数据")]))
rec("ser-wau", "status", "series", "fact", "周活跃用户（公司口径）", "公司只公布过两次。", "公司口径",
    "两次口径可能不同（“来过”与“活跃”）。", ["e-welcome", "e-bi"],
    series=dict(unit="万人／周", definition="公司公布的每周活跃或到访人数", points=[
        dict(period="2021-01", value=200, basis="B 轮公告：过去一周来过", evidenceIds=["e-welcome"]),
        dict(period="2021-02 下旬", value=1000, basis="公司所说每周活跃超过 1000 万（转述）", evidenceIds=["e-bi"]),
        dict(period="2021-03 以后", value=None, basis="—", evidenceIds=["e-bi"], missingReason="公司此后不再公布")]))

data = dict(
    meta=dict(taskType="external-company", title="Clubhouse：爆红之后为什么留不住人",
              question="Clubhouse 靠什么起步、为什么没把注意力变成习惯、哪些做法值得借鉴？", asOf=ACC,
              scope="2019 年 Talkshow 至 2026-10；外部公开资料；对照 Twitter Spaces、Discord Stage、Spotify Greenroom、Houseparty。",
              notice="外部公司研究：数字来自公司口径、第三方估算和媒体报道，未经审计；同批留存和收入金额从未公开。研究目的暂按“理解机制与借鉴经验”。",
              verdictId="verdict", keyMetricIds=["m-wau", "m-installs", "m-revenue"], subjectCompanyId="clubhouse", actionSectionId="next"),
    companies=[dict(id="clubhouse", name="Clubhouse", period="2019–2026"),
               dict(id="spaces", name="Twitter Spaces", period="2020-12–2021"),
               dict(id="stage", name="Discord Stage", period="2021"),
               dict(id="greenroom", name="Spotify Greenroom", period="2021–2023"),
               dict(id="houseparty", name="Houseparty", period="2020–2021")],
    sections=S, topics=topics, records=R, evidence=E)
json.dump(data, open(sys.argv[1], "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("records", len(R), "evidence", len(E), "sections", len(S))
