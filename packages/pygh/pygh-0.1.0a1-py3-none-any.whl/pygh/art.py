#-----------------------------欢迎使用pyart库-----------------------------#
#-使用前，请先安装jieba库、os库（可选）、webrrowser库（可选）、pyecharts库（可选）-#
#---------------github网站：https://github/fourlight/pygh ---------------#
import jieba

# 词云
class wordcloud():
    def __init__(self, txt):
        with open(txt, 'r', encoding="utf-8") as f:
            text = f.read()
            self.words = jieba.lcut(text)

    # 统计
    def count(self, ignore=[]):
        words_dict = {}
        # 默认忽略词语
        drop = ['我们', '你们', '他们', '就是', '不是', '什么', '虽然', '但是', '可是', '因为', '所以', '没有', '不是', '可能', '自己']
        drop += ignore
        for word in self.words:
            if word not in drop and '一' not in word and len(word) > 1:
                if word in words_dict:
                    words_dict[word] += 1
                else:
                    words_dict[word] = 1

        # 字典转列表
        key = list(words_dict.keys())
        value = list(words_dict.values())
        self.words_list = []
        for i in range(len(words_dict)):
            self.words_list.append((key[i], value[i]))

    # 最终绘制
    def draw(self, name):
        from pyecharts.charts import WordCloud
        wordcloud = WordCloud()
        wordcloud.add(series_name=name, data_pair=self.words_list)
        wordcloud.render()

    # 打开
    def open(self):
        import os, webbrowser
        webbrowser.open('file://' + os.path.realpath('render.html'))

    # 一次性操作（该操作下，忽略词语默认为空，不可更改）
    def go(self, name):
        self.count()
        self.draw(name)
        self.open()