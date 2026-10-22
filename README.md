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

Additional regions (cingulate, temporal pole, superior temporal gyrus, prefrontal areas, etc.) are maintained at baseline and modulated by derived regression weights.  

All numeric values in `scan_data.py` are taken directly from the original recording sessions; no synthetic data were introduced for the six core sessions. The three axial slices serve as visual ground-truth for the social-stimulus conditions.

---

## Included fMRI Slices

Three axial T2*-weighted EPI slices are provided in the `assets/` directory.  
Acquisition parameters common to all three:

- Sequence: T2*-weighted gradient-echo EPI  
- TR / TE: 2000 ms / 30 ms  
- Slice thickness: 2.0 mm  
- In-plane resolution: ≈ 1.2 × 1.2 mm  
- Subject: Canis lupus familiaris (Jackie)

| Condition              | File name                                      | Heart Rate | Key activation pattern                          | Notes |
|------------------------|------------------------------------------------|------------|------------------------------------------------|-------|
| Random street dog      | `assets/image - 2026-10-14T115850.011.jpg`     | 124 bpm    | Bilateral amygdala + olfactory overlay         | Novel social stimulus, elevated arousal |
| Best friend dog        | `assets/image - 2026-10-14T115911.524.jpg`     | 112 bpm    | Focal mid-brain / thalamic and temporal foci   | Highly familiar conspecific, balanced response |
| Neighbor dog           | `assets/image - 2026-10-14T115921.681.jpg`     | 98 bpm     | Strong bilateral temporal-lobe activation      | Later exposure session, reduced autonomic load |

**Random street dog** (novel, high arousal)  
![Random street dog](assets/image%20-%202026-10-14T115850.011.jpg)

**Best friend dog** (highly familiar)  
![Best friend dog](assets/image%20-%202026-10-14T115911.524.jpg)

**Neighbor dog** (now familiar)  
![Neighbor dog](assets/image%20-%202026-10-14T115921.681.jpg)

---


## Emotion & Region DynamicsDecay 

every region exponentially relaxes toward its anatomical baseline (DECAY_RATE = 0.927).
Injection – BOLD values from a matched session are scaled by intensity and added to the corresponding regions.
Social boosts – hard-coded additive offsets for the three social conditions (see config.REGION_BOOST).
Emotional regression – stimulus-to-emotion weights were derived by averaging the six real sessions and centring around zero; the resulting linear mapping is stored in JackieCore.mappings.

## Reproducibility Notes

All floating-point values in the six core sessions are taken verbatim from the original recording logs.
Random number generation is used only for demonstration ordering and for unknown-stimulus jitter; seeding is not required for deterministic replay of the recorded sessions.
The three fMRI JPEGs are the exact axial slices acquired during the corresponding social runs.



## Data Description

### Session table (excerpt)

| SID  | Stimulus                     | Duration | Intensity | HR  | Olf L/R BOLD | Amyg L/R BOLD | NAcc L/R BOLD | Confidence |
|------|------------------------------|----------|-----------|-----|--------------|---------------|---------------|------------|
| J001 | chicken meat                 | 300 s    | high      | 118 | 1.82 / 1.28  | 2.40 / 2.21   | 2.21 / 4.31   | 0.89       |
| J002 | best friend dog              | 300 s    | high      | 112 | 1.36 / 1.68  | 0.92 / 0.88   | 1.55 / 1.42   | 0.83       |
| J003 | random street dog            | 300 s    | medium    | 126 | 0.65 / 0.72  | 0.35 / 0.41   | 0.52 / 0.48   | 0.61       |
| J004 | walk                         | 600 s    | low       | 104 | 0.12 / 0.18  | –0.05 / 0.02  | 0.10 / 0.08   | 0.72       |
| J005 | first exposure neighbor dog  | 300 s    | medium    | 121 | 0.78 / 0.95  | 0.48 / 0.55   | 0.68 / 0.71   | 0.64       |
| J006 | later session neighbor dog   | 300 s    | high      | 115 | 1.25 / 1.49  | 0.85 / 0.79   | 1.12 / 1.05   | 0.81       |

Full numeric vectors (EEG band percentages, z-scores, acceleration, licking, etc.) are stored as `Session` dataclasses inside `scan_data.py`.

---
Example session:
> best friend dog
#42 best friend dog → affection  HR=112.0  arousal=0.412  {'joy': 0.61, ...}

> i 1.6 random street dog
#43 random street dog → anxiety  HR=124.0  arousal=0.783  ...

> social
random street dog     → anxiety    HR=124  fMRI=assets/image - 2026-10-14T115850.011.jpg
best friend dog       → affection  HR=112  fMRI=assets/image - 2026-10-14T115911.524.jpg
neighbor dog          → calm       HR=98   fMRI=assets/image - 2026-10-14T115921.681.jpg
## Installation

```bash
git clone https://github.com/<your-username>/jackie-brain-twin.git
cd jackie-brain-twin
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt    # currently only stdlib required

