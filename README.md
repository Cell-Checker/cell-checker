<a name="readme-top"></a>
# Cell Checker
![Alt text](./cell-checker.png?raw=true "Title")

An open-source data validation framework designed to ensure the integrity and accuracy of your datasets. Built using Python, Cell Checker empowers data professionals and developers to efficiently validate data across various sources, ensuring compliance with predefined rules and standards.

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

## About The Project

Cell Checker was developed as a collaborative effort to achieve two primary goals for the QA Team at EcoATM:

* Facilitate the QA Team's transition from a manual testing organization to an automation-focused organization.
* Enable the shift from manual data quality testing to automated data quality testing.

By working together, we aim to create a robust framework that not only enhances our internal processes but also serves as a valuable tool for the broader community. Your contributions and feedback are essential to the continued success and evolution of Cell Checker.

### Built With

* Python
* Typer
* Pandas


## Getting Started



### Prerequisites

+ python 3.9.6+
+ pip 24.0
+ pyenv

### Installation

1. Clone project
2. Install modules (pip install -r requirements.txt)
3. Verify installation `python main.py --help`

## Usage

1. Create a test file called test.yaml
   2. ```yaml 
      test:
        name: "Simple Test"
      source:
        type: "csv"
        location: "./data.csv"
      target:
        type: "csv"
        location: "./data.csv"
        comparison_rules:
          row_count: "equal"
          exact_match: "exact" 
      ```
2. Execute the test, ```python main.py --config test.yaml```
3. Review the results (Coming Soon)

## Roadmap

- [ ] Add logging
- [ ] Add unit tests for modules in libs folder
- [ ] Add HTML Reporting
- [ ] Add Allure reporting capabilities
- [ ] Add "components" document to easily copy & paste sections of the readme
- [ ] Create additional Connectors
    - [ ] Excel
    - [ ] Oracle
    - [ ] MySql
    - [ ] SQLSERVER
    - [ ] Snowflake
    - [ ] API/JSON 

See the [open issues](https://github.com/Cell-Checker/cell-checker/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Melvin Laguren - [@mlaguren](https://twitter.com/mlaguren) - melvin@laguren.net

Project Link: [https://github.com/Cell-Checker/cell-checker](https://github.com/Cell-Checker/cell-checker)

<p align="right">(<a href="#readme-top">back to top</a>)</p>