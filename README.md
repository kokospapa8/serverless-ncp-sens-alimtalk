#Servereless Simple & Easy Notification Service alimtalk
네이버 클라우드 [Simple & Easy Notification Service](https://www.ncloud.com/product/applicationService/sens)의 알림톡 API를 AWS SAM을 사용해 서버리스로 배포할 수 있는 템플릿입니다.
AWS Lambda의 [Asnychronous invocation](https://docs.aws.amazon.com/ko_kr/lambda/latest/dg/invocation-async.html)을 사용해 백엔드 서버에서 
비동기적으로 알림을 보냅니다.


# 네이버 클라우드 프로젝트 및 카카오 채널 생성
- [프로젝트 생성](https://console.ncloud.com/sens/project) :생성후 서비스 ID 저장
- [카카오톡 채널 생성](https://guide.ncloud-docs.com/docs/ko/sens-sens-1-5) : 생성후 카카오톡 채널 아아디 저장 -> @kakaoid
- [알림톡 템플릿 생성](https://console.ncloud.com/sens/kakao-alimtalk-template) : 템플릿 코드 저장
- [계정 인증키 생(https://www.ncloud.com/mypage/manage/authkey) : Access Key ID 및 Secert Key 저장


# 빌드 및 배포 환경 설정
## AWS CLI 
아래부터는 MAC에서 설치및 배포 방법을 설명합니다 윈도우등 다른 OS에서는 [AWS SAM 문서](https://docs.aws.amazon.com/ko_kr/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)를 참고하세요.
```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
brew tap aws/tap
brew install aws-sam-cli
```

## AWS 자격증명 설정
[설정 문서참조](https://docs.aws.amazon.com/ko_kr/serverless-application-model/latest/developerguide/serverless-getting-started-set-up-credentials.html)

```
$ aws configure
AWS Access Key ID [None]: your_access_key_id
AWS Secret Access Key [None]: your_secret_access_key
Default region name [None]: 
Default output format [None]: 
```

## python 환경 
```
curl https://pyenv.run | bash
exec "$SHELL" 
pyenv install 3.8.8
pyenv virtualenv 3.8.8 serverless-sense-alimtalk
pyenv activate serverless-sense-alimtalk
pip install -r checkplus/requirements.txt 
```

# 빌드, 로컬테스트, 배포
## 빌드
```
sam build
```
## 로컬 test 
docker엔진이 설치 되어있어야 합니다.
event.json의 template code와 message를 등록한 포맷에 맞게 수정해야합니다. 메시지 발송시의 payload에 대한 자세한 설명은 [네이버 문서](https://api.ncloud-docs.com/docs/ko/ai-application-service-sens-alimtalkv2)를 확인하세요.
```
event.json

{
  "template_code": "<템플릿 코드>",
  "payload": [
        {
            "countryCode":"82",
            "to":"01012341234",
            "content": "test"

        },
        {
            "countryCode":"82",
            "to":"01012341235",
            "content": "test"

        }
  ]
}


```
environment 설정도 변경해야합니다. 
```
  PLUS_FIREND_ID:
    Type: String
    Default: "@kakao"
    Description: 카카오톡 채널명 ((구)플러스친구 아이디)
  SERVICE_ID:
    Type: String
    Default: ""
    Description: 프로젝트 등록 시 발급받은 서비스 아이디
  NAVER_ACCESS_KEY:
    Type: String
    Default: ""
    Description: 포탈 또는 Sub Account에서 발급받은 Access Key ID
  NAVER_SECRET_KEY:
    Type: String
    Default: ""
    Description: 포탈 또는 Sub Account에서 발급받은 Access Key ID

env.json
{
  "Parameters": {
    "PLUS_FIREND_ID": "",
    "SERVICE_ID": "",
    "NAVER_ACCESS_KEY": "",
    "NAVER_SECRET_KEY": ""

  }
}

```
다음 명령어로 로컬에서 실행가능합니다.  

```
sam local invoke -e events/event.json -n env.json
```


배포
```
sam deploy --guided
```

배포후 lambda configuration의 환경변수를 위에서 저장한 대로 설정해줘야한다.
```
  PLUS_FIREND_ID:
    Type: String
    Default: "@kakao"
    Description: 카카오톡 채널명 ((구)플러스친구 아이디)
  SERVICE_ID:
    Type: String
    Default: ""
    Description: 프로젝트 등록 시 발급받은 서비스 아이디
  NAVER_ACCESS_KEY:
    Type: String
    Default: ""
    Description: 포탈 또는 Sub Account에서 발급받은 Access Key ID
  NAVER_SECRET_KEY:
    Type: String
    Default: ""
    Description: 포탈 또는 Sub Account에서 발급받은 Access Key ID

```

# BE에서 lambda 호출
python boto3 예제
```

    payload = {
      "template_code": "test001",
      "messages": [
            {
                "countryCode": "82",
                "to": "01012341234"
                "content": "test message"

            }
      ]
    }
    lambda_client = boto3.client('lambda', region_name=settings.AWS_DEFAULT_REGION)
    ret = lambda_client.invoke(
        FunctionName=settings.LAMBDA_FUNCTION_NAMES['NotificaitonKakao'],
        InvocationType="DryRun" if settings.ENV == "test" else "Event",
        Payload=json.dumps(payload)
    )

```



