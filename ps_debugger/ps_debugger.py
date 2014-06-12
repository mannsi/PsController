__author__ = 'mannsi'

from tkinter import *
from tkinter.ttk import *
from ps_controller.protocol.ProtocolFactory import ProtocolFactory
from ps_controller.logging.CustomLoggerInterface import CustomLoggerInterface
from ps_controller.Commands import *


class PsDebugger:
    def __init__(self):
        self.set_v_button = None
        self.set_v_entry = None
        self.set_c_button = None
        self.set_c_entry = None
        self.get_all_button = None
        self.connected_label = None
        self.tree = None
        self.last_message_id = None
        custom_logger = DebugLogger(ps_debugger=self)
        self._hardware_interface = ProtocolFactory(logger=custom_logger).get_protocol("usb")
        root = Tk()
        self.add_ui(root)
        root.mainloop()

    def add_ui(self, tk_root: Tk):
        self.add_communications(tk_root)
        self.add_operations(tk_root)
        self.add_connect_panel(tk_root)

    def add_communications(self, tk_root: Tk):
        Label(tk_root, text="Communication").grid(row=0, column=0)
        self.tree = Treeview(tk_root)
        self.tree.column('#0', width=100, anchor='w')
        self.tree.heading('#0', text='Direction', anchor='w')
        self.tree['columns'] = ('command', 'data', 'serial', 'message')
        self.tree.column('command', width=150, anchor='w')
        self.tree.heading('command', text='Command', anchor='w')
        self.tree.column('data', width=100, anchor='w')
        self.tree.heading('data', text='Data', anchor='w')
        self.tree.column('serial', width=150, anchor='w')
        self.tree.heading('serial', text='Serial', anchor='w')
        self.tree.column('message', width=500, anchor='w')
        self.tree.heading('message', text='Message', anchor='w')

        self.tree.grid(column=0, row=1, rowspan=3)
        s = Scrollbar(tk_root, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=s.set)
        s.grid(column=1, row=1, rowspan=3, sticky=(N, S))

    def add_operations(self, tk_root: Tk):
        Label(tk_root, text="Operations").grid(row=0, column=2, columnspan=2)
        self.set_v_button = Button(
            tk_root, text="Set V",
            command=lambda: self.run_operation(ReadTargetCurrentCommand(), self.set_v_entry.get()))
        self.set_v_button.grid(row=1, column=2)
        self.set_v_entry = Entry(tk_root)
        self.set_v_entry.grid(row=1, column=3)

        self.set_c_button = Button(
            tk_root, text="Set C",
            command=lambda: self.run_operation(ReadTargetCurrentCommand(), self.set_c_entry.get()))
        self.set_c_button.grid(row=2, column=2)
        self.set_c_entry = Entry(tk_root)
        self.set_c_entry.grid(row=2, column=3)

        self.get_all_button = Button(
            tk_root, text="Get all",
            command=lambda: self.run_operation(WriteAllValuesCommand(), ''))
        self.get_all_button.grid(row=3, column=2)

    def add_connect_panel(self, tk_root: Tk):
        (num_rows, num_columns) = tk_root.grid_size()
        self.connected_label = Label(tk_root, text="")
        self.connected_label.grid(row=num_rows, column=0, sticky=W)
        Button(tk_root, text="Connect", command=self.button_connect_click).grid(row=num_rows, column=3, sticky=E)

    def button_connect_click(self):
        self._hardware_interface.connect()
        if self._hardware_interface.connected():
            self.connected_label["text"] = "Connected"

    def add_message(self, to_device: bool, command: BaseCommand, data: str, serial: str, message: str):
        if to_device:
            first_string = "To PS201"
        else:
            first_string = "From PS201"
        self.last_message_id = self.tree.insert('', 'end', '', text=first_string,
                                                values=(command.readable(), data, serial, message))

    def add_error_message(self, error_message: str):
        self.tree.insert('', 'end', text='', values=('', '', '', error_message))

    def add_info_message(self, info_message: str):
        self.tree.insert('', 'end', text='', values=('', '', '', info_message))

    def run_operation(self, command: BaseCommand, data):
        try:
            if command == WriteAllValuesCommand():
                self._hardware_interface.get_all_values()
            elif command == ReadTargetVoltageCommand():
                self._hardware_interface.set_target_voltage(data)
            elif command == ReadTargetCurrentCommand():
                self._hardware_interface.set_target_current(data)
            elif command == TurnOnOutputCommand():
                self._hardware_interface.set_device_is_on(True)
            elif command == TurnOffOutputCommand():
                self._hardware_interface.set_device_is_on(False)
            elif command == StartStreamCommand():
                self._hardware_interface.start_streaming()
            elif command == StopStreamCommand():
                self._hardware_interface.stop_streaming()
        except Exception as e:
            self.add_error_message("ERROR. Message: " + str(e))


class DebugLogger(CustomLoggerInterface):
    def __init__(self, ps_debugger: PsDebugger):
        self.ps_debugger = ps_debugger

    def log_sending(self, command, data, serial, message=''):
        self.ps_debugger.add_message(to_device=True, command=command, data=data, serial=str(serial), message=message)

    def log_receiving(self, device_response):
        self.ps_debugger.add_message(to_device=FALSE, command=device_response.command,
                                     data=device_response.data, serial=device_response.readable_serial, message='')

    def log_error(self, error_message):
        self.ps_debugger.add_error_message(error_message)

    def log_info(self, info_message):
        self.ps_debugger.add_info_message(info_message)

if __name__ == "__main__":
    PsDebugger()









