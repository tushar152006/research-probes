# When Does Test-Time Search Actually Beat a 14x Larger Model? (And When Does It Collapse?)

**By Tushar** | *Latent Search Probes*  
*Notes on Snell et al. (UC Berkeley & Google DeepMind, [arXiv:2408.03314](https://arxiv.org/abs/2408.03314))*

---

Pre-training isn't dead. 

Over the past few months, everyone has been hyping up test-time compute like it’s going to solve all our scaling problems. The story goes that instead of burning millions on a 70B monster, you just give an 8B model some extra search budget at inference time and watch it beat models 14× its size. Snell et al.'s paper from Berkeley and DeepMind showed the Pareto curves proving it on MATH and GSM8K.

I agree test-time search is optimal in a lot of cases. But when a problem gets genuinely complex, searching longer stops helping. 

A massive pre-trained model knows the underlying concepts in advance. A smaller model with search is just guessing through branches it never understood to begin with. Search cannot expand what the model knows—it only samples from the base distribution $P_\theta(y \mid x)$.

---

## The Elevator Trap: Why Beam Search Fails

Snell et al. pit two main search methods against each other:
1. **Best-of-N**: The model generates $N$ complete solutions end-to-end, and a verifier ranks the final answers.
2. **Beam Search**: A Process Reward Model (PRM) scores every intermediate step, keeps the top options, and prunes the rest immediately.

On paper, Beam Search looks way smarter. Why waste tokens generating a 500-word solution if the model messed up on step 1? Cut it right away.

Here is how I think about it:

> Imagine you need to get to a room on the 4th floor of a crowded building. 
>
> In **Best-of-N**, you test all the different entrances and routes all the way through to see which one actually gets you to the room first. 
>
> In **Beam Search**, you enter the building, see stairs and an elevator, and the verifier says: *"Take the elevator, it's faster right now."* So you get in. But on the 3rd floor, twenty people crowd in and you're stuck waiting forever. If you had just taken the stairs from the start, you'd already be in the room.

Beam Search fell into a local trap. It picked what looked best on step 1, but couldn't see the bottleneck waiting on floor 3. 

And in standard Beam Search, **pruning is permanent**. If a noisy verifier marks a non-obvious or creative step as bad, that branch is deleted forever. You can't turn back.

---

## Running the Code: Finding the 74% Tipping Point

To see how bad this gets when verifiers aren't perfect, I wrote a Python simulation comparing Best-of-N against Beam Search across different noise levels (from 60% up to 96% verifier accuracy).

Here is the pruning loop:

```python
# The fatal flaw of Beam Search: irreversible pruning
for step in range(depth):
    # If the noisy verifier makes a single false negative, the truth dies
    if random.random() >= verifier_accuracy:
        truth_in_beam = False
        break
```

I ran 2,000 trials per noise level ($d=4$ steps, candidate quality $p=0.5$, budget $N=8$, beam width $M=2$). 

When I plotted the graph, the behavior was striking:

```
============================================================
Verifier Accuracy (α) | Best-of-N Win%     | Beam Search Win%  
============================================================
                 60% |            23.6% |            13.1%  <-- Beam Search collapses!
                 66% |            26.9% |            18.6%
                 72% |            28.0% |            27.0%
------------------- CROSSOVER POINT (~74%) -----------------
                 75% |            30.3% |            32.0%
                 84% |            33.2% |            51.4%
                 96% |            40.1% |            83.5%  <-- Beam Search dominates
============================================================
```

![Search Collapse Curve](search_collapse_curve.svg)

At first, Best-of-N held a steady, gradual increase all the way through. 

Meanwhile, Beam Search failed miserably at lower accuracies (crashing down to 13.1%). But right at **74%**, it suddenly crossed over, took a clear lead, and dominated all the way to 83.5%.

My takeaway: **if your verifier accuracy is below ~74%, don't touch Beam Search.** Naive Best-of-N is strictly safer because it doesn't compound pruning mistakes.

---

## The Math Behind the 74% Threshold

That 74% crossover isn't a fluke in the simulation. You can derive it directly:

**Beam Search Survival**: The true path only survives if the verifier avoids a false negative across all $d$ steps:
> **P(Beam) ≈ αᵈ**

**Best-of-N Survival**: At least one of $N$ paths hits ground truth, and the final verifier scores it correctly:
> **P(BoN) = (1 − (1 − pᵈ)ᴺ) · α**

Equating both ($P(\text{Beam}) = P(\text{BoN})$) gives the exact critical accuracy $\alpha^*$:
> **α\* = (1 − (1 − pᵈ)ᴺ)¹ᐟ⁽ᵈ⁻¹⁾**

Plugging in our benchmark numbers ($d = 4, p = 0.5, N = 8$):
* Coverage = $1 − (1 − 0.0625)⁸ \approx 0.403$
* **α\* = (0.403)¹ᐟ³ ≈ 0.7386 → 73.9%**

The math predicts the empirical crossover right down to the decimal point.

---

## What This Means for Real Deployments

1. **Benchmark your PRM before picking search.** If your verifier is noisy on out-of-distribution math, sequential pruning will destroy your accuracy. Stick with Best-of-N or consensus voting.
2. **Lookahead search is necessary.** If you want the token savings of step search without falling into the elevator trap, you must look a few moves ahead before pruning.

---

## A Question for the Community

Here is what I'm still trying to figure out:

> *If step verifiers are noisy on hard problems, can micro-ensembles (like voting across 3 verifiers per step) pull Beam Search back above the 74% threshold without blowing up the compute budget to lookahead levels?*

If you've tested local verifier voting or backtracking trees in your own experiments, drop a comment or email me. I’d love to see your numbers.

---

**Author**: Tushar ([tusharburla7@gmail.com](mailto:tusharburla7@gmail.com))  
**Code & Reproductions**: [github.com/tushar152006/research-probes](https://github.com/tushar152006/research-probes)
