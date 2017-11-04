package com.leedian.demo;

import android.support.v4.app.NavUtils;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuInflater;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import android.widget.CompoundButton;
import android.widget.EditText;
import android.widget.Switch;

public class MySettingActivity extends MainActivity implements View.OnClickListener {
    private static final String TAG = "MySettingActivity";
    private Switch Switch_1;
    private Switch Switch_2;
    private Switch Switch_3;
    private Button mButton1;
    private EditText mEdit1;
    private EditText mEdit2;
    private EditText mEdit3;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_my_setting);

        Switch_1 = (Switch) findViewById(R.id.switch1);
        Switch_2 = (Switch) findViewById(R.id.switch2);
        Switch_3 = (Switch) findViewById(R.id.switch3);
        mButton1 = (Button) findViewById(R.id.button1);
        mButton1.setOnClickListener(this);
        mEdit1 = (EditText) findViewById(R.id.editText1);
        mEdit2   = (EditText)findViewById(R.id.editText2);
        mEdit3 = (EditText) findViewById(R.id.editText3);

        Switch_1.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(CompoundButton compoundButton, boolean b) {
                PreferenceUtil.getInstance(MySettingActivity.this).putBooleanByApply("chip1",b);
            }
        });
        Switch_2.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(CompoundButton compoundButton, boolean b) {
                PreferenceUtil.getInstance(MySettingActivity.this).putBooleanByApply("chip2",b);
            }
        });
        Switch_3.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(CompoundButton compoundButton, boolean b) {
                PreferenceUtil.getInstance(MySettingActivity.this).putBooleanByApply("chip3",b);
            }
        });

        boolean chip1 = PreferenceUtil.getInstance(this).getBoolean("chip1",false);
        boolean chip2 = PreferenceUtil.getInstance(this).getBoolean("chip2",false);
        boolean chip3 = PreferenceUtil.getInstance(this).getBoolean("chip3",false);

        Switch_1.setChecked(chip1);
        Switch_2.setChecked(chip2);
        Switch_3.setChecked(chip3);

        String chip_1 = PreferenceUtil.getInstance(this).getString("chip1_name", "chip1_name");
        String chip_2 = PreferenceUtil.getInstance(this).getString("chip2_name", "chip2_name");
        String chip_3 = PreferenceUtil.getInstance(this).getString("chip3_name", "chip3_name");

        mEdit1.setText(chip_1);
        mEdit2.setText(chip_2);
        mEdit3.setText(chip_3);
    }

    @Override
    public void onClick(View view) {
        switch (view.getId()) {
            case R.id.button1:
                PreferenceUtil.getInstance(MySettingActivity.this).putStringByApply("chip1_name",mEdit1.getText().toString());
                PreferenceUtil.getInstance(MySettingActivity.this).putStringByApply("chip2_name",mEdit2.getText().toString());
                PreferenceUtil.getInstance(MySettingActivity.this).putStringByApply("chip3_name",mEdit3.getText().toString());
                break;
        }
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        MenuInflater inflater = getMenuInflater();
        inflater.inflate(R.menu.main, menu);
        return super.onCreateOptionsMenu(menu);
    }
    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        switch (item.getItemId()) {
            case R.id.home:
                NavUtils.navigateUpFromSameTask(this);
                return true;
            default:
                return super.onOptionsItemSelected(item);
        }
    }
}