


<!-- <p align="center" background-color='red' width="100%">
    <img width="33%" src="https://www.qmr.ai/wp-content/uploads/2022/03/qmr_logo.png">
</p> -->

# qmrExchange

## qmrExchange Overview
The qmrExchange project is an open-source financial markets exchange simulator that realistically mimics all the main components of modern trading venues. It allows us to test and quantify the behavior of different agents in a laboratory and isolated environment without the high noise-to-signal ratio that is otherwise unavoidable in live settings.
By creating a completely functioning trading venue whose access is only granted to a finite and known number of agents or trading algorithms, qmrExchange enables analyzing causation and quantifying the impact of each agent in a way that is otherwise unfeasible.


## Use cases for qmrExchange
The implementation of qmrExchange closely resembles the backend of most FIFO trading exchanges and replicates the market microstructure of the most popular venues. As a consequence, the system is especially useful for:
- Teaching, studying, and researching topics related to market microstructure and algorithmic trading.
- Estimating the impact of new regulations and how they affect each type of agent
- Implementing and analyzing market-making and high-frequency trading algorithms
-	Creating algorithmic trading challenges and tournaments both for university students and industry professionals alike


## Potential Research Topics with qmrExchange
Due to its precise resemblance to real-life trading venues, qmrExchange is perfectly suited for researching plenty of topics, such as:
### Market-Making Algorithms
By implementing a finite number of market participants, such as institutional investors and indicator-based trading algorithms, market-making algorithms can be studied. For a rigorous implementation, refer to Avellaneda & Stoikov (2008)
### Optimal Execution Algorithms
qmrExchange is an ideal environment for implementing, testing, and quantifying the market impact of different execution algorithms. By creating a laboratory, sterile and isolated venue whose market participants and their behavior is known with absolute certainty, optimal execution algorithms can be easily implemented, researched, and calibrated. For a formal presentation of such an algorithm, refer to Almgren & Chriss (1999).
### Adversarial Algorithms
Much like in the spirit of General Adversarial Networks and Game Theory, an implementation where a profit-maximizing agent’s behavior is calibrated based on the predefined behavior of other market participants is possible. For an interesting introduction to game theory applied to financial markets, refer to Allen & Morris (2022).
