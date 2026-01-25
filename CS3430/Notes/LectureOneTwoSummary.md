# CS3430 S26 — Scientific Computing

## Master Conceptual Summary (Lectures 1–2 + Readings)

---

## 1. Scientific Computing Lives in an Approximate World

Scientific computing is **not mathematics on a computer**. It is computation in a world where:

* numbers are **finite**,
* values are **rounded**,
* arithmetic is **approximate**,
* and error is **unavoidable**.

Floating-point numbers are not real numbers. They are discrete approximations with fixed precision. Every numerical method must be understood with this constraint in mind .

---

## 2. Floating-Point Numbers (Floats)

### 2.1 What Floats Are

* Floats are stored in **binary scientific notation**:

  $$
  x = \pm (1.\text{binary fraction}) \times 2^{\text{exponent}}
  $$

* Because the number of bits is fixed:

  * only finitely many numbers exist,
  * most real numbers cannot be represented exactly,
  * decimals like `0.1` repeat forever in base-2.

### 2.2 Precision Is Not Uniform

* Floats are **densely packed near zero**.
* They become **widely spaced at large magnitudes**.
* Absolute error grows with magnitude.
* Relative precision stays roughly constant.

This explains why:

```python
0.1 + 0.2 != 0.3
```

and why adding tiny values to large numbers often does nothing .

---

## 3. Machine Epsilon (ε)

### 3.1 Definition

Machine epsilon is the smallest representable gap near 1:

$$
\varepsilon = \text{nextafter}(1.0, +\infty) - 1.0
$$

For double precision:

$$
\varepsilon \approx 2.22 \times 10^{-16}
$$

### 3.2 Why It Matters

Machine epsilon sets the **fundamental limit of numerical accuracy**:

* Differences smaller than ε are invisible.
* More printed digits ≠ more information.
* Every convergence test and tolerance must respect ε.

This value governs **everything** in scientific computing .

---

## 4. Roundoff Error & Loss of Significance

### 4.1 Roundoff Error

* Every floating-point operation introduces tiny error.
* Over many operations, error accumulates.
* Order of operations matters.
* Algorithm design determines whether error stays small or explodes.

### 4.2 Loss of Significance (Catastrophic Cancellation)

Occurs when subtracting nearly equal numbers:

* Leading digits cancel.
* Only low-precision noise remains.
* Result may have **almost no meaningful digits**.

This is why expressions like:

$$
f'(x) \approx \frac{f(x+h)-f(x)}{h}
$$

fail for very small (h) .

---

## 5. Conditioning vs. Stability (Critical Distinction)

### 5.1 Conditioning — Property of the Problem

* Measures how sensitive the **true solution** is to small input changes.
* Ill-conditioned problems amplify tiny perturbations.
* No algorithm can fix a fundamentally ill-conditioned problem.

Example: nearly singular linear systems.

### 5.2 Stability — Property of the Algorithm

* Measures how numerical errors propagate during computation.
* Stable algorithms control error growth.
* Unstable algorithms magnify roundoff and cancellation.

**Key rule**:

> A stable algorithm + well-conditioned problem → accurate results
> An unstable algorithm or ill-conditioned problem → trouble



---

## 6. Numerical Differentiation: Why It’s Hard

### 6.1 Truncation vs. Roundoff

* Truncation error ↓ as step size (h) decreases.
* Roundoff error ↑ as (h) gets too small.
* There is always an **optimal step size**.

### 6.2 Central Difference

$$
f'(x) \approx \frac{f(x+h)-f(x-h)}{2h}
$$

* Symmetry cancels leading error terms.
* Truncation error improves to (O(h^2)).
* Still fails for very small (h) due to cancellation.

### 6.3 Richardson Extrapolation

If an approximation has predictable error:

$$
A(h) = A^* + Ch^p + \dots
$$

Then:

$$
A^* \approx \frac{2^p A(h/2) - A(h)}{2^p - 1}
$$

* Cancels leading error terms.
* Boosts accuracy **without knowing the true value**.
* Eventually loses to roundoff.



---

## 7. Numerical vs. Symbolic Computation

### 7.1 NumPy (Numerical)

* Fast
* General
* Approximate
* Sensitive to noise and step size

### 7.2 SymPy (Symbolic)

* Exact
* Expression-based
* Can be slow or infeasible

### 7.3 `lambdify`

Bridges symbolic truth to numerical computation:

```python
f = sp.lambdify(x, f_sym, "numpy")
```

* Enables vectorized evaluation.
* Essential for scientific workflows.



---

## 8. Numerical Integration: Romberg Integration

### 8.1 Core Idea

* Start with trapezoidal rule.
* Error has even-power structure.
* Apply Richardson extrapolation repeatedly.

Produces a **Romberg table** of refined estimates.

### 8.2 Strengths & Limits

Works well when:

* integrand is smooth,
* data is noise-free.

Breaks when:

* function has cusps/discontinuities,
* evaluations are noisy,
* roundoff dominates.

Elegant, powerful, but not magic .

---

## 9. Type Annotations: Making Assumptions Explicit

Type annotations in CS3430 are not about enforcement — they are about **communication**.

They:

* document intent,
* expose assumptions,
* support reasoning,
* prevent silent conceptual errors.

Annotations make scientific reasoning **visible**, aligning with Python’s future (PEP 563, PEP 649) .

---

## 10. Cargo Cult Programming (And Why Scripts Matter)

### 10.1 Cargo Cult Programming

Occurs when:

* code is copied without understanding,
* outputs are trusted blindly,
* parameters are tweaked until results “look right”.

The danger is **plausible but meaningless results**.

### 10.2 Why Scripts Over Notebooks

Python scripts enforce:

* linear execution,
* explicit assumptions,
* reproducibility,
* traceable data flow.

This discipline prevents hidden state and forces real reasoning.

Scientific computing values **understanding over appearance** .

---

## 11. Core Rules to Carry Forward

1. Floats are approximate — always.
2. Avoid subtracting nearly equal numbers.
3. Scaling matters.
4. More digits ≠ more accuracy.
5. Conditioning ≠ stability.
6. Prefer stable algorithms.
7. Validate results.
8. Understand **why**, not just **how**.
9. Never trust numerical output without context.

---

## Bottom Line

Scientific computing is about **controlled approximation** guided by insight, not blind execution.

The goal of CS3430 is to teach you how to:

* see error,
* reason about limits,
* design stable methods,
* and avoid fooling yourself.

That mindset matters far more than any single algorithm.

---

*End of Master Summary*
