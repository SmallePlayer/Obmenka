#define ENCODER_LU1 3
#define ENCODER_LU2 1
#define ENCODER_RU1 2
#define ENCODER_RU2 0
#define ENCODER_LD1 30
#define ENCODER_LD2 32
#define ENCODER_RD1 34
#define ENCODER_RD2 9

volatile int encoderPositionLU = 0;
volatile int encoderPositionRU = 0;
volatile int encoderPositionLD = 0;
volatile int encoderPositionRD = 0;


void setup(){
  Serial.begin(9600);
  pinMode(ENCODER_LU1, INPUT);
  pinMode(ENCODER_LU2, INPUT);
  pinMode(ENCODER_RU1, INPUT);
  pinMode(ENCODER_RU2, INPUT);
  pinMode(ENCODER_LD1, INPUT);
  pinMode(ENCODER_LD2, INPUT);
  pinMode(ENCODER_RD1, INPUT);
  pinMode(ENCODER_RD2, INPUT);

  attachInterrupt(digitalPinToInterrupt(ENCODER_LU1),readEncoderLU,RISING);
  attachInterrupt(digitalPinToInterrupt(ENCODER_RU1),readEncoderRU,RISING);
  attachInterrupt(digitalPinToInterrupt(ENCODER_LD1),readEncoderLD,RISING);
  attachInterrupt(digitalPinToInterrupt(ENCODER_RD1),readEncoderRD,RISING);
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

void readEncoderLD(){
  if (digitalRead(ENCODER_LD1) == digitalRead(ENCODER_LD2)){
    encoderPositionLD++;
  }
  else{
    encoderPositionLD--;
  }
}


void readEncoderRD(){
  if (digitalRead(ENCODER_RD1) == digitalRead(ENCODER_RD2)){
    encoderPositionRD++;
  }
  else{
    encoderPositionRD--;
  }
}

void loop(){
  Serial.print("LU: ");
  Serial.print(encoderPositionLU);
  Serial.print(" | RU: ");
  Serial.print(encoderPositionRU);
  Serial.print(" | LD: ");
  Serial.print(encoderPositionLD);
  Serial.print(" | RD: "); 
  Serial.println(encoderPositionRD);
}