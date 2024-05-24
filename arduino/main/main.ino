#define BAUDRATE 9600 //실험을 통해서 조정(조정 가능이 떨어지기는 함)
#define DELAY 30  // 실험을 통해서 조정
#define REF_VOLTAGE 2 // 실험을 통해서 조정

#define YES "y"
#define NO "n"

#define EMG_PIN  A0//emg pin number(회로 연결시 정할 것)

unsigned int SYS_MS = 0; //system control clock
double EMG_STACKED_DATA = 0;//stacked data(unit time : lms)

void setup() {
  Serial.begin(BAUDRATE);
}

void loop() {

  if (SYS_MS > DELAY) {
    if (isSnatched(EMG_STACKED_DATA))
      Serial.write(YES);
    else
      Serial.write(NO);

    EMG_STACKED_DATA = 0;
    SYS_MS = 0;
  } 
  else {
    EMG_STACKED_DATA += getEmgVal();
    SYS_MS++;
  }

  delay(1);
}

bool isSnatched(double stacked_data) {
  double avg = stacked_data/SYS_MS;

  if(avg > REF_VOLTAGE)
    return true;
  else
    return false;
}

int getEmgVal() {
  return analogRead(EMG_PIN);
}