#define Encod_Left_Forward 1
#define Encod_Right_Forward 2
#define Encod_Left_Back 3
#define Encod_Right_Back 4

volatile int score_ELF = 0;
volatile int score_ERF = 0;
volatile int score_ELB = 0;
volatile int score_ERB = 0;

const int data[] = {score_ELF, score_ELB, score_ERF, score_ERB};

void read_ELF() {score_ELF++;}

void read_ELB() {score_ELB++;}

void read_ERF() {score_ERF++;}

void read_ERB() {score_ERB++;}

void setup() {
    Serial.begin(115200);

    pinMode(Encod_Left_Forward, INPUT);
    pinMode(Encod_Left_Back, INPUT);
    pinMode(Encod_Right_Forward, INPUT);
    pinMode(Encod_Right_Back, INPUT);

    attachInterrupt(digitalPinToInterrupt(Encod_Left_Forward), read_ELF, CHANGE);
    attachInterrupt(digitalPinToInterrupt(Encod_Left_Back), read_ELB, CHANGE);
    attachInterrupt(digitalPinToInterrupt(Encod_Right_Forward), read_ERF, CHANGE);
    attachInterrupt(digitalPinToInterrupt(Encod_Right_Back), read_ERB, CHANGE);
}

void loop() {
  const int arraySize = sizeof(data) / sizeof(data[0]);
  Serial.flush();

  Serial.write((uint8_t *)&arraySize, sizeof(arraySize));

  for (int i = 0; i < arraySizel; ++i)
  {
    uint16_t element = data[i];
    Serial.write((uint8_t *)&element, sizeof(element));
  }

  Serial.print("Encod_Left_Forward: ");
  Serial.print(score_ELF);
  Serial.print(" | Encod_Left_Back: ");
  Serial.print(score_ELB);
  Serial.print(" | Encod_Right_Forward: ");
  Serial.print(score_ERF);
  Serial.print(" | Encod_Right_Back: "); 
  Serial.println(score_ERB);
}
