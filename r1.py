from selenium import webdriver
from datetime import datetime
from PIL import Image
import time
import configparser
import urllib

myCity = '광주 광산구 첨단1동'
naver_input = urllib.parse.quote(myCity + ' 날씨')
WeatherURL = 'https://search.naver.com/search.naver?ie=utf8&query='+ naver_input
AlertTime = 8 #매일 날씨를 알려줄 시간 (오전 여덟시)

while True:
    
    if (datetime.now().hour > AlertTime) :
 
        #알리기
        #Config = configparser.ConfigParser()
 
        #카카오 아이디, 비밀번호 불러옴
        #Config.read('info.conf')
        #Config = Config['MAIN']

        id = '' #여기에 본인 카톡 로그인 이메일
        pw = '' #여기에 본인 비밀번호

        KaKaoURL = 'https://accounts.kakao.com/login/kakaoforbusiness?continue=https://center-pf.kakao.com/'
        ChatRoom = '' #여기에 본인이 만든 카톡 채널 주소
        options = webdriver.ChromeOptions()
 
 
        #user-agent 변경
        options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.187")
 
        #크롬 드라이버 로드
        driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver', options=options)
        driver.implicitly_wait(3)
 
 
        #날씨 페이지 로드
        driver.get(WeatherURL)
 
 
        #스크린샷 저장
        screenshot_name = "/home/pi/Documents/kakao_robot/weather.png" #저장소에 따라 파일 이름 바뀜
        driver.save_screenshot(screenshot_name)
 
        #스크린샷 불러오기
        img = Image.open('/home/pi/Documents/kakao_robot/weather.png')
        cutted_img = img.crop((39,210,622,677))
        cutted_img.save('/home/pi/Documents/kakao_robot/weather.png')
 
 
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
        driver.find_element_by_id('countryCodeRequired').find_element_by_xpath("//button[@type='submit']").click()
        time.sleep(3)
 
 
 
        #채팅방 로드
        driver.get(ChatRoom)
        time.sleep(3)
        
       
 
        #글 작성
        driver.find_element_by_id('chatWrite').send_keys('라즈베리로봇 테스트 메시지입니다')  #메시지 작성
        driver.find_element_by_xpath("//input[@class='custom uploadInput']").send_keys('/home/pi/robot/weather.png') #날씨 사진 전송
        time.sleep(1)
        driver.find_element_by_xpath("//div[@class='wrap_inp']//button[@type='button']").click()  #전송버튼
   
        driver.quit()
        time.sleep(60)
        break
