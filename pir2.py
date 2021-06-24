import RPi.GPIO as GPIO
import time

from selenium import webdriver
import urllib

GPIO.setmode(GPIO.BCM)

pirPin = 7

GPIO.setup(pirPin, GPIO.IN, GPIO.PUD_UP)

detectednum = 0

while True:

    if GPIO.input(pirPin) == GPIO.LOW:

        print ("Motion detected!")
        detectednum += 1
        if (detectednum >= 10) :
            break

    else:

        print ("No motion")

    time.sleep(0.2)




while True:
    
    if (detectednum >= 10) :
    
        id = 'songsoo0037@naver.com' #카카오톡 아이디
        pw = 'kakaoss00.' #카카오톡 비밀번호

        KaKaoURL = 'https://accounts.kakao.com/login/kakaoforbusiness?continue=https://center-pf.kakao.com/'
        ChatRoom = 'https://center-pf.kakao.com/_dLeCs/chats/4812080438129747' #카카오톡챗봇 주소
        options = webdriver.ChromeOptions()
        #driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver')

 
        #user-agent 변경
        options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.187")
 
 
        #크롬 드라이버 로드
        driver = webdriver.Chrome('/lib/chromium-browser/chromedriver', options=options)
        driver.implicitly_wait(3)
         
 
        #카카오 메인 페이지 로드
        driver.get(KaKaoURL)
        time.sleep(3)
        
        #iframes = driver.find_elements_by_tag_name('iframe')
        #driver.switch_to.frame(len(iframes))
        #html = driver.page_source
        #soup = BeautifulSoup(html, 'html.parser')
        #soup.find()
        #soup.find_all()
        #driver.switch_to.default_content()
 
        #로그인
       # driver.execute_script("document.getElementsByName('id')[0].value=\'" + id + "\'")
        #time.sleep(1)
        #driver.execute_script("document.getElementsByName('pw')[0].value=\'" + pw + "\'")
        #time.sleep(1)
        #driver.find_element_by_xpath('//*[@id="frmNIDLogin"]/fieldset/input').click()
        
        driver.find_element_by_id('id_email_2').send_keys(id)
        driver.find_element_by_id('id_password_3').send_keys(pw)
        
        
        driver.find_element_by_xpath('//*[@id="login-form"]/fieldset/div[8]/button[1]').click()
        time.sleep(3)
 
  
        #채팅방 로드
        driver.get(ChatRoom)
        time.sleep(3)
        
    
        #글 작성
        driver.find_element_by_id('chatWrite').send_keys('테스트 메시지입니')  #메시지 작성
        #driver.find_element_by_xpath("//div[@class='box_tf']//button[@class='btn_g btn_submit']//button[@type='button']").click()  #전송버튼
        driver.find_element_by_xpath("//div[@class='wrap_inp']//button[@type='button']").click()
        #driver.find_element_by_xpath("//button[@class='btn_g btn_submit']//button[@type='button']").click()
        #<button class="btn_g btn_submit" type="button">전송</button>
        #driver.find_element(By.NAME, "q").send_keys("webdriver" + Keys.ENTER)
  
        driver.quit()
        time.sleep(60)
        break