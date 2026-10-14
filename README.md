# jackie-brain-twin

**Digital twin of the canine subject “Jackie” (Canis lupus familiaris)**  
Reconstructed from multi-session functional MRI, simultaneous EEG, physiological telemetry and behavioural annotation.

![License](https://img.shields.io/badge/license-MIT-blue)
![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![Status](https://img.shields.io/badge/status-research%20prototype-orange)

---

## Table of Contents

1. [Project Summary](#project-summary)
2. [Scientific Background](#scientific-background)
3. [Included fMRI Slices](#included-fmri-slices)
4. [Repository Layout](#repository-layout)
5. [Data Description](#data-description)
6. [Installation](#installation)
7. [Quick Start](#quick-start)
8. [Interactive Commands](#interactive-commands)
9. [Core Architecture](#core-architecture)
10. [Emotion & Region Dynamics](#emotion--region-dynamics)
11. [Extending the Model](#extending-the-model)
12. [Reproducibility Notes](#reproducibility-notes)
13. [Limitations](#limitations)
14. [Citation](#citation)
15. [License](#license)

---

## Project Summary

`jackie-brain-twin` is a modular Python framework that reconstructs the real-time emotional and regional brain state of a single dog (Jackie) from actual neuroimaging and physiological recordings.  

The system ingests:

- Six fully annotated scan sessions (J001–J006) containing BOLD values for olfactory bulbs, amygdalae and nucleus accumbens, EEG band-power percentages, heart rate, respiration, acceleration and behavioural markers.
- Three high-resolution axial fMRI slices acquired under distinct social conditions (novel street dog, highly familiar best-friend dog, and a neighbor dog after repeated exposure).

From these data the model continuously updates a six-dimensional emotional vector (joy, curiosity, calm, excitement, anxiety, affection) and a 25-region activation map. The resulting digital twin can be queried with arbitrary textual stimuli and returns an interpretable state vector together with the most probable behavioural phenotype.

---

## Scientific Background

Dogs possess an expanded olfactory system and a well-developed social brain network. The present reconstruction focuses on three key nodes repeatedly implicated in canine social neuroscience:

- **Olfactory bulbs** – primary sensory gate for conspecific and environmental odours  
- **Amygdala** – rapid valence and threat evaluation  
- **Nucleus accumbens** – reward and social motivation  

Additional regions (cingulate, temporal
