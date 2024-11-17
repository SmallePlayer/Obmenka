#define LU1 13
#define LU2 12
#define RU1 11
#define RU2 10
#define LD1 6
#define LD2 7
#define RD1 8
#define RD2 9

#define ENCODER_LU1 3
#define ENCODER_LU2 1
#define ENCODER_RU1 2
#define ENCODER_RU2 0

#define speed_forward 255
#define speed_back 250
#define speed_stop 0

volatile int encoderPositionLU = 0;
volatile int encoderPositionRU = 0;

void setup() {
  Serial.begin(9600);
  pinMode(ENCODER_LU1, INPUT);
  pinMode(ENCODER_LU2, INPUT);
  pinMode(ENCODER_RU1, INPUT);
  pinMode(ENCODER_RU2, INPUT);

  pinMode(LU1,OUTPUT);
  pinMode(LU2,OUTPUT);
  pinMode(RU1,OUTPUT);
  pinMode(RU2,OUTPUT);
  pinMode(LD1,OUTPUT);
  pinMode(LD2,OUTPUT);
  pinMode(RD1,OUTPUT);
  pinMode(RD2,OUTPUT);

  attachInterrupt(digitalPinToInterrupt(ENCODER_LU1),readEncoderLU,RISING);
  attachInterrupt(digitalPinToInterrupt(ENCODER_RU1),readEncoderRU,RISING);
}

void readEncoderRU(){
  if (digitalRead(ENCODER_RU1) == digitalRead(ENCODER_RU2)){
    encoderPositionRU++;
  }
  else{
    encoderPositionRU--;
  }
}

void readEncoderLU(){
  if (digitalRead(ENCODER_LU1) == digitalRead(ENCODER_LU2)){
    encoderPositionLU++;
  }
  else{
    encoderPositionLU--;
  }
}

void forward(){
  analogWrite(LU1,speed_forward);
  analogWrite(RU1,speed_forward);
  analogWrite(LD1,speed_forward);
  analogWrite(RD1,speed_forward);

  analogWrite(LU2,speed_stop);
  analogWrite(RU2,speed_stop);
  analogWrite(LD2,speed_stop);
  analogWrite(RD2,speed_stop);
}

void left(){
  digitalWrite(LU1,speed_stop);
  digitalWrite(RU1,speed_forward);
  digitalWrite(LD1,speed_stop);
  digitalWrite(RD1,speed_forward);

  digitalWrite(LU2,speed_back);
  digitalWrite(RU2,speed_stop);
  digitalWrite(LD2,speed_back);
  digitalWrite(RD2,speed_stop);

}

void right(){
  digitalWrite(LU1,speed_forward);
  digitalWrite(RU1,speed_stop);
  digitalWrite(LD1,speed_forward);
  digitalWrite(RD1,speed_stop);

  digitalWrite(LU2,speed_stop);
  digitalWrite(RU2,speed_back);
  digitalWrite(LD2,speed_stop);
  digitalWrite(RD2,speed_back);

}

void back(){
  digitalWrite(LU1,speed_stop);
  digitalWrite(RU1,speed_stop);
  digitalWrite(LD1,speed_stop);
  digitalWrite(RD1,speed_stop);

  digitalWrite(LU2,speed_back);
  digitalWrite(RU2,speed_back);
  digitalWrite(LD2,speed_back);
  digitalWrite(RD2,speed_back);

}

void stop(){
  digitalWrite(LU1,speed_stop);
  digitalWrite(RU1,speed_stop);
  digitalWrite(LD1,speed_stop);
  digitalWrite(RD1,speed_stop);

  digitalWrite(LU2,speed_stop);
  digitalWrite(RU2,speed_stop);
  digitalWrite(LD2,speed_stop);
  digitalWrite(RD2,speed_stop);
  
}

void loop() {
  Serial.print("LU: ");
  Serial.print(encoderPositionLU);
  Serial.print(" | RU: ");
  Serial.print(encoderPositionRU);


  // forward();
  // delay(2000);
  // left();
  // delay(1000);
  // right();
  // delay(1000);
  // back();
  // delay(1000);
  stop();
  delay(2000);

}
