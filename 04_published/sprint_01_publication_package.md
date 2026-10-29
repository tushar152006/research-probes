# Sprint 01 Publication Package

**Paper Dissected**: *Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters* (Snell et al., UC Berkeley / Google DeepMind)  
**Artifacts**:
- Full Essay: `03_drafts/sprint_01_draft.md`
- Simulation Code: `02_experiments/sprint_01_search_collapse.py`
- Vector Graphic: `02_experiments/search_collapse_curve.svg`

---

## Part 1: Substack / Blog Setup

* **Post Title**: When Does Test-Time Search Actually Beat a 14x Larger Model? (And When Does It Collapse?)
* **Subtitle**: Why step-level beam search plummets below a 73.9% verifier accuracy threshold—and why naive Best-of-N is surprisingly resilient.
* **Cover Image**: Upload `02_experiments/search_collapse_curve.svg` (or export as PNG).
* **Tags**: `Artificial Intelligence`, `Machine Learning`, `Test-Time Compute`, `LLM Reasoning`, `Research Notes`.

---

## Part 2: The 7-Tweet X (Twitter) Thread

Copy and paste each numbered tweet below into a thread on X:

### Tweet 1 (The Hook)
Can an 8B model with smart search genuinely beat a model 14× its size?

UC Berkeley & DeepMind showed it can on Pareto frontiers.

But there’s an operational catch nobody talks about: if your verifier accuracy drops below 74%, step-level Beam Search collapses.

Here is the math & simulation 🧵👇
*(Attach image: `02_experiments/search_collapse_curve.svg`)*

---

### Tweet 2 (The Mechanism)
The intuition behind test-time compute is simple: 
Search cannot expand the policy's support $P_\theta(y \mid x)$, but on medium tasks, base models already possess the facts. They just get derailed early.

A search budget lets an 8B explore alternative branches and verify them.

---

### Tweet 3 (The Skeptic's Catch)
The paper pits two search mechanisms against each other:
1. Best-of-N (sample $N$ full solutions, pick the best)
2. Beam Search with a PRM (score and prune intermediate steps)

Beam search looks 10x more efficient. But it relies on a dangerous assumption: an infallible verifier.

---

### Tweet 4 (The Empirical Failure Mode)
What happens when your PRM is noisy?

In Beam Search, pruning is irreversible. If an imperfect verifier rejects a creative step (false negative), that path is dead forever.

I simulated this across 2,000 trials. The results:

• At 90% verifier acc: Beam dominates (64.5% vs 38%)
• At 60% verifier acc: Beam collapses to 13.1% (Best-of-N holds at 23.6%)

---

### Tweet 5 (The Analytical Proof)
The ~74% crossover isn't random noise. It can be derived in closed-form:

$P(\text{Beam}) \approx \alpha^d$
$P(\text{BoN}) = (1 - (1 - p^d)^N) \cdot \alpha$

Equating both yields the critical threshold:
$\alpha^* = (1 - (1 - p^d)^N)^{\frac{1}{d-1}}$

For $d=4, p=0.5, N=8$, $\alpha^* \approx 73.9\%$.
Exact match with our empirical tipping point.

---

### Tweet 6 (Engineering Rules of Thumb)
If you're building test-time reasoning systems today:
1. Never deploy step-level Beam Search on OOD tasks without benchmarking your PRM's false-negative rate.
2. If your verifier is noisy, naive Best-of-N or majority voting is strictly safer.
3. Lookahead search is the only real bridge against greedy myopia.

---

### Tweet 7 (Discussion & Repo)
Open question for researchers & practitioners:
Can micro-ensembles (3-verifier voting per step) rescue Beam Search below 74% without blowing up compute to lookahead levels?

Full dissection & reproducible Python script:
🔗 Substack: [Your Substack Post Link]
💻 Code: https://github.com/tushar152006/research-probes

Feedback & critiques welcome in replies or via email (in bio).

