from random import randint
from tkinter import *
from tkinter.messagebox import showerror, showinfo

import requests
# 开头先定义颜色变量，可以省去查询的步骤
color_red = "#ff8e8e"
color_blue = "#188eff"

def get_ssq() -> dict:
    # 获取双色球号码【核心】
    ssq = requests.get('http://www.17500.cn/ajax/awards.html',\
                        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36 Edg/97.0.1072.76'}).json()
    ssq = ssq['ssq']
    return ssq

def select_window():
    # 摇号窗口
    def generate_lott_red(continuous = False) -> list:
        # 生成红球
        if continuous:
            # 如果要求连续，则进行如下操作，看好了
            res = [0, 0, 0, 0, 0, 0]
            # ↑ 用0标注为需要随机数填补的地区，首先程序会将连续的数填入
            while True:
                # 重复，直到选出合适的位置和开始值
                length = randint(3, randint(3, 4))
                start_point = randint(0, 5)
                start_number = randint(1, 33)
                if start_point + length > 6:
                    # 如果超出了列表范围，就重开
                    continue
                else:
                    # 终于弄完了，退出
                    break
            
            # 接下来，开始循环填入数字
            j = 0
            for i in range(start_point, start_point + length):
                res[i] = str(start_number + j).rjust(2, '0')
                # ↑ 巧妙的运用rjust方法，不仅可以让字符串右对齐，
                # 还可以给数字补0。
                j += 1
            
            # 至此，复杂的连续部分已生成完毕，让我们把重心放到补坑上。
            for i in range(len(res)):
                # 循环
                if res[i] == 0:
                    # 如果是空位，则填数
                    while True:
                        tmp = str(randint(1, 33)).rjust(2, '0')
                        # ↑ 像这样的补0，以后你还会见到。
                        if tmp not in res:
                            # 如果该数字不在列表中，就填入，再退出死循环。
                            # 如果有这个数的话，就得继续重开。
                            res[i] = tmp
                            break
        else:
            # 如果没有复杂的连续数字的困扰，
            # 只用这些代码便可解决这个问题。
            res = []
            for i in range(6):
                while True:
                    tmp = str(randint(1, 33)).rjust(2, '0')
                    if tmp not in res:
                        res.append(tmp)
                        break
        
        # 双色球是需要排序的，这里排一下序，但是字符串怎么排序呢？
        # 当然是按照转换为整数后的排了。这样，我们还能保证
        # 显示出来的数字还有前面的0，因为转换为整数可以自动去除0。
        res = sorted(res, key=int)
        return ' '.join(res) # 根据空格分割，送给别的函数备用。
        # -------------------------------------------------------------
    
    def update_label():
        # 把功能封装一下，到时候用到。
        lott_red_text.config(text=generate_lott_red(continuous.get()))
        lott_blue_text.config(text=str(randint(1, 16)).rjust(2, '0'))
    # 随机选号窗口
    window_choose = Tk()
    window_choose.title('彩票助手 - 选号')
    window_choose.resizable(False, False)

    # 红球展示的文字
    lott_red_text = Label(window_choose, text='请点击按钮',\
                        font=('华文琥珀', 20), fg=color_red, height=2)
    lott_red_text.grid(row=0, column=0, padx=10, pady=10)

    # 蓝球展示的文字
    lott_blue_text = Label(window_choose, text='摇号吧~', \
                        font=('华文琥珀', 20), fg=color_blue)
    lott_blue_text.grid(row=0, column=1, padx=10, pady=10)

    # 设计的界面中也要有连续出号的选项
    # 使用一个Tk里独有的数字变量，存储
    # 用户选了什么
    continuous = IntVar()
    # 选了之后这个复选框会将上方变量设为1
    # 不选择就是0
    continuous_button = Checkbutton(window_choose, text='连续出号', \
                                    font=('等线', 15), onvalue=1,\
                                    offvalue=0, variable=continuous)
    continuous_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    # 把这个按钮跟那个封装的函数绑起来，点了就执行那个
    start = Button(window_choose, text='开始摇号', command=update_label,\
                    height=2, font=('等线', 15))
    start.grid(row=2, column=0, columnspan=2, padx=10, pady=10)



def check_window():
    # 查彩窗口
    def check_lottery():
        # 先试试，如果有错误就弹窗
        try:
            num_1 = [int(i) for i in input_entry_1.get().split()]
            num_2 = [int(i) for i in input_entry_2.get().split()]
            win_num_1 = [int(i) for i in get_ssq()['winnum']]
            win_num_2 = [int(i) for i in get_ssq()['winnum2']]
            if num_1 == win_num_1 and num_2 == win_num_2:
                # 6红 1蓝 （全等于）
                showinfo('OHHHHHHH', '你中了一等奖！我不敢相信！')
                showinfo('不想说啥了', '现在就去兑奖！快！')
            elif num_1 == win_num_1 and num_2 != win_num_2:
                # 6红 0蓝（红相等）
                showinfo('太牛了你！', '中了二等奖！')
            elif num_1 != win_num_1 and num_2 == win_num_2:
                # 0红 1蓝（最次的，只是蓝等于）
                showinfo('六等奖', '等于五元')
                # 以上是一些比较简单的判断条件
            else:
                # 上面记过了只中蓝的情况，因此那样子的情况不用再比对
                red_count = 0
                for i in range(6):
                    if num_1[i] == win_num_1[i]:
                        red_count += 1
                
                # 从5红 1蓝开始
                if red_count == 5 and num_2 == win_num_2:
                    # 三等奖
                    showinfo('三等奖', '真厉害！三等奖！3000元呢，快去拿！')
                elif red_count == 5 and num_2 != win_num_2 or red_count == 4 and num_2 == win_num_2:
                    # 四等
                    showinfo('四等奖（200元）', '不错！应该把本挣回来了吧')
                elif red_count == 4 and num_2 != win_num_2 or red_count == 3 and num_2 == win_num_2:
                    # 五等
                    showinfo('五等奖 （10元）', '还行')
                elif red_count >= 0 and num_2 == win_num_2:
                    # 否则后面的估计都是六了吧
                    showinfo('六等奖 （5元）', '中奖了，不过才5元，彩票公司真扣。')
                else:
                    showinfo('很抱歉', '这次彩票并没有中奖，若认为结果有误，可前往首页查看')
        except IndexError:
            # 我就好奇了哪个人会乱按，烦死了
            showerror('出错了', '你输入的内容有误')
        finally:
            # 最后关窗口，不为别的，就是觉得得关掉
            window_check.destroy()
    
    # 创建窗口
    window_check = Tk()
    window_check.resizable(False, False)
    window_check.title('彩票助手 - 查彩')
    input_tips = Label(window_check, \
                        text='请输入红球和蓝球 数字之间空格隔开',\
                        font=('等线', 15))
    
    # 本来想挨个数字都一个输入框的，但是做起来很麻烦
    # 有时候为了一些目标，你总要舍弃一些，对吧？
    # （自我安慰）
    input_entry_1 = Entry(window_check, font=('华文琥珀', 16))
    input_entry_2 = Entry(window_check, width=3, font=('华文琥珀', 16))

    # 完成按钮
    ok_button = Button(window_check, text='查询中奖情况', \
                        font=('等线', 16), command=check_lottery)

    # 排列位置
    input_tips.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
    input_entry_1.grid(row=1, column=0, padx=10, pady=10)
    input_entry_2.grid(row=1, column=1, padx=10, pady=10)
    ok_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
        

def main_window():
    # 重要嘉宾：主窗口来了
    window = Tk()
    window.title('彩票助手')
    window.resizable(False, False)
    # 第一个，中奖规则
    # 话说LabelFrame是个好东西，很好的把元素们分割出了层级感
    # 编程上亦是如此
    frame_win = LabelFrame(window, text='加油吧，少年', labelanchor='n')
    frame_win.grid(row=0, column=0, rowspan=2, padx=10, pady=10)
    lott_red = Label(
        frame_win,
        text='6红\n\n6红\n\n5红\n\n5红\n\n4红\n\n4红\n\n3红\n\n2红\n\n1红\n\n0红',
        fg=color_red,
        font=(
            '等线',
            15 
        )
    )
    lott_red.grid(row=0, column=0, padx=10, pady=10)

    lott_blue = Label(
        frame_win,
        text='1蓝\n\n0蓝\n\n1蓝\n\n0蓝\n\n1蓝\n\n0蓝\n\n1蓝\n\n1蓝\n\n1蓝\n\n1蓝',
        fg=color_blue,
        font=(
            '等线',
            15 
        )
    )
    lott_blue.grid(row=0, column=1, padx=0, pady=10)

    lott_money = Label(
        frame_win,
        text='等于很多钱\n\n等于很多钱\n\n等于3000元\n\n等于200元\n\n等于200元\n\n等于10元\n\n等于10元\n\n等于5元\n\n等于5元\n\n等于5元',
        font=(
            '等线',
            15 
        )
    )
    lott_money.grid(row=0, column=2, padx=10, pady=10)

    # 终于弄完了，虽然有很多不完美的地方
    # 第二个，一览
    frame_view = LabelFrame(window, text='一览', labelanchor='n')
    frame_view.grid(row=0, column=1, padx=10, pady=10)
    # 这里用到了get_ssq ↓
    situation = Label(
        frame_view,
        text='上次第{}期开奖情况\n({})'.format(get_ssq()['issue'] ,get_ssq()['xinqi']),
        font=(
            '等线',
            15
        )
    )
    situation.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

    win_num_red = Label(
        frame_view,
        text=' '.join(get_ssq()['winnum']),
        font=(
            '华文琥珀',
            18
        ),
        fg=color_red
    )
    win_num_red.grid(row=1, column=0, padx=10, pady=10)

    win_num_blue = Label(
        frame_view,
        text=get_ssq()['winnum2'],
        font=(
            '华文琥珀',
            18
        ),
        fg=color_blue
    )
    win_num_blue.grid(row=1, column=1, padx=10, pady=10)

    # 第三个，操作
    frame_op = LabelFrame(window, text='操作', labelanchor='n')
    frame_op.grid(row=1, column=1, padx=10, pady=10)


    # 仍然是无趣的调参和排列
    choose_num = Button(frame_op, text='搏一搏，单车变摩托！', width=28,\
                        height=2, font=('等线', 12), command=select_window)
    query_lott = Button(frame_op, text='手气不错，中奖了没？', width=28,\
                        height=2, font=('等线', 12), command=check_window)
    choose_num.grid(row=0, column=0, padx=10, pady=41)
    query_lott.grid(row=1, column=0, padx=10, pady=41)
    # 最后一个，警示语
    # （我也不知道这玩意真正用处是啥）
    fbi_warning = Label(window,\
                        text='[ FBI WARNING ]\n\n购彩有节制，请理性投注！未满18周岁的未成年人不得购买彩票及兑奖！',\
                        font=('等线 Bold', 13),\
                        fg='#d6bc00')
    fbi_warning.grid(row=2, column=0, columnspan=2, padx=10, pady=4)
    # 至此 第一个页面已完成

    # 容易报错，下面这行代码暂时不要了
    # window.protocol("WM_DELETE_WINDOW", close)#只要其中一个窗口关闭,就同时关闭两个窗口

# 齐活，好了，跑一遍
main_window()
mainloop()

'''
这也许是我有史以来写过最多的代码了
量很多
说复杂也不复杂
只是Ctrl + C Ctrl + V罢了
整体上还行
耗时1.7天
嘿嘿(。・∀・)ノ
'''
