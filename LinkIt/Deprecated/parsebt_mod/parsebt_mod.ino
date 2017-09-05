String blue = "DISISOK+"
              "DISC:12345678:74278BDAB64445208F0C720EAF059935:1234FA01C5:D43639DC486A:-070OK+"
              "DISC:12345678:14278BDAB64445208F0C720EAF059935:1234FA01C5:D43639DC486A:-070OK+"
              "DISC:12345678:24278BDAB64445208F0C720EAF059935:1234FA01C5:D43639DC486A:-070OK+"
              "DISC:12345678:34278BDAB64445208F0C720EAF059935:1234FA01C5:D43639DC486A:-070OK+";
int data_flags[4] = {0, 0, 0, 0};
String read_in;
String data;
String rssi[4];
String to_send;

void setup() {
  Serial.begin(9600); // open serial connection to USB Serial port
  Serial1.begin(57600); // open internal serial connection to MT7688
}
void loop() {
  for (int i = 0; i < blue.length(); i++) {//
    read_in = blue.substring(i, i + 1);//
    //read_in = Serial.read();
    if (read_in == "+") {
      if (data.substring(0, 5) == "DISIS")
        data = "";
      else if (data.substring(14, 46) == "74278BDAB64445208F0C720EAF059935") { //from 0 to but not including 2
        rssi[0] = (data.substring(71, 75));
        data_flags[0] = 1;
        data = "";
      }
      else if (data.substring(14, 46) == "14278BDAB64445208F0C720EAF059935") { //from 0 to but not including 2
        rssi[1] = (data.substring(71, 75));
        data_flags[1] = 1;
        data = "";
      }
      else if (data.substring(14, 46) == "24278BDAB64445208F0C720EAF059935") { //from 0 to but not including 2
        rssi[2] = (data.substring(71, 75));
        data_flags[2] = 1;
        data = "";
      }
      else if (data.substring(14, 46) == "34278BDAB64445208F0C720EAF059935") { //from 0 to but not including 2
        rssi[3] = (data.substring(71, 75));
        data_flags[3] = 1;
        data = "";
      }
      else {
        data = "";
        data_flags[0] = 0;
        data_flags[1] = 0;
      }
      if ((data_flags[0] == 1) && (data_flags[1] == 1) && (data_flags[2] == 1) && (data_flags[3] == 1))
      {
        data_flags[0] = 0;
        data_flags[1] = 0;
        to_send = rssi[0] + "," + rssi[1] + "," + rssi[2] + "," + rssi[3] + "," + "\n";
        Serial1.print(to_send);
      }
    }
    else {
      data += read_in;
    }
  }
}//


