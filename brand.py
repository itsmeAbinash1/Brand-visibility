import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sqlite3

# Connect Database
conn = sqlite3.connect("brand_visibility.db")

df = pd.read_sql(
    "SELECT * FROM products",
    conn
)
conn.close()
st.write()

# HEADER
st.markdown("""
<h1 style='text-align:center;color:#2563EB;'>
📊 Brand Visibility Dashboard
</h1>
""", unsafe_allow_html=True)

#PAGE CONFIGURATION

st.set_page_config(
    page_title="Brand Visibility Dashboard",
    page_icon="📊",
    layout="wide"
)

# SIDEBAR 
# ─────────────────────────────────────────
with st.sidebar:
    st.title("📊 Filters")
    st.divider()

    from datetime import datetime
    st.caption(
    f"Last Updated: {datetime.now().strftime('%d %b %Y %H:%M')}")


#css
    st.markdown("""
<style>
[data-testid="stSidebar"] {
    background-color: #97a8ac;
}
</style>
""", unsafe_allow_html=True)

    keyword = st.selectbox(
        "🔑 Keyword",
        ["All Keywords"] + sorted(df["keyword"].dropna().unique().tolist())
    )

    brand = st.selectbox(
        "🏷 Brand",
        ["All Brands"] + sorted(df["brand"].dropna().unique().tolist())
    )

    platform = st.selectbox(
        "🛒 Platform",
        ["All Platforms"] + sorted(df["platform"].dropna().unique().tolist())
    )

    price_range = st.slider(
        "💰 Price Range",
        min_value=int(df["price"].min()),
        max_value=int(df["price"].max()),
        value=(int(df["price"].min()), int(df["price"].max()))
    )

    rating_range = st.slider(
        "⭐ Rating Range",
        min_value=float(df["rating"].min()),
        max_value=float(df["rating"].max()),
        value=(float(df["rating"].min()), float(df["rating"].max())),
        step=0.1
    )

    position_range = st.slider(
        "🏆 Position (Ranking)",
        min_value=int(df["position"].min()),
        max_value=int(df["position"].max()),
        value=(int(df["position"].min()), int(df["position"].max()))
    )


# APPLY FILTERS
filtered_df = df.copy()

if keyword != "All Keywords":
    filtered_df = filtered_df[filtered_df["keyword"] == keyword]

if brand != "All Brands":
    filtered_df = filtered_df[filtered_df["brand"] == brand]

if platform != "All Platforms":
    filtered_df = filtered_df[filtered_df["platform"] == platform]

filtered_df = filtered_df[
    (filtered_df["price"].between(price_range[0], price_range[1])) &
    (filtered_df["rating"].between(rating_range[0], rating_range[1])) &
    (filtered_df["position"].between(position_range[0], position_range[1]))
]
#styling the tabs

st.markdown("""
<style>

/* =========================
   SIDEBAR
========================= */

[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #1E3A8A 0%,
        #2563EB 50%,
        #0F766E 100%
    );
}

[data-testid="stSidebar"] * {
    color: black;
}

[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stSlider label {
    color: white !important;
    font-weight: 600;
}

/* =========================
   TABS
========================= */

.stTabs [data-baseweb="tab-list"] {
    gap: 10px;
}

.stTabs [data-baseweb="tab"] {
    height: 60px;
    border-radius: 12px 12px 0 0;
    padding: 10px 20px;
    font-size: 16px;
    font-weight: 500;
    background-color: #F1F5F9;
    color: #334155;
}

.stTabs [aria-selected="true"] {
    background-color: #2563EB !important;
    color: white !important;
}

/* =========================
   KPI CARDS
========================= */

[data-testid="metric-container"] {
    background-color: white;
    border-radius: 10px;
    padding: 10px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
    border-top: 4px solid #2563EB;
}

/* =========================
   MAIN PAGE
========================= */

.main {
    background-color: #F8FAFC;
}

h1 {
    color: #2563EB;
}

</style>
""", unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📋 OVERVIEW",
    "🏷️ BRAND INSIGHTS",
    "💰 PRICING ANALYSIS",
    "🖥️ PLATFORM ANALYSIS",
    "📊 VISIBILITY & RANKING",
    "🔍 PRODUCT EXPLORER"
])
st.sidebar.write("Rows After Filter:", len(filtered_df))

#Overview KPIs*************************************************************

st.markdown("""
<style>

/* KPI Metric Cards */
div[data-testid="stMetric"] {
    background-color: #ffffff;
    border: 1px solid #e5e7eb;
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.08);
}

/* Metric Label */
div[data-testid="stMetricLabel"] {
    font-size: 16px;
    font-weight: 600;
}

/* Metric Value */
div[data-testid="stMetricValue"] {
    font-size: 28px;
    font-weight: bold;
    color: #2563EB;
}

</style>
""", unsafe_allow_html=True)

#KPI CARDS.

with tab1:

    st.header("📊 Overview")
    st.divider()

    total_products = len(filtered_df)

    avg_price = round(
        filtered_df["price"].mean(), 2
    )

    avg_rating = round(
        filtered_df["rating"].mean(), 2
    )

    total_reviews = int(
        filtered_df["reviews"].sum()
    )

    total_platforms = filtered_df["platform"].nunique()

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric(
        "🛍️Total Products",
        f"{total_products:,}"
    )

    col2.metric(
        "💲Avg Price",
        f"${avg_price:,.2f}"
    )

    col3.metric(
        "⭐️Avg Rating",
        avg_rating
    )

    col4.metric(
        "💬Total Reviews",
        f"{total_reviews:,}"
    )

    col5.metric(
        "🖥️Platforms",
        total_platforms
    )

    st.divider()


    #Chart 1: Price Distribution (Histogram).
    import plotly.express as px

    st.subheader("💰 Price Distribution")

    fig = px.histogram(
        filtered_df,
        x="price",
        nbins=25,
        title="Price Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    #Chart 2: Products per Keyword (Bar Chart)

    st.subheader("🔑 Products per Keyword")

    keyword_count = (
        filtered_df["keyword"]
        .value_counts()
        .reset_index()
    )

    keyword_count.columns = [
        "Keyword",
        "Count"
    ]

    fig = px.bar(
        keyword_count,
        x="Keyword",
        y="Count",
        text="Count",
        title="Products per Keyword"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    #Chart 3: Platform Share (Pie Chart)
    st.subheader("🛒 Platform Share")

    platform_count = (
        filtered_df["platform"]
        .value_counts()
        .reset_index()
    )

    platform_count.columns = [
        "Platform",
        "Count"
    ]

    fig = px.pie(
        platform_count,
        names="Platform",
        values="Count",
        title="Platform Share"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )
#Brand Insights KPIs*************************************************************

with tab2:
    st.header("🏷️ Brand Insights")
    st.divider()

    top_brand = filtered_df["brand"].value_counts().idxmax()

    avg_visibility = round(
        filtered_df["visibility_score"].mean(),
        2
    )

    col1, col2 = st.columns(2)

    col1.metric(
        "Top Brand",
        top_brand
    )

    col2.metric(
        "Avg Visibility Score",
        avg_visibility
    )

    st.divider()

# chart1 = Brand vs Product Count

    st.subheader("Brand vs Product Count")

    brand_count = (
        filtered_df["brand"]
        .value_counts()
        .head(15)
        .reset_index()
    )

    brand_count.columns = [
        "Brand",
        "Product Count"
    ]

    fig = px.bar(
        brand_count,
        x="Brand",
        y="Product Count",
        text="Product Count",
        title="Top Brands by Product Count"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )
    #chart 2 = Brand vs Average Rating
    st.subheader("Brand vs Average Rating")

    brand_rating = (
        filtered_df
        .groupby("brand")["rating"]
        .mean()
        .sort_values(ascending=False)
        .head(15)
        .reset_index()
    )

    brand_rating.columns = [
        "Brand",
        "Average Rating"
    ]

    fig = px.bar(
        brand_rating,
        x="Brand",
        y="Average Rating",
        text="Average Rating",
        title="Top Rated Brands"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )
    #Top Brands in Top 10 Positions
    st.subheader("Top Brands in Top 10 Positions")

    top10 = filtered_df[
        filtered_df["position"] <= 10
    ]
    top10_brand = (
        top10["brand"]
        .value_counts()
        .head(15)
        .reset_index()
    )

    top10_brand.columns = [
        "Brand",
        "Count"
    ]
    fig = px.bar(
        top10_brand,
        x="Brand",
        y="Count",
        text="Count",
        title="Brands Appearing Most in Top 10 Positions"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )    


#-3-Pricing Analysis KPIs***************************************************************
with tab3:

    st.header("💰 Pricing Analysis")
    st.divider()

    avg_price = round(
        filtered_df["price"].mean(),
        2
    )

    max_price = round(
        filtered_df["price"].max(),
        2
    )
    discount_percent = "N/A"
    col1, col2, col3 = st.columns(3)

    col1.metric(
     "Avg Price",
     f"${avg_price:,.2f}"
    )

    col2.metric(
        "Max Price",
        f"${max_price:,.2f}"
    )

    col3.metric(
         "% Discounted Products",
         discount_percent
    )   

    st.divider()

    #PRICE DISTRIBUTION CHART.
    price_category = (
        filtered_df["price_category"]
        .value_counts()
        .reset_index()
    )

    price_category.columns = [
        "Category",
        "Count"
    ]

    fig = px.pie(
        price_category,
        names="Category",
        values="Count",
        title="Price Category Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )
    #PRICE VS RANKING (SCATTER PLOT)
    st.subheader("Price vs Ranking")

    fig = px.scatter(
        filtered_df,
        x="price",
        y="position",
        color="brand",
        hover_data=["product_name"],
        title="Price vs Ranking Position"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    #PRICE VS RATING .
    st.subheader("Price vs Rating")

    fig = px.scatter(
        filtered_df,
        x="price",
        y="rating",
        color="brand",
        hover_data=["product_name"],
        title="Price vs Rating"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )
#Platform Analysis KPIs*************************************************

with tab4:
    st.header("🛒 Platform Analysis")
    st.divider()

    total_platforms = filtered_df["platform"].nunique()

    top_platform = (
        filtered_df["platform"]
        .value_counts()
        .idxmax()
    )

    col1, col2 = st.columns(2)

    col1.metric(
        "Total Platforms",
        total_platforms
    )

    col2.metric(
        "Best Platform",
        top_platform
    )
    st.divider()

    #PLATFORM VS PRODUCT COUNT .
    st.subheader("Platform vs Product Count")

    platform_count = (
        filtered_df["platform"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    platform_count.columns = [
        "Platform",
        "Product Count"
    ]

    fig = px.bar(
        platform_count,
        x="Platform",
        y="Product Count",
        text="Product Count",
        title="Top Platforms by Product Count"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    #PLATFORM VS AVERAGE PRICE.
    st.subheader("Platform vs Average Price")

    platform_price = (
        filtered_df
        .groupby("platform")["price"]
        .mean()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    platform_price["price"] = (
        platform_price["price"]
        .round(2)
    )

    fig = px.bar(
        platform_price,
        x="platform",
        y="price",
        text="price",
        title="Average Price by Platform"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    #PLATFPRM VS AVERAGE RATING.
    st.subheader("Platform vs Average Rating")

    platform_rating = (
        filtered_df
        .groupby("platform")["rating"]
        .mean()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    platform_rating["rating"] = (
        platform_rating["rating"]
        .round(2)
    )

    fig = px.bar(
        platform_rating,
        x="platform",
        y="rating",
        text="rating",
        title="Average Rating by Platform"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

#Visibility & Ranking KPIs*******************************************

with tab5:
    st.header("🔝 Visibility & Ranking")
    st.divider()

    #avg postion .
    avg_position = round(
       filtered_df["position"].mean(),2
    )
    #AVG VISIBILITY SCORE.
    avg_visibility = round(
       filtered_df["visibility_score"].mean(),2
    )
    col1, col2 = st.columns(2)

    col1.metric(
    "Avg Position",
    avg_position
    )

    col2.metric(
         "Avg Visibility Score",
        avg_visibility
    )

    st.divider()

    #Chart 1: Ranking Distribution(Shows how products distributed across ranking positions.)
    st.subheader("Ranking Distribution(histogram)")

    fig = px.histogram(
        filtered_df,
        x="position",
        nbins=20,
        title="Ranking Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    #Chart 2: Rating vs Ranking(Shows whether highly rated products rank better).
    st.subheader("Rating vs Ranking(scatter plot)")

    fig = px.scatter(
        filtered_df,
        x="rating",
        y="position",
        hover_data=["brand", "product_name"],
        title="Rating vs Ranking"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )
    #CHART 3:  Reviews vs Ranking (Bubble Chart)
    fig = px.scatter(
    filtered_df,
    x="reviews",
    y="position",
    size="rating",
    hover_data=["brand", "product_name"],
    title="Reviews vs Ranking"
    )

    fig.update_layout(
    template="plotly_white",
    title_x=0.5,
    plot_bgcolor="white",
    paper_bgcolor="white"
    )

    fig.update_traces(
    marker=dict(
        sizemode="area",
        line=dict(width=1)
    )
    )
    st.plotly_chart(
    fig,
    use_container_width=True
    )

with tab6:

    st.header("🔍 Product Explorer")

    # Search Box
    search_product = st.text_input(
        "Search Product Title"
    )

    explorer_df = filtered_df.copy()

    if search_product:
        explorer_df = explorer_df[
            explorer_df["product_name"]
            .str.contains(
                search_product,
                case=False,
                na=False
            )
        ]

    st.divider()

    st.subheader("Products")

    display_columns = [
        "product_name",
        "brand",
        "price",
        "rating",
        "reviews",
        "platform",
        "position"
    ]

    # Add discount column only if present
    if "discount" in explorer_df.columns:
        display_columns.append("discount")

    st.dataframe(
        explorer_df[display_columns],
        use_container_width=True,
        hide_index=True
    )

# Download CSV Button.
st.download_button(
    label="📥 Download Products CSV",
    data=explorer_df.to_csv(index=False),
    file_name="products.csv",
    mime="text/csv"
)