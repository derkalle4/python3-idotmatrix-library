<br/>
<p align="center">
  <a href="https://github.com/derkalle4/python3-idotmatrix-library">
    <img src="images/logo.png" alt="Logo" width="250" height="250">
  </a>

  <h3 align="center">Pixel Display Library</h3>

  <p align="center">
    control all your 16x16 or 32x32 iDotMatrix Pixel Displays
    <br/>
    <br/>
    <a href="https://github.com/derkalle4/python3-idotmatrix-library"><strong>Explore the docs »</strong></a>
    <br/>
    <br/>
    <a href="https://github.com/derkalle4/python3-idotmatrix-library/issues">Report Bug</a>
    .
    <a href="https://github.com/derkalle4/python3-idotmatrix-library/issues">Request Feature</a>
  </p>
</p>

![Downloads](https://img.shields.io/github/downloads/derkalle4/python3-idotmatrix-library/total) ![Contributors](https://img.shields.io/github/contributors/derkalle4/python3-idotmatrix-library?color=dark-green) ![Forks](https://img.shields.io/github/forks/derkalle4/python3-idotmatrix-library?style=social) ![Stargazers](https://img.shields.io/github/stars/derkalle4/python3-idotmatrix-library?style=social) ![Issues](https://img.shields.io/github/issues/derkalle4/python3-idotmatrix-library) ![License](https://img.shields.io/github/license/derkalle4/python3-idotmatrix-library) 

## Table Of Contents

* [About the Project](#about-the-project)
* [Built With](#built-with)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [Usage](#usage)
* [Roadmap](#roadmap)
* [Contributing](#contributing)
* [License](#license)
* [Authors](#authors)
* [Acknowledgements](#acknowledgements)

## About The Project

This repository aims to reverse engineer the [iDotMatrix](https://play.google.com/store/apps/details?id=com.tech.idotmatrix&pli=1) Android App for pixel screen displays like [this one on Aliexpress](https://de.aliexpress.com/item/1005006105517779.html). The goal is to provide a simple library which you can use to connect to your display(s).

## Built With

* [Python 3](https://www.python.org/downloads/)
* [asyncio](https://docs.python.org/3/library/asyncio.html)
* [bleak](https://github.com/hbldh/bleak)
* [pillow](https://python-pillow.org)

## Getting Started

To get a local copy up and running or use the latest pypi package follow these simple example steps:

### Prerequisites

Please install the following for your distribution (Windows may work but it is untested):

* latest Python3
* Python3 Virtual Env

### Installation

#### use latest github source code

1. Clone the repo

```sh
git clone https://github.com/derkalle4/python3-idotmatrix-library.git
```

2. Install the latest version locally

```sh
cd python3-idotmatrix-library/
pip install .
```

#### install latest public version via pypi

```sh
pip install idotmatrix
```

## Usage

If you want to use the integrated bleak library to talk to your device, you have to initialize the ConnectionManager first. If you omit this step all classes will return the bytecode which you then can send to the device with your own bluetooth implementation.

```python
import asyncio
from idotmatrix import ConnectionManager

async def main():
    # connect to first found iDotMatrix Pixel Display
    conn = ConnectionManager()
    await conn.connectBySearch()
    # do something with this connection afterwards

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        quit()
```

### Chronograph

The Chronograph has 4 different modes. Using mode 1 will automatically open the Chronograph on the device and start the countdown. This should be the first mode used or otherwise the device may does not respond properly.

- 0 = reset
- 1 = (re)start
- 2 = pause
- 3 = continue after pause

```python
from idotmatrix import Chronograph

chronograph = Chronograph()
await chronograph.setMode(1)
```

## Roadmap

If you want to contribute please focus on the reverse-engineering part because my personal skills are not that good. Many thanks for all contributions! If you want to dive deep into other issues please check for "#TODO" comments in the source code as well.

* [ ] Reverse Engineering
    * [X] Chronograph
    * [X] Clock
    * [X] Countdown
    * [x] Graffiti Board
    * [X] DIY-Mode
    * [X] Animated Images
    * [X] Display Text
    * [ ] Alarm & Buzzer (available according to issue #18)
    * [ ] Cloud-API to download images
    * [ ] Cloud-API to upload images to device
    * [ ] Cloud-Firmware Update possible?
    * [X] Eco-Mode
    * [X] Fullscreen Color
    * [ ] MusicSync
    * [X] Scoreboard
    * [ ] bluetooth password protection
    * [ ] understand the returned byte arrays of the device for better error logs

## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.
* If you have suggestions for adding or removing projects, feel free to [open an issue](https://github.com/derkalle4/python3-idotmatrix-library/issues/new) to discuss it, or directly create a pull request after you edit the *README.md* file with necessary changes.
* Please make sure you check your spelling and grammar.
* Create individual PR for each suggestion.
* Please also read through the [Code Of Conduct](https://github.com/derkalle4/python3-idotmatrix-library/blob/main/CODE_OF_CONDUCT.md) before posting your first idea as well.

### Creating A Pull Request

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the GNU GENERAL PUBLIC License. See [LICENSE](https://github.com/derkalle4/python3-idotmatrix-library/blob/main/LICENSE) for more information.

## Authors

* [Kalle Minkner](https://github.com/derkalle4) - *Project Founder*
* [Jon-Mailes Graeffe](https://github.com/jmgraeffe) - *Co-Founder*

## Acknowledgements

* [Othneil Drew](https://github.com/othneildrew/Best-README-Template) - *README Template*
* [LordRippon](https://github.com/LordRippon) - *Reverse Engineering for the Displays*
* [8none1](https://github.com/8none1) - *Reverse Engineering for the Displays*
* [schorsch3000](https://github.com/schorsch3000) - *smaller fixes*
* [tekka007](https://github.com/tekka007) - *code refactoring and reverse engineering*
* [inselberg](https://github.com/inselberg) - *Reverse Engineering for the Displays*
