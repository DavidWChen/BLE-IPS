package com.leedian.demo;

import android.Manifest;
import android.app.AlertDialog;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.View;

import android.content.Intent;
import android.content.Context;
import android.content.DialogInterface;
import android.content.pm.PackageManager;

import android.os.AsyncTask;
import android.os.Handler;
import android.os.Bundle;
import android.os.SystemClock;

import android.widget.Button;
import android.widget.Chronometer;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothManager;
import android.bluetooth.le.BluetoothLeScanner;
import android.bluetooth.le.ScanCallback;
import android.bluetooth.le.ScanFilter;
import android.bluetooth.le.ScanResult;
import android.bluetooth.le.ScanSettings;




import com.google.gson.Gson;
import com.squareup.picasso.MemoryPolicy;
import com.squareup.picasso.Picasso;

import java.io.IOException;
import java.text.DateFormat;
import java.text.DecimalFormat;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.TimeZone;
import java.util.ArrayList;
import java.util.List;

import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.FormBody;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;
import okhttp3.RequestBody;
import okhttp3.MediaType;

public class MainActivity extends AppCompatActivity implements View.OnClickListener {
    private static final String TAG = "MainActivity";
    private TextView tvShowData;
    private TextView tvShowDataTime;
    public Button btnGetData;
    public Button btnPostData;
    private Chronometer timer;
    private Button btnSettings;
    private ImageView Img;
    //Bluetooth Setup
    BluetoothManager btManager;
    BluetoothAdapter btAdapter;
    BluetoothLeScanner btScanner;
    private final static int REQUEST_ENABLE_BT = 1;
    private static final int PERMISSION_REQUEST_COARSE_LOCATION = 1;
    /**
     * 把控件的初始化放在这个方法里面
     * @param savedInstanceState
     */
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        //Setup
        Img = (ImageView) findViewById(R.id.imageView);
        timer = (Chronometer) findViewById(R.id.timer);
        btnGetData = (Button) findViewById(R.id.btn_get_data);
        tvShowData = (TextView) findViewById(R.id.tv_show_data);
        tvShowDataTime = (TextView) findViewById(R.id.tv_show_data_time);
        btnGetData.setOnClickListener(this);
        btnSettings = (Button) findViewById(R.id.settings);
        btnSettings.setOnClickListener(this);
        btnPostData = (Button)findViewById(R.id.mylocation);
        btnPostData.setOnClickListener(this);
        //Bluetooth And Permissions
        btManager = (BluetoothManager)getSystemService(Context.BLUETOOTH_SERVICE);
        btAdapter = btManager.getAdapter();
        btScanner = btAdapter.getBluetoothLeScanner();
        if (btAdapter != null && !btAdapter.isEnabled()) {
            Intent enableIntent = new Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE);
            startActivityForResult(enableIntent,REQUEST_ENABLE_BT);
        }

        // Make sure we have access coarse location enabled, if not, prompt the user to enable it
        if (this.checkSelfPermission(Manifest.permission.ACCESS_COARSE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
            final AlertDialog.Builder builder = new AlertDialog.Builder(this);
            builder.setTitle("This app needs location access");
            builder.setMessage("Please grant location access so this app can detect peripherals.");
            builder.setPositiveButton(android.R.string.ok, null);
            builder.setOnDismissListener(new DialogInterface.OnDismissListener() {
                @Override
                public void onDismiss(DialogInterface dialog) {
                    requestPermissions(new String[]{Manifest.permission.ACCESS_COARSE_LOCATION}, PERMISSION_REQUEST_COARSE_LOCATION);
                }
            });
            builder.show();
        }
   }
    //Permissions Handler-necessary for BLE support
    @Override
    public void onRequestPermissionsResult(int requestCode, String permissions[], int[] grantResults) {
        switch (requestCode) {
            case PERMISSION_REQUEST_COARSE_LOCATION: {
                if (grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                    System.out.println("coarse location permission granted");
                } else {
                    final AlertDialog.Builder builder = new AlertDialog.Builder(this);
                    builder.setTitle("Functionality limited");
                    builder.setMessage("Since location access has not been granted, this app will not be able to discover beacons when in the background.");
                    builder.setPositiveButton(android.R.string.ok, null);
                    builder.setOnDismissListener(new DialogInterface.OnDismissListener() {
                        @Override
                        public void onDismiss(DialogInterface dialog) {
                        }
                    });
                    builder.show();
                }
                return;
            }
        }
    }

    String chip1Name;
    String chip2Name;
    String chip3Name;
    String r1, r2, r3, r4;
    Boolean rf1, rf2, rf3, rf4;

    //Gather Recorded Chip Names
    @Override
    protected void onResume() {
        super.onResume();
         chip1Name= PreferenceUtil.getInstance(MainActivity.this).getString("chip1_name","chip1_name");
         chip2Name= PreferenceUtil.getInstance(MainActivity.this).getString("chip2_name","chip2_name");
         chip3Name= PreferenceUtil.getInstance(MainActivity.this).getString("chip3_name","chip3_name");
    }

    /**
     * 控件的点击事件
     * @param view
     */
    @Override
    public void onClick(View view) {
        int hour;
        switch (view.getId()) {
            case R.id.btn_get_data:
                getdata();
                timer.setBase(SystemClock.elapsedRealtime());//计时器清零
                hour = (int) ((SystemClock.elapsedRealtime() - timer.getBase()) / 1000 / 60);
                timer.setFormat("0" + String.valueOf(hour) + ":%s");
                timer.start();
                break;
            case R.id.mylocation:
                startScanning();
                timer.setBase(SystemClock.elapsedRealtime());//计时器清零
                hour = (int) ((SystemClock.elapsedRealtime() - timer.getBase()) / 1000 / 60);
                timer.setFormat("0" + String.valueOf(hour) + ":%s");
                timer.start();
                break;
            case R.id.settings:
                startActivity(new Intent(MainActivity.this, MySettingActivity.class));
                break;
            default:
        }
    }

    //Record Scan Values until a set of all 4 are found
    private ScanCallback leScanCallback = new ScanCallback() {
        @Override
        public void onScanResult(int callbackType, ScanResult result) {
            if (result.getDevice().getAddress().equals("FF:FF:FF:FF:FF:FF")){
                r1 = Integer.toString(result.getRssi());
                rf1 = Boolean.TRUE;
            }
            else if (result.getDevice().getAddress().equals("19:18:FC:04:20:18")){
                r2 = Integer.toString(result.getRssi());
                rf2 = Boolean.TRUE;
            }
            else if (result.getDevice().getAddress().equals("19:18:FC:04:20:EE")){
                r3 = Integer.toString(result.getRssi());
                rf3 = Boolean.TRUE;
            }
            else if (result.getDevice().getAddress().equals("19:18:FC:04:21:01")){
                r4 = Integer.toString(result.getRssi());
                rf4 = Boolean.TRUE;
            }
            else {;}
            if(rf1&&rf2&&rf3&&rf4){
                btScanner.stopScan(leScanCallback);
                postData(r1,r2,r3,r4);
                handler.removeCallbacks(runnable);
            }
        }
    };

    public void startScanning() {
        //Set up var, filter and settings for BLE Scan
        rf1 = rf2 = rf3 = rf4 = Boolean.FALSE;
        final ScanSettings settings = new ScanSettings.Builder().setCallbackType(ScanSettings.CALLBACK_TYPE_ALL_MATCHES).build();
        final List<ScanFilter> filters = new ArrayList<>();
        String[] filterlist = {
                "FF:FF:FF:FF:FF:FF",
                "19:18:FC:04:20:18",
                "19:18:FC:04:20:EE",
                "19:18:FC:04:21:01"};
        for (int i = 0; i < filterlist.length; i++) {
            ScanFilter filter = new ScanFilter.Builder().setDeviceAddress(filterlist[i]).build();
            filters.add(filter);
        }
        //Setup timeout for scan
        handler.postAtTime(runnable, System.currentTimeMillis()+interval);
        handler.postDelayed(runnable, interval);
        //Scan
        AsyncTask.execute(new Runnable() {
            @Override
            public void run() {
                btScanner.startScan(filters, settings,leScanCallback);
            }
        });
    }
    final int interval = 5000;
    Handler handler = new Handler();
    Runnable runnable = new Runnable(){
        public void run(){
            btScanner.stopScan(leScanCallback);
            Toast.makeText(MainActivity.this, "Unable to connect to Beacons!", Toast.LENGTH_LONG).show();
        }
    };

    //POST collected Bluetooth data to server
    public void postData(String rssi1, String rssi2, String rssi3, String rssi4) {
        final MediaType JSON
                = MediaType.parse("application/json");
        OkHttpClient client = new OkHttpClient();
        RequestBody body = new FormBody.Builder()
                .add("rssi1",rssi1)
                .add("rssi2",rssi2)
                .add("rssi3",rssi3)
                .add("rssi4",rssi4)
                .build();
        Request request = new Request.Builder()
                .url("http://192.168.1.77:8080/update")
                .post(body)
                .build();
        Response response = null;
        client.newCall(request).enqueue(new Callback() {
            @Override
            public void onFailure(Call call, IOException e) {
                e.printStackTrace();
            }
            @Override
            public void onResponse(Call call, final Response response) throws IOException {
                if (!response.isSuccessful()) {
                    throw new IOException("Unexpected code " + response);
                }
                else
                    //Get Data from server if POST was successful
                    getdata();
            }
        });
    }

    /**
     * 使用okhttp 进行网络请求
     * 各种请求方式参考(http://blog.csdn.net/hzl9966/article/details/51434716)
     */
    public void getdata() {
        String url = "http://192.168.1.77:8080/data";
        OkHttpClient client = new OkHttpClient();
        Request request = new Request.Builder().url(url).build();
        client.newCall(request).enqueue(new Callback() {
            @Override
            public void onFailure(Call call, IOException e) {
                Log.i(TAG, "onFailure: " + e);
            }
            @Override
            public void onResponse(Call call, Response response) throws IOException {
                MyData myData = new Gson().fromJson(response.body().charStream(), MyData.class);
                double current = myData.getChip1().getRaw_time() ;
                long Newcurrent = (long) ridDecimal(current*1000);
                Date date = new Date(Newcurrent);
                DateFormat format = new SimpleDateFormat("MM/dd/yyyy HH:mm:ss");
                format.setTimeZone(TimeZone.getTimeZone("GMT+8:00"));
                String formatted = format.format(date);
                SwitchCheck(myData,formatted);
            }
        });
    }

    private String  showChipData;

    //check for which chip to display
    public void SwitchCheck( MyData myData ,  String formatted ) {
        showChipData="";
        boolean chip1 = PreferenceUtil.getInstance(MainActivity.this).getBoolean("chip1", false);
        boolean chip2 = PreferenceUtil.getInstance(MainActivity.this).getBoolean("chip2", false);
        boolean chip3 = PreferenceUtil.getInstance(MainActivity.this).getBoolean("chip3", false);
        MyData.Chip1Bean chip11 = myData.getChip1();
        MyData.Chip2Bean chip21 = myData.getChip2();
        MyData.Chip3Bean chip13 = myData.getChip3();
        if (chip1 == true) {
            if (chip11!=null){
                showChipData+=chip1Name+chip11.toString();
            }else {
                showChipData+="No Data";
            }
        }
        if (chip2 == true) {
            if (chip21!=null){
                showChipData+=chip2Name+chip21.toString();
            }else {
                showChipData+="\n"+"\n"+"No Data";
            }
        }
        if (chip3 == true) {
            if (chip13!=null){
                showChipData+=chip1Name+chip13.toString();
            }else {
                showChipData+="\n"+"\n"+"No Data";
            }
        }
        if (chip1==false&&chip2==false&&chip3==false){
            showChipData="Please select a chip to display.";
        }
        setDataUI(showChipData, formatted + "");
    }

    //remove decimals from a number
    private double ridDecimal(double a) {
        DecimalFormat df = new DecimalFormat(".");
        a = Double.valueOf(df.format(a));
        return a;
    }

    //handles text and image display
    public void setDataUI(final String str1,final String str2){
        this.runOnUiThread(new Runnable() {
            @Override
            public void run() {
                tvShowData.setText(str1);
                tvShowDataTime.setText(str2);
                Picasso.with(MainActivity.this).load("http://192.168.1.77:8080/location.png").memoryPolicy(MemoryPolicy.NO_CACHE).into(Img);
                if (str1 == "Please select a chip to display."){
                    Picasso.with(MainActivity.this).load(R.drawable.map).into(Img);
                }
            }
        });
    }
}


