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
        self.switch_output_on_button = None
        self.switch_output_off_button = None
        self.connected_label = None
        self.tree = None
        self.operation_frame = None
        self.last_message_id = None
        custom_logger = DebugLogger(ps_debugger=self)
        self._hardware_interface = ProtocolFactory(logger=custom_logger).get_protocol("usb")
        root = Tk()
        root.geometry("1500x500")
        content_frame = Frame(root)
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_rowconfigure(1, weight=1)
        self.add_ui(content_frame)
        content_frame.pack(fill=BOTH, expand=True)
        root.mainloop()

    def add_ui(self, root: Frame):
        Label(root, text="Communication").grid(row=0, column=0)
        tree = self.get_communication_tree(root)
        tree.grid(row=1, column=0, sticky=(NSEW))
        s = Scrollbar(root, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=s.set)
        s.grid(column=0, row=1, sticky=(N, S, E))

        Label(root, text="Operations").grid(row=0, column=1)
        operation_frame = self.get_operation_frame(root)
        operation_frame.grid(row=1, column=1, sticky=N)

        self.connected_label = Label(root, text="")
        self.connected_label.grid(row=2, column=0)
        Button(root, text="Connect", command=self.button_connect_click).grid(row=2, column=1, sticky=(SE))

        # self.add_operations(parent)
        # self.add_connect_panel(parent)

    def get_communication_tree(self, parent: Frame):
        self.tree = Treeview(parent)
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
        return self.tree

    def get_operation_frame(self, parent: Frame):
        operation_frame = Frame(parent)

        self.set_v_button = Button(
            operation_frame, text="Set V",
            command=lambda: self.run_operation(ReadTargetVoltageCommand(), self.set_v_entry.get()))
        self.set_v_button.grid(row=0, column=0, sticky=(EW))
        self.set_v_entry = Entry(operation_frame)
        self.set_v_entry.grid(row=0, column=1)

        self.set_c_button = Button(
            operation_frame, text="Set C",
            command=lambda: self.run_operation(ReadTargetCurrentCommand(), self.set_c_entry.get()))
        self.set_c_button.grid(row=1, column=0, sticky=(EW))
        self.set_c_entry = Entry(operation_frame)
        self.set_c_entry.grid(row=1, column=1)

        self.get_all_button = Button(
            operation_frame, text="Get all",
            command=lambda: self.run_operation(WriteAllValuesCommand(), ''))
        self.get_all_button.grid(row=2, column=0, sticky=(EW))

        self.switch_output_on_button = Button(
            operation_frame, text="Output on",
            command=lambda: self.run_operation(TurnOnOutputCommand(), ''))
        self.switch_output_on_button.grid(row=3, column=0,  sticky=(EW))

        self.switch_output_off_button = Button(
            operation_frame, text="Output off",
            command=lambda: self.run_operation(TurnOffOutputCommand(), ''))
        self.switch_output_off_button.grid(row=4, column=0,  sticky=(EW))

        return operation_frame

    def button_connect_click(self):
        self._hardware_interface.connect()
        if self._hardware_interface.connected():
            self.connected_label["text"] = "Connected"

    def add_message(self, to_device: bool, command: BaseCommand, data: str, serial: str, message: str):
        if to_device:
            first_string = "To PS201"
        else:
            first_string = "From PS201"
        self.last_message_id = self.tree.insert('', 0, '', text=first_string,
                                                values=(command.readable(), data, serial, message))

    def add_error_message(self, error_message: str):
        self.tree.insert('', 0, text='', values=('', '', '', error_message))

    def add_info_message(self, info_message: str):
        self.tree.insert('', 0, text='', values=('', '', '', info_message))

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









