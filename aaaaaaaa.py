try:
  while True:
    while (a < 10):
      distance = measure_average()
      time.sleep(1)
      if (distance <= 30) : # 임의 숫자 / 일정 거리 이내에 사람이 감지됨
        a = a+1 # 감지 횟수를 1씩 증가시킴 - 초음파 센서 통해 1차 확인
        print(str(distance))
      else :
        a = 0 # 일정 거리 이내에 사람이 감지되지 않음 
            
    while (humanfound < 100):
      # 임의 숫자 / 사람 감지 횟수가 일정 횟수를 증가하면 다음 단계 진행 
      # capture frames from the camera
      for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
          img = frame.array
          gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
          gray = cv2.equalizeHist(gray)
          rects = detect(gray, fullbody_cascade)
          vis = img.copy()
          draw_rects(vis, rects, (0, 255, 0))

          # show the frame
          cv2.imshow("Frame", vis)
          key = cv2.waitKey(1) & 0xFF

          if len(rects)>0: # 사람이 한명이상 인식되면 
              humanfound += 1 # 사람 감지 횟수를 1씩 증가시킴 - 카메라 openCV 통해 2차 확인 
          else:
              humanfound = 0

          # clear the stream in preparation for the next frame
          rawCapture.truncate(0)
          print(str(humanfound))
                
      #record()
      app.app.run(host='0.0.0.0', debug=True, threaded=True) # 실시간 영상 스트리밍

      login()
      driver.find_element_by_id('chatWrite').send_keys('움직임이 감지되었습니다.') # 메세지 작성
      time.sleep(3)
      driver.find_element_by_xpath('//*[@id="kakaoWrap"]/div[1]/div[2]/div/div[2]/div[2]/form/fieldset/button').click() # 메세지 전송 버튼
      time.sleep(5)
      driver.find_element_by_xpath('//*[@id="kakaoWrap"]/div[1]/div[2]/div/div[2]/div[1]/div[1]/div[1]/button').click() # 파일 업로드 버튼
      driver.find_element_by_css_selector('#kakaoWrap > div.chat_popup > div.popup_body > div > div.write_chat2 > div.write_menu > div:nth-child(1) > div.upload_btn > input').send_keys('파일경로')
      # 짧은 영상 파일 전송 
      time.sleep(20) 
      driver.quit()
      time.sleep(60)
      a = 0

finally:
  GPIO.cleanup()
