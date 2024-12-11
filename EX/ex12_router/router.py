"""Route all the packets."""
import re


class Packet:
    """Packet class."""

    def __init__(self, content: str, source_ip: str, destination_ip: str, id: int, sequence_number: int):
        """Initialize packet class."""
        self.content = content
        self.source_ip = source_ip
        self.destination_ip = destination_ip
        self.id = id
        self.sequence_number = sequence_number

    def __repr__(self) -> str:
        """
        Represent packet.

        Format the string of the packet as:
        '[content] from [source_ip] to [destination_ip] ([id]:[sequence_number])'
        """
        return f'{self.content} from {self.source_ip} to {self.destination_ip} ({self.id}:{self.sequence_number})'


class EndDevice:
    """End device class."""

    def __init__(self):
        """
        Initialize end device.

        End device will have an IP address if they are connected to a router.
        Also, end device will collect all packets that are sent to them.
        """
        self.ip_address = ""
        self.packets = []

    def get_ip_address(self) -> str:
        """Return the current IP address of the device."""
        return self.ip_address

    def set_ip_address(self, ip_address: str) -> None:
        """
        Set an IP address for the device.

        You don't need to validate the IP address here.
        """
        self.ip_address = ip_address

    def add_packet(self, packet: Packet) -> None:
        """Add a packet to end device."""
        self.packets.append(packet)

    def clear_packet_history(self) -> None:
        """Clear all packets from history."""
        self.packets = []

    def get_all_packets(self) -> list[Packet]:
        """Get a list of all packets in the order they were added."""
        return self.packets

    def get_all_packets_by_id(self, given_id: int) -> list[Packet]:
        """Get a list of all packets that have the given ID."""
        return list(filter(lambda packet: packet.id == given_id, self.packets))

    def get_all_packets_by_source_ip(self, given_ip: str) -> list[Packet]:
        """Get a list of all packets that have given source IP."""
        return list(filter(lambda packet: packet.source_ip == given_ip, self.packets))


class Router:
    """Router class."""

    def __validate_ipv4(self, ip_address: str) -> bool:
        """Validate IPv4."""
        pattern_ip = r"((\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5]))"
        match = re.fullmatch(pattern_ip, ip_address)
        return match is not None

    def __init__(self, ip_address: str):
        """
        Initialize router.

        IP address must be a string in the format "x.x.x.1"
        where x is a number in the range [0, 255], such as "192.168.0.1".

        If the IP address does not match this criteria, set the IP address to "192.168.0.1".

        The first 3 sections ("192.168.0" in this example) form a subnet. You will need this later!
        """
        self.ip_address = ip_address if self.__validate_ipv4(ip_address) else "192.168.0.1"
        self.ip_list = self.ip_address.split(".")
        self.ip_address = self.ip_address if self.ip_list[-1] == "1" else "192.168.0.1"

        self.devices = []

    def get_ip_address(self) -> str:
        """Return the current IP address of the router."""
        return self.ip_address

    def generate_ip_address(self, ip_last_part=2) -> str:
        """
        Generate a valid IP address.

        The IP address must be in the router's subnet.
        This means that the first 3 sections of the IP address must be the same as in the router's IP.

        The final section can be a random number in the range [2, 254].

        Make sure you can't generate an IP address that's already in use by a device!

        If there are no possible IP addresses to generate, raise an IPv4AddressSpaceExhaustedException().

        :raises IPv4AddressSpaceExhaustedException: If no IPs are left to generate.
        """
        ip_basis = ".".join(self.ip_list[:3])
        # create new ip
        new_ip = ip_basis + "." + str(ip_last_part)

        if ip_last_part >= 255:
            raise IPv4AddressSpaceExhaustedException()

        # check if the ip in the devices
        if new_ip in map(lambda device: device.get_ip_address(), self.devices):
            return self.generate_ip_address(ip_last_part + 1)
        else:
            return new_ip

    def add_device(self, device: EndDevice) -> bool:
        """
        Add end device to router.

        The same device can not be added twice.
        Each device should be assigned an unique IP address in the correct subnet.

        The method should return True if device was added, else False.
        """
        if device in self.devices:
            return False
        else:
            device.set_ip_address(self.generate_ip_address())
            self.devices.append(device)
            return True

    def remove_device(self, device: EndDevice) -> bool:
        """
        Remove an end device from the router.

        If a device is removed from the router, then the router can no longer send
        packets to the device and the device's IP address is set to an empty string.

        The method should return True if device was removed, else False.
        """
        for index, dev_from_list in enumerate(self.devices):
            if dev_from_list == device:
                dev_from_list.set_ip_address("")
                del self.devices[index]
                return True
        else:
            return False

    def get_devices(self) -> list[EndDevice]:
        """Get all devices that are connected to the router in the order they were connected."""
        return self.devices

    def get_device_by_ip(self, ip: str) -> EndDevice | None:
        """
        Get a device by given IP.

        If there is no device with given IP, then return None.
        Otherwise return the found device.
        """
        device_ip_list = map(lambda device: device.get_ip_address(), self.devices)  # can use filter but I already did this....
        for index, ip_from_list in enumerate(device_ip_list):
            if ip_from_list == ip:
                return self.devices[index]
        else:
            return None

    def receive_packet(self, packet: Packet) -> None:
        """
        Receive a packet from the Internet.

        If there is a device with the destination IP in this subnet then forward this packet to this device.
        Otherwise drop this packet. (don't do anything with it)
        """
        device = self.get_device_by_ip(packet.destination_ip)
        if device is not None:
            device.add_packet(packet)


class IPv4AddressSpaceExhaustedException(Exception):
    """Raised when there are no more available IP addresses."""


if __name__ == "__main__":
    """Main for testing the functions."""
    # Initialize router
    router = Router("192.168.1.1")
    print(router.get_ip_address())  # 192.168.1.1
    print(router.get_devices())     # []
    print()

    # Initialize end devices
    device1 = EndDevice()
    device2 = EndDevice()
    print(f"{device1.get_ip_address()!a}")     # ''
    print()

    # Add devices to router
    print(router.add_device(device1))   # True
    print(router.add_device(device1))   # False (no duplicates allowed)
    print(router.add_device(device2))   # True
    print(len(router.get_devices()))    # 2
    print()

    # Check generated IP addresses
    print(device1.get_ip_address().startswith("192.168.1."))                # True (correct subnet)
    print(1 < int(device1.get_ip_address().split(".")[-1]) < 255)           # True (correct ending)
    print(device1.get_ip_address() == device2.get_ip_address())             # False (different IP addresses generated)
    print(router.get_device_by_ip(device1.get_ip_address()) == device1)     # True
    print()

    # Create packet from device1 to device2
    packet1 = Packet("message1", device1.get_ip_address(), device2.get_ip_address(), 1, 1)
    print(packet1)                          # message1 from 192.168.1.[some number] to 192.168.1.[some number](1:1)
    router.receive_packet(packet1)          # (this should send packet to device2)
    print(len(device2.get_all_packets()))   # 1
    print(len(device1.get_all_packets()))   # 0
    print(len(device2.get_all_packets_by_id(1)))    # 1
    print(len(device2.get_all_packets_by_source_ip(device1.get_ip_address())))  # 1
    print()

    # Create packet from device1 to unknown destination
    packet2 = Packet("message2", device1.get_ip_address(), "10.0.255.44", 2, 1)
    router.receive_packet(packet2)          # (this should drop the packet)
    print(len(device1.get_all_packets()))   # 0
    print(len(device2.get_all_packets()))   # 1
    print()

    # Remove end device from router
    print(router.remove_device(device1))    # True
    print(router.remove_device(device1))    # False (already removed)
    print(f"{device1.get_ip_address()!a}")  # ''
    print(len(router.get_devices()))        # 1
