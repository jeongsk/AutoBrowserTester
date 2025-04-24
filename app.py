"""
To use it, you'll need to install streamlit, and run with:

python -m streamlit run app.py

"""

import asyncio
import os
import sys
from typing import Optional, Union

import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from browser_use.browser.context import BrowserContext

# Ensure local repository (browser_use) is accessible
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from browser_use import Agent, BrowserContextConfig
from browser_use.browser.browser import Browser, BrowserConfig
from custom_controller import CustomController

# Load environment variables
load_dotenv()


config = BrowserContextConfig(
    locale="ko-KR",
    save_recording_path="recording",
    wait_for_network_idle_page_load_time=3.0,
)

browser = Browser(
    config=BrowserConfig(headless=False),
)

context = BrowserContext(browser=browser, config=config)


api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    st.error("Error: ANTHROPIC_API_KEY is not set. Please provide a valid API key.")
    st.stop()

llm = ChatAnthropic(
    model_name="claude-3-5-sonnet-20240620", timeout=25, stop=None, temperature=0.0
)

controller = CustomController()


# Streamlit UI
st.title("테스트 자동화 도구 🤖")

# 파일 업로드 섹션
st.subheader("엑셀/ODS 파일 업로드")
uploaded_file = st.file_uploader("파일을 선택해주세요", type=["xlsx", "ods"])


def parse_excel_file(file: Union[str, bytes]) -> Optional[pd.DataFrame]:
    try:
        if file.name.endswith(".xlsx"):
            df = pd.read_excel(file, engine="openpyxl")
        elif file.name.endswith(".ods"):
            df = pd.read_excel(file, engine="odf")
        else:
            st.error(
                "지원하지 않는 파일 형식입니다. .xlsx 또는 .ods 파일을 업로드해주세요."
            )
            return None

        # 빈 행 제거 (모든 컬럼이 NaN인 행)
        df = df.dropna(how="all")

        # 첫 번째 NaN이 발견된 행까지의 데이터만 사용
        first_nan_row = None
        for idx, row in df.iterrows():
            if row.isna().any():  # 행에 하나라도 NaN이 있으면
                first_nan_row = idx
                break

        if first_nan_row is not None:
            df = df.iloc[:first_nan_row]

        return df
    except Exception as e:
        st.error(f"파일 파싱 중 오류가 발생했습니다: {str(e)}")
        return None


if uploaded_file is not None:
    df = parse_excel_file(uploaded_file)
    if df is not None:
        st.session_state.df = df  # DataFrame을 session state에 저장
        st.success("파일이 성공적으로 업로드되었습니다!")
        st.dataframe(df, hide_index=True)  # 업로드된 데이터프레임을 표시


def create_task_prompt(row):
    """테스트 케이스 정보를 기반으로 Agent를 위한 프롬프트를 생성합니다."""
    return f"""
    다음 테스트 케이스를 수행해주세요:

    ## 테스트 ID: 
    {row["테스트 케이스 ID"]}
    -----------------------------

    ## 테스트할 기능: 
    {row["기능"]}
    -----------------------------
    
    ## 상세 조건:
    {row["테스트 조건"]}
    -----------------------------
    
    ## 사용할 입력 값:
    {row["입력 값"]}
    -----------------------------
    
    ## 최종적으로 확인해야 할 기대 결과:
    {row["기대 결과"]}"

    위 조건에 따라 웹 브라우저를 자동으로 조작하고, 최종 결과가 기대 결과와 일치하는지 확인 후 종료해주세요.
    """


if st.button("Run Test"):
    if "df" not in st.session_state or st.session_state.df is None:
        st.error("테스트를 실행하기 전에 엑셀 파일을 업로드해주세요.")
        st.stop()

    st.write("테스트 실행을 시작합니다...")
    results = []

    # 진행 상황을 표시할 프로그레스 바
    progress_bar = st.progress(0)
    status_text = st.empty()

    async def run_agent_for_test(row, total_tests):
        test_id = row["테스트 케이스 ID"]
        log_dir = f"logs/{test_id}"
        os.makedirs(log_dir, exist_ok=True)

        task_prompt = create_task_prompt(row)

        agent = Agent(
            task=task_prompt,
            llm=llm,
            use_vision=True,
            max_actions_per_step=1,
            browser=browser,
            controller=controller,
            browser_context=context,
            save_conversation_path=log_dir,
        )

        try:
            coroutine = await agent.run(max_steps=25)
            print(f"action_results: {coroutine.action_results()}")
            print(f"final_result: {coroutine.final_result()}")
            success = coroutine.is_successful()
            return test_id, success
        except Exception as e:
            st.error(f"테스트 {test_id} 실행 중 오류 발생: {str(e)}")
            return test_id, False

    async def run_all_tests():
        total_tests = len(df)

        for index, row in df.iterrows():
            status_text.text(f"테스트 케이스 {row['테스트 케이스 ID']} 실행 중...")
            result = await run_agent_for_test(row, total_tests)
            results.append(result)
            progress_bar.progress((index + 1) / total_tests)

        # 결과 표시
        st.write("## 테스트 결과")
        for test_id, success in results:
            color = "green" if success else "red"
            result_text = "성공 ✅" if success else "실패 ❌"
            st.markdown(f"테스트 {test_id}: :{color}[{result_text}]")
            # TODO: 실패인 경우 사유 기재
            # st.write(f"실패 사유: {reason}")  # 실패 사유를 기록하는 방법을 구현해야 함

        # 전체 요약
        total_success = sum(1 for _, success in results if success)
        st.write("\n### 요약")
        st.write(f"총 테스트: {len(results)}")
        st.write(f"성공: {total_success}")
        st.write(f"실패: {len(results) - total_success}")

        progress_bar.progress(1.0)
        status_text.text("모든 테스트가 완료되었습니다.")

    asyncio.run(run_all_tests())

    st.button("Close Browser", on_click=lambda: asyncio.run(browser.close()))
