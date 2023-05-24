from kivy.app import App
from kivy.properties import ListProperty, StringProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput

# Own module
from ip_calc import Network


class NumEntry(TextInput):
    supported_chars = ListProperty(tuple())

    def insert_text(self, substring: str, from_undo=False):
        if substring.isdecimal() or substring in self.supported_chars:
            if substring in self.supported_chars:
                if not len(self.text):  # add to text if there is no text
                    return super(NumEntry, self).insert_text(substring, from_undo)
                elif substring in self.supported_chars:  # and substring not in self.text:
                    return super(NumEntry, self).insert_text(substring, from_undo)  # only one . or - in text
                return super(NumEntry, self).insert_text('', from_undo)  # can't type - in the middle
            return super(NumEntry, self).insert_text(substring, from_undo)  # type numbers
        return super(NumEntry, self).insert_text('', from_undo)  # if not number don't type

    @property
    def float(self):
        """
        :return: Float of text
        """
        return float(self.text)

    @property
    def int(self):
        """
        :return: int of text
        """
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
            self.network_address = str(Network(self.input_box.text).network_address)
            self.broadcast_address = str(Network(self.input_box.text).broadcast_address)
            self.host0 = str(Network(self.input_box.text).host0)
            self.host_1 = str(Network(self.input_box.text).host_1)
            self.max_hosts = str(Network(self.input_box.text).max_hosts)

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
