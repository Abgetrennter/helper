import flet as ft
import pypinyin as py
from enum import Enum
import json
from collections import namedtuple


class ButtonState(Enum):
    未定义 = 0
    不确定位置 = 1
    确定位置 = 2
    不存在 = 3


class text_button(ft.CupertinoFilledButton):
    def my_click(self, *args, **kwarg):
        match self.stat:
            # 未定义不能返回，后三者循环
            case ButtonState.未定义:
                self.stat = ButtonState.不确定位置
                self._text.color = '#ffDE7525'
            case ButtonState.不确定位置:
                self.stat = ButtonState.确定位置
                self._text.color = '#ff1D9C9C'
            case ButtonState.确定位置:
                self.stat = ButtonState.不存在
                self._text.color = '#ffAAAFB5'
            case ButtonState.不存在:
                self.stat = ButtonState.不确定位置
                self._text.color = '#ffDE7525'
        # print(self.stat)
        # args[0].page.update()
        self.update()

    def __init__(self, text, width, height, size=40):  # 显示文字
        super().__init__(opacity_on_click=0.8, on_click=self.my_click)
        self._text = ft.Text(text, size=size, font_family='sf')
        self.content = self._text
        self.padding = 0
        self.width = width
        self.height = height

        self.stat = ButtonState.未定义  # 应该在未定义、不确定位置、确定位置、无中间切换
        self.bgcolor = ft.colors.GREY_200
        self._text.color = '#ff5D6673'

    def updates(self, text):
        self._text.value = text
        self._text.color = '#ff5D6673'
        self._text.update()
        self.stat = ButtonState.未定义

    @property
    def value(self):
        return self._text.value


class TextBox(ft.CupertinoFilledButton):

    def __init__(self, click, text, width, height, size=40):  # 显示文字
        self.click = click
        super().__init__(opacity_on_click=0.8, on_click=lambda e: click(self._text.value))
        self._text = ft.Text(text, size=size, font_family='sf')
        self.content = self._text
        self.padding = 0
        self.width = width
        self.height = height
        self.bgcolor = ft.colors.GREY_200
        self._text.color = '#ff5D6673'


num2tone = {1: 'ˉ', 2: 'ˊ', 3: 'ˇ', 4: 'ˋ', 5: ' '}
字音 = namedtuple('字音', '声母 韵母 声调 汉字')


class 成语字音:
    def __init__(self, 成语: str = None, _list=None):
        self.成语 = None
        if 成语:
            self.成语 = 成语
            self.声母集合 = [i[0] if i[0] else ' ' for i in
                             py.pinyin(成语, style=py.Style.INITIALS, heteronym=True, strict=False)]
            ym_t = [[i[0][:-1], i[0][-1]] if i[0][:-1] else [i[0][-1], 5] for i in
                    py.pinyin(成语, style=py.Style.FINALS_TONE3, heteronym=True, strict=False)]
            self.韵母集合 = [i[0] if i[0] else ' ' for i in ym_t]
            self.声调集合 = [num2tone[int(i[1])] for i in ym_t]
            self.拼音集合 = [字音(*i) for i in zip(self.声母集合, self.韵母集合, self.声调集合, self.成语)]
        else:
            self.成语 = "".join(i[-1] for i in _list)
            self.声母集合 = [i[0] if i[0] else ' ' for i in _list]
            self.韵母集合 = [i[1] if i[1] else ' ' for i in _list]
            self.声调集合 = [num2tone[int(i[2])] for i in _list]
            self.拼音集合 = [字音(*i) for i in zip(self.声母集合, self.韵母集合, self.声调集合, self.成语)]

    def __iter__(self):
        return iter(self.拼音集合)


class P1(ft.Container):
    def __init__(self, 字: 字音):
        self.字 = 字
        self.汉字 = text_button(text=字.汉字, width=80, height=80, size=50)
        self.汉字.disabled = True
        self.声母 = text_button(text=字.声母, width=20, height=25, size=20)
        self.韵母 = text_button(text=字.韵母, width=55, height=25, size=20)
        self.声调 = text_button(text=字.声调, width=80, height=20, size=30)
        super().__init__()
        self.width = 100
        self.height = 150
        # self.border = ft.border.all(1, ft.colors.GREY_300)
        self.content = ft.Column([
                ft.Row([self.声调], alignment=ft.MainAxisAlignment.CENTER, ),
                ft.Row([self.声母, self.韵母], alignment=ft.MainAxisAlignment.CENTER, spacing=5),
                ft.Row([self.汉字], alignment=ft.MainAxisAlignment.CENTER, spacing=0), ],
                spacing=5, alignment=ft.MainAxisAlignment.CENTER)

    def updates(self, 字: 字音):
        self.字 = 字
        self.汉字.updates(字.汉字)
        self.声母.updates(字.声母)
        self.韵母.updates(字.韵母)
        self.声调.updates(字.声调)

    def disableds(self):
        self.汉字.disabled = True
        self.声母.disabled = True
        self.韵母.disabled = True
        self.声调.disabled = True

    def enables(self):
        self.汉字.disabled = True
        self.声母.disabled = False
        self.韵母.disabled = False
        self.声调.disabled = False

    def get_state(self):
        return self.声母.stat, self.韵母.stat, self.声调.stat


class P2(ft.Container):

    def __init__(self, 成语="一败涂地"):
        self.成语字音 = 成语字音(成语)
        self.c = [P1(h) for h in self.成语字音]

        super().__init__()
        self.content = ft.Column(
                [ft.Row(self.c[:2], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
                 ft.Row(self.c[2:], alignment=ft.MainAxisAlignment.CENTER, spacing=10), ], spacing=5,
                alignment=ft.MainAxisAlignment.CENTER
        )

    def updates(self, 成语):
        self.成语字音 = 成语字音(成语)
        for index, value in enumerate(self.成语字音):
            self.c[index].updates(value)
        self.update()

    def disableds(self):
        for i in self.c:
            i.disableds()

    def enables(self):
        for i in self.c:
            i.enables()

    def get_state(self):
        """
        {right: [s, y, t], maybe:[q,w],wrong:[z,x]}×
        right{s:[(s,0)]}
        """
        right = {'声母': [], '韵母': [], '声调': [], '成语': self.成语字音.成语}
        for i, v in enumerate(self.c):
            if v.声母.stat == ButtonState.确定位置:
                right['声母'].append((v.声母.value, i))
            if v.韵母.stat == ButtonState.确定位置:
                right['韵母'].append((v.韵母.value, i))
            if v.声调.stat == ButtonState.确定位置:
                right['声调'].append((v.声调.value, i))
        return right


def main(page: ft.Page):
    idioms = {}
    with open("assets/datas.json", "r", encoding='utf-8') as dataset:
        raw_idioms = json.load(dataset)
    #
    for raw_idiom in raw_idioms:
        idioms[raw_idiom] = 成语字音(_list=raw_idioms[raw_idiom])
    pass

    def 开始修改(text):
        # global now
        nonlocal display
        if type(text) is str:
            now = text
            inputs.value = text
        else:
            now = inputs.value

        if len(now) == 4 and all('\u4e00' <= i <= '\u9fff' for i in now):
            display.updates(now)
            display.enables()
            submit.disabled = False
            # sbutton.disabled = True
            page.update()

    def 确认修改(e):
        nonlocal display
        display.disableds()
        submit.disabled = True
        sbutton.disabled = False
        """
        放搜索的部分
        """
        # print(display.get_state())
        筛选(display.get_state())
        更新列表(e)
        page.update()

    def 筛选(_dict):
        """
        {right: [s, y, t], maybe:[q,w],wrong:[z,x]}×
        right{s:[(s,0)]}
        """
        nonlocal idioms
        if _dict['成语'] in idioms:
            del idioms[_dict['成语']]

        s = idioms.copy()

        for k, v in s.items():
            if not all(i[0] == v.声母集合[i[1]] for i in _dict['声母']):
                del idioms[k]
                continue
            if not all(i[0] == v.韵母集合[i[1]] for i in _dict['韵母']):
                del idioms[k]
                continue
            if not all(i[0] == v.声调集合[i[1]] for i in _dict['声调']):
                del idioms[k]
                continue

    def 更新列表(e=None):
        lv.controls.clear()
        for i in list(idioms)[:10]:
            lv.controls.append(TextBox(text=str(i), click=开始修改, width=50, height=50))
        lv.update()

    page.title = "春日影"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.fonts = {
            "wxkai": "fonts/wxkai.ttf",
            "sf"   : "fonts/SF.TTF",

    }
    page.theme = ft.Theme(font_family='wxkai')
    display = P2("武运昌隆")
    display.disableds()
    inputs = ft.TextField(label="输入成语", width=200, height=50, )
    submit = ft.ElevatedButton(text="修改完成", disabled=True, on_click=确认修改)
    sbutton = ft.ElevatedButton(text="确认", on_click=开始修改)
    lv = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=False)

    page.add(
            display,
            ft.Row([inputs, sbutton], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
            ft.Row([submit], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
            ft.Divider(height=9, thickness=3),
            lv
    )


ft.app(main, assets_dir="assets")
