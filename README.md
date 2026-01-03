# Binomial Model Theory Overview

**Disclaimer**: Many regulatory bodies, including the European Securities and Markets Authority (ESMA) and the U.S. Federal Bureau of Investigation (FBI), have issued warnings or outright banned retail binary options trading due to widespread fraud. Most platforms are unregulated, and the business model often pits the trader against the broker, making it mathematically designed for traders to lose money. Binary options are often described as a form of gambling rather than a legitimate investment. 

**This is only for educational purposes, this is NOT financial advice**


## Table of Contents
1. [Introduction](#introduction)
2. [Core Concepts](#core-concepts)
3. [Forward Binary Tree](#forward-binary-tree)
4. [Backward Induction - European Options](#backward-induction---european-options)
5. [Backward Induction - American Options](#backward-induction---american-options)
6. [The Greeks](#the-greeks)
7. [Conclusion and Takeaways](#conclusion-and-takeaways)
8. [Further Comments](#further-comments)

## Introduction
The **Binomial Model** provides a method to determine an option's fair price in present value by projecting future price movements of an underlying asset over a discrete amount of time. In the simplest forms, this model only considers that the price of the underlying asset can only move in two directions -- up and down -- at a fixed magnitude.


## Core Concepts
### 5 Key Components

1. Beginning Asset Value ($S$)
→ The initial value of the underlying asset.

2. Up Move Factor (U)
→ The proportional gain when the asset price increases.
→ Represented as U.

3. Down Move Factor (D)
→ The proportional loss when the asset price decreases.
→ Represented as D = 1 / U.

4. Strike Price ($S_k$)
→ The price at which the option can be exercised.

5. Risk Free Rate ($r$)
→ Guaranteed rate of return with no risk. 

### **Note** 
Although it may seem intuitive to consider the probability of the underlying asset rising or falling, we'll later argue that the option's fair price is mutually exclusive due to arbitrage considerations.  

## Forward Binary Tree
Say the current stock price is P₀ at time T₀.
From this point, it can only move up or down at the next time step (T₁).

We model this by adding two child nodes from the current one:

Right child = P₀ × U (upward movement)

Left child = P₀ × D (downward movement)

We then repeat this process recursively for each new node until we reach the option’s expiration time T.


<p align="center">
  <img src="Picture1.png" alt="Binomial Tree Illustration" width="500"><br>
  <em>Figure 1: Stock Price Visualization</em>
</p>


#### Example
If we set iterations = 2 and U = 1.1, D = 0.9, our tree looks like:

```
            ┌── 133.10
        ┌── 121.00
        │   └── 110.00
    ┌── 110.00
    │   │   ┌── 110.00
    │   └── 100.00
    │       └── 90.91
   100.00
    │       ┌── 110.00
    │   ┌── 100.00
    │   │   └── 90.91
    └── 90.91
        │   ┌── 90.91
        └── 82.64
            └── 75.13

```

## Backward Induction - European Options

At expiration, each **terminal node** has a payoff -- the value of the option at expiration. 
Given these payoffs, we want to ask, what is the fair price of the option today? 

### Step 1: Calculate the Payoffs
Recall that for an option, there are two components for determining payoff:
\
Stock Price: $S$
\
Strike Price: $S_k$ 



For a **call** option, the payoff is as follows:
$$Payoff = max(0, S - S_k)$$

For a **put** option, the payoff is as follows:
$$Payoff = max(0, S_k - S)$$


<p align="center">
  <img src="Picture2.png" alt="Backward Induction Visualization" width="500"><br>
  <em>Figure 2: Stock Price Visualization</em>
</p>

### Step 2: Work Backward (Induction)

<p align="center">
  <img src="Picture3.png" alt="Backward Induction Visualization" width="500"><br>
  <em>Figure 3:  Option Price Visualization</em>
</p>
At the earlier node (that is, the parent node of the current children), we want to calculate the expected discount value given the two future outcomes:

$$ V_{current} = e^{-r \cdot Δt} \cdot (p \cdot V_{\text{up}} + (1-p) \cdot V_{\text{down}}) $$

Where 
* $r$ is the risk-free rate
* $Δt$ is the time between steps
* $p$ is the risk-neutral probability

$$ p = \frac{e^{r \cdot \Delta t} - D}{U - D} $$

Note that instead of the probabilities given, P(U) or P(D), we use risk-neutral probability. This is because we want to ensure **no arbitrage** -- meaning there is no way to make a riskless profit by combining stocks and options. [^Further Info]

Although it may be complicated, it'll be easier to understand once broken down. 
Inside the formula, it'll look identical as if you were to compute the regular expected value of the option, except we used risk-neutral probability instead of up and down probabilities.

$$
V_{current} = (p_{up} \cdot V_{\text{up}} + (1-p_{down}) \cdot V_{\text{down}})
$$

The factor being multiplied by the expected value ($e^{-r \cdot Δt}$) is the discount factor. Since money is flowing from the future and closer to the present day, we must discount it so that it is equivalent in value. [^Time Value of Money]

We'll repeat this process until we've reached the root node, which gives the fair option price today. 




#### Example
Parameters:

Iterations = 3

U = 1.1, D = 0.9

Risk-free rate = 0.03

Strike = 102

Call option = True

```

Option Value: 7.19
            ┌── 31.10
        ┌── 19.76
        │   └── 8.00
    ┌── 12.08
    │   │   ┌── 8.00
    │   └── 4.09
    │       └── 0.00
   7.19
    │       ┌── 8.00
    │   ┌── 4.09
    │   │   └── 0.00
    └── 2.10
        │   ┌── 0.00
        └── 0.00
            └── 0.00

```
## Backward Induction - American Options
### Key differences
Whereas European options are only allowed to be exercised upon the date of expiration, American options can be exercised throughout their lifetime. Overall, this generally provides **flexibility** as the option can be exercised at any time to potentially achieve a greater profit (or loss).  

### Calculations
At each node at some **time T**, we ask one question: **What would the value of the option be if we exercised it**? The immediate exercise value ($IEV_t$) answers that question. If you did exercise it at some time T, the immediate exercise value is simply the payoff you'd receive if you exercised the option right at that moment.

For a **call** option, the payoff at time T is as follows: 
$$IEV_t = max(0, S_t - S_k)$$

For a **put** option, the payoff at time T is as follows:
$$IEV_t  = max(S_k - S, 0)$$

Then there's the other possibility: **what if we did not exercise it**? Logically, its price would be **identical** to that of a European option, since at time T the option would **not** be exercised. We already know that value, the continuation value ($CV_t$), which is simply: 

$$CV_t = e^{-r \cdot Δt} \cdot (p \cdot V_{\text{up}} + (1-p) \cdot V_{\text{down}})$$

Now we're given two values to consider, the immediate exercise value and the continuation value. To determine the option's price at that price, we take the max of the two values:

$$V_t = max(IET_t, CV_t)$$

At first glance, we take the max simply because a rational investor wants the higher payoff.
But deeper than that, choosing anything other than the max creates an arbitrage opportunity.

#### Abritrage Example

If $IEV_t = 15$ and $CV_t = 20$ but the option is priced in at $15, an investor could buy it for $15 and hold it for a risk-free gain to $20. This guaranteed $5 profit violates no-arbitrage, so the option must be worth $20.

#### General Example
Parameters:

Iterations = 3

U = 1.1, D = 0.9

Risk-free rate = 0.1

Strike = 102

Call option = False (Put Option)

European option = False (American Option)

**Underlying Asset Price Action**
```
            ┌── 133.10
        ┌── 121.00
        │   └── 110.00
    ┌── 110.00
    │   │   ┌── 110.00
    │   └── 100.00
    │       └── 90.91
  100.00
    │       ┌── 110.00
    │   ┌── 100.00
    │   │   └── 90.91
    └── 90.91
        │   ┌── 90.91
        └── 82.64
            └── 75.13
```
**American Option** 
```
 Option Value: 5.19
            ┌── 0.00
        ┌── 0.00
        │   └── 0.00
    ┌── 1.61
    │   │   ┌── 0.00
    │   └── 4.23
    │       └── 11.09
   5.19
    │       ┌── 0.00
    │   ┌── 4.23
    │   │   └── 11.09
    └── 11.09
        │   ┌── 11.09
        └── 19.36
            └── 26.87
```

**European Option (For comparison)**

```
 Option Value: 4.37

            ┌── 0.00
        ┌── 0.00
        │   └── 0.00
    ┌── 1.61
    │   │   ┌── 0.00
    │   └── 4.23
    │       └── 11.09
   4.37
    │       ┌── 0.00
    │   ┌── 4.23
    │   │   └── 11.09
    └── 8.94
        │   ┌── 11.09
        └── 16.84
            └── 26.87
```




## Conclusion and Takeaways
The **Binomial Model** combines two integral components of finance together -- time value of money and risk neutrality -- to determine a fair price for an option.

One of my biggest takeaways was the absence of upward and downward probabilities: **Regardless of the chances of the stock going up or down, the price of the option will be the same**. Another way to look at it is we're pricing the volatility of the underlying asset. Intuitively, it makes sense, since market makers need to be hedged against up or down movement -- they don't profit off of guessing price direction, but from ensuring a fair and riskless price.  [^Additional Resource]

Another key insight was the concept of arbitrage; It gave me perspective on how options are priced in from a market maker's standpoint. It also showed me how there is no *free lunch* in a free, efficient market. I'm curious to see how other instruments are priced in with arbitrage, and if there are any limitations to this approach. 


## Further Comments
### Outlook
Since the [Black-Scholes](https://en.wikipedia.org/wiki/Black%E2%80%93Scholes_model) model can be derived from the binary options model, I may consider tackling it in the future. I may also consider doing more complex operations, such as adding the Greeks for sensitivity changes, or maybe a computational approach to determining the volatility, U. 

From a trading perspective, I may also consider applying the binary options model to the live market to see how well the model does in practice. 

### Remarks

I'd like to thank my finance professor, [Sara Smiarowski](https://www.isenberg.umass.edu/people/sara-smiarowski), for introducing me to this topic. I'm very grateful for her guidance.

I'd also like to thank my statistics professor, [Mike Sullivan](https://www.umass.edu/mathematics-statistics/about/directory/mike-sullivan), for not only deriving but explaining the mathematical components behind the binomial model. I'm very grateful for his assistance. 

If you have any comments, suggestions, or questions, feel free to reach out to me at gsokhin@umass.edu.







 [^Further Info]: https://www.youtube.com/watch?v=fZa75q5Fkkk\

 [^Additional Resource]: https://www.youtube.com/watch?v=eA5AtTx3rRI

 [^Time Value of Money]: https://en.wikipedia.org/wiki/Time_value_of_money
