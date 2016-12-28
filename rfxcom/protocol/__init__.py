"""
Protocol Constants
==================

"""

from .base import Packet
from .elec import Elec
from .humidity import Humidity
from .lighting1 import Lighting1
from .lighting2 import Lighting2
from .lighting3 import Lighting3
from .lighting4 import Lighting4
from .lighting5 import Lighting5
from .lighting6 import Lighting6
from .rain import Rain
from .status import Status
from .temperature import Temperature
from .temphumidity import TempHumidity
from .temphumiditybaro import TempHumidityBaro
from .ultraviolet import UltraViolet
from .wind import Wind

#: Write all zeros to reset the RFXtrx
RESET_PACKET = b'\x0D\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

#: Packet to request the status from the RFXtrx, this will let us know what
#: modes are enabled and that the device is ready.
STATUS_PACKET = b'\x0D\x00\x00\x01\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00'

#: Packet to set the mode for the RFXtrx. The key parts are \x00\x0E\x2F
#: These correlate to a set of 8 bits each which in turn disable or enable
#: an individual protocol. The SDK documentation should be referred to for
#: these or the RFXmngr application can be used to configure the device.
MODE_PACKET = b'\x0D\x00\x00\x01\x03\x53\x00\x00\x0E\x2F\x00\x00\x00\x00'

#: A list containing all the packet types supported in python-rfxcom. The
#: last one is a raw packet and will be used for any unrecognised devices.
HANDLERS = [
    Elec,
    Humidity,
    Lighting1,
    Lighting2,
    Lighting3,
    Lighting4,
    Lighting5,
    Lighting6,
    Rain,
    Status,
    Temperature,
    TempHumidity,
    TempHumidityBaro,
    UltraViolet,
    Wind,
    Packet,  # At the end as we should try it last.
]
