# cubed4th


FORTH^3, relicensed with permission from https://github.com/p-unity


# -- THE FORTH-79 STANDARD --

The text here was done by OCR and contains may reading errors.  Please feel free to submit corrections.

# 4. DEFINITICNS OF TERMS 

These definitions, when in lower case, are terms used within this Standard.

They present tenns as specifically used within FORI'H.

# `A`

## address, byte
An unsigned number that locates an 8-bit byte in a standard FOR'll! ,; address space over { 0 •• 65, 535 } • It may be a native machine address or a representation on a virtual machine; locating the 'addr-th' yte within the virtual byte address space. Address arithmetic is modul.o 65, 536 without overflow.

## address, compilation
The numerical value equivalent to a FORTH word definition, which is compi.Led for that definition. The  ddress interpreter uses this value to locate the machine cede corresponding to each definition. (May al. o be called the code field address. ) 

## address, native �chine
The natural address representation of the host computer.

## address, parameter field
The address of the first byte of mencry associated with a word definition for the storage of compilation addresses (in a colon-definition), numeric data and text characters. arithmetic All integer arithmetic is performed with signed 16 or 32 bit two's complement results, unless noted.

# `B`

# block
The unit of data from mass storage, referenced by block number. A block
must contain 1024 bytes regardless of the minimum data unit read/written
from mass storage. The translation from block number to device and
physical reC'Ord is a function of the implementation.

# block buffer
A menory area where a mass storage block is maintained.

# byte
An assembly of 8 bi ts. In reference to mencry, it is the storage capa.ci ty
for 8 bits.