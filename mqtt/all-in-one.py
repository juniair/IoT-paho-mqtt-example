import RPi.GPIO as gpio
import dht11
import time
import datetime

# GPIO 핀 정의 및 데이터 초기
trig_pin = 13
echo_pin = 19
# GREEN LED PIN: 16
# YELLOW LED PIN: 16
# RED LED PIN: 21
LED = (16, 20, 21)
instance = None
distance = None
temperature = None

# 함수 정의
# GPIO 핀 초기화
def init_gpio():
    global instance
    # setwarnings(False): 다른 시스템에서 사용시 warning 메시지 무시
    gpio.setwarnings(False)
    
    # 라즈베리파이 B+ 보드로 설정
    gpio.setmode(gpio.BCM)
    
    # 초음파 pin 설정
    gpio.setup(trig_pin, gpio.OUT)
    gpio.setup(echo_pin, gpio.IN)
    
    # 온도/ 습도 핀 설정
    instance = dht11.DHT11(pin = 12)
    
    # LED 핀 설정
    for pin in LED:
        gpio.setup(pin, gpio.OUT)
    
# LED 출력 설정 함수
def set_blink(LED, values):
    # 해당 LED에 맞는 value 값을 출력
    for index in range(0, 3):
        gpio.output(LED[index], values[index]);

# 초음파 거리에 따른 LED 출력값 선택 함수
def select_led(distance):

    
    if distance >= 100.0: # 거리가 100cm 이상
        # GREEN LED는 ON, 나머지는 OFF
        set_blink(LED, (True, False, False))    
    elif 30.0 <= distance and distance < 100.0: # 30cm이상 100cm 미만
        # YELLOW LED는 ON, 나머지는 OFF
        set_blink(LED, (False, True, False))
    else:   # 30cm 미만
        # RED LED는 ON, 나머지는 OFF
        set_blink(LED, (False, False, True))
# 온도 기준치 확인 함수        
def is_temp(temp):
    return temp <= 20

#초음파 센서 동작 함수
def run_wave():
    global distance
    gpio.output(trig_pin, False)
    time.sleep(1)
    gpio.output(trig_pin, True)
    time.sleep(0.00001)
    gpio.output(trig_pin, False)
        
    while gpio.input(echo_pin) == 0:
        pulse_start = time.time()
        
    while gpio.input(echo_pin) == 1:
        pulse_end = time.time()

    pulse_dration = pulse_end - pulse_start
    distance = pulse_dration * 17000
    distance = round(distance, 2)

# 온도/습도 센서 동작 함수
def run_temp():
    global temperature
    result = instance.read()
    
    # 유효한 값 입력 확인
    """ 
         유효한 값이 들어오면 들어온 시간과 값을 출력한다.
        이 때 해당 온도가 기준치 온도 이상인 경우 False를 반환 하고
        이하인 경우 True 값을 반환한다.
         유효한 값이 안들어 온 경우 최근에 들어온 온도 값으로 기준치 온도를
         비교하여 True나 False를 반환한다. 
    """
    if result.is_valid(): # True
        
        print "Last valid input: " + str(datetime.datetime.now())
        print "Temperature: %d C" % result.temperature
        
        temperature = result.temperature

        if is_temp(temperature):
            return True
        else:
            return False
    else: #False
        if is_temp(temperature):
            return True
        else:
            return False

        
# GPIO 초기화
init_gpio()

try:
    while True:
        run_wave() # 초음파센서 값 읽기
        if run_temp(): # 온도/습도 센서 결과에 따른 처리
            print "Distance:", distance, "cm"
            select_led(distance)    # 거리에 따른 LED 선택
        else:   # 온도가 기준치 이상인 경우
            # 모든 LED OFF
            set_blink(LED, (False, False, False))
except KeyboardInterrupt:
    gpio.cleanup()
