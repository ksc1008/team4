# Better Chat-GPT

## 서비스 소개

Chat-GPT를 다양한 환경에서 활용할 수 있게, 음성인식 기능과 오버레이 기반 GUI를 접목한 애플리케이션 서비스입니다.

## 서비스 개발 배경
ChatGPT는 현재로서도 매우 좋은 성능을 보이고 있고, 빠르게 발전하고 있지만, ChatGPT를 더 편하게 활용하기 위한 여러 방법들을 고안하던 중, 음성인식 기능과 오버레이 기능을 활용하여 개선할 수 있겠다고 생각하여 개발하게 됨


## 서비스 목적 밎 대상
### 목적
- ChatGPT를 다양한 환경에서 더 효율적으로 사용할 수 있는 통합적 애플리케이션을 제공.
### 대상
- ChatGPT를 편하게 활용하고자 하는 모든 사용자.
- 인터넷 환경에 익숙하지 않거나, 키보드 입력에 불편함을 겪는 사용자. (노약자 / 장애인)

## 서비스 방식
![그림3](https://user-images.githubusercontent.com/54511614/233769776-f9ee83d0-28a2-46e9-a9cc-0b4780633291.jpg)
(full video)
(4 gifs)

## 기대효과
- 문서 편집, 영상 시청, 게임 등 다양한 작업 중 GPT가 필요한 상황에, 동시성을 확보해 줌으로써, 사용자가 방해받지 않고, 다중 사용 환경을 조성 가능
- 키보드 입력에 불편함을 겪거나 인터넷 환경에 접근하기 어려운 노약자 및 장애인에게 음성인식 기능을 탑재한 편리한 데스크톱 애플리케이션을 제공함으로써, 접근성 증진


## Quickstart
### OpenAI API Key 설정 (Windows)
시작 검색 > '시스템 환경 변수 편집' > 시스템 속성 > 환경 변수 > 시스템 변수 - 새로 만들기 > [변수 이름] 값을 "OPENAI_API_KEY" 로 지정 > [변수 값] 값에 OpenAI API Key 대입
### 개발 환경
python 3.10
### Start
파이썬 가상 환경 설정
```python
pip install -r requirements.txt
```
다음 명령어를 통해 서비스 시작
```
python3 main.py
``` 

## Usage

기본적으로 Push-To-Talk 방식으로 음성인식이 이루어집니다.   
[Ctrl + M]을 누르고 있으면, 마이크 녹음이 활성화 됩니다.
[Ctrl + M]을 떼면, 녹음이 종료됩니다.
ChatGPT 명령 수행이 끝나면 오버레이를 통해 응답 결과를 알려줍니다.

### Shortcuts

- [Ctrl+M]: 음성인식   
- [Ctrl+F3]: 답변 표기   
- [Ctrl+F4]: 답변 복사   
- [Ctrl+Q]: 종료


## LISCENSE
------------------------------------------------------------------------------
<a href="https://www.flaticon.com/free-icons/micro" title="micro icons">Micro icons created by Freepik - Flaticon</a>   

This project is licensed under the GPL 3.0 license. Please see the LICENSE file for more information.
