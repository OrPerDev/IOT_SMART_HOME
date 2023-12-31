# Follow Upets - Collar

This project is part of a C.S department course assignment.

The assignment is to think of a product that will help people in their daily lives, and to develop a prototype of the product.

The product we chose to develop is a collar for pets that will help the owner to track the pet's location and communicate with it.

## Description:
Pets have evolved into cherished family members, providing joy and unconditional love.

The fear of losing them is a distressing reality for many pet owners. But with the revolutionary Follow Upets Collar, utilizing advanced GPS technology, you can track your pet's real-time location, ensuring they never go astray.

Moreover, the collar's audio module enables remote communication with your furry friend through voice commands or pre-recorded messages, granting peace of mind from anywhere in the world.

### Product Visual Review:
[Presentation](./assets/presentation.pptx)

[Video](https://youtu.be/R2VEhrLEWE4)

## Features:

💎 **Real-Time GPS Tracking:** The Follow Upets Collar employs advanced GPS technology to track and display your pet's live location on the mobile app. Stay informed about your pet's whereabouts at all times.

💎 **Last Known Location:** The collar's GPS module stores the last known location of your pet. If your pet goes out of range, you can still track their location and find them.

💎 **Voice Recording Storage:** Store personalized voice recordings on the collar. Record comforting messages or commands to communicate with your pet.

💎 **Voice Message Playback:** Send stored voice recordings to your pet through the collar. Deliver affectionate messages, cues, or reassurance from afar.

💎 **Easy To Use:** The collar is designed to be user-friendly and intuitive. The app is simple to navigate and provides a seamless experience.


## Demo:
<img src="./assets/demo.gif" alt="demo"/>


## Block Diagram:
<img src="./assets/block-diagram.jpg" alt="block_diagram"/>

## Use Cases Diagram:
<img src="./assets/use-cases-diagram.jpeg" alt="use_case_diagram"/>

## Hardware:
⚙️ [**Raspberry Pi Pico**](https://thepihut.com/products/raspberry-pi-pico): The main microcontroller and foundation for the IoT project.

⚙️ [**Male Header Set for Raspberry Pi Pico** x2](https://thepihut.com/products/male-headers-for-raspberry-pi-pico): Those male header pins are used to connect the Pico to the Waveshare board and to the notecarrier.

📡 [**Blues Notecard (Cellular)**](https://blues.io/products/notecard/): The Notecard is a small, low-power cellular IoT card that adds wireless connectivity to the Raspberry Pi Pico.
  - The Notecard has a SIM embedded in it and is used to send and receive data from the cloud.
  - This Notecard is also Geo-aware, meaning it can be used to get the device's location.
  - This Notecard uses LTE-M, NB-IoT, or Cat-1 cellular networks, so it can be configured to work in most countries.
> The Notecard is connected to the Pico via the Notecarrier-A.

⚙️ [**Blues Notecarrier-A**](https://blues.io/products/notecarrier/notecarrier-a/): The Notecarrier-A is a Raspberry Pi add-on board that allows you to connect a Notecard to a Raspberry Pi Pico.
> The carrier is connected to the controller as a HAT.

🔊 [**Waveshare Audio Expansion Module**](https://www.waveshare.com/pico-audio.htm): The Pico-Audio-Exp module is an audio expansion module that provides audio functionality to the Raspberry Pi Pico.
> The Audio Module is connected to the Pico via onboard female headers for direct connection to the Pico's Male headers.

🔋 [**14500 Li-ion Battery**](https://www.amazon.com/14500-battery/s?k=14500+battery): A battery is used to power the device.
> The battery is connected to the Pico via a battery holder.

⚙️ [**Battery Holder Power Module**](https://www.kubii.com/en/modulos-reles/3295-power-module-battery-holder-for-raspberry-pi-pico-3272496306134.html): The battery is held in place by a battery holder that is connected to the Waveshare board.


## Required Software:
### Collar:
- [Raspberry Pi OS](https://www.raspberrypi.org/software/operating-systems/)
- [MicroPython](https://micropython.org/download/rp2-pico/)

### Client GUI Application:
- [Python 3.11](https://www.python.org/downloads/)


## License

This library is licensed under the MIT License.

## Contributing

Contributions are welcome! Please open an issue or a pull request if you have any suggestions or if you find a bug.

## Contact

Project owners:
> <a href="https://github.com/chapost1"><kbd><img src="https://avatars.githubusercontent.com/u/39523779?s=25"/></kbd></a> &nbsp; Shahar Tal
>
> [Github](https://github.com/chapost1) | [LinkedIn](https://www.linkedin.com/in/shahar-tal-4aa887166/) 

> <a href="https://github.com/OrPerDev"><kbd><img src="https://avatars.githubusercontent.com/u/91319947?s=25"/></kbd></a> &nbsp; Or Peretz
>
> [Github](https://github.com/OrPerDev) | [LinkedIn](https://www.linkedin.com/in/or-peretz/) 
