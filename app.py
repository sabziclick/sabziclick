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
    .price-tag {
        color: #2e7d32;
        font-weight: bold;
        font-size: 1.1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Fixed & Verified Direct Image URLs for Vegetables
DEFAULT_CATALOG = {
    # 1. दैनिक सब्जियाँ
    "🥔 आलू (Potato)": {"price": 25.0, "unit": "kg", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ab/Patatas.jpg/400px-Patatas.jpg"},
    "🧅 प्याज (Onion)": {"price": 35.0, "unit": "kg", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/25/Onion_on_White.JPG/400px-Onion_on_White.JPG"},
    "🍅 टमाटर (Tomato)": {"price": 30.0, "unit": "kg", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/89/Tomato_je.jpg/400px-Tomato_je.jpg"},
    "🌶️ हरी मिर्च (Green Chilli)": {"price": 60.0, "unit": "kg", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Green_Chili_Pepper.jpg/400px-Green_Chili_Pepper.jpg"},
    "🫚 अदरक (Ginger)": {"price": 120.0, "unit": "kg", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2b/Ginger_root.jpg/400px-Ginger_root.jpg"},
    "🧄 लहसुन (Garlic)": {"price": 180.0, "unit": "kg", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Garlic_bulbs.jpg/400px-Garlic_bulbs.jpg"},
    "🍋 नींबू (Lemon)": {"price": 5.0, "unit": "pc", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e4/Lemon.jpg/400px-Lemon.jpg"},

    # 2. हरी और पत्तेदार सब्जियाँ
    "🥬 पालक (Spinach)": {"price": 30.0, "unit": "kg", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/03/Spinach_leaves.jpg/400px-Spinach_leaves.jpg"},
    "🌿 धनिया पत्ती (Coriander)": {"price": 80.0, "unit": "kg", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Cilantro.jpg/400px-Cilantro.jpg"},
    "🌱 पुदीna (Mint)": {"price": 60.0, "unit": "kg", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/52/Mint-leaves.jpg/400px-Mint-leaves.jpg"},

    # 3. गोभी और बीन्स परिवार
    "🥦 फूलगोभी (Cauliflower)": {"price": 40.0, "unit": "pc", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Cauliflower.jpg/400px-Cauliflower.jpg"},
    "🥬 पत्तागोभी (Cabbage)": {"price": 30.0, "unit": "kg", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6f/Cabbage_and_cross_section.jpg/400px-Cabbage_and_cross_section.jpg"},
    "🥦 ब्रोकोली (Broccoli)": {"price": 80.0, "unit": "kg", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/03/Broccoli_and_cross_section_edit.jpg/400px-Broccoli_and_cross_section_edit.jpg"},
    "🫘 फ़्रेंच बीन्स (French Beans)": {"price": 50.0, "unit": "kg", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/91/Green_beans_display.jpg/400px-Green_beans_display.jpg"},

    # 4. लौकी, कद्दू और खीरा
    "🥒 लौकी (Bottle Gourd)": {"price": 30.0, "unit": "pc", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/14/Calabash_2.jpg/400px-Calabash_2.jpg"},
    "🎃 कद्दू / कोहरा (Pumpkin)": {"price": 25.0, "unit": "kg", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5c/GREAT_PUMPKIN.jpg/400px-GREAT_PUMPKIN.jpg"},
    "🥒 खीरा (Cucumber)": {"price": 30.0, "unit": "kg", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/96/Cucumbers_building.jpg/400px-Cucumbers_building.jpg"},

    # 5. जड़ वाली सब्जियाँ
    "🥕 गाजर (Carrot)": {"price": 40.0, "unit": "kg", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/bd/Carrots_at_Ljubljana_Central_Market.jpg/400px-Carrots_at_Ljubljana_Central_Market.jpg"},
    "🧅 चुकंदर (Beetroot)": {"price": 40.0, "unit": "kg", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a4/Beetroot_bundle.jpg/400px-Beetroot_bundle.jpg"},

    # 6. अन्य लोकप्रिय सब्जियाँ
    "🫑 शिमला मिर्च (Capsicum)": {"price": 60.0, "unit": "kg", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/52/Green_bell_pepper.jpg/400px-Green_bell_pepper.jpg"},
    "🍆 बैंगन (Brinjal)": {"price": 35.0, "unit": "kg", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/76/Solanum_melongena_24_08_2012_%281%29.JPG/400px-Solanum_melongena_24_08_2012_%281%29.JPG"},
    "🫛 हरा मटर (Green Peas)": {"price": 60.0, "unit": "kg", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/11/Peas_in_pod_-_Studio.jpg/400px-Peas_in_pod_-_Studio.jpg"},
    "🌽 मक्का / भुट्टा (Sweet Corn)": {"price": 20.0, "unit": "pc", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f0/Corn_on_the_cob_1.jpg/400px-Corn_on_the_cob_1.jpg"}
}

# Session Data Setup
if "vendors" not in st.session_state:
    init_items = {}
    for k, v in DEFAULT_CATALOG.items():
        init_items[k] = {"price": v["price"], "unit": v["unit"], "available": True}
        
    st.session_state.vendors = {
        "महफीज़ सब्जी (Mohfeez Sabzi)": {
            "phone": "919876543210",
            "items": init_items
        }
    }

st.markdown("<h1 style='text-align: center; color: #2e7d32;'>🥦 Sabziclick</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-weight: bold; color: #555;'>किशनगंज ताज़ा ऑनलाइन सब्जी मंडी</p>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["🛒 ग्राहक दुकान (Customer View)", "🏪 दुकानदार पोर्टल (Vendor Control)"])

# TAB 1: CUSTOMER VIEW
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
                img_url = DEFAULT_CATALOG.get(item_name, {}).get("image", "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ab/Patatas.jpg/400px-Patatas.jpg")
                
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

# TAB 2: VENDOR CONTROL
with tab2:
    st.subheader("🏪 दुकानदार मैनेजमेंट पोर्टल")
    v_action = st.radio("आप क्या करना चाहते हैं?", ["नई दुकान रजिस्टर करें", "अपनी दुकान का स्टॉक/रेट बदलें"])

    if v_action == "नई दुकान रजिस्टर करें":
        new_shop = st.text_input("दुकान का नाम (उदा: गुप्ता वेजीटेबल्स)")
        new_phone = st.text_input("WhatsApp नंबर (उदा: 919876543210)")
        if st.button("दुकान खोलें"):
            if new_shop and new_phone:
                v_init_items = {}
                for k, v in DEFAULT_CATALOG.items():
                    v_init_items[k] = {"price": v["price"], "unit": v["unit"], "available": True}
                st.session_state.vendors[new_shop] = {"phone": new_phone, "items": v_init_items}
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
                    is_avail = st.checkbox("चालू", value=details.get("available", True), key=f"a_{curr_v}_{item_name}")
                    details['available'] = is_avail
                st.markdown("<hr style='margin:5px 0;'>", unsafe_allow_html=True)
            
            st.success("सारे बदलाव सेव हो गए हैं!")
