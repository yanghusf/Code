# encoding=utf-8
import jieba
import jieba.posseg as pseg #词性标注
import jieba.analyse as anls #关键词提取
# seg_list = jieba.cut("我来到北京清华大学", cut_all=True)
# print("Full Mode: " + "/ ".join(seg_list),type(seg_list)) # 全模式
#
# l_seg_list = jieba.lcut("我来到北京清华大学")
# print("l_seg_list Mode: " + "/ ".join(l_seg_list), type(l_seg_list)) # 精确模式返回列表模式
#
# seg_list = jieba.cut("我来到北京清华大学", cut_all=False)
# print("Default Mode: " + "/ ".join(seg_list)) # 精确模式
#
# seg_list = jieba.cut("他来到了网易杭研大厦") # 默认是精确模式
# print(", ".join(seg_list))
#
# seg_list = jieba.cut_for_search("小明硕士毕业于中国科学院计算所，后在日本京都大学深造") # 搜索引擎模式
# print(", ".join(seg_list),type(seg_list))

# words = pseg.cut("他改变了中国")
# for word, flag in words:
#     print("{0} {1}".format(word, flag))

# 添加自定义词典
# jieba.add_word("蜂蜜很甜")

# seg_list = jieba.cut("蜂蜜很甜很好吃")
# print(' '.join(seg_list))

# 添加自己的文本
jieba.load_userdict(r'F:\pro\development\use_dict')
seg_list = jieba.cut("蜂蜜很甜很好吃")
print()
print(' '.join(seg_list))

jieba.suggest_freq(("垃", "圾"), tune=True)

sege_list = jieba.cut("最近找工作真的很垃圾")
print(''.join(sege_list))




















