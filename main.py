import base64
import streamlit as st
from openai import OpenAI


# -----------------------------------
# 페이지 설정
# -----------------------------------
st.set_page_config(
    page_title="하늘 사진으로 구름 종류 알아맞히기 ☁️",
    page_icon="☁️",
    layout="centered"
)


# -----------------------------------
# 제목
# -----------------------------------
st.title("☁️ 하늘 사진으로 구름 종류 알아맞히기")
st.write(
    "하늘 사진을 업로드하면 AI가 사진 속 구름을 분석하여 "
    "구름의 종류와 형성 고도, 예상되는 날씨를 알려줘요!"
)

st.info(
    "📸 구름이 잘 보이는 하늘 사진을 JPG 또는 PNG 형식으로 업로드해 주세요."
)


# -----------------------------------
# API 키 확인
# -----------------------------------
try:
    api_key = st.secrets["OPENAI_API_KEY"]
except Exception:
    st.error(
        "⚠️ OpenAI API 키를 찾을 수 없습니다.\n\n"
        "Streamlit Cloud의 Secrets에 다음과 같이 입력했는지 확인해 주세요:\n\n"
        "`OPENAI_API_KEY = \"여기에_API_키\"`"
    )
    st.stop()


client = OpenAI(api_key=api_key)


# -----------------------------------
# 이미지 업로드
# -----------------------------------
uploaded_file = st.file_uploader(
    "☁️ 하늘 사진을 업로드하세요",
    type=["jpg", "jpeg", "png"],
    help="JPG, JPEG, PNG 형식의 하늘 사진을 업로드할 수 있습니다."
)


# -----------------------------------
# 구름 분석 함수
# -----------------------------------
def analyze_cloud(image_bytes, image_type):
    """
    OpenAI Vision API를 이용하여 하늘 사진을 분석합니다.
    """

    # 이미지를 Base64로 변환
    base64_image = base64.b64encode(image_bytes).decode("utf-8")

    prompt = """
당신은 기상학과 구름 분류를 잘 알고 있는 AI입니다.

제공된 하늘 사진을 관찰하고 사진에 보이는 구름을 분석하세요.

반드시 다음 5대 운형 중 가장 적절한 하나를 선택하세요.

1. 적운
2. 권운
3. 층운
4. 적란운
5. 난층운
6. 잘 모르겠음


단, 사진만으로 정확한 구름 종류를 확정하기 어려운 경우에는
가장 가능성이 높은 종류를 선택하고 '사진만으로 판단한 추정'이라고 밝혀 주세요.

답변은 반드시 다음 형식을 지켜 주세요.

구름 종류:
[5대 운형 중 하나]

형성 고도:
[대략적인 고도 범위]

예상되는 날씨/기상 특성:
[해당 구름이 나타날 때 예상되는 날씨와 기상 특성을 2~3문장으로 설명]

판단 근거:
[사진에서 관찰되는 구름의 모양, 높이감, 배열, 투명도 등의 특징을 간단히 설명]

주의:
사진만으로 실제 기상 상황이나 향후 날씨를 확정할 수 없으며,
구름의 형태를 바탕으로 한 교육용 분석임을 마지막에 짧게 밝혀 주세요.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "당신은 구름과 기상 현상을 설명하는 "
                    "교육용 기상 분석 AI입니다."
                )
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": (
                                f"data:{image_type};base64,"
                                f"{base64_image}"
                            )
                        }
                    }
                ]
            }
        ],
        max_tokens=800
    )

    return response.choices[0].message.content


# -----------------------------------
# 업로드된 사진 처리
# -----------------------------------
if uploaded_file is not None:

    image_bytes = uploaded_file.getvalue()

    st.divider()

    st.subheader("📸 업로드한 하늘 사진")

    st.image(
        image_bytes,
        caption=uploaded_file.name,
        use_container_width=True
    )

    st.divider()

    # 분석 버튼
    if st.button(
        "☁️ AI에게 구름 종류 알아맞히기!",
        use_container_width=True
    ):

        with st.spinner("🔍 하늘 사진을 분석하고 있어요..."):

            try:
                result = analyze_cloud(
                    image_bytes,
                    uploaded_file.type
                )

                st.success("☁️ 분석이 완료되었습니다!")

                st.subheader("🔎 AI 구름 분석 결과")

                st.markdown(result)

            except Exception as e:

                st.error(
                    "❌ 사진을 분석하는 중 오류가 발생했습니다."
                )

                st.warning(
                    "다음 사항을 확인해 주세요.\n\n"
                    "• OpenAI API 키가 올바른지 확인\n"
                    "• OpenAI API 사용 권한 및 잔액 확인\n"
                    "• 인터넷 연결 상태 확인\n"
                    "• JPG 또는 PNG 이미지인지 확인\n\n"
                    f"오류 내용: `{str(e)}`"
                )

else:

    st.markdown(
        """
        ### 🌤️ 사용 방법

        **①** 위의 업로드 버튼을 눌러 하늘 사진을 선택하세요.

        **②** 사진이 화면에 나타나면  
        **「☁️ AI에게 구름 종류 알아맞히기!」** 버튼을 눌러주세요.

        **③** AI가 사진을 분석하여 다음 정보를 알려줍니다.

        - ☁️ **구름 종류**
        - ⛰️ **형성 고도**
        - 🌦️ **예상되는 날씨/기상 특성**
        - 🔍 **사진을 보고 그렇게 판단한 근거**
        """
    )


# -----------------------------------
# 하단 안내
# -----------------------------------
st.divider()

st.caption(
    "☁️ 이 앱은 AI를 활용한 교육용 구름 분류 프로젝트입니다. "
    "사진만으로 실제 날씨를 확정할 수는 없습니다."
)
