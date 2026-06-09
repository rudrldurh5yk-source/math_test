import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 1. 페이지 기본 설정 및 디자인 테마 🎒
st.set_page_config(
    page_title="기하 융합 탐구: 건물 그림자와 정사영 🏢",
    page_icon="📐",
    layout="centered"
)

# 귀여운 파스텔톤 폰트 및 UI 디자인 적용 ✨
st.markdown("""
    <style>
    .main-title {
        font-size: 2.6rem !important;
        color: #FF6B81;
        text-align: center;
        font-weight: bold;
        margin-bottom: 5px;
    }
    .sub-title {
        font-size: 1.1rem !important;
        color: #57606F;
        text-align: center;
        margin-bottom: 25px;
    }
    .mission-box {
        background-color: #FFF9E6;
        padding: 20px;
        border-radius: 15px;
        border: 2px dashed #FFA502;
        margin-bottom: 25px;
    }
    .math-box {
        background-color: #F1F2F6;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #2F3542;
        margin-top: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# 헤더 영역 ☀️
st.markdown('<div class="main-title">☀️ 빛과 건물, 그리고 정사영(Orthogonal Projection) 🏢</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">수학 교실 안에서 펼쳐지는 나만의 그림자 시뮬레이터 실습실! 🗺️📐</div>', unsafe_allow_html=True)
st.divider()

# 2. 수업 맥락 및 탐구 미션 안내 박스 📜
st.markdown("""
<div class="mission-box">
    <h4 style="margin-top:0; color:#FF6B81;">💡 [오늘의 탐구 미션]</h4>
    <p style="font-size:0.95rem; line-height:1.6; color:#2F3542; margin-bottom:0;">
        태양이 지면과 이루는 각도에 따라 건물의 그림자 길이는 어떻게 변할까요?<br>
        <b>벽면(높이)이 만드는 그림자</b>와 <b>지붕(너비)이 만드는 그림자</b>의 원리를 비교해 보고, 
        우리가 교과서에서 배운 <b>정사영 공식</b>과 일치하는지 데이터로 검증해 봅시다! 🕵️‍♂️✨
    </p>
</div>
""", unsafe_allow_html=True)

# 3. 사이드바 - 세계 유명 건물 템플릿 및 변수 제어 🛠️
st.sidebar.header("🏢 실험실 변수 제어 센터")

# 세계 유명 건물 데이터 셋팅
building_presets = {
    "직접 입력하기 ✏️": {"height": 50.0, "width": 20.0},
    "대한민국 롯데월드타워 🗼 (서울)": {"height": 555.0, "width": 70.0},
    "프랑스 에펠탑 🇫🇷 (파리)": {"height": 330.0, "width": 125.0},
    "미국 엠파이어 스테이트 빌딩 🇺🇸 (뉴욕)": {"height": 381.0, "width": 130.0},
    "이집트 쿠푸왕의 대피라미드 🇪🇬 (카이로)": {"height": 138.0, "width": 230.0}
}

preset_choice = st.sidebar.selectbox("🗺️ 탐구할 세계 건물 템플릿을 골라보세요:", list(building_presets.keys()))

# 템플릿 선택에 따른 기본값 연동 및 수동 슬라이더 배치
if preset_choice == "직접 입력하기 ✏️":
    b_height = st.sidebar.slider("🏢 건물의 높이(H)를 정해주세요 (m)", 10, 600, 100)
    b_width = st.sidebar.slider("📏 건물의 너비(W)를 정해주세요 (m)", 5, 300, 30)
else:
    b_height = building_presets[preset_choice]["height"]
    b_width = building_presets[preset_choice]["width"]
    st.sidebar.info(f"선택한 건물 정보 -> 높이: {b_height}m, 너비: {b_width}m")

# 햇빛의 각도 설정 슬라이더
sun_angle = st.sidebar.slider("☀️ 햇빛과 지면이 이루는 각도 (θ)", 10, 80, 45, help="태양이 지면과 이루는 사잇각입니다.")

# 4. 수학적 시뮬레이션 계산 연산 루틴 🧮
# 햇빛과 지면이 이루는 각도 theta (라디안 변환)
theta_rad = np.radians(sun_angle)

# 삼각비를 통한 실제 물리적 그림자 총 길이 계산
# 건물의 수직 벽면(높이)에 의해 생기는 그림자 길이 = H / tan(theta)
shadow_from_height = b_height / np.tan(theta_rad)
# 건물의 수평 지붕(너비)에 의해 지면에 투영되는 그림자 길이 = W (지면과 평행하므로 빛의 방향과 관계없이 기본 너비만큼 바닥에 깔림)
total_shadow_length = shadow_from_height + b_width

# 5. 시각화 그래픽 생성 (Matplotlib) 🎨
fig, ax = plt.subplots(figsize=(7, 4.5))

# 지면 그리기 (y=0)
ax.axhline(0, color='#2F3542', linewidth=2)

# 건물 그리기 (단면을 직사각형으로 시각화)
# 건물의 x 좌표축 위치는 [-b_width, 0]으로 설정하여 원점 오른쪽에 그림자가 뻗어나가도록 배치
building_rect = plt.Rectangle((-b_width, 0), b_width, b_height, color='#747D8C', alpha=0.8, label='Building')
ax.add_patch(building_rect)

# 그림자 영역 시각화 (원점 0부터 그림자 총 길이까지)
shadow_rect = plt.Rectangle((0, -b_height*0.02), total_shadow_length, b_height*0.02, color='#2F3542', alpha=0.6, label='Shadow')
ax.add_patch(shadow_rect)

# 태양 빛 선 그리기 (건물 우측 상단 꼭대기에서 지면으로 떨어지는 광선)
sun_ray_x = np.array([0, shadow_from_height])
sun_ray_y = np.array([b_height, 0])
ax.plot(sun_ray_x, sun_ray_y, color='#FFA502', linestyle='--', linewidth=2, label='Sun Ray')

# 햇빛 각도 표시 장식 호(Arc) 그리기
act_angle_x = shadow_from_height - (shadow_from_height * 0.15)
ax.text(shadow_from_height * 0.8, b_height * 0.1, f"{sun_angle}°", color='#FF6B81', fontweight='bold')

# 차트 디테일 설정 (여백 및 비율 조절)
ax.set_xlim(-b_width * 1.5, total_shadow_length * 1.3)
ax.set_ylim(-b_height * 0.1, b_height * 1.3)
ax.set_aspect('equal')
ax.axis('off') # 격자나 기본 축은 숨겨서 기하학적 도형 선만 돋보이게 처리
st.pyplot(fig)

# 6. 수학적 분석 및 학생들의 자기주도식 질문 검증 피드백 🔮
st.subheader("📊 시뮬레이션 측정 데이터 리포트")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="🏢 건물의 전체 높이 (H)", value=f"{b_height} m")
with col2:
    st.metric(label="📏 건물의 바닥 너비 (W)", value=f"{b_width} m")
with col3:
    st.metric(label="👥 최종 계산된 그림자 전체 길이", value=f"{total_shadow_length:.2f} m")

# 정사영 개념 연결을 위한 공식 해설판
st.markdown('<div class="math-box">', unsafe_allow_html=True)
st.markdown("#### 📐 정사영 관점에서의 핵심 단서 및 힌트")
st.write("교과서에서 배운 정사영의 정의는 **'도형의 각 점에서 평면에 내린 수선의 발들이 이루는 도형'** 입니다.")
st.latex(r"S' = S \times \cos\alpha")
st.write("🤔 **여기서 잠깐!** 태양광선과 건물 단면의 관계를 정사영으로 변환해 해석해 볼까요?")
st.markdown(
    f"""
    1. **건물의 지붕(너비 $W$):** 지면과 평행하므로 빛의 각도와 상관없이 항상 일정한 크기($W$)로 바닥에 그대로 투영(정사영)됩니다. 👉 **현재 투영 길이: {b_width}m**
    2. **건물의 벽면(높이 $H$):** 빛이 비스듬히 비출 때, 빛의 진행 방향과 수직인 가상의 가림막 단면을 기준으로 정사영 공식을 역으로 설계해 유도할 수 있습니다. 위 시뮬레이션에서 순수하게 높이 때문에 늘어난 지면 그림자 공식은 다음과 같습니다:
    """
)
st.latex(r"\text{벽면 그림자 길이} = \frac{H}{\tan\theta}")
st.markdown(fr"👉 **수식 대입 결과:** ${b_height} \div \tan({sun_angle}^\circ) = {shadow_from_height:.2f}\text{{m}}$")
st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# 7. 학생들이 생각하고 토론할 질문 가이드라인 (탐구 과제용) 📝
st.subheader("🧠 기하학 성장을 위한 스스로 토론 질문지")
st.info("""
✍️ **다음 질문들을 공책에 기록하며 스스로 답을 찾아보세요!**

1. ☀️ **햇빛과 지면의 각도($\theta$)가 $90^\circ$(직각)에 가까워질수록 그림자의 전체 길이는 어느 값에 수렴하게 될까요? 그 이유를 정사영의 개념과 연결하여 설명해 보세요.**
2. 📐 **만약 건물의 벽면과 빛의 진행 방향이 이루는 각을 $\alpha$라고 정의한다면, 순수 벽면의 높이($H$)와 정사영 공식($S' = S \cos\alpha$)을 결합하여 지면 그림자 공식을 다르게 유도할 수 있을까요?**
3. 🗺️ **세계 다른 건물들을 대입해 보았을 때, 건물의 비율(높이에 비해 너비가 극단적으로 넓은 피라미드 등)에 따라 각도 변화가 그림자 길이에 미치는 영향력이 어떻게 달라지는지 분석해 보세요.**
""")

# 예쁜 푸터 마무리 🧸
st.caption("⚙️ 본 웹 시뮬레이터는 고등학교 기하 수업 클래스 탐구 활동을 지원하기 위해 제작되었습니다. 정사영의 마법을 정복한 여러분을 응원해요! 🎀")
