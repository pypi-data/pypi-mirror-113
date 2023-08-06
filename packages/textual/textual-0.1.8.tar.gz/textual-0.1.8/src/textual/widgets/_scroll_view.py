from __future__ import annotations

from rich.console import RenderableType
from rich.style import StyleType


from .. import events
from ..layouts.grid import GridLayout
from ..message import Message
from ..scrollbar import ScrollTo, ScrollBar
from ..geometry import clamp
from ..page import Page
from ..view import View
from ..reactive import Reactive


class ScrollView(View):
    def __init__(
        self,
        renderable: RenderableType | None = None,
        *,
        name: str | None = None,
        style: StyleType = "",
        fluid: bool = True,
    ) -> None:
        self.fluid = fluid
        self.vscroll = ScrollBar(vertical=True)
        self.hscroll = ScrollBar(vertical=False)
        self.page = Page(renderable or "", style=style)
        layout = GridLayout()
        layout.add_column("main")
        layout.add_column("vscroll", size=1)
        layout.add_row("main")
        layout.add_row("hscroll", size=1)
        layout.add_areas(
            content="main,main", vscroll="vscroll,main", hscroll="main,hscroll"
        )
        layout.show_row("hscroll", False)
        layout.show_row("vscroll", False)
        super().__init__(name=name, layout=layout)

    x: Reactive[float] = Reactive(0, repaint=False)
    y: Reactive[float] = Reactive(0, repaint=False)

    target_x: Reactive[float] = Reactive(0, repaint=False)
    target_y: Reactive[float] = Reactive(0, repaint=False)

    def validate_x(self, value: float) -> float:
        return clamp(value, 0, self.page.contents_size.width - self.size.width)

    def validate_target_x(self, value: float) -> float:
        return clamp(value, 0, self.page.contents_size.width - self.size.width)

    def validate_y(self, value: float) -> float:
        return clamp(value, 0, self.page.contents_size.height - self.size.height)

    def validate_target_y(self, value: float) -> float:
        return clamp(value, 0, self.page.contents_size.height - self.size.height)

    async def watch_x(self, new_value: float) -> None:
        self.page.x = round(new_value)
        self.hscroll.position = round(new_value)

    async def watch_y(self, new_value: float) -> None:
        self.page.y = round(new_value)
        self.vscroll.position = round(new_value)

    async def update(self, renderabe: RenderableType) -> None:
        self.page.update(renderabe)
        self.require_repaint()

    async def on_mount(self, event: events.Mount) -> None:
        assert isinstance(self.layout, GridLayout)
        self.layout.place(
            content=self.page,
            vscroll=self.vscroll,
            hscroll=self.hscroll,
        )
        await self.layout.mount_all(self)

    def scroll_up(self) -> None:
        self.target_y += 1.5
        self.animate("y", self.target_y, easing="out_cubic", speed=80)

    def scroll_down(self) -> None:
        self.target_y -= 1.5
        self.animate("y", self.target_y, easing="out_cubic", speed=80)

    def page_up(self) -> None:
        self.target_y -= self.size.height
        self.animate("y", self.target_y, easing="out_cubic")

    def page_down(self) -> None:
        self.target_y += self.size.height
        self.animate("y", self.target_y, easing="out_cubic")

    def page_left(self) -> None:
        self.target_x -= self.size.width
        self.animate("x", self.target_x, speed=120, easing="out_cubic")

    def page_right(self) -> None:
        self.target_x += self.size.width
        self.animate("x", self.target_x, speed=120, easing="out_cubic")

    async def on_mouse_scroll_up(self, event: events.MouseScrollUp) -> None:
        self.scroll_up()

    async def on_mouse_scroll_down(self, event: events.MouseScrollUp) -> None:
        self.scroll_down()

    async def on_key(self, event: events.Key) -> None:
        await self.dispatch_key(event)

    async def key_down(self) -> None:
        self.target_y += 2
        self.animate("y", self.target_y, easing="linear", speed=100)

    async def key_up(self) -> None:
        self.target_y -= 2
        self.animate("y", self.target_y, easing="linear", speed=100)

    async def key_pagedown(self) -> None:
        self.target_y += self.size.height
        self.animate("y", self.target_y, easing="out_cubic")

    async def key_pageup(self) -> None:
        self.target_y -= self.size.height
        self.animate("y", self.target_y, easing="out_cubic")

    async def key_end(self) -> None:
        self.target_x = 0
        self.target_y = self.page.contents_size.height - self.size.height
        self.animate("x", self.target_x, duration=1, easing="out_cubic")
        self.animate("y", self.target_y, duration=1, easing="out_cubic")

    async def key_home(self) -> None:
        self.target_x = 0
        self.target_y = 0
        self.animate("x", self.target_x, duration=1, easing="out_cubic")
        self.animate("y", self.target_y, duration=1, easing="out_cubic")

    async def on_resize(self, event: events.Resize) -> None:
        if self.fluid:
            self.page.update()

    async def message_scroll_up(self, message: Message) -> None:
        self.page_up()

    async def message_scroll_down(self, message: Message) -> None:
        self.page_down()

    async def message_scroll_left(self, message: Message) -> None:
        self.page_left()

    async def message_scroll_right(self, message: Message) -> None:
        self.page_right()

    async def message_scroll_to(self, message: ScrollTo) -> None:
        if message.x is not None:
            self.target_x = message.x
        if message.y is not None:
            self.target_y = message.y
        self.animate("x", self.target_x, speed=150, easing="out_cubic")
        self.animate("y", self.target_y, speed=150, easing="out_cubic")

    async def message_page_update(self, message: Message) -> None:
        self.x = self.validate_x(self.x)
        self.y = self.validate_y(self.y)
        self.vscroll.virtual_size = self.page.virtual_size.height
        self.vscroll.window_size = self.size.height
        update = False
        if self.layout.show_column(
            "vscroll", self.page.virtual_size.height > self.size.height
        ):
            update = True

        self.hscroll.virtual_size = self.page.virtual_size.width
        self.hscroll.window_size = self.size.width

        if self.layout.show_row(
            "hscroll", self.page.virtual_size.width > self.size.width
        ):
            update = True

        if update:
            self.page.update()
            self.layout.reset_update()
