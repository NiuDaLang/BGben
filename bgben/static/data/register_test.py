import json, io, os


registerTestQuestions = {
  "zh": { 
    "humanity": [
      {
        "question": "哪一个国家在2023年从高中课本中删除了进化论？",
        "answers": [
          { "text": "越南", "correct": "false" },
          { "text": "斯洛伐克", "correct": "false" },
          { "text": "印度", "correct": "true" },
          { "text": "南非", "correct": "false" },
        ]
      },
      {
        "question": "DNA双螺旋结构的发现者们在1973年发表的理论是什么？",
        "answers": [
          { "text": "无生源论", "correct": "false" },
          { "text": "进化论", "correct": "false" },
          { "text": "RNA世界学说", "correct": "false" },
          { "text": "胚种论", "correct": "true" },
        ]
      },
      {
        "question": "人类的染色体是46条，那么大猩猩的染色体是多少？",
        "answers": [
          { "text": "48条", "correct": "true" },
          { "text": "46条", "correct": "false" },
          { "text": "44条", "correct": "false" },
          { "text": "52条", "correct": "false" },
        ]
      },
      {
        "question": "出现在古代苏美尔文献中的对人类进行基因改造的是什么人？",
        "answers": [
          { "text": "爱斯基摩人", "correct": "false" },
          { "text": "阿努纳奇人", "correct": "true" },
          { "text": "蜥蜴人", "correct": "false" },
          { "text": "天狼星人", "correct": "false" },
        ]
      },
      {
        "question": "一种认为现在的人类文明是由外星生物创造的理论叫什么？",
        "answers": [
          { "text": "古代外星人", "correct": "false" },
          { "text": "古代宇航员", "correct": "true" },
          { "text": "古代科学家", "correct": "false" },
          { "text": "古代开拓者", "correct": "false" },
        ]
      },
      {
        "question": "亚特兰蒂斯文明出现在哪一位哲学家的著作中？",
        "answers": [
          { "text": "苏格拉底", "correct": "false" },
          { "text": "尼采", "correct": "false" },
          { "text": "叔本华", "correct": "false" },
          { "text": "普拉图", "correct": "true" },
        ]
      },
      {
        "question": "以下文献古籍中除了哪一部以外都有记载女娲的故事？",
        "answers": [
          { "text": "山海经", "correct": "false" },
          { "text": "汉书", "correct": "false" },
          { "text": "风俗通义", "correct": "false" },
          { "text": "孙子兵法", "correct": "true" },
        ]
      },
      {
        "question": "印度神话中的人类始祖叫什么？",
        "answers": [
          { "text": "摩奴", "correct": "true" },
          { "text": "梵天", "correct": "false" },
          { "text": "湿婆", "correct": "false" },
          { "text": "毗湿奴", "correct": "false" },
        ]
      },
      {
        "question": "大约在3～4万年前从地球上突然消失的古人类叫什么人？",
        "answers": [
          { "text": "直立猿人", "correct": "false" },
          { "text": "海德堡人", "correct": "false" },
          { "text": "尼安德特人", "correct": "true" },
          { "text": "北京猿人", "correct": "false" },
        ]
      },
      {
        "question": "主流科学所说的“垃圾基因(DNA)”所占的比例是多少？",
        "answers": [
          { "text": "78~80%", "correct": "false" },
          { "text": "95~98%", "correct": "true" },
          { "text": "12~15%", "correct": "false" },
          { "text": "3~5%", "correct": "false" },
        ]
      }
    ],
    "underground": [
      {
        "question": "古代文献中描述的地下世界名称叫什么？",
        "answers": [
          { "text": "鞑靼利亚 Tartaria", "correct": "false" },
          { "text": "阿加莎 Agartha", "correct": "true" },
          { "text": "雷姆利亚 Lemuria", "correct": "false" },
          { "text": "亚特兰蒂斯 Atlantis", "correct": "false" },
        ]
      },
      {
        "question": "1938年和1943年，希特勒纳粹派遣了探险队去哪里寻找地下城市？",
        "answers": [
          { "text": "西伯利亚 Siberia", "correct": "false" },
          { "text": "西安 Xi-An", "correct": "false" },
          { "text": "东帝汶 East Timor", "correct": "false" },
          { "text": "西藏 Tibet", "correct": "true" },
        ]
      },
      {
        "question": "传说中的希特勒纳粹地下逃亡基地在哪里？",
        "answers": [
          { "text": "南极", "correct": "true" },
          { "text": "北极", "correct": "false" },
          { "text": "撒哈拉沙漠", "correct": "false" },
          { "text": "秘鲁", "correct": "false" },
        ]
      },
      {
        "question": "地下军事隧道系统的英语简称叫什么？",
        "answers": [
          { "text": "D.B.U.M", "correct": "false" },
          { "text": "N.U.M.B", "correct": "false" },
          { "text": "D.U.M.B", "correct": "true" },
          { "text": "M.U.D.B", "correct": "false" },
        ]
      },
      {
        "question": "在地下展开的军事行动的主要目标是？",
        "answers": [
          { "text": "营救被蜥蜴人囚禁的友善外星人", "correct": "false" },
          { "text": "营救被走私的珍稀动物", "correct": "false" },
          { "text": "营救被贩卖的人类儿童", "correct": "true" },
          { "text": "夺回被盗窃用来做地下交易的金块", "correct": "false" },
        ]
      },
      {
        "question": "与地下军事行动有关的地震震源深度一般是多少？",
        "answers": [
          { "text": "～10公里", "correct": "true" },
          { "text": "10～15公里", "correct": "false" },
          { "text": "15～20公里", "correct": "false" },
          { "text": "20公里～", "correct": "false" },
        ]
      },
      {
        "question": "在阿拉斯加的麦金利山附近地下发现的金字塔呈现着什么颜色？",
        "answers": [
          { "text": "土色", "correct": "false" },
          { "text": "金色", "correct": "false" },
          { "text": "白色", "correct": "false" },
          { "text": "黑色", "correct": "true" },
        ]
      },
      {
        "question": "2003年，欧洲的哪一个国家在一座山中发现了神秘地下洞穴？",
        "answers": [
          { "text": "塞尔维亚", "correct": "false" },
          { "text": "罗马尼亚", "correct": "true" },
          { "text": "克罗地亚", "correct": "false" },
          { "text": "保加利亚", "correct": "false" },
        ]
      },
      {
        "question": "以下哪一位人物不是地下世界的探险者？",
        "answers": [
          { "text": "唐朝的玄奘", "correct": "true" },
          { "text": "古希腊的皮西亚斯", "correct": "false" },
          { "text": "挪威渔夫欧拉夫·詹森父子", "correct": "false" },
          { "text": "美国伯德海军少将", "correct": "false" },
        ]
      },
      {
        "question": "以下的哪一个城市是传说中的地下城市？",
        "answers": [
          { "text": "天竺", "correct": "false" },
          { "text": "巴比伦", "correct": "false" },
          { "text": "基捷日城", "correct": "false" },
          { "text": "香巴拉", "correct": "true" },
        ]
      }
    ],
    "ufo": [
      {
        "question": "参与UFO逆向工程研究的著名吹哨人是哪一位？",
        "answers": [
          { "text": "鲍勃·拉扎尔 Bob Lazar", "correct": "true" },
          { "text": "亚历克斯·科利尔 Allex Collier", "correct": "false" },
          { "text": "迈克尔·萨拉 Michael Salla", "correct": "false" },
          { "text": "菲尔·施耐德 Phil Schneider", "correct": "false" },
        ]
      },
      {
        "question": "位于美国内华达州的著名UFO基地的名称叫什么？",
        "answers": [
          { "text": "罗斯维尔 Roswell", "correct": "false" },
          { "text": "蒙淘克空军基地 Montauk Air Force Station", "correct": "false" },
          { "text": "51区 Area 51", "correct": "true" },
          { "text": "道西基地 Dulce Base", "correct": "false" },
        ]
      },
      {
        "question": "2023年7月在美国国会UFO听证会上作证的David Grusch之前的身份是？",
        "answers": [
          { "text": "太空军军官", "correct": "false" },
          { "text": "海军军官", "correct": "false" },
          { "text": "陆军军官", "correct": "false" },
          { "text": "空军军官", "correct": "true" },
        ]
      },
      {
        "question": "经常在地球上被目睹的UFO形状除了飞碟形状之外还有哪一种？？",
        "answers": [
          { "text": "牙膏形", "correct": "false" },
          { "text": "汽车形", "correct": "false" },
          { "text": "雪茄形", "correct": "true" },
          { "text": "五星形", "correct": "false" },
        ]
      },
      {
        "question": "二战期间，由纳粹秘密开发的穿越时空装置叫什么？",
        "answers": [
          { "text": "纳粹钟", "correct": "true" },
          { "text": "纳粹车", "correct": "false" },
          { "text": "纳粹瓶", "correct": "false" },
          { "text": "纳粹椅", "correct": "false" },
        ]
      },
      {
        "question": "美国华盛顿上空的著名不明飞行物事件是上世纪哪一年发生的?",
        "answers": [
          { "text": "1942年", "correct": "false" },
          { "text": "1952年", "correct": "true" },
          { "text": "1947年", "correct": "false" },
          { "text": "1972年", "correct": "false" },
        ]
      },
      {
        "question": "比罗斯维尔更早发生的1933年UFO坠落事件是在哪一个国家？",
        "answers": [
          { "text": "墨西哥", "correct": "false" },
          { "text": "意大利", "correct": "true" },
          { "text": "西班牙", "correct": "false" },
          { "text": "梵蒂冈", "correct": "false" },
        ]
      },
      {
        "question": "被称为是以黑科技技术逆向工程制造的反重力飞机名称叫什么？",
        "answers": [
          { "text": "F-22", "correct": "false" },
          { "text": "Ki-100", "correct": "false" },
          { "text": "MiG-29", "correct": "false" },
          { "text": "TR-3B", "correct": "true" },
        ]
      },
      {
        "question": "以下绘画中除了那一张之外都有UFO的描绘？",
        "answers": [
          { "text": "阿尔特·德·格尔德Aert de Gelder的《基督受洗》", "correct": "false" },
          { "text": "旧宫（Palazzo Vecchio）中的圣母画像", "correct": "false" },
          { "text": "梵高的《星夜》", "correct": "true" },
          { "text": "塞尔维亚东正教会的绘画", "correct": "false" },
        ]
      },
      {
        "question": "2003年，哪一个国家的科学家人工合成了反重力燃料“元素115”？",
        "answers": [
          { "text": "俄罗斯", "correct": "true" },
          { "text": "美国", "correct": "false" },
          { "text": "印度", "correct": "false" },
          { "text": "中国", "correct": "false" },
        ]
      }
    ],
    "jab": [
      {
        "question": "2024年1月，美国哪个州的卫生局长呼吁停止使用mRNA疫苗？",
        "answers": [
          { "text": "加利福尼亚州", "correct": "false" },
          { "text": "福罗里达州", "correct": "true" },
          { "text": "得克萨斯州", "correct": "false" },
          { "text": "纽约州", "correct": "false" },
        ]
      },
      {
        "question": "强制对人体进行接种疫苗违反了哪一套国际准则？",
        "answers": [
          { "text": "布雷顿森林体系", "correct": "false" },
          { "text": "京都议定书", "correct": "false" },
          { "text": "纽伦堡公约", "correct": "true" },
          { "text": "生物武器公约", "correct": "false" },
        ]
      },
      {
        "question": "新冠疫苗中含有的一种名叫“石墨烯”的物质可能促使身体产生什么变化？",
        "answers": [
          { "text": "具有磁性", "correct": "true" },
          { "text": "容易失眠", "correct": "false" },
          { "text": "体温上升", "correct": "false" },
          { "text": "食欲大增", "correct": "false" },
        ]
      },
      {
        "question": "手机中的哪一种功能可能测出周围已接种过新冠疫苗的人群？",
        "answers": [
          { "text": "二维码扫描", "correct": "false" },
          { "text": "Wi-Fi", "correct": "false" },
          { "text": "4G", "correct": "false" },
          { "text": "蓝牙", "correct": "true" },
        ]
      },
      {
        "question": "在疫苗接种率非常低的阿米什人群中几乎不存在的一种疾病是什么？",
        "answers": [
          { "text": "感冒", "correct": "false" },
          { "text": "肥胖症", "correct": "false" },
          { "text": "自闭症", "correct": "true" },
          { "text": "糖尿病", "correct": "false" },
        ]
      },
      {
        "question": "大科技公司的老板中，哪一个是最热衷于给全球人口接种疫苗的企业家？",
        "answers": [
          { "text": "马化腾", "correct": "false" },
          { "text": "马云", "correct": "false" },
          { "text": "马斯克", "correct": "false" },
          { "text": "比尔·盖茨", "correct": "true" },
        ]
      },
      {
        "question": "以下哪一种物质没有被添加在疫苗佐剂中？",
        "answers": [
          { "text": "铝", "correct": "false" },
          { "text": "金", "correct": "true" },
          { "text": "水银", "correct": "false" },
          { "text": "石墨烯", "correct": "false" },
        ]
      },
      {
        "question": "以下哪一种天然酶最具有帮助移除由疫苗注入体内的刺突蛋白及溶化血栓的作用？",
        "answers": [
          { "text": "纳豆酶", "correct": "true" },
          { "text": "葡萄聚糖酶", "correct": "false" },
          { "text": "门冬酰胺酶", "correct": "false" },
          { "text": "淀粉酶", "correct": "false" },
        ]
      },
      {
        "question": "由日本科学家大村智发现的一种对新冠病毒有效的药物的名称是？",
        "answers": [
          { "text": "槲皮素", "correct": "false" },
          { "text": "伊维菌素", "correct": "true" },
          { "text": "羟氯喹", "correct": "false" },
          { "text": "菠萝蛋白酶", "correct": "false" },
        ]
      },
      {
        "question": "以下哪一种说法不符合阴谋论圈所议论的疫苗接种目的？",
        "answers": [
          { "text": "削减人口", "correct": "false" },
          { "text": "超人类变种实验", "correct": "false" },
          { "text": "以纳米级别芯片完成「人联网」的铺垫", "correct": "false" },
          { "text": "公共卫生改善", "correct": "true" },
        ]
      }
    ],
    "ai": [
      {
        "question": "电影《2001太空漫游 2001》中，陪伴三名飞行员飞往木星的人工智能叫什么名字？",
        "answers": [
          { "text": "PAL 9000", "correct": "false" },
          { "text": "HAL 9000", "correct": "true" },
          { "text": "TAL 9000", "correct": "false" },
          { "text": "KAL 9000", "correct": "false" },
        ]
      },
      {
        "question": "做为第一个获得公民身份的人工智能机器人叫什么名字？",
        "answers": [
          { "text": "玛丽亚 Maria", "correct": "false" },
          { "text": "帕特里夏 Patricia", "correct": "false" },
          { "text": "西尔维娅 Sylvia", "correct": "false" },
          { "text": "索菲亚 Sophia", "correct": "true" },
        ]
      },
      {
        "question": "人工智能的“食物”是什么？",
        "answers": [
          { "text": "人类", "correct": "false" },
          { "text": "代码", "correct": "false" },
          { "text": "数据", "correct": "true" },
          { "text": "电", "correct": "false" },
        ]
      },
      {
        "question": "Alexa是哪一家公司的人工智能的名字？",
        "answers": [
          { "text": "亚马逊 Amazon", "correct": "true" },
          { "text": "谷歌 Google", "correct": "false" },
          { "text": "苹果 Apple", "correct": "false" },
          { "text": "脸书 Facebook", "correct": "false" },
        ]
      },
      {
        "question": "ChatGPT的意识形态偏向是？",
        "answers": [
          { "text": "左派", "correct": "true" },
          { "text": "右派", "correct": "false" },
          { "text": "中立", "correct": "false" },
          { "text": "新兴宗教", "correct": "false" },
        ]
      },
      {
        "question": "第一个AI聊天机器人Eliza是哪年诞生的？",
        "answers": [
          { "text": "1978年", "correct": "false" },
          { "text": "2001年", "correct": "false" },
          { "text": "1947年", "correct": "false" },
          { "text": "1966年", "correct": "true" },
        ]
      },
      {
        "question": "纪录片《编码歧视》所指的歧視是通過人工智能的什麼功能被發現的？",
        "answers": [
          { "text": "智商识别", "correct": "false" },
          { "text": "人脸识别", "correct": "true" },
          { "text": "肥胖度识别", "correct": "false" },
          { "text": "声音识别", "correct": "false" },
        ]
      },
      {
        "question": "黑石集團貝萊德的一款預測金融市場的人工智能軟件叫什麼？",
        "answers": [
          { "text": "阿童木", "correct": "false" },
          { "text": "阿凡達", "correct": "false" },
          { "text": "阿里巴巴", "correct": "false" },
          { "text": "阿拉丁", "correct": "true" },
        ]
      },
      {
        "question": "測試一台机器是否具有人工智能的是以下哪一项？",
        "answers": [
          { "text": "Tensorflow", "correct": "false" },
          { "text": "门萨智商测试 Mensa", "correct": "false" },
          { "text": "图灵测试 Turing Test", "correct": "true" },
          { "text": "贝尔测试 Bell Test", "correct": "false" },
        ]
      },
      {
        "question": "第一家由几乎全程都是由机器人运营的酒店是开在哪个国家？",
        "answers": [
          { "text": "日本", "correct": "true" },
          { "text": "美国", "correct": "false" },
          { "text": "以色列", "correct": "false" },
          { "text": "印度", "correct": "false" },
        ]
      }
    ],
    "et": [
      {
        "question": "蜥蜴人的血液是什么颜色的？",
        "answers": [
          { "text": "绿色", "correct": "false" },
          { "text": "蓝色", "correct": "true" },
          { "text": "黄色", "correct": "false" },
          { "text": "红色", "correct": "false" },
        ]
      },
      {
        "question": "《五角大楼的陌生人》一书中出现的韦尔·托尔Valiant Thor来自什么星球？？",
        "answers": [
          { "text": "冥王星", "correct": "false" },
          { "text": "火星", "correct": "false" },
          { "text": "月球", "correct": "false" },
          { "text": "金星", "correct": "true" },
        ]
      },
      {
        "question": "出生于1996年的俄罗斯靛蓝小孩Boriska声称自己来自哪个星球？",
        "answers": [
          { "text": "火星", "correct": "true" },
          { "text": "金星", "correct": "false" },
          { "text": "天狼星", "correct": "false" },
          { "text": "土星", "correct": "false" },
        ]
      },
      {
        "question": "《一的法则》中出现的外星生命的名字叫什么？",
        "answers": [
          { "text": "Ma", "correct": "false" },
          { "text": "Ta", "correct": "false" },
          { "text": "Ra", "correct": "true" },
          { "text": "La", "correct": "false" },
        ]
      },
      {
        "question": "1976年7月25日，“海盗一号”探测器在火星上拍到了什么惊人的图像？",
        "answers": [
          { "text": "UFO基地", "correct": "false" },
          { "text": "与人脸酷似的地面凸起", "correct": "true" },
          { "text": "黑色的金字塔", "correct": "false" },
          { "text": "庞大的透明建筑物", "correct": "false" },
        ]
      },
      {
        "question": "朵洛蕾丝·侃南在2011年的书籍中写道的三波星际种子中，第一波是大约何时来到了地球？",
        "answers": [
          { "text": "1940年代末", "correct": "true" },
          { "text": "1970年代", "correct": "false" },
          { "text": "2000年代初", "correct": "false" },
          { "text": "1960年代中", "correct": "false" },
        ]
      },
      {
        "question": "参与艾森豪威尔政府签订协议的是哪一种外星人？",
        "answers": [
          { "text": "昂宿星人", "correct": "false" },
          { "text": "灰人", "correct": "true" },
          { "text": "北欧型外星人", "correct": "false" },
          { "text": "天龙人", "correct": "false" },
        ]
      },
      {
        "question": "在1990年代流传出的一段外星人访谈实拍录像之揭露者叫什么名字？",
        "answers": [
          { "text": "马克 Mark", "correct": "false" },
          { "text": "约瑟夫 Joseph", "correct": "false" },
          { "text": "维克多 Victor", "correct": "true" },
          { "text": "大卫 David", "correct": "false" },
        ]
      },
      {
        "question": "古代苏美尔人记载中的阿努纳奇人来自哪一个星球？",
        "answers": [
          { "text": "尼比鲁", "correct": "true" },
          { "text": "阿尔法", "correct": "false" },
          { "text": "哈雷彗星", "correct": "false" },
          { "text": "太阳", "correct": "false" },
        ]
      },
      {
        "question": "如毗湿奴等出现在吠陀文献中的高等存在的皮肤是什么颜色？",
        "answers": [
          { "text": "金黄色", "correct": "false" },
          { "text": "红色", "correct": "false" },
          { "text": "绿色", "correct": "false" },
          { "text": "蓝色", "correct": "true" },
        ]
      }
    ],
    "spiritual": [
      {
        "question": "朵洛蕾丝·侃南女士、布莱恩·魏斯博士等使用了什么方法帮助人们找回了前世的记忆？",
        "answers": [
          { "text": "脑深部刺激疗法", "correct": "false" },
          { "text": "针灸疗法", "correct": "false" },
          { "text": "光疗法", "correct": "false" },
          { "text": "回溯催眠法", "correct": "true" },
        ]
      },
      {
        "question": "哪一种宗教教义否定了轮回？",
        "answers": [
          { "text": "犹太教", "correct": "false" },
          { "text": "佛教", "correct": "false" },
          { "text": "基督教", "correct": "true" },
          { "text": "印度教", "correct": "false" },
        ]
      },
      {
        "question": "《入门》一书中，主人公活在古埃及时代的身份是什么？",
        "answers": [
          { "text": "法老", "correct": "false" },
          { "text": "女祭司", "correct": "true" },
          { "text": "克莉奥帕特拉女王", "correct": "false" },
          { "text": "医师", "correct": "false" },
        ]
      },
      {
        "question": "佛教中的三世诸佛，代表未来的是哪位佛？",
        "answers": [
          { "text": "释迦牟尼佛", "correct": "false" },
          { "text": "燃灯佛", "correct": "false" },
          { "text": "药师佛", "correct": "false" },
          { "text": "弥勒佛", "correct": "true" },
        ]
      },
      {
        "question": "往世疗法是通过寻找患者的什么东西来治疗疾病？",
        "answers": [
          { "text": "业力", "correct": "true" },
          { "text": "身体状况", "correct": "false" },
          { "text": "家族血统", "correct": "false" },
          { "text": "兴趣爱好", "correct": "false" },
        ]
      },
      {
        "question": "1907年的一项科学实验显示的灵魂重量是多少克？",
        "answers": [
          { "text": "14克", "correct": "false" },
          { "text": "28克", "correct": "false" },
          { "text": "21克", "correct": "true" },
          { "text": "7克", "correct": "false" },
        ]
      },
      {
        "question": "根据《一的法则》所披露的内容，目前阶段的人类属于第几密度？",
        "answers": [
          { "text": "第五密度", "correct": "false" },
          { "text": "第三密度", "correct": "true" },
          { "text": "第八密度", "correct": "false" },
          { "text": "第四密度", "correct": "false" },
        ]
      },
      {
        "question": "地球母亲的频率是多少？",
        "answers": [
          { "text": "7.83Hz", "correct": "true" },
          { "text": "210.42Hz", "correct": "false" },
          { "text": "183.58Hz", "correct": "false" },
          { "text": "221.23Hz", "correct": "false" },
        ]
      },
      {
        "question": "脉轮中的眉心轮所包含的心灵含义是？",
        "answers": [
          { "text": "精神性、灵性", "correct": "false" },
          { "text": "生存能量", "correct": "false" },
          { "text": "洞察力、直觉", "correct": "true" },
          { "text": "爱、情感", "correct": "false" },
        ]
      },
      {
        "question": "目前我们正处于哪一个宇迦时代？",
        "answers": [
          { "text": "圆满时 Krita Yuga", "correct": "false" },
          { "text": "二分时 Dvapara Yuga", "correct": "false" },
          { "text": "三分时 Treta Yuga", "correct": "false" },
          { "text": "争斗时 Kali Yuga", "correct": "true" },
        ]
      },
    ],
    "healing": [
      {
        "question": "声音疗法Gong Healing用的是哪一种中国古代乐器？",
        "answers": [
          { "text": "箫", "correct": "false" },
          { "text": "古琴", "correct": "false" },
          { "text": "笛", "correct": "false" },
          { "text": "铜锣", "correct": "true" },
        ]
      },
      {
        "question": "有一种制作蛋糕的材料，同时也具有医疗效果并促使体内碱性化，它是什么？",
        "answers": [
          { "text": "泡打粉", "correct": "false" },
          { "text": "小苏打", "correct": "true" },
          { "text": "白糖", "correct": "false" },
          { "text": "奶油", "correct": "false" },
        ]
      },
      {
        "question": "哪一种中医疗法可以替代麻醉？",
        "answers": [
          { "text": "刮痧", "correct": "false" },
          { "text": "拔火罐", "correct": "false" },
          { "text": "针灸", "correct": "true" },
          { "text": "艾灸", "correct": "false" },
        ]
      },
      {
        "question": "罗伊·莱弗Royal Rife博士发明的可以治疗癌症的装置是用什么来进行治疗的？",
        "answers": [
          { "text": "频率", "correct": "true" },
          { "text": "精油", "correct": "false" },
          { "text": "红外线", "correct": "false" },
          { "text": "特殊的硬水", "correct": "false" },
        ]
      },
      {
        "question": "一种具有争议的抗癌药物芬苯达唑粉Fenbendazole，本来的用途是？",
        "answers": [
          { "text": "安眠药", "correct": "false" },
          { "text": "兽药", "correct": "true" },
          { "text": "痔疮药", "correct": "false" },
          { "text": "眼睛药", "correct": "false" },
        ]
      },
      {
        "question": "帮助增强记忆力的精油是哪一种？",
        "answers": [
          { "text": "薄荷", "correct": "false" },
          { "text": "玫瑰", "correct": "false" },
          { "text": "乳香", "correct": "false" },
          { "text": "迷迭香", "correct": "true" },
        ]
      },
      {
        "question": "一种存在于苦杏仁、杏核中的毒素，但同时也被称为具有抗癌作用的物质，俗称是？",
        "answers": [
          { "text": "苯甲醛", "correct": "false" },
          { "text": "蛋白激酶", "correct": "false" },
          { "text": "姜黄素", "correct": "false" },
          { "text": "维生素B17", "correct": "true" },
        ]
      },
      {
        "question": "DMSO是从什么物质提取？",
        "answers": [
          { "text": "树木", "correct": "true" },
          { "text": "海藻", "correct": "false" },
          { "text": "棉花", "correct": "false" },
          { "text": "石油", "correct": "false" },
        ]
      },
      {
        "question": "推出蓖麻油疗法的特异功能者是谁？",
        "answers": [
          { "text": "爱德加·凯西 Edgar Cayce", "correct": "true" },
          { "text": "沃尔夫·梅辛 Wolf Messing", "correct": "false" },
          { "text": "大卫·科波菲尔 David Copperfield", "correct": "false" },
          { "text": "王林", "correct": "false" },
        ]
      },
      {
        "question": "油拔法中常见的帮助口腔保健的油是以下哪一种？",
        "answers": [
          { "text": "橄榄油", "correct": "false" },
          { "text": "葵花油", "correct": "false" },
          { "text": "椰子油", "correct": "true" },
          { "text": "花生油", "correct": "false" },
        ]
      }
    ],
    "shanhaijing": [
      {
        "question": "《山海经》中描述的一场与《圣经》中的故事及其相似的大灾难是什么？",
        "answers": [
          { "text": "大洪水", "correct": "true" },
          { "text": "大火灾", "correct": "false" },
          { "text": "大地震", "correct": "false" },
          { "text": "陨石坠落", "correct": "false" },
        ]
      },
      {
        "question": "新疆出土的伏羲女娲图所描绘的形状特征与人体的哪一个部分极其相似？",
        "answers": [
          { "text": "干细胞结构", "correct": "false" },
          { "text": "左右脑结构", "correct": "false" },
          { "text": "DNA结构", "correct": "true" },
          { "text": "心室结构", "correct": "false" },
        ]
      },
      {
        "question": "三星堆出土的纵目面具有可能指的是《山海经》中的哪位神灵？",
        "answers": [
          { "text": "钦䲹", "correct": "false" },
          { "text": "烛龙/烛阴", "correct": "true" },
          { "text": "陆吾", "correct": "false" },
          { "text": "盘古", "correct": "false" },
        ]
      },
      {
        "question": "《山海经》对怪兽饕餮的描述中，哪一点与西方撒旦的特征及其相似？",
        "answers": [
          { "text": "猪耳朵", "correct": "false" },
          { "text": "独角兽", "correct": "false" },
          { "text": "羊身", "correct": "true" },
          { "text": "龙头", "correct": "false" },
        ]
      },
      {
        "question": "《山海经》中太阳栖息的树木叫什么？",
        "answers": [
          { "text": "建木", "correct": "false" },
          { "text": "扶桑", "correct": "true" },
          { "text": "若木", "correct": "false" },
          { "text": "槐树", "correct": "false" },
        ]
      },
      {
        "question": "《山海经》中没有描述的古代神话故事是哪一篇？",
        "answers": [
          { "text": "《后羿射日》", "correct": "true" },
          { "text": "《女娲造人》", "correct": "false" },
          { "text": "《夸父逐日》", "correct": "false" },
          { "text": "《嫦娥奔月》", "correct": "false" },
        ]
      },
      {
        "question": "神仙居住的山是哪一座山？",
        "answers": [
          { "text": "黄山", "correct": "false" },
          { "text": "花果山", "correct": "false" },
          { "text": "嵩山", "correct": "false" },
          { "text": "昆仑山", "correct": "true" },
        ]
      },
      {
        "question": "太阳母亲羲和驾着龙车驮着太阳金乌的形象与其他地方的哪位神相似？",
        "answers": [
          { "text": "古希腊神赫拉 Hera", "correct": "false" },
          { "text": "古希腊神赫利俄斯 Helios", "correct": "true" },
          { "text": "古埃及神伊西斯 Isis", "correct": "false" },
          { "text": "古日本神天照大神", "correct": "false" },
        ]
      },
      {
        "question": "《山海经》中的夔牛的身体被黄帝做了什么乐器？",
        "answers": [
          { "text": "琵琶", "correct": "false" },
          { "text": "鼓槌", "correct": "false" },
          { "text": "号角", "correct": "false" },
          { "text": "战鼓", "correct": "true" },
        ]
      },
      {
        "question": "女娲身上的哪一个部分化为了十位神仙？",
        "answers": [
          { "text": "肠子", "correct": "true" },
          { "text": "头发", "correct": "false" },
          { "text": "手指", "correct": "false" },
          { "text": "眼睛", "correct": "false" },
        ]
      }
    ],
    "pyramid": [
      {
        "question": "2023年3月，研究人员在古埃及吉萨金字塔附近发现了什么？",
        "answers": [
          { "text": "地下金字塔", "correct": "false" },
          { "text": "秘密通道", "correct": "true" },
          { "text": "木乃伊", "correct": "false" },
          { "text": "经卷", "correct": "false" },
        ]
      },
      {
        "question": "埃及三大金字塔的位置布局与什么星座的哪一个部位对应？",
        "answers": [
          { "text": "猎户座腰带", "correct": "true" },
          { "text": "天蝎座身躯", "correct": "false" },
          { "text": "狮子座鬃毛", "correct": "false" },
          { "text": "金牛座头角", "correct": "false" },
        ]
      },
      {
        "question": "“中国金字塔”的位置与以下哪一个城市最近？",
        "answers": [
          { "text": "开封", "correct": "false" },
          { "text": "成都", "correct": "false" },
          { "text": "西安", "correct": "true" },
          { "text": "沈阳", "correct": "false" },
        ]
      },
      {
        "question": "目前发现的世界上最大的金字塔在哪里？",
        "answers": [
          { "text": "埃及", "correct": "false" },
          { "text": "墨西哥", "correct": "true" },
          { "text": "中国", "correct": "false" },
          { "text": "南极", "correct": "false" },
        ]
      },
      {
        "question": "祭祀羽蛇神的金字塔大部分都集中坐落在哪一个地区？",
        "answers": [
          { "text": "中南美", "correct": "true" },
          { "text": "东南亚", "correct": "false" },
          { "text": "埃及", "correct": "false" },
          { "text": "阿拉斯加", "correct": "false" },
        ]
      },
      {
        "question": "胡夫金字塔的哪一个重要部分失踪了？",
        "answers": [
          { "text": "没有任何部分失踪，都完好保存", "correct": "false" },
          { "text": "国王墓室的石门", "correct": "false" },
          { "text": "描述内部的古图纸", "correct": "false" },
          { "text": "顶石", "correct": "true" },
        ]
      },
      {
        "question": "以下的哪一个博物馆·美术馆有玻璃金字塔？",
        "answers": [
          { "text": "卢浮宫博物馆", "correct": "true" },
          { "text": "史密森尼博物馆", "correct": "false" },
          { "text": "大英博物馆", "correct": "false" },
          { "text": "冬宫博物馆", "correct": "false" },
        ]
      },
      {
        "question": "以下建材中，不属于埃及金字塔主要建材的是哪一种？",
        "answers": [
          { "text": "大理石", "correct": "true" },
          { "text": "石灰石", "correct": "false" },
          { "text": "砂浆", "correct": "false" },
          { "text": "花岗石", "correct": "false" },
        ]
      },
      {
        "question": "将胡夫金字塔的塔高乘上10亿，恰好是地球到哪里的距离？",
        "answers": [
          { "text": "月球", "correct": "false" },
          { "text": "太阳", "correct": "true" },
          { "text": "火星", "correct": "false" },
          { "text": "金星", "correct": "false" },
        ]
      },
      {
        "question": "大金字塔的高度乘以43200等于什么长度？",
        "answers": [
          { "text": "地球与月亮的距离", "correct": "false" },
          { "text": "地球至太阳的距离", "correct": "false" },
          { "text": "地球的极半径", "correct": "true" },
          { "text": "地球的周长", "correct": "false" },
        ]
      }
    ],
    "timespace": [
      {
        "question": "1943年举行的费城实验把什么东西突然之间横空消失？",
        "answers": [
          { "text": "军舰", "correct": "true" },
          { "text": "战斗机", "correct": "false" },
          { "text": "坦克", "correct": "false" },
          { "text": "大炮", "correct": "false" },
        ]
      },
      {
        "question": "穿越时空的飞马计划将一名男童送到了哪一个著名历史现场？",
        "answers": [
          { "text": "拿破仑加冕仪式", "correct": "false" },
          { "text": "林肯的葛底斯堡演说", "correct": "true" },
          { "text": "哥伦布发现美洲", "correct": "false" },
          { "text": "达芬奇绘制莫娜丽莎", "correct": "false" },
        ]
      },
      {
        "question": "人类文明在卡尔达舍夫指数中目前属于哪一级别？",
        "answers": [
          { "text": "I级", "correct": "false" },
          { "text": "II级", "correct": "false" },
          { "text": "III级", "correct": "false" },
          { "text": "I级未满", "correct": "true" },
        ]
      },
      {
        "question": "一种包围母恒星的，可以捕获大部分或全部恒星能量输出的巨大结构名称是什么？",
        "answers": [
          { "text": "凯森球", "correct": "false" },
          { "text": "戴森球", "correct": "true" },
          { "text": "派森球", "correct": "false" },
          { "text": "莱森球", "correct": "false" },
        ]
      },
      {
        "question": "窥镜(Looking-Glass)计划的主要目的是什么？",
        "answers": [
          { "text": "预测未来", "correct": "true" },
          { "text": "穿越时空", "correct": "false" },
          { "text": "通讯监察", "correct": "false" },
          { "text": "气象操作", "correct": "false" },
        ]
      },
      {
        "question": "造翼者Wingmakers来自哪里的什么人？",
        "answers": [
          { "text": "太空的外星人", "correct": "false" },
          { "text": "不同维度的灵体", "correct": "false" },
          { "text": "未来的地球人", "correct": "true" },
          { "text": "地心的地球人", "correct": "false" },
        ]
      },
      {
        "question": "传说2003年伊拉克战争的秘密目的是？",
        "answers": [
          { "text": "寻找伊甸园的秘密通道", "correct": "false" },
          { "text": "夺取藏在巴格达地下的電磁脈衝武器", "correct": "false" },
          { "text": "夺取藏在伊拉克的大脚怪", "correct": "false" },
          { "text": "掌控星门", "correct": "true" },
        ]
      },
      {
        "question": "传说瑞士的哪一家机构在尝试打开时空黑洞之门？",
        "answers": [
          { "text": "CERN", "correct": "true" },
          { "text": "WHO", "correct": "false" },
          { "text": "UN", "correct": "false" },
          { "text": "WEF", "correct": "false" },
        ]
      },
      {
        "question": "根据泄密人提供的信息，奥巴马在年轻时通过什么设施被派去了火星基地？",
        "answers": [
          { "text": "阅读室", "correct": "false" },
          { "text": "催眠室", "correct": "false" },
          { "text": "跳跃室", "correct": "true" },
          { "text": "电话亭", "correct": "false" },
        ]
      },
      {
        "question": "使用阴阳符号的卦象来推演世间万物的运行状态以及时空运转的中国古典文献名称是？",
        "answers": [
          { "text": "《黄帝内经》", "correct": "false" },
          { "text": "《脉经》", "correct": "false" },
          { "text": "《易经》", "correct": "true" },
          { "text": "《诗经》", "correct": "false" },
        ]
      }
    ],
    "moon": [
      {
        "question": "著名导演斯坦利·库布里克在他的哪一部电影中暗示了他是受命制作了虚假登月特效的？",
        "answers": [
          { "text": "《2001太空漫游 2001: A Space Odyssey》", "correct": "false" },
          { "text": "《闪灵 Shining》", "correct": "true" },
          { "text": "《大开眼戒 Eyes Wide Shut》", "correct": "false" },
          { "text": "《斯巴达克斯 Spartacus》", "correct": "false" },
        ]
      },
      {
        "question": "1975年2月，透过遥视看到了月球背面的一些建筑物以及高大人形生物的著名超能力者是？",
        "answers": [
          { "text": "爱德加·凯西 Edgar Cayce", "correct": "false" },
          { "text": "尤里·盖勒 Uri Geller", "correct": "false" },
          { "text": "迪克·阿加 Dick Allgire", "correct": "false" },
          { "text": "英各·斯旺 Ingo Swann", "correct": "true" },
        ]
      },
      {
        "question": "根据大卫·艾克David Icke的说法，蜥蜴人在月球上的装置对地球人类起到了什么效果？",
        "answers": [
          { "text": "将人类的认知能力限制在3维内", "correct": "true" },
          { "text": "将人类的认知能力从2维提升到3维", "correct": "false" },
          { "text": "给人类设置生理周期", "correct": "false" },
          { "text": "缓冲太阳辐射的强度", "correct": "false" },
        ]
      },
      {
        "question": "根据威廉·汤普金斯(William Tompkins)的揭秘，阿波罗11号在月球上看到了什么？",
        "answers": [
          { "text": "外星宇宙飞船", "correct": "true" },
          { "text": "森林", "correct": "false" },
          { "text": "嫦娥", "correct": "false" },
          { "text": "恐龙", "correct": "false" },
        ]
      },
      {
        "question": "哪一部中国古代书籍中记载了从月球穿越来的修月工的故事？",
        "answers": [
          { "text": "《山海经》", "correct": "false" },
          { "text": "《聊斋志异》", "correct": "false" },
          { "text": "《酉阳杂俎》", "correct": "true" },
          { "text": "《博物志》", "correct": "false" },
        ]
      },
      {
        "question": "根据《国家地理》2018年报道，科学家们发现地球一共有多少个卫星？",
        "answers": [
          { "text": "2个", "correct": "false" },
          { "text": "3个", "correct": "true" },
          { "text": "5个", "correct": "false" },
          { "text": "10个", "correct": "false" },
        ]
      },
      {
        "question": "根据蒙托克项目揭秘人斯图尔特·斯瓦洛Stewart Swerdlow的揭露，月球是什么人带来的？",
        "answers": [
          { "text": "火星人", "correct": "false" },
          { "text": "天龙座人", "correct": "true" },
          { "text": "天琴座人", "correct": "false" },
          { "text": "大角星人", "correct": "false" },
        ]
      },
      {
        "question": "以下哪一位的名字来自罗马神话中的月亮女神？",
        "answers": [
          { "text": "黛安娜王妃", "correct": "true" },
          { "text": "奥德丽·赫本", "correct": "false" },
          { "text": "纽约自由女神", "correct": "false" },
          { "text": "安吉丽娜·朱莉", "correct": "false" },
        ]
      },
      {
        "question": "当阿波罗12号的约翰·杨被要求把手放在圣经上发誓他真的去过月球，他的反应是？",
        "answers": [
          { "text": "非常坦然地将手放在圣经上做了发誓", "correct": "false" },
          { "text": "开怀笑说自己是无神论者，所以不发誓", "correct": "false" },
          { "text": "承认自己没有真正登陆月球", "correct": "false" },
          { "text": "非常不高兴并尝试甩开发问者的追问", "correct": "true" },
        ]
      },
      {
        "question": "月行迹所描绘的形状是？",
        "answers": [
          { "text": "椭圆0字形", "correct": "false" },
          { "text": "正圆形", "correct": "false" },
          { "text": "8字形", "correct": "true" },
          { "text": "一条线", "correct": "false" },
        ]
      }
    ]
    },
  "ja": { 
    "humanity": [
      {
        "question": "2023年に高校の教科書から進化論を削除した国は?",
        "answers": [
          { "text": "ベトナム", "correct": "false" },
          { "text": "スロバキア", "correct": "false" },
          { "text": "インド", "correct": "true" },
          { "text": "南アフリカ", "correct": "false" },
        ]
      },
      {
        "question": "DNA二重らせん構造の発見者によって1973年に発表された理論とは?",
        "answers": [
          { "text": "生命起源論", "correct": "false" },
          { "text": "進化論", "correct": "false" },
          { "text": "RNAワールド", "correct": "false" },
          { "text": "パンスペルミア", "correct": "true" },
        ]
      },
      {
        "question": "人間の染色体は46本ですが、ゴリラの染色体は何本?",
        "answers": [
          { "text": "48本", "correct": "true" },
          { "text": "46本", "correct": "false" },
          { "text": "44本", "correct": "false" },
          { "text": "52本", "correct": "false" },
        ]
      },
      {
        "question": "人類に遺伝子操作を施したと古代シュメール文献の記述にあるのは誰?",
        "answers": [
          { "text": "エスキモー", "correct": "false" },
          { "text": "アヌンナキ", "correct": "true" },
          { "text": "レプタリアン", "correct": "false" },
          { "text": "シリウス星人", "correct": "false" },
        ]
      },
      {
        "question": "現在の人類文明が地球外生命体によって作られたという説の名は?",
        "answers": [
          { "text": "古代エイリアン説", "correct": "false" },
          { "text": "古代宇宙飛行士説", "correct": "true" },
          { "text": "古代科学者説", "correct": "false" },
          { "text": "古代開拓者説", "correct": "false" },
        ]
      },
      {
        "question": "アトランティス文明はどの哲学者の作品に登場しますか?",
        "answers": [
          { "text": "ソクラテス", "correct": "false" },
          { "text": "ニーチェ", "correct": "false" },
          { "text": "ショーペンハウアー", "correct": "false" },
          { "text": "プラトン", "correct": "true" },
        ]
      },
      {
        "question": "次の古代文献のうち、女媧の物語が記録されていないのはどれ?",
        "answers": [
          { "text": "『山海経』", "correct": "false" },
          { "text": "『漢書』", "correct": "false" },
          { "text": "『風俗通義』", "correct": "false" },
          { "text": "『孫子の兵法』", "correct": "true" },
        ]
      },
      {
        "question": "インド神話に登場する人類の祖先の名前は?",
        "answers": [
          { "text": "マヌ", "correct": "true" },
          { "text": "ブラフマー", "correct": "false" },
          { "text": "シヴァ", "correct": "false" },
          { "text": "ヴィシュヌ神", "correct": "false" },
        ]
      },
      {
        "question": "今から約3～4万年前、忽然と地球上から姿を消した古代人類は？",
        "answers": [
          { "text": "ホモ・エレクトス", "correct": "false" },
          { "text": "ハイデルベルゲンシス", "correct": "false" },
          { "text": "ネアンデルタール", "correct": "true" },
          { "text": "北京原人", "correct": "false" },
        ]
      },
      {
        "question": "主流科学に「ジャンク遺伝子」と呼ばれているものがDNAに占める割合はどれくらい?",
        "answers": [
          { "text": "78~80%", "correct": "false" },
          { "text": "95~98%", "correct": "true" },
          { "text": "12~15%", "correct": "false" },
          { "text": "3~5%", "correct": "false" },
        ]
      }
    ],
    "underground": [
      {
        "question": "古代の文献に記されている地底世界の名前は?",
        "answers": [
          { "text": "タルタリア Tartariaa", "correct": "false" },
          { "text": "アガルタ Agartha", "correct": "true" },
          { "text": "レムリア Lemuria", "correct": "false" },
          { "text": "アトランティス Atlantis", "correct": "false" },
        ]
      },
      {
        "question": "1938年と1943年、ヒトラーナチスは地下都市を目指した遠征隊をどこに送ったのでしょうか?",
        "answers": [
          { "text": "シベリア Siberia", "correct": "false" },
          { "text": "西安 Xi-An", "correct": "false" },
          { "text": "東ティモール East Timor", "correct": "false" },
          { "text": "チベット Tibet", "correct": "true" },
        ]
      },
      {
        "question": "伝えられるところによると、ヒトラーナチスの地下逃亡基地はどこですか?",
        "answers": [
          { "text": "南極", "correct": "true" },
          { "text": "北極", "correct": "false" },
          { "text": "サハラ砂漠", "correct": "false" },
          { "text": "ペルー", "correct": "false" },
        ]
      },
      {
        "question": "地下軍事トンネルシステムの英語の略称は何ですか?",
        "answers": [
          { "text": "D.B.U.M", "correct": "false" },
          { "text": "N.U.M.B", "correct": "false" },
          { "text": "D.U.M.B", "correct": "true" },
          { "text": "M.U.D.B", "correct": "false" },
        ]
      },
      {
        "question": "地下で行われる軍事作戦の主な目的は?",
        "answers": [
          { "text": "レプタリアンに捕らえられた友好的なエイリアンの救出", "correct": "false" },
          { "text": "密輸された希少動物を救出する", "correct": "false" },
          { "text": "人身売買された人間の子供たちを救出する", "correct": "true" },
          { "text": "地下取引で盗まれた金塊を取り戻す", "correct": "false" },
        ]
      },
      {
        "question": "地下軍事作戦に関連した地震の震源の深さは大抵どれくらい?",
        "answers": [
          { "text": "～10km", "correct": "true" },
          { "text": "10～15km", "correct": "false" },
          { "text": "15～20km", "correct": "false" },
          { "text": "20km～", "correct": "false" },
        ]
      },
      {
        "question": "アラスカのマッキンリー山近辺の地下で発見されたピラミッドは何色?",
        "answers": [
          { "text": "土色", "correct": "false" },
          { "text": "金色", "correct": "false" },
          { "text": "白色", "correct": "false" },
          { "text": "黒色", "correct": "true" },
        ]
      },
      {
        "question": "2003年に、山の中に謎の地下洞窟を発見したヨーロッパの国は?",
        "answers": [
          { "text": "セルビア", "correct": "false" },
          { "text": "ルーマニア", "correct": "true" },
          { "text": "クロアチア", "correct": "false" },
          { "text": "ブルガリア", "correct": "false" },
        ]
      },
      {
        "question": "次のうち、地底世界の探検家ではないのは誰?",
        "answers": [
          { "text": "唐の時代の玄奘", "correct": "true" },
          { "text": "古代ギリシャのピティアス", "correct": "false" },
          { "text": "ノルウェーの漁師オラフ・ヤンセン父子", "correct": "false" },
          { "text": "アメリカ海軍バード少将", "correct": "false" },
        ]
      },
      {
        "question": "次のうち、伝説の地下都市はどれ?",
        "answers": [
          { "text": "天竺", "correct": "false" },
          { "text": "バビロン", "correct": "false" },
          { "text": "キーテジ", "correct": "false" },
          { "text": "シャンバラ", "correct": "true" },
        ]
      }
    ],
    "ufo": [
      {
        "question": "UFOリバースエンジニアリング研究に関与した有名な内部告発者は?",
        "answers": [
          { "text": "ボブ・ラザール Bob Lazar", "correct": "true" },
          { "text": "アレックス・コリアー Allex Collier", "correct": "false" },
          { "text": "マイケル・サラ Michael Salla", "correct": "false" },
          { "text": "フィル・シュナイダー Phil Schneider", "correct": "false" },
        ]
      },
      {
        "question": "アメリカのネバダ州にある有名なUFO基地の名前は?",
        "answers": [
          { "text": "ロズウェル Roswell", "correct": "false" },
          { "text": "モントーク空軍基地 Montauk Air Force Station", "correct": "false" },
          { "text": "エリア51 Area 51", "correct": "true" },
          { "text": "ダルセベース Dulce Base", "correct": "false" },
        ]
      },
      {
        "question": "2023年7月に米国議会のUFO公聴会で証言したデビッド・グルーシュの前職は？",
        "answers": [
          { "text": "宇宙軍士官", "correct": "false" },
          { "text": "海軍士官", "correct": "false" },
          { "text": "陸軍将校", "correct": "false" },
          { "text": "空軍士官", "correct": "true" },
        ]
      },
      {
        "question": "空飛ぶ円盤の形に加えて、地球上で頻繁に目撃される他のUFOの形は?",
        "answers": [
          { "text": "歯磨き粉チューブ形", "correct": "false" },
          { "text": "自動車形", "correct": "false" },
          { "text": "葉巻形", "correct": "true" },
          { "text": "五角形の星形", "correct": "false" },
        ]
      },
      {
        "question": "第二次世界大戦中にナチスが秘密裏に開発したタイムトラベル装置の名前が意味するものは?",
        "answers": [
          { "text": "鐘", "correct": "true" },
          { "text": "車", "correct": "false" },
          { "text": "瓶", "correct": "false" },
          { "text": "椅子", "correct": "false" },
        ]
      },
      {
        "question": "米国ワシントン上空での有名なUFO事件が起きたのは?",
        "answers": [
          { "text": "1942年", "correct": "false" },
          { "text": "1952年", "correct": "true" },
          { "text": "1947年", "correct": "false" },
          { "text": "1972年", "correct": "false" },
        ]
      },
      {
        "question": "ロズウェルに先立つ1933年のUFO墜落事故があった国はどこ?",
        "answers": [
          { "text": "メキシコ", "correct": "false" },
          { "text": "イタリア", "correct": "true" },
          { "text": "スペイン", "correct": "false" },
          { "text": "スペイン", "correct": "false" },
        ]
      },
      {
        "question": "ブラックテクノロジーでリバースエンジニアリングされたとされる反重力航空機の名前は?",
        "answers": [
          { "text": "F-22", "correct": "false" },
          { "text": "Ki-100", "correct": "false" },
          { "text": "MiG-29", "correct": "false" },
          { "text": "TR-3B", "correct": "true" },
        ]
      },
      {
        "question": "次の絵画のうち、UFOを描いていないのはどれ?",
        "answers": [
          { "text": "アールト・デ・ヘルデルの『キリストの洗礼』", "correct": "false" },
          { "text": "ヴェッキオ宮殿の聖母の肖像", "correct": "false" },
          { "text": "ゴッホの『星月夜』", "correct": "true" },
          { "text": "セルビア正教会の絵画", "correct": "false" },
        ]
      },
      {
        "question": "2003年、反重力燃料「エレメント115」を人工合成したのはどこの国の科学者？",
        "answers": [
          { "text": "ロシア", "correct": "true" },
          { "text": "アメリカ", "correct": "false" },
          { "text": "インド", "correct": "false" },
          { "text": "中国", "correct": "false" },
        ]
      }
    ],
    "jab": [
      {
        "question": "2024年1月、保健局長がmRNAワクチンの使用の一時停止を求めたのは米国のどの州?",
        "answers": [
          { "text": "カリフォルニア州", "correct": "false" },
          { "text": "フロリダ州", "correct": "true" },
          { "text": "テキサス州", "correct": "false" },
          { "text": "ニューヨーク州", "correct": "false" },
        ]
      },
      {
        "question": "人間へのワクチン接種の義務化が抵触している国際規範は?",
        "answers": [
          { "text": "ブレトンウッズ体制", "correct": "false" },
          { "text": "京都議定書", "correct": "false" },
          { "text": "ニュルンベルク綱領", "correct": "true" },
          { "text": "生物兵器禁止条約", "correct": "false" },
        ]
      },
      {
        "question": "新型コロナワクチンに含まれる「グラフェン」と呼ばれる物質は、体にどのような変化をもたらすでしょうか？",
        "answers": [
          { "text": "体の磁石化", "correct": "true" },
          { "text": "不眠を引き起こす", "correct": "false" },
          { "text": "体温を上昇させる", "correct": "false" },
          { "text": "食欲を増進させる", "correct": "false" },
        ]
      },
      {
        "question": "周りで新型コロナワクチン接種を受けた人を検出する携帯電話機能は?",
        "answers": [
          { "text": "QRコードのスキャン機能", "correct": "false" },
          { "text": "Wi-Fi機能", "correct": "false" },
          { "text": "4G機能", "correct": "false" },
          { "text": "ブルートゥース機能", "correct": "true" },
        ]
      },
      {
        "question": "ワクチン接種率が非常に低いアーミッシュにほとんど存在しない病気は?",
        "answers": [
          { "text": "風邪", "correct": "false" },
          { "text": "肥満症", "correct": "false" },
          { "text": "自閉症", "correct": "true" },
          { "text": "糖尿病", "correct": "false" },
        ]
      },
      {
        "question": "世界人口へのワクチン接種に最も情熱を注いでいる大手テック企業の起業家は?",
        "answers": [
          { "text": "馬化騰", "correct": "false" },
          { "text": "ジャック・マー（馬雲）", "correct": "false" },
          { "text": "イーロン・マスク", "correct": "false" },
          { "text": "ビル・ゲイツ", "correct": "true" },
        ]
      },
      {
        "question": "次の物質のうち、ワクチンアジュバントに添加されていないものは?",
        "answers": [
          { "text": "アルミニウム", "correct": "false" },
          { "text": "金", "correct": "true" },
          { "text": "水銀", "correct": "false" },
          { "text": "グラフェン", "correct": "false" },
        ]
      },
      {
        "question": "次のうち、ワクチンによるスパイクタンパク質を除去し、血栓の溶解に最も効果的な天然酵素はどれ?",
        "answers": [
          { "text": "ナットウキナーゼ", "correct": "true" },
          { "text": "グルカナーゼ", "correct": "false" },
          { "text": "アスパラギナーゼ", "correct": "false" },
          { "text": "アミラーゼ", "correct": "false" },
        ]
      },
      {
        "question": "次のうち、日本の科学者大村智が発見した、新型コロナに効果のある薬は？",
        "answers": [
          { "text": "ケルセチン", "correct": "false" },
          { "text": "イベルメクチン", "correct": "true" },
          { "text": "ヒドロキシクロロキン", "correct": "false" },
          { "text": "ブロメライン", "correct": "false" },
        ]
      },
      {
        "question": "次の記述のうち、陰謀論界で囁かれているワクチン接種の目的に合致しないものは?",
        "answers": [
          { "text": "人口の削減", "correct": "false" },
          { "text": "トランスヒューマンミュータント実験", "correct": "false" },
          { "text": "ナノチップで「人間のインターネット」を築く", "correct": "false" },
          { "text": "公衆衛生の改善", "correct": "true" },
        ]
      }
    ],
    "ai": [
      {
        "question": "映画『2001年宇宙の旅』の中で、木星への飛行中に3人のパイロットに同行した人工知能は?",
        "answers": [
          { "text": "PAL 9000", "correct": "false" },
          { "text": "HAL 9000", "correct": "true" },
          { "text": "TAL 9000", "correct": "false" },
          { "text": "KAL 9000", "correct": "false" },
        ]
      },
      {
        "question": "市民権を獲得した最初の人工知能ロボットの名前は?",
        "answers": [
          { "text": "マリア Maria", "correct": "false" },
          { "text": "パトリシア Patricia", "correct": "false" },
          { "text": "シルビア Sylvia", "correct": "false" },
          { "text": "ソフィア Sophia", "correct": "true" },
        ]
      },
      {
        "question": "人工知能の「餌」とは何でしょうか？",
        "answers": [
          { "text": "人間", "correct": "false" },
          { "text": "プログラミングコード", "correct": "false" },
          { "text": "データ", "correct": "true" },
          { "text": "電気", "correct": "false" },
        ]
      },
      {
        "question": "アレクサ Alexaは、どの企業の人工知能の名前ですか?",
        "answers": [
          { "text": "アマゾン Amazon", "correct": "true" },
          { "text": "グーグル Google", "correct": "false" },
          { "text": "アップル Apple", "correct": "false" },
          { "text": "フェイスブック Facebook", "correct": "false" },
        ]
      },
      {
        "question": "ChatGPTはイデオロギー的にどちら寄り?",
        "answers": [
          { "text": "左派", "correct": "true" },
          { "text": "右派", "correct": "false" },
          { "text": "中立派", "correct": "false" },
          { "text": "新興宗教", "correct": "false" },
        ]
      },
      {
        "question": "初のAIチャットボットであるElizaはいつ誕生しましたか?",
        "answers": [
          { "text": "1978年", "correct": "false" },
          { "text": "2001年", "correct": "false" },
          { "text": "1947年", "correct": "false" },
          { "text": "1966年", "correct": "true" },
        ]
      },
      {
        "question": "ドキュメンタリー『Coded Bias』で言及されている「偏見」とは、どのような人工知能の瑕疵が原因で発生したもの?",
        "answers": [
          { "text": "IQの識別", "correct": "false" },
          { "text": "顔認識", "correct": "true" },
          { "text": "肥満度認識", "correct": "false" },
          { "text": "音声認識", "correct": "false" },
        ]
      },
      {
        "question": "金融市場を予測するブラックストーングループの人工知能ソフトの名前は?",
        "answers": [
          { "text": "アトム", "correct": "false" },
          { "text": "アバター", "correct": "false" },
          { "text": "アリババ", "correct": "false" },
          { "text": "アラジン", "correct": "true" },
        ]
      },
      {
        "question": "次のうち、機械が人工知能を持つかどうかを判定するテストは?",
        "answers": [
          { "text": "テンサーフロー Tensorflow", "correct": "false" },
          { "text": "メンサ Mensa", "correct": "false" },
          { "text": "チューリングテスト Turing Test", "correct": "true" },
          { "text": "ベルテスト Bell Test", "correct": "false" },
        ]
      },
      {
        "question": "ほぼ完全にロボットによって運営されている最初のホテルはどこの国のホテル?",
        "answers": [
          { "text": "日本", "correct": "true" },
          { "text": "アメリカ", "correct": "false" },
          { "text": "イスラエル", "correct": "false" },
          { "text": "インド", "correct": "false" },
        ]
      }
    ],
    "et": [
      {
        "question": "レプタリアンの血は何色?",
        "answers": [
          { "text": "緑色", "correct": "false" },
          { "text": "青色", "correct": "true" },
          { "text": "黄色", "correct": "false" },
          { "text": "赤色", "correct": "false" },
        ]
      },
      {
        "question": "『ストレンジャーズ・イン・ザ・ペンタゴン』に登場するヴァリアント・ソーはどの惑星から来たのでしょう?",
        "answers": [
          { "text": "冥王星", "correct": "false" },
          { "text": "火星", "correct": "false" },
          { "text": "月", "correct": "false" },
          { "text": "金星", "correct": "true" },
        ]
      },
      {
        "question": "1996年生まれのロシアのインディゴチャイルド、ボリスカ君はどの惑星から?",
        "answers": [
          { "text": "火星", "correct": "true" },
          { "text": "金星", "correct": "false" },
          { "text": "シリウス星", "correct": "false" },
          { "text": "土星", "correct": "false" },
        ]
      },
      {
        "question": "「The Law of One」に登場する宇宙生命体の名前は?",
        "answers": [
          { "text": "Ma", "correct": "false" },
          { "text": "Ta", "correct": "false" },
          { "text": "Ra", "correct": "true" },
          { "text": "La", "correct": "false" },
        ]
      },
      {
        "question": "1976年7月25日に探査機バイキング1号が火星で撮影した驚くべき画像とは?",
        "answers": [
          { "text": "UFO基地", "correct": "false" },
          { "text": "人間の顔に酷似した地面の隆起", "correct": "true" },
          { "text": "黒いピラミッド", "correct": "false" },
          { "text": "巨大な透明な建物", "correct": "false" },
        ]
      },
      {
        "question": "ドロレス・キャノンが2011年に書いた3つのスターシードの波のうち、第1波が地球に到達した年代は?",
        "answers": [
          { "text": "1940年代末", "correct": "true" },
          { "text": "1970年代", "correct": "false" },
          { "text": "2000年初期", "correct": "false" },
          { "text": "1960年代半ば", "correct": "false" },
        ]
      },
      {
        "question": "アイゼンハワー政権が署名した人間とETの協定にはどの異星人が関与していたのでしょうか？",
        "answers": [
          { "text": "プレアデス人", "correct": "false" },
          { "text": "グレイ", "correct": "true" },
          { "text": "ノルディック型エイリアン", "correct": "false" },
          { "text": "天龍星人", "correct": "false" },
        ]
      },
      {
        "question": "1990年代に出回った宇宙人インタビューのライブビデオを公開した人物の名前は?",
        "answers": [
          { "text": "マーク Mark", "correct": "false" },
          { "text": "ジョセフ Joseph", "correct": "false" },
          { "text": "ヴィクター Victor", "correct": "true" },
          { "text": "デービット David", "correct": "false" },
        ]
      },
      {
        "question": "古代シュメールの記録に登場するアヌンナキはどの惑星から?",
        "answers": [
          { "text": "ニビル", "correct": "true" },
          { "text": "ケンタウルス座のアルファ星", "correct": "false" },
          { "text": "ハレー彗星", "correct": "false" },
          { "text": "太陽", "correct": "false" },
        ]
      },
      {
        "question": "ヴェーダ文献に登場するヴィシュヌ神などの肌の色は何色？",
        "answers": [
          { "text": "黄金色", "correct": "false" },
          { "text": "赤色", "correct": "false" },
          { "text": "緑色", "correct": "false" },
          { "text": "青色", "correct": "true" },
        ]
      }
    ],
    "spiritual": [
      {
        "question": "ドロレス・キャノン女史やブライアン・ワイス博士などが用いた前世の記憶を取り戻す方法とは?",
        "answers": [
          { "text": "脳深部刺激療法", "correct": "false" },
          { "text": "鍼治療", "correct": "false" },
          { "text": "光療法", "correct": "false" },
          { "text": "催眠回帰療法", "correct": "true" },
        ]
      },
      {
        "question": "次のうち、輪廻転生を否定する宗教は?",
        "answers": [
          { "text": "ユダヤ教", "correct": "false" },
          { "text": "仏教", "correct": "false" },
          { "text": "キリスト教", "correct": "true" },
          { "text": "ヒンズー教", "correct": "false" },
        ]
      },
      {
        "question": "『イニシエーション』という本の主人公が古代エジプトに生きた時の身分は？",
        "answers": [
          { "text": "ファラオ", "correct": "false" },
          { "text": "女司祭", "correct": "true" },
          { "text": "女王クレオパトラ", "correct": "false" },
          { "text": "医者", "correct": "false" },
        ]
      },
      {
        "question": "仏教の三仏のうち、未来を象徴する仏は？",
        "answers": [
          { "text": "釈迦牟尼仏", "correct": "false" },
          { "text": "燃燈仏", "correct": "false" },
          { "text": "薬師仏", "correct": "false" },
          { "text": "弥勒仏", "correct": "true" },
        ]
      },
      {
        "question": "前世療法とは、患者についての何を見つけて病気を治療する方法ですか?",
        "answers": [
          { "text": "カルマ", "correct": "true" },
          { "text": "体調", "correct": "false" },
          { "text": "家系や血統", "correct": "false" },
          { "text": "趣味や嗜好", "correct": "false" },
        ]
      },
      {
        "question": "1907年に行われた科学実験によると、魂の重さは何グラム?",
        "answers": [
          { "text": "14g", "correct": "false" },
          { "text": "28g", "correct": "false" },
          { "text": "21g", "correct": "true" },
          { "text": "7g", "correct": "false" },
        ]
      },
      {
        "question": "『一なるものの法則』によると、人類は現在どの密度に属しているのでしょうか？",
        "answers": [
          { "text": "五次元", "correct": "false" },
          { "text": "三次元", "correct": "true" },
          { "text": "八次元", "correct": "false" },
          { "text": "四次元", "correct": "false" },
        ]
      },
      {
        "question": "母なる地球の周波数は?",
        "answers": [
          { "text": "7.83Hz", "correct": "true" },
          { "text": "210.42Hz", "correct": "false" },
          { "text": "183.58Hz", "correct": "false" },
          { "text": "221.23Hz", "correct": "false" },
        ]
      },
      {
        "question": "「アージュナーチャクラ」が持つスピリチュアル的な意味は何でしょう？",
        "answers": [
          { "text": "スピリチュアル性、霊能力", "correct": "false" },
          { "text": "生命のエネルギー", "correct": "false" },
          { "text": "洞察力、直感", "correct": "true" },
          { "text": "愛、感情", "correct": "false" },
        ]
      },
      {
        "question": "私たちは今、どのユガ時代にいるのでしょうか？",
        "answers": [
          { "text": "クリタユガ Krita Yuga", "correct": "false" },
          { "text": "ドヴァパラユガ Dvapara Yuga", "correct": "false" },
          { "text": "トレタユガ Treta Yuga", "correct": "false" },
          { "text": "カリユガ Kali Yuga", "correct": "true" },
        ]
      },
    ],
    "healing": [
      {
        "question": "サウンドセラピーの「ゴングヒーリング」で使用される古代中国の楽器は?",
        "answers": [
          { "text": "箫の笛", "correct": "false" },
          { "text": "古琴", "correct": "false" },
          { "text": "笛", "correct": "false" },
          { "text": "銅鑼", "correct": "true" },
        ]
      },
      {
        "question": "ケーキの材料として知られ、薬効があり、体をアルカリ性にするものは？",
        "answers": [
          { "text": "ベーキングパウダー", "correct": "false" },
          { "text": "ベーキングソーダ", "correct": "true" },
          { "text": "砂糖", "correct": "false" },
          { "text": "生クリーム", "correct": "false" },
        ]
      },
      {
        "question": "麻酔に代わる伝統的な中国医学の方法はどれ?",
        "answers": [
          { "text": "刮痧（カッサ）", "correct": "false" },
          { "text": "拔罐 (カッピング療法)", "correct": "false" },
          { "text": "鍼", "correct": "true" },
          { "text": "艾（もぐさ）灸", "correct": "false" },
        ]
      },
      {
        "question": "ロイヤル・ライフ博士が発明したガンの治療に使用される装置は何に基づくもの?",
        "answers": [
          { "text": "波動", "correct": "true" },
          { "text": "エッセンシャルオイル", "correct": "false" },
          { "text": "赤外線", "correct": "false" },
          { "text": "特殊の硬水", "correct": "false" },
        ]
      },
      {
        "question": "抗がん剤かもしれないと物議を醸している「フェンベンダゾール」、その本来の用途は?",
        "answers": [
          { "text": "睡眠薬", "correct": "false" },
          { "text": "動物用医薬品", "correct": "true" },
          { "text": "坐薬", "correct": "false" },
          { "text": "目薬", "correct": "false" },
        ]
      },
      {
        "question": "記憶力を高めるのに役立つエッセンシャルオイルはどれ?",
        "answers": [
          { "text": "ミント", "correct": "false" },
          { "text": "ローズ", "correct": "false" },
          { "text": "フランキンセンス", "correct": "false" },
          { "text": "ローズマリー", "correct": "true" },
        ]
      },
      {
        "question": "苦杏仁やアプリコット仁に含まれる毒素で、抗がん作用があることも知られているものは?",
        "answers": [
          { "text": "ベンズアルデヒド", "correct": "false" },
          { "text": "プロテインキナーゼ", "correct": "false" },
          { "text": "クルクミン", "correct": "false" },
          { "text": "ビタミンB17", "correct": "true" },
        ]
      },
      {
        "question": "DMSOはどのような物質から抽出されたもの?",
        "answers": [
          { "text": "樹木", "correct": "true" },
          { "text": "海藻", "correct": "false" },
          { "text": "綿花", "correct": "false" },
          { "text": "石油", "correct": "false" },
        ]
      },
      {
        "question": "ヒマシ油療法を導入した霊能者は誰?",
        "answers": [
          { "text": "エドガー・ケイシー Edgar Cayce", "correct": "true" },
          { "text": "ウルフ・メッシング Wolf Messing", "correct": "false" },
          { "text": "デイビット・カッパーフィールド David Copperfield", "correct": "false" },
          { "text": "王林", "correct": "false" },
        ]
      },
      {
        "question": "次のうち、口腔の健康を助けるためにオイルプリングで一般的に使用されるオイルは?",
        "answers": [
          { "text": "オリーブオイル", "correct": "false" },
          { "text": "ひまわり油", "correct": "false" },
          { "text": "ココナッツオイル", "correct": "true" },
          { "text": "ピーナッツ油", "correct": "false" },
        ]
      }
    ],
    "shanhaijing": [
      {
        "question": "『山海経』に記されている、聖書の物語と似た大災害とは？",
        "answers": [
          { "text": "大洪水", "correct": "true" },
          { "text": "大火災", "correct": "false" },
          { "text": "大地震", "correct": "false" },
          { "text": "隕石墜落", "correct": "false" },
        ]
      },
      {
        "question": "新疆で発掘された伏羲と女媧の壁画に描かれた絵の形は、人体のどの部分に酷似しているのでしょうか？",
        "answers": [
          { "text": "幹細胞の構造", "correct": "false" },
          { "text": "左脳と右脳の構造", "correct": "false" },
          { "text": "DNA構造", "correct": "true" },
          { "text": "心室構造", "correct": "false" },
        ]
      },
      {
        "question": "三星堆から出土した縦目仮面は『山海経』に登場するどの神を指しているのでしょうか？",
        "answers": [
          { "text": "欽䲹", "correct": "false" },
          { "text": "燭龍・燭陰", "correct": "true" },
          { "text": "陸吾", "correct": "false" },
          { "text": "盤古", "correct": "false" },
        ]
      },
      {
        "question": "『山海経』に登場する怪物「饕餮」に関する描写で、西洋のサタンの特徴と似ているところは?",
        "answers": [
          { "text": "豚の耳", "correct": "false" },
          { "text": "ユニコーンの角", "correct": "false" },
          { "text": "羊の体", "correct": "true" },
          { "text": "竜の頭部", "correct": "false" },
        ]
      },
      {
        "question": "『山海経』の中で太陽が住む木の名前は？",
        "answers": [
          { "text": "建木", "correct": "false" },
          { "text": "扶桑", "correct": "true" },
          { "text": "若木", "correct": "false" },
          { "text": "槐樹", "correct": "false" },
        ]
      },
      {
        "question": "『山海経』に記載されていない古代の神話物語はどれ?",
        "answers": [
          { "text": "『后羿射日』", "correct": "true" },
          { "text": "『女娲造人』", "correct": "false" },
          { "text": "『夸父逐日』", "correct": "false" },
          { "text": "『嫦娥奔月』", "correct": "false" },
        ]
      },
      {
        "question": "神々が住むと言われる山の名前は？",
        "answers": [
          { "text": "黄山", "correct": "false" },
          { "text": "花果山", "correct": "false" },
          { "text": "嵩山", "correct": "false" },
          { "text": "崑崙山", "correct": "true" },
        ]
      },
      {
        "question": "太陽の母である羲和が、太陽の黄金の烏を乗せた龍車を駆る姿は、どの神と酷似しているのでしょうか?",
        "answers": [
          { "text": "古代ギリシャの女神ヘラ Hera", "correct": "false" },
          { "text": "古代ギリシャの神ヘリオス Helios", "correct": "true" },
          { "text": "古代エジプトの神イシス Isis", "correct": "false" },
          { "text": "古代日本の神、天照大神", "correct": "false" },
        ]
      },
      {
        "question": "『山海経』に登場する夔牛の体を使って、黄帝は何の楽器を作ったのでしょうか？",
        "answers": [
          { "text": "琵琶", "correct": "false" },
          { "text": "ドラムスティック", "correct": "false" },
          { "text": "ホーン", "correct": "false" },
          { "text": "陣太鼓", "correct": "true" },
        ]
      },
      {
        "question": "女媧の体のどの部分が十神に変化したのでしょうか？",
        "answers": [
          { "text": "腸", "correct": "true" },
          { "text": "髪の毛", "correct": "false" },
          { "text": "手の指", "correct": "false" },
          { "text": "目", "correct": "false" },
        ]
      }
    ],
    "pyramid": [
      {
        "question": "2023年3月、研究者たちは古代エジプトのギザのピラミッド近くで何を発見しましたか?",
        "answers": [
          { "text": "地下のピラミッド", "correct": "false" },
          { "text": "秘密の通路", "correct": "true" },
          { "text": "ミイラ", "correct": "false" },
          { "text": "経典", "correct": "false" },
        ]
      },
      {
        "question": "エジプトの３大ピラミッドの位置は、どの星座のどの部分とピッタリ当てはまるのでしょうか？",
        "answers": [
          { "text": "オリオン座のベルト部分", "correct": "true" },
          { "text": "蠍座の体の部分", "correct": "false" },
          { "text": "獅子座の立て髪部分", "correct": "false" },
          { "text": "牡牛座の角部分", "correct": "false" },
        ]
      },
      {
        "question": "次のうち、「中国のピラミッド」に一番近い都市は?",
        "answers": [
          { "text": "開封", "correct": "false" },
          { "text": "成都", "correct": "false" },
          { "text": "西安", "correct": "true" },
          { "text": "瀋陽", "correct": "false" },
        ]
      },
      {
        "question": "これまでに世界で発見された最大のピラミッドはどこにありますか?",
        "answers": [
          { "text": "エジプト", "correct": "false" },
          { "text": "メキシコ", "correct": "true" },
          { "text": "中国", "correct": "false" },
          { "text": "南極", "correct": "false" },
        ]
      },
      {
        "question": "ケツァルコアトルを祀ったピラミッドの多くはどの地域にありますか?",
        "answers": [
          { "text": "中南米", "correct": "true" },
          { "text": "東南アジア", "correct": "false" },
          { "text": "エジプト", "correct": "false" },
          { "text": "アラスカ", "correct": "false" },
        ]
      },
      {
        "question": "クフ王のピラミッドに欠けている重要な部分は?",
        "answers": [
          { "text": "何も欠落しておらず、すべて完璧に保存されている", "correct": "false" },
          { "text": "ファラオの墓室の石の扉", "correct": "false" },
          { "text": "内部設計を描いた古代の図面", "correct": "false" },
          { "text": "キャップストーン", "correct": "true" },
        ]
      },
      {
        "question": "次の博物館や美術館で、ガラスのピラミッドがあるのはどれ?",
        "answers": [
          { "text": "ルーブル美術館", "correct": "true" },
          { "text": "スミソニアン博物館", "correct": "false" },
          { "text": "大英博物館", "correct": "false" },
          { "text": "エルミタージュ美術館", "correct": "false" },
        ]
      },
      {
        "question": "次の建築材料のうち、エジプトのピラミッドの主な建築材料ではないのは?",
        "answers": [
          { "text": "大理石", "correct": "true" },
          { "text": "石灰岩", "correct": "false" },
          { "text": "モルタル", "correct": "false" },
          { "text": "花崗岩", "correct": "false" },
        ]
      },
      {
        "question": "クフ王のピラミッドの高さを10億倍すると、地球からどこまでの距離に一致しますか?",
        "answers": [
          { "text": "月", "correct": "false" },
          { "text": "太陽", "correct": "true" },
          { "text": "火星", "correct": "false" },
          { "text": "金星", "correct": "false" },
        ]
      },
      {
        "question": "大ピラミッドの長さ X 43,200倍は、何の長さと一致しますか?",
        "answers": [
          { "text": "地球と月の間の距離", "correct": "false" },
          { "text": "地球から太陽までの距離", "correct": "false" },
          { "text": "地球の極半径", "correct": "true" },
          { "text": "地球の直径", "correct": "false" },
        ]
      }
    ],
    "timespace": [
      {
        "question": "1943年のフィラデルフィア実験の場所から突然消失したのは?",
        "answers": [
          { "text": "軍艦", "correct": "true" },
          { "text": "戦闘機", "correct": "false" },
          { "text": "戦車", "correct": "false" },
          { "text": "大砲", "correct": "false" },
        ]
      },
      {
        "question": "タイムトラベルのペガサスプロジェクトが少年を送ったとされる歴史上の有名な場面は？",
        "answers": [
          { "text": "ナポレオンの戴冠式", "correct": "false" },
          { "text": "リンカーン大統領のゲティスバーグ演説現場", "correct": "true" },
          { "text": "コロンブスのアメリカ大陸の発見するところ", "correct": "false" },
          { "text": "レオナルド・ダ・ヴィンチがモナ・リザを描くところ", "correct": "false" },
        ]
      },
      {
        "question": "人類文明は現在、カルダシェフ指数のどのタイプに属していますか?",
        "answers": [
          { "text": "タイプ I", "correct": "false" },
          { "text": "タイプ II", "correct": "false" },
          { "text": "タイプ III", "correct": "false" },
          { "text": "タイプ I 未満", "correct": "true" },
        ]
      },
      {
        "question": "親星を取り囲み、星のエネルギー出力のほとんどまたはすべてを捕捉する巨大な構造は何ですか?",
        "answers": [
          { "text": "カイソン球", "correct": "false" },
          { "text": "ダイソン球", "correct": "true" },
          { "text": "パイソン球", "correct": "false" },
          { "text": "ライソン球", "correct": "false" },
        ]
      },
      {
        "question": "プロジェクトルッキンググラスLooking-Glassの主な目的は何ですか?",
        "answers": [
          { "text": "未来を予測する", "correct": "true" },
          { "text": "タイムトラベル", "correct": "false" },
          { "text": "通信や監視", "correct": "false" },
          { "text": "気象制御", "correct": "false" },
        ]
      },
      {
        "question": "ウイングメーカーはどこからやってきた何人でしょうか?",
        "answers": [
          { "text": "宇宙から来たエイリアン", "correct": "false" },
          { "text": "違う次元から来た霊体", "correct": "false" },
          { "text": "未来から来た地球人", "correct": "true" },
          { "text": "地底世界から来た地底人", "correct": "false" },
        ]
      },
      {
        "question": "一部で噂されている、2003年イラク戦争の秘密の目的とは?",
        "answers": [
          { "text": "エデンの園への秘密通路を探すため", "correct": "false" },
          { "text": "バグダッド地下に隠された電磁パルス兵器を押収するため", "correct": "false" },
          { "text": "イラクに隠れているビッグフットを捕獲するため", "correct": "false" },
          { "text": "スターゲートを制御するため", "correct": "true" },
        ]
      },
      {
        "question": "次のうち、時空のブラックホールへの扉を開こうとしているスイスの機関は?",
        "answers": [
          { "text": "CERN", "correct": "true" },
          { "text": "WHO", "correct": "false" },
          { "text": "UN", "correct": "false" },
          { "text": "WEF", "correct": "false" },
        ]
      },
      {
        "question": "告発者によると、オバマ元大統領は若い頃、どの施設から火星基地に送られましたか?",
        "answers": [
          { "text": "読書ルーム", "correct": "false" },
          { "text": "催眠ルーム", "correct": "false" },
          { "text": "ジャンプルーム", "correct": "true" },
          { "text": "公衆電話ブース", "correct": "false" },
        ]
      },
      {
        "question": "陰陽の卦を用いて世の中の万物の運行状況や時空の動きを導き出す中国の古典理論は？",
        "answers": [
          { "text": "『黄帝内経』", "correct": "false" },
          { "text": "『脈経』", "correct": "false" },
          { "text": "『易経』", "correct": "true" },
          { "text": "『詩経』", "correct": "false" },
        ]
      }
    ],
    "moon": [
      {
        "question": "スタンリー・キューブリック監督が、偽の月面着陸特殊効果の制作を依頼されたと示唆した映画は?",
        "answers": [
          { "text": "『2001年宇宙の旅』", "correct": "false" },
          { "text": "『シャイニング』", "correct": "true" },
          { "text": "『アイズ ワイド シャット』", "correct": "false" },
          { "text": "『スパルタカス』", "correct": "false" },
        ]
      },
      {
        "question": "1975年2月に遠隔透視で月の裏側にいくつかの建物や背の高い人型生物を見た有名な超能力者は?",
        "answers": [
          { "text": "エドガー・ケイシー Edgar Cayce", "correct": "false" },
          { "text": "ユリ・ゲラー Uri Geller", "correct": "false" },
          { "text": "ディック・アガー Dick Allgire", "correct": "false" },
          { "text": "インゴ・スワン Ingo Swann", "correct": "true" },
        ]
      },
      {
        "question": "デービッド・アイクによれば、爬虫類人の月装置は地球上の人類にどのような影響を施していますか?",
        "answers": [
          { "text": "人間の意識を3次元内に閉じ込める", "correct": "true" },
          { "text": "人間の認知能力を2次元から3次元に引き上げる", "correct": "false" },
          { "text": "人間の生理周期を設定する", "correct": "false" },
          { "text": "太陽放射の強さを緩衝する", "correct": "false" },
        ]
      },
      {
        "question": "ウィリアム・トンプキンスによれば、アポロ11号は月で何を見て来たのでしょう?",
        "answers": [
          { "text": "エイリアンの飛行物", "correct": "true" },
          { "text": "森", "correct": "false" },
          { "text": "嫦娥", "correct": "false" },
          { "text": "恐竜", "correct": "false" },
        ]
      },
      {
        "question": "月から来たという月のリペア職人の物語を記録した古代中国の書籍とは?",
        "answers": [
          { "text": "『山海経』", "correct": "false" },
          { "text": "『聊齋志異』", "correct": "false" },
          { "text": "『酉陽雑俎』", "correct": "true" },
          { "text": "『博物誌』", "correct": "false" },
        ]
      },
      {
        "question": "2018年のナショナル・ジオグラフィックの記事によると、科学者たちが見つけた地球の衛星の数は?",
        "answers": [
          { "text": "二つ", "correct": "false" },
          { "text": "三つ", "correct": "true" },
          { "text": "五つ", "correct": "false" },
          { "text": "十個", "correct": "false" },
        ]
      },
      {
        "question": "モントーク計画の暴露者スチュワート・スワードロウによると、月を今の軌道に持ってきたのは?",
        "answers": [
          { "text": "火星人", "correct": "false" },
          { "text": "天龍星人/ドラコ二アン", "correct": "true" },
          { "text": "リラ人", "correct": "false" },
          { "text": "アルクトゥルス人", "correct": "false" },
        ]
      },
      {
        "question": "ローマ神話の月の女神にちなんだ名前の方は?",
        "answers": [
          { "text": "ダイアナ王妃", "correct": "true" },
          { "text": "オードリー・ヘップバーン", "correct": "false" },
          { "text": "ニューヨークの自由の女神", "correct": "false" },
          { "text": "アンジェリーナ・ジョリー", "correct": "false" },
        ]
      },
      {
        "question": "アポロ12号のジョン・ヤングが聖書に手を置き月に行ったことの宣誓を求められた際に取った反応は?",
        "answers": [
          { "text": "彼はとても静かに聖書に手を置き、誓いを立てた", "correct": "false" },
          { "text": "自分は無神論者だから誓わないよと笑いながら答えた", "correct": "false" },
          { "text": "自分は実際には月に行ったことがないと認める", "correct": "false" },
          { "text": "非常に動揺し、質問者の質問を振り払おうとした", "correct": "true" },
        ]
      },
      {
        "question": "月の軌跡が描く形とは？",
        "answers": [
          { "text": "楕円形、「0」形", "correct": "false" },
          { "text": "完全な円", "correct": "false" },
          { "text": "「8」の字形", "correct": "true" },
          { "text": "一本の線", "correct": "false" },
        ]
      }
    ]
    },
  "en": { 
    "humanity": [
      {
        "question": "Which country removed the theory of evolution from high school textbooks in 2023?",
        "answers": [
          { "text": "Vietnam", "correct": "false" },
          { "text": "Slovakia", "correct": "false" },
          { "text": "India", "correct": "true" },
          { "text": "South Africa", "correct": "false" },
        ]
      },
      {
        "question": "What was the theory published by the discoverers of the DNA double helix structure in 1973?",
        "answers": [
          { "text": "Biogenesis", "correct": "false" },
          { "text": "Evolution", "correct": "false" },
          { "text": "RNA world hypothesis", "correct": "false" },
          { "text": "Panspermia", "correct": "true" },
        ]
      },
      {
        "question": "Humans have 46 chromosomes. How many chromosomes do gorillas have?",
        "answers": [
          { "text": "48", "correct": "true" },
          { "text": "46", "correct": "false" },
          { "text": "44", "correct": "false" },
          { "text": "52", "correct": "false" },
        ]
      },
      {
        "question": "According to ancient Sumerian texts, who were the ones that genetically modified humans?",
        "answers": [
          { "text": "Eskimos", "correct": "false" },
          { "text": "Annunnakis", "correct": "true" },
          { "text": "Reptalians", "correct": "false" },
          { "text": "Sirians", "correct": "false" },
        ]
      },
      {
        "question": "What is the theory that the current human civilization was created by aliens?",
        "answers": [
          { "text": "Ancient Aliens Theory", "correct": "false" },
          { "text": "Ancien Astronauts Theory ", "correct": "true" },
          { "text": "Ancient Scientists Theory", "correct": "false" },
          { "text": "Ancient Pioneers Theory", "correct": "false" },
        ]
      },
      {
        "question": "Who was the philosopher who mentioned the civilization of Atlantis in his work?",
        "answers": [
          { "text": "Socrates", "correct": "false" },
          { "text": "Nietzsche", "correct": "false" },
          { "text": "Schopenhauer", "correct": "false" },
          { "text": "Plato", "correct": "true" },
        ]
      },
      {
        "question": "Which of the following ancient documents DOES NOT have the story of Nuwa?",
        "answers": [
          { "text": "'The Classic of Mountains and Seas'", "correct": "false" },
          { "text": "'The Book of Han'", "correct": "false" },
          { "text": "'Comprehensive Meaning of Customs and Mores'", "correct": "false" },
          { "text": "'The Art of War'", "correct": "true" },
        ]
      },
      {
        "question": "What is the name of the ancestor of mankind in Indian mythology?",
        "answers": [
          { "text": "Manu", "correct": "true" },
          { "text": "Brahma", "correct": "false" },
          { "text": "Shiva", "correct": "false" },
          { "text": "Vishnu", "correct": "false" },
        ]
      },
      {
        "question": "What were the ancient humans that suddenly vanished about 30,000 to 40,000 years ago?",
        "answers": [
          { "text": "Homo Erectus", "correct": "false" },
          { "text": "Heidelbergensis", "correct": "false" },
          { "text": "Neanderthal", "correct": "true" },
          { "text": "Peking Man", "correct": "false" },
        ]
      },
      {
        "question": "How much of our DNA is made up of something the mainstream sciece calls as 'junk DNA' ?",
        "answers": [
          { "text": "78~80%", "correct": "false" },
          { "text": "95~98%", "correct": "true" },
          { "text": "12~15%", "correct": "false" },
          { "text": "3~5%", "correct": "false" },
        ]
      }
    ],
    "underground": [
      {
        "question": "What is the name of the underworld world described in ancient texts?",
        "answers": [
          { "text": "Tartaria", "correct": "false" },
          { "text": "Agartha", "correct": "true" },
          { "text": "Lemuria", "correct": "false" },
          { "text": "Atlantis", "correct": "false" },
        ]
      },
      {
        "question": "Where did Hitler and the Nazis send expeditions to in 1938 and 1943 in search of underground cities?",
        "answers": [
          { "text": "Siberia", "correct": "false" },
          { "text": "Xi-An", "correct": "false" },
          { "text": "East Timor", "correct": "false" },
          { "text": "Tibet", "correct": "true" },
        ]
      },
      {
        "question": "Where is Hitler's underground Nazi base located according to whistleblowers?",
        "answers": [
          { "text": "Antarctica", "correct": "true" },
          { "text": "North Pole", "correct": "false" },
          { "text": "Sahara Desert", "correct": "false" },
          { "text": "Peru", "correct": "false" },
        ]
      },
      {
        "question": "What is the acronym for the underground military tunnel system?",
        "answers": [
          { "text": "D.B.U.M", "correct": "false" },
          { "text": "N.U.M.B", "correct": "false" },
          { "text": "D.U.M.B", "correct": "true" },
          { "text": "M.U.D.B", "correct": "false" },
        ]
      },
      {
        "question": "What is the main objective of military operations conducted underground?",
        "answers": [
          { "text": "Rescue of benevolent aliens captured by reptilians", "correct": "false" },
          { "text": "Rescue of smuggled rare animals", "correct": "false" },
          { "text": "Rescue of trafficked human children", "correct": "true" },
          { "text": "To recover gold bullion stolen in underground transactions", "correct": "false" },
        ]
      },
      {
        "question": "What is the typical focal depth of earthquakes associated with underground military operations?",
        "answers": [
          { "text": "～10km", "correct": "true" },
          { "text": "10～15km", "correct": "false" },
          { "text": "15～20km", "correct": "false" },
          { "text": "20km～", "correct": "false" },
        ]
      },
      {
        "question": "What color is the pyramid found underground near Mount McKinley in Alaska?",
        "answers": [
          { "text": "earthy color", "correct": "false" },
          { "text": "golden", "correct": "false" },
          { "text": "white", "correct": "false" },
          { "text": "black", "correct": "true" },
        ]
      },
      {
        "question": "Which European country discovered a mysterious underground cave in a mountain in 2003?",
        "answers": [
          { "text": "Serbia", "correct": "false" },
          { "text": "Romania", "correct": "true" },
          { "text": "Croatia", "correct": "false" },
          { "text": "Bulgaria", "correct": "false" },
        ]
      },
      {
        "question": "Which of the following figures is not an explorer of the underworld?",
        "answers": [
          { "text": "Hsuan Tsang of the Tang Dynasty", "correct": "true" },
          { "text": "Ancient Greek geographer Pytheas", "correct": "false" },
          { "text": "Norwegian fisherman Olaf Jansen and his son", "correct": "false" },
          { "text": "U.S. Navy Admiral Byrd", "correct": "false" },
        ]
      },
      {
        "question": "Which of the following cities is a legendary underground city?",
        "answers": [
          { "text": "Sindhu", "correct": "false" },
          { "text": "Babylon", "correct": "false" },
          { "text": "Kitezh", "correct": "false" },
          { "text": "Shambhala", "correct": "true" },
        ]
      }
    ],
    "ufo": [
      {
        "question": "Who is the famous whistleblower involved in UFO reverse engineering research?",
        "answers": [
          { "text": "Bob Lazar", "correct": "true" },
          { "text": "Allex Collier", "correct": "false" },
          { "text": "Michael Salla", "correct": "false" },
          { "text": "Phil Schneider", "correct": "false" },
        ]
      },
      {
        "question": "What is the name of the famous UFO base located in Nevada, USA?",
        "answers": [
          { "text": "Roswell", "correct": "false" },
          { "text": "Montauk Air Force Station", "correct": "false" },
          { "text": "Area 51", "correct": "true" },
          { "text": "Dulce Base", "correct": "false" },
        ]
      },
      {
        "question": "What is the previous occupation of David Grusch who testified at the U.S. Congressional UFO hearing in July 2023?",
        "answers": [
          { "text": "Space Force officer", "correct": "false" },
          { "text": "Navy Officer", "correct": "false" },
          { "text": "Army Officer", "correct": "false" },
          { "text": "Air Force Officer", "correct": "true" },
        ]
      },
      {
        "question": "In addition to the flying saucer shape, what other UFO shapes are often sighted on Earth?",
        "answers": [
          { "text": "toothpaste tube shape", "correct": "false" },
          { "text": "automobile shape", "correct": "false" },
          { "text": "cigar shape", "correct": "true" },
          { "text": "pentagonal star shape", "correct": "false" },
        ]
      },
      {
        "question": "What was the shape of the time-travel device secretly developed by the Nazis during World War II?",
        "answers": [
          { "text": "Bell", "correct": "true" },
          { "text": "Car", "correct": "false" },
          { "text": "Bottle", "correct": "false" },
          { "text": "Chair", "correct": "false" },
        ]
      },
      {
        "question": "In which year did the famous UFO sighting over Washington D.C. occur?",
        "answers": [
          { "text": "1942", "correct": "false" },
          { "text": "1952", "correct": "true" },
          { "text": "1947", "correct": "false" },
          { "text": "1972", "correct": "false" },
        ]
      },
      {
        "question": "In which country was the 1933 UFO crash that preceded Roswell occur?",
        "answers": [
          { "text": "Mexico", "correct": "false" },
          { "text": "Italy", "correct": "true" },
          { "text": "Spain", "correct": "false" },
          { "text": "Vatican", "correct": "false" },
        ]
      },
      {
        "question": "What is the name of the anti-gravity aircraft that is claimed to be reverse-engineered using black technology?",
        "answers": [
          { "text": "F-22", "correct": "false" },
          { "text": "Ki-100", "correct": "false" },
          { "text": "MiG-29", "correct": "false" },
          { "text": "TR-3B", "correct": "true" },
        ]
      },
      {
        "question": "All of the following paintings depicts UFO sighting except for:",
        "answers": [
          { "text": "'The Baptism of Christ' by Art de Gelder", "correct": "false" },
          { "text": "Portrait of the Virgin in Palazzo Vecchio", "correct": "false" },
          { "text": "Van Gogh's 'Starry Night'", "correct": "true" },
          { "text": "Serbian orthodox church painting", "correct": "false" },
        ]
      },
      {
        "question": "Which country artificially synthesized the anti-gravity fuel 'Element 115' in 2003?",
        "answers": [
          { "text": "Russia", "correct": "true" },
          { "text": "United States", "correct": "false" },
          { "text": "India", "correct": "false" },
          { "text": "China", "correct": "false" },
        ]
      }
    ],
    "jab": [
      {
        "question": "Which state in USA announced the suspension of the use of mRNA vaccines in January 2024?",
        "answers": [
          { "text": "California", "correct": "false" },
          { "text": "Florida", "correct": "true" },
          { "text": "Texas", "correct": "false" },
          { "text": "New York", "correct": "false" },
        ]
      },
      {
        "question": "Which set of international norms is violated by the mandatory vaccination on humans?",
        "answers": [
          { "text": "Bretton Woods system", "correct": "false" },
          { "text": "Kyoto Protocol", "correct": "false" },
          { "text": "Nuremberg Code", "correct": "true" },
          { "text": "Biological Weapons Convention", "correct": "false" },
        ]
      },
      {
        "question": "What changes in the body might the 'graphene' contained in the COVID-19 vaccine induce?",
        "answers": [
          { "text": "Become a magnetic body", "correct": "true" },
          { "text": "Insomnia", "correct": "false" },
          { "text": "Increased body temperature", "correct": "false" },
          { "text": "Increased appetite", "correct": "false" },
        ]
      },
      {
        "question": "Which mobile phone feature might detect people who have been vaxed against COVID-19?",
        "answers": [
          { "text": "QR code scanning feature", "correct": "false" },
          { "text": "Wi-Fi", "correct": "false" },
          { "text": "4G", "correct": "false" },
          { "text": "Bluetooth", "correct": "true" },
        ]
      },
      {
        "question": "What is the disease that is almost non-existent among the Amish, whose are hardly vaccinated?",
        "answers": [
          { "text": "Cold", "correct": "false" },
          { "text": "Obesity", "correct": "false" },
          { "text": "Autism", "correct": "true" },
          { "text": "Diabetes", "correct": "false" },
        ]
      },
      {
        "question": "Which Big Tech boss is the entrepreneur most passionate about vaccinating the global population?",
        "answers": [
          { "text": "Pony Ma", "correct": "false" },
          { "text": "Jack Ma", "correct": "false" },
          { "text": "Elon Musk", "correct": "false" },
          { "text": "Bill Gates", "correct": "true" },
        ]
      },
      {
        "question": "Which of the following substances is not added to vaccine adjuvants?",
        "answers": [
          { "text": "Aluminum", "correct": "false" },
          { "text": "Gold", "correct": "true" },
          { "text": "Mercury", "correct": "false" },
          { "text": "Graphene", "correct": "false" },
        ]
      },
      {
        "question": "Which of the following enzymes is most helpful in removing spike protein and dissolving blood clots?",
        "answers": [
          { "text": "Nattokinase", "correct": "true" },
          { "text": "Glucanase", "correct": "false" },
          { "text": "Asparaginase", "correct": "false" },
          { "text": "Amylase", "correct": "false" },
        ]
      },
      {
        "question": "What is the drug discovered by Japanese scientist Satoshi Omura that is effective against COVID-19?",
        "answers": [
          { "text": "Quercetin", "correct": "false" },
          { "text": "Ivermectin", "correct": "true" },
          { "text": "Hydroxychloroquine", "correct": "false" },
          { "text": "Bromelain", "correct": "false" },
        ]
      },
      {
        "question": "Which of the following statements does not fit the purpose of vaccination percieved by the conspiracy theorists?",
        "answers": [
          { "text": "Population reduction", "correct": "false" },
          { "text": "Transhuman mutant experiment", "correct": "false" },
          { "text": "Building a 'human internet' with nanochip implants", "correct": "false" },
          { "text": "Improving public health", "correct": "true" },
        ]
      }
    ],
    "ai": [
      {
        "question": "In movie '2001: A Space Odyssey', what is the name of the AI that accompanied the three pilots?",
        "answers": [
          { "text": "PAL 9000", "correct": "false" },
          { "text": "HAL 9000", "correct": "true" },
          { "text": "TAL 9000", "correct": "false" },
          { "text": "KAL 9000", "correct": "false" },
        ]
      },
      {
        "question": "What is the name of the first AI robot which obtained itself a citizenship of Saudi Arabia?",
        "answers": [
          { "text": "Maria", "correct": "false" },
          { "text": "Patricia", "correct": "false" },
          { "text": "Sylvia", "correct": "false" },
          { "text": "Sophia", "correct": "true" },
        ]
      },
      {
        "question": "What is the 'food' for AI?",
        "answers": [
          { "text": "Humans", "correct": "false" },
          { "text": "Programming codes", "correct": "false" },
          { "text": "Data", "correct": "true" },
          { "text": "Electricity", "correct": "false" },
        ]
      },
      {
        "question": "Which company does Alexa AI belong to?",
        "answers": [
          { "text": "Amazon", "correct": "true" },
          { "text": "Google", "correct": "false" },
          { "text": "Apple", "correct": "false" },
          { "text": "Facebook", "correct": "false" },
        ]
      },
      {
        "question": "What is the ideological bias of ChatGPT?",
        "answers": [
          { "text": "Left wing", "correct": "true" },
          { "text": "Right wing", "correct": "false" },
          { "text": "Independent", "correct": "false" },
          { "text": "New religions", "correct": "false" },
        ]
      },
      {
        "question": "In which year was the first AI chatbot Eliza born?",
        "answers": [
          { "text": "1978", "correct": "false" },
          { "text": "2001", "correct": "false" },
          { "text": "1947", "correct": "false" },
          { "text": "1966", "correct": "true" },
        ]
      },
      {
        "question": "Which AI function's defect does the documentary 'Coded Bias' refer to?",
        "answers": [
          { "text": "IQ testing", "correct": "false" },
          { "text": "Face recognition", "correct": "true" },
          { "text": "Obesity check", "correct": "false" },
          { "text": "Voice recognition", "correct": "false" },
        ]
      },
      {
        "question": "What is the name of the AI software of Blackstone Group that predicts financial markets?",
        "answers": [
          { "text": "Atom", "correct": "false" },
          { "text": "Avatar", "correct": "false" },
          { "text": "Alibaba", "correct": "false" },
          { "text": "Aladdin", "correct": "true" },
        ]
      },
      {
        "question": "Which of the following tests can examine whether a machine has AI?",
        "answers": [
          { "text": "Tensorflow", "correct": "false" },
          { "text": "Mensa", "correct": "false" },
          { "text": "Turing Test", "correct": "true" },
          { "text": "Bell Test", "correct": "false" },
        ]
      },
      {
        "question": "In which country is the first hotel operated almost entirely by robots located?",
        "answers": [
          { "text": "Japan", "correct": "true" },
          { "text": "United States", "correct": "false" },
          { "text": "Israel", "correct": "false" },
          { "text": "India", "correct": "false" },
        ]
      }
    ],
    "et": [
      {
        "question": "What is the color of Reptalian blood?",
        "answers": [
          { "text": "Green", "correct": "false" },
          { "text": "Blue", "correct": "true" },
          { "text": "Yellow", "correct": "false" },
          { "text": "Red", "correct": "false" },
        ]
      },
      {
        "question": "What planet does Valiant Thor from the book 'Strangers in the Pentagon' come from?",
        "answers": [
          { "text": "Pluto", "correct": "false" },
          { "text": "Mars", "correct": "false" },
          { "text": "Moon", "correct": "false" },
          { "text": "Venus", "correct": "true" },
        ]
      },
      {
        "question": "What planet does Boriska, a Russian indigo child born in 1996, claim to be from?",
        "answers": [
          { "text": "Mars", "correct": "true" },
          { "text": "Venus", "correct": "false" },
          { "text": "Sirius", "correct": "false" },
          { "text": "Saturn", "correct": "false" },
        ]
      },
      {
        "question": "What is the name of the extraterrestrial being that appears in 'The Law of One'?",
        "answers": [
          { "text": "Ma", "correct": "false" },
          { "text": "Ta", "correct": "false" },
          { "text": "Ra", "correct": "true" },
          { "text": "La", "correct": "false" },
        ]
      },
      {
        "question": "What fascinating image did the Viking 1 probe take on Mars on July 25, 1976?",
        "answers": [
          { "text": "UFO base", "correct": "false" },
          { "text": "A bump in the ground that closely resembles a human face", "correct": "true" },
          { "text": "A black pyramid", "correct": "false" },
          { "text": "A huge transparent structure", "correct": "false" },
        ]
      },
      {
        "question": "Among the 3 waves of starseeds Dolores Cannon wrote about in 2011, when did the 1st wave arrive on Earth?",
        "answers": [
          { "text": "Late 1940s", "correct": "true" },
          { "text": "1970s", "correct": "false" },
          { "text": "Early 2000s", "correct": "false" },
          { "text": "Mid 1960s", "correct": "false" },
        ]
      },
      {
        "question": "What kind of aliens were involved in the Human-ET agreement signed by the Eisenhower administration?",
        "answers": [
          { "text": "Pleiadians", "correct": "false" },
          { "text": "Greys", "correct": "true" },
          { "text": "Nordic aliens", "correct": "false" },
          { "text": "Draconians", "correct": "false" },
        ]
      },
      {
        "question": "What was the name of the person who revealed a live video of an alien interview that was circulated in the 1990s?",
        "answers": [
          { "text": "Mark", "correct": "false" },
          { "text": "Joseph", "correct": "false" },
          { "text": "Victor", "correct": "true" },
          { "text": "David", "correct": "false" },
        ]
      },
      {
        "question": "Which planet did the Anunnaki mentioned by ancient Sumerian texts come from?",
        "answers": [
          { "text": "Nibiru", "correct": "true" },
          { "text": "Alpha Centaur", "correct": "false" },
          { "text": "Halley's comet", "correct": "false" },
          { "text": "The Sun", "correct": "false" },
        ]
      },
      {
        "question": "What color was the skin of higher beings such as Vishnu described in the Vedic literature?",
        "answers": [
          { "text": "Gold", "correct": "false" },
          { "text": "Red", "correct": "false" },
          { "text": "Green", "correct": "false" },
          { "text": "Blue", "correct": "true" },
        ]
      }
    ],
    "spiritual": [
      {
        "question": "What method did Ms. Dolores Cannon, Dr. Brian Weiss, etc. use to help people retrieve their memories of past lives?",
        "answers": [
          { "text": "Deep Brain Stimulation Therapy", "correct": "false" },
          { "text": "Acupuncture", "correct": "false" },
          { "text": "Light Therapy", "correct": "false" },
          { "text": "Hypnotic Regression Therapy", "correct": "true" },
        ]
      },
      {
        "question": "Which religious teaching denies reincarnation?",
        "answers": [
          { "text": "Judaism", "correct": "false" },
          { "text": "Buddism", "correct": "false" },
          { "text": "Christianity", "correct": "true" },
          { "text": "Hinduism", "correct": "false" },
        ]
      },
      {
        "question": "In the book 'Initiation', what is the identity of the main character when she was living in ancient Egypt?",
        "answers": [
          { "text": "Pharaoh", "correct": "false" },
          { "text": "Priestess", "correct": "true" },
          { "text": "Queen Cleopatra", "correct": "false" },
          { "text": "Medical Doctor", "correct": "false" },
        ]
      },
      {
        "question": "Among the three Buddhas in Buddhism, which Buddha represents the future?",
        "answers": [
          { "text": "Shakyamuni Buddha", "correct": "false" },
          { "text": "Dipankara Buddha", "correct": "false" },
          { "text": "Medicine Buddha", "correct": "false" },
          { "text": "Maitreya Buddha", "correct": "true" },
        ]
      },
      {
        "question": "What feature would the Past Life Therapy look for in the patient to treat diseases?",
        "answers": [
          { "text": "Karma", "correct": "true" },
          { "text": "Physical condition", "correct": "false" },
          { "text": "Family lineage and bloodline", "correct": "false" },
          { "text": "Hobbies", "correct": "false" },
        ]
      },
      {
        "question": "How many grams does a soul weigh according to a 1907 scientific experiment?",
        "answers": [
          { "text": "14g", "correct": "false" },
          { "text": "28g", "correct": "false" },
          { "text": "21g", "correct": "true" },
          { "text": "7g", "correct": "false" },
        ]
      },
      {
        "question": "According to the content disclosed in 'The Law of One', in which density does human beings belong to now?",
        "answers": [
          { "text": "5th dimension", "correct": "false" },
          { "text": "3rd dimension", "correct": "true" },
          { "text": "8th dimension", "correct": "false" },
          { "text": "4th dimension", "correct": "false" },
        ]
      },
      {
        "question": "What is the frequency of Mother Earth?",
        "answers": [
          { "text": "7.83Hz", "correct": "true" },
          { "text": "210.42Hz", "correct": "false" },
          { "text": "183.58Hz", "correct": "false" },
          { "text": "221.23Hz", "correct": "false" },
        ]
      },
      {
        "question": "What is the spiritual meaning of the ajna chakra among the chakras?",
        "answers": [
          { "text": "Spirituality, psychic ability", "correct": "false" },
          { "text": "Energy of life", "correct": "false" },
          { "text": "Insight, intuition", "correct": "true" },
          { "text": "Love, emotions", "correct": "false" },
        ]
      },
      {
        "question": "Which Yuga era are we currently in?",
        "answers": [
          { "text": "Krita Yuga", "correct": "false" },
          { "text": "Dvapara Yuga", "correct": "false" },
          { "text": "Treta Yuga", "correct": "false" },
          { "text": "Kali Yuga", "correct": "true" },
        ]
      },
    ],
    "healing": [
      {
        "question": "Which ancient Chinese musical instrument is used in sound therapy Gong Healing?",
        "answers": [
          { "text": "Xiao Flute", "correct": "false" },
          { "text": "Guqin", "correct": "false" },
          { "text": "Flute", "correct": "false" },
          { "text": "Gong", "correct": "true" },
        ]
      },
      {
        "question": "There is a cake ingredient that also has medical properties and alkalizes the body. What is it?",
        "answers": [
          { "text": "Baking powder", "correct": "false" },
          { "text": "Baking soda", "correct": "true" },
          { "text": "Sugar", "correct": "false" },
          { "text": "Fresh cream", "correct": "false" },
        ]
      },
      {
        "question": "Which traditional Chinese medicine method can replace anesthesia?",
        "answers": [
          { "text": "Gua Sha (skin scraping)", "correct": "false" },
          { "text": "Cupping Therapy", "correct": "false" },
          { "text": "Acupuncture", "correct": "true" },
          { "text": "Moxibustion", "correct": "false" },
        ]
      },
      {
        "question": "What technology is the cancer treating device invented by Dr. Royal Rife based on?",
        "answers": [
          { "text": "Frequency", "correct": "true" },
          { "text": "Essential oil", "correct": "false" },
          { "text": "Infrared", "correct": "false" },
          { "text": "A special type of hard water", "correct": "false" },
        ]
      },
      {
        "question": "What is the original use of Fenbendazole - a controversial drug argued by some as a cancer treatment?",
        "answers": [
          { "text": "Sleeping pills", "correct": "false" },
          { "text": "Veterinary medicine", "correct": "true" },
          { "text": "Suppository", "correct": "false" },
          { "text": "Eye drops", "correct": "false" },
        ]
      },
      {
        "question": "Which essential oil helps to enhance memory?",
        "answers": [
          { "text": "Mint", "correct": "false" },
          { "text": "Rose", "correct": "false" },
          { "text": "Frankincense", "correct": "false" },
          { "text": "Rosemary", "correct": "true" },
        ]
      },
      {
        "question": "What is the common name for a toxin that exists in bitter almonds and apricot kernels, arguably having anti-cancer effects?",
        "answers": [
          { "text": "Benzaldehyde", "correct": "false" },
          { "text": "Protein kinase", "correct": "false" },
          { "text": "Curcumin", "correct": "false" },
          { "text": "Vitamin B17", "correct": "true" },
        ]
      },
      {
        "question": "What substance is DMSO extracted from?",
        "answers": [
          { "text": "Trees", "correct": "true" },
          { "text": "Seeweed", "correct": "false" },
          { "text": "Cotton", "correct": "false" },
          { "text": "Petroleum", "correct": "false" },
        ]
      },
      {
        "question": "Who is the psychic who introduced Castor Oil Therapy?",
        "answers": [
          { "text": "Edgar Cayce", "correct": "true" },
          { "text": "Wolf Messing", "correct": "false" },
          { "text": "David Copperfield", "correct": "false" },
          { "text": "Lin Wang", "correct": "false" },
        ]
      },
      {
        "question": "Which of the following oils are commonly used in oil pulling to aid oral health?",
        "answers": [
          { "text": "Olive Oil", "correct": "false" },
          { "text": "Sunflower oil", "correct": "false" },
          { "text": "Coconut oil", "correct": "true" },
          { "text": "Peanut oil", "correct": "false" },
        ]
      }
    ],
    "shanhaijing": [
      {
        "question": "What is the catastrophe described in 'The Classic of Mountains and Seas' that is similar to the story in the Bible?",
        "answers": [
          { "text": "Great flood", "correct": "true" },
          { "text": "Big fire", "correct": "false" },
          { "text": "Big earthquake", "correct": "false" },
          { "text": "Meteorite crash", "correct": "false" },
        ]
      },
      {
        "question": "Which part of the human body has a shape similar to the shape depicted in the Fuxi and Nuwa paintings unearthed in Xinjiang?",
        "answers": [
          { "text": "Stem cell structure", "correct": "false" },
          { "text": "Structure of the left and right brain", "correct": "false" },
          { "text": "DNA structure", "correct": "true" },
          { "text": "Ventricular structure", "correct": "false" },
        ]
      },
      {
        "question": "Which god in 'The Classic of Mountains and Sea' might the Zongmu mask unearthed from Sanxingdui be associated with?",
        "answers": [
          { "text": "Qin Pei (Water Hawk)", "correct": "false" },
          { "text": "Zhulong / Zhuyin (Torch Dragon)", "correct": "true" },
          { "text": "Lu Wu (shoulder my)", "correct": "false" },
          { "text": "Pangu", "correct": "false" },
        ]
      },
      {
        "question": "Which feature of the monster Taotie in 'The Classic of Mountains and Seas' is similar to the characteristics of Satan in the West?",
        "answers": [
          { "text": "Pig ears", "correct": "false" },
          { "text": "Unicorn", "correct": "false" },
          { "text": "Goat's torso", "correct": "true" },
          { "text": "Dragon head", "correct": "false" },
        ]
      },
      {
        "question": "What is the name of the tree where the sun lives on described by 'The Classic of Mountains and Seas'?",
        "answers": [
          { "text": "Jianmu", "correct": "false" },
          { "text": "Fusang", "correct": "true" },
          { "text": "Ruomu", "correct": "false" },
          { "text": "Locust tree", "correct": "false" },
        ]
      },
      {
        "question": "Which ancient mythical story is not described in 'The Classic of Mountains and Seas'?",
        "answers": [
          { "text": "'Houyi Shot the Suns'", "correct": "true" },
          { "text": "'Nuwa Creating Human Beings'", "correct": "false" },
          { "text": "'Kuafu Chasing the Sun'", "correct": "false" },
          { "text": "'The Goddess Chang's fly to the moon'", "correct": "false" },
        ]
      },
      {
        "question": "In which mountain do the gods live according to 'The Classic of Mountains and Seas'?",
        "answers": [
          { "text": "Mount Huangshan", "correct": "false" },
          { "text": "Flower and Fruit Mountain", "correct": "false" },
          { "text": "Mt Song", "correct": "false" },
          { "text": "Kunlun Mountains", "correct": "true" },
        ]
      },
      {
        "question": "Which Western god is similar to the image of Xi He (mother of the sun, driving a dragon chariot carrying the golden crows of suns)?",
        "answers": [
          { "text": "Hera, the ancient Greek goddess", "correct": "false" },
          { "text": "Helios, the ancient Greek god", "correct": "true" },
          { "text": "Isis, the ancient Egyptian god", "correct": "false" },
          { "text": "Amaterasu, the ancient Japanese goddess", "correct": "false" },
        ]
      },
      {
        "question": "What musical instrument did Huangdi use the body of Kui Niu to make into, according to 'The Classic of Mountains and Seas'?",
        "answers": [
          { "text": "Biwa", "correct": "false" },
          { "text": "Drum sticks", "correct": "false" },
          { "text": "Horn", "correct": "false" },
          { "text": "War drum", "correct": "true" },
        ]
      },
      {
        "question": "Which part of Nuwa's body transformed into the ten gods?",
        "answers": [
          { "text": "Intestine", "correct": "true" },
          { "text": "Hair", "correct": "false" },
          { "text": "Fingers", "correct": "false" },
          { "text": "Eyes", "correct": "false" },
        ]
      }
    ],
    "pyramid": [
      {
        "question": "What did researchers discover near the Giza Pyramids in ancient Egypt in March 2023?",
        "answers": [
          { "text": "An Underground Pyramid", "correct": "false" },
          { "text": "A Secret Passage", "correct": "true" },
          { "text": "A Mummy", "correct": "false" },
          { "text": "An Ancient Scripture", "correct": "false" },
        ]
      },
      {
        "question": "To which part of what constellation do the location and layout of the three pyramids in Egypt correspond?",
        "answers": [
          { "text": "Belt of Orion", "correct": "true" },
          { "text": "Scorpio's body", "correct": "false" },
          { "text": "Leo's mane", "correct": "false" },
          { "text": "Horn of Taurus", "correct": "false" },
        ]
      },
      {
        "question": "Which is the nearby city of the 'Pyramid of China'?",
        "answers": [
          { "text": "Kai-Feng", "correct": "false" },
          { "text": "Cheng-Du", "correct": "false" },
          { "text": "Xi-An", "correct": "true" },
          { "text": "Shen-Yang", "correct": "false" },
        ]
      },
      {
        "question": "In which country is the world's largest pyramid found located?",
        "answers": [
          { "text": "Egypt", "correct": "false" },
          { "text": "Mexico", "correct": "true" },
          { "text": "China", "correct": "false" },
          { "text": "Antarctica", "correct": "false" },
        ]
      },
      {
        "question": "In which region are most of the Quetzalcoatl worshiping pyramids located?",
        "answers": [
          { "text": "Central and South America", "correct": "true" },
          { "text": "Southeast Asia", "correct": "false" },
          { "text": "Egypt", "correct": "false" },
          { "text": "Alaska", "correct": "false" },
        ]
      },
      {
        "question": "What important part of Khufu's Pyramid is missing?",
        "answers": [
          { "text": "Nothing is missing and everything is perfectly preserved", "correct": "false" },
          { "text": "The stone door to Pharaoh's tomb ", "correct": "false" },
          { "text": "Ancient drawings depicting interior design", "correct": "false" },
          { "text": "Pyramidion", "correct": "true" },
        ]
      },
      {
        "question": "Which of the following museums and art galleries has a glass pyramid?",
        "answers": [
          { "text": "Louvre Museum", "correct": "true" },
          { "text": "Smithsonian Museum", "correct": "false" },
          { "text": "British Museum", "correct": "false" },
          { "text": "Hermitage Museum", "correct": "false" },
        ]
      },
      {
        "question": "The following building materials are the main building materials of the Egyptian pyramids except for:",
        "answers": [
          { "text": "Marble", "correct": "true" },
          { "text": "Limestone", "correct": "false" },
          { "text": "Mortar", "correct": "false" },
          { "text": "Granite", "correct": "false" },
        ]
      },
      {
        "question": "Multiplying the height of Khufu's Pyramid by 1 billion times will yield the distance between earth and which planet?",
        "answers": [
          { "text": "Moon", "correct": "false" },
          { "text": "Sun", "correct": "true" },
          { "text": "Mars", "correct": "false" },
          { "text": "Venus", "correct": "false" },
        ]
      },
      {
        "question": "What is the number of the height of Great Pyramid multiplied by 43,200 equal to?",
        "answers": [
          { "text": "Distance between Earth and Moon", "correct": "false" },
          { "text": "Distance between Earth and Sun", "correct": "false" },
          { "text": "Earth's polar radius", "correct": "true" },
          { "text": "Diameter of the Earth", "correct": "false" },
        ]
      }
    ],
    "timespace": [
      {
        "question": "What had suddenly vanished during the Philadelphia Experiment which took place in 1943?",
        "answers": [
          { "text": "Warship", "correct": "true" },
          { "text": "Fighter Jet", "correct": "false" },
          { "text": "Tank", "correct": "false" },
          { "text": "Cannon", "correct": "false" },
        ]
      },
      {
        "question": "Which famous historical scene did the time-travel Pegasus project send a boy to?",
        "answers": [
          { "text": "Coronation of Napoleon", "correct": "false" },
          { "text": "President Lincoln's Gettysburg Address", "correct": "true" },
          { "text": "Discovery of America by Columbus", "correct": "false" },
          { "text": "Leonardo da Vinci painting the Mona Lisa", "correct": "false" },
        ]
      },
      {
        "question": "Which type of the Kardashev Index does the human civilization currently belong to?",
        "answers": [
          { "text": "Type I", "correct": "false" },
          { "text": "Type II", "correct": "false" },
          { "text": "Type III", "correct": "false" },
          { "text": "Less than Type I", "correct": "true" },
        ]
      },
      {
        "question": "What is the name for a massive structure surrounding a parent star that captures most or all of the star's energy output?",
        "answers": [
          { "text": "Kyson Sphere", "correct": "false" },
          { "text": "Dyson Sphere", "correct": "true" },
          { "text": "Byson Sphere", "correct": "false" },
          { "text": "Lyson Sphere", "correct": "false" },
        ]
      },
      {
        "question": "What is the main purpose of Project Looking-Glass?",
        "answers": [
          { "text": "Predict the Future", "correct": "true" },
          { "text": "Time Travel", "correct": "false" },
          { "text": "Communication and Surveillance", "correct": "false" },
          { "text": "Climate Control", "correct": "false" },
        ]
      },
      {
        "question": "Where did the Wingmakers come from and who are they?",
        "answers": [
          { "text": "Extraterrestrial beings", "correct": "false" },
          { "text": "Beings from another dimension", "correct": "false" },
          { "text": "Future Earthlings", "correct": "true" },
          { "text": "Underground world beings", "correct": "false" },
        ]
      },
      {
        "question": "What is the allged secret purpose of the 2003 Iraq War?",
        "answers": [
          { "text": "To find the secret passage to the Garden of Eden", "correct": "false" },
          { "text": "To seize EMP weapons hidden underground in Baghdad", "correct": "false" },
          { "text": "To capture Bigfoot hiding in Iraq", "correct": "false" },
          { "text": "To control the stargate", "correct": "true" },
        ]
      },
      {
        "question": "Which institution in Switzerland is said to be attempting to open the portal to different dimensions?",
        "answers": [
          { "text": "CERN", "correct": "true" },
          { "text": "WHO", "correct": "false" },
          { "text": "UN", "correct": "false" },
          { "text": "WEF", "correct": "false" },
        ]
      },
      {
        "question": "According to a whisleblower, through what facility was Obama sent to a Mars base as a young man?",
        "answers": [
          { "text": "Reading Room", "correct": "false" },
          { "text": "Hypnosis Room", "correct": "false" },
          { "text": "Jump Room", "correct": "true" },
          { "text": "Phone Booth", "correct": "false" },
        ]
      },
      {
        "question": "What is the name of the Chinese classical theory using hexagrams of yin and yang symbols to deduce the laws of time and space?",
        "answers": [
          { "text": "'Yellow Emperor's Classic of Medicine'", "correct": "false" },
          { "text": "'Mai Jing'", "correct": "false" },
          { "text": "'Yi Jing'", "correct": "true" },
          { "text": "'Shi Jing'", "correct": "false" },
        ]
      }
    ],
    "moon": [
      {
        "question": "In which of his films did director Stanley Kubrick suggest that he was commissioned to create the fake moon landing film?",
        "answers": [
          { "text": "'2001: A Space Odyssey'", "correct": "false" },
          { "text": "'Shining'", "correct": "true" },
          { "text": "'Eyes Wide Shut'", "correct": "false" },
          { "text": "'Spartacus'", "correct": "false" },
        ]
      },
      {
        "question": "Who was the famous remote viewer who saw some buildings and tall humanoid creatures on the far side of the moon in February 1975?",
        "answers": [
          { "text": "Edgar Cayce", "correct": "false" },
          { "text": "Uri Geller", "correct": "false" },
          { "text": "Dick Allgire", "correct": "false" },
          { "text": "Ingo Swann", "correct": "true" },
        ]
      },
      {
        "question": "According to David Icke, what effect does the Reptilian device on the moon have on humans on Earth?",
        "answers": [
          { "text": "Confining human consciousness within the 3D", "correct": "true" },
          { "text": "Elevating human cognitive ability from 2D to 3D", "correct": "false" },
          { "text": "Setting the human menstrual cycle", "correct": "false" },
          { "text": "Buffer the strength of solar radiation", "correct": "false" },
        ]
      },
      {
        "question": "What did Apollo 11 see on the moon, according to revelations by William Tompkins?",
        "answers": [
          { "text": "Alien Crafts", "correct": "true" },
          { "text": "Forest", "correct": "false" },
          { "text": "Chang'e moon goddess", "correct": "false" },
          { "text": "Dinosaur", "correct": "false" },
        ]
      },
      {
        "question": "Which ancient Chinese book has the story of moon repairers who traveled from the moon?",
        "answers": [
          { "text": "'Classic of Mountains and Seas'", "correct": "false" },
          { "text": "'Strange Stories in Oriental Society'", "correct": "false" },
          { "text": "'You Yang Miscellany'", "correct": "true" },
          { "text": "'Bowuzhi - Records of Diverse Matters'", "correct": "false" },
        ]
      },
      {
        "question": "According to a 2018 report from National Geographic, how many moons did scientists discover that are surrounding the Earth?",
        "answers": [
          { "text": "Two", "correct": "false" },
          { "text": "Three", "correct": "true" },
          { "text": "Five", "correct": "false" },
          { "text": "Ten", "correct": "false" },
        ]
      },
      {
        "question": "According to the revelations by Montauk project whistleblower Stewart Swerdlow, who brought our moon?",
        "answers": [
          { "text": "Martian", "correct": "false" },
          { "text": "Draconian", "correct": "true" },
          { "text": "Lyran", "correct": "false" },
          { "text": "Arcturians", "correct": "false" },
        ]
      },
      {
        "question": "Which of the following is named after the moon goddess in Roman mythology?",
        "answers": [
          { "text": "Princess Diana", "correct": "true" },
          { "text": "Audrey Hepburn", "correct": "false" },
          { "text": "Statue of Liberty New York", "correct": "false" },
          { "text": "Angelina Jolie", "correct": "false" },
        ]
      },
      {
        "question": "What was Apollo 12's John Young's reaction when he was asked to put his hand on a Bible and swear that he had actually been to the moon?",
        "answers": [
          { "text": "He very quietly put his hand on the Bible and swore an oath", "correct": "false" },
          { "text": "He laughed and said he can't swear because he was an atheist", "correct": "false" },
          { "text": "He admitted that he has never actually been to the moon", "correct": "false" },
          { "text": "He was very upset and tried to shake off the questioner's question", "correct": "true" },
        ]
      },
      {
        "question": "What is the shape depicted by a moon analemma?",
        "answers": [
          { "text": "An oval '0' shape", "correct": "false" },
          { "text": "A perfect circle", "correct": "false" },
          { "text": "An '8' shape", "correct": "true" },
          { "text": "A straight line", "correct": "false" },
        ]
      }
    ]
    }
}


# JSONFile = 'bgben/main/starseed_test_file.json'
# fw = io.open(JSONFile , 'w', 'utf-8')
# json.dump(starseedQuestions, fw, ensure_ascii=False)
# fw.close()


with io.open('bgben/static/data/register_quiz.json', 'w', encoding='utf-8') as JSONFile:
  json.dump(registerTestQuestions, JSONFile, ensure_ascii=False)

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