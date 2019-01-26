# RPI-Weather-App
Application built for showing current wind speed and direction using LEDs and a VU meter using a Raspberry Pi

Requires a data.txt in the same directory to load the required details.

data.txt must be in the form
appid
cityid

Any lines after that will be ignored

## Raspberry Pi Setup ##

With GPIO pins facing upward and on the right:

```
                  1   2
                  3   4
North-West LED  - 5   6   - Ground for LEDs
                  7   8
 Ground for VU  - 9   10  - North LED
    Out for VU  - 11  12  - North-East LED
                  13	14
                  15	16  - East LED
                  17	18  - South-East LED
                  19	20
                  21	22  - South LED
                  23	24  - South-West LED
                  25	26  - West LED
                  27	28
                  29	30
                  31	32
                  33	34
                  35	36
                  37	38
                  39	40
```
