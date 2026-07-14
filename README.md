# Traveling Tournament Problem (TTP)

![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)

## 📖 Overview

The **Traveling Tournament Problem (TTP)** is a combinatorial optimization problem that combines aspects of:
- **Sports scheduling** – creating a valid round-robin tournament timetable
- **Traveling salesman problem** – minimizing the total travel distance for all teams

The goal is to schedule a double round-robin tournament (each team plays every other team twice – once at home and once away) while minimizing the total distance traveled by all teams, subject to constraints such as no more than a fixed number of consecutive home or away games.

## 🚀 Getting Started

### Prerequisites

- Python 3.12+
- Required dependencies (install via pip):

```bash
pip install -r requirements.txt
```

### Installation

Clone the repository:

```bash
git clone https://github.com/LukasHassel/TravelingTournamentProblem.git
cd TravelingTournamentProblem
```

### (Re)running

```bash
python main.py
```

### Figures
*this uses the output created by `main.py`*
```bash
python figures.py
```


## 📄 License

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.

---

*Feel free to open an issue if you encounter any bugs or have suggestions for improvement!*
