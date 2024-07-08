import flet as ft
import pypinyin as py
from enum import Enum


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


class P1(ft.Container):
    def __init__(self, 汉字='草', 声母='c', 韵母='ang', 声调='ˇ'):
        self.汉字 = text_button(text=汉字, width=80, height=80, size=50)
        self.汉字.disabled = True
        self.声母 = text_button(text=声母, width=20, height=25, size=20)
        self.韵母 = text_button(text=韵母, width=55, height=25, size=20)
        self.声调 = text_button(text=声调, width=80, height=20, size=30)
        super().__init__()
        self.width = 100
        self.height = 150
        # self.border = ft.border.all(1, ft.colors.GREY_300)
        self.content = ft.Column([
                ft.Row([self.声调], alignment=ft.MainAxisAlignment.CENTER, ),
                ft.Row([self.声母, self.韵母], alignment=ft.MainAxisAlignment.CENTER, spacing=5),
                ft.Row([self.汉字], alignment=ft.MainAxisAlignment.CENTER, spacing=0), ],
                spacing=5, alignment=ft.MainAxisAlignment.CENTER)

    def updates(self, 汉字, 声母, 韵母, 声调):
        self.汉字.updates(汉字)
        self.声母.updates(声母)
        self.韵母.updates(韵母)
        self.声调.updates(声调)

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


num2tone = {1: 'ˉ', 2: 'ˊ', 3: 'ˇ', 4: 'ˋ', 5: ' '}


class P2(ft.Container):

    def get_pinyin(self, 成语):
        sm = [i[0] if i[0] else ' ' for i in py.pinyin(成语, style=py.Style.INITIALS, heteronym=True, strict=False)]
        ym_t = [[i[0][:-1], i[0][-1]] if i[0][:-1] else [i[0][-1], 5] for i in
                py.pinyin(成语, style=py.Style.FINALS_TONE3, heteronym=True, strict=False)]
        c = []
        for i, ii, iii in zip(sm, ym_t, 成语):
            c.append([iii, i, ii[0], num2tone[int(ii[1])]])
        return c

    def __init__(self, 成语="一败涂地"):
        self.c = []

        for i, ii, iii, iiii in self.get_pinyin(成语):
            self.c.append(P1(汉字=i, 声母=ii, 韵母=iii, 声调=iiii))
        super().__init__()
        self.content = ft.Column(
                [ft.Row(self.c[:2], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
                 ft.Row(self.c[2:], alignment=ft.MainAxisAlignment.CENTER, spacing=10), ], spacing=5,
                alignment=ft.MainAxisAlignment.CENTER
        )

    def updates(self, 成语):
        for index, value in enumerate(self.get_pinyin(成语)):
            i, ii, iii, iiii = value
            self.c[index].updates(i, ii, iii, iiii)
        self.update()

    def disableds(self):
        for i in self.c:
            i.disableds()

    def enables(self):
        for i in self.c:
            i.enables()


def main(page: ft.Page):
    def 开始修改(text):
        # global now
        nonlocal display
        if type(text) is str:
            now = text
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
        更新列表(e)
        page.update()

    def 更新列表(e):
        nonlocal lv
        lv.controls.clear()
        for i in ['风声鹤唳', '草木皆兵', '一板一眼', '一鼓作气', '凄凄切切']:
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
