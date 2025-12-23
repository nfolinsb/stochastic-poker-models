# Stochastic poker models
Python models of the distribution of winning in poker games. These were created to have greater clarity on the tradeoff between EV and variance and to help with stuff like deciding which stakes and how much volume to play. They are inspired by the [Primedope variance calculator](https://www.primedope.com/poker-variance-calculator/), but support the ability to simulate hands at multiple stakes, simulate a bad beat jackpot (BBJ) and simulate movement between stakes, which is highly relevant in today's games.

### Update 17/12/2025
I've created an interactive web app for the multi-stake model using Streamlit. It is currently hosted [here](https://multi-stake-poker-model.streamlit.app/).

### Update 23/12/2025
The speed of the BBJ model has been improved considerably and is now practically instant. This was done by using a Poisson distribution to simulate the BBJ results, rather than simulating individual hands. The model allowing movement between stakes remains quite slow, but I added a mention about a means to improve it by batching certain computations. It could possibly be improved further by using some results from Stochastic calculus.