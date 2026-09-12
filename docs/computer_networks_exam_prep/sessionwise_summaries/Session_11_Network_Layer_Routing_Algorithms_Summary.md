# Computer Networks (BSDCBZC481)
# Session 11: Network Layer Control Plane — Routing Algorithms (Dijkstra, Bellman-Ford, OSPF & BGP)
### Exhaustive Slide-by-Slide Academic Exam Revision Manual & Problem Solving Guide

---

## 1. Session Context & Pedagogical Scope
- **Course Code & Title**: BSDCBZC481 — Computer Networks
- **Instructor**: Dr. K. Kalaiselvi (BITS Pilani)
- **Primary Textbooks**:
  - J.F. Kurose & K.W. Ross, *Computer Networking: A Top-Down Approach*, 5th/6th Edition, Chapters 4 & 5 (T1)
  - B.A. Forouzan, *Data Communications and Networking*, 4th Edition, Chapter 22 (T2)
- **Lecture Slide Mapping**: CS11: Network Layer — Slides 1 to 65 (Complete Coverage)
- **Core Syllabus Covered**:
  1. Routing Graph Abstraction: Nodes, Edges, Cost Functions & Classification Taxonomies
  2. Link-State (LS) Routing: Dijkstra's Algorithm, State Flooding, Step-by-Step Table Execution & $O(V^2)$ Complexity
  3. Traffic-Sensitive Cost Oscillations & Damping Strategies
  4. Distance-Vector (DV) Routing: The Bellman-Ford Dynamic Programming Equation
  5. Distance-Vector Distributed Convergence & Neighbor Table Message Exchanges
  6. The Count-to-Infinity Catastrophe, Routing Loops & The Poisoned Reverse Technique
  7. Scalability Limits of Flat Routing & Hierarchical Autonomous Systems (AS)
  8. Intra-AS Routing Protocols: OSPF (Link-State, Area Hierarchies) vs. RIP (Hop Count Distance Vector)
  9. Inter-AS Routing Protocols: Border Gateway Protocol (BGP-4), eBGP vs. iBGP & Path Vectors
  10. Policy-Based Routing Economics: Customer-Provider Relationships & Hot-Potato Routing
  11. High-Yield Open-Book Exam Traps, Rigorous Numerical Problems & Fast Revision Checklist

---

## 2. Graph Abstraction & Routing Algorithm Taxonomies (Slides 3–8)

The network core is modeled mathematically as an undirected weighted graph:
$$G = (V, E)$$
- $V$: Set of network routers (nodes or vertices).
- $E$: Set of physical communication links connecting router pairs (edges).
- $c(x, y)$: Cost of the link connecting node $x$ to node $y$. If $(x, y) \notin E$, then $c(x, y) = \infty$.
- **Path Cost**: For path $p = (v_1, v_2, \dots, v_k)$, total cost is $\sum_{i=1}^{k-1} c(v_i, v_{i+1})$.

```
        (2)
   [u]-------[v]
   / \       / \
(1)   (2) (3)   (1)
 /     \ /       \
[x]-----[w]-------[y]
   (1)       (2)
```

### 2.1 Classification Dimensions (Slide 5)
1. **Global vs. Decentralized**:
   - **Global (Link-State)**: Every router possesses a complete, identical map of the entire network topology and all link costs.
   - **Decentralized (Distance-Vector)**: No router has complete global knowledge. Routers know only the costs to their immediate physical neighbors and iteratively exchange distance vectors with those neighbors.
2. **Static vs. Dynamic**:
   - **Static**: Routes change very slowly, altered only through manual human administrative intervention.
   - **Dynamic**: Routes change automatically in real time in response to link failures, router reboots, or fluctuating traffic loads.

---

## 3. Link-State Routing: Dijkstra’s Algorithm (Slides 9–20)

In Link-State routing, every router discovers its neighbors and costs, packs them into **Link-State Advertisements (LSAs)**, and reliably floods them across the network. Once all LSAs are received, each router runs **Dijkstra's Shortest-Path Algorithm** locally to compute the least-cost path tree from itself as the root to all destinations.

### 3.1 Mathematical Notation & Algorithm Specification
Let:
- $u$: The source router running the algorithm.
- $N'$: The set of nodes whose least-cost paths from $u$ have been definitively determined.
- $D(v)$: The current estimate of the least-cost path from source $u$ to destination $v$.
- $p(v)$: Predecessor node immediately preceding $v$ along the current shortest path from $u$.
- $c(x, y)$: Physical link cost between adjacent nodes $x$ and $y$.

```
+-----------------------------------------------------------------------------------------+
|                              DIJKSTRA'S ALGORITHM PSEUDOCODE                            |
|                                                                                         |
| 1. INITIALIZATION:                                                                      |
|    N' = {u}                                                                             |
|    for all nodes v:                                                                     |
|        if v is adjacent to u:                                                           |
|            D(v) = c(u, v),  p(v) = u                                                    |
|        else:                                                                            |
|            D(v) = infinity                                                              |
|                                                                                         |
| 2. LOOP:                                                                                |
|    find w not in N' such that D(w) is MINIMUM                                           |
|    add w to N'                                                                          |
|    update D(v) for all neighbors v of w not in N':                                      |
|        D(v) = min( D(v),  D(w) + c(w, v) )                                              |
|        if D(v) was updated, set p(v) = w                                                |
|                                                                                         |
| 3. TERMINATION:                                                                         |
|    Repeat loop until N' contains ALL nodes in the network graph (N' = V).               |
+-----------------------------------------------------------------------------------------+
```

### 3.2 Computational Complexity & Routing Oscillations (Slides 18–20)
- **Time Complexity**:
  - Naive linear array search: $n$ iterations searching up to $n$ nodes $\implies O(n^2)$.
  - Binary min-heap / Priority Queue: $\mathbf{O(|E| + |V| \log |V|)}$, enabling rapid calculation on large graphs.
- **Routing Flapping / Oscillations (Slide 20)**:
  - If link costs are defined dynamically based on traffic volume (congestion-sensitive routing), link costs change continuously.
  - When traffic shifts to a low-cost link, that link becomes congested, driving its cost up. Routers recompute and shift all traffic back to the opposite link, creating a high-frequency **ping-pong routing oscillation**.
  - *Mitigation*: Ensure link metrics do not depend strictly on instantaneous load, or introduce randomized measurement timers to desynchronize router calculations.

---

## 4. Distance-Vector Routing: Bellman-Ford Algorithm (Slides 21–35)

Distance-Vector routing is an **iterative, asynchronous, and distributed** algorithm where nodes communicate exclusively with direct physical neighbors.

### 4.1 The Bellman-Ford Optimality Equation (Slide 23)
Let $d_x(y)$ be the cost of the least-cost path from node $x$ to destination node $y$.
$$d_x(y) = \min_{v \in \text{neighbors}(x)} \left\{ c(x, v) + d_v(y) \right\}$$

```
          c(x, v)                   d_v(y)
[ Node x ] ======> [ Neighbor v ] ==========> [ Destination y ]
```
The least cost from $x$ to $y$ is the minimum sum of the direct cost to a neighbor $v$ plus neighbor $v$'s advertised distance to $y$, evaluated across all direct neighbors $v$.

### 4.2 Distance Vector Exchange Logic (Slide 25)
Each node $x$ maintains:
1. Direct link costs to each neighbor: $c(x, v)$.
2. Its own distance vector: $\mathbf{D}_x = [D_x(y) : y \in V]$.
3. Distance vectors received from each neighbor: $\mathbf{D}_v = [D_v(y) : y \in V]$.
Whenever a node detects a local link cost change or receives an updated distance vector from a neighbor, it re-evaluates the Bellman-Ford equation. If its own vector changes, it broadcasts the new vector to all direct neighbors.

---

## 5. The Count-to-Infinity Problem & Poisoned Reverse (Slides 32–35)

### 5.1 The Asymmetry of Good News vs. Bad News
- **"Good news travels fast"**: When a link cost decreases, distance vector nodes update and converge in a single iteration.
- **"Bad news travels slowly"**: When a link cost increases or breaks, routing loops emerge that cause node distance estimates to increment slowly toward infinity (**Count-to-Infinity**).

```
COUNT-TO-INFINITY SCENARIO:
[ x ] -------(4)------- [ y ] -------(1)------- [ z ]
Before failure:
y's path to x: direct link (cost = 4).
z's path to x: via y (cost = 1 + 4 = 5).

DISASTER: Link between x and y BREAKS (cost becomes infinity)!
1. y detects link failure: c(x, y) = infinity.
2. y checks z's advertised vector: z previously advertised D_z(x) = 5.
3. y mistakenly concludes: "z has an alternative path to x with cost 5! I can reach x through z!"
4. y updates: D_y(x) = c(y, z) + D_z(x) = 1 + 5 = 6. y routes to x via z.
5. z receives y's update (D_y(x) = 6).
6. z computes: D_z(x) = c(z, y) + D_y(x) = 1 + 6 = 7. z routes to x via y.
7. y and z bounce packets back and forth, incrementing costs: 6 -> 7 -> 8 -> 9 ...
   until the metric reaches infinity (16 in RIP)!
```

### 5.2 The Poisoned Reverse Solution (Slide 35)
To break this 2-node loop:
> [!IMPORTANT]
> **Poisoned Reverse Rule**:
> If node $z$ routes through node $y$ to reach destination $x$, node $z$ advertises to $y$ that its distance to $x$ is **infinity**:
> $$D_z(x) = \infty$$
> This explicitly prevents $y$ from ever falsely attempting to route to $x$ through $z$!

- **Limitation**: Poisoned Reverse solves loops involving 2 adjacent nodes. It does **NOT** prevent routing loops involving 3 or more nodes (e.g., loops spanning $A \to B \to C \to A$).

---

## 6. Hierarchical Routing & Autonomous Systems (AS) (Slides 36–42)

A flat network model cannot scale to the global Internet:
1. **Scale**: Storing hundreds of millions of destinations in router routing tables would require terabytes of memory; Dijkstra or Bellman-Ford computations would consume $100\%$ CPU.
2. **Administrative Autonomy**: Independent organizations (universities, corporations, ISPs) mandate the authority to configure and run their own internal networks independently without external interference.

### 6.1 Autonomous Systems (AS)
The global Internet is partitioned into **Autonomous Systems (ASes)**. An AS is a collection of routers under a single administrative authority running an internal routing protocol.

```
+------------------------------------+           +------------------------------------+
|          AUTONOMOUS SYSTEM 1       |           |          AUTONOMOUS SYSTEM 2       |
|                                    |           |                                    |
|   [ Router 1a ] --- [ Router 1b ]  |           |   [ Router 2a ] --- [ Router 2b ]  |
|         \                /         |           |         \                /         |
|          \              /          |           |          \              /          |
|       [ Gateway Router 1c ] <==== eBGP Peering ====> [ Gateway Router 2c ]          |
|                 ^                  |           |                 ^                  |
|                 | iBGP             |           |                 | iBGP             |
|                 v                  |           |                 v                  |
|       [ Internal Router 1d ]       |           |       [ Internal Router 2d ]       |
+------------------------------------+           +------------------------------------+
```

- **Intra-AS Routing (IGP - Interior Gateway Protocol)**: Directs routing between routers within the same AS. Focuses strictly on **performance and shortest path**.
- **Inter-AS Routing (EGP - Exterior Gateway Protocol)**: Directs routing between different ASes. Focuses strictly on **business policies and economic agreements**.

---

## 7. Intra-AS Protocols: OSPF vs. RIP (Slides 43–48)

### 7.1 Open Shortest Path First (OSPF, RFC 2328)
- **Algorithm**: Link-State algorithm using Dijkstra's shortest-path calculations.
- **Protocol Encapsulation**: Runs directly over **raw IP (Protocol 89)**, completely bypassing TCP and UDP.
- **Key Advanced Features**:
  - *Security*: All LSA exchanges are authenticated (HMAC-MD5 or SHA-256).
  - *Multi-Path Load Balancing*: Equal-Cost Multi-Path (ECMP) allows multiple paths with identical cost to share traffic.
  - *Hierarchical Areas*: Divides an AS into a **Backbone Area (Area 0)** and multiple peripheral local areas. Detailed topology is hidden within local areas, reducing LSA flooding overhead.

### 7.2 Routing Information Protocol (RIP, RFC 2453)
- **Algorithm**: Distance-Vector algorithm based on Bellman-Ford.
- **Metric**: Strictly **Hop Count** (cost of every link $= 1$). Maximum allowable hop count is **15**. A distance of **16 denotes infinity** (unreachable destination).
- **Protocol Encapsulation**: Runs over **UDP on port 520**.
- **Update Frequency**: Advertises complete distance vectors to neighbors every **30 seconds**.

---

## 8. Inter-AS Routing: Border Gateway Protocol (BGP-4) (Slides 49–65)

BGP-4 (RFC 4271) is the de facto standard inter-domain routing protocol of the global Internet.

### 8.1 Path-Vector Architecture
BGP is a **Path-Vector protocol** (a generalized distance vector protocol). Instead of advertising a mere numeric cost, BGP advertisements include the **complete sequence of Autonomous System Numbers (ASNs)** traversed to reach the destination prefix:
$$\text{AS-PATH} = [AS\ 64512, AS\ 1239, AS\ 7018]$$
- **Instant Loop Detection**: If a router receives a BGP advertisement containing its own ASN inside the `AS-PATH` attribute, it **immediately discards the route**, preventing inter-domain routing loops!

### 8.2 eBGP vs. iBGP
- **External BGP (eBGP)**: Runs over TCP (port 179) between two gateway routers belonging to **different** Autonomous Systems. Used to learn reachable destination prefixes from neighbor ASes.
- **Internal BGP (iBGP)**: Runs over TCP (port 179) between routers **within the same** Autonomous System to distribute externally learned eBGP prefix routes to all internal routers.

### 8.3 Policy-Based Routing Economics (Slides 58–62)
In inter-AS routing, commercial contracts dictate routing paths, completely overriding shortest-path metrics:
1. **Customer-Provider Relationship**: The customer pays the provider for Internet transit. A provider will happily route traffic to and from its paying customers.
2. **Peer-to-Peer Peering**: Two ISPs agree to exchange traffic between their own customers for free (**Settlement-Free Peering**). An ISP will NEVER transit traffic between two peering partners (refuses to carry transit traffic for free!).
3. **Hot-Potato Routing**: When multiple internal gateway routers can reach an external destination, the originating router dumps the packet onto the gateway router with the **least intra-AS cost**, pushing the packet out of its own network as fast as humanly possible!

---

## 9. Master Architectural Comparison Matrix

| Architectural Dimension | Link-State (OSPF) | Distance-Vector (RIP) | Path-Vector (BGP) |
| :--- | :--- | :--- | :--- |
| **Network Scope** | Intra-AS (Interior Gateway) | Intra-AS (Interior Gateway) | **Inter-AS (Exterior Gateway)** |
| **Underlying Algorithm**| Dijkstra's Shortest Path | Bellman-Ford Dynamic Prog. | Path Vector Protocol |
| **Information Shared** | Entire topology map via LSAs | Vector of costs to destinations | Prefix reachability + **AS-PATH** |
| **Communication Target**| Flooded to **ALL routers** in area | Sent **ONLY to direct neighbors**| Exchanged over TCP with BGP peers |
| **Transport Protocol** | Raw IP (Protocol 89) | UDP (Port 520) | **TCP (Port 179)** |
| **Convergence Speed** | Fast ($O(|V| \log |V|)$) | Slow (Count-to-Infinity) | Fast (Path-Vector loop filter) |
| **Routing Metric** | Configurable cost (bandwidth) | Hop count strictly ($\le 15$) | Policy, AS-PATH length, hot-potato |

---

## 10. High-Yield Open-Book Exam Traps & Examiner Tricks

1. **The RIP Infinity Metric Trap**:
   - *Question*: *"Why does RIP define 16 as infinity instead of a large number like 65,535?"*
   - *Fact*: To limit the duration of the **Count-to-Infinity** problem! If infinity were 65,535, a routing loop with 30-second updates would take weeks to resolve. With infinity set to 16, loops terminate in at most $16 \times 30\,\text{s} = 8\,\text{minutes}$.
2. **The OSPF Encapsulation Trap**:
   - *Question*: *"Does OSPF run over TCP or UDP?"*
   - *Fact*: **Neither!** OSPF implements its own reliable transport mechanisms and runs directly over **raw IP packets (Protocol 89)**.
3. **The BGP Shortest Path Myth**:
   - *Question*: *"Does BGP always choose the path with the fewest router hops or lowest latency?"*
   - *Fact*: **NO!** BGP enforces **commercial policy rules first**. A 10-hop free customer path is chosen over a 2-hop expensive provider transit path.

---

## 11. Solved High-Yield Numerical Exam Problems

### Problem 1: Dijkstra's Shortest Path Algorithm Step-by-Step
**Problem Statement**:
Consider the network topology with nodes $\{u, v, w, x, y, z\}$ and symmetric link costs:
- $c(u, v) = 2$, $c(u, w) = 5$, $c(u, x) = 1$
- $c(x, v) = 2$, $c(x, w) = 3$, $c(x, y) = 1$
- $c(v, w) = 3$, $c(v, y) = 1$
- $c(w, y) = 1$, $c(w, z) = 5$
- $c(y, z) = 2$
Use Dijkstra's algorithm to compute the shortest paths from source node $u$ to all other destinations. Show the complete execution table at each step.

**Step-by-Step Solution**:

Construct the tracking table:

| Step | $N'$ (Settled Set) | $D(v), p(v)$ | $D(w), p(w)$ | $D(x), p(x)$ | $D(y), p(y)$ | $D(z), p(z)$ | Selection Explanation |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **Init**| $\{u\}$ | $2, u$ | $5, u$ | $\mathbf{1, u}$ | $\infty$ | $\infty$ | Min is $x$ with cost 1 |
| **1** | $\{u, x\}$ | $2, u$ | $4, x$ | --- | $\mathbf{2, x}$ | $\infty$ | $D(w)=\min(5, 1+3)=4$; $D(y)=1+1=2$. Min is $v$ or $y$ (tie, pick $y$) |
| **2** | $\{u, x, y\}$ | $\mathbf{2, u}$ | $3, y$ | --- | --- | $4, y$ | $D(w)=\min(4, 2+1)=3$; $D(z)=2+2=4$. Min is $v$ with cost 2 |
| **3** | $\{u, x, y, v\}$ | --- | $\mathbf{3, y}$ | --- | --- | $4, y$ | $D(w)=\min(3, 2+3)=3$. Min is $w$ with cost 3 |
| **4** | $\{u, x, y, v, w\}$ | --- | --- | --- | --- | $\mathbf{4, y}$ | $D(z)=\min(4, 3+5)=4$. Min is $z$ with cost 4 |
| **5** | $\{u, x, y, v, w, z\}$ | --- | --- | --- | --- | --- | All nodes settled! |

#### Resulting Forwarding Table at Node $u$:
- Destination $x$: Next hop is **$x$** (Cost = 1).
- Destination $v$: Next hop is **$v$** (Cost = 2).
- Destination $y$: Path $u \to x \to y$, Next hop is **$x$** (Cost = 2).
- Destination $w$: Path $u \to x \to y \to w$, Next hop is **$x$** (Cost = 3).
- Destination $z$: Path $u \to x \to y \to z$, Next hop is **$x$** (Cost = 4).

---

### Problem 2: Bellman-Ford Distance Vector Convergence
**Problem Statement**:
Consider three directly connected nodes $X, Y, Z$:
$c(X, Y) = 2$, $c(Y, Z) = 1$, $c(X, Z) = 7$.
Compute the converged distance vectors $\mathbf{D}_X$, $\mathbf{D}_Y$, $\mathbf{D}_Z$ using the Bellman-Ford equation:
$$d_x(y) = \min_v \{ c(x, v) + d_v(y) \}$$

**Step-by-Step Solution**:

1. **Initial Distance Vectors (Local knowledge only)**:
   - $\mathbf{D}_X = [D_X(X)=0, D_X(Y)=2, D_X(Z)=7]$
   - $\mathbf{D}_Y = [D_Y(X)=2, D_Y(Y)=0, D_Y(Z)=1]$
   - $\mathbf{D}_Z = [D_Z(X)=7, D_Z(Y)=1, D_Z(Z)=0]$

2. **Iteration 1 (Nodes exchange initial vectors)**:
   - **Node $X$ recomputes distance to $Z$**:
     $$D_X(Z) = \min\Big( c(X, Y) + D_Y(Z),\ c(X, Z) + D_Z(Z) \Big) = \min(2 + 1, 7 + 0) = \min(3, 7) = \mathbf{3} \quad (\text{via } Y)$$
     $X$ updates its distance vector to: $\mathbf{D}_X = [0, 2, \mathbf{3}]$.
   - **Node $Z$ recomputes distance to $X$**:
     $$D_Z(X) = \min\Big( c(Z, Y) + D_Y(X),\ c(Z, X) + D_X(X) \Big) = \min(1 + 2, 7 + 0) = \min(3, 7) = \mathbf{3} \quad (\text{via } Y)$$
     $Z$ updates its distance vector to: $\mathbf{D}_Z = [\mathbf{3}, 1, 0]$.
   - Node $Y$ recomputes: no changes.

3. **Iteration 2 (Nodes broadcast updated vectors)**:
   - Nodes receive updated vectors; no distances decrease further.
   - **Network has converged in 2 iterations**!
   - Final Shortest Path from $X$ to $Z$ is via $Y$ with total cost $\mathbf{3}$.

---

## 12. Ultra-Fast Exam Revision Checklist
- [ ] Link-State (OSPF): Global algorithm; all routers know full topology; runs Dijkstra's algorithm ($O(|V|\log|V|)$).
- [ ] Distance-Vector (RIP): Decentralized algorithm; exchanges vectors with neighbors; Bellman-Ford: $d_x(y) = \min_v [c(x,v) + d_v(y)]$.
- [ ] Count-to-Infinity: Caused by routing loops during link cost increases; mitigated by Poisoned Reverse ($D_z(x) = \infty$).
- [ ] OSPF features: Runs directly over IP (Protocol 89), supports MD5 authentication, ECMP, and hierarchical Area 0.
- [ ] RIP limits: Max hop count is 15 (16 is infinity); updates every 30s over UDP 520.
- [ ] BGP is a Path-Vector inter-AS routing protocol; includes `AS-PATH` attribute to eliminate loops immediately.
- [ ] eBGP connects gateway routers of different ASes; iBGP distributes routes internally within the same AS over TCP port 179.
- [ ] Hot-Potato Routing: Transmits packets to the exit gateway router with the lowest intra-AS cost.
