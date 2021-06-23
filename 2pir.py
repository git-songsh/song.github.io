import RPi.GPIO as GPIO
import time
import time
import urllib

GPIO.setmode(GPIO.BCM)

pirPin = 7

GPIO.setup(pirPin, GPIO.IN, GPIO.PUD_UP)

detectednum = 0

while True:

    if GPIO.input(pirPin) == GPIO.LOW:

        print "Motion detected!"
        detectednum += 1
        if (detectednum >= 10) :
            break

    else:

        print "No motion"

    time.sleep(0.2)




while True:
    
    if (detectednum >= 10) :
    
        id = 'songsoo0037@naver.com' #카카오톡 아이디
        pw = 'kakaoss00' #카카오톡 비밀번호

        KaKaoURL = 'https://accounts.kakao.com/login/kakaoforbusiness?continue=https://center-pf.kakao.com/'
        ChatRoom = 'http://pf.kakao.com/_dLeCs' #카카오톡챗봇 주소
        options = webdriver.ChromeOptions()
 
 
        #user-agent 변경
        options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.187")
 
        #카카오 메인 페이지 로드
        driver.get(KaKaoURL)
        time.sleep(3)
        
        iframes = driver.find_elements_by_tag_name('iframe')
        driver.switch_to.frame(len(iframes))
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        soup.find()
        soup.find_all()
        driver.switch_to.default_content()
 
        #로그인 
        driver.find_element_by_id('loginEmail').send_keys(id)
        driver.find_element_by_id('loginPw').send_keys(pw)
        time.sleep(3)
 
  
        #채팅방 로드
        driver.get(ChatRoom)
        time.sleep(3)
        
    
        #글 작성
        driver.find_element_by_id('chatWrite').send_keys('라즈베리로봇 테스트 메시지입니다')  #메시지 작성
        driver.find_element_by_xpath("//div[@class='wrap_inp']//button[@type='button']").click()  #전송버튼
   
        driver.quit()
        time.sleep(60)
        break
