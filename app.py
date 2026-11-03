import streamlit as st
from supabase import create_client

# 페이지 기본 설정 (다크 테마 및 넓은 레이아웃)
st.set_page_config(page_title="SDH 내신자료실", layout="wide", page_icon="📚")

# 대표 원장님 스타일의 다크 에메랄드 커스텀 디자인 CSS
st.markdown("""
<style>
    .stApp {
        background-color: #0d1412;
        color: #e0e8e3;
    }
    .header-card {
        background: linear-gradient(135deg, #122820 0%, #17382c 100%);
        border: 1px solid #1f4d3c;
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 25px;
    }
    .badge-btn {
        background-color: #1a2f26;
        border: 1px solid #2a5241;
        color: #8be0b2;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 13px;
        display: inline-block;
        margin-right: 6px;
    }
</style>
""", unsafe_allow_html=True)

# Supabase 클라이언트 연결 설정
@st.cache_resource
def get_supabase():
    url = st.secrets.get("SUPABASE_URL", "")
    key = st.secrets.get("SUPABASE_KEY", "")
    if url and key:
        return create_client(url, key)
    return None

supabase = get_supabase()

# 상단 헤더 배너
st.markdown("""
<div class="header-card">
    <div style="font-size: 13px; color: #4ade80; font-weight: 600; margin-bottom: 6px;">2022 개정 · 중고등 영어</div>
    <div style="font-size: 28px; font-weight: 700; color: #ffffff; margin-bottom: 8px;">SDH 내신자료실</div>
    <div style="font-size: 14px; color: #94a3b8;">교과서·모의고사 단원별 자료 및 변형문제 자동 생성 시스템 (캠퍼스 교사용)</div>
</div>
""", unsafe_allow_html=True)

# 사이드바 메뉴 구성
with st.sidebar:
    st.title("📂 학년 선택")
    grade = st.radio(
        "학년을 선택하세요",
        ["중1", "중2", "중3", "고등 공통영어1", "고등 공통영어2", "영어I", "영어II"],
        index=1
    )
    st.divider()
    page_mode = st.radio("작업 선택", ["자료 조회 및 다운로드", "새 지문 등록하기"])

# 1. 새 지문 등록하기 화면
if page_mode == "새 지문 등록하기":
    st.subheader(f"📝 {grade} 새 지문 데이터베이스 등록")
    
    with st.form("passage_form"):
        col1, col2 = st.columns(2)
        with col1:
            category = st.selectbox("구분", ["교과서", "3월 모의고사", "6월 모의고사", "9월 모의고사", "11월 모의고사", "수능특강/부교재"])
            publisher = st.text_input("출판사/저자 (예: NE능률 김기택, 교육청)")
        with col2:
            lesson = st.text_input("단원/번호 (예: 1과, 20번, 21번)")
            title = st.text_input("지문 제목 / 주제 (선택)")

        original_text = st.text_area("영어 원문 (English Passage)", height=220, placeholder="영어 본문 지문을 붙여넣으세요.")
        korean_translation = st.text_area("한글 해석 (선택사항)", height=150, placeholder="해당 지문의 한글 해석을 붙여넣으세요.")

        submit = st.form_submit_button("지문 데이터베이스에 저장")

        if submit:
            if not original_text.strip() or not lesson.strip():
                st.error("단원/번호와 영어 원문은 필수 입력 사항입니다.")
            elif not supabase:
                st.warning("Supabase 열쇠가 아직 등록되지 않아 임시 저장되었습니다. (다음 단계에서 연결)")
            else:
                try:
                    data = {
                        "grade": grade,
                        "category": category,
                        "publisher": publisher,
                        "lesson": lesson,
                        "title": title,
                        "original_text": original_text,
                        "korean_translation": korean_translation
                    }
                    supabase.table("passages").insert(data).execute()
                    st.success("지문이 성공적으로 데이터베이스에 등록되었습니다!")
                except Exception as e:
                    st.error(f"저장 중 오류 발생: {e}")

# 2. 자료 조회 및 다운로드 화면 (대표 원장님 스타일 테이블)
else:
    st.subheader(f"📑 {grade} 등록 자료 및 생성 목록")
    
    # 필터 옵션
    f_col1, f_col2 = st.columns([1, 2])
    with f_col1:
        st.write("**자료 유형:**")
        st.markdown("""
        <span class="badge-btn">전체</span>
        <span class="badge-btn">지문분석지</span>
        <span class="badge-btn">단어장</span>
        <span class="badge-btn">워크북</span>
        <span class="badge-btn">변형문제</span>
        """, unsafe_allow_html=True)
    
    st.write("")
    
    # 지문 목록 불러오기
    passages = []
    if supabase:
        try:
            res = supabase.table("passages").select("*").eq("grade", grade).order("id", desc=True).execute()
            passages = res.data
        except Exception:
            passages = []

    if not passages:
        st.info(f"현재 {grade}에 등록된 지문이 없습니다. 왼쪽 메뉴에서 **'새 지문 등록하기'**를 눌러 첫 지문을 넣어보세요!")
    else:
        for p in passages:
            with st.container():
                st.markdown(f"""
                <div style="background-color: #14221d; border: 1px solid #234839; border-radius: 8px; padding: 16px; margin-bottom: 12px;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-size: 16px; font-weight: bold; color: #4ade80;">[{p.get('category')}] {p.get('publisher', '')} - {p.get('lesson')}</span>
                        <span style="font-size: 12px; color: #94a3b8;">{p.get('created_at', '')[:10]}</span>
                    </div>
                    <div style="margin-top: 6px; font-size: 14px; color: #cbd5e1;">{p.get('title') or (p.get('original_text')[:90] + '...')}</div>
                </div>
                """, unsafe_allow_html=True)
                
                # 버튼 열
                b1, b2, b3, b4 = st.columns(4)
                with b1:
                    st.button(f"지문분석지 생성", key=f"ana_{p['id']}")
                with b2:
                    st.button(f"단어장 생성", key=f"voc_{p['id']}")
                with b3:
                    st.button(f"워크북 생성", key=f"wb_{p['id']}")
                with b4:
                    st.button(f"변형문제 40제 생성", key=f"q_{p['id']}")
