package me.yuval.brainstorm;

import static java.lang.System.out;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.widget.TextView;
import android.widget.Toast;

import java.io.*;
import java.net.*;

public class ConnectionActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_connection);
        Intent getExtrasFromMainIntent = getIntent();
        String[] arr = getExtrasFromMainIntent.getStringArrayExtra("ip_port");

        String ip = arr[0];
        String _port = arr[1];
        int port = Integer.parseInt(_port);

        Thread connectionThread = new Thread(new Runnable() {
            @Override
            public void run() {
                try {
                    Socket client = new Socket(ip, port);

                    MainActivity.setClient(client);
                    PrintWriter out = new PrintWriter(client.getOutputStream(), true);
                    BufferedReader in = new BufferedReader(new InputStreamReader(client.getInputStream()));

                    String subject = in.readLine();
                    out.println("Got the subject. " + subject);

                    Intent forwardIntent = new Intent(getApplicationContext(), SendActivity.class);
                    forwardIntent.putExtra("ip_port_subj", new String[] {ip, _port, subject});
                    startActivity(forwardIntent);

                } catch (IOException e) {
                    //Toast.makeText(getApplicationContext(), "Couldn't connect. Try again.", Toast.LENGTH_SHORT).show();
                    Intent returnIntent = new Intent(getApplicationContext(), MainActivity.class);
                    startActivity(returnIntent);
                }

            }
        });

        connectionThread.start();

    }
}