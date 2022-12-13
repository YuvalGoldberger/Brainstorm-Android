package me.yuval.brainstorm;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.os.Looper;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import java.net.*;
import java.io.*;



public class SendActivity extends AppCompatActivity {

    private Button sendButton;
    private EditText NAME, MESSAGE;
    private Socket client;
    private BufferedReader in;
    private String subj = "";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_send);
        // ----- Get IP, Port, Subject and Name ----
        Intent getExtrasFromMainIntent = getIntent();
        String[] arr = getExtrasFromMainIntent.getStringArrayExtra("ip_port_subj_name");
        String ip = arr[0];
        String port = arr[1];
        // ----- Shows what server you are connected to -----
        Toast.makeText(getApplicationContext(), "Connected to " + ip + ":" + port, Toast.LENGTH_SHORT).show();
        subj = arr[2];
        Toast.makeText(getApplicationContext(), subj, Toast.LENGTH_SHORT).show();

        // ----- Gets the name and subject from last intent and sets it in the TextView -----
        String name = arr[3];
        TextView nameTextView = findViewById(R.id.name);
        nameTextView.setText("מחובר כ: " + name);

        TextView subjTextView = findViewById(R.id.subject);
        subjTextView.setText(subj);

        // ----- Back to MainActivity if error happens -----
        Intent backwardIntent = new Intent(getApplicationContext(), MainActivity.class);

        client = MainActivity.getClient();
        if(client == null) {
            /*
            ----- If client is null return to MainActivity -----
            */
            Toast.makeText(getApplicationContext(), "client is null", Toast.LENGTH_SHORT).show();
            startActivity(backwardIntent);
        }

        // ----- Start thread again as MainUIThread cannot use sockets -----
        Thread sendThread = new Thread(new Runnable() {
            @Override
            public void run() {
                // ----- Prepare Looper to use MainUIThread in another Thread (Toast) -----
                Looper.prepare();

                try {
                    // ----- Get message from EditText and make sure it's not empty -----
                    MESSAGE = findViewById(R.id.msg);
                    String message = MESSAGE.getText().toString();

                    if(message.isEmpty()) {
                        Toast.makeText(getApplicationContext(), "הכנס אסוציאציה", Toast.LENGTH_SHORT).show();
                    }
                    // ----- Create a Sender -----
                    PrintWriter out1 = new PrintWriter(client.getOutputStream(), true);

                    // :breakHere: will be the "code" to split the data in Python (e.g. data.split(":breakHere:"))
                    out1.println(name + ":breakHere:" + message);
                    Toast.makeText(getApplicationContext(), "Sent " + message + " from " + name, Toast.LENGTH_SHORT).show();

                    finish();
                    startActivity(getIntent());
                    overridePendingTransition(0, 0);

                } catch (Exception e) {
                    Toast.makeText(getApplicationContext(), e.toString(), Toast.LENGTH_SHORT).show();
                    startActivity(backwardIntent);
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