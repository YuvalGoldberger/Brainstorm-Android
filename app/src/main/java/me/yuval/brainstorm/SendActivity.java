package me.yuval.brainstorm;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.os.Looper;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import java.net.*;
import java.io.*;



public class SendActivity extends AppCompatActivity {

    private Button sendButton;
    private EditText NAME, MESSAGE;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_send);
        Intent getExtrasFromMainIntent = getIntent();
        String[] arr = getExtrasFromMainIntent.getStringArrayExtra("ip_port");
        String ip = arr[0];
        String port = arr[1];
        Toast.makeText(getApplicationContext(), "Connected to " + ip + ":" + port, Toast.LENGTH_SHORT).show();

        Socket client = MainActivity.getClient();
        if(client == null) Toast.makeText(getApplicationContext(), "client is null", Toast.LENGTH_SHORT).show();
        Thread sendThread = new Thread(new Runnable() {
            @Override
            public void run() {
                Looper.prepare();

                try {
                    PrintWriter out = new PrintWriter(client.getOutputStream(), true);
                    NAME = findViewById(R.id.name);
                    MESSAGE = findViewById(R.id.msg);

                    String name = NAME.getText().toString();
                    String message = MESSAGE.getText().toString();

                    // :breakHere: will be the "code" to split the data in Python (e.g. data.split(":breakHere:"))
                    out.println(name + ":breakHere:" + message);
                    Toast.makeText(getApplicationContext(), "Sent " + message + " from " + name, Toast.LENGTH_SHORT).show();

                    finish();
                    startActivity(getIntent());
                    overridePendingTransition(0, 0);

                } catch (Exception e) {
                    Toast.makeText(getApplicationContext(), e.toString(), Toast.LENGTH_SHORT).show();
                }
                Looper.loop();

            }
            });


        sendButton = (Button) findViewById(R.id.send_button);
        sendButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                sendThread.start();

            }
        });

    }
}