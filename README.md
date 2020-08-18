## CNN-Based Resource Allocation for Energy-Efficient D2D Communications
In this thesis, we introduce the application of Device-to-Device (D2D) communication into the scenario of massive Machine Type Communication (mMTC). More specifically speaking, we formulate the joint channel allocation and power control problem aiming at maximizing the system energy efficiency under the constraints of minimum rate requirements and power budget limitations of cellular users and D2D pairs. However, the formulated resource allocation problem is NP-hard, which is difficult to obtain the optimal solution directly. To solve the problem efficiently, we propose an iterative algorithm that utilizes convex approximation techniques to approximate the original problem as a geometric programming problem. In each iteration, we solve the approximated problem by some off-the-shelf optimization tools (e.g., CVX) to maximize the system energy efficiency progressively. Based on the sub-optimal resource allocation results, a convolutional neural network (CNN) with spatial pyramid pooling layer is constructed to obtain the decisions on resource allocation to reduce the computational time. The simulation results demonstrate that the proposed CNN outperforms the other neural networks in terms of system energy efficiency and system sum rate, and even achieves similar performance as the iterative algorithm with ultra-low CPU runtime.
