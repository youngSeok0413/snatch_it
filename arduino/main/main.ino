#define BAUDRATE 9600
#define SIGNAL  "a"
#define DELAY 30 // 1000/fps


void setup() {
  Serial.begin(BAUDRATE);
}

void loop() {
  if(isSnatched())
  {
    Serial.write(SIGNAL);
  }

  delay(DELAY);
}

bool isSnatched()
{
  return true;
}