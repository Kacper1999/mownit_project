from plot_config import Plot
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.slider import Slider
import matplotlib.pyplot as plt
from kivy.uix.screenmanager import ScreenManager, Screen

p = Plot()


class ParameterSlider(BoxLayout):
    def __init__(self, text, lb, ub, value, round_to=2, **kwargs):
        super(ParameterSlider, self).__init__(orientation="vertical", **kwargs)
        self.text = text
        self.round_to = round_to
        self.label = Label(text=f"{text}: {value}")
        self.slider = Slider(min=lb, max=ub, value=value)
        self.slider.bind(value=self.update)
        self.add_widget(self.label)
        self.add_widget(self.slider)

    def update(self, _, value):
        self.label.text = f"{self.text}: {value:.{self.round_to}f}"


class SetupScreen(BoxLayout):
    def __init__(self, **kwargs):
        super(SetupScreen, self).__init__(orientation="vertical", **kwargs)
        self.add_widget(FigureCanvasKivyAgg(p.fig))

        def click_update(event):
            p.on_click(event)

        p.fig.canvas.mpl_connect('button_press_event', click_update)

        self.parameters_box = BoxLayout(size_hint=(1, 0.1))

        self.steps = ParameterSlider(text="Steps", lb=100, ub=2000, value=500, round_to=0)
        self.parameters_box.add_widget(self.steps)

        self.temperature = ParameterSlider(text="Temperature", lb=10, ub=100, value=20)
        self.parameters_box.add_widget(self.temperature)

        self.alpha = ParameterSlider(text="Alpha", lb=0.8, ub=0.999, value=0.99, round_to=4)
        self.parameters_box.add_widget(self.alpha)

        animate_button = Button(text="Animate")
        animate_button.bind(on_press=self.animate)
        self.parameters_box.add_widget(animate_button)

        def clear(_):
            p.clear()

        clear_button = Button(text="Clear")
        clear_button.bind(on_press=clear)
        self.parameters_box.add_widget(clear_button)

        self.add_widget(self.parameters_box)

    def animate(self, _):
        s = int(self.steps.slider.value)
        a = self.alpha.slider.value
        t = self.temperature.slider.value
        p.animate(steps=s, t=t, alpha=a)


class Manager(ScreenManager):
    pass


class MyApp(App):
    def build(self):
        self.screen_manager = ScreenManager()
        self.setup_screen = SetupScreen()
        screen = Screen(name="setup")
        screen.add_widget(self.setup_screen)
        self.screen_manager.add_widget(screen)

        return self.screen_manager


if __name__ == '__main__':
    app = MyApp()
    app.run()
