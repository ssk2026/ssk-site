# 문의 메일 설정

홈페이지 문의 양식은 Cloudflare Worker가 Resend API를 호출해
`psych.law.du@gmail.com`으로 전달합니다. API 키는 저장소에 넣지 않습니다.

## 1. Resend 발신 도메인 등록

1. Resend 계정을 만들고 **Domains > Add Domain**에서 `genairisk-ssk.com`을 추가합니다.
2. Resend가 안내하는 DNS 레코드를 Cloudflare DNS에 추가합니다.
3. Resend에서 도메인 상태가 **Verified**가 될 때까지 기다립니다.

## 2. API 키를 Cloudflare 비밀변수로 저장

1. Resend의 **API Keys**에서 발송 전용 API 키를 만듭니다.
2. Cloudflare Dashboard에서 `ssk-site` Worker를 엽니다.
3. **Settings > Variables and Secrets > Add**를 선택합니다.
4. 이름을 `RESEND_API_KEY`로 지정하고, 유형은 **Secret**으로 저장합니다.
5. Worker를 다시 배포합니다.

수신 주소와 발신 주소는 `wrangler.jsonc`의 `CONTACT_TO_EMAIL`,
`CONTACT_FROM_EMAIL`에서 관리합니다. API 키 값은 GitHub에 커밋하지 마세요.

## 3. 동작 확인

`https://genairisk-ssk.com/contact/`에서 테스트 문의를 한 번 보낸 뒤,
수신함과 스팸함을 모두 확인합니다. 수신된 메일의 **답장**을 누르면 방문자가
양식에 입력한 이메일 주소로 회신됩니다.
