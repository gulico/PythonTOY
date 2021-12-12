# J_SnowMan目黑莲11月30日《消失的初恋》宣传weibo评论分析&用户最近参与超话情况调查

- 数据来源：[J_SnowMan一些话想对大家说](https://m.weibo.cn/detail/4709336482318969)


## 基本情况

- 调查时间：2021.12.10-11
- 获取有效评论**11809**条，占显示数据1.7w条的**70%**
  - 技术问题，爬到后面好多重复的
  - 但是占总数比例还可以，可信度算70%吧
- 参与评论的用户**7656**位，其中最近有参与超话的**7486**位，占**98%**
- 为什么不获取转发和点赞情况？
  - 夹总限制转发只能查看前280页、点赞前250页，能获取的数据占总体比例太少，参考价值有限。
  - 评论可以根据每次json数据中带的max_id获得下一“页”的参数，操作得当的话应该是可以取全的🤔。

## 大家都评论了什么

### 词云

## ![comment_all_f](https://github.com/gulico/PythonTOY/tree/master/LLZ_WB/fig/comment_all_f.png)

### 词频

|    词语    | 词频 |  词性  |
| :--------: | :--: | :----: |
|    meme    | 9924 | 字符串 |
|   第二季   | 5904 |  数词  |
| 消失的初恋 | 5679 | 字符串 |
|    中文    | 5253 |  名词  |
|     め     | 4797 | 字符串 |
|    喜欢    | 4656 |  动词  |
|   啊啊啊   | 4629 |  名词  |
|     🖤      | 4455 | 字符串 |
|     た     | 3684 | 字符串 |

## 最近参与的超话

![超话前20](https://github.com/gulico/PythonTOY/tree/master/LLZ_WB/fig/超话前20.png)

- 《消失的初恋》主演以及相关cp超话一骑绝尘不用说了。

- 看一下其他的基本上都是一些耽改/耽美主演及其cp超话，还有目黑君的团超和队友们。（我们同人女跑来跑去还是这群人唉🤔）

- 我觉得比较特别的是四字居然也在榜上，咨询了一下认识的纸鸟姐姐，总结了几点可能性
  1. 最近拍戏纸鸟太闲了；
  2. 人多；
  3. 爱嗑cp。

## 参与'目黑莲''道枝駿佑''莲理枝memi'超话分布

![三个超话分布（注释版）](https://github.com/gulico/PythonTOY/tree/master/LLZ_WB/fig/三个超话分布（注释版）.png)

直接上注释版了。

- 众所周知这条weibo鸟人和莲姨有在battle，battle的结果嘛🥺。。看来有在关注莲理枝memi的用户是纯莲姨的近3倍呢🥺

p.s:如果你想说“我没关注x超话啊，但我还是喜欢x”or“我关注了x超话，但是随便关注的”。我想说一个人没办法代表全体，特例不在我的考虑范围内。

pps:枝姨和花妈不来这条微博互动太正常了，毕竟是相方的weibo啊😂。要是道枝也有微博就好了，我一定大搞特搞。

## 文件结构

- [LLZ_WB_COMMENT.ipynb](https://github.com/gulico/PythonTOY/tree/master/LLZ_WB/LLZ_WB_COMMENT.ipynb)  按热度获取指定weibo评论
- [LLZ_WB_REPOST.ipynb](https://github.com/gulico/PythonTOY/tree/master/LLZ_WB/LLZ_WB_REPOST.ipynb) 翻页获取指定weibo转发（限制280页）
- [get_suTopic.ipynb](https://github.com/gulico/PythonTOY/tree/master/LLZ_WB/get_suTopic.ipynb) 获取指定用户最近参与的超话列表
- [analysis.ipynb](https://github.com/gulico/PythonTOY/tree/master/LLZ_WB/analysis.ipynb) 数据处理&分析
- comment_*.txt 分别是所有用户的评论、只关注目黑莲不关注莲理枝memi和道枝骏佑超话的用户评论、只关注道枝骏佑不关注莲理枝memi和目黑莲超话的用户评论
- 词频_*.txt 分别是所有用户的评论的词频、只关注目黑莲不关注莲理枝memi和道枝骏佑超话的用户评论的词频、只关注道枝骏佑不关注莲理枝memi和目黑莲超话的用户评论的词频
- [stopwords1893.txt](https://github.com/gulico/PythonTOY/tree/master/LLZ_WB/stopwords1893.txt) 停止词
- [userdict.txt](https://github.com/gulico/PythonTOY/tree/master/LLZ_WB/userdict.txt) 用户辞典
- [J_SNOWMAN_4709336482318969.db](https://github.com/gulico/PythonTOY/tree/master/LLZ_WB/J_SNOWMAN_4709336482318969.db) 数据库
- [SourceHanSans-Bold.ttf](https://github.com/gulico/PythonTOY/tree/master/LLZ_WB/SourceHanSans-Bold.ttf) 生成词云所需字体

## 参考

1. [用python实现词频分析+词云](https://blog.csdn.net/weixin_43969938/article/details/104092240)

2. [我用python爬了榜姐微博下60000个女生小秘密！](https://www.52pojie.cn/thread-1123043-1-1.html)

