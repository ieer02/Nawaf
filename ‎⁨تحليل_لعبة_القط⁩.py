
import streamlit as st
import pandas as pd

st.set_page_config(page_title="محلل لعبة القط", layout="centered")

st.title("🎯 أداة تحليل لعبة القط")
st.markdown("أدخل نتائج الجولة مثل: 🍅 🥕 🍅 🐟 🌽")

user_input = st.text_input("📥 أدخل الرموز هنا:")

if user_input:
    symbols = user_input.strip().split()
    counts = pd.Series(symbols).value_counts()
    total = counts.sum()

    df = pd.DataFrame({
        "الرمز": counts.index,
        "عدد التكرار": counts.values,
        "الاحتمال (%)": [round(v / total * 100, 2) for v in counts.values]
    })

    st.subheader("📊 تحليل الرموز:")
    st.dataframe(df, use_container_width=True)

    st.subheader("🎯 التوصيات:")
    top_symbol = df.iloc[0]["الرمز"]
    st.markdown(f"🔸 **الرمز الأقوى حاليًا:** {top_symbol}")

    # استراتيجية آمنة
    safe_strategy = {
        "🍅": 0.6, "🥕": 0.3, "🐟": 0.1, "🌽": 0.0, "🦐": 0.0
    }

    # استراتيجية مخاطرة
    risky_strategy = {
        "🍅": 0.4, "🥕": 0.25, "🐟": 0.15, "🌽": 0.1, "🦐": 0.1
    }

    wager = st.number_input("💰 أدخل مبلغ الرهان (مثلاً 4000):", min_value=1, step=100)
    if wager:
        st.markdown("### 🔐 توزيع الرهان (آمن):")
        for sym, pct in safe_strategy.items():
            st.write(f"{sym}: {int(wager * pct)}")

        st.markdown("### ⚡ توزيع الرهان (مخاطرة):")
        for sym, pct in risky_strategy.items():
            st.write(f"{sym}: {int(wager * pct)}")
