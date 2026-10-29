# Research Probes: Empirical Dissections of Frontier AI

Independent empirical probes, reproduction experiments, and failure-mode analyses of frontier AI preprints in **Test-Time Compute, Reasoning Search & Verification**.

Authored by **Tushar** ([GitHub](https://github.com/tushar152006) | [Substack](https://substack.com))

---

## Sprint 01: The Search Collapse Vulnerability

- **Paper Dissected**: *Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters* (Snell et al., UC Berkeley / Google DeepMind, [arXiv:2408.03314](https://arxiv.org/abs/2408.03314))
- **Key Finding**: In step-level Beam Search, errors compound multiplicatively across sequential reasoning steps ($\alpha^d$). When verifier accuracy drops below the analytical threshold:
  $$\alpha^* = \left(1 - (1 - p^d)^N\right)^{\frac{1}{d-1}} \approx \mathbf{73.9\%}$$
  Beam Search plummets down to **13.1%**, while naive Best-of-N remains resilient at **23.6%**.

### Reproduction
Run the zero-dependency simulation:
```bash
python 02_experiments/sprint_01_search_collapse.py
```
This generates the empirical table and exports the vector curve to `02_experiments/search_collapse_curve.svg`.

### Repository Structure
```
├── 01_reading_vault/   # Paper annotations and raw math notes
├── 02_experiments/     # Standalone Python probing scripts & generated plots
├── 03_drafts/          # Technical write-ups and closed-form derivations
├── 04_published/       # Launch packages (Substack & X threads)
├── templates/          # Standardized paper dissection rubrics
├── AGENTS.md           # Autonomous agent squad architecture & rules
└── WEEKLY_TRACKER.md   # Sprint progress & roadmap
```

---

## Contact & Collaborations
If you are researching inference-time compute scaling, verifier dynamics, or tree-search architectures, feel free to open an issue or reach out via email: **tusharburla7@gmail.com**.

