import streamlit as st
import random
import numpy as np
import matplotlib.pyplot as plt
from deap import base, creator, tools, algorithms
import time

# --- 1. CONFIGURATION & MAZE SETUP ---
st.set_page_config(page_title="Genetic Algorithm Maze Solver", layout="wide")

# 0 = Path, 1 = Wall
MAZE_LAYOUT = [
    [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0],
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0],
    [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
    [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0]
]

START_PT, END_PT = (0, 0), (len(MAZE_LAYOUT[0])-1, len(MAZE_LAYOUT)-1)

# --- 2. DEAP SETUP (Protected against reload errors) ---
if not hasattr(creator, "FitnessMin"):
    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
if not hasattr(creator, "Individual"):
    creator.create("Individual", list, fitness=creator.FitnessMin)

def get_toolbox(mut_prob):
    toolbox = base.Toolbox()
    toolbox.register("attr_direction", random.choice, ['U', 'D', 'L', 'R'])
    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_direction, n=100)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    
    toolbox.register("evaluate", evaluate_fitness)
    toolbox.register("select", tools.selTournament, tournsize=3)
    toolbox.register("mate", tools.cxTwoPoint)
    
    # We pass the user-defined mutation probability here
    toolbox.register("mutate", custom_mutate, indpb=mut_prob)
    return toolbox

def evaluate_fitness(individual):
    x, y = START_PT
    steps = 0
    for move in individual:
        nx, ny = x, y
        if move == 'U': ny -= 1
        elif move == 'D': ny += 1
        elif move == 'L': nx -= 1
        elif move == 'R': nx += 1

        # Boundary & Wall Check
        if not (0 <= ny < len(MAZE_LAYOUT) and 0 <= nx < len(MAZE_LAYOUT[0])): break
        if MAZE_LAYOUT[ny][nx] == 1: break
        
        x, y = nx, ny
        steps += 1
        if (x, y) == END_PT: return (0,)

    # Fitness = Manhattan Distance (primary) + small step penalty (secondary)
    # This helps distinguish between two paths that end at the same distance
    dist = abs(END_PT[0] - x) + abs(END_PT[1] - y)
    return (dist,)

def custom_mutate(individual, indpb):
    directions = ['U', 'D', 'L', 'R']
    for i in range(len(individual)):
        if random.random() < indpb:
            possible = [d for d in directions if d != individual[i]]
            individual[i] = random.choice(possible)
    return individual,

# --- 3. STREAMLIT UI ---
st.title("🧬 AI Maze Solver (Genetic Algorithm)")
st.markdown("Watch an evolutionary algorithm learn to solve a maze in real-time.")

# Sidebar Controls
st.sidebar.header("Parameters")
pop_size = st.sidebar.slider("Population Size", 50, 500, 200, step=50)
generations = st.sidebar.slider("Generations", 10, 200, 100, step=10)
cx_prob = st.sidebar.slider("Crossover Probability", 0.1, 1.0, 0.7)
mut_prob = st.sidebar.slider("Mutation Probability (per step)", 0.01, 0.2, 0.05)
anim_speed = st.sidebar.slider("Animation Delay (sec)", 0.0, 0.5, 0.05)

start_btn = st.sidebar.button("🚀 Start Evolution", type="primary")

# Layout Containers
col1, col2 = st.columns([2, 1])

with col1:
    maze_placeholder = st.empty()

with col2:
    stats_placeholder = st.empty()
    code_debug = st.expander("View Best Path DNA")

# --- 4. MAIN ALGORITHM LOOP ---
if start_btn:
    toolbox = get_toolbox(mut_prob)
    pop = toolbox.population(n=pop_size)
    
    # Initial Evaluation
    fits = list(map(toolbox.evaluate, pop))
    for fit, ind in zip(fits, pop):
        ind.fitness.values = fit

    # Prepare Figure once to save memory
    fig, ax = plt.subplots(figsize=(6, 6))

    for gen in range(generations):
        # 1. Evolution Step
        offspring = algorithms.varAnd(pop, toolbox, cxpb=cx_prob, mutpb=0.3) # 0.3 chance to mutate *individual*
        fits = list(map(toolbox.evaluate, offspring))
        for fit, ind in zip(fits, offspring):
            ind.fitness.values = fit
        pop = toolbox.select(offspring, k=len(pop))
        
        # 2. Get Statistics
        top_ind = tools.selBest(pop, k=1)[0]
        best_score = top_ind.fitness.values[0]
        
        # 3. Visualization (Update every few gens or if solved)
        if gen % 2 == 0 or best_score == 0:
            ax.clear()
            ax.imshow(MAZE_LAYOUT, cmap="binary")
            
            # Trace path
            px, py = [START_PT[0]], [START_PT[1]]
            curr_x, curr_y = START_PT
            for move in top_ind:
                nx, ny = curr_x, curr_y
                if move == 'U': ny -= 1
                elif move == 'D': ny += 1
                elif move == 'L': nx -= 1
                elif move == 'R': nx += 1
                
                if not (0 <= ny < len(MAZE_LAYOUT) and 0 <= nx < len(MAZE_LAYOUT[0])): break
                if MAZE_LAYOUT[ny][nx] == 1: break
                
                curr_x, curr_y = nx, ny
                px.append(curr_x)
                py.append(curr_y)
                if (curr_x, curr_y) == END_PT: break

            ax.plot(px, py, color="#4CAF50", linewidth=3, marker="o", markersize=4, label="Best Path")
            ax.plot(START_PT[0], START_PT[1], "go", markersize=10)
            ax.plot(END_PT[0], END_PT[1], "ro", markersize=10)
            ax.legend(loc='upper right')
            ax.set_title(f"Generation {gen} | Distance: {int(best_score)}")
            ax.axis('off')
            
            maze_placeholder.pyplot(fig)
            
            stats_placeholder.markdown(f"""
            ### Status
            - **Generation:** {gen} / {generations}
            - **Best Distance:** {int(best_score)}
            - **Current Location:** {curr_x}, {curr_y}
            """)
            
            # Update DNA view
            code_debug.code("".join(top_ind[:len(px)+5]) + "...", language="text")
            
            time.sleep(anim_speed)

        if best_score == 0:
            st.success(f"🎉 Solved in {gen} generations!")
            break
            
    plt.close(fig)