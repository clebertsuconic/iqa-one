"""
Abstract (base) implementations of supported external client commands.
All options here are common to all kind of client commands, be it a
receiver, sender or connector.
Options are also common to implementation language (java, python, etc).
In case an implementation has a different set of options, specialize it
in a separate module inside abstract.client.command.impl.
"""
from iqa.components.clients.external.command.options.client_options import *
from iqa.system.command.command_base import Command


class ClientCommand(Command):
    """
    Base abstraction class for external clients commands. It encapsulates the
    args property and getter generates a new list based on ClientCommand's
    implementation details (based on states of internal ClientOptionsBase
    properties).
    """

    def __init__(self, args):
        super().__init__(args)

    @property
    def args(self):
        return self._build_command()

    def main_command(self) -> list:
        """
        List of arguments needed to run the client implementation.
        :return:
        """
        return NotImplemented

    def _build_command(self) -> list:
        """
        Builds the external client command based on all
        ClientOptionsBase properties available on implementing class,
        using optconstruct to produce the arguments list.
        :return:
        """
        all_options = {}
        valid_options = []

        for opt_name, opt_value in self.__dict__.items():
            # Skip members that are not an instance of ClientOptionsBase
            if not isinstance(opt_value, ClientOptionsBase):
                continue
            # List of populated options
            all_options.update(opt_value.to_dict())
            # Append list of valid options for each ClientOptionsBase
            # implementation
            valid_options += opt_value.valid_options()

        # Generates parameters list (only allowed will be added)
        params = [
                opt.generate(all_options).split(' ', 1)
                for opt in valid_options
                if opt.satisfied(all_options)
        ]
        params_flat = [item for param in params for item in param]

        return self.main_command() + params_flat


class ConnectorClientCommand(ClientCommand):
    """
    Abstract implementation of common Connector client options.
    """

    def main_command(self) -> list:
        return NotImplemented

    def __init__(self, stdout: bool = False, stderr: bool = False,
                 daemon: bool = False, timeout: int = 0,
                 encoding: str = "utf-8"):
        super(ClientCommand, self).__init__([], stdout, stderr, daemon,
                                            timeout, encoding)
        self.control = ControlOptionsCommon()
        self.logging = LoggingOptionsCommon()
        self.connection = ConnectionOptionsCommon()
        self.connector = ConnectorOptions()


class ReceiverClientCommand(ClientCommand):
    """
    Abstract implementation of common Receiver client options.
    """

    def main_command(self) -> list:
        return NotImplemented

    def __init__(self, stdout: bool = False, stderr: bool = False,
                 daemon: bool = False, timeout: int = 0,
                 encoding: str = "utf-8"):
        super(ClientCommand, self).__init__([], stdout, stderr, daemon,
                                            timeout, encoding)
        self.control = ControlOptionsReceiver()
        self.logging = LoggingOptionsSenderReceiver()
        self.transaction = TransactionOptionsSenderReceiver()
        self.connection = ConnectionOptionsCommon()
        self.receiver = ReceiverOptions()


class SenderClientCommand(ClientCommand):
    """
        Abstract implementation of common Sender client options.
    """

    def main_command(self) -> list:
        pass

    def __init__(self, stdout: bool = False, stderr: bool = False,
                 daemon: bool = False, timeout: int = 0,
                 encoding: str = "utf-8"):
        super(ClientCommand, self).__init__([], stdout, stderr, daemon,
                                            timeout, encoding)
        self.control = ControlOptionsSenderReceiver()
        self.logging = LoggingOptionsSenderReceiver()
        self.transaction = TransactionOptionsSenderReceiver()
        self.connection = ConnectionOptionsCommon()
        self.message = MessageOptionsSender()
