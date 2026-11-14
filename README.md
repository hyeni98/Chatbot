# Streamlit 여자친구 페르소나 챗봇 💜

## 로컬 실행
```bash
pip install -r requirements.txt
streamlit run app.py
```

API 키가 없으면 체험 모드로 실행됩니다.

## Streamlit Community Cloud 배포
1. 이 폴더의 `app.py`, `requirements.txt`, `.gitignore`를 GitHub 저장소에 업로드합니다.
2. https://share.streamlit.io 에서 저장소를 연결하고 메인 파일 `app.py`를 선택합니다.
3. 앱의 **Secrets** 설정에 다음을 입력합니다.

```toml
OPENAI_API_KEY = "여기에_본인의_OpenAI_API_키"
OPENAI_MODEL = "gpt-4.1-mini"
ACCESS_CODE = "남자친구와_공유할_초대코드"
```

4. 배포된 URL을 남자친구에게 보내고 초대 코드를 별도로 전달합니다.

**주의:** API 키를 코드나 GitHub에 직접 넣지 마세요. `ACCESS_CODE`는 간단한 접근 제한이며 강력한 사용자 인증 수단은 아닙니다. API 사용 요금이 발생할 수 있고 ChatGPT Plus와 별도 과금입니다. 공개 배포 시 사용량·비용을 모니터링하세요. 대화는 Streamlit 세션에서만 유지되며 AI 모드에서는 OpenAI API로 전달됩니다.

## 수정
- `PERSONA`: 성격, 말투, 반응 스타일
- `st.title`: 챗봇 이름
- 첫 메시지: `st.session_state.messages`의 초기 문구

실제 사람의 감정·기억을 재현하거나 대변하는 서비스가 아닌 가상 캐릭터입니다.
