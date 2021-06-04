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

    // 현재 보고있는 페이지 ( 액티비티 ) 에 대한 정보
    String[] page_name = new String[]{"loading", "login", "join", "main", "rent", "myinfo", "loglist", "logview", "map", "camera"};
    int page_stat = 0;

    // 기본적인 고정 항목
    String host = "http://project-geek.cc";

    // 각 객체간 넘겨주는 전역 변수급에 대한 정보
    String uri = "";                // 접근 uri
    String req = "";                // 리퀘스트 json형식 string
    String gp = "GET";              // GET / POST 등의 REST 구분
    JSONObject json;

    // 액티비티 뷰
    TextView tv;
    EditText ed_login_id;
    EditText ed_login_pw;
    Button btn_login;

    // 클릭 리스너
    View.OnClickListener cl;

    // 파일 스트림
    FileInputStream fis;
    FileOutputStream fos;
    byte[] btext;
    String s;
    File[] fileArray;



    MyHandler mh;
    class MyHandler extends Handler {
        @Override
        public void handleMessage(@NonNull Message msg) {
            super.handleMessage(msg);
            switch (msg.what){
                case 0:
                    break;
                case 1:
                    break;
                case 2:
                    break;
                case 3:
                    break;
                case 4:
                    break;
                case 5:
                    break;
                case 6:
                    break;
                case 7:
                    break;
                case 8:
                    break;
                case 9:
                    break;
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
                json = new JSONObject(result);
                mh.sendEmptyMessage(1);
            }
            catch (Exception e) {
                // Error calling the rest api
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
                            JSONObject js = new JSONObject();
                            try {
                                String id = ed_login_id.getText().toString();
                                String pw = ed_login_pw.getText().toString();
                                js.put("id", id);
                                js.put("pw", pw);
                                req = host + uri + js.toString();
                                gp = "GET";
                                MyThread mt = new MyThread();
                                mt.start();
                            }
                            catch (JSONException e){
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