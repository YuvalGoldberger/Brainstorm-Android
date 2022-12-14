package me.yuval.brainstorm;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.os.CountDownTimer;
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
    private TextView timer;
    private boolean sent = false;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_send);
        // ----- Get IP, Port, Subject and Name ----
        Intent getExtrasFromMainIntent = getIntent();
        String[] arr = getExtrasFromMainIntent.getStringArrayExtra("subj_name");


        // ----- Gets the name and subject from last intent and sets it in the TextView -----
        subj = arr[0];
        Toast.makeText(getApplicationContext(), subj, Toast.LENGTH_SHORT).show();

        String name = arr[1];
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

        // ----- Set countdown of 30000ms (30s) -----
        timer = findViewById(R.id.timer);
        new CountDownTimer(30000, 1000) {
            @Override
            public void onTick(long millisUntilFinished) {
                timer.setText("הזמן שנותר לענות: " + millisUntilFinished / 1000);
            }

            @Override
            public void onFinish() {
                if(!sent) {
                    Toast.makeText(getApplicationContext(), "לא שלחת אסוציאציה בזמן!", Toast.LENGTH_SHORT).show();
                    startActivity(backwardIntent);
                }
            }
        }.start();

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

                    sent = true;
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