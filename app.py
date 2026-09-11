import streamlit as st

st.set_page_config(page_title="Kishanganj Sabzi Mandi", page_icon="🥦")

st.title("🥦 किशनगंज ताज़ा सब्ज़ी बाज़ार")
st.write("किशनगंज के स्थानीय विक्रेताओं से सीधे घर पर ताज़ा सब्ज़ी मँगवाएँ!")

tab1, tab2 = st.tabs(["🛒 सब्ज़ी खरीदें (Customer)", "🧺 सब्ज़ी बेचें (Vendor)"])

with tab1:
    st.header("ताज़ा सब्ज़ियों की दरें")
    
    veggies = [
        {"name": "आलू (Potato)", "price": 25, "unit": "kg", "vendor": "रामू गुप्ता", "phone": "919876543210"},
        {"name": "प्याज (Onion)", "price": 35, "unit": "kg", "vendor": "रामू गुप्ता", "phone": "919876543210"},
        {"name": "टमाटर (Tomato)", "price": 40, "unit": "kg", "vendor": "अहमद ट्रेडर्स", "phone": "919123456789"}
    ]
    
    selected_items = []
    for veg in veggies:
        col1, col2, col3 = st.columns([2, 1, 1])
        col1.write(f"**{veg['name']}** ({veg['vendor']})")
        col2.write(f"₹{veg['price']} / {veg['unit']}")
        qty = col3.number_input(f"मात्रा ({veg['unit']})", min_value=0.0, step=0.5, key=veg['name'])
        
        if qty > 0:
            selected_items.append({"name": veg['name'], "qty": qty, "price": veg['price'] * qty, "phone": veg['phone']})

    st.divider()
    
    if selected_items:
        st.subheader("आपका ऑर्डर (Order Summary)")
        total_amount = sum(item["price"] for item in selected_items)
        
        for item in selected_items:
            st.write(f"- {item['name']}: {item['qty']} kg = ₹{item['price']}")
        st.markdown(f"### कुल राशि: **₹{total_amount}**")
        
        cust_name = st.text_input("आपका नाम")
        cust_address = st.text_input("पूरा पता (किशनगंज)")
        
        if st.button("WhatsApp पर ऑर्डर भेजें 📲"):
            if cust_name and cust_address:
                msg = f"नया ऑर्डर!\nनाम: {cust_name}\nपता: {cust_address}\nसामान:\n"
                for item in selected_items:
                    msg += f"- {item['name']}: {item['qty']} kg\n"
                msg += f"कुल: ₹{total_amount}"
                
                vendor_phone = selected_items[0]['phone']
                whatsapp_url = f"https://wa.me/{vendor_phone}?text={msg.replace(' ', '%20').replace('\n', '%0A')}"
                
                st.success("ऑर्डर तैयार है! नीचे दिए बटन पर क्लिक करके WhatsApp पर भेजें:")
                st.markdown(f"[📲 WhatsApp पर मैसेज भेजें]({whatsapp_url})", unsafe_allow_html=True)
            else:
                st.error("कृपया नाम और पता भरें!")

with tab2:
    st.header("विक्रेता पोर्टल (Vendor Portal)")
    st.write("अपनी दुकान और आज की ताज़ा सब्ज़ियाँ जोड़ें")
    
    v_name = st.text_input("दुकान / आपका नाम")
    v_phone = st.text_input("व्हाट्सएप नंबर")
    veg_name = st.text_input("सब्ज़ी का नाम (उदा. बैंगन)")
    veg_price = st.number_input("दाम (₹ प्रति kg)", min_value=1)
    
    if st.button("सब्ज़ी लिस्ट करें"):
        st.success(f"{veg_name} (₹{veg_price}/kg) सफलतापूर्वक जोड़ दिया गया!")

