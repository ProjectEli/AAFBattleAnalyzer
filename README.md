# AAF 전투 분석기
승패 통합 분석 | 렙차 페이즈 상관성 분석
:-------------------------:|:-------------------------:
![Figure_1](https://user-images.githubusercontent.com/16854214/152920777-2c66b778-fc89-45b5-a223-cb16cc04a90e.png) | ![Figure_12](https://user-images.githubusercontent.com/16854214/152920848-2cf3410a-8a2e-4feb-860a-5a142bc4ea50.png)
페이즈 통합 분석 | 수집품 분석
![Figure_31](https://user-images.githubusercontent.com/16854214/152921195-05b6360c-62d2-4126-b84c-2096f9b058cb.png) | ![Figure_40](https://user-images.githubusercontent.com/16854214/152921248-dc52c4e2-d49e-4d4d-a29d-597b8e75ecce.png)
몹별 승률 분석 | 몹별 스킬 발동률 분석
![Figure_11](https://user-images.githubusercontent.com/16854214/152931949-c41acc2b-91f5-4364-9886-15d5e96dd7b1.png) | ![image](https://user-images.githubusercontent.com/16854214/152927989-865e5975-627a-47e4-9a21-a02c94922fa0.png)

몹별 전투내역 상세분석 |
:-------------------------:|
![image](https://user-images.githubusercontent.com/16854214/152928203-f42bacad-9b34-40d5-97d4-3c999d028265.png) |

# 간단 소개
AAF 전투 페이지에서 저장한 html 전투 로그 파일을 모아서 분석하는 python 모듈 및 실행파일입니다. 대충 막 만들었으니 로직 위주로 참고하세요.

## 사용 방법
추후 작성

## 파일 구조
```
AAFBattleAnalyzer
│   README.md
│   AAFLog.db
│   AafLogArrange.py
│   AAFLogRegister.py
│   LICENSE
│   D2Coding-Ver1.3.2-20180524-all.ttc
└───src
│   │   __init__.py
│   │   AAFDbAnalyzer.py
│   │   AAFDbOperation.py
│   │   AAFFileManager.py
│   │   AAFLogCore.py
│   
└───Logset3
    │   2022_02_08_00_27_24.html
    │   2022_02_08_00_28_02.html
    │   ...
```

## 개발환경 및 사용 라이브러리
OS: Windows 11

Language: Python ( https://www.python.org/ )

IDE: Visual studio code ( https://code.visualstudio.com/ )

Virtual env: Miniconda ( https://conda.io/miniconda.html )

Log collection: Microsoft power automate desktop ( https://powerautomate.microsoft.com/ko-kr/desktop/ )

Html parsing: pyquery ( https://github.com/gawel/pyquery )

DB: python sqlite 3 built-in module ( https://docs.python.org/ko/3/library/sqlite3.html )

DBMS(optional): DBeaver ( https://dbeaver.io/ )

Graph plotting: matplotlib ( https://matplotlib.org/ )

## 라이센스
프로그램 자체: GNU GPLv3 (v1에서 MIT로 변경예정)

D2coding: [github 페이지](https://github.com/naver/d2codingfont), 라이센스 = [OpenFontLicense](https://github.com/naver/d2codingfont/wiki/Open-Font-License)
