import streamlit as st
import pickle
import numpy as np
import pandas as pd

# Inject custom CSS for modern, crazy aesthetics
st.markdown('''
    <style>
    body {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: #fff;
    }
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    }
    .big-font {
        font-size: 2.5rem !important;
        font-weight: bold;
        color: #fff;
        text-shadow: 2px 2px 8px #00000055;
    }
    .result-card {
        background: rgba(255,255,255,0.1);
        border-radius: 20px;
        padding: 2rem;
        margin-top: 2rem;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        text-align: center;
        animation: pop 0.7s cubic-bezier(.68,-0.55,.27,1.55) 1;
    }
    @keyframes pop {
        0% { transform: scale(0.7); opacity: 0; }
        100% { transform: scale(1); opacity: 1; }
    }
    .stButton>button {
        background: linear-gradient(90deg, #ff8a00 0%, #e52e71 100%);
        color: white;
        font-size: 1.2rem;
        border-radius: 10px;
        border: none;
        padding: 0.75rem 2rem;
        box-shadow: 0 4px 14px 0 #e52e7140;
        transition: 0.2s;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #e52e71 0%, #ff8a00 100%);
        transform: scale(1.05);
    }
    .error-message {
        background: rgba(255, 0, 0, 0.1);
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        color: #ff4444;
        text-align: center;
        animation: shake 0.5s cubic-bezier(.36,.07,.19,.97) both;
    }
    @keyframes shake {
        10%, 90% { transform: translate3d(-1px, 0, 0); }
        20%, 80% { transform: translate3d(2px, 0, 0); }
        30%, 50%, 70% { transform: translate3d(-4px, 0, 0); }
        40%, 60% { transform: translate3d(4px, 0, 0); }
    }
    </style>
''', unsafe_allow_html=True)

# Load model and data
pipe=pickle.load(open('pipe.pkl','rb'))
df=pickle.load(open('df.pkl','rb'))

st.markdown('<div class="big-font">💻 Laptop Price Predictor 🚀</div>', unsafe_allow_html=True)
st.markdown('''<p style="font-size:1.2rem; color:#f3f3f3;">Enter your laptop specs and get a crazy accurate price prediction!<br>✨ Try different combos for fun results! ✨</p>''', unsafe_allow_html=True)

# Layout: group inputs in columns for modern look
col1, col2, col3 = st.columns(3)

with col1:
    company=st.selectbox('🏢 Brand',df['Company'].unique())
    type=st.selectbox('💼 Type',df['TypeName'].unique())
    ram=st.selectbox('🧠 RAM (GB)',[2,4,6,8,12,16,24,32,64])
    weight=st.number_input('⚖️ Weight (kg)', min_value=0.1, value=2.0, step=0.1)

with col2:
    touchscreen=st.selectbox('🖐️ Touchscreen',['No','Yes'])
    ips=st.selectbox('🌈 IPS Display',['No','Yes'])
    screen_size=st.number_input('📏 Screen Size (inches)', min_value=10.0, max_value=20.0, value=15.6, step=0.1)
    resolution=st.selectbox('🖥️ Resolution',['1920x1080','1366x768','1600x900','3840x2160','3200x1800','2880x1800','2560x1600','2560x1440','2304x1440'])

with col3:
    cpu=st.selectbox('🧩 CPU',df['Cpu brand'].unique())
    hdd=st.selectbox('💾 HDD (GB)',[0,128,256,512,1024,2048])
    ssd=st.selectbox('⚡ SSD (GB)',[0,8,32,64,128,256,512,1024])
    gpu=st.selectbox('🎮 GPU',df['Gpu brand'].unique())
    os=st.selectbox('🖱️ OS',df['os'].unique())

# Predict button with animation
if st.button('🔮 Predict Price!'):
    try:
        # Fun animation
        st.balloons()
        
        # Convert inputs to proper format
        touchscreen = 1 if touchscreen == 'Yes' else 0
        ips = 1 if ips == 'Yes' else 0
        
        # Calculate PPI
        x_res = int(resolution.split('x')[0])
        y_res = int(resolution.split('x')[1])
        ppi = ((x_res**2) + (y_res**2))**0.5 / screen_size
        
        # Create a DataFrame with the correct column names matching the training data
        query_df = pd.DataFrame({
            'Company': [company],
            'TypeName': [type],
            'Inches': [screen_size],
            'ScreenResolution': [resolution],
            'Cpu': [cpu],
            'Ram': [f"{ram}GB"],
            'Memory': [f"{ssd}GB SSD + {hdd}GB HDD"],
            'Gpu': [gpu],
            'OpSys': [os],
            'Weight': [f"{weight}kg"],
            'Touchscreen': [touchscreen],
            'IPS': [ips],
            'ppi': [ppi]
        })
        
        # Make prediction
        price = int(np.exp(pipe.predict(query_df)[0]))
        
        # Display result with animation
        st.markdown(f'''<div class="result-card">
            <span style="font-size:2.5rem;">💸 <b>{price:,} INR</b> 💸</span><br>
            <span style="font-size:1.2rem; color:#fff;">Estimated Price</span>
            <br><br><span style="font-size:1.5rem;">🎉 Enjoy your dream laptop! 🎉</span>
        </div>''', unsafe_allow_html=True)
        
    except Exception as e:
        st.markdown(f'''<div class="error-message">
            <span style="font-size:1.2rem;">⚠️ Oops! Something went wrong:</span><br>
            {str(e)}<br>
            Please check your inputs and try again!
        </div>''', unsafe_allow_html=True)