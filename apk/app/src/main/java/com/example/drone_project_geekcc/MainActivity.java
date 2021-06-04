package com.example.drone_project_geekcc;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

import android.content.Context;
import android.os.Bundle;
import android.os.Handler;
import android.os.Message;
import android.util.JsonReader;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedInputStream;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;

public class MainActivity extends AppCompatActivity {

    TextView tv;
    EditText ed_login_id;
    EditText ed_login_pw;

    View.OnClickListener cl;
    Button btn_login;

    FileInputStream fis;
    FileOutputStream fos;
    byte[] btext;
    String s;
    File[] fileArray;

    String host = "http://project-geek.cc";
    String uri = "";
    JSONObject js;
    String gp = "GET";
    String logs = "";
    String req = "";

    MyHandler mh;
    String handle = "";

    class MyHandler extends Handler {
        @Override
        public void handleMessage(@NonNull Message msg) {
            super.handleMessage(msg);
            if (msg.what == 1){
            }
        }
    }

    class MyThread extends Thread{
        @Override
        public void run() {
            super.run();
            String result = null;
            try {
                // Open the connection

                URL url = new URL(req);
                HttpURLConnection conn = (HttpURLConnection) url.openConnection();
                conn.setRequestMethod("GET");
                InputStream is = conn.getInputStream();

                // Get the stream
                StringBuilder builder = new StringBuilder();
                BufferedReader reader = new BufferedReader(new InputStreamReader(is, "UTF-8"));
                String line;
                while ((line = reader.readLine()) != null) {
                    builder.append(line);
                }

                // Set the result
                result = builder.toString();
                //result = result.replace("'", "\"");
                JSONObject json = new JSONObject(result);

                if(handle == "login"){
                    try{
                        fos = openFileOutput("logon.txt", Context.MODE_PRIVATE);
                        fos.write(json.toString().getBytes());
                        fos.close();
                        setContentView(R.layout.main);
                    }catch (Exception e){
                        logs = e.getMessage();
                        mh.sendEmptyMessage(1);
                    }
                }
                mh.sendEmptyMessage(1);
            }
            catch (Exception e) {
                // Error calling the rest api
                logs = e.getMessage();
                mh.sendEmptyMessage(1);
            }

        }
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.loading);

        String line = null;


        mh = new MyHandler();

        try{
            fis = openFileInput("logon.txt");
            btext = new byte[fis.available()];
            fis.read(btext);
            s = new String(btext);
            JSONObject json = new JSONObject(s);
            logs = json.toString();
            mh.sendEmptyMessage(1);
        }catch (Exception e) {
            s = e.getMessage();
        }
        setContentView(R.layout.login);

        btn_login = (Button) findViewById(R.id.login);
        ed_login_id = (EditText) findViewById(R.id.login_id);
        ed_login_pw = (EditText) findViewById(R.id.login_pw);

        cl = new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                try{
                    switch (v.getId()) {
                        case R.id.login:
                            tv = (TextView)findViewById(R.id.textView);
                            uri = "/client/login/";
                            js = new JSONObject();
                            try {
                                String id = ed_login_id.getText().toString();
                                String pw = ed_login_pw.getText().toString();
                                js.put("id", id);
                                js.put("pw", pw);
                                req = host + uri + js.toString();
                                gp = "GET";
                                handle = "login";
                                MyThread mt = new MyThread();
                                mt.start();
                            }
                            catch (JSONException e){
                                logs = e.getMessage();
                                mh.sendEmptyMessage(1);
                            }
                            break;
                    }
                }catch (Exception e){

                }
            }
        };

        btn_login.setOnClickListener(cl);

    }
}