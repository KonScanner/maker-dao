import streamlit as st
from utils.utils import get_maker_dao, hide_streamlit_style, plot_vlines_mkr
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


st.set_page_config(
    page_title="DAI on the Market", page_icon="./img/mkr.png", layout="wide"
)
st.markdown("# [DAI on the Market]()", unsafe_allow_html=True)


st.markdown(hide_streamlit_style, unsafe_allow_html=True)
st.markdown(
    """
    In this investigation we'll be looking at how the amount of `DAI` in the market
    has changed over the past 365 days from the current date. We'll be looking at
    wether or not these events have some correlation to the Increase/Decrease of the
    [Stability Fee](https://makerdao.world/en/learn/vaults/stability-fees/#:~:text=Stability%20Fees%20are%20a%20Risk,associated%20with%20maintaining%20the%20protocol.)
    or the reason behind Burning or Minting `DAI` is different.
    """
)
st.markdown(
    """
    All data are aggregated/obtained from [FlipsideCrypto](https://flipsidecrypto.xyz/).
    """
)

st.markdown(
    """
    ## DAI on the Market
    """
)
st.markdown(
    """
    First we'll be looking at the amount of `DAI` in the market, minted/burned and their difference
    over the past 365 days (from current date). Also noted on all the charts are the stability fee
    amount change dates.
    """
)

option = "daily"
option = st.selectbox("View:", ("daily", "weekly", "monthly"), index=0)


@st.cache(suppress_st_warning=True)
def load_data():
    data = get_maker_dao(trunc_date="daily", normal_df=True)
    data2 = get_maker_dao(trunc_date=option, normal_df=True)
    return data, data2


(daily_data, full_data) = load_data()

fig_cols = st.columns(2)
with fig_cols[0]:
    # st.markdown("### Second Chart Title")
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Scatter(x=full_data["Date"], y=full_data["Num_minted"], name="DAI Minted"),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(x=full_data["Date"], y=full_data["Num_repaid"], name="DAI Repaid"),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(
            x=full_data["Date"],
            y=full_data["Diff_mint_repay"],
            name="DAI Minted - Repaid",
        ),
        secondary_y=False,
    )

    fig.update_layout(title_text=f"DAI on the Market | {option.capitalize()}")
    fig.update_xaxes(title_text="Date")
    fig.update_yaxes(title_text="Amount (DAI)", secondary_y=False)
    plot_vlines_mkr(fig)
    fig.update_layout(autosize=True, width=800, height=600)
    st.write(fig)

with fig_cols[1]:
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Scatter(
            x=full_data["Date"],
            y=full_data["Diff_mint_repay"],
            name="DAI Minted - Repaid",
        ),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(
            x=full_data["Date"], y=full_data["Eth_price"], name="ETH Average Price"
        ),
        secondary_y=True,
    )

    fig.update_layout(
        title_text=f"ETH (WETH) Average Price  vs Difference between Mint and Repay | {option.capitalize()}"
    )
    fig.update_xaxes(title_text="Date")
    fig.update_yaxes(title_text="Amount (DAI)", secondary_y=False)
    fig.update_yaxes(title_text="Amount ($)", secondary_y=True)
    plot_vlines_mkr(fig)
    fig.update_layout(autosize=True, width=800, height=600)
    st.write(fig)

st.markdown(
    """
    Other than this massive spike that lasted for about 1.5-2 months, the amount of `DAI` in the market, at least in terms
    of the difference between the amount burned and minted, has been on stable/slight decrease over the past year. What we can also
    see, is that a lot of these huge mint spikes are also followed by almost equivalent amounts in burns. In fact there's more
    burning in these spikes than minting (for the majority of them).
    
    As `ETH` price soared in the previous bull run the `DAI` minting also found an all time high, regardless of the Stability fee
    increase. We can also see a huge spike down on may 11th which follows the collapse of `UST` and fears of hardcore regulation
    on stablecoins. 
    """
)

st.markdown(
    """
        <hr>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    f"""
    ## DAI Minted/Burned vs `DAI` Price
    """
)
st.markdown(
    """
    Let's now look at specifically minting and burning and the impact it has had on the price of `DAI`.
    """
)

fig_cols2 = st.columns(2)
with fig_cols2[0]:
    # st.markdown("### Second Chart Title")
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Scatter(
            x=daily_data["Date"],
            y=daily_data["Num_minted"],
            name="DAI Minted",
        ),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(
            x=daily_data["Date"], y=daily_data["Dai_price"], name="DAI Average Price"
        ),
        secondary_y=True,
    )

    fig.update_layout(title_text=f"DAI Minted vs DAI price | Daily")
    fig.update_xaxes(title_text="Date")
    fig.update_yaxes(title_text="Amount (DAI)", secondary_y=False)
    fig.update_yaxes(title_text="Amount ($)", secondary_y=True)
    plot_vlines_mkr(fig)
    fig.update_layout(autosize=True, width=800, height=600)
    st.write(fig)

with fig_cols2[1]:
    # st.markdown("### Second Chart Title")
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Scatter(
            x=daily_data["Date"],
            y=daily_data["Num_repaid"],
            name="DAI Burned/Repaid",
        ),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(
            x=daily_data["Date"], y=daily_data["Dai_price"], name="DAI Average Price"
        ),
        secondary_y=True,
    )

    fig.update_layout(title_text=f"DAI Repaid vs DAI price | Daily")
    fig.update_xaxes(title_text="Date")
    fig.update_yaxes(title_text="Amount (DAI)", secondary_y=False)
    fig.update_yaxes(title_text="Amount ($)", secondary_y=True)
    plot_vlines_mkr(fig)
    fig.update_layout(autosize=True, width=800, height=600)
    st.write(fig)

st.markdown(
    """
    What we can see, is that when a lot of minting occured around that massive spike, price infact went bellow peg, which is
    counter intuitive (in my opition) as I would think green button (buy) -> price go up. On the contrary what we can also see
    is that when there was a lot of burning of `DAI` recently, post the `UST` collapse, `DAI` went above peg. With these few datapoints
    in mind, we can draw the conclusion that with massive burns, price spikes (less supply) and massive minting, price drops (more supply).
    Now the above **actually** makes sense, and is how it should work. Bravo to `MKR` for not being like `UST`.
    """
)

st.markdown(
    """
    ### A different view
    """
)
st.markdown("Let's now look at the amount of `DAI` minted and burned vs `DAI` price.")

st.markdown(
    """
        <iframe loading="lazy" src="https://velocity-app.flipsidecrypto.com/velocity/visuals/3ce232d2-3350-4539-8902-6cae1456fdbd/43fa7dee-c660-463b-8434-169c686584c9" width="100%" height="600"></iframe>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    What we can see is a better view of the difference in Minted - Burned `DAI` and how it affects the peg.
    """
)

st.markdown(
    """
    ### Summary
    """
)
st.markdown(
    """
    In summary, what we have found out in the following, is that the contributions of how the Stability Fee has not varied minting/burning of `DAI` by much.  
    We've seen that as we were nearing the top of the bull run there was more and more interest for burning/minting of `DAI`. The fact that they seem to average
    each other out, seems to indicate that there was a lot of trading back and fourth (`ETH`<->`DAI`). We also observed that `DAI` minting causes the price/peg to go down,
    and `DAI` burning causes the price/peg to go up, which is expected.
    """
)
