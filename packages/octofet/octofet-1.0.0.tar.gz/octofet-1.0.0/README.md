# OctofetPi

Raspberry Pi library to interface with the Amperka Octofet 8-channel power switches.

# Installation

If you haven’t enabled SPI support in your Raspbian Linux yet, open the terminal and run the
following commands:

1. Run `sudo raspi-config`.
2. Use the down arrow to select `5 Interfacing Options`.
3. Arrow down to `P4 SPI`.
4. Select `<Yes>` when it asks you to enable SPI.
5. Press `<Ok>` when it tells you that SPI is enabled.
6. Use the right arrow to select the `<Finish>` button.
7. Reboot your Raspberry Pi to make the SPI interface appear.

After reboot, log in and enter the following command:

```shell
$ ls /dev/spi*
```

The Pi should respond with:

```shell
/dev/spidev0.0  /dev/spidev0.1
```

These represent SPI devices on chip enable pins 0 and 1, respectively. These pins are hardwired
within the Pi.

Then use `pip` to install the library:

```shell
pip3 install octofet
```

## API

Quickstart example:

```python
import time
import octofet

# Create an Octofet object connected to the CE0 pin of the Raspberry Pi board.
octo = octofet.Octofet(0)
# Switch state variable.
state = True

while True:
    # For each switch.
    for switch in range(8):
        # Set the current state for the switch.
        octo.digital_write(switch, state)
        # Wait 1 second.
        time.sleep(1)
    # Toogle state.
    state = not state
```

See full [API reference in API.md](https://github.com/amperka/OctofetPi/blob/master/API.md).
