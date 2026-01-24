from kivy.app import App
from kivy.properties import ListProperty, StringProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput

# Own module
from ip_calc import Network


class NumEntry(TextInput):
    supported_chars = ListProperty(tuple())

    def insert_text(self, substring: str, from_undo=False):
        # not a number or a supported character
        if not substring.isdecimal() and substring not in self.supported_chars:
            return super().insert_text('', from_undo)

        # validate special characters
        if substring in self.supported_chars:
            if substring in self.text:
                return super().insert_text('', from_undo)

        return super().insert_text(substring, from_undo)

    @property
    def float(self):
        return float(self.text)

    @property
    def int(self):
        return int(self.text)


class Root(BoxLayout):
    network_address = StringProperty()
    broadcast_address = StringProperty()
    host0 = StringProperty()
    host_1 = StringProperty()
    max_hosts = StringProperty()

    input_box = ObjectProperty()

    def update(self):
        try:
            network = Network(*self.input_box.text.split(' '))
            self.network_address = str(network.network_address)
            self.broadcast_address = str(network.broadcast_address)
            self.host0 = str(network.host0)
            self.host_1 = str(network.host_1)
            self.max_hosts = str(network.max_hosts)

        except ValueError:
            self.network_address = 'Wrong IP'
            self.broadcast_address = 'Wrong IP'
            self.host0 = 'Wrong IP'
            self.host_1 = 'Wrong IP'
            self.max_hosts = 'Wrong IP'


class NetworkCalculator(App):
    pass


if __name__ == '__main__':
    NetworkCalculator().run()
