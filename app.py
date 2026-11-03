import streamlit as st
from supabase import create_client

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="SDH ACADEMY | 내신·모의고사 자료 시스템",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. 고급 다크 차콜 테마 CSS (시인성 및 대비 대폭 개선)
st.markdown("""
<style>
    /* 전체 배경: 완전 블랙 대신 눈이 편한 다크 차콜(#121316) */
    .stApp {
        background-color: #121316 !important;
        color: #f3f4f6 !important;
        font-family: -apple-system, BlinkMacSystemFont, "Apple SD Gothic Neo", "Pretendard", Roboto, sans-serif;
    }

    /* 상단 기본 헤더 투명화 처리 */
    header[data-testid="stHeader"] {
        background-color: #121316 !important;
    }

    /* 사이드바 스타일 개선 (글자 또렷하게) */
    [data-testid="stSidebar"] {
        background-color: #18191e !important;
        border-right: 1px solid #272830 !important;
    }
    [data-testid="stSidebar"] * {
        color: #d1d5db !important;
    }
    [data-testid="stSidebar"] h3, [data-testid="stSidebar"] h5 {
        color: #ffffff !important;
        font-weight: 700 !important;
    }

    /* 입력창 및 셀렉트박스 다크 스타일로 통일 (눈부심 방지) */
    input, select, textarea, div[data-baseweb="select"] > div {
        background-color: #1e2025 !important;
        color: #ffffff !important;
        border: 1px solid #32353e !important;
        border-radius: 6px !important;
    }
    div[data-baseweb="select"] * {
        color: #ffffff !important;
    }

    /* 지문 카드 스타일 (너른터 프리미엄 스타일) */
    .custom-card {
        background-color: #181a1f;
        border: 1px solid #282a32;
        border-radius: 10px;
        padding: 22px 24px;
        margin-bottom: 16px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    }
    .custom-card:hover {
        border-color: #3b82f6;
    }

    /* 뱃지 태그 */
    .badge-grade {
        background-color: #1d3557;
        color: #60a5fa;
        padding: 4px 10px;
        border-radius: 4px;
        font-size: 13px;
        font-weight: 700;
        margin-right: 6px;
    }
    .badge-cat {
        background-color: #272832;
        color: #9ca3af;
        padding: 4px 10px;
        border-radius: 4px;
        font-size: 13px;
        margin-right: 6px;
    }

    /* 액션 버튼 디자인 (지문분석, 워크북 등) */
    .stButton > button {
        background-color: #23262f !important;
        color: #e5e7eb !important;
        border: 1px solid #373b46 !important;
        border-radius: 6px !important;
        font-weight: 600 !important;
        padding: 6px 14px !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button:hover {
        background-color: #2563eb !important;
        color: #ffffff !important;
        border-color: #3b82f6 !important;
    }
</style>
""", unsafe_allow_html=True)

# 3. Supabase 클라이언트 초기화
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
    st.markdown("### ⚡ SDH ACADEMY")
    st.caption("캠퍼스 통합 내신·모의고사 자료 시스템")
    st.write("")
    
    menu = st.radio(
        "메뉴 바로가기",
        ["지문 데이터베이스", "자료 생성기", "기출 유형 세팅", "선생님 계정 관리"],
        index=0
    )
    
    st.divider()
    st.markdown("##### 👤 접속 교사 정보")
    st.markdown("**권희성 원장** (세종캠퍼스)")
    st.caption("권한: 최고 관리자 (Super Admin)")

# ==========================================
# 메뉴 1: 지문 데이터베이스
# ==========================================
if menu == "지문 데이터베이스":
    st.markdown("## 📚 지문 데이터베이스")
    st.markdown("<p style='color:#9ca3af; font-size:15px; margin-top:-10px;'>원문 및 분석용 지문을 검색하고, 신규 시험 지문을 등록합니다.</p>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["🔍 지문 검색 및 열람 (너른터형 목록)", "➕ 새 지문 등록"])

    with tab1:
        # 상단 필터 & 검색바
        col1, col2, col3, col4 = st.columns([1.2, 1.2, 1.5, 3])
        with col1:
            f_grade = st.selectbox("학년", ["전체", "중1", "중2", "중3", "고1", "고2", "고3"])
        with col2:
            f_cat = st.selectbox("구분", ["전체", "교과서", "3월 모의고사", "6월 모의고사", "9월 모의고사", "11월 모의고사", "부교재"])
        with col3:
            f_pub = st.text_input("출판사/교육청", placeholder="예: NE능률, 교육청")
        with col4:
            f_query = st.text_input("검색어 (단원, 제목, 본문 키워드)", placeholder="예: 20번, environmental, 3과")

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

        # 임시 샘플 데이터 (DB 지문이 없을 경우 표시)
        if not passages:
            passages = [
                {
                    "id": 1,
                    "grade": "고1",
                    "category": "3월 모의고사",
                    "publisher": "서울시교육청",
                    "lesson": "20번",
                    "title": "부모의 즉각적인 개입보다 스스로 해결할 시간 주기",
                    "original_text": "Though we are marching toward a more global, interconnected world, our children face challenges that demand critical problem solving. Giving them time to reflect is essential..."
                },
                {
                    "id": 2,
                    "grade": "중2",
                    "category": "교과서",
                    "publisher": "NE능률(김기택)",
                    "lesson": "1과",
                    "title": "A Day at the Animal Shelter",
                    "original_text": "Last Saturday, Minho and his classmates visited the local animal shelter. They spent the whole morning cleaning kennels and walking abandoned dogs..."
                }
            ]

        st.markdown(f"<p style='color:#9ca3af; font-size:14px; margin-bottom:14px;'>총 <b>{len(passages)}건</b>의 지문이 조회되었습니다.</p>", unsafe_allow_html=True)

        # 지문 카드 리스트
        for item in passages:
            with st.container():
                st.markdown(f"""
                <div class="custom-card">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                        <div>
                            <span class="badge-grade">{item.get('grade')}</span>
                            <span class="badge-cat">{item.get('category')}</span>
                            <span class="badge-cat">{item.get('publisher', '')}</span>
                            <strong style="font-size:17px; margin-left:8px; color:#ffffff;">{item.get('lesson')}</strong>
                        </div>
                        <span style="font-size:13px; color:#6b7280;">문항 ID: #{item.get('id')}</span>
                    </div>
                    <div style="font-size:16px; font-weight:700; color:#f3f4f6; margin-bottom:8px;">
                        {item.get('title') or '제목 미입력'}
                    </div>
                    <div style="font-size:14px; color:#9ca3af; line-height:1.6; margin-bottom:14px;">
                        {item.get('original_text')[:180]}...
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # 액션 버튼 열
                b1, b2, b3, b4, _ = st.columns([1.1, 1.1, 1.3, 1.1, 2.5])
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
        st.subheader("➕ 새 지문 등록")
        with st.form("add_passage_form"):
            c1, c2, c3 = st.columns(3)
            with c1:
                in_grade = st.selectbox("학년 *", ["중1", "중2", "중3", "고1", "고2", "고3"])
            with c2:
                in_cat = st.selectbox("구분 *", ["교과서", "3월 모의고사", "6월 모의고사", "9월 모의고사", "11월 모의고사", "부교재/수능특강"])
            with c3:
                in_pub = st.text_input("출판사 / 저자", placeholder="예: YBM(박준언), 교육청")

            c4, c5 = st.columns([1, 2])
            with c4:
                in_lesson = st.text_input("단원 / 번호 *", placeholder="예: 2과 본문, 31번")
            with c5:
                in_title = st.text_input("지문 제목 / 주제 (선택)", placeholder="지문의 핵심 주제문 또는 소제목")

            in_original = st.text_area("영어 원문 (Passage) *", height=200, placeholder="영어 문장을 복사하여 붙여넣으세요.")
            in_trans = st.text_area("한글 해석 (선택)", height=120, placeholder="대응되는 한글 해석이 있다면 입력하세요.")

            submit_btn = st.form_submit_button("지문 데이터베이스에 영구 저장")

            if submit_btn:
                if not in_original.strip() or not in_lesson.strip():
                    st.error("필수 항목(단원/번호, 영어 원문)을 입력해 주세요.")
                elif not supabase:
                    st.warning("Supabase 연결(Secrets) 완료 후 실제 DB에 반영됩니다.")
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
                        st.success("지문이 데이터베이스에 등록되었습니다!")
                    except Exception as err:
                        st.error(f"저장 실패: {err}")

# ==========================================
# 메뉴 2: 자료 생성기
# ==========================================
elif menu == "자료 생성기":
    st.markdown("## ⚡ 자료 생성기")
    st.markdown("<p style='color:#9ca3af; font-size:15px; margin-top:-10px;'>선택한 지문으로 [지문분석지 / 단어장 / 10종 워크북 / 변형문제]를 생성합니다.</p>", unsafe_allow_html=True)

    gen_col1, gen_col2 = st.columns([1, 1.8])
    with gen_col1:
        st.subheader("1. 대상 지문 선택")
        st.selectbox("교재/모의고사 선택", ["2026년 고1 3월 모의고사", "2026년 고2 3월 모의고사", "중2 NE능률(김기택)"])
        st.multiselect("생성할 지문 번호 선택", ["18번", "19번", "20번", "21번", "22번", "23번"], default=["20번", "21번"])
        
        st.subheader("2. 생성할 패키지 선택")
        st.checkbox("지문 분석지 (구문 분석 + 해석)", value=True)
        st.checkbox("단어장 (표제어, 품사, 예문 빈칸)", value=True)
        st.checkbox("10단계 워크북 (빈칸, 어순, 어법선택 등)", value=True)
        st.checkbox("기출 스타일 변형문제 (객관식/서술형)", value=True)
        
        st.subheader("3. 파일 출력 서식")
        st.radio("다운로드 포맷", ["DOCX (워드 A4 2단 서식)", "HWPX (한글 표준 양식)", "PDF 바로 인쇄용"])
        
        st.write("")
        st.button("🚀 자료 패키지 일괄 생성 시작")

    with gen_col2:
        st.subheader("미리보기 및 진행 상태")
        st.markdown("""
        <div style="background-color:#181a1f; border:1px dashed #373b46; border-radius:10px; padding:60px 30px; text-align:center; color:#9ca3af;">
            좌측에서 지문과 필요한 자료 유형을 선택한 뒤 [일괄 생성 시작]을 누르세요.<br><br>
            생성된 문서는 학원 규격(A4 2단)이 완벽히 적용되어 깨짐 없이 출력됩니다.
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# 메뉴 3: 기출 유형 세팅
# ==========================================
elif menu == "기출 유형 세팅":
    st.markdown("## 🎯 학교별 기출 유형 세팅")
    st.markdown("<p style='color:#9ca3af; font-size:15px; margin-top:-10px;'>인근 학교의 실제 출제 스타일을 등록하여 AI가 모방하도록 설정합니다.</p>", unsafe_allow_html=True)

    school_list = ["세종고등학교", "아름고등학교", "도담고등학교", "양지고등학교", "새롬고등학교"]
    sel_school = st.selectbox("설정할 대상 학교 선택", school_list)

    st.write("")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"#### 📌 {sel_school} 출제 문항 비중")
        st.number_input("어법상 틀린 것 모두 고르기 (복수정답) 비중 (%)", value=20)
        st.number_input("문맥상 부적절한 어휘 비중 (%)", value=25)
        st.number_input("서술형 조건 제시형 영작 비중 (%)", value=20)
        st.number_input("빈칸 추론 / 주제 요약 비중 (%)", value=35)

    with c2:
        st.markdown("#### 📝 대표 기출문제 예시 등록 (Few-Shot)")
        st.text_area("객관식 고난도 문제 예시", height=120, placeholder="[어법] 다음 밑줄 친 ⓐ~ⓔ 중 어법상 틀린 것의 개수는?")
        st.text_area("서술형 조건 영작 문제 예시", height=120, placeholder="[조건] <보기>의 단어를 모두 사용할 것, 필요시 어형 변화...")

    st.button("💾 학교별 기출 템플릿 저장")

# ==========================================
# 메뉴 4: 선생님 계정 관리
# ==========================================
elif menu == "선생님 계정 관리":
    st.markdown("## 👥 캠퍼스 선생님 계정 관리")
    st.markdown("<p style='color:#9ca3af; font-size:15px; margin-top:-10px;'>SDH 캠퍼스 강사진의 ID/PW를 발급하고 접근 권한을 관리합니다.</p>", unsafe_allow_html=True)

    col_admin1, col_admin2 = st.columns([1, 1.4])
    with col_admin1:
        st.subheader("신규 강사 계정 생성")
        with st.form("new_teacher_form"):
            st.text_input("선생님 성함")
            st.text_input("아이디 (이메일 형태)")
            st.text_input("초기 비밀번호", type="password")
            st.selectbox("소속 캠퍼스", ["세종 캠퍼스", "본원", "대전 캠퍼스"])
            st.multiselect("담당 학년", ["중등부", "고1", "고2", "고3"], default=["고1", "고2"])
            st.form_submit_button("선생님 계정 발급")

    with col_admin2:
        st.subheader("현재 등록된 선생님 목록")
        st.markdown("""
        | 이름 | 캠퍼스 | 아이디 | 담당 | 상태 |
        | :--- | :--- | :--- | :--- | :--- |
        | **권희성 (원장)** | 세종 | master@sdh.edu | 전 학년 | **관리자** |
        | **김철수 T** | 세종 | kim_cs@sdh.edu | 고등부 | 정상 승인 |
        | **이영희 T** | 세종 | lee_yh@sdh.edu | 중등부 | 정상 승인 |
        """)
