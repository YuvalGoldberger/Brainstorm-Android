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
    private EditText IP, Port;
    private static Socket client;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        connectButton = (Button) findViewById(R.id.connect_button);
        connectButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                IP = findViewById(R.id.ip);
                Port = findViewById(R.id.port);

                String ip = IP.getText().toString();
                String _port = Port.getText().toString();

                if(ip.isEmpty()) {
                    Toast.makeText(getApplicationContext(), "Please add IP address.", Toast.LENGTH_SHORT).show();
                    return;
                } else if(_port.isEmpty()) {
                    Toast.makeText(getApplicationContext(), "Please add Port.", Toast.LENGTH_SHORT).show();
                    return;
                }

                Intent intent = new Intent(getApplicationContext(), ConnectionActivity.class);
                intent.putExtra("ip_port", new String[] { ip, _port });
                startActivity(intent);

                finish();

            }
        });

    }

    public static Socket getSocket() {
        return client;
    }
}