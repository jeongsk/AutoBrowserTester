# AutoBrowserTester

웹 브라우저 자동화 테스트 도구 - AI를 활용한 E2E 테스트 자동화 솔루션

## 소개

AutoBrowserTester는 Claude 3.5 Sonnet AI 모델을 활용하여 웹 애플리케이션의 E2E(End-to-End) 테스트를 자동화하는 도구입니다. 사용자는 엑셀 파일로 테스트 케이스를 정의하고, AI가 실제 브라우저를 조작하여 테스트를 수행합니다.

이 도구는 다음과 같은 장점을 제공합니다:
- 코드 작성 없이 테스트 자동화 가능
- 자연어로 테스트 케이스 정의
- 실제 브라우저 환경에서 테스트 수행
- 테스트 결과 시각화 및 보고서 생성

## 데모 비디오

[![AutoBrowserTester 데모](https://img.youtube.com/vi/b7mGRdDSs4Y/0.jpg)](https://youtu.be/b7mGRdDSs4Y)

위 이미지를 클릭하면 데모 비디오를 시청할 수 있습니다.

## 설치 방법

### 요구 사항
- Python 3.13 이상
- Anthropic API 키

### 설치 단계

1. 저장소 클론
   ```bash
   git clone https://github.com/jeongsk/AutoBrowserTester.git
   cd AutoBrowserTester
   ```

2. 가상 환경 설정 및 의존성 설치
   ```bash
   # uv 설치 (아직 설치하지 않은 경우)
   # macOS/Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh
   # Windows
   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
   
   # 의존성 설치 (uv.lock 파일을 읽어서 의존성 설치, 가상환경 자동 생성)
   uv sync
   # 개발 의존성을 제외하고 설치하려면 다음 명령어 사용
   # uv sync --no-dev
   
   # 가상 환경 활성화
   # Linux/macOS
   source .venv/bin/activate
   # Windows
   .venv\Scripts\activate
   ```

3. 환경 변수 설정
   ```bash
   cp .env.example .env
   ```
   `.env` 파일을 열고 `ANTHROPIC_API_KEY`에 유효한 API 키를 입력하세요.

## 사용 방법

1. Streamlit 앱 실행
   ```bash
   uv run -m streamlit run app.py
   ```

2. 웹 브라우저에서 Streamlit 앱 접속 (기본 URL: http://localhost:8501)

3. 테스트 케이스가 정의된 엑셀 파일 업로드
   - 예제 파일은 `example/단위 테스트 시나리오 샘플.xlsx`를 참고하세요.

4. "Run Test" 버튼을 클릭하여 테스트 실행

5. 테스트 결과 확인

## 테스트 케이스 작성 방법

테스트 케이스는 다음 열을 포함하는 엑셀 파일(.xlsx 또는 .ods)로 정의합니다:

| 테스트 케이스 ID | 기능 | 테스트 조건 | 입력 값 | 기대 결과 |
|-----------------|------|------------|---------|----------|
| TC001 | 로그인 | 유효한 사용자 정보로 로그인 | 아이디: user1, 비밀번호: pass123 | 로그인 성공 및 대시보드 표시 |

각 열의 의미:
- **테스트 케이스 ID**: 테스트 케이스의 고유 식별자
- **기능**: 테스트할 기능 또는 모듈
- **테스트 조건**: 테스트 수행을 위한 전제 조건
- **입력 값**: 테스트에 사용할 입력 데이터
- **기대 결과**: 테스트 성공 시 예상되는 결과

## 주요 기능

- **엑셀 파일 업로드**: 테스트 케이스가 정의된 엑셀 파일을 업로드하여 테스트 실행
- **AI 기반 브라우저 자동화**: Claude 3.5 Sonnet 모델이 자연어 지시에 따라 브라우저 조작
- **테스트 결과 시각화**: 테스트 결과를 시각적으로 표시하고 성공/실패 여부 확인
- **로그 및 스크린샷 저장**: 테스트 실행 과정의 로그와 스크린샷을 저장하여 디버깅 지원 (예정)
- **클립보드 지원**: 텍스트 복사 및 붙여넣기 기능 제공 (예정)

## 프로젝트 구조

```
AutoBrowserTester/
├── app.py                  # Streamlit 애플리케이션 메인 파일
├── custom_controller.py    # 사용자 정의 브라우저 컨트롤러
├── pyproject.toml          # 프로젝트 메타데이터 및 의존성
├── .env.example            # 환경 변수 예제 파일
├── example/                # 예제 파일 디렉토리
│   └── 단위 테스트 시나리오 샘플.xlsx  # 테스트 케이스 예제 파일
├── logs/                   # 테스트 로그 저장 디렉토리 (자동 생성)
└── recording/              # 테스트 녹화 파일 저장 디렉토리 (자동 생성)
```

## 의존성

- browser-use: 브라우저 자동화 라이브러리
- langchain-anthropic: Claude AI 모델 연동
- pandas: 데이터 처리
- streamlit: 웹 인터페이스
- openpyxl/odfpy: 엑셀/ODS 파일 처리
- pyperclip: 클립보드 조작

## 라이센스

이 프로젝트는 MIT 라이센스 하에 배포됩니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

## 기여 방법

1. 이 저장소를 포크합니다.
2. 새 기능 브랜치를 생성합니다 (`git checkout -b feature/amazing-feature`).
3. 변경 사항을 커밋합니다 (`git commit -m 'Add some amazing feature'`).
4. 브랜치에 푸시합니다 (`git push origin feature/amazing-feature`).
5. Pull Request를 생성합니다.
