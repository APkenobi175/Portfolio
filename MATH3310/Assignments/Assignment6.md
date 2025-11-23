```latex
\documentclass{article}
\usepackage{amsmath, amssymb}
\usepackage{graphicx}

\begin{document}

\section*{Homework Assignment 7}
Ammon Phipps

\section*{Question 1}

Use the Principle of Inclusion/Exclusion to determine a formula for  
\[
\left\{ {n \atop k} \right\}.
\]

\bigskip

First lets draw a universe around $\left\{ {n \atop k} \right\}$, and create a people in rooms analogy.

\medskip

We have people,
\[
N = \{1, \ldots, n\}
\]
and rooms,
\[
K = \{\text{ENG104},\ \text{FAV150},\ \ldots,\ \text{MAIN227},\ k\}.
\]

\medskip

The universe would then be
\[
U = \{ f : |N| \to |K| \}.
\]

We are trying to have $n$ people pick one of the $k$ rooms, so
\[
|U| = k^n.
\]

\bigskip

To apply the principle of inclusion and exclusion lets create a Venn diagram of all the $k$ rooms, then draw a box around it and shade in the box outside the circles. Everything inside the box is our universe $U$.

For each room $i$,
\[
A_i = \{\text{the assignments in which room $i$ is empty}\}.
\]

Each $A_i$ is a large overlapping region of the circles.

\[
A_1 \cup A_2 \cup \cdots \cup A_k
\]
represents all the assignments with at least one empty room.

The region outside all the circles, but still in $U$, is the assignments where \emph{no} rooms are empty.

\bigskip

The outside, shaded region inside $U$ is what we are trying to count. This matches the midterm experience question 3 where we partition $n$ people into $k$ nonempty labeled rooms. A surjection from $|N|$ to $|K|$ equals
\[
k! \left\{ {n \atop k} \right\}.
\]

\bigskip

Using the principle of inclusion and exclusion,

\begin{enumerate}
    \item Start by counting everything in the universe: $k^n$.
    \item Subtract regions where one room is empty:
    \[
    \binom{k}{1}(k-1)^n.
    \]
    \item Add back the regions where two rooms are empty:
    \[
    \binom{k}{2}(k-2)^n.
    \]
    \item By the Meeting 35 notes we organize all these intersections with alternating signs with ``The PIE'' Theorem and get
    \[
    k! \left\{ {n \atop k} \right\}
    = \sum_{i=0}^{k} (-1)^i \binom{k}{i} (k-i)^n.
    \]
\end{enumerate}

\bigskip

Now to find $\left\{ {n \atop k} \right\}$ we can divide both sides by $k!$ and get
\[
\boxed{
\left\{ {n \atop k} \right\}
= \frac{1}{k!} \sum_{i=0}^{k} (-1)^i \binom{k}{i} (k-i)^n
}.
\]

\end{document}

```