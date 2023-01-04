package me.yuval.brainstorm;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import java.net.*;
import java.io.*;

public class MainActivity extends AppCompatActivity {

    private Button connectButton;
    private EditText IP, Name;
    private static Socket client;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        /*
        ----- When application starts it creates this page -----
        */
        // ----- Uses AppCompatActivity's onCreate method to create page -----
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // ----- Get the connect button and start a event listener (onClick) -----
        connectButton = (Button) findViewById(R.id.connect_button);
        connectButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                /*
                ----- Send the name, ip and port to the next page -----
                */

                // ----- Get the String values from EditTexts -----
                IP = findViewById(R.id.ip);
                Name = findViewById(R.id.name);

                String ip = IP.getText().toString();
                String name = Name.getText().toString();

                // ----- Check if user didn't enter ip, port or name -----
                if(ip.isEmpty()) {
                    Toast.makeText(getApplicationContext(), "הכנס כתובת אייפי.", Toast.LENGTH_SHORT).show();
                    return;
                } if (name.isEmpty()) {
                    Toast.makeText(getApplicationContext(), "הכנס את שמך.", Toast.LENGTH_SHORT).show();
                    return;
                }

                // Create an intent of the ConnectionActivity page, add the ip, port and name and start the new activity -----
                Intent intent = new Intent(getApplicationContext(), ConnectionActivity.class);
                intent.putExtra("ip_name", new String[] { ip, name });
                startActivity(intent);

                finish();

            }
        });

    }

    public static Socket getClient() {
        /*
        ----- Static method of getting client so it can be used everywhere -----
        */
        return client;
    }
    public static void setClient(Socket newClient) {
        /*
        ----- Static method of setting the client -----
        */
        client = newClient;
    }
}