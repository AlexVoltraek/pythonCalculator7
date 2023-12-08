from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
import math

class CalculatorApp(App):
    def build(self):
        self.display = TextInput(font_size=32, multiline=False, readonly=True, halign='right', background_color=(1, 1, 1, 1), size_hint=(1, 1))
        self.root_number = ""

        bl = BoxLayout(orientation='vertical')
        bl.add_widget(self.display)

        buttons = [
            ['C', ' ', ' ', 'Del'],
            ['√', '(', ')', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['.', '0', '**', '=']
        ]

        for row in buttons:
            h_layout = BoxLayout(size_hint_y=None, height=85)
            for label in row:
                button = Button(text=label, font_size=32, size_hint_x=32, width=100)
                button.bind(on_press=self.on_button_press)
                h_layout.add_widget(button)
            bl.add_widget(h_layout)

        return bl

    def on_button_press(self, instance):
        button_text = instance.text

        if 'Error' in self.display.text:
            self.display.text = ""

        if button_text == '=':
            try:
                result = self.evaluate_expression(self.display.text)
                self.display.text = str(result)
            except Exception:
                self.display.text = "Error"
        elif button_text == 'Del':
            self.display.text = self.display.text[:-1]
        elif button_text == 'C':
            self.display.text = ""
            self.root_number = ""
        elif button_text == '√':
            current_text = self.display.text
            if not current_text.endswith('**') and not current_text.endswith('√'):
                self.display.text += '√('
                self.root_number = '√('
        elif button_text == '**':
            self.display.text += '**'
        elif button_text.isnumeric() or button_text in {'(', ')', '.', '+', '-', '*', '/'}:
            current_text = self.display.text
            if self.root_number and current_text.endswith('√('):
                self.root_number += button_text
                self.display.text = self.root_number
            elif current_text.endswith('√('):
                self.root_number = '√(' + button_text
                self.display.text = self.root_number
            else:
                self.display.text += button_text
        else:
            self.display.text = button_text

    def evaluate_expression(self, expression):
        expression = expression.replace('√(', 'math.sqrt(').replace('^', '**')
        result = eval(expression)

        return result / 2

if __name__ == '__main__':
    CalculatorApp().run()
