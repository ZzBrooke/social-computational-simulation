# social-computational-simulation
A computational simulation of individual learning, social interaction, and generational transmission in form–meaning learning.

## Research Motivation
This project started from a question that came up while reading work on language evolution and usage-based approaches, particularly Arie Verhagen's discussion of the relationship between individual linguistic knowledge and community-level conventions.

Language can be understood at both the individual and population levels. Individual speakers may develop different form–meaning associations, while repeated interaction can lead to shared patterns at the community level (Dąbrowska, 2020; Schmid, 2020; Verhagen, 2024).

This led to a computational question: **can a simple agent-based simulation be used to examine how individual learning, social interaction, and population-level patterns are related?** To explore this question, the project uses a simplified form–meaning system and gradually extends the model from individual learning to social interaction and generational transmission. It does not attempt to model language evolution or community conventions in full, but instead provides a simple computational setting for examining how individual preferences and shared population-level patterns develop together.

## Research Question
The main question is:
**How do individual learning, social interaction, and generational transmission interact to shape form–meaning preferences at the individual and population levels?**

The project explores this question through three stages:
1. **Individual learning:** How do individual form–meaning preferences develop through repeated input?
2. **Social interaction:** How do these preferences change when learners interact with one another?
3. **Generational transmission:** How do population-level patterns change when the preferences of one generation become the basis for input to the next?

## Model Overview
The simulation models a small population of learners acquiring associations between forms and meanings. The model uses four form labels (*laap*, *siu*, *zung*, and *faai*) and two abstract meanings (M1 and M2). The three experiments use the same basic learning system, with social interaction and generational transmission added step by step.

### Agents and Associations
The population consists of 10 learners. Each learner maintains association weights for the four forms and two meanings. All weights start at 1.0, so learners do not begin with a preference for any particular form.

For each meaning, a learner's preferred form is the form with the highest association weight.

### Input and Individual Learning
Each learner receives 6 input tokens per meaning in each round. The input is sampled from a probability distribution over the four forms. The model starts from the following base input probabilities:
| **Meaning** | **laap** | **siu** | **zung** | **faai** |
| ----------- | -------: | ------: | -------: | -------: |
| **M1**      |     0.35 |    0.30 |     0.20 |     0.15 |
| **M2**      |     0.20 |    0.15 |     0.35 |     0.30 |

To introduce individual variation, each base probability is multiplied by a random value between 0.3 and 1.7 and then normalized. This gives each learner a slightly different input distribution.

When a learner observes a form–meaning pair, the corresponding association weight increases by 0.1.

### Social Interaction
Social interaction is introduced in Experiment 2 and retained in Experiment 3. Within each round, learners are randomly ordered and paired. For each meaning, each learner observes the other learner's current preferred form and increases the corresponding association weight by 0.1.

This is a simple form of mutual social exposure rather than an explicit persuasion or communication mechanism.

### Generational Transmission
Generational transmission is introduced in Experiment 3. At the end of each generation, the aggregate preferences of the population are used to construct the input distribution for the next generation.

The new input distribution is then randomly perturbed and normalized, so the next generation receives input based on the previous population-level pattern but not an exact copy of it. Individual association weights are not directly passed from one generation to the next.

### Measures
The simulation tracks three main measures:
* **Preference strength:** the highest association weight for a meaning divided by the total association weight for that meaning.
* **Aggregate preference:** the distribution obtained by summing learners' association weights and normalizing them separately for each meaning.
* **Learner similarity:** the proportion of learners whose preferred form matches the population's dominant form for a given meaning.

### Simulation Settings
Each experiment is run 30 times. Experiments 1 and 2 run for 30 rounds per run. Experiment 3 runs for 20 generations, with 10 learning rounds in each generation. The individual learning rate is 0.1 throughout the experiments, while Experiments 2 and 3 use a social learning rate of 0.1.

## Experiment 1: Individual Learning
### Question
The first experiment asks:
**How do individual form–meaning preferences develop through repeated input when learners do not interact with one another?**

This experiment provides a baseline for examining the effects of social interaction in Experiment 2.

### Method
Ten learners were simulated for 30 learning rounds. In each round, each learner received 6 input tokens for each meaning, sampled from their own input distribution. The learners started with equal association weights for all forms and increased the weight of an observed form–meaning pair by 0.1.

No social interaction was included in this experiment. The simulation was repeated 30 times to examine variation across runs.

Preference strength was recorded after each round. Final aggregate preferences and learner similarity were also calculated at round 30.

### Results
Preference strength increased throughout the 30 learning rounds for both meanings.
| Meaning | Round 1 | Round 30 |
| ------- | ------: | -------: |
| M1      |  0.2869 |   0.3811 |
| M2      |  0.2851 |   0.3872 |

At round 30, the mean preference strength was **0.3811 (SD = 0.0191)** for M1 and **0.3872 (SD = 0.0200)** for M2. The gradual increase shows that repeated input led learners to develop stronger form–meaning preferences over time.

The aggregate preferences at round 30 broadly followed the initial input distributions. For M1, *laap* remained the most preferred form, followed by *siu*, while *zung* and *faai* had lower preferences. For M2, *zung* remained the most preferred form, followed by *faai*. The ranking of forms was consistent with the initial input probabilities, although the final normalized preference proportions were not identical to them.
| Meaning | Form |   Mean |
| ------- | ---- | -----: |
| M1      | laap | 0.3186 |
| M1      | siu  | 0.2976 |
| M1      | zung | 0.2140 |
| M1      | faai | 0.1698 |
| M2      | zung | 0.3321 |
| M2      | faai | 0.2885 |
| M2      | laap | 0.2069 |
| M2      | siu  | 0.1724 |

Learner similarity at round 30 was **0.53 (SD = 0.1264)** for M1 and **0.59 (SD = 0.1398)** for M2. With four possible forms, a random baseline would be 0.25. The observed similarity scores were therefore above this baseline, but still well below complete consensus.

### Interpretation
The results show that repeated individual learning increased form–meaning preference strength, but did not make learners highly similar to one another. Different learners retained different preferences even though they were exposed to similar input patterns.

This suggests that individual learning alone can strengthen associations without producing a shared population-level preference. This provides the baseline for examining what changes when social interaction is added in Experiment 2.

## Experiment 2: Social Interaction
### Question
The second experiment asks:
**How do individual form–meaning preferences change when learners are also exposed to one another's preferences?**

This experiment extends the individual learning baseline by adding social interaction between learners.

### Method
The same setup of 10 learners, 30 learning rounds, and 30 simulation runs was used as in Experiment 1. In each round, learners first received individual input sampled from their own input distributions.

After individual learning, learners were randomly ordered and paired for social interaction. For each meaning, each learner observed their partner's current preferred form and increased the corresponding association weight by 0.1. The interaction was mutual, so both learners were exposed to each other's preferences.

Preference strength and learner similarity were recorded after each round. Final aggregate preferences were also calculated at round 30.

### Results
Preference strength increased steadily over the 30 learning rounds for both meanings.
| Meaning | Round 1 | Round 30 |
| ------- | ------: | -------: |
| M1      |  0.2898 |   0.3953 |
| M2      |  0.2884 |   0.4007 |

At round 30, the mean preference strength was **0.3953 (SD = 0.0254)** for M1 and **0.4007 (SD = 0.0230)** for M2. The overall pattern was similar to Experiment 1, with learners developing stronger preferences through repeated exposure.

Learner similarity showed a larger change. For M1, similarity increased from **0.4567** in round 1 to **0.6967 (SD = 0.1650)** in round 30. For M2, it increased from **0.5133** to **0.6967 (SD = 0.1938)**.
| Meaning | Round 1 | Round 30 |
| ------- | ------: | -------: |
| M1      |  0.4567 |   0.6967 |
| M2      |  0.5133 |   0.6967 |

Similarity increased rapidly during the early rounds and remained around 0.70 in the later rounds, although it continued to fluctuate rather than increasing monotonically. These fluctuations are consistent with the stochastic nature of the model, including random pairing between learners in each round.

The aggregate preferences at round 30 continued to show the same general ranking as in Experiment 1. For M1, *laap* and *siu* remained the most strongly represented forms, while *zung* and *faai* had lower aggregate preferences. For M2, *zung* and *faai* remained the two strongest forms.

### Interpretation
Adding social interaction changed the pattern observed in Experiment 1. Preference strength increased only slightly compared with the individual-learning baseline, while learner similarity increased much more clearly, from **0.53 to 0.6967** for M1 and from **0.59 to 0.6967** for M2.

This suggests that mutual exposure to other learners' preferences affected how preferences were distributed across learners more than how strong individual preferences became. Learners became more similar without a comparable increase in individual preference strength.

However, similarity remained below complete consensus and continued to fluctuate across runs. Social interaction therefore increased population-level alignment in the model, but did not produce full convergence.

## Experiment 3: Generational Transmission
### Question
The third experiment asks:
**How do population-level form–meaning preferences change when the patterns of one generation become the input for the next generation?**

This experiment extends Experiment 2 by introducing generational transmission. Instead of keeping the original input distributions throughout the simulation, the aggregate preferences of one generation are used to construct the input distribution for the next generation.

### Method
The simulation used 10 learners across 20 generations, with 10 learning rounds within each generation. Each generation followed the setup of Experiment 2, including individual learning and social interaction.

At the end of each generation, the aggregate preferences of the population were used to construct the input distribution for the next generation. Each preference was then multiplied by a random value between 0.3 and 1.7 and normalized before being used as input for the new generation. This introduced variation into the transmission process.

Individual association weights were not directly passed from one generation to the next. Instead, each new generation started with new learners whose weights were initialized at 1.0, while population-level preference patterns were carried forward through the input distribution.

Preference strength and learner similarity were recorded across 20 generations for 30 simulation runs.

### Results
Preference strength did not show a sustained increase across generations. It started at **0.3616 for M1** and **0.3677 for M2** in Generation 1, decreased during the early generations, and then remained within a relatively narrow range.
| Meaning | Generation 1 | Generation 20 |
| ------- | -----------: | ------------: |
| M1      |       0.3616 |        0.3425 |
| M2      |       0.3677 |        0.3464 |

At Generation 20, the mean preference strength was **0.3425 (SD = 0.0248)** for M1 and **0.3464 (SD = 0.0213)** for M2.

The lower preference strength compared with Experiments 1 and 2 is also consistent with the shorter learning period within each generation. Each generation contains only 10 learning rounds, and learners' association weights are reset when a new generation is created. This prevents preference strength from simply accumulating across generations.

Learner similarity also fluctuated across generations rather than showing a steady increase.
| Meaning | Generation 1 | Generation 20 |
| ------- | -----------: | ------------: |
| M1      |       0.6333 |        0.6033 |
| M2      |       0.6600 |        0.6233 |

At Generation 20, learner similarity was **0.6033 (SD = 0.2236)** for M1 and **0.6233 (SD = 0.2063)** for M2. Across the 20 generations, M1 similarity varied roughly between **0.57 and 0.64**, while M2 varied between **0.56 and 0.68**.

Compared with Experiment 2, learner similarity at the end of Experiment 3 was lower. Experiment 2 reached **0.6967 for both meanings** at round 30, whereas Experiment 3 ended at **0.6033 for M1** and **0.6233 for M2** at Generation 20.

### Interpretation
The results show that generational transmission did not lead to a **sustained increase** in preference strength or learner similarity. Instead, both measures fluctuated within a similar range across generations.

This pattern is consistent with the structure of the model. Each new generation starts with fresh learners whose association weights are reset, while the previous generation's aggregate preferences are used as the basis for the next generation's input. The random perturbation applied during transmission can therefore carry population-level patterns forward while also introducing variation between generations.

Compared with Experiment 2, similarity at the end of Experiment 3 was lower than the approximately **0.70** observed after 30 rounds of social interaction. This suggests that the alignment produced within a generation was not simply accumulated across generations in the presence of transmission variation.

Overall, the three experiments show a progression from **stronger individual preferences**, to **greater alignment through social interaction**, to **continued variation** when these population-level patterns are transmitted across generations.

## Discussion & Limitations
### Discussion
The three experiments show how individual learning, social interaction, and generational transmission led to different patterns in the simulation. Individual learning strengthened learners' preferences for particular form–meaning pairs, but did not lead to high similarity between learners. When social interaction was added, learner similarity increased more clearly than preference strength. This suggests that interaction mainly helped learners develop more similar preferences, rather than simply making their individual preferences stronger. In the generational experiment, population-level preferences were passed on as input to new learners, but this did not lead to a steady increase in either preference strength or learner similarity across generations.

These results show that individual preferences and similarity between learners are not the same thing. A learner can develop a strong preference for a particular form without other learners developing the same preference. Social interaction can make learners' preferences more similar, even when it does not greatly increase the strength of their individual preferences. The generational experiment also suggests that passing on existing population-level patterns does not automatically make those patterns stronger or more consistent over time.

The three experiments provide a simple way to explore how individual learning and shared patterns in a group may influence each other, without treating them as the same process.

### Limitations
This project has several limitations:
1. **Simplified form–meaning system:** The simulation uses four abstract form labels and two meanings rather than real linguistic forms and meanings. It therefore represents a simple learning problem rather than the complexity of natural language.
2. **Simplified social interaction:** Social interaction is limited to learners observing their partners' current preferred forms. The model does not include communication success, communicative goals, negotiation, or other factors that can affect real language use.
3. **Simplified generational transmission:** Population-level preferences are used to create input for the next generation, with random perturbation added during transmission. Individual association weights are reset rather than directly passed on, so the model does not represent the full process of language transmission between generations.
4. **Small population and fixed settings:** The model uses 10 learners, fixed input sizes, fixed learning rates, and a limited number of rounds and generations. Different population sizes or parameter settings could produce different patterns.
5. **Random variation:** Input distributions, learner pairings, and generational input are affected by random variation. The experiments were repeated across 30 runs, but the project focuses on describing the patterns in the simulations rather than using formal statistical tests to compare conditions.

The simulation is a small-scale computational exploration rather than a complete model of language evolution. Its main purpose is to provide a simple setting for exploring how individual form–meaning learning, social interaction, and shared patterns within a group are related.

## How to Run
### Requirements
* Python 3
* NumPy
* pandas
* matplotlib

### Run the Experiments
Clone the repository and run the experiment scripts from the project root:
```bash
python scripts/Experiment1_individual_learning.py
python scripts/Experiment2_social_coordination.py
python scripts/Experiment3_generational_transmission.py
```
The scripts run the simulations and save the output files automatically:
* **Figures:** `results/figures/`
* **Summary tables:** `results/tables/`

The experiments use the parameter settings specified in the scripts. The reported results can be reproduced by running the corresponding experiment scripts.

## Project Structure
```text
social-computational-simulation/
├── scripts/
│   ├── Experiment1_individual_learning.py
│   ├── Experiment2_social_coordination.py
│   └── Experiment3_generational_transmission.py
├── results/
│   ├── figures/
│   └── tables/
├── .gitignore
└── README.md
```
* `scripts/` contains the code for the three experiments.
* `results/figures/` contains the figures generated by the simulations.
* `results/tables/` contains summary tables from the experiments.
* `.gitignore` specifies files and folders that should not be tracked by Git.
* `README.md` describes the research question, model, experiments, and results.
