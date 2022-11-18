package me.yuval.brainstorm;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
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

        Socket client = MainActivity.getSocket();

        sendButton = (Button) findViewById(R.id.send_button);
        sendButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                try {
                    PrintWriter out = new PrintWriter(client.getOutputStream(), true);
                    NAME = findViewById(R.id.name);
                    MESSAGE = findViewById(R.id.msg);

                    String name = NAME.getText().toString();
                    String message = MESSAGE.getText().toString();

                    out.println(message);
                    Toast.makeText(getApplicationContext(), "Sent " + message, Toast.LENGTH_SHORT).show();
                } catch(Exception e) {
                    Toast.makeText(getApplicationContext(), "Something went wrong.", Toast.LENGTH_SHORT).show();
                }
            }
        });
    }
}