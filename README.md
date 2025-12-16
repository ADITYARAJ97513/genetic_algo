# 🧬 AI Maze Solver with Genetic Algorithms

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Library](https://img.shields.io/badge/Library-DEAP-orange)

An interactive Artificial Intelligence application that evolves a solution to a complex maze using **Genetic Algorithms (GA)**. Built with **Python** and **Streamlit**, this project visualizes how evolutionary concepts (natural selection, mutation, and crossover) can be applied to pathfinding problems.

## 📸 Demo
<img width="1912" height="900" alt="Screenshot 2025-12-16 200126" src="https://github.com/user-attachments/assets/e7d418b2-80e7-4481-a65c-6025a6c879c4" />


## 🚀 Live Demo
[**Click here to run the app live!**](https://adityaraj97513-genetic-algo-app-fjyauy.streamlit.app/)

## ✨ Features
* **Real-time Visualization:** Watch the "fittest" individual of each generation attempt the maze in real-time.
* **Interactive Controls:** Tweak GA parameters on the fly:
    * **Population Size:** How many "agents" explore at once.
    * **Mutation Rate:** The randomness factor to prevent getting stuck.
    * **Crossover Probability:** How often paths mix to create new solutions.
* **Performance Metrics:** Tracks the best solution's fitness (distance to goal) per generation.

## 🛠️ Tech Stack
* **Language:** Python
* **Algorithm Library:** [DEAP](https://github.com/DEAP/deap) (Distributed Evolutionary Algorithms in Python)
* **Visualization:** Matplotlib & Streamlit
* **Numeric Computation:** NumPy

## 🧠 How it Works
The AI treats the pathfinding problem as an evolutionary process:
1.  **DNA:** Each agent has a "chromosome" consisting of a list of directions (`UP`, `DOWN`, `LEFT`, `RIGHT`).
2.  **Fitness Function:** Agents are scored based on how close they get to the exit (Manhattan Distance). Walls and boundaries result in penalties.
3.  **Selection:** The best agents are selected to reproduce.
4.  **Crossover:** Two parent paths swap segments to create offspring (e.g., combining the beginning of one path with the end of another).
5.  **Mutation:** Random changes are introduced to the path to explore new routes and avoid local optima.

## 📦 Installation & Setup

To run this project locally:

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/maze-solver-ai.git](https://github.com/YOUR_USERNAME/maze-solver-ai.git)
    cd maze-solver-ai
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the app:**
    ```bash
    streamlit run app.py
    ```

## 📂 Project Structure
