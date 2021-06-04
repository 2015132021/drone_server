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
import android.widget.Toast;

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

import static java.lang.Thread.sleep;

public class MainActivity extends AppCompatActivity {

    // 현재 보고있는 페이지 ( 액티비티 ) 에 대한 정보
    String[] page_name = new String[]{"loading", "login", "join", "main", "rent", "myinfo", "loglist", "logview", "map", "camera"};
    int[] page_src = new int[]{R.layout.loading, R.layout.login, R.layout.join, R.layout.main, R.layout.rent, R.layout.myinfo, R.layout.loglist, R.layout.logview, R.layout.map, R.layout.camera};
    int page_stat = 0;

    // 기본적인 고정 항목
    String host = "http://project-geek.cc";

    // 각 객체간 넘겨주는 전역 변수급에 대한 정보
    String uri = "";                // 접근 uri
    String req = "";                // 리퀘스트 json형식 string
    String gp = "GET";              // GET / POST 등의 REST 구분
    JSONObject json;
    int dest = 0;

    // 액티비티 항목
    // login.xml
    EditText login_id;
    EditText login_pw;
    Button login_login;
    Button login_join;

    // 로그인 정보
    String id;
    String hash;

    // 클릭 리스너
    View.OnClickListener cl;

    // 파일 스트림
    FileInputStream fis;
    FileOutputStream fos;
    byte[] btext;
    String s;
    File[] fileArray;
    String fname = "autologoin.json";


    MyHandler mh;
    class MyHandler extends Handler {
        @Override
        public void handleMessage(@NonNull Message msg) {
            super.handleMessage(msg);
            setContentView(page_src[msg.what]);
            if(msg.what == 1) {
                try{
                    if(json.getBoolean("error") == false){
                        switch (dest){
                            case 0:
                                break;
                            case 1:
                                break;
                            case 2:
                                break;
                            case 3:
                                fos = openFileOutput(fname, Context.MODE_PRIVATE);
                                JSONObject fjs = new JSONObject();
                                fjs.put("id", id);
                                fjs.put("hash", hash);
                                fos.write(fjs.toString().getBytes());
                                fos.close();
                                System.out.println("save hash");
                                page_main();
                                break;
                        }
                    }

                }catch (JSONException e){
                    System.out.println("JSON error");
                }catch (Exception e){
                    System.out.println(e.getMessage());
                }
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
                System.out.println("/get ready");

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

                result = builder.toString();
                json = new JSONObject(result);
                System.out.println(result);
                mh.sendEmptyMessage(1);
            }
            catch (Exception e) {
                mh.sendEmptyMessage(0);
            }

        }
    }

    // 여기서부터는 각 페이지 별 실행 함수입니다.
    protected void page_loading(){
        page_stat = 0;
        // Storage에서 Hash 읽어옴 >> Hash, id를 Server-autologin에 보냄 --> return 에러가 없으면 >> main
        // return 에러가 있거나 Exception 발생 시 login

        try{
            fis = openFileInput(fname);
            btext = new byte[fis.available()];
            fis.read(btext);
            s = new String(btext);
            JSONObject fjs = new JSONObject(s);
            id = fjs.getString("id");
            hash = fjs.getString("hash");
            req = host + uri + fjs.toString();
            gp = "GET";
            dest = 3;
            MyThread mt = new MyThread();
            mt.start();

        }catch (Exception e) {
            s = e.getMessage();
            mh.sendEmptyMessage(1);
        }

        // 해시 파일이 없는 경우

        page_login();

    }

    protected void page_login(){
        setContentView(page_src[1]);

        // login.xml 로딩
        login_id = (EditText) findViewById(R.id.login_id);
        login_pw = (EditText) findViewById(R.id.login_pw);
        login_login = (Button) findViewById(R.id.login_login);
        login_join = (Button) findViewById(R.id.login_tojoin);

        cl = new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                System.out.println("click");
                try{
                    switch (v.getId()) {
                        case R.id.login_login:
                            System.out.println("login_login");

                            uri = "/client/login/";
                            JSONObject js = new JSONObject();
                            try {
                                String id = login_id.getText().toString();
                                String pw = login_pw.getText().toString();
                                js.put("id", id);
                                js.put("pw", pw);
                                req = host + uri + js.toString();
                                gp = "GET";
                                dest = 3;
                                MyThread mt = new MyThread();
                                mt.start();
                            }
                            catch (JSONException e){
                                System.out.println("error");
                            }
                            break;
                    }
                }catch (Exception e){

                }
            }
        };

        login_login.setOnClickListener(cl);
        login_join.setOnClickListener(cl);
    }

    protected void page_main(){
        setContentView(page_src[3]);

    }



    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.loading);
        mh = new MyHandler();
        System.out.println("create");

        page_loading();
    }
}