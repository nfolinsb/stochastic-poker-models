import streamlit as st
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

st.set_page_config(page_title="Multi-Stake Poker Model", layout="centered")

st.title("Multi-Stake Poker Model")
st.write("Interactive tool to compute expected value, variance, Sharpe ratio, "
         "and confidence intervals when playing hands across multiple stakes.")

# ---- Input Section ----
st.header("Input Parameters")

col1, col2 = st.columns(2)

with col1:
    stake_bb_value = st.text_input("Stake big blind values ($)", "2,5,10")
    winrates_100 = st.text_input("Winrates (bb per 100 hands)", "5,5,5")
    conf_int = st.text_input("Condifence intervals to be returned (%)", "50,75,90,95")

with col2:
    n_hands = st.text_input("Number of hands at each stake", "100000,100000,100000")
    sd_100 = st.text_input("Standard deviations (bb per 100 hands)", "100,100,100")



# Convert inputs to arrays
try:
    stake_bb_value = np.array(list(map(float, stake_bb_value.split(","))))
    n_hands = np.array(list(map(int, n_hands.split(","))))
    winrates_100 = np.array(list(map(float, winrates_100.split(","))))
    sd_100 = np.array(list(map(float, sd_100.split(","))))
    conf_int = np.array(list(map(float, conf_int.split(","))))*0.01
except:
    st.error("❌ Invalid input format. Please use comma-separated numbers.")
    st.stop()


# ---- Validation ----
if not (len(stake_bb_value) == len(n_hands) == len(winrates_100) == len(sd_100)):
    st.error("❌ All input lists must have the same length.")
    st.stop()

for c in conf_int:
    if c < 0 or c > 1:
        st.error("❌ The inputs for the confidence interval must be between 0 and 100.")
        st.stop()


# ---- Computation ----
sd = sd_100 * 0.1
winrates = winrates_100 * 0.01

stake_mean = n_hands * stake_bb_value * winrates
total_mean = np.sum(stake_mean)

stake_sigma = np.sqrt(n_hands) * stake_bb_value * sd
total_sigma = np.sqrt(np.sum(stake_sigma**2))

mu, sigma = total_mean, total_sigma


# ---- Results Section ----
st.header("Results")

colA, colB, colC = st.columns(3)
colA.metric("EV ($)", f"{total_mean:.2f}")
colB.metric("Standard Deviation on Winnings ($)", f"{total_sigma:.2f}")
colC.metric("Sharpe Ratio", f"{total_mean/total_sigma:.2f}")


st.subheader("Confidence Intervals")
for c in conf_int:
    lower = mu - norm.ppf((c+1)/2)*sigma
    upper = mu + norm.ppf((c+1)/2)*sigma
    st.write(f"**{100*c}% CI:** [{lower:.2f}, {upper:.2f}]")


# ---- Plot ----
st.header("Distribution of Winnings")

fig, ax = plt.subplots(figsize=(8, 4))

x = np.linspace(mu - 3*sigma, mu + 3*sigma, 400)
y = norm.pdf(x, mu, sigma)

ax.plot(x, y, "k", linewidth=2)
ax.set_xlabel("Winnings ($)")
ax.set_ylabel("Probability Density")
ax.set_title(f"Expected Distribution After {int(sum(n_hands)):,} Hands")
ax.grid(True, alpha=0.3)

st.pyplot(fig)

def simulate_run(stakes, wrs, sds, hands):
    total_sample = []

    for i, stake in enumerate(stakes):
        if hands[i] > 0:
            stake_sim = np.random.normal(wrs[i], sds[i], size=hands[i])
            stake_sim = stake * stake_sim
            total_sample.append(stake_sim)

    total_sample = np.concatenate(total_sample)
    np.random.shuffle(total_sample)

    return np.cumsum(total_sample)

# -------------------------
# Simulated Runs Plot
# -------------------------
#st.subheader("Simulated Runs")

#fig2, ax2 = plt.subplots(figsize=(12, 6))

runs = 10
def simulate(runs):
    for _ in range(runs):
        run = simulate_run(
            stakes=stake_bb_value,
            wrs=winrates,
            sds=sd,
            hands=n_hands,
        )
        ax2.plot(run, alpha=0.6)

    ax2.axhline(0, color="black", linewidth=1)
    ax2.set_title(f"{runs} Simulated Runs ({n_hands.sum():,} Hands)")
    ax2.set_xlabel("Hands")
    ax2.set_ylabel("Cumulative Winnings ($)")
    ax2.grid(True)

    st.pyplot(fig2)

url = "https://github.com/nfolinsb/stochastic-poker-models/blob/main/stochastic_poker_models.ipynb"
st.info("Edit the inputs above to instantly update the model. Code and explantation "
        "of the math behind the model, along with other models, can be found [here](%s)." %url)