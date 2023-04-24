import openai
import speech_recognition as sr
import pyttsx3
import env


# OpenAI API 인증 정보
openai.api_key = env.OPEN_AI_KEY

# 음성 인식 모듈 초기화
r = sr.Recognizer()

# 음성 출력 모듈 초기화
engine = pyttsx3.init()

# 사용자가 '그만'이라고 말할 때까지 대화를 이어나감
while True:
    # 사용자 음성 입력
    with sr.Microphone() as source:
        print("말씀해주세요.")
        audio = r.listen(source)

    # 사용자 음성을 텍스트로 변환
    try:
        text = r.recognize_google(audio, language='ko-KR')
        print("당신 : " + text)

        # 사용자가 '그만'이라고 말하면 대화 종료
        if text == '그만':
            break

        # OpenAI API를 사용하여 응답 생성
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": text
                }
            ],
        )
        print(response)
        # 응답에서 텍스트 추출
        # result = response.choices[0].content.strip()
        result = response.choices[0].message.content.strip()
        # 응답을 음성으로 출력
        engine.say(result)
        print("챗봇 : " + result)
        engine.runAndWait()

        # 응답 텍스트 출력
        print(result)

    except sr.UnknownValueError:
        print("죄송합니다. 이해하지 못했습니다.")
        engine.say("죄송합니다. 이해하지 못했습니다.")
        engine.runAndWait()
    except sr.RequestError as e:
        print("음성 인식 서비스에 접근할 수 없습니다; {0}".format(e))
        engine.say("음성 인식 서비스에 접근할 수 없습니다.")
        engine.runAndWait()
