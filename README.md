# NFA to REGEX

Converts a nondeterministic finite accepter to a regular expression.

## Introduction
A Nondeterministic Finite Acceptor (NFA) is a finite state machine that reads in a string as input and either can accept or reject it. Unlike deterministic finite acceptors, a NFA is nondeterministic meaning the machine at times can have a choice for its next state given an input. An example of a finite state machine is given below in figure below.

<p align="center">
  <img src="https://github.com/denkovarik/NFA-to-Regex/blob/master/images/nfa.PNG">
  Figure 1: Nondeterministic Finite Acceptor Example
</p>

In the above example, λ is an empty string, q_0 is the initial state and is also the final state. An edge reading 1 means that the machine moves down that edge when the next character in the input is a 1, and edges label ‘1,0’ means that the machine can move down that edge to the next state on a 1 or a 0. The input string is accepted if the the machines state after reading the last character is in the final state q_0. Otherwise it is rejected. For example, if the input is λ, or 10, or 1010, then the machine will most likely accept the input. What makes this graph nondeterministic is the presence of a λ transition along the edge from q_0 to q_2. This mean that if the machine is is q_0, it can go to q_2 on an empty string. In addition, if the machine is currently in q_1 and then reads a 0 as the next character, the machine could go back to q_0 via the edge labeled ‘0’, or it can go to q_2 via the edge labeled ‘0,1’. Let’s say the input string in 10. This means the machine can go from q_0 to q_1 back to q_0, it can go from q_0 to q_1 to q_1, or it can go directly to q_2. The machine essentially has a choice for its next state given certain inputs.

A regular expression can sometimes be used to to represent a NFA. For example the regular expression that would describe the above graph is ‘(10)*, meaning that an string of ‘01’ repeated 0 or more times would be accepted by the finite state machine (the * symbol means the that previous character of group of characters in parentheses can be repeated 0 or more times. Given an input NFA described in dot notation, this program will convert the NFA to an equivalent regular expression.

## Dependencies
* Python
* Graphviz
* Graphviz 0.16 Python Package
* Networkx

## Setup

### Clone the Repo
* SSH
```
git clone git@github.com:denkovarik/NFA-to-Regex.git
```
* HTTPS
```
git clone https://github.com/denkovarik/NFA-to-Regex.git
```

### Usage
```
python nfa2Rex.py path/to/nfa/dot/file.gv
```
* Example usage
```
python nfa2Rex.py testing/NFAs/tests/test1.gv
```

### Testing
* Run all Unit and Functional Tests
```
python testing/runTests.py
```
Test NFA graphs can be found in the 'testing/NFAs/tests/' directory.

## Description of Algorithms
Given an NFA with a single final state the is distinct from the initial state, the basic algorithm is to iteratively remove nodes one at a time until there are only 2 states left. An equation is then applied to the final 2 states the get the final regular expression. The algorithm is as follows:

1. > Start with an nfa with states q0, q1, … , qn, and a single final state, distinct from its initial state.
2. > Convert the nfa into a complete generalized transition graph (GTG). This means that you generate a complete graph where every node is connected to every other node. Each new node that needs to be added is labeled with ∅. An example of a complete generalized transition graph for the nfa from figure 1 is given below in figure 2.
   > <p align="center">
   >   <img src="https://github.com/denkovarik/NFA-to-Regex/blob/master/images/gtg.PNG">
   >   
   >   Figure 1: Complete Generalized Transition Graph
   > </p>
3. > If the GTG has only two states, with qi as its initial state and qj its final state, its associated regular expression is
   > <p align="center">
   >   <img src="https://github.com/denkovarik/NFA-to-Regex/blob/master/images/eq1.PNG">
   >   
   >   Equation 1
   > </p>
4. > If the GTG has three states, with an initial state qi, final state qj, and third state qk, introduce new edges labeled
   > <p align="center">
   >   <img src="https://github.com/denkovarik/NFA-to-Regex/blob/master/images/eq2.PNG">
   >   
   >   Equation 2
   > </p>
5. > 	If the GTG has four or more states, pick a state qk to be removed. Apply rule 4 for all pairs of states (q_i,q_j ),i≠k,j≠k. At each step apply the simplifying rules
   > <p align="center">
   >   <img src="https://github.com/denkovarik/NFA-to-Regex/blob/master/images/simpRules.PNG">
   >   
   >   Simplification Rules
   > </p>
   > wherever possible. When this is done, remove state qk.
6. > Repeat Steps 3 to 5 until the correct regular expression is obtained.

For the special cases where the given NFA has a final state that is the same as the initial state, follow the algorithm above you the graph is reduced to to states. When the graph is reduced to two states with an initial and final state of p and a second state k, apply the following equation to get the regular expression for the graph while applying the simplifying rues from step 5.

<p align="center">
  <img src="https://github.com/denkovarik/NFA-to-Regex/blob/master/images/eq3.PNG">
  
  Equation 3
</p>

## Author
* Dennis Kovarik 
