================================================================
CTF Writeup: "Espresso" (Hardware / Firmware)
================================================================

Challenge
---------
"Someone leaked the new Espresso firmware, can you try to figure
out what it does?"

Provided file: firmware.bin (4 MB)

----------------------------------------------------------------
1. Identification
----------------------------------------------------------------
firmware.bin starts with 0xFF padding, then at offset 0x1000 the
ESP image magic byte 0xE9 appears. This is a raw flash dump of an
Espressif ESP32 ("Espresso" = pun on Espressif).

Layout found:
  0x1000   - 2nd stage bootloader
  0x8000   - partition table (magic 0xAA50)
  0x9000   - nvs        (6 KB,  empty)
  0xf000   - phy_init   (4 KB,  empty)
  0x10000  - factory app (project name: "espresso", ESP-IDF v6.1-dev)

----------------------------------------------------------------
2. Static analysis
----------------------------------------------------------------
Extracted the factory app partition and ran `strings` over it.
No flag string was present, but the following app-specific
strings stood out among the ESP-IDF boilerplate:

  "flag did not generate correctly."
  "It seems you are running the firmware on cloned hadware."
  "Buy the real hardware, or perhaps try to emulate it. ;)"

-> The firmware has an anti-clone/anti-emulation check that
   normally blocks flag generation. The winking message is a
   direct hint: try running it in an emulator.

A proper Xtensa disassembler (objdump/capstone with Xtensa
support) was not available locally, so static reversing of the
exact check was skipped in favor of dynamic execution.

----------------------------------------------------------------
3. Dynamic analysis (QEMU)
----------------------------------------------------------------
Mainline QEMU has no ESP32 machine type. Espressif maintains a
fork with ESP32 support (github.com/espressif/qemu, branch
esp-develop).

Steps:
  1. Downloaded espressif/qemu (esp-develop branch).
  2. Built only the xtensa-softmmu target:
       ./configure --target-list=xtensa-softmmu \
                    --enable-slirp --enable-gcrypt
       ninja qemu-system-xtensa
  3. Ran the leaked flash image directly:

       qemu-system-xtensa -nographic -machine esp32 \
         -drive file=firmware.bin,if=mtd,format=raw

Result: the firmware booted, app_main() ran, and the UART log
printed the flag directly (no eFuse/MAC spoofing needed):

       I (1856) main: HTB{3mul4ting_hw_is_s0_c00l!!!}

----------------------------------------------------------------
4. Flag
----------------------------------------------------------------
HTB{3mul4ting_hw_is_s0_c00l!!!}

----------------------------------------------------------------
5. Takeaways
----------------------------------------------------------------
- "Espresso" / leaked firmware.bin = full ESP32 flash dump
  (bootloader + partition table + app), starting at offset 0x1000.
- Strings in the binary directly hinted at the solution path
  ("...try to emulate it ;)").
- No real hardware or eFuse trickery was required - simply
  booting the image in Espressif's QEMU fork was enough to reach
  app_main() and print the flag over UART.
================================================================
