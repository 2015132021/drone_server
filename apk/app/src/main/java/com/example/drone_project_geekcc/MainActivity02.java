package com.example.drone_project_geekcc;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;

public class MainActivity02 extends AppCompatActivity {

    Button rent, myinfo, rentlog;
    View.OnClickListener cl;

    Intent i;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.main);

        rent = (Button) findViewById(R.id.main_rent);
        myinfo = (Button) findViewById(R.id.main_myinfo);
        rentlog = (Button) findViewById(R.id.main_rentlog);

        cl = new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                switch (v.getId()){
                    case R.id.main_rent:
                        i = new Intent(getApplicationContext(), RentActivity.class);
                        startActivity(i);
                        break;

                    case R.id.main_myinfo:
                        i = new Intent(getApplicationContext(), MyinfoActivity.class);
                        startActivity(i);
                        break;

                    case R.id.main_rentlog:
                        i = new Intent(getApplicationContext(), LoglistActivity.class);
                        startActivity(i);
                        break;
                }
            }
        };

        rent.setOnClickListener(cl);
        myinfo.setOnClickListener(cl);
        rentlog.setOnClickListener(cl);

    }
}