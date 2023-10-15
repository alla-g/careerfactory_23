import math
import streamlit as st
from statsmodels.stats.power import NormalIndPower
from statsmodels.stats.proportion import proportion_effectsize

power_analysis = NormalIndPower()

st.set_page_config(page_title="Калькулятор А/Б теста",
                   page_icon=':abacus:')

st.title('Калькулятор минимального эффекта и размера выборки')
st.subheader('Выберите тип калькулятора:')

tab1, tab2 = st.tabs(['Минимальный эффект по размеру выборки', 'Размер выборки по минимальному эффекту'])

with tab1:
    alpha1 = 0.05
    power1 = 0.8

    st.write("Уровень значимости: 0.05")
    st.write("Мощность: 0.8")

    size = st.slider("Размер каждой группы в выборке:", min_value=10, max_value=30000, value=100, key='s1')
    mde = power_analysis.solve_power(nobs1=size, alpha=alpha1, power=power1,
                                     ratio=1, alternative='two-sided')

    st.metric(label="Минимальный детектируемый эффект:", value=round(mde, 4))
    uplift = (math.sin(math.asin(math.sqrt(0.1531)) - (mde / 2)) ** 2) - 0.1531
    st.metric(label="Для текущего значения в 15,31% \"плохих\" вакансий минимальная абсоютная разница (± n%) составит:",
              value=f"{round(abs(uplift) * 100, 2)}%")

with tab2:
    alpha2 = 0.05
    power2 = 0.8

    st.write("Уровень значимости: 0.05")
    st.write("Мощность: 0.8")

    uplift2 = st.slider("Минимальная абсолютная разница в процентах (± n%):", min_value=0.1, max_value=100.0,
                        value=5.0, key='u2')
    mde2 = proportion_effectsize(0.1531, 0.1531 + uplift2 / 100)
    st.write("MDE составит:", abs(mde2))

    sample_size = power_analysis.solve_power(effect_size=mde2, alpha=alpha2, power=power2,
                                             ratio=1, alternative='two-sided')
    
    st.metric("Минимальный размер каждой группы в выборке:", math.ceil(sample_size))
