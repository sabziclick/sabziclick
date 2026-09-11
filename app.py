import streamlit as st
import urllib.parse

# Page layout & styling
st.set_page_config(page_title="Sabziclick", page_icon="🥦", layout="centered")

# Custom CSS for App-like Colorful Look
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button {
        background-color: #2e7d32 !important;
        color: white !important;
        font-weight: bold !important;
        border-radius: 8px !important;
        padding: 10px 20px !important;
        border: none !important;
        width: 100%;
    }
    .card {
        background-color: white;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 12px;
        border-left: 5px solid #2e7d32;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize Session Data
if "vendors" not in st.session_state:
    st.session_state.vendors = {
        "Mohfeez sabzi": {
            "phone": "919876543210",
            "items": {
                "Phool kobi": {"price": 50.0, "unit": "kg"},
                "Tamator": {"price": 30.0, "unit": "kg"}
            }
        }
    }

st.markdown("<h1 style='text-align: center; color: #2e7d32;'>🥦 Sabziclick</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-weight: bold;'>किशनगंज ताज़ा ऑनलाइन सब्जी मंडी</p>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["🛒 ग्राहक दुकान (Buy)", "🏪 दुकानदार पोर्टल (Vendor)"])

# ---------------------------------------------------------
# TAB 1: CUSTOMER VIEW
# ---------------------------------------------------------
with tab1:
    if not st.session_state.vendors:
        st.info("अभी कोई दुकान उपलब्ध नहीं है।")
    else:
        v_name = st.selectbox("🏪 सब्जी विक्रेता चुनें:", list(st.session_state.vendors.keys()))
        vendor_data = st.session_state.vendors[v_name]
        
        st.subheader(f"{v_name} का ताज़ा स्टॉक")
        
        order_list = []
        total_bill = 0.0

        for item_name, details in vendor_data["items"].items():
            st.markdown(f"""
            <div class="card">
                <h4 style="margin:0; color:#1b5e20;">🥦 {item_name}</h4>
                <p style="margin:0; color:#555;">रेट: ₹{details['price']} / {details['unit']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            qty = st.number_input(f"मात्रा ({details['unit']})", min_value=0.0, step=0.5, key=f"c_{v_name}_{item_name}")
            if qty > 0:
                cost = qty * details['price']
                order_list.append(f"• {item_name}: {qty} {details['unit']} = ₹{cost:.1f}")
                total_bill += cost
            st.write("---")

        if total_bill > 0:
            st.markdown(f"### 🧾 कुल बिल: <span style='color:#2e7d32;'>₹{total_bill:.1f}</span>", unsafe_allow_html=True)
            c_name = st.text_input("आपका नाम")
            c_addr = st.text_input("पूरा पता (लैंडमार्क के साथ)")
            
            if st.button("📲 WhatsApp पर डायरेक्ट ऑर्डर भेजें"):
                if c_name and c_addr:
                    msg = f"🛒 *नया ऑर्डर ({v_name})*\n👤 *ग्राहक:* {c_name}\n📍 *पता:* {c_addr}\n\n*सामान List:*\n"
                    msg += "\n".join(order_list)
                    msg += f"\n\n💰 *कुल योग:* ₹{total_bill:.1f}"
                    
                    url = f"https://wa.me/{vendor_data['phone']}?text={urllib.parse.quote(msg)}"
                    st.markdown(f'<a href="{url}" target="_blank" style="background:#25D366;color:white;display:block;text-align:center;padding:12px;border-radius:8px;text-decoration:none;font-weight:bold;">कन्फर्म करने के लिए क्लिक करें</a>', unsafe_allow_html=True)
                else:
                    st.error("कृपया नाम और पता भरें!")

# ---------------------------------------------------------
# TAB 2: VENDOR MANAGEMENT
# ---------------------------------------------------------
with tab2:
    st.subheader("दुकानदार डैशबोर्ड")
    v_opt = st.radio("विकल्प चुनें:", ["नई दुकान खोलें", "सब्जी जोड़ें/हटाएं"])

    if v_opt == "नई दुकान खोलें":
        new_shop = st.text_input("दुकान का नाम")
        new_phone = st.text_input("WhatsApp नंबर (जैसे 919876543210)")
        if st.button("रजिस्टर करें"):
            if new_shop and new_phone:
                st.session_state.vendors[new_shop] = {"phone": new_phone, "items": {}}
                st.success(f"'{new_shop}' सफ़लतापूर्वक रजिस्टर हो गई!")
            else:
                st.error("सभी जानकारी भरें।")

    elif v_opt == "सब्जी जोड़ें/हटाएं":
        if st.session_state.vendors:
            curr_v = st.selectbox("अपनी दुकान चुनें:", list(st.session_state.vendors.keys()))
            
            st.markdown("---")
            st.write("➕ **नई सब्जी जोड़ें या रेट बदलें:**")
            p_name = st.text_input("सब्जी का नाम")
            p_price = st.number_input("रेट (₹)", min_value=1.0)
            p_unit = st.selectbox("इकाई", ["kg", "pc", "packet"])
            
            if st.button("स्टॉक में जोड़ें"):
                if p_name:
                    # Smart overwrite (No Duplicates)
                    st.session_state.vendors[curr_v]["items"][p_name] = {"price": p_price, "unit": p_unit}
                    st.success(f"'{p_name}' अपडेट हो गई!")
                    st.rerun()

            st.markdown("---")
            st.write("📋 **आपकी मौजूदा सब्जियाँ:**")
            items = st.session_state.vendors[curr_v]["items"]
            
            if items:
                for item_k, item_v in list(items.items()):
                    c1, c2 = st.columns([3, 1])
                    with c1:
                        st.write(f"• **{item_k}**: ₹{item_v['price']} / {item_v['unit']}")
                    with c2:
                        if st.button("🗑️ हटाएँ", key=f"del_{curr_v}_{item_k}"):
                            del st.session_state.vendors[curr_v]["items"][item_k]
                            st.rerun()
            else:
                st.info("कोई सब्जी उपलब्ध नहीं है।")
