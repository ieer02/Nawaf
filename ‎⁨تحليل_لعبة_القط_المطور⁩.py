
import streamlit as st
import pandas as pd

st.set_page_config(page_title="محلل لعبة القط", layout="centered")

st.title("🎯 أداة تحليل لعبة القط")

# Session state to store history
if "history" not in st.session_state:
    st.session_state.history = []

# --- إدخال الرموز ---
st.markdown("### 📥 أدخل نتائج الجولة")
cols = st.columns(5)
symbols_list = ["🍅", "🥕", "🐟", "🌽", "🦐"]
selected_symbols = []

for i, col in enumerate(cols):
    selected = col.selectbox(f"رمز {i+1}", [""] + symbols_list, key=f"symbol_{i}")
    if selected:
        selected_symbols.append(selected)

# أيضاً مدخل نصي للي يفضل يكتب الرموز
user_input = st.text_input("أو أدخل الرموز يدوياً (مثال: 🍅 🥕 🐟):")
if user_input:
    selected_symbols = user_input.strip().split()

if selected_symbols:
    st.markdown("### ✅ الرموز المدخلة:")
    st.write(" ".join(selected_symbols))

    # --- التحليل ---
    counts = pd.Series(selected_symbols).value_counts()
    total = counts.sum()

    df = pd.DataFrame({
        "الرمز": counts.index,
        "عدد التكرار": counts.values,
        "الاحتمال (%)": [round(v / total * 100, 2) for v in counts.values]
    })

    st.subheader("📊 تحليل الرموز:")
    st.dataframe(df, use_container_width=True)

    top_symbol = df.iloc[0]["الرمز"]
    st.markdown(f"🔸 **الرمز الأقوى حاليًا:** {top_symbol}")

    # --- التوصيات ---
    safe_strategy = {
        "🍅": 0.6, "🥕": 0.3, "🐟": 0.1, "🌽": 0.0, "🦐": 0.0
    }
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

    # --- التنبؤ ---
    st.subheader("🔮 التوقع بناءً على البيانات:")
    st.markdown("نسبة ظهور كل رمز تساعد على توقع النتيجة القادمة.")

    prediction = df[df["الاحتمال (%)"] == df["الاحتمال (%)"].max()]
    st.markdown(f"📌 **الأكثر احتمالاً للفوز في الجولة القادمة:** {prediction.iloc[0]['الرمز']}")

    # --- حفظ التاريخ ---
    st.session_state.history.append(" ".join(selected_symbols))

# --- عرض التاريخ الكامل ---
if st.session_state.history:
    st.subheader("🕘 سجل الجولات السابقة:")
    st.write(st.session_state.history)
