import streamlit as st
from supabase import create_client

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="SDH ACADEMY | 문제은행 & 자료실",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Linear / Vercel 풍 초세련 다크 모드 CSS
st.markdown("""
<style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');

    /* 전역 스타일 */
    html, body, [class*="css"], .stApp {
        font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif !important;
        background-color: #0b0c10 !important;
        color: #f1f5f9 !important;
    }

    /* 상단 기본 헤더 숨김 및 패딩 정리 */
    header[data-testid="stHeader"] {
        background-color: transparent !important;
    }
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 3rem !important;
    }

    /* 사이드바 스타일링 */
    [data-testid="stSidebar"] {
        background-color: #0e1017 !important;
        border-right: 1px solid #1e2230 !important;
    }
    [data-testid="stSidebar"] * {
        color: #94a3b8 !important;
    }
    [data-testid="stSidebar"] h3, [data-testid="stSidebar"] h5 {
        color: #ffffff !important;
        font-weight: 700 !important;
        letter-spacing: -0.5px;
    }

    /* 탭 디자인: 미니멀 언더라인 바 */
    button[data-baseweb="tab"] {
        background: transparent !important;
        border: none !important;
        color: #64748b !important;
        font-size: 15px !important;
        font-weight: 600 !important;
        padding: 10px 18px !important;
        transition: all 0.2s ease;
    }
    button[data-baseweb="tab"]:hover {
        color: #cbd5e1 !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #38bdf8 !important;
        border-bottom: 2px solid #38bdf8 !important;
    }

    /* 입력 폼 라벨 */
    label[data-testid="stWidgetLabel"] p {
        color: #e2e8f0 !important;
        font-size: 13px !important;
        font-weight: 600 !important;
        letter-spacing: -0.3px;
        margin-bottom: 6px;
    }

    /* 인풋, 셀렉트박스: 슬릭한 플랫 다크 인풋 */
    input, textarea, div[data-baseweb="select"] > div {
        background-color: #141721 !important;
        border: 1px solid #232838 !important;
        border-radius: 8px !important;
        color: #f8fafc !important;
        font-size: 14px !important;
        transition: border-color 0.2s ease, box-shadow 0.2s ease;
    }
    input:focus, textarea:focus, div[data-baseweb="select"] > div:focus-within {
        border-color: #38bdf8 !important;
        box-shadow: 0 0 0 2px rgba(56, 189, 248, 0.15) !important;
    }
    div[data-baseweb="select"] * {
        color: #f8fafc !important;
    }
    input::placeholder, textarea::placeholder {
        color: #475569 !important;
    }

    /* 카드 컴포넌트: 글래스모피즘 & 미세 그라디언트 테두리 */
    .saas-card {
        background: linear-gradient(180deg, #131620 0%, #10121a 100%);
        border: 1px solid #1e2433;
        border-radius: 12px;
        padding: 22px 26px;
        margin-bottom: 16px;
        transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
    }
    .saas-card:hover {
        border-color: #2e384d;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5), 0 0 15px rgba(56, 189, 248, 0.08);
        transform: translateY(-2px);
    }

    /* 모던 칩 뱃지 */
    .chip-grade {
        background: rgba(56, 189, 248, 0.1);
        color: #38bdf8;
        border: 1px solid rgba(56, 189, 248, 0.25);
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 12px;
        font-weight: 600;
        letter-spacing: -0.2px;
        margin-right: 6px;
    }
    .chip-tag {
        background: #191e2b;
        color: #94a3b8;
        border: 1px solid #242b3d;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 12px;
        font-weight: 500;
        margin-right: 6px;
    }

    /* 액션 버튼 디자인 */
    .stButton > button {
        background-color: #171b26 !important;
        color: #cbd5e1 !important;
        border: 1px solid #283042 !important;
        border-radius: 8px !important;
        font-size: 13px !important;
        font-weight: 600 !important;
        padding: 6px 14px !important;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #0284c7 0%, #2563eb 100%) !important;
        color: #ffffff !important;
        border-color: #38bdf8 !important;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.25) !important;
        transform: translateY(-1px) !important;
    }

    /* 히어로 헤더 배너 */
    .hero-banner {
        background: radial-gradient(circle at 10% 20%, rgba(56, 189, 248, 0.08) 0%, transparent 40%),
                    radial-gradient(circle at 90% 80%, rgba(99, 102, 241, 0.08) 0%, transparent 40%);
        border: 1px solid #1a202c;
        border-radius: 14px;
        padding: 24px 28px;
        margin-bottom: 24px;
    }
</style>
""", unsafe_allow_html=True)

# 3. Supabase 연동 초기화
@st.cache_resource
def init_supabase():
    url = st.secrets.get("SUPABASE_URL", "")
    key = st.secrets.get("SUPABASE_KEY", "")
    if url and key:
        return create_client(url, key)
    return None

supabase = init_supabase()

# 4. 사이드바 구성
with st.sidebar:
    st.markdown("""
    <div style="display:flex; align-items:center; gap:8px; margin-bottom:4px;">
        <span style="font-size:22px;">⚡</span>
        <span style="font-size:18px; font-weight:800; color:#ffffff; letter-spacing:-0.5px;">SDH ACADEMY</span>
    </div>
    <div style="font-size:12px; color:#64748b; margin-bottom:20px;">캠퍼스 통합 내신·모의고사 자료실</div>
    """, unsafe_allow_html=True)
    
    menu = st.radio(
        "NAVIGATION",
        ["지문 데이터베이스", "자료 생성기", "기출 유형 세팅", "선생님 계정 관리"],
        index=0
    )
    
    st.divider()
    st.markdown("""
    <div style="padding: 12px; background: #131620; border-radius: 8px; border: 1px solid #1f2533;">
        <div style="font-size:11px; font-weight:700; color:#38bdf8; text-transform:uppercase; margin-bottom:4px;">ACTIVE PROFILE</div>
        <div style="font-size:14px; font-weight:700; color:#f1f5f9;">권희성 원장</div>
        <div style="font-size:12px; color:#64748b;">세종캠퍼스 · 최고관리자</div>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# 메뉴 1: 지문 데이터베이스
# ==========================================
if menu == "지문 데이터베이스":
    st.markdown("""
    <div class="hero-banner">
        <div style="font-size:13px; font-weight:700; color:#38bdf8; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:4px;">PASSAGE VAULT</div>
        <div style="font-size:26px; font-weight:800; color:#ffffff; letter-spacing:-0.5px; margin-bottom:6px;">지문 데이터베이스</div>
        <div style="font-size:14px; color:#94a3b8;">출판사 교과서 및 모의고사 지문을 정밀하게 아카이빙하고 자료를 추출합니다.</div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["🔍 아카이브 열람 (너른터형 탐색)", "➕ 신규 지문 등록"])

    with tab1:
        # 상단 필터 & 검색바
        with st.container():
            col1, col2, col3, col4 = st.columns([1.2, 1.2, 1.4, 2.8])
            with col1:
                f_grade = st.selectbox("학년", ["전체", "중1", "중2", "중3", "고1", "고2", "고3"])
            with col2:
                f_cat = st.selectbox("구분", ["전체", "교과서", "3월 모의고사", "6월 모의고사", "9월 모의고사", "11월 모의고사", "부교재"])
            with col3:
                f_pub = st.text_input("출판사/교육청", placeholder="예: NE능률, 교육청")
            with col4:
                f_query = st.text_input("통합 검색", placeholder="단원, 번호, 지문 키워드...")

        st.write("")

        # Supabase 지문 쿼리
        passages = []
        if supabase:
            try:
                q = supabase.table("passages").select("*")
                if f_grade != "전체":
                    q = q.eq("grade", f_grade)
                if f_cat != "전체":
                    q = q.eq("category", f_cat)
                res = q.order("id", desc=True).limit(30).execute()
                passages = res.data
            except Exception:
                passages = []

        if not passages:
            passages = [
                {
                    "id": 1,
                    "grade": "고1",
                    "category": "3월 모의고사",
                    "publisher": "서울시교육청",
                    "lesson": "20번",
                    "title": "부모의 개입 속도와 자녀의 독립적 문제해결력 간의 상관관계",
                    "original_text": "Though we are marching toward a more global, interconnected world, our children face challenges that demand critical problem solving. Giving them time to reflect without immediate interference is essential for cognitive autonomy..."
                },
                {
                    "id": 2,
                    "grade": "중2",
                    "category": "교과서",
                    "publisher": "NE능률(김기택)",
                    "lesson": "1과",
                    "title": "A Day at the Local Animal Care Shelter",
                    "original_text": "Last Saturday, Minho and his classmates visited the local animal shelter. They spent the whole morning cleaning kennels and walking abandoned dogs, learning the real value of empathy..."
                }
            ]

        st.markdown(f"<div style='font-size:13px; color:#64748b; margin-bottom:14px;'>검색 결과 총 <b style='color:#38bdf8;'>{len(passages)}</b>개의 지문</div>", unsafe_allow_html=True)

        # 모던 카드 뷰
        for item in passages:
            with st.container():
                st.markdown(f"""
                <div class="saas-card">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
                        <div>
                            <span class="chip-grade">{item.get('grade')}</span>
                            <span class="chip-tag">{item.get('category')}</span>
                            <span class="chip-tag">{item.get('publisher', '')}</span>
                            <span style="font-size:16px; font-weight:700; color:#ffffff; margin-left:6px;">{item.get('lesson')}</span>
                        </div>
                        <span style="font-size:12px; color:#475569; font-weight:500;">#{item.get('id')}</span>
                    </div>
                    <div style="font-size:16px; font-weight:700; color:#f8fafc; letter-spacing:-0.3px; margin-bottom:8px;">
                        {item.get('title') or '지문 타이틀 미입력'}
                    </div>
                    <div style="font-size:13.5px; color:#94a3b8; line-height:1.65; margin-bottom:16px;">
                        {item.get('original_text')[:180]}...
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # 액션 버튼 그룹
                b1, b2, b3, b4, _ = st.columns([1, 1, 1.2, 1.1, 2.2])
                with b1:
                    st.button("🔍 지문분석", key=f"btn_an_{item['id']}")
                with b2:
                    st.button("📖 단어장", key=f"btn_vc_{item['id']}")
                with b3:
                    st.button("📝 10단 워크북", key=f"btn_wb_{item['id']}")
                with b4:
                    st.button("⚡ 변형문제", key=f"btn_qz_{item['id']}")
                
                st.write("")

    with tab2:
        st.markdown("### ➕ 신규 지문 등록")
        st.caption("새로운 시험 본문과 해석을 데이터베이스에 정형 등록합니다.")
        
        with st.form("add_passage_form"):
            c1, c2, c3 = st.columns(3)
            with c1:
                in_grade = st.selectbox("대상 학년 *", ["중1", "중2", "중3", "고1", "고2", "고3"])
            with c2:
                in_cat = st.selectbox("출처 분류 *", ["교과서", "3월 모의고사", "6월 모의고사", "9월 모의고사", "11월 모의고사", "수능특강/부교재"])
            with c3:
                in_pub = st.text_input("출판사 / 기관", placeholder="예: NE능률, 교육청")

            c4, c5 = st.columns([1.2, 2.8])
            with c4:
                in_lesson = st.text_input("단원 / 문항 번호 *", placeholder="예: 2과 본문, 31번")
            with c5:
                in_title = st.text_input("지문 주제문 / 한줄 요약 (선택)", placeholder="지문의 핵심 토픽 또는 요약문")

            in_original = st.text_area("영어 원문 (Passage) *", height=200, placeholder="영어 문장을 복사하여 붙여넣으세요.")
            in_trans = st.text_area("한글 해석 (선택사항)", height=120, placeholder="해당 지문의 전문 해석을 입력하세요.")

            submit_btn = st.form_submit_button("지문 데이터베이스에 영구 등록", use_container_width=True)

            if submit_btn:
                if not in_original.strip() or not in_lesson.strip():
                    st.error("단원/번호와 영어 원문은 필수 입력 사항입니다.")
                elif not supabase:
                    st.warning("Supabase 열쇠 연동 후 실제 저장소에 기록됩니다.")
                else:
                    try:
                        payload = {
                            "grade": in_grade,
                            "category": in_cat,
                            "publisher": in_pub,
                            "lesson": in_lesson,
                            "title": in_title,
                            "original_text": in_original,
                            "korean_translation": in_trans
                        }
                        supabase.table("passages").insert(payload).execute()
                        st.success("지문이 데이터베이스에 성공적으로 아카이빙되었습니다!")
                    except Exception as err:
                        st.error(f"저장 오류: {err}")

# ==========================================
# 메뉴 2: 자료 생성기
# ==========================================
elif menu == "자료 생성기":
    st.markdown("""
    <div class="hero-banner">
        <div style="font-size:13px; font-weight:700; color:#818cf8; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:4px;">AUTOMATED ENGINE</div>
        <div style="font-size:26px; font-weight:800; color:#ffffff; letter-spacing:-0.5px; margin-bottom:6px;">자료 생성기</div>
        <div style="font-size:14px; color:#94a3b8;">원클릭으로 분석지, 10단계 워크북, 학교별 변형문제를 생성하고 A4 서식으로 조판합니다.</div>
    </div>
    """, unsafe_allow_html=True)

    gen_col1, gen_col2 = st.columns([1.1, 1.9])
    with gen_col1:
        st.markdown("##### 1. 대상 지문 범위")
        st.selectbox("교재/모의고사", ["2026년 고1 3월 모의고사", "2026년 고2 3월 모의고사", "중2 NE능률(김기택)"])
        st.multiselect("선택 문항", ["18번", "19번", "20번", "21번", "22번", "23번"], default=["20번", "21번"])
        
        st.markdown("##### 2. 패키지 구성")
        st.checkbox("지문 분석지 (구문 분석 + 해석)", value=True)
        st.checkbox("단어장 (표제어, 품사, 예문 빈칸)", value=True)
        st.checkbox("10단계 워크북 (빈칸, 어순, 어법선택 등)", value=True)
        st.checkbox("기출 스타일 변형문제 (객관식/서술형)", value=True)
        
        st.markdown("##### 3. 포맷 선택")
        st.radio("다운로드 포맷", ["DOCX (워드 A4 2단 서식)", "HWPX (한글 표준 양식)", "PDF 바로 인쇄용"])
        
        st.write("")
        st.button("🚀 자료 일괄 생성 시작", use_container_width=True)

    with gen_col2:
        st.markdown("##### 생성 미리보기 및 파일 아웃풋")
        st.markdown("""
        <div style="background-color:#10131c; border:1px dashed #242c3d; border-radius:12px; padding:65px 30px; text-align:center; color:#64748b;">
            <div style="font-size:32px; margin-bottom:12px;">📑</div>
            <div style="font-size:15px; font-weight:600; color:#94a3b8; margin-bottom:6px;">생성 대기 중</div>
            <div style="font-size:13px; line-height:1.6;">
                좌측에서 지문과 문항을 고르고 생성 버튼을 누르면<br>
                학원 로고와 2단 그리드가 맞춰진 인쇄용 파일이 즉시 렌더링됩니다.
            </div>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# 메뉴 3: 기출 유형 세팅
# ==========================================
elif menu == "기출 유형 세팅":
    st.markdown("""
    <div class="hero-banner">
        <div style="font-size:13px; font-weight:700; color:#38bdf8; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:4px;">FEW-SHOT TUNING</div>
        <div style="font-size:26px; font-weight:800; color:#ffffff; letter-spacing:-0.5px; margin-bottom:6px;">학교별 기출 유형 세팅</div>
        <div style="font-size:14px; color:#94a3b8;">캠퍼스 인근 고교의 실제 시험 스타일을 AI에 학습시켜 적중률 높은 문제를 만듭니다.</div>
    </div>
    """, unsafe_allow_html=True)

    school_list = ["세종고등학교", "아름고등학교", "도담고등학교", "양지고등학교", "새롬고등학교"]
    sel_school = st.selectbox("설정 대상 학교", school_list)

    st.write("")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"##### 📌 {sel_school} 출제 밸런스")
        st.number_input("어법상 틀린 것 모두 고르기 (복수정답) 비중 (%)", value=20)
        st.number_input("문맥상 부적절한 어휘 비중 (%)", value=25)
        st.number_input("서술형 조건 제시형 영작 비중 (%)", value=20)
        st.number_input("빈칸 추론 / 요약문 완성 비중 (%)", value=35)

    with c2:
        st.markdown("##### 📝 실제 기출 패턴 예시 (AI 가이드라인)")
        st.text_area("객관식 고난도 문제 예시", height=120, placeholder="[어법] 다음 밑줄 친 ⓐ~ⓔ 중 어법상 틀린 것의 개수는?")
        st.text_area("서술형 조건 영작 문제 예시", height=120, placeholder="[조건] <보기>의 단어를 모두 활용할 것...")

    st.button("💾 기출 템플릿 저장", use_container_width=True)

# ==========================================
# 메뉴 4: 선생님 계정 관리
# ==========================================
elif menu == "선생님 계정 관리":
    st.markdown("""
    <div class="hero-banner">
        <div style="font-size:13px; font-weight:700; color:#38bdf8; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:4px;">CAMPUS ACCESS</div>
        <div style="font-size:26px; font-weight:800; color:#ffffff; letter-spacing:-0.5px; margin-bottom:6px;">선생님 계정 관리</div>
        <div style="font-size:14px; color:#94a3b8;">SDH 캠퍼스 소속 강사진 계정을 발급하고 자료 권한을 관리합니다.</div>
    </div>
    """, unsafe_allow_html=True)

    col_admin1, col_admin2 = st.columns([1, 1.4])
    with col_admin1:
        st.markdown("##### ➕ 신규 강사 계정 발급")
        with st.form("new_teacher_form"):
            st.text_input("선생님 성함")
            st.text_input("아이디 (이메일)")
            st.text_input("초기 비밀번호", type="password")
            st.selectbox("소속 캠퍼스", ["세종 캠퍼스", "본원", "대전 캠퍼스"])
            st.multiselect("접근 권한 학년", ["중등부", "고1", "고2", "고3"], default=["고1", "고2"])
            st.form_submit_button("선생님 계정 발급 완료", use_container_width=True)

    with col_admin2:
        st.markdown("##### 👥 등록 강사진 현황")
        st.markdown("""
        | 강사명 | 캠퍼스 | 계정 | 담당 | 권한 |
        | :--- | :--- | :--- | :--- | :--- |
        | **권희성 원장** | 세종캠퍼스 | master@sdh.edu | 전 학년 | **최고 관리자** |
        | **김철수 T** | 세종캠퍼스 | kim_cs@sdh.edu | 고등부 | 자료실 정회원 |
        | **이영희 T** | 세종캠퍼스 | lee_yh@sdh.edu | 중등부 | 자료실 정회원 |
        """)
