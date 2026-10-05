import random
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


# Basic settings
forms = ['laap', 'siu', 'zung', 'faai']
meanings = ['M1', 'M2']

n_learners = 10
n_rounds = 30
input_size = 6
n_runs = 30
learning_rate = 0.1

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
            main_forms[meaning] = max(
                self.weights[meaning],
                key=self.weights[meaning].get
            )

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
def create_learners():
    learners = []

    for _ in range(n_learners):
        input_probs = create_input_probs()
        learners.append(Agent(input_probs))

    return learners


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
        population_main_forms[meaning] = max(
            prefs[meaning],
            key=prefs[meaning].get
        )

    similarity = {}

    for meaning in meanings:
        matches = 0

        for agent in learners:
            agent_main_forms = agent.get_main_forms()

            if agent_main_forms[meaning] == population_main_forms[meaning]:
                matches += 1

        similarity[meaning] = matches / len(learners)

    return similarity


# Run one simulation
def run_simulation(seed):
    random.seed(seed)

    learners = create_learners()
    records = []

    for r in range(1, n_rounds + 1):

        for agent in learners:
            inputs = generate_inputs(agent.input_probs)
            agent.receive(inputs)

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
                'round': r,
                'meaning': meaning,
                'strength': (
                    sum(strengths[meaning])
                    / n_learners
                )
            })

    prefs = get_aggregate_prefs(learners)
    similarity = get_similarity(learners, prefs)

    return learners, records, prefs, similarity


# Save final results
def save_results(all_runs, all_prefs, all_sim):
    # Save final weights
    weight_records = []

    for run, learners in enumerate(all_runs, start=1):
        for learner, agent in enumerate(learners, start=1):
            for meaning in meanings:
                for form in forms:
                    weight_records.append({
                        'run': run,
                        'learner': learner,
                        'meaning': meaning,
                        'form': form,
                        'weight': agent.weights[meaning][form]
                    })

    weights_df = pd.DataFrame(weight_records)

    weights_df.to_csv(
        table_dir / 'final_weights.csv',
        index=False
    )

    # Save aggregate preferences
    pref_records = []

    for run, prefs in enumerate(all_prefs, start=1):
        for meaning in meanings:
            for form in forms:
                pref_records.append({
                    'run': run,
                    'meaning': meaning,
                    'form': form,
                    'proportion': prefs[meaning][form]
                })

    prefs_df = pd.DataFrame(pref_records)

    pref_summary = (
        prefs_df
        .groupby(['meaning', 'form'])['proportion']
        .agg(['mean', 'std'])
        .reset_index()
    )

    prefs_df.to_csv(
        table_dir / 'aggregate_preferences_all_runs.csv',
        index=False
    )

    pref_summary.to_csv(
        table_dir / 'aggregate_preferences_summary.csv',
        index=False
    )

    # Save learner similarity
    sim_records = []

    for run, similarity in enumerate(all_sim, start=1):
        for meaning in meanings:
            sim_records.append({
                'run': run,
                'meaning': meaning,
                'similarity': similarity[meaning]
            })

    sim_df = pd.DataFrame(sim_records)

    sim_summary = (
        sim_df
        .groupby('meaning')['similarity']
        .agg(['mean', 'std'])
        .reset_index()
    )

    sim_df.to_csv(
        table_dir / 'learner_similarity_all_runs.csv',
        index=False
    )

    sim_summary.to_csv(
        table_dir / 'learner_similarity_summary.csv',
        index=False
    )

    return pref_summary, sim_summary


# Run all simulations
def main():
    all_runs = []
    all_records = []
    all_prefs = []
    all_sim = []

    for run in range(n_runs):
        learners, records, prefs, similarity = (
            run_simulation(seed=run)
        )

        all_runs.append(learners)
        all_prefs.append(prefs)
        all_sim.append(similarity)

        for record in records:
            record['run'] = run + 1
            all_records.append(record)

    # Save preference strength over time
    records_df = pd.DataFrame(all_records)

    strength_df = (
        records_df
        .groupby(['round', 'meaning'])['strength']
        .agg(['mean', 'std'])
        .reset_index()
    )

    strength_df.to_csv(
        table_dir / 'preference_strength_over_time.csv',
        index=False
    )

    # Plot preference strength over time
    plt.figure(figsize=(8, 5))

    for meaning in meanings:
        data = strength_df[
            strength_df['meaning'] == meaning
        ]

        plt.plot(
            data['round'],
            data['mean'],
            label=meaning
        )

    plt.xlabel('Learning round')
    plt.ylabel('Preference strength')
    plt.title('Preference Strength over Learning Rounds')
    plt.legend()
    plt.tight_layout()

    plt.savefig(
        figure_dir / 'preference_strength_over_time.png',
        dpi=300
    )

    plt.close()

    # Save other results
    pref_summary, sim_summary = save_results(
        all_runs,
        all_prefs,
        all_sim
    )

    # Print summaries
    print('Preference strength summary:')
    print(
        strength_df[
            strength_df['round'] == n_rounds
        ]
    )

    print('\nAggregate preference summary:')
    print(pref_summary)

    print('\nLearner similarity summary:')
    print(sim_summary)

    print('\nResults saved to:')
    print(results_dir)


if __name__ == '__main__':
    main()