import streamlit as st
import urllib.parse

st.set_page_config(page_title="Sabziclick - Multi-Vendor Mandi", page_icon="🥦", layout="centered")

# Correct session state initialization
if "vendors" not in st.session_state:
    st.session_state.vendors = {
        "रामू गुप्ता (गुप्ता वेजीटेबल्स)": {
            "phone": "919876543210",
            "items": [
                {"name": "आलू (Potato)", "price": 25, "unit": "kg"},
                {"name": "प्याज (Onion)", "price": 35, "unit": "kg"}
            ]
        },
        "अहमद ट्रेडर्स": {
            "phone": "919123456789",
            "items": [
                {"name": "टमाटर (Tomato)", "price": 40, "unit": "kg"},
                {"name": "गोभी (Cauliflower)", "price": 30, "unit": "pc"}
            ]
        }
    }

st.title("🥦 Sabziclick - किशनगंज सब्जी मंडी")
st.caption("स्थानीय विक्रेताओं से सीधे घर पर ताज़ा सब्ज़ी मँगवाएँ!")

tab1, tab2 = st.tabs(["🛒 सब्जी खरीदें (Customer)", "🏪 दुकानदार पोर्टल (Vendor Register/Login)"])

# ---------------------------------------------------------
# TAB 1: CUSTOMER VIEW (Buy Vegetables)
# ---------------------------------------------------------
with tab1:
    st.header("दुकानदार चुनें")
    
    if not st.session_state.vendors:
        st.info("अभी कोई दुकानदार रजिस्टर नहीं है।")
    else:
        vendor_names = list(st.session_state.vendors.keys())
        selected_vendor_name = st.selectbox("सब्जी की दुकान चुनें:", vendor_names)
        
        vendor_info = st.session_state.vendors[selected_vendor_name]
        vendor_phone = vendor_info["phone"]
        vendor_items = vendor_info["items"]
        
        st.subheader(f"🏪 {selected_vendor_name} की ताज़ा दरें")
        
        order_details = []
        total_amount = 0.0
        
        for idx, item in enumerate(vendor_items):
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.write(f"**{item['name']}**")
                st.write(f"₹{item['price']} / {item['unit']}")
            with col2:
                qty = st.number_input(f"मात्रा ({item['unit']})", min_value=0.0, step=0.5, key=f"cust_{selected_vendor_name}_{idx}")
            with col3:
                item_total = qty * item['price']
                st.write(f"कुल: ₹{item_total:.1f}")
                
            if qty > 0:
                order_details.append(f"• {item['name']}: {qty} {item['unit']} (₹{item_total:.1f})")
                total_amount += item_total
            st.divider()
            
        if total_amount > 0:
            st.success(f"**कुल योग: ₹{total_amount:.1f}**")
            st.subheader("डिलीवरी का पता लिखें")
            cust_name = st.text_input("आपका नाम", key="c_name")
            cust_address = st.text_input("पूरा पता (जैसे: लाइन मस्जिद रोड, किशनगंज)", key="c_addr")
            
            if st.button("📲 WhatsApp पर ऑर्डर भेजें"):
                if not cust_name or not cust_address:
                    st.error("कृपया अपना नाम और पता दर्ज करें!")
                else:
                    msg = f"नया ऑर्डर ({selected_vendor_name} के लिए)!\n"
                    msg += f"नाम: {cust_name}\n"
                    msg += f"पता: {cust_address}\n\n"
                    msg += "सामान:\n" + "\n".join(order_details) + "\n\n"
                    msg += f"कुल बिल: ₹{total_amount:.1f}"
                    
                    encoded_msg = urllib.parse.quote(msg)
                    whatsapp_url = f"https://wa.me/{vendor_phone}?text={encoded_msg}"
                    
                    st.markdown(f'<a href="{whatsapp_url}" target="_blank" style="background-color:#25D366;color:white;padding:10px 15px;border-radius:5px;text-decoration:none;font-weight:bold;">ऑर्डर की पुष्टि करें (WhatsApp खोलें)</a>', unsafe_allow_html=True)

# ---------------------------------------------------------
# TAB 2: VENDOR PORTAL (Register & Manage Products)
# ---------------------------------------------------------
with tab2:
    st.header("अपनी दुकान रजिस्टर करें या नई सब्जी जोड़ें")
    
    vendor_action = st.radio("आप क्या करना चाहते हैं?", ["नई दुकान रजिस्टर करें", "मौजूदा दुकान में सब्जी जोड़ें"])
    
    if vendor_action == "नई दुकान रजिस्टर करें":
        st.subheader("1. नई दुकान का रजिस्ट्रेशन")
        new_v_name = st.text_input("दुकान या विक्रेता का नाम (उदा: गुप्ता वेजीटेबल्स)")
        new_v_phone = st.text_input("WhatsApp नंबर (देश के कोड के साथ, उदा: 919876543210)")
        
        if st.button("दुकान रजिस्टर करें"):
            if new_v_name and new_v_phone:
                if new_v_name not in st.session_state.vendors:
                    st.session_state.vendors[new_v_name] = {"phone": new_v_phone, "items": []}
                    st.success(f"बधाई हो! '{new_v_name}' रजिस्टर हो गई है। अब नीचे सब्जी जोड़ें।")
                else:
                    st.warning("यह दुकान पहले से रजिस्टर है!")
            else:
                st.error("कृपया दुकान का नाम और WhatsApp नंबर दोनों भरें।")

    elif vendor_action == "मौजूदा दुकान में सब्जी जोड़ें":
        st.subheader("2. अपनी दुकान में सामान/रेट अपडेट करें")
        if not st.session_state.vendors:
            st.info("पहले कोई दुकान रजिस्टर करें।")
        else:
            v_select = st.selectbox("अपनी दुकान चुनें:", list(st.session_state.vendors.keys()))
            
            st.write("---")
            st.markdown("**नई सब्जी जोड़ें:**")
            prod_name = st.text_input("सब्जी का नाम (उदा: भिंडी / Lady Finger)")
            prod_price = st.number_input("दाम (₹)", min_value=1.0, step=1.0)
            prod_unit = st.selectbox("इकाई (Unit)", ["kg", "pc", "gram", "packet"])
            
            if st.button("सब्जी जोड़ें"):
                if prod_name:
                    st.session_state.vendors[v_select]["items"].append({
                        "name": prod_name,
                        "price": prod_price,
                        "unit": prod_unit
                    })
                    st.success(f"'{prod_name}' आपकी दुकान में जोड़ दी गई है!")
                else:
                    st.error("सब्जी का नाम दर्ज करें।")
            
            st.write("---")
            st.subheader(f"आपकी वर्तमान सब्जियाँ ({v_select}):")
            current_items = st.session_state.vendors[v_select]["items"]
            if current_items:
                for item in current_items:
                    st.write(f"• **{item['name']}** - ₹{item['price']} / {item['unit']}")
            else:
                st.info("अभी कोई सब्जी नहीं जोड़ी गई है।")
