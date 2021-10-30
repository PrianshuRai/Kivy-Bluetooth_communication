from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.list import TwoLineListItem
from kivymd.uix.snackbar import Snackbar
# from kivy.core.window import Window
import bluetooth
import json
import time


# use this to define window size
# Window.size = (400, 600)


class Scanner(Screen):

    def run_bt(self):
        print('inside first screen')
        print('switching screen')


class Devices(Screen):
    pass


class Inputs(Screen):
    pass


class Landing(Screen):
    pass


scr = ScreenManager()
scr.add_widget(Scanner(name='scan'))
scr.add_widget(Devices(name='device'))
scr.add_widget(Inputs(name='data'))
scr.add_widget(Landing(name='land'))


class BluetoothApp(MDApp):

    main_data = {}

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        self.screens = Builder.load_file('layout.kv')
        return self.screens

    def bluetooth(self):
        phones = {}

        list_page = self.screens.get_screen('device').ids.bt_lst  # getting the id from screen
        list_page.clear_widgets()
        nearby_devices = bluetooth.discover_devices(
            duration=20,  # change the value to increase scan time
            lookup_names=True,  # get the name of the devices
            flush_cache=True,
            lookup_class=False)
        print(nearby_devices)
        for address, name in nearby_devices:
            phones[name] = address

        print('phones: ', phones)
        for name, address in phones.items():
            list_page.add_widget(
                TwoLineListItem(
                    text=f"Device: {name}",
                    secondary_text=f"addr: {address}"
                )
            )

    def runner(self):
        bd_addr = "28:C2:DD:20:26:16"

        port1 = 2

        sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        print("sock", sock)
        sock.connect((bd_addr, port1))
        print("connected")
        new_data = self.sender()
        sock.send(new_data)

        sock.close()

    def sender(self):
        self.main_data['user'] = self.screens.get_screen('data').ids.user.text
        self.main_data['ip'] = self.screens.get_screen('data').ids.ip.text
        self.main_data['port'] = self.screens.get_screen('data').ids.port.text
        self.main_data['netmask'] = self.screens.get_screen('data').ids.netmask.text
        self.main_data['interface'] = self.screens.get_screen('data').ids.interface.text
        self.main_data['syspassword'] = self.screens.get_screen('data').ids.syspassword.text
        self.main_data['management_server_ip'] = self.screens.get_screen('data').ids.management_server_ip.text
        self.main_data['gateway'] = self.screens.get_screen('data').ids.gateway.text
        self.main_data['Mac_id'] = self.screens.get_screen('data').ids.Mac_id.text
        self.main_data['status'] = self.screens.get_screen('data').ids.status.text
        print('Data added successfully...')
        dict_new = json.dumps(self.main_data)
        for i in self.main_data.values():
            if i == ('' and None):
                card = self.screens.get_screen('data').ids.crd
                card.add_widget(
                    Snackbar(
                        text='Some values are missing... Please check!',
                        snackbar_x="10dp",
                        snackbar_y="10dp"
                    )
                )
        print(self.main_data)
        config = json.loads(dict_new)
        return config


if __name__ == '__main__':
    BluetoothApp().run()
