import streamlit as st
import urllib.parse

st.set_page_config(page_title="Sabziclick - किशनगंज ताज़ा मंडी", page_icon="🥦", layout="centered")

# Custom UI Styling
st.markdown("""
    <style>
    .main { background-color: #f4f6f8; }
    .stButton>button {
        background-color: #2e7d32 !important;
        color: white !important;
        font-weight: bold !important;
        border-radius: 8px !important;
        padding: 10px 20px !important;
        border: none !important;
        width: 100%;
    }
    .veg-card {
        background-color: white;
        padding: 12px;
        border-radius: 12px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.06);
        margin-bottom: 15px;
        border: 1px solid #e0e0e0;
    }
    .price-tag {
        color: #2e7d32;
        font-weight: bold;
        font-size: 1.1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Master Vegetable Catalog with Photos and Default Kishanganj Market Rates
DEFAULT_CATALOG = {
    "टमाटर (Tomato)": {
        "price": 30.0, "unit": "kg",
        "image": "https://images.unsplash.com/photo-1592924357228-91a4daadcfea?w=300"
    },
    "आलू (Potato)": {
        "price": 25.0, "unit": "kg",
        "image": "https://images.unsplash.com/photo-1518977676601-b53f82aba655?w=300"
    },
    "प्याज (Onion)": {
        "price": 35.0, "unit": "kg",
        "image": "https://images.unsplash.com/photo-1618512496248-a07fe83aa8cb?w=300"
    },
    "फूलगोभी (Cauliflower)": {
        "price": 40.0, "unit": "pc",
        "image": "https://images.unsplash.com/photo-1568584711075-3d021a7c3ca3?w=300"
    },
    "पत्तागोभी (Cabbage)": {
        "price": 30.0, "unit": "kg",
        "image": "https://images.unsplash.com/photo-1615485290382-441e4d049cb5?w=300"
    },
    "भिंडी (Lady Finger)": {
        "price": 40.0, "unit": "kg",
        "image": "https://images.unsplash.com/photo-1628773822503-930a8581898e?w=300"
    },
    "बैंगन (Brinjal)": {
        "price": 35.0, "unit": "kg",
        "image": "https://images.unsplash.com/photo-1613743983387-f827471fb62e?w=300"
    },
    "हरी मिर्च (Green Chilli)": {
        "price": 60.0, "unit": "kg",
        "image": "https://images.unsplash.com/photo-1588252303782-cb80119abd6d?w=300"
    },
    "धनिया पत्ती (Coriander)": {
        "price": 80.0, "unit": "kg",
        "image": "https://images.unsplash.com/photo-1588879460618-924a1329a6b1?w=300"
    }
}

# Initialize Multi-vendor Session Data
if "vendors" not in st.session_state:
    st.session_state.vendors = {
        "महफीज़ सब्जी (Mohfeez Sabzi)": {
            "phone": "919876543210",
            "items": {
                "टमाटर (Tomato)": {"price": 30.0, "unit": "kg", "available": True},
                "आलू (Potato)": {"price": 25.0, "unit": "kg", "available": True},
                "प्याज (Onion)": {"price": 35.0, "unit": "kg", "available": True},
                "फूलगोभी (Cauliflower)": {"price": 40.0, "unit": "pc", "available": True}
            }
        }
    }

st.markdown("<h1 style='text-align: center; color: #2e7d32;'>🥦 Sabziclick</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-weight: bold; color: #555;'>किशनगंज ताज़ा ऑनलाइन सब्जी मंडी</p>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["🛒 ग्राहक दुकान (Customer View)", "🏪 दुकानदार पोर्टल (Vendor Control)"])

# ---------------------------------------------------------
# TAB 1: CUSTOMER SHOPPING VIEW
# ---------------------------------------------------------
with tab1:
    if not st.session_state.vendors:
        st.info("अभी कोई दुकान उपलब्ध नहीं है।")
    else:
        v_name = st.selectbox("🏪 अपनी पसंदीदा दुकान चुनें:", list(st.session_state.vendors.keys()))
        vendor_data = st.session_state.vendors[v_name]
        
        st.subheader(f"🏬 {v_name} की ताज़ा सब्ज़ियाँ")
        
        order_list = []
        total_bill = 0.0

        for item_name, details in vendor_data["items"].items():
            if details.get("available", True):
                img_url = DEFAULT_CATALOG.get(item_name, {}).get("image", "https://images.unsplash.com/photo-1540420773420-3366772f4999?w=300")
                
                col_img, col_desc = st.columns([1, 2])
                with col_img:
                    st.image(img_url, use_container_width=True)
                with col_desc:
                    st.markdown(f"### {item_name}")
                    st.markdown(f"<p class='price-tag'>₹{details['price']} / {details['unit']}</p>", unsafe_allow_html=True)
                    qty = st.number_input(f"मात्रा ({details['unit']})", min_value=0.0, step=0.5, key=f"cust_{v_name}_{item_name}")
                    
                    if qty > 0:
                        cost = qty * details['price']
                        order_list.append(f"• {item_name}: {qty} {details['unit']} = ₹{cost:.1f}")
                        total_bill += cost
                st.markdown("<hr style='margin:10px 0;'>", unsafe_allow_html=True)

        if total_bill > 0:
            st.markdown(f"## 🧾 कुल योग: <span style='color:#2e7d32;'>₹{total_bill:.1f}</span>", unsafe_allow_html=True)
            c_name = st.text_input("आपका नाम", key="cust_name_inp")
            c_addr = st.text_input("पूरा पता (लैंडमार्क के साथ)", key="cust_addr_inp")
            
            if st.button("📲 WhatsApp पर ऑर्डर भेजें"):
                if c_name and c_addr:
                    msg = f"🛒 *नया ऑर्डर ({v_name})*\n👤 *ग्राहक:* {c_name}\n📍 *पता:* {c_addr}\n\n*सामान List:*\n"
                    msg += "\n".join(order_list)
                    msg += f"\n\n💰 *कुल बिल:* ₹{total_bill:.1f}"
                    
                    url = f"https://wa.me/{vendor_data['phone']}?text={urllib.parse.quote(msg)}"
                    st.markdown(f'<a href="{url}" target="_blank" style="background:#25D366;color:white;display:block;text-align:center;padding:12px;border-radius:8px;text-decoration:none;font-weight:bold;font-size:1.1rem;">ऑर्डर की पुष्टि करें (WhatsApp खोलें)</a>', unsafe_allow_html=True)
                else:
                    st.error("कृपया अपना नाम और पता दर्ज करें!")

# ---------------------------------------------------------
# TAB 2: VENDOR MANAGEMENT PORTAL
# ---------------------------------------------------------
with tab2:
    st.subheader("🏪 दुकानदार मैनेजमेंट पोर्टल")
    v_action = st.radio("आप क्या करना चाहते हैं?", ["नई दुकान रजिस्टर करें", "अपनी दुकान का स्टॉक/रेट बदलें"])

    if v_action == "नई दुकान रजिस्टर करें":
        new_shop = st.text_input("दुकान का नाम (उदा: किशनगंज वेजीटेबल्स)")
        new_phone = st.text_input("WhatsApp नंबर (उदा: 919876543210)")
        if st.button("दुकान खोलें"):
            if new_shop and new_phone:
                # Initialize new vendor with master catalog
                init_items = {}
                for k, v in DEFAULT_CATALOG.items():
                    init_items[k] = {"price": v["price"], "unit": v["unit"], "available": True}
                st.session_state.vendors[new_shop] = {"phone": new_phone, "items": init_items}
                st.success(f"बधाई हो! '{new_shop}' की दुकान चालू हो गई है।")
                st.rerun()
            else:
                st.error("दुकान का नाम और WhatsApp नंबर भरें!")

    elif v_action == "अपनी दुकान का स्टॉक/रेट बदलें":
        if st.session_state.vendors:
            curr_v = st.selectbox("अपनी दुकान चुनें:", list(st.session_state.vendors.keys()))
            v_items = st.session_state.vendors[curr_v]["items"]
            
            st.write("---")
            st.markdown("### 🥦 अपनी सब्जियों की उपलब्धता और रेट मैनेज करें")
            st.caption("जो सब्जी दुकान में चालू रखनी है उसे चालू (ON) रखें, और ज़रूरत पड़ने पर रेट बदल लें:")
            
            for cat_item, cat_info in DEFAULT_CATALOG.items():
                if cat_item not in v_items:
                    v_items[cat_item] = {"price": cat_info["price"], "unit": cat_info["unit"], "available": False}

            for item_name, details in v_items.items():
                col1, col2, col3 = st.columns([2, 1, 1])
                with col1:
                    st.write(f"**{item_name}**")
                with col2:
                    new_price = st.number_input(f"रेट (₹/{details['unit']})", min_value=1.0, value=float(details['price']), key=f"p_{curr_v}_{item_name}")
                    details['price'] = new_price
                with col3:
                    is_avail = st.checkbox("दुकान में चालू", value=details.get("available", True), key=f"a_{curr_v}_{item_name}")
                    details['available'] = is_avail
                st.markdown("<hr style='margin:5px 0;'>", unsafe_allow_html=True)
            
            st.success("सारे बदलाव अपने आप सेव हो रहे हैं!")
