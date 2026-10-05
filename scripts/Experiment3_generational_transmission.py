import random
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


# Basic settings
forms = ['laap', 'siu', 'zung', 'faai']
meanings = ['M1', 'M2']

n_learners = 10
n_generations = 20
input_size = 6
n_runs = 30
learning_rate = 0.1
social_learning_rate = 0.1

base_probs = {
    'M1': {'laap': 0.35, 'siu': 0.30, 'zung': 0.20, 'faai': 0.15},
    'M2': {'laap': 0.20, 'siu': 0.15, 'zung': 0.35, 'faai': 0.30}
}


# Set output folders
project_dir = Path(__file__).resolve().parent.parent
results_dir = project_dir / 'results'
figure_dir = results_dir / 'figures'
table_dir = results_dir / 'tables'

figure_dir.mkdir(parents=True, exist_ok=True)
table_dir.mkdir(parents=True, exist_ok=True)


# Create one learner's input distribution
def create_input_probs():
    probs = {}

    for meaning in meanings:
        probs[meaning] = {}

        for form in forms:
            base = base_probs[meaning][form]
            change = random.uniform(0.3, 1.7)
            probs[meaning][form] = base * change

        total = sum(probs[meaning].values())

        for form in forms:
            probs[meaning][form] /= total

    return probs


# Create input distribution from the previous generation
def create_generation_probs(previous_prefs):
    probs = {}

    for meaning in meanings:
        probs[meaning] = {}

        for form in forms:
            base = previous_prefs[meaning][form]
            change = random.uniform(0.3, 1.7)
            probs[meaning][form] = base * change

        total = sum(probs[meaning].values())

        for form in forms:
            probs[meaning][form] /= total

    return probs


# Agent
class Agent:
    def __init__(self, input_probs):
        self.input_probs = input_probs
        self.weights = {}

        for meaning in meanings:
            self.weights[meaning] = {}

            for form in forms:
                self.weights[meaning][form] = 1.0

    def receive(self, inputs):
        for meaning, form in inputs:
            self.weights[meaning][form] += learning_rate

    def receive_social(self, meaning, form):
        self.weights[meaning][form] += social_learning_rate

    def get_strength(self):
        strength = {}

        for meaning in meanings:
            total = sum(self.weights[meaning].values())
            strongest = max(self.weights[meaning].values())
            strength[meaning] = strongest / total

        return strength

    def get_main_forms(self):
        main_forms = {}

        for meaning in meanings:
            max_weight = max(
                self.weights[meaning].values()
            )

            candidates = [
                form
                for form in forms
                if self.weights[meaning][form] == max_weight
            ]

            main_forms[meaning] = random.choice(candidates)

        return main_forms


# Generate input for one round
def generate_inputs(probs):
    inputs = []

    for meaning in meanings:
        form_list = list(probs[meaning].keys())
        weights = list(probs[meaning].values())

        sampled_forms = random.choices(
            form_list,
            weights=weights,
            k=input_size
        )

        for form in sampled_forms:
            inputs.append((meaning, form))

    random.shuffle(inputs)

    return inputs


# Create learners
def create_learners(input_probs=None):
    learners = []

    for _ in range(n_learners):
        if input_probs is None:
            probs = create_input_probs()
        else:
            probs = create_generation_probs(input_probs)

        learners.append(Agent(probs))

    return learners


# Social interaction between learners
def interact(learners):
    order = list(range(len(learners)))
    random.shuffle(order)

    for i in range(0, len(order), 2):
        agent1 = learners[order[i]]
        agent2 = learners[order[i + 1]]

        forms1 = agent1.get_main_forms()
        forms2 = agent2.get_main_forms()

        for meaning in meanings:
            agent1.receive_social(
                meaning,
                forms2[meaning]
            )

            agent2.receive_social(
                meaning,
                forms1[meaning]
            )


# Calculate aggregate form proportions
def get_aggregate_prefs(learners):
    prefs = {}

    for meaning in meanings:
        totals = {}

        for form in forms:
            totals[form] = sum(
                agent.weights[meaning][form]
                for agent in learners
            )

        total = sum(totals.values())
        prefs[meaning] = {}

        for form in forms:
            prefs[meaning][form] = totals[form] / total

    return prefs


# Compare individual and aggregate preferences
def get_similarity(learners, prefs):
    population_main_forms = {}

    for meaning in meanings:
        max_pref = max(
            prefs[meaning].values()
        )

        candidates = [
            form
            for form in forms
            if prefs[meaning][form] == max_pref
        ]

        population_main_forms[meaning] = random.choice(candidates)

    similarity = {}

    for meaning in meanings:
        matches = 0

        for agent in learners:
            agent_main_forms = agent.get_main_forms()

            if agent_main_forms[meaning] == population_main_forms[meaning]:
                matches += 1

        similarity[meaning] = matches / len(learners)

    return similarity


# Run one generation
def run_generation(learners):
    for _ in range(10):
        for agent in learners:
            inputs = generate_inputs(agent.input_probs)
            agent.receive(inputs)

        interact(learners)

    prefs = get_aggregate_prefs(learners)
    similarity = get_similarity(learners, prefs)

    return prefs, similarity


# Run one simulation
def run_simulation(seed):
    random.seed(seed)

    learners = create_learners()
    records = []

    for generation in range(1, n_generations + 1):

        prefs, similarity = run_generation(learners)

        strengths = {
            meaning: []
            for meaning in meanings
        }

        for agent in learners:
            strength = agent.get_strength()

            for meaning in meanings:
                strengths[meaning].append(
                    strength[meaning]
                )

        for meaning in meanings:
            records.append({
                'generation': generation,
                'meaning': meaning,
                'strength': (
                    sum(strengths[meaning])
                    / n_learners
                ),
                'similarity': similarity[meaning]
            })

        # Create the next generation from the current generation
        learners = create_learners(prefs)

    return records


# Save results
def save_results(all_records):
    records_df = pd.DataFrame(all_records)

    strength_df = (
        records_df
        .groupby(['generation', 'meaning'])['strength']
        .agg(['mean', 'std'])
        .reset_index()
    )

    similarity_df = (
        records_df
        .groupby(['generation', 'meaning'])['similarity']
        .agg(['mean', 'std'])
        .reset_index()
    )

    strength_df.to_csv(
        table_dir / 'generational_preference_strength.csv',
        index=False
    )

    similarity_df.to_csv(
        table_dir / 'generational_similarity.csv',
        index=False
    )

    return strength_df, similarity_df


# Run all simulations
def main():
    all_records = []

    for run in range(n_runs):
        records = run_simulation(seed=run)

        for record in records:
            record['run'] = run + 1
            all_records.append(record)

    strength_df, similarity_df = save_results(
        all_records
    )

    # Plot preference strength across generations
    plt.figure(figsize=(8, 5))

    for meaning in meanings:
        data = strength_df[
            strength_df['meaning'] == meaning
        ]

        plt.plot(
            data['generation'],
            data['mean'],
            label=meaning
        )

    plt.xlabel('Generation')
    plt.ylabel('Preference strength')
    plt.title('Preference Strength across Generations')
    plt.legend()
    plt.tight_layout()

    plt.savefig(
        figure_dir / 'generational_preference_strength.png',
        dpi=300
    )

    plt.close()

    # Plot learner similarity across generations
    plt.figure(figsize=(8, 5))

    for meaning in meanings:
        data = similarity_df[
            similarity_df['meaning'] == meaning
        ]

        plt.plot(
            data['generation'],
            data['mean'],
            label=meaning
        )

    plt.xlabel('Generation')
    plt.ylabel('Learner similarity')
    plt.title('Learner Similarity across Generations')
    plt.legend()
    plt.tight_layout()

    plt.savefig(
        figure_dir / 'generational_similarity.png',
        dpi=300
    )

    plt.close()

    # Print summaries
    print('Preference strength summary:')
    print(
        strength_df[
            strength_df['generation'] == n_generations
        ]
    )

    print('\nLearner similarity summary:')
    print(
        similarity_df[
            similarity_df['generation'] == n_generations
        ]
    )

    print('\nResults saved to:')
    print(results_dir)


if __name__ == '__main__':
    main()