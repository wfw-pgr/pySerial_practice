import serial
import time

# ------------------------------------------------- #
# --- [0] parameters                            --- #
# ------------------------------------------------- #

COM           = "COM3"
COM_lnx       = "/dev/ttys0"
bitRate       = 9600
timeout       = 0.1
Tsleep        = 0.01
dt            = 0.1
duration      = 2.0
maxRange      = "0.3"

range_table   = {"0.3":"R0", "0.6":"R1", "1.2":"R2", "3.0":"R3" }
mode_table    = {"D":"DC mode", "A":"AC mode", "C":"Continuous mode", "V":"triggered mode"}

# ------------------------------------------------- #
# --- [1] preparation                           --- #
# ------------------------------------------------- #
# -- open          -- #
ser     = serial.Serial( COM, bitRate, timeout=timeout )
ser.open()

# ------------------------------------------------- #
# --- [2] settings part                         --- #
# ------------------------------------------------- #

# -- select DC mode -- #
ser.write( b"GD" )

# -- check mode     -- #
ser.write( b"IG" )
time.sleep( Tsleep )
recv  = ser.read(1)
print( "[RS232C-DTM-151] mode == {0}".format( table["recv"] ) )

# -- Range Settings -- #
rangeString = range_table[maxRange]
ser.write( rangeString.encode() )

# ------------------------------------------------- #
# --- [3] Field Measuring                       --- #
# ------------------------------------------------- #

nTime   = int( duration / dt )
times   = np.linspace( 0.0, duration, nTime )
Tsleep_ = dt - Tsleep
fields  = np.zeros( (nTime,2) )

for it in range( nTime ):
    ser.write( b"F" )
    time.sleep( Tsleep )
    recv       = ser.read_line()
    fields[it] = float( recv.decode("utf-8") )
    time.sleep( Tsleep_ )

# ------------------------------------------------- #
# --- [4] post process                          --- #
# ------------------------------------------------- #

ser.close()
