#-----------------------------欢迎使用pyart库-----------------------------#
#-使用前，请先安装jieba库、os库（可选）、webrrowser库（可选）、pyecharts库（可选）-#
#---------------github网站：https://github/fourlight/pyart --------------#
import jieba

class wordcloud():
    def __init__(self, txt):
        with open(txt, 'r', encoding="utf-8") as f:
            text = f.read()
            self.words = jieba.lcut(text)

    def add(self, word, words_dict):
        if word in words_dict:
            words_dict[word] += 1
        else:
            words_dict[word] = 1

    # 统计
    def count(self,
              ignore_single = True, # 忽略单个字（符）
              ignore_num = True # 忽略数字
              ):
        words_dict = {}

        drop = ['我们', '你们', '他们', '就是', '不是', '什么', '虽然', '但是', '可是', '因为', '所以', '没有', '不是', '可能', '自己']

        for word in self.words:
            if word not in drop and '一' not in word:
                # 单个字（符）检测
                single = len(word) == 1
                # 数字检测
                num = True
                try:
                    int(word)
                except:
                    num = False

                if ignore_num and ignore_single:
                    if not single and not num:
                        self.add(word, words_dict)
                elif ignore_single and not ignore_num:
                    if not single:
                        self.add(word, words_dict)
                elif ignore_num:
                    if not num:
                        self.add(word, words_dict)
                else:
                    self.add(word, words_dict)

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