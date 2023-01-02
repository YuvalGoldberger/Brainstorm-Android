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

        // ----- Gets the ip, port and name from MainActivity -----
        Intent getExtrasFromMainIntent = getIntent();
        String[] arr = getExtrasFromMainIntent.getStringArrayExtra("ip_port_name");

        String ip = arr[0];
        String _port = arr[1];
        String name = arr[2];
        // ----- Cast _port to int -----
        int port = Integer.parseInt(_port);

        // ----- Start a thread since MainUIThread cannot use sockets -----
        Thread connectionThread = new Thread(new Runnable() {
            @Override
            public void run() {
                /*
                ----- Connect to server and get Subject -----
                */
                try {
                    // ----- Connect to server -----
                    Socket client = new Socket(ip, port);

                    // ----- Set the static client as the new one and create a Sender and Receiver -----
                    MainActivity.setClient(client);
                    PrintWriter out = new PrintWriter(client.getOutputStream(), true);
                    BufferedReader in = new BufferedReader(new InputStreamReader(client.getInputStream()));

                    // ----- Receive Subject and send it back to server -----
                    String subject = in.readLine();
                    out.println("Got the subject. " + subject);

                    // ----- Go to next page -----
                    Intent forwardIntent = new Intent(getApplicationContext(), SendActivity.class);
                    forwardIntent.putExtra("ip_port_subj_name", new String[] { ip, _port, subject, name });
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