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

