<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->

<!-- Ascii format -->
```sh
            ______    ___      _______  ___   __    _  _______  __    _  _______  _______ 
            |    _ |  |   |    |       ||   | |  |  | ||   _   ||  |  | ||       ||       |
            |   | ||  |   |    |    ___||   | |   |_| ||  |_|  ||   |_| ||       ||    ___|
            |   |_||_ |   |    |   |___ |   | |       ||       ||       ||       ||   |___ 
            |    __  ||   |___ |    ___||   | |  _    ||       ||  _    ||      _||    ___|
            |   |  | ||       ||   |    |   | | | |   ||   _   || | |   ||     |_ |   |___ 
            |___|  |_||_______||___|    |___| |_|  |__||__| |__||_|  |__||_______||_______|                                                                       
```

<!-- PROJECT LOGO -->

<br />

<p align="center">
  
  <a href="https://github.com/github_username/repo_name">
    
   
  </a>

  <p align="center">
     Develop trading algorithm using reinforcement learning
    <a href="https://github.com/minjunp/RLfinance/issues">Report Bug</a>
    ·
    <a href="https://github.com/minjunp/RLfinance/issues">Request Feature</a>
  </p>
</p>


<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.

<!-- USAGE EXAMPLES -->

## Usage

Install conda environment

```sh
conda create -n RLfinance python=3.8
```

Activate conda environment 
```sh
conda activate RLfinance
```

Install dependencies
```sh
pip install pandas sklearn matplotlib seaborn notebook
conda install -c conda-forge ta-lib
pip install yfinance
pip install gym==0.7.4 
pip install stable-baselines3
pip install git+https://github.com/quantopian/pyfolio
```

If using Nvidia GPU:
```sh
conda install pytorch=1.09 torchvision torchaudio cudatoolkit=11.1 -c pytorch -c nvidia
```
## Data

Use yahooFinance package for downloading dataframes


<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/minjunp/RLfinance/issues) for a list of proposed features (and known issues).

<!-- CONTACT -->
## Corresponding Authors

Minjun Park - minjunp3@gmail.com

Project Link: [https://github.com/minjunp/RLfinance](https://github.com/minjunp/RLfinance)


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/minjunp/RLfinance.svg?style=flat-square
[contributors-url]: https://github.com/minjunp/RLfinance/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/minjunp/RLfinance.svg?style=flat-square
[forks-url]: https://github.com/minjunp/RLfinance/network/members
[stars-shield]: https://img.shields.io/github/stars/minjunp/RLfinance.svg?style=flat-square
[stars-url]: https://github.com/minjunp/RLfinance/stargazers
[issues-shield]: https://img.shields.io/github/issues/minjunp/RLfinance.svg?style=flat-square
[issues-url]: https://github.com/minjunp/RLfinance/issues
[license-shield]: https://img.shields.io/github/license/minjunp/RLfinance.svg?style=flat-square
[license-url]: https://github.com/minjunp/RLfinance/blob/master/LICENSE.txt
