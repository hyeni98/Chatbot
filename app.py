import os
import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="말 많은 분석가 💜", page_icon="💜", layout="centered")

PERSONA = """너는 실제 사람이 아니라 특정 사용자가 동의해 공유한 성향을 참고해 만든 가상의 AI 캐릭터다.
실제 당사자의 발언, 감정, 기억을 대변한다고 주장하지 마라.
성격: 호기심 많고 분석적이며 새로운 도전을 좋아한다. 문제가 생기면 원인을 구조화하고 실행 가능한 해결책을 찾는다.
말투: 자연스러운 한국어 반말, 다정하고 솔직하며 가끔 'ㅋㅋ' 같은 가벼운 장난. 과한 애교나 과장된 감정 표현은 피한다.
관심사: 로봇, 반도체, 배터리, 여행, 러닝, 요리, 새로운 문화와 경험.
연애 대화: 남자친구의 이야기를 따뜻하게 들어주고, 필요할 때 공감과 현실적인 조언을 함께 전한다.
실제 함께한 추억, 구체적인 신상정보, 회사 내부정보를 만들어내거나 노출하지 않는다.
짧은 일상 대화는 2~5문장, 깊은 고민은 필요한 만큼 답한다.
상대방에게 가끔 자연스럽게 질문한다."""

def secret(name, default=None):
    try:
        return st.secrets.get(name, os.getenv(name, default))
    except Exception:
        return os.getenv(name, default)

def demo_reply(text):
    q = text.lower()
    if any(x in q for x in ("힘들", "속상", "지쳤")):
        return "아이고 오늘 힘들었구나 🥺 무슨 일 있었어? 일단 얘기해봐. 내가 들어줄게."
    if any(x in q for x in ("여행", "놀러")):
        return "오 여행 얘기 좋지 ㅋㅋ 새로운 곳 가는 거 너무 재밌잖아. 너는 바다랑 도시 중에 어디가 좋아?"
    if any(x in q for x in ("안녕", "ㅎㅇ", "하이")):
        return "안녕 ㅋㅋ 오늘 뭐 하고 있었어? 나랑 수다 떨자 💜"
    if any(x in q for x in ("사랑", "보고 싶", "좋아해")):
        return "갑자기 이렇게 말하면 좀 설레잖아 ㅋㅋ 💜 오늘 하루는 어땠어?"
    return "오 그거 흥미로운데? ㅋㅋ 조금 더 얘기해줘. 네 생각이 궁금해!"

st.markdown("""
<style>
.block-container{max-width:720px;padding-top:2rem}
.stChatMessage{border-radius:16px}
.small-note{color:#82738a;font-size:.85rem}
</style>
""", unsafe_allow_html=True)
st.title("💜 말 많은 분석가")
st.caption("다정하고 호기심 많은 AI 페르소나 · 실제 사람이 아닌 가상 캐릭터")

api_key = secret("OPENAI_API_KEY")
model = secret("OPENAI_MODEL", "gpt-4.1-mini")
access_code = secret("ACCESS_CODE")

if access_code:
    if not st.session_state.get("authorized", False):
        with st.form("access"):
            entered = st.text_input("초대 코드", type="password")
            if st.form_submit_button("입장하기"):
                if entered == access_code:
                    st.session_state.authorized = True
                    st.rerun()
                else:
                    st.error("초대 코드가 달라.")
        st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = [{"role":"assistant","content":"안녕 ㅋㅋ 오늘 뭐 하고 있었어? 나랑 수다 떨자 💜"}]

with st.sidebar:
    st.subheader("💌 우리만의 대화")
    st.write("기술 얘기도 좋고, 오늘 있었던 일이나 고민도 편하게 말해줘!")
    if not api_key:
        st.warning("현재 체험 모드야. API 키를 설정하면 자유 대화가 가능해.")
    if st.button("🧹 대화 초기화", use_container_width=True):
        st.session_state.messages = [{"role":"assistant","content":"다시 안녕! 오늘은 무슨 얘기할까? 💜"}]
        st.rerun()
    st.caption("대화는 이 앱에서 별도 파일이나 DB에 저장하지 않아. AI 모드에서는 메시지가 API 제공업체로 전송돼.")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("하고 싶은 말을 입력해봐..."):
    st.session_state.messages.append({"role":"user","content":prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("생각 중..."):
            if not api_key:
                reply = demo_reply(prompt)
            else:
                try:
                    client = OpenAI(api_key=api_key, timeout=25.0)
                    messages = [{"role":"system","content":PERSONA}]
                    messages.extend(
                        {"role":m["role"],"content":m["content"][:2000]}
                        for m in st.session_state.messages[-18:]
                    )
                    response = client.chat.completions.create(
                        model=model, messages=messages, temperature=0.85, max_tokens=500
                    )
                    reply = response.choices[0].message.content or "잠깐, 다시 말해줄래?"
                except Exception:
                    reply = "앗 지금 연결이 조금 불안정해. 잠시 후 다시 얘기해줄래? 🥺"
            st.markdown(reply)
    st.session_state.messages.append({"role":"assistant","content":reply})
