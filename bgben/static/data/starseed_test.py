import json, io


starseedQuestions = {
  "zh": { 
    "testA": [
    {
      "text": "以下内容，您最感兴趣的是什么？",
      "answers": [
        { "answer": "大自然", "score": 3.3 },
        { "answer": "宇宙", "score": 9.9 },
        { "answer": "各种声音", "score": 7.7 },
        { "answer": "古代遗迹", "score": 5.5 },
      ]
    },
    {
      "text": "您喜欢与谁一起度过休闲时间？",
      "answers": [
        { "answer": "与家人度过", "score": 5.5 },
        { "answer": "与朋友社交", "score": 3.3 },
        { "answer": "与自己独处", "score": 9.9 },
        { "answer": "与动物玩耍", "score": 7.7 },
      ]
    },
    {
      "text": "您有没有前世的记忆？",
      "answers": [
        { "answer": "没有，完全没有", "score": 3.3 },
        { "answer": "有，而且记得很多次投生的经历", "score": 9.9 },
        { "answer": "没有，但经常有与现实生活不同的清醒梦", "score": 5.5 },
        { "answer": "有上辈子的记忆，其他不知道", "score": 7.7 },
      ]
    },
    {
      "text": "您对以下哪一种存在最感兴趣？",
      "answers": [
        { "answer": "外星人", "score": 7.7 },
        { "answer": "地心人", "score": 5.5 },
        { "answer": "地球智人（人类）", "score": 3.3 },
        { "answer": "不同维度的存在", "score": 9.9 },
      ]
    },
    {
      "text": "以下情况，您对什么最在意？",
      "answers": [
        { "answer": "社会对您的评价", "score": 3.3 },
        { "answer": "朋友对您的评价", "score": 5.5 },
        { "answer": "您自己对自己的评价", "score": 9.9 },
        { "answer": "家人对您的评价", "score": 7.7 },
      ]
    },
    {
      "text": "您(希望)‘另一半’扮演的是什么角色？",
      "answers": [
        { "answer": "一起探讨宇宙的灵魂伴侣", "score": 9.9 },
        { "answer": "一起传承灯火的合作伙伴", "score": 5.5 },
        { "answer": "一起欢度生活的搭档", "score": 7.7 },
        { "answer": "分享柴米油盐的室友", "score": 3.3 },
      ]
    },
    {
      "text": "您看到过UFO吗？",
      "answers": [
        { "answer": "有，经常看到", "score": 9.9 },
        { "answer": "没有，从来都没有看到过", "score": 3.3 },
        { "answer": "有，但很少，只有一两次", "score": 7.7 },
        { "answer": "不确定，也许那次看到的就是…", "score": 5.5 },
      ]
    },
    {
      "text": "您每天必须要做的最重要的是哪一件事？",
      "answers": [
        { "answer": "写日记", "score": 7.7 },
        { "answer": "打坐冥想", "score": 9.9 },
        { "answer": "运动健身", "score": 5.5 },
        { "answer": "以上都不是", "score": 3.3 },
      ]
    },
    {
      "text": "您有没有以下特异功能？",
      "answers": [
        { "answer": "透视/通灵", "score": 9.9 },
        { "answer": "悬浮", "score": 5.5 },
        { "answer": "瞬间移动", "score": 7.7 },
        { "answer": "以上都没有", "score": 3.3 },
      ]
    },
    {
      "text": "您有没有经历过任何‘上帝/命中安排’的往事？",
      "answers": [
        { "answer": "有，至少有一次", "score": 7.7 },
        { "answer": "应该有，但是不确定", "score": 5.5 },
        { "answer": "没有，从来都没有", "score": 3.3 },
        { "answer": "有，经常有，太神奇了", "score": 9.9 },
      ]
    },
  ],
    "testB": [
    {
      "text": "您是否容易感觉到各种压力？",
      "answers": [
        { "answer": "总是会，而且身体也受影响", "score": 9.9 },
        { "answer": "不太会，除非有重大事件发生", "score": 5.5 },
        { "answer": "经常有，但是不会太严重", "score": 7.7 },
        { "answer": "不会，我很抗压", "score": 3.3 },
      ]
    },
    {
      "text": "您对宇宙话题的兴趣点是什么？",
      "answers": [
        { "answer": "我们是孤独的吗？外星人的那些事…", "score": 5.5 },
        { "answer": "宇宙的物理科学", "score": 3.3 },
        { "answer": "我的故乡在哪里？", "score": 9.9 },
        { "answer": "平行宇宙、时间线、暗物质的真相", "score": 7.7 },
      ]
    },
    {
      "text": "您有灵感吗？",
      "answers": [
        { "answer": "我的第六感从小就很灵光", "score": 9.9 },
        { "answer": "偶尔会发现梦中的情景成为了现实", "score": 7.7 },
        { "answer": "目睹过别人的第六感，但自己没有", "score": 5.5 },
        { "answer": "不相信有什么第六感", "score": 3.3 },
      ]
    },
    {
      "text": "您的人生是否充满着坎坷不平的经历？",
      "answers": [
        { "answer": "一直都是，但是我还是很乐观", "score": 9.9 },
        { "answer": "还好，至今我基本都比较幸运", "score": 3.3 },
        { "answer": "有一段时间是，但是后来我成功了", "score": 5.5 },
        { "answer": "一直都充满着坎坷…", "score": 7.7 },
      ]
    },
    {
      "text": "您有耳鸣吗？",
      "answers": [
        { "answer": "没有，最多也就是偶尔听到短暂的", "score": 3.3 },
        { "answer": "不断有一种高频的声音在耳边响", "score": 9.9 },
        { "answer": "一直都听到低频的嗡嗡声", "score": 5.5 },
        { "answer": "经常会听到，但不是一直持续的那种", "score": 7.7 },
      ]
    },
    {
      "text": "您会感到孤独吗？",
      "answers": [
        { "answer": "不会，总是有人在身边陪伴", "score": 3.3 },
        { "answer": "一个人的时候经常会感到孤独", "score": 5.5 },
        { "answer": "与别人在一起的时候也会感到孤独", "score": 7.7 },
        { "answer": "我喜欢孤独", "score": 9.9 },
      ]
    },
    {
      "text": "您的身上有没有明显的胎记或痣？",
      "answers": [
        { "answer": "有，在脸上就有一处很明显的胎记", "score": 7.7 },
        { "answer": "有，在一般别人看不到的地方", "score": 5.5 },
        { "answer": "没有，我的皮肤很完美", "score": 3.3 },
        { "answer": "有，不止一处，都很明显", "score": 9.9 },
      ]
    },
    {
      "text": "您从事的职业与哪一类最接近？",
      "answers": [
        { "answer": "会计师、律师、医生、教师", "score": 3.3 },
        { "answer": "艺术家、设计师、作家", "score": 7.7 },
        { "answer": "文职、公共、服务·生产行业", "score": 5.5 },
        { "answer": "自由职业", "score": 9.9 },
      ]
    },
    {
      "text": "您在别人眼中看上去与实际年龄的相比是？",
      "answers": [
        { "answer": "基本上比实际年龄看上去要年轻", "score": 9.9 },
        { "answer": "基本与实际年龄相应", "score": 5.5 },
        { "answer": "比实际年龄看上去年长", "score": 3.3 },
        { "answer": "根据年龄段有过不同的变化", "score": 7.7 },
      ]
    },
    {
      "text": "您对别人说的话和态度是否会有敏感的感受？",
      "answers": [
        { "answer": "有，经常会察觉到对方的真正用意", "score": 7.7 },
        { "answer": "我基本不在乎别人的言行", "score": 5.5 },
        { "answer": "我都按字面说的去理解对方的意思", "score": 3.3 },
        { "answer": "我连对方的潜意识都能看到", "score": 9.9 },
      ]
    },
  ],
    "testC": [
    {
      "text": "您对金钱的看法是什么？",
      "answers": [
        { "answer": "为了满足温饱的工具而已", "score": 5.5 },
        { "answer": "人类邪恶部分的根源", "score": 7.7 },
        { "answer": "陌生或不理解的概念，为什么需要金钱？", "score": 9.9 },
        { "answer": "为了达到目的是不可缺的东西", "score": 3.3 },
      ]
    },
    {
      "text": "您能看到别人的光轮吗？",
      "answers": [
        { "answer": "可以，而且还能看到不同颜色", "score": 7.7 },
        { "answer": "不止是光轮，还能判断其含义", "score": 9.9 },
        { "answer": "什么是光轮？", "score": 3.3 },
        { "answer": "我正在练习此技能", "score": 5.5 },
      ]
    },
    {
      "text": "别人经常说您：",
      "answers": [
        { "answer": "对事物非常敏感", "score": 9.9 },
        { "answer": "比较迟钝，后知后觉", "score": 3.3 },
        { "answer": "做事情一丝不苟", "score": 5.5 },
        { "answer": "对待事物不会斤斤计较", "score": 7.7 },
      ]
    },
    {
      "text": "以下的词语中，您最认同的是？",
      "answers": [
        { "answer": "自由、热情、成功", "score": 7.7 },
        { "answer": "奉献、喜悦、和谐", "score": 9.9 },
        { "answer": "富裕、尊严、荣华", "score": 3.3 },
        { "answer": "美丽、俊俏、气质", "score": 5.5 },
      ]
    },
    {
      "text": "您对昂贵的东西感兴趣吗？",
      "answers": [
        { "answer": "取决于是否是货真价实的东西", "score": 5.5 },
        { "answer": "价格很重要吗？", "score": 9.9 },
        { "answer": "就算我有很多钱也不会感兴趣", "score": 7.7 },
        { "answer": "有，如果我是富豪的话", "score": 3.3 },
      ]
    },
    {
      "text": "您对法律、规则等的约束有什么感受？",
      "answers": [
        { "answer": "无论内容如何，只要遵守不犯错就好", "score": 5.5 },
        { "answer": "不认同很多内容，但也无奈", "score": 7.7 },
        { "answer": "为什么人类需要用规则来管理？", "score": 9.9 },
        { "answer": "人性的邪恶只能用规则来约束", "score": 3.3 },
      ]
    },
    {
      "text": "您对周围的圈子、人类社会感到归属感吗？",
      "answers": [
        { "answer": "基本有，我是社会的一份子", "score": 3.3 },
        { "answer": "仅对特定的圈子感到归属感", "score": 5.5 },
        { "answer": "没有，我感觉自己不属于人类", "score": 7.7 },
        { "answer": "我已知道自己的归属不是地球人类", "score": 9.9 },
      ]
    },
    {
      "text": "您能理解动物的语言吗？",
      "answers": [
        { "answer": "我能理解伴侣动物想说什么", "score": 5.5 },
        { "answer": "我对与自己伴侣动物同类的动物比较了解", "score": 7.7 },
        { "answer": "我普遍能够察觉到动植物的意识", "score": 9.9 },
        { "answer": "我完全不明白它们想说什么", "score": 3.3 },
      ]
    },
    {
      "text": "您有孩子吗？",
      "answers": [
        { "answer": "目前还没有，但是打算成为父母", "score": 5.5 },
        { "answer": "有", "score": 3.3 },
        { "answer": "没有，本来就没有打算，但我喜欢小朋友的", "score": 9.9 },
        { "answer": "我更喜欢伴侣动物", "score": 7.7 },
      ]
    },
    {
      "text": "您善于看出别人的···",
      "answers": [
        { "answer": "短处", "score": 3.3 },
        { "answer": "长处", "score": 9.9 },
        { "answer": "秘密", "score": 7.7 },
        { "answer": "年龄", "score": 5.5 },
      ]
    }
  ],
    "testD": [
    {
      "text": "您觉得人活在这个世界上的真正目的是？",
      "answers": [
        { "answer": "学习", "score": 9.9 },
        { "answer": "服刑", "score": 7.7 },
        { "answer": "传承", "score": 5.5 },
        { "answer": "不知道，没好好思考过", "score": 3.3 },
      ]
    },
      {
      "text": "地球是一个怎样的星球？",
      "answers": [
        { "answer": "学校", "score": 7.7 },
        { "answer": "幻觉", "score": 9.9 },
        { "answer": "乐园", "score": 3.3 },
        { "answer": "监狱", "score": 5.5 },
      ]
    },
    {
      "text": "您的信仰与哪一种描述最接近？",
      "answers": [
        { "answer": "我的信仰基于某种意识形态", "score": 3.3 },
        { "answer": "我的信仰基础是科学", "score": 5.5 },
        { "answer": "我的信仰直通造物主", "score": 9.9 },
        { "answer": "我的信仰以某宗教代表", "score": 7.7 },
      ]
    },
    {
      "text": "您最善于用哪一种方式表达自己？",
      "answers": [
        { "answer": "语言（说、写）", "score": 3.3 },
        { "answer": "表情（喜怒哀乐）", "score": 5.5 },
        { "answer": "某一种具体的行为", "score": 7.7 },
        { "answer": "通过心灵感应", "score": 9.9 },
      ]
    },
    {
      "text": "您对结婚感兴趣吗？",
      "answers": [
        { "answer": "一直都很向往 / 已婚很满足", "score": 5.5 },
        { "answer": "只有来自周围的压力 / 已婚但不幸福", "score": 3.3 },
        { "answer": "无论别人怎么想，从来都不觉得适合自己", "score": 9.9 },
        { "answer": "一旦真正爱上了谁才会考虑", "score": 7.7 },
      ]
    },
    {
      "text": "您喜欢成为引人注目的对象吗？",
      "answers": [
        { "answer": "很喜欢，我的梦想就是成为公众人物", "score": 3.3 },
        { "answer": "非常不喜欢，我宁愿成为空气", "score": 9.9 },
        { "answer": "我只喜欢在自己的朋友圈里摆弄一下", "score": 5.5 },
        { "answer": "我不太在意，随缘", "score": 7.7 },
      ]
    },
    {
      "text": "您每天的平均睡眠时间是？",
      "answers": [
        { "answer": "4小时以下", "score": 3.3 },
        { "answer": "6小时左右", "score": 5.5 },
        { "answer": "8小时左右", "score": 7.7 },
        { "answer": "9小时以上", "score": 9.9 },
      ]
    },
    {
      "text": "如果您要面临与别人竞争或对抗的情况，您会：",
      "answers": [
        { "answer": "不理解为何会有这种情况或概念", "score": 9.9 },
        { "answer": "我没有信心，还是放手认输吧", "score": 5.5 },
        { "answer": "试图和解，与对方和平相处", "score": 7.7 },
        { "answer": "将对抗进行到底，绝不认输", "score": 3.3 },
      ]
    },
    {
      "text": "您对金钱最大的感受是？",
      "answers": [
        { "answer": "绝大部分问题的根源", "score": 9.9 },
        { "answer": "解决自己各种欲望的方法", "score": 5.5 },
        { "answer": "解决人类问题的工具", "score": 3.3 },
        { "answer": "不是我自己要去担心的东西", "score": 7.7 },
      ]
    },
    {
      "text": "您对‘为他人奉献’是什么看法？",
      "answers": [
        { "answer": "只要不影响到自己的利益，是值得的", "score": 7.7 },
        { "answer": "哪怕自己吃亏，也要坚持为他人造福", "score": 9.9 },
        { "answer": "没什么意义，也没兴趣去作秀", "score": 3.3 },
        { "answer": "为了自己的声誉，值得去做", "score": 5.5 },
      ]
    }
  ],
    "testE": [
    {
      "text": "小说或电影，您容易对剧情产生共鸣吗？",
      "answers": [
        { "answer": "我就当作虚构的故事来看，不会入戏太深", "score": 5.5 },
        { "answer": "我非常容易‘泪失禁’", "score": 9.9 },
        { "answer": "仅对与我经历相似的剧情深感共鸣", "score": 7.7 },
        { "answer": "就算是真的故事，我也没什么感觉", "score": 3.3 },
      ]
    },
      {
      "text": "您对哪些话题最感兴趣？",
      "answers": [
        { "answer": "宇宙、灵性、哲学、宗教", "score": 9.9 },
        { "answer": "科学技术", "score": 7.7 },
        { "answer": "娱乐八卦、人际关系", "score": 5.5 },
        { "answer": "金融理财、财米油盐", "score": 3.3 },
      ]
    },
    {
      "text": "别人对您的评价中，最多的是：",
      "answers": [
        { "answer": "善于与别人打成一片", "score": 3.3 },
        { "answer": "成功、精英人士", "score": 5.5 },
        { "answer": "神秘寡言，不合群", "score": 7.7 },
        { "answer": "比实际年龄更加成熟", "score": 9.9 },
      ]
    },
    {
      "text": "周末休息时，您最喜欢做些什么？",
      "answers": [
        { "answer": "一个人阅读、冥想、思考等等···", "score": 9.9 },
        { "answer": "逛街、社交派对、游玩等", "score": 3.3 },
        { "answer": "与另一半或家人温馨度过", "score": 5.5 },
        { "answer": "与伴侣动物、大自然亲近", "score": 7.7 },
      ]
    },
    {
      "text": "您认为社会上的普世价值观是：",
      "answers": [
        { "answer": "建立在绝大部分人利益上的价值观", "score": 3.3 },
        { "answer": "具体不知如何指点，但不敢苟同", "score": 5.5 },
        { "answer": "建立在谎言上的虚构叙述", "score": 7.7 },
        { "answer": "基本上是地球监狱的行动规范", "score": 9.9 },
      ]
    },
    {
      "text": "您认为第六感或‘灵感’真的存在吗？",
      "answers": [
        { "answer": "我只相信五感，其他一切都纯属偶然", "score": 3.3 },
        { "answer": "我确信自己的第六感是千真万确的", "score": 7.7 },
        { "answer": "半信半疑，但看到过别人确实说准了很多事", "score": 5.5 },
        { "answer": "我知道第六感是什么，没什么稀奇的", "score": 9.9 },
      ]
    },
    {
      "text": "人类社会中，您认为最荒谬的是什么？",
      "answers": [
        { "answer": "自以为是宇宙唯一的存在", "score": 7.7 },
        { "answer": "唯物主义·唯科学主义", "score": 9.9 },
        { "answer": "贫富差距", "score": 5.5 },
        { "answer": "宗教对立", "score": 3.3 },
      ]
    },
    {
      "text": "您会莫名其妙感到一种寂寞感吗？为什么？",
      "answers": [
        { "answer": "会，无法完全信任任何人", "score": 7.7 },
        { "answer": "会，经常会望着天空感到一种乡愁", "score": 9.9 },
        { "answer": "不会，我周围一直都有人陪伴", "score": 3.3 },
        { "answer": "我知道如何面对孤独", "score": 5.5 },
      ]
    },
    {
      "text": "您对工作的定义是？",
      "answers": [
        { "answer": "给别人带来喜悦", "score": 9.9 },
        { "answer": "为生活奔波", "score": 3.3 },
        { "answer": "做喜欢的事情", "score": 5.5 },
        { "answer": "人生的事业", "score": 7.7 },
      ]
    },
      {
      "text": "您的烦恼主要属于来自哪一种原因？",
      "answers": [
        { "answer": "物质生活", "score": 3.3 },
        { "answer": "人际关系", "score": 5.5 },
        { "answer": "人生的使命感", "score": 9.9 },
        { "answer": "各种社会问题", "score": 7.7 },
      ]
    },
  ],
  },
  'ja': { 
    "testA": [
    {
      "text": "次のうち最も興味があるのは?",
      "answers": [
        { "answer": "大自然", "score": 3.3 },
        { "answer": "宇宙", "score": 9.9 },
        { "answer": "様々な音色", "score": 7.7 },
        { "answer": "古代遺跡", "score": 5.5 },
      ]
    },
    {
      "text": "休暇は誰と一緒に過ごすのがお好きですか?",
      "answers": [
        { "answer": "家族と過ごす", "score": 5.5 },
        { "answer": "友人たちと過ごす", "score": 3.3 },
        { "answer": "自分一人で楽しむ", "score": 9.9 },
        { "answer": "動物たちと戯れる", "score": 7.7 },
      ]
    },
    {
      "text": "前世の記憶はありますか？",
      "answers": [
        { "answer": "全くありません", "score": 3.3 },
        { "answer": "はい、多くの輪廻体験を覚えています", "score": 9.9 },
        { "answer": "無いけど、現実とは異なる明晰夢はよく見る", "score": 5.5 },
        { "answer": "前世の記憶はあるが、それ以外は何も...", "score": 7.7 },
      ]
    },
    {
      "text": "次のうち、最も興味を抱くのはどの「存在」ですか?",
      "answers": [
        { "answer": "異星人", "score": 7.7 },
        { "answer": "地底人", "score": 5.5 },
        { "answer": "ホモ・サピエンス", "score": 3.3 },
        { "answer": "他の次元の存在（意識）", "score": 9.9 },
      ]
    },
    {
      "text": "次のうち、最も気にしているのは?",
      "answers": [
        { "answer": "自分の社会的評価", "score": 3.3 },
        { "answer": "友人たちの目に映る自分", "score": 5.5 },
        { "answer": "自分が評価する自分", "score": 9.9 },
        { "answer": "家族にどう見られているか", "score": 7.7 },
      ]
    },
    {
      "text": "あなたはパートナーにどのような役割を求めますか？",
      "answers": [
        { "answer": "宇宙を一緒に探索するソウルメイト", "score": 9.9 },
        { "answer": "共に血筋を守る人生のパートナー", "score": 5.5 },
        { "answer": "一緒に生活をエンジョイする相方", "score": 7.7 },
        { "answer": "共に困難を生き抜いてゆくルームメイト", "score": 3.3 },
      ]
    },
    {
      "text": "UFOを見たことはありますか？",
      "answers": [
        { "answer": "よく見かけることがある", "score": 9.9 },
        { "answer": "一度も見たことがない", "score": 3.3 },
        { "answer": "あるけど、せいぜい１、2回ほどかな", "score": 7.7 },
        { "answer": "どうかな、あの時見たのがUFOだったかも", "score": 5.5 },
      ]
    },
    {
      "text": "次のうち、あなたの最も重要視している日課は?",
      "answers": [
        { "answer": "日記を書く", "score": 7.7 },
        { "answer": "瞑想する", "score": 9.9 },
        { "answer": "運動する", "score": 5.5 },
        { "answer": "上記いずれでもない", "score": 3.3 },
      ]
    },
    {
      "text": "次のような超能力をお持ちですか？",
      "answers": [
        { "answer": "遠隔透視・霊能力", "score": 9.9 },
        { "answer": "空中浮揚", "score": 5.5 },
        { "answer": "テレポーテーション", "score": 7.7 },
        { "answer": "上記のいずれでもない", "score": 3.3 },
      ]
    },
    {
      "text": "過去に神様・運命の体験をしたことはありますか？",
      "answers": [
        { "answer": "はい、少なくとも一度は", "score": 7.7 },
        { "answer": "あるかも、でも確かではない", "score": 5.5 },
        { "answer": "一度もない", "score": 3.3 },
        { "answer": "何度もあるよ", "score": 9.9 },
      ]
    },
  ],
    "testB": [
    {
      "text": "あなたはストレスを感じやすいですか？",
      "answers": [
        { "answer": "はい、そのせいでよく体調不良に...", "score": 9.9 },
        { "answer": "度合いにもよるかな、大きいストレスには弱い", "score": 5.5 },
        { "answer": "よく感じるが、大事には至らない", "score": 7.7 },
        { "answer": "ストレスなんか全然へっちゃらさ", "score": 3.3 },
      ]
    },
    {
      "text": "次のうち、宇宙についてどのテーマに興味がありますか?",
      "answers": [
        { "answer": "エイリアンは存在するのかどうか", "score": 5.5 },
        { "answer": "宇宙に関する物理科学", "score": 3.3 },
        { "answer": "自分の故郷がいったいどこにあるのか", "score": 9.9 },
        { "answer": "並行宇宙、時間軸、暗黒物質などについて", "score": 7.7 },
      ]
    },
    {
      "text": "霊能力をお持ちですか？",
      "answers": [
        { "answer": "子供の頃から第六感が冴えていた", "score": 9.9 },
        { "answer": "時折、夢で見た光景が現実化することがある", "score": 7.7 },
        { "answer": "他人の霊能力を目撃したことがあるが、自分にはない", "score": 5.5 },
        { "answer": "そんな迷信は信じないね", "score": 3.3 },
      ]
    },
    {
      "text": "あなたの人生は波瀾万丈ですか？",
      "answers": [
        { "answer": "ずーっと怒涛の如く大変だったけど、いつも至って楽天的よ", "score": 9.9 },
        { "answer": "どうかな、今ままでの人生は比較的ラッキーだったと思う", "score": 3.3 },
        { "answer": "一時期はどん底だったけど、その後持ち直したよ", "score": 5.5 },
        { "answer": "ずっと試練だらけの人生よ・・・クスン", "score": 7.7 },
      ]
    },
    {
      "text": "耳鳴りを感じますか？",
      "answers": [
        { "answer": "普段感じないけど、最近たまに一瞬聞こえたりする", "score": 3.3 },
        { "answer": "「キーン」と高い音が絶え間なく耳の周りで鳴り響いている", "score": 9.9 },
        { "answer": "低い「ブーン」という音がずっと聴こえる", "score": 5.5 },
        { "answer": "よく聞くけど、そんなに続かない軽いヤツ", "score": 7.7 },
      ]
    },
    {
      "text": "孤独を感じることはありますか？",
      "answers": [
        { "answer": "いつも誰かがそばにいてくれるので、寂しくないよ", "score": 3.3 },
        { "answer": "一人でいる時はよく孤独を感じる", "score": 5.5 },
        { "answer": "そばに誰かがいても孤独を強く感じることがある", "score": 7.7 },
        { "answer": "自分はむしろ孤独を愛するタイプ", "score": 9.9 },
      ]
    },
    {
      "text": "体に目立つ母斑やあざ、ほくろはありますか?  ",
      "answers": [
        { "answer": "はい、顔にハッキリとあざがあります", "score": 7.7 },
        { "answer": "あるけど、普段は服で隠れてる場所だよ", "score": 5.5 },
        { "answer": "全然ないよ、肌は完璧さ", "score": 3.3 },
        { "answer": "何ヶ所も目立つアザやホクロがあるよ", "score": 9.9 },
      ]
    },
    {
      "text": "次のうち、ご職業はどのカテゴリに最も当てはまりますか?",
      "answers": [
        { "answer": "会計士、弁護士、医師、教師", "score": 3.3 },
        { "answer": "アーティスト、デザイナー、作家", "score": 7.7 },
        { "answer": "事務員、公共、サービスおよび生産産業", "score": 5.5 },
        { "answer": "フリーランス、自由業", "score": 9.9 },
      ]
    },
    {
      "text": "あなたは実年齢と比べてどう見られていますか？",
      "answers": [
        { "answer": "基本的に実年齢より若く見える", "score": 9.9 },
        { "answer": "基本的には実年齢相応に見られる", "score": 5.5 },
        { "answer": "実年齢より老けて見える", "score": 3.3 },
        { "answer": "年代ごとにさまざまな変化があった", "score": 7.7 },
      ]
    },
    {
      "text": "あなたは他人の言葉や態度に敏感ですか？",
      "answers": [
        { "answer": "はい、よく相手の真意を察知してしまう", "score": 7.7 },
        { "answer": "基本、他人の言動は気にいない、我が道をゆくタイプ", "score": 5.5 },
        { "answer": "相手の言っていることは文字通りに理解する", "score": 3.3 },
        { "answer": "相手の潜在意識までも分かってしまうほど敏感よ", "score": 9.9 },
      ]
    },
  ],
    "testC": [
    {
      "text": "お金についてどう思いますか？",
      "answers": [
        { "answer": "衣食住を満たすための単なる道具", "score": 5.5 },
        { "answer": "人間の邪悪な部分の根源", "score": 7.7 },
        { "answer": "理解に苦しむ概念、お金ってなぜ必要なの？", "score": 9.9 },
        { "answer": "目的を達成するためには欠かせないもの", "score": 3.3 },
      ]
    },
    {
      "text": "他人のオーラが見えますか？",
      "answers": [
        { "answer": "もちろん、オーラの色も識別できるさ", "score": 7.7 },
        { "answer": "見えるだけでなく、その色や形の意味も分かるよ", "score": 9.9 },
        { "answer": "オーラって何？", "score": 3.3 },
        { "answer": "ちょうど今、オーラを見る能力を習得中", "score": 5.5 },
      ]
    },
    {
      "text": "他人からあなたについてよく言われるのは？",
      "answers": [
        { "answer": "物事に対して非常に敏感なタイプ", "score": 9.9 },
        { "answer": "比較的鈍感でいつも周りより一歩遅れている", "score": 3.3 },
        { "answer": "物事に対して慎重なタイプ", "score": 5.5 },
        { "answer": "物事に対してあまり拘らない", "score": 7.7 },
      ]
    },
    {
      "text": "次の言葉のうち、最も共感できるのは?",
      "answers": [
        { "answer": "自由、情熱、成功", "score": 7.7 },
        { "answer": "献身、喜び、調和", "score": 9.9 },
        { "answer": "富、尊厳、栄光", "score": 3.3 },
        { "answer": "美しさ、カッコ良さ、気質", "score": 5.5 },
      ]
    },
    {
      "text": "高価なものには興味ありますか？",
      "answers": [
        { "answer": "質とか本物かどうかによる", "score": 5.5 },
        { "answer": "価格って重要なの?", "score": 9.9 },
        { "answer": "大金持ちだったとしても興味はない", "score": 7.7 },
        { "answer": "はい、もしお金持ちだったら", "score": 3.3 },
      ]
    },
    {
      "text": "法やルールで束縛されることについて思うのは？",
      "answers": [
        { "answer": "内容は何であれ、守ってさえすればOK", "score": 5.5 },
        { "answer": "理不尽だと思うことも多いが、仕方ないさ", "score": 7.7 },
        { "answer": "なぜ人間はルールに支配されるの？", "score": 9.9 },
        { "answer": "人間性の悪の部分はルールによってのみ抑制できる", "score": 3.3 },
      ]
    },
    {
      "text": "ご自分の周りや人間社会への帰属意識を感じますか?",
      "answers": [
        { "answer": "はい、自分は社会の一員だと自覚している", "score": 3.3 },
        { "answer": "特定のサークルにだけ帰属意識を感じる", "score": 5.5 },
        { "answer": "いいえ、自分は人間に属さないような気がする", "score": 7.7 },
        { "answer": "自分が実は地球の人類でないことをすでに知っている", "score": 9.9 },
      ]
    },
    {
      "text": "あなたは動物の言葉を理解できますか？",
      "answers": [
        { "answer": "ペットの言うことなら理解できる", "score": 5.5 },
        { "answer": "自分のペットと同じ動物については比較的よく解る", "score": 7.7 },
        { "answer": "私は動物や植物の意識が読み取れる", "score": 9.9 },
        { "answer": "何を言いたいのかさっぱり...", "score": 3.3 },
      ]
    },
    {
      "text": "お子さんはいますか？",
      "answers": [
        { "answer": "まだいないが、子供は欲しい", "score": 5.5 },
        { "answer": "はい、います", "score": 3.3 },
        { "answer": "いいえ、欲しくないけど子供は好き", "score": 9.9 },
        { "answer": "子供よりペットの方がもっと好きかも", "score": 7.7 },
      ]
    },
    {
      "text": "次のうち、他人の何を見抜くことが得意ですか？",
      "answers": [
        { "answer": "短所", "score": 3.3 },
        { "answer": "長所", "score": 9.9 },
        { "answer": "秘密", "score": 7.7 },
        { "answer": "年齢", "score": 5.5 },
      ]
    }
  ],
    "testD": [
    {
      "text": "この世に生きる本当の目的は何だと思いますか？",
      "answers": [
        { "answer": "学ぶこと", "score": 9.9 },
        { "answer": "懲役に服すること", "score": 7.7 },
        { "answer": "伝承すること", "score": 5.5 },
        { "answer": "よく分からないし、考えたこともない", "score": 3.3 },
      ]
    },
      {
      "text": "地球はどんな惑星ですか?",
      "answers": [
        { "answer": "学校", "score": 7.7 },
        { "answer": "全ては幻さ", "score": 9.9 },
        { "answer": "楽園", "score": 3.3 },
        { "answer": "監獄", "score": 5.5 },
      ]
    },
    {
      "text": "あなたの信仰は次のうちのどれに最も近いですか?",
      "answers": [
        { "answer": "イデオロギーに基づいた信念・信仰", "score": 3.3 },
        { "answer": "科学ベースの信仰・信念", "score": 5.5 },
        { "answer": "私は創造主と直接繋がっているよ", "score": 9.9 },
        { "answer": "特定の宗教に基づく信仰", "score": 7.7 },
      ]
    },
    {
      "text": "どのような方法でご自分を表現するのが一番得意ですか?",
      "answers": [
        { "answer": "言語（話す、書く）", "score": 3.3 },
        { "answer": "表情（感情、怒り、悲しみ、喜び）", "score": 5.5 },
        { "answer": "特定の行動パターン", "score": 7.7 },
        { "answer": "テレパシーによって", "score": 9.9 },
      ]
    },
    {
      "text": "結婚に興味はありますか？",
      "answers": [
        { "answer": "ずっと憧れている/既婚でとても幸せ", "score": 5.5 },
        { "answer": "プレッシャーに圧倒されそう.../結婚したが不幸", "score": 3.3 },
        { "answer": "他人がどう思おうと、自分には合わないと思う", "score": 9.9 },
        { "answer": "誰かを本気で好きになったら考えるかも", "score": 7.7 },
      ]
    },
    {
      "text": "注目の的になるのはお好きですか？",
      "answers": [
        { "answer": "大好き、夢は有名人になること", "score": 3.3 },
        { "answer": "大嫌い、むしろ空気になりたい", "score": 9.9 },
        { "answer": "友人や家族ならいいけど、公衆の前ではちょっと・・・", "score": 5.5 },
        { "answer": "あまり気にしない、どっちでもOK", "score": 7.7 },
      ]
    },
    {
      "text": "毎日の平均睡眠時間はどれくらいですか?",
      "answers": [
        { "answer": "4時間未満", "score": 3.3 },
        { "answer": "およそ6時間", "score": 5.5 },
        { "answer": "およそ8時間", "score": 7.7 },
        { "answer": "9時間以上", "score": 9.9 },
      ]
    },
    {
      "text": "他の人と競争や対立する場面になると、あなたは…",
      "answers": [
        { "answer": "なぜこのような状況になるのかが理解できない", "score": 9.9 },
        { "answer": "自信がないのであっさり負けを認めるかも", "score": 5.5 },
        { "answer": "相手と和解しようと試みる", "score": 7.7 },
        { "answer": "負けるもんかと最後まで徹底抗戦", "score": 3.3 },
      ]
    },
    {
      "text": "お金について一番感じていることは何ですか?",
      "answers": [
        { "answer": "ほとんどのトラブルの元", "score": 9.9 },
        { "answer": "さまざまな欲求を解決する道具", "score": 5.5 },
        { "answer": "人間の問題を解決するためのツール", "score": 3.3 },
        { "answer": "私が心配するようなものではない", "score": 7.7 },
      ]
    },
    {
      "text": "「他人への奉仕」についてどう思いますか？",
      "answers": [
        { "answer": "自分が損さえしなければやる価値はある", "score": 7.7 },
        { "answer": "他人の為になるのなら自分が損してもやるべき", "score": 9.9 },
        { "answer": "偽善者がやることだと思う", "score": 3.3 },
        { "answer": "自分の評判のためならやる価値はある", "score": 5.5 },
      ]
    }
  ],
    "testE": [
    {
      "text": "物語や映画のプロットに共感しやすいタイプですか?",
      "answers": [
        { "answer": "あくまで架空の話だからあまり深入りしない", "score": 5.5 },
        { "answer": "はい、「涙失禁」をよく起こします", "score": 9.9 },
        { "answer": "自分の体験と似たストーリーには共感できる", "score": 7.7 },
        { "answer": "たとえ実話だったとしても何も感じない", "score": 3.3 },
      ]
    },
      {
      "text": "次のうち、最も興味のあるトピックは何ですか?",
      "answers": [
        { "answer": "宇宙、スピリチュアル、哲学、宗教", "score": 9.9 },
        { "answer": "科学技術", "score": 7.7 },
        { "answer": "芸能ゴシップ、人間関係", "score": 5.5 },
        { "answer": "資産運用、お金のこと", "score": 3.3 },
      ]
    },
    {
      "text": "あなたに対する他人の評価の中で、最も多いのは？",
      "answers": [
        { "answer": "他人と仲良くしたり輪に溶け込むのが得意", "score": 3.3 },
        { "answer": "成功したエリート", "score": 5.5 },
        { "answer": "ミステリアス、無口、無愛想", "score": 7.7 },
        { "answer": "実年齢よりも大人っぽい", "score": 9.9 },
      ]
    },
    {
      "text": "週末やお休みは何をして過ごすのが一番好きですか?",
      "answers": [
        { "answer": "一人で本を読んだり、瞑想したり、考えに耽る…", "score": 9.9 },
        { "answer": "一人でショッピング、社交、遊ぶこと", "score": 3.3 },
        { "answer": "大切な人や家族と一緒に時間を過ごす", "score": 5.5 },
        { "answer": "人間よりも動物や自然と過ごす", "score": 7.7 },
      ]
    },
    {
      "text": "社会における普遍的価値をどう思いますか？",
      "answers": [
        { "answer": "大多数の人々の利益に基づいた価値観だと思う", "score": 3.3 },
        { "answer": "どう言えば良いか分からないが、あまりしっくり来ない", "score": 5.5 },
        { "answer": "嘘に基づいた架空のナラティブ", "score": 7.7 },
        { "answer": "本質的には地球刑務所の行動規範だと思う", "score": 9.9 },
      ]
    },
    {
      "text": "第六感や霊感は本当に存在すると思いますか?",
      "answers": [
        { "answer": "五感だけは確かだが、それ以外は全くの偶然", "score": 3.3 },
        { "answer": "私の第六感はきっと本物よ", "score": 7.7 },
        { "answer": "半信半疑かな、他人の霊能力が当たるのはよく目撃する", "score": 5.5 },
        { "answer": "第六感って当たり前だよ、何がそんなに珍しいの？", "score": 9.9 },
      ]
    },
    {
      "text": "人間社会で最も不条理で滑稽なことは何だと思いますか?",
      "answers": [
        { "answer": "人類が宇宙唯一の知能体だという思い込み", "score": 7.7 },
        { "answer": "唯物論・科学主義", "score": 9.9 },
        { "answer": "貧富の差", "score": 5.5 },
        { "answer": "宗教間の対立", "score": 3.3 },
      ]
    },
    {
      "text": "言い知れぬ孤独感を感じていませんか？なぜ？",
      "answers": [
        { "answer": "はい、他人を信じることができないから", "score": 7.7 },
        { "answer": "はい、よく空を見てはノスタルジーを感じてしまう", "score": 9.9 },
        { "answer": "いいえ、私の周りにはいつも誰かがいてくれます", "score": 3.3 },
        { "answer": "私は孤独と向き合う方法を知っているので大丈夫", "score": 5.5 },
      ]
    },
    {
      "text": "あなたにとって、仕事とは何ですか?",
      "answers": [
        { "answer": "他の人に喜びをもたらすもの", "score": 9.9 },
        { "answer": "生活のために仕方なくすること", "score": 3.3 },
        { "answer": "好きな事を仕事にしている", "score": 5.5 },
        { "answer": "人生のミッションとしてやるべきこと", "score": 7.7 },
      ]
    },
      {
      "text": "あなたのお悩みは主にどこから来ていますか?",
      "answers": [
        { "answer": "物欲に関する悩み", "score": 3.3 },
        { "answer": "人間関係", "score": 5.5 },
        { "answer": "自分の人生の使命について", "score": 9.9 },
        { "answer": "世の中の問題", "score": 7.7 },
      ]
    },
  ],
  },
  "en": { 
    "testA": [
    {
      "text": "Which of the following are you most interested in?",
      "answers": [
        { "answer": "Nature", "score": 3.3 },
        { "answer": "Universe", "score": 9.9 },
        { "answer": "Various sounds", "score": 7.7 },
        { "answer": "Ancient ruins", "score": 5.5 },
      ]
    },
    {
      "text": "Whom do you like to spend time with?",
      "answers": [
        { "answer": "Family and loved ones", "score": 5.5 },
        { "answer": "Friends", "score": 3.3 },
        { "answer": "By myself", "score": 9.9 },
        { "answer": "Animals", "score": 7.7 },
      ]
    },
    {
      "text": "Do you have any past life memories?",
      "answers": [
        { "answer": "No, not at all", "score": 3.3 },
        { "answer": "Yes, I remember many reincarnation experiences", "score": 9.9 },
        { "answer": "No, but I often have lucid dreams that are different from reality", "score": 5.5 },
        { "answer": "I only remember my previous life, but nothing beyond that one", "score": 7.7 },
      ]
    },
    {
      "text": "Which kind of beings are you most interested in?",
      "answers": [
        { "answer": "Extraterrestrials", "score": 7.7 },
        { "answer": "Underground beings", "score": 5.5 },
        { "answer": "Homo sapiens", "score": 3.3 },
        { "answer": "Beings / consciousness from other dimensions", "score": 9.9 },
      ]
    },
    {
      "text": "Which of the following do you care the most?",
      "answers": [
        { "answer": "My social status / recognition", "score": 3.3 },
        { "answer": "How my friends think of me", "score": 5.5 },
        { "answer": "How I view myself", "score": 9.9 },
        { "answer": "How my family thinks of me", "score": 7.7 },
      ]
    },
    {
      "text": "What role do you except your partner to play?",
      "answers": [
        { "answer": "Soulmate exploring the universe together", "score": 9.9 },
        { "answer": "A life partner who would protect the family bloodline together", "score": 5.5 },
        { "answer": "Someone to enjoy the life with", "score": 7.7 },
        { "answer": "A roommate who will survive with me together", "score": 3.3 },
      ]
    },
    {
      "text": "Have you ever seen a UFO?",
      "answers": [
        { "answer": "Yes, I see them often", "score": 9.9 },
        { "answer": "No, I've never seen any", "score": 3.3 },
        { "answer": "Yes, but once or twice at most", "score": 7.7 },
        { "answer": "I don't know, maybe but not sure...", "score": 5.5 },
      ]
    },
    {
      "text": "What is the most important thing you do in your daily routine?",
      "answers": [
        { "answer": "Write a diary or journal", "score": 7.7 },
        { "answer": "Meditation", "score": 9.9 },
        { "answer": "Workout exercise", "score": 5.5 },
        { "answer": "None of the above", "score": 3.3 },
      ]
    },
    {
      "text": "Do you have any of the following abilities?",
      "answers": [
        { "answer": "Remote viewing / psychic ability", "score": 9.9 },
        { "answer": "Levitation", "score": 5.5 },
        { "answer": "Teleportation", "score": 7.7 },
        { "answer": "None of the above", "score": 3.3 },
      ]
    },
    {
      "text": "Have you ever had any experience that you believe to be the act of God or destiny?",
      "answers": [
        { "answer": "Yes, at least once", "score": 7.7 },
        { "answer": "Maybe, but I'm not sure", "score": 5.5 },
        { "answer": "No, never", "score": 3.3 },
        { "answer": "Yes, it happened many times", "score": 9.9 },
      ]
    },
  ],
    "testB": [
    {
      "text": "Do you get stressed out easily?",
      "answers": [
        { "answer": "Yes, my physical condition is often affected", "score": 9.9 },
        { "answer": "Not often, except in cases of serious incidents", "score": 5.5 },
        { "answer": "I often get stressed, but after all it's not a big deal", "score": 7.7 },
        { "answer": "I don't mind getting stressed out at all", "score": 3.3 },
      ]
    },
    {
      "text": "What aspect of universe are you most interested in?",
      "answers": [
        { "answer": "Intelligent life forms other than humans, aliens", "score": 5.5 },
        { "answer": "Physics / science in relation to the universe", "score": 3.3 },
        { "answer": "Where on earth is my home planet?", "score": 9.9 },
        { "answer": "Parallel universes, timelines, dark matter, etc.", "score": 7.7 },
      ]
    },
    {
      "text": "Do you have psychic ability?",
      "answers": [
        { "answer": "I have had a strong sixth sense since I was a child", "score": 9.9 },
        { "answer": "Sometimes my dreams become reality", "score": 7.7 },
        { "answer": "I've witnessed other people's psychic power, but I don't have it myself", "score": 5.5 },
        { "answer": "I never believe in this kind of BS", "score": 3.3 },
      ]
    },
    {
      "text": "Is your life full of ups and downs?",
      "answers": [
        { "answer": "My life has been full of challenges, but I'm always optimistic", "score": 9.9 },
        { "answer": "I guess I've been relatively lucky so far", "score": 3.3 },
        { "answer": "Life once had been quite tough for a period of time, but then it picked up", "score": 5.5 },
        { "answer": "It's always been rough...", "score": 7.7 },
      ]
    },
    {
      "text": "Do you feel ringing in your ears?",
      "answers": [
        { "answer": "I don't usually feel it, but lately it occurred to me a few times", "score": 3.3 },
        { "answer": "A high-pitched sound is constantly ringing around my ears", "score": 9.9 },
        { "answer": "I hear a constant low 'buzzing' sound", "score": 5.5 },
        { "answer": "I often have ringing in my ears but they don't last long", "score": 7.7 },
      ]
    },
    {
      "text": "Do you feel lonely?",
      "answers": [
        { "answer": "I don't feel lonely because someone is always by my side", "score": 3.3 },
        { "answer": "I often feel lonely when I'm alone", "score": 5.5 },
        { "answer": "Even if there is someone by my side, I still feel very lonely", "score": 7.7 },
        { "answer": "I love being in solitude", "score": 9.9 },
      ]
    },
    {
      "text": "Do you have any noticeable birthmarks or moles on your body?",
      "answers": [
        { "answer": "Yes, there is an obvious birthmark on my face", "score": 7.7 },
        { "answer": "Yes, but it's usually hidden under the clothes", "score": 5.5 },
        { "answer": "Not at all, my skin is perfect", "score": 3.3 },
        { "answer": "I do, not just one but a few spots", "score": 9.9 },
      ]
    },
    {
      "text": "Which category does your occupation most closely fit into?",
      "answers": [
        { "answer": "Accountant, lawyer, doctor, teacher", "score": 3.3 },
        { "answer": "Artist, designer, writer", "score": 7.7 },
        { "answer": "Admin, public, service and production industries", "score": 5.5 },
        { "answer": "Freelance", "score": 9.9 },
      ]
    },
    {
      "text": "How do you look compared to your actual age?",
      "answers": [
        { "answer": "I look younger than my actual age", "score": 9.9 },
        { "answer": "I basically look like my actual age", "score": 5.5 },
        { "answer": "I look older than my actual age", "score": 3.3 },
        { "answer": "I had been looked differently depending on age period", "score": 7.7 },
      ]
    },
    {
      "text": "Are you sensitive to other people's words and behavior?",
      "answers": [
        { "answer": "Yes, I often sense the true intention of other people's words", "score": 7.7 },
        { "answer": "Basically, I don't care about what other people say or do", "score": 5.5 },
        { "answer": "I just take the literal meaning of whatever people say", "score": 3.3 },
        { "answer": "I can even see the other person's subconscious mind", "score": 9.9 },
      ]
    },
  ],
    "testC": [
    {
      "text": "What roles do you think money plays?",
      "answers": [
        { "answer": "It's merely a tool for food, clothing and shelter", "score": 5.5 },
        { "answer": "The root of human evil", "score": 7.7 },
        { "answer": "Why do we need money anyway?", "score": 9.9 },
        { "answer": "An indispensable tool for achieving my objectives", "score": 3.3 },
      ]
    },
    {
      "text": "Can you see other people's auras?",
      "answers": [
        { "answer": "Yes,I can even distinguish their different colors", "score": 7.7 },
        { "answer": "I can not only see the aura but also their meanings", "score": 9.9 },
        { "answer": "What is an aura?", "score": 3.3 },
        { "answer": "I'm currently learning this ability", "score": 5.5 },
      ]
    },
    {
      "text": "What do people often say about you?",
      "answers": [
        { "answer": "Someone who is very sensitive to things", "score": 9.9 },
        { "answer": "Relatively insensitive and always one step behind others", "score": 3.3 },
        { "answer": "Very prudent", "score": 5.5 },
        { "answer": "A carefree person", "score": 7.7 },
      ]
    },
    {
      "text": "Which of the following words resonates with you the most?",
      "answers": [
        { "answer": "Freedom, Passion, Success", "score": 7.7 },
        { "answer": "Dedication, Joy, Harmony", "score": 9.9 },
        { "answer": "Wealth, Dignity, Glory", "score": 3.3 },
        { "answer": "Beauty, Coolness, Temperament", "score": 5.5 },
      ]
    },
    {
      "text": "Are you interested in expensive things?",
      "answers": [
        { "answer": "Depends on quality / whether it's real or not", "score": 5.5 },
        { "answer": "Why does price matter?", "score": 9.9 },
        { "answer": "I don't care even if I were rich", "score": 7.7 },
        { "answer": "Yes, only if I were rich", "score": 3.3 },
      ]
    },
    {
      "text": "What do you think about being bound by laws and rules?",
      "answers": [
        { "answer": "It doesn't matter what the content is, as long as I stay compliant", "score": 5.5 },
        { "answer": "There are many things I don't agree with, but what can I do?", "score": 7.7 },
        { "answer": "Why are humans ruled by rules?", "score": 9.9 },
        { "answer": "The evils of humanity can only be suppressed by rules", "score": 3.3 },
      ]
    },
    {
      "text": "Do you feel a sense of belonging to your community or to the human society?",
      "answers": [
        { "answer": "Yes, I consider myself a member of the society", "score": 3.3 },
        { "answer": "I feel a sense of belonging only to a certain group(s) of people", "score": 5.5 },
        { "answer": "No, I feel like I don't belong to humanity", "score": 7.7 },
        { "answer": "I already know that I am not an Earthling", "score": 9.9 },
      ]
    },
    {
      "text": "Can you understand what animals say?",
      "answers": [
        { "answer": "I can understand what my pets want to say", "score": 5.5 },
        { "answer": "I have a relatively good understanding of animals same as my pet", "score": 7.7 },
        { "answer": "I understand the consciousness of animals and plants very well", "score": 9.9 },
        { "answer": "I have no idea what they're talking about…", "score": 3.3 },
      ]
    },
    {
      "text": "Do you have any children?",
      "answers": [
        { "answer": "Not yet, but I do plan to have kids", "score": 5.5 },
        { "answer": "Yes, I do", "score": 3.3 },
        { "answer": "No, I don't want any, but I like kids", "score": 9.9 },
        { "answer": "Maybe I like pets more than kids", "score": 7.7 },
      ]
    },
    {
      "text": "Which of the following traits of other people are you good at guessing?",
      "answers": [
        { "answer": "Weakness", "score": 3.3 },
        { "answer": "Strength", "score": 9.9 },
        { "answer": "Secrets", "score": 7.7 },
        { "answer": "Age", "score": 5.5 },
      ]
    }
  ],
    "testD": [
    {
      "text": "What do you think is the true purpose of life?",
      "answers": [
        { "answer": "To learn", "score": 9.9 },
        { "answer": "To serve imprisonment", "score": 7.7 },
        { "answer": "To pass on something", "score": 5.5 },
        { "answer": "Don't know, never thought about it", "score": 3.3 },
      ]
    },
      {
      "text": "What kind of planet is Earth?",
      "answers": [
        { "answer": "A school", "score": 7.7 },
        { "answer": "An illusion", "score": 9.9 },
        { "answer": "A paradise", "score": 3.3 },
        { "answer": "A prison", "score": 5.5 },
      ]
    },
    {
      "text": "Which of the following best describes your faith?",
      "answers": [
        { "answer": "Beliefs based on a certain ideology", "score": 3.3 },
        { "answer": "Science-based belief", "score": 5.5 },
        { "answer": "My faith is directly connected to the Creator / Origin", "score": 9.9 },
        { "answer": "My belief is based on a particular religion", "score": 7.7 },
      ]
    },
    {
      "text": "By what means do you best express yourself?",
      "answers": [
        { "answer": "Language (speaking, writing)", "score": 3.3 },
        { "answer": "Facial/physical expressions of emotions", "score": 5.5 },
        { "answer": "Specific behavioral patterns", "score": 7.7 },
        { "answer": "By telepathy", "score": 9.9 },
      ]
    },
    {
      "text": "Are you interested in marriage?",
      "answers": [
        { "answer": "I've always dreamed of being married / I'm happily married", "score": 5.5 },
        { "answer": "I feel overwhelmed by the pressure... / married but unhappy", "score": 3.3 },
        { "answer": "No matter what others may think, I don't think I'm fit for marriage", "score": 9.9 },
        { "answer": "I might think about it if I really fell in love with someone", "score": 7.7 },
      ]
    },
    {
      "text": "Do you like being the center of attention?",
      "answers": [
        { "answer": "I love it, my dream is to become a celebrity", "score": 3.3 },
        { "answer": "I hate it, I'd rather be invisible", "score": 9.9 },
        { "answer": "It's fun only if within my own circles of friends and family", "score": 5.5 },
        { "answer": "I don't really care and it doesn't bother me", "score": 7.7 },
      ]
    },
    {
      "text": "How much time do you sleep on average each day?",
      "answers": [
        { "answer": "Less than 4 hours", "score": 3.3 },
        { "answer": "Approximately 6 hours", "score": 5.5 },
        { "answer": "Approximately 8 hours", "score": 7.7 },
        { "answer": "More than 9 hours", "score": 9.9 },
      ]
    },
    {
      "text": "When it comes to competition or conflict with others, you would:",
      "answers": [
        { "answer": "not be able to comprehend why such conflict would exist", "score": 9.9 },
        { "answer": "mostly not be conident enough, so why not just surrender", "score": 5.5 },
        { "answer": "try to reconcile with the other side", "score": 7.7 },
        { "answer": "never surrender, fight with all my strengths", "score": 3.3 },
      ]
    },
    {
      "text": "What do you think of money?",
      "answers": [
        { "answer": "Root to most troubles", "score": 9.9 },
        { "answer": "A means for meeting various needs", "score": 5.5 },
        { "answer": "A tool for solving human problems", "score": 3.3 },
        { "answer": "It's not something I would worry about", "score": 7.7 },
      ]
    },
    {
      "text": "What do you think about 'service to others'?",
      "answers": [
        { "answer": "It's worth doing as long as I don't lose anything", "score": 7.7 },
        { "answer": "If it's for the others, it's worth doing even it may cost me", "score": 9.9 },
        { "answer": "I'm not interested in the fake hypocrisy", "score": 3.3 },
        { "answer": "It's worth it for my reputation and credit", "score": 5.5 },
      ]
    }
  ],
    "testE": [
    {
      "text": "Do you tend to resonate with / relate to stories and movie plots?",
      "answers": [
        { "answer": "I know they are fictions, so I won't go into it too much", "score": 5.5 },
        { "answer": "Yes, I tend to burst into tears after reading/watching them", "score": 9.9 },
        { "answer": "I empathize with stories that tell of experiences similar to my own", "score": 7.7 },
        { "answer": "Even if it was a true story, I don't feel anything", "score": 3.3 },
      ]
    },
      {
      "text": "Which of the following topics are you most interested in?",
      "answers": [
        { "answer": "Space, Spirituality, Philosophy, Religion", "score": 9.9 },
        { "answer": "Science and Technology", "score": 7.7 },
        { "answer": "Entertainment, Gossip, Relationships", "score": 5.5 },
        { "answer": "Asset Management, Money", "score": 3.3 },
      ]
    },
    {
      "text": "What is the most common evaluation of you by others?",
      "answers": [
        { "answer": "Good at getting along with others folks", "score": 3.3 },
        { "answer": "A successful elite", "score": 5.5 },
        { "answer": "Mysterious, taciturn, unfriendly", "score": 7.7 },
        { "answer": "Looks more mature than my actual age", "score": 9.9 },
      ]
    },
    {
      "text": "What is your favorite thing to do on your days off?",
      "answers": [
        { "answer": "Read a book, meditate, think alone...", "score": 9.9 },
        { "answer": "Shopping, socializing and playing", "score": 3.3 },
        { "answer": "Spend time with loved ones and family", "score": 5.5 },
        { "answer": "Spend time with animals and nature", "score": 7.7 },
      ]
    },
    {
      "text": "What do you think about universal values?",
      "answers": [
        { "answer": "They are based on the interests of the majority of people", "score": 3.3 },
        { "answer": "I don't know what to say, but they don't really sit well with me", "score": 5.5 },
        { "answer": "A fictional narrative based on lies", "score": 7.7 },
        { "answer": "They are basically the Earth Prison's Code of Conduct", "score": 9.9 },
      ]
    },
    {
      "text": "Do you think a sixth sense or psychic power really exists?",
      "answers": [
        { "answer": "Only the five senses are certain, everything else is pure coincidence", "score": 3.3 },
        { "answer": "My sixth sense must be legit", "score": 7.7 },
        { "answer": "I'm skeptical, but I often witness other people's psychic power", "score": 5.5 },
        { "answer": "Having a sixth sense is commonplace, what's so rare about it?", "score": 9.9 },
      ]
    },
    {
      "text": "What do you think is the most absurd thing about human society?",
      "answers": [
        { "answer": "The belief that humans are the only intelligence in the universe", "score": 7.7 },
        { "answer": "Materialism / Scientism", "score": 9.9 },
        { "answer": "The gap between rich and poor", "score": 5.5 },
        { "answer": "Conflicts between religions", "score": 3.3 },
      ]
    },
    {
      "text": "Are you feeling an indescribable sense of loneliness? why?",
      "answers": [
        { "answer": "Yes, I can't trust others", "score": 7.7 },
        { "answer": "Yes, I often feel nostalgic when I look at the sky", "score": 9.9 },
        { "answer": "No, there are always people around me", "score": 3.3 },
        { "answer": "I know how to face solitude", "score": 5.5 },
      ]
    },
    {
      "text": "What does work mean to you?",
      "answers": [
        { "answer": "Something that brings joy to the others", "score": 9.9 },
        { "answer": "Something you have no choice but to do for a living", "score": 3.3 },
        { "answer": "I'm working on what I love", "score": 5.5 },
        { "answer": "It's my mission in life", "score": 7.7 },
      ]
    },
      {
      "text": "Where do your worries mainly come from?",
      "answers": [
        { "answer": "Material needs and desires", "score": 3.3 },
        { "answer": "Relationships with other humans...", "score": 5.5 },
        { "answer": "Quest for life mission", "score": 9.9 },
        { "answer": "Problems faced by the world and humanity", "score": 7.7 },
      ]
    },
  ],
  }
}

starseedQuestionsRestuls = {
  "zh": {
    "a": "从您目前的身心特征看上去，您更有可能是地球的原生灵魂。但是您挑战这项测试本身就证明了您是一个具有觉醒潜力的灵魂！",
    "b": "您对自己有可能是一颗星际种子的可能性有了一定的意识，但还需要进一步的苏醒。建议您在每天的生活中通过冥想等方式去继续寻找自己的根源！",
    "c": "您很可能是一颗带有特定使命的星际种子，已对自己来到地球的目的有了清晰的认知，并在积极采取行动唤醒更多的灵魂。欢迎您来一起分享您知道的阿卡西记录片段！"
  },
  "ja": {
    "a": "現状の心身の特徴から判断すると、あなたは地球由来の魂である可能性が高いと思われます。あなたがこのテストに挑戦するということ自体が、目覚めの可能性を秘めた魂であることを証明しています。",
    "b": "あなたはご自分がスターシードである可能性にある程度お気づきですが、さらなる覚醒が必要です。日々の生活の中で瞑想などの方法でご自分のルーツを探し続けるましょう！",
    "c": "おそらくあなたは特定の使命を持ったスターシードであり、地球上での自分の目的を明確に理解し、より多くの目覚めを目指して積極的に行動を起こしています。ぜひご一緒にアカシックレコードの記録を！"
  },
  "en": {
    "a": "From your current physical and mental conditions, it seems that you are more likely to be a native soul of the earth. But the fact that you challenged this test itself proves that you are a soul with awakening potential!",
    "b": "You have some awareness of the possibility that you may be a starseed, but further awakening is needed. It is recommended that you continue to find your root through meditation and other methods in your daily life!",
    "c": "You are most likely a starseed with a specific mission. You have a clear understanding of your purpose on earth and are actively taking actions to awaken more souls. You are welcome to share your unique piece of the Akashic Records!"
  }
}








# JSONFile = 'bgben/main/starseed_test_file.json'
# fw = io.open(JSONFile , 'w', 'utf-8')
# json.dump(starseedQuestions, fw, ensure_ascii=False)
# fw.close()

with io.open('bgben/static/data/starseed_test_file.json', 'w', encoding='utf-8') as JSONFile:
  json.dump(starseedQuestions, JSONFile, ensure_ascii=False)


# io.open(
#     file,
#     mode="r",
#     buffering=-1,
#     encoding=None,
#     errors=None,
#     newline=None,
#     closefd=True,
#     opener=None,
# )