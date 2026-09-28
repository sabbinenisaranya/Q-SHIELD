import hashlib
import platform


def get_device_id():
    """
    Generate a stable identifier for the current computer.

    The identifier is derived from non-secret machine
    information and is used only as a prototype device ID.
    """

    machine_info = "|".join([
        platform.system(),
        platform.release(),
        platform.machine(),
        platform.node()
    ])

    device_hash = hashlib.sha256(
        machine_info.encode("utf-8")
    ).hexdigest()

    return "DEVICE-" + device_hash[:12].upper()