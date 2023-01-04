package me.yuval.brainstorm;

import static java.lang.System.out;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.os.Looper;
import android.widget.TextView;
import android.widget.Toast;

import java.io.*;
import java.net.*;

public class ConnectionActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_connection);

        // ----- Gets the ip and name from MainActivity -----
        Intent getExtrasFromMainIntent = getIntent();
        String[] arr = getExtrasFromMainIntent.getStringArrayExtra("ip_name");

        String ip = arr[0];
        String name = arr[1];

        // ----- Start a thread since MainUIThread cannot use sockets -----
        Thread connectionThread = new Thread(new Runnable() {
            @Override
            public void run() {
                Looper.prepare();
                /*
                ----- Connect to server and get Subject -----
                */
                try {
                    // ----- Connect to server -----
                    Socket client = new Socket(ip, 25565);
                    Toast.makeText(getApplicationContext(), "Connected to " + ip + " : 25565", Toast.LENGTH_SHORT).show();

                    // ----- Set the static client as the new one and create a Sender and Receiver -----
                    MainActivity.setClient(client);
                    PrintWriter out = new PrintWriter(client.getOutputStream(), true);
                    BufferedReader in = new BufferedReader(new InputStreamReader(client.getInputStream()));

                    // ----- Receive Subject and send it back to server -----
                    String subject = in.readLine();
                    //out.println("Got the subject. " + subject);

                    // ----- Go to next page -----
                    Intent forwardIntent = new Intent(getApplicationContext(), SendActivity.class);
                    forwardIntent.putExtra("subj_name", new String[] { subject, name });
                    startActivity(forwardIntent);

                } catch (IOException e) {
                    /*
                    ----- Catch IOException if cannot connect and return to MainActivity -----
                    */
                    Intent returnIntent = new Intent(getApplicationContext(), MainActivity.class);
                    startActivity(returnIntent);
                }

            }
        });

        connectionThread.start();

    }
}