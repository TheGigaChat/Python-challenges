"""Serve all the packets."""

from router import Packet, EndDevice, Router
import re


class EndDevicePlus(EndDevice):
    """
    End Device Plus class.

    This class extends the EndDevice class from EX12.
    """

    def __init__(self):
        """Initialize End Device Plus."""
        super().__init__()

    def get_message(self, id: int) -> str:
        """
        Get message from packets by ID.

        Message is a string formed by the contents of all received packets with the specified ID.

        Make sure you pay attention to the correct order of the packets using their sequence number.
        If the device has not received any packets with this ID, return an empty string.
        There must be no extra symbols between the contents of two packets.

        If some packets have been lost (such as there being packets 1 and 3, but not packet 2),
        then add an underscore (_) in place of each missing packet.
        """
        packets_with_id = self.get_all_packets_by_id(id)

        if not packets_with_id:
            return ""

        # Sort by sequence number
        packets_with_id.sort(key=lambda packet: packet.sequence_number)

        # Determine the sequence numbers present and construct the message
        message = []
        expected_sequence = 1

        for packet in packets_with_id:
            # Add underscores for missing sequence numbers
            while expected_sequence < packet.sequence_number:
                message.append("_")
                expected_sequence += 1
            # Add the packet's content
            message.append(packet.content)
            expected_sequence += 1

        return "".join(message)


class RouterPlus(Router):
    """
    Router Plus class.

    This class extends the Router class.
    """

    def __init__(self, ip_address: str):
        """Initialize Router Plus."""
        super().__init__(ip_address)

    def receive_packet(self, packet: Packet) -> None:
        """
        Receive a packet from the Internet with additional functionality.

        If packet's destination IP ends with .255, it is broadcasted to every known device on the router.
        In other cases, the packet is handled as in the base Router class (using super()).

        Only packets in the same subnet as the router are processed.
        """
        # Check if the packet's destination is in the router's subnet
        packet_subnet = ".".join(packet.destination_ip.split(".")[:3])  # 188.198.199
        router_subnet = ".".join(self.ip_list[:3])

        if packet_subnet != router_subnet:
            return None

        # If the destination IP === .255, broadcast the packet
        destination_ip_final_part = ".".join(packet.destination_ip.split(".")[3:])
        if destination_ip_final_part == "255":
            for device in self.devices:
                device.add_packet(packet)
        else:
            # Handle the packet as in the base Router class
            super().receive_packet(packet)

    def restart_router(self) -> None:
        """
        Restart the router.

        Upon restarting the router, all devices get new IP addresses.
        The new IP addresses must be unique and cannot be the same as the devices' previous IP addresses.
        The order of devices must not change.
        """
        devices_copy = []
        old_ips = []  # Store old IP to check
        new_ips = set()

        # Reassign new IP
        for device in self.devices:
            old_ip = device.get_ip_address()
            old_ips.append(old_ip)

            ip_last_part = 2
            while True:
                try:
                    new_ip = self.generate_ip_address(ip_last_part)
                    if new_ip not in old_ips and new_ip not in new_ips:
                        break
                    ip_last_part += 1  # Increment if collision detected
                except IPv4AddressSpaceExhaustedException:
                    raise RuntimeError("Unable to generate enough unique IP addresses.")

            device.set_ip_address(new_ip)
            devices_copy.append(device)

        self.devices = devices_copy


def validate_ipv4(ip_address: str) -> bool:
    """Validate IPv4."""
    pattern_ip = r"((\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5]))"
    match = re.fullmatch(pattern_ip, ip_address)
    return match is not None


class Server:
    """Server class."""

    def __init__(self):
        """Initialize server."""
        self.ip_address = ""
        self.routers = {}

    def split_message(self, message: str) -> list[str]:
        """
        Split message into smaller pieces.

        Because the maximum content length for a packet is 5 symbols,
        then we have to split up bigger messages in order to send them over the network.

        The messages have to be split into maximum length pieces and put into a list in the correct order.
        The list of message pieces has to be returned.

        If the message is exactly 5 symbols or less then just return the message in a list.
        Example:
            "Hello World" -> ["Hello", " Worl", "d"]
        """
        result_list = []
        for i in range(0, len(message), 5):
            split_message = message[i:i + 5]
            result_list.append(split_message)

        return result_list

    def set_ip_address(self, ip_address: str) -> None:
        """
        Set an IP address for the Server.

        Make sure to validate the IP address here.
        A Server's IP cannot end with 0 (network identifier), 1 (router) or 255 (broadcast).
        If given IP is not a valid IP, do not modify the current IP address.
        """
        if validate_ipv4(ip_address):
            last_ip_numbers = int(ip_address.split(".")[-1])
            if last_ip_numbers not in {0, 1, 255}:
                self.ip_address = ip_address
        else:
            return None

    def get_ip_address(self) -> str:
        """Return the current IP address of the server."""
        return self.ip_address

    def add_router(self, router: Router) -> bool:
        """
        Add router to the server.

        Same router can not be added to the server multiple times.

        The method should return True if a router was added to the server, else False.
        """
        ip_address = router.get_ip_address()
        if ip_address not in self.routers:
            self.routers[ip_address] = router
            return True
        return False

    def remove_router(self, router: Router) -> bool:
        """
        Remove a router from the server.

        If a router is removed from the router, then the server can no longer send
        packets to the router.

        The method should return True if a router was removed from the server, else False.
        """
        ip_address = router.get_ip_address()
        if ip_address in self.routers:
            del self.routers[ip_address]
            return True
        return False

    def get_routers(self) -> list[Router]:
        """Get all routers that are connected to the server in the order they were connected."""
        return list(self.routers.values())

    def send_packet_to_ip(self, packet: Packet) -> None:
        """
        Send a Packet to a device with the Packet's destination IP address.

        You'll first need to check your connected routers to see if any of them have
        the same subnet as the target IP address.

        If there are no suitable routers or the IP address is invalid, drop the packet (do not send it).
        Also, packet should be dropped if packet's content size is over the limit (5 symbols).

        If you find a router with the same subnet as the target IP, you can use that router's
        receive_packet() method to handle the rest of the delivery.
        """
        if len(packet.content) > 5:
            return None

        target_ip = ".".join(packet.destination_ip.split(".")[:3])
        for router in self.routers.values():
            router_ip_full = router.get_ip_address()
            router_ip = ".".join(router_ip_full.split(".")[:3])
            if router_ip == target_ip:
                router.receive_packet(packet)

    def send_message_to_ip(self, message: str, ip_address: str, id: int) -> None:
        """
        Send message to given IP addess.

        You have to create new Packets to be sent yourself.
        Remember that a Packet's content can not be longer than 5 symbols.

        Given ID is used to differentiate messages.
        This ID has to be used in the packets.

        You should use send_packet_to_ip() method here.
        """
        parts = self.split_message(message)
        for sequence_number, part in enumerate(parts, start=1):  # sequence_number starts with 1
            new_packet = Packet(part, self.ip_address, ip_address, id, sequence_number)
            self.send_packet_to_ip(new_packet)

    def send_message_to_all(self, message: str, id: int) -> None:
        """
        Send message to every known router and to every end device on these routers.

        You should use send_message_to_ip() method here.
        Sending to every end device should be handled by the router.
        """
        for router in self.get_routers():
            for device in router.get_devices():
                self.send_message_to_ip(message, device.get_ip_address(), id)


class IPv4AddressSpaceExhaustedException(Exception):
    """Raised when there are no more available IP addresses."""


if __name__ == "__main__":
    """Main for testing the functions."""
    # Initialize RouterPlus
    router = RouterPlus("192.168.1.1")
    print(router.get_ip_address())  # 192.168.1.1
    print(router.get_devices())     # []
    print()

    # Initialize end devices
    device1 = EndDevicePlus()
    device2 = EndDevicePlus()
    print(f"{device1.get_ip_address()!a}")     # ''
    print()

    # Add devices to router
    print(router.add_device(device1))   # True
    print(router.add_device(device1))   # False (no duplicates allowed)
    print(router.add_device(device2))   # True
    print(len(router.get_devices()))    # 2
    print()

    # # Check generated IP addresses
    print(device1.get_ip_address().startswith("192.168.1."))                # True (correct subnet)
    print(1 < int(device1.get_ip_address().split(".")[-1]) < 255)           # True (correct ending)
    print(device1.get_ip_address() == device2.get_ip_address())             # False (different IP addresses generated)
    print(router.get_device_by_ip(device1.get_ip_address()) == device1)     # True
    print()

    # Get message
    router.receive_packet(Packet("Te", "192.168.1.1", device1.get_ip_address(), 2, 1))
    router.receive_packet(Packet("re!", "192.168.1.1", device1.get_ip_address(), 2, 3))
    print(device1.get_message(2))           # Te_re!
    print(len(device1.get_all_packets()))   # 2
    print(len(device2.get_all_packets()))   # 0
    print()

    # Packet with a destination IP that ends with .255 is sent to all connected devices
    packet_broadcast = Packet("test", "192.168.1.1", "192.168.1.255", 1, 1)
    router.receive_packet(packet_broadcast)
    print(len(device1.get_all_packets()))   # 3
    print(len(device2.get_all_packets()))   # 1
    print()

    # Restarting router gives every device a new IP
    old_ip_device1 = device1.get_ip_address()
    old_ip_device2 = device2.get_ip_address()
    router.restart_router()
    print(device1.get_ip_address() == old_ip_device1)   # False
    print(device2.get_ip_address() == old_ip_device2)   # False
    print()

    # Initialize Server
    server = Server()
    print(f"{server.get_ip_address()!a}")       # ''
    server.set_ip_address("1.2.3.4")
    print(f"{server.get_ip_address()!a}")       # '1.2.3.4'
    print(server.add_router(router))            # True
    print(len(server.get_routers()))            # 1
    print()

    # Server send packet
    packet_server = Packet("test", "1.2.3.4", device2.get_ip_address(), 3, 1)
    server.send_packet_to_ip(packet_server)
    print(len(device1.get_all_packets()))       # 3
    print(len(device2.get_all_packets()))       # 2
    print()

    # Server send message
    server.send_message_to_ip("pretty long message", device2.get_ip_address(), 4)
    print(f"{device2.get_message(4)!a}")        # 'pretty long message'
    print(f"{device1.get_message(4)!a}")        # ''
    print()

    # Server send message to all
    router2 = RouterPlus("10.0.0.1")
    device3 = EndDevicePlus()
    device4 = EndDevicePlus()
    router2.add_device(device3)
    router2.add_device(device4)
    server.add_router(router2)
    server.send_message_to_all("All your files have been encrypted!", 1337)
    print(device1.get_message(1337))    # All your files have been encrypted!
    print(device4.get_message(1337))    # All your files have been encrypted!
    print()
