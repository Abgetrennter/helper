import flet as ft

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
        print(self.stat)
        args[0].page.update()

    def __init__(self, text, width, height, size=40):  # 显示文字
        super().__init__(opacity_on_click=0.8, on_click=self.my_click)
        self._text = ft.Text(text, size=size)
        self.content = self._text
        self.padding = 0
        self.width = width
        self.height = height

        self.stat = ButtonState.未定义  # 应该在未定义、不确定位置、确定位置、无中间切换
        self.bgcolor = ft.colors.GREY_200
        self._text.color = '#ff5D6673'


class P1(ft.Container):
    def __init__(self, 汉字='草', 声母='c', 韵母='ang', 声调='ˇ'):
        self.汉字 = text_button(text=汉字, width=80, height=80, size=50)
        self.声母 = text_button(text=声母, width=20, height=25, size=20)
        self.韵母 = text_button(text=韵母, width=60, height=25, size=20)
        self.声调 = text_button(text=声调, width=80, height=20, size=30)
        super().__init__()
        self.width = 100
        self.height = 150
        #self.border = ft.border.all(1, ft.colors.GREY_300)
        self.content = ft.Column([
                ft.Row([self.声调],alignment=ft.MainAxisAlignment.CENTER, ),
                ft.Row([self.声母, self.韵母], alignment=ft.MainAxisAlignment.CENTER, spacing=0),
                ft.Row([self.汉字], alignment=ft.MainAxisAlignment.CENTER, spacing=0), ],
                spacing=0, alignment=ft.MainAxisAlignment.CENTER)


def main(page: ft.Page):
    page.title = "Hello World"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.fonts = {
            "wxkai": "fonts/wxkai.ttf",
            "sf"   : "fonts/ST.TTF",

    }
    page.theme = ft.Theme(font_family='sf')
    page.add(
            ft.Row([P1(),P1(),P1(),P1()],alignment=ft.MainAxisAlignment.CENTER)
    )


ft.app(main, assets_dir="assets")
