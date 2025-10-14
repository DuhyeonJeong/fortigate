# FortiGate Block Script Maker (EXE via GitHub Actions)

이 리포는 **로컬 PC에 Python/Docker 설치 없이** GitHub Actions에서 Windows EXE를 만들어줍니다.

## 빠른 사용법
1. 이 폴더 통째로 GitHub 새 리포지토리에 업로드합니다.
2. GitHub → **Actions** → 우측 **Run workflow** 클릭 (또는 main 브랜치로 푸시해도 자동으로 실행).
3. 빌드 완료 후, Actions 실행 페이지의 **Artifacts**에서 `save_as_fortigate_exe`를 다운로드합니다.
4. 압축을 풀면 `save_as_fortigate.exe`가 있습니다. 더블클릭(또는 CMD)로 실행하세요.

## EXE 사용법 (CMD 예시)
```
save_as_fortigate.exe 10.13_유해IP.txt
```
옵션:
- `--no-dedupe` : 중복 제거 없이 그대로 모두 사용
- `--exclude-private` : 사설대역(10/8, 172.16/12, 192.168/16) 제외
- `--year 2025` : YYYYMMDD에 사용할 연도 지정(기본 2025)

## 동작 규칙
- 파일명에서 `MM.DD` 추출 → `YYYYMMDD`(기본 2025) 생성
- 내용에서는 IPv4만 추출(도메인/URL/국가명/기타 텍스트 무시)
- 원본 순서 유지 + **중복 제거**(기본). `--no-dedupe`로 비활성화 가능
- `fortigate_block_YYYYMMDD_script.txt`(UTF-8) 파일 생성

## 주의
- 일부 백신/EDR이 PyInstaller 산출물을 오탐지할 수 있습니다. 필요시 코드서명 권장.
- 콘솔 창 숨기려면 워크플로에서 `--noconsole` 추가 후 다시 빌드하세요.
