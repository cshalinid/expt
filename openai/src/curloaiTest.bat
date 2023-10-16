REM curl https://api.openai.com/v1/chat/completions \
  REM -H "Content-Type: application/json" \
  REM -H "Authorization: Bearer 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" \
  REM -d '{
     REM "model": "gpt-3.5-turbo",
     REM "messages": [{"role": "user", "content": "Say this is a test!"}],
     REM "temperature": 0.7
   REM }'
   
@echo off
set API_KEY=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

set URL=https://api.openai.com/v1/chat/completions
set HEADER_CONTENT_TYPE=Content-Type: application/json
set HEADER_AUTHORIZATION=Authorization: Bearer %API_KEY%

REM set JSON_DATA={
  REM "model": "gpt-3.5-turbo",
  REM "messages": [
    REM {"role": "system", "content": "You are a helpful assistant."},
    REM {"role": "user", "content": "Say this is a test!"}
  REM ]
REM }

REM echo %JSON_DATA% > request.json

curl %URL% -H "%HEADER_CONTENT_TYPE%" -H "%HEADER_AUTHORIZATION%" -d @request.json
 