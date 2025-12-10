import streamlit as st
import numpy as np
import librosa
import soundfile as sf
from io import BytesIO

st.title("🎵 Echo Generator")

# رفع الملف
uploaded_file = st.file_uploader("ارفع ملف الصوت", type=['mp3', 'wav'])

if uploaded_file is not None:
    # عرض الملف الأصلي
    st.audio(uploaded_file)
    
    # إعدادات
    alpha = st.slider("Alpha", 0.4, 0.8, 0.6, 0.1)
    delay_sec = st.slider("Delay (seconds)", 0.05, 2.0, 0.5, 0.05)
    
    if st.button("Generate Echo"):
        # قراءة ملف الصوت
        x, fs = librosa.load(uploaded_file, sr=None, mono=True)
        
        # معاملات Echo
        # alpha و delay_sec من الـ sliders
        
        # حساب Nd
        Nd = int(delay_sec * fs)
        
        # إنشاء إشارة الخرج
        output_length = len(x) + Nd + int(3 * fs)
        y = np.zeros(output_length)
        
        # نسخ الإشارة الأصلية
        for n in range(len(x)):
            y[n] = x[n]
        
        # تطبيق Echo: Y[n] = x[n] + alpha * Y[n-Nd]
        for n in range(len(y)):
            if n >= Nd:
                y[n] = y[n] + alpha * y[n - Nd]
        
        # تطبيع
        y = y / np.max(np.abs(y))
        
        # حفظ في الذاكرة
        output_buffer = BytesIO()
        sf.write(output_buffer, y, fs, format='WAV')
        output_buffer.seek(0)
        
        st.success(f"Echo generated: alpha={alpha}, delay={delay_sec}s")
        
        # عرض وتحميل الملف
        st.audio(output_buffer)
        
        st.download_button(
            label="Download Echo Audio",
            data=output_buffer,
            file_name="output_echo.wav",
            mime="audio/wav"
        )
