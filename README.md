<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/joaoofreitas/mudp/>
    <img src="icon.png" alt="Logo" width="320" height="226">
  </a>

  <h3 align="center">MUDP - Message User Datagram Protocol</h3>

  <p align="center">
    An implementation of a secure, decentralised and privacy-focused messaging network protocol.
    <br />
    <a href="https://github.com/joaoofreitas/mudp/"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/joaoofreitas/mudp/">View</a>
    ·
    <a href="https://github.com/joaoofreitas/mudp/issues">Report Bug</a>
    ·
    <a href="https://github.com/joaoofreitas/mudp/issues">Request Feature</a>
    ·
    <a href="https://github.com/joaoofreitas/mudp/pulls">Send a Pull Request</a>
  </p>
</p>


## Table of Contents

* [About the Project](#about-the-project)
  * [Built With](#built-with)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [Usage](#usage)
* [Contributing](#contributing)
* [License](#license)
* [Contact](#contact)



<!-- ABOUT THE PROJECT -->
## About The Project

__MUDP__ stands for _Messaging User Datagram Protocol_ and it is a UDP based protocol created by [_@joaoofreitas_](https://github.com/joaoofreitas) that sends and receives asynchronous encrypted messages from a peer to another.

This project is a code implementation of this protocol _(I consider the protocol itself just theory)_.

I decided to start this project mostly for learning and going a little bit deeper around networking. This project gave me skills in sockets, encryption, compression and raw packet networking.

Use cases:

- Full control of communication with another person without sniffing or network tracking.

### Built With

- [python](https://www.python.org)
- [rsa](https://pypi.org/project/rsa/)

## Getting Started

Follow the steps bellow for installing test te project in your machine.

### Prerequisites

To install this software you need to have installed:
  - [Git](https://git-scm.com/downloads)
  - [Python3](https://www.python.org)
  - [Python package manager - _pip3_](https://pip.pypa.io/en/stable/installing/)

### Installation

1. Clone the repository
```sh
  git clone https://github.com/joaoofreitas/mudp.git
```
2. Install dependencies
```sh
  pip3 install -r requirements.txt
```

3. Give execution permission

- On Linux/MacOS
```sh
  chmod +x main.py
```

<!-- USAGE EXAMPLES -->
## Usage
For running this program you can use optional argument flags such as _username_, _port_ and _debug_.

- Example
```sh
  ./main.py --username=Anonymous --port=8080
```
- If you are having problems you can add the flag `--debug` to see what may be happening.
  ```sh
    ./main.py --debug
  ```
  Or:
  ```sh
    ./main.py --username=Anonymous --port=8080 --debug
  ```

Anyways if you have any trouble running the program feel free o open a [issue](https://github.com/joaoofreitas/mudp/issues).

<!-- CONTRIBUTING -->
## 🤝 Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **extremely appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



<!-- LICENSE -->
## 📝 License
Describe your License for your project. 

Distributed under the MIT License. See `LICENSE` for more information.

<!-- CONTACT -->
## 📫 Contact

João Freitas - [@joaoofreitas](https://github.com/joaoofreitas) - joaoofreitas@pm.me

Miguel Andrade - [@miguel1996](https://github.com/miguel1996)
