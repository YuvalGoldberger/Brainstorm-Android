package me.yuval.brainstorm;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.widget.Toast;

import java.io.IOException;
import java.net.Socket;

import me.yuval.brainstorm.Sockets.Client;

public class ConnectionActivity extends AppCompatActivity {
    //192.168.1.153
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_connection);
        Intent getExtrasFromMainIntent = getIntent();
        String[] arr = getExtrasFromMainIntent.getStringArrayExtra("ip_port");

        Toast.makeText(getApplicationContext(), "HELLO", Toast.LENGTH_SHORT).show();
        String ip = arr[0].toString();
        String _port = arr[1];
        int port = Integer.parseInt(_port);

        class clientConnection extends AsyncTask<Void, Void, Void> {

            private Socket client = MainActivity.getClient();

            @Override
            protected Void doInBackground(Void... params) {
                try {
                    Toast.makeText(getApplicationContext(), "testt", Toast.LENGTH_SHORT).show();
                    client = new Socket("192.168.1.153", 12345);
                    Toast.makeText(getApplicationContext(), "Connected to " + ip + ":" + String.valueOf(port), Toast.LENGTH_SHORT).show();
                    Intent forwardIntent = new Intent(getApplicationContext(), SendActivity.class);
                    startActivity(forwardIntent);

                } catch (IOException e) {
                    Toast.makeText(getApplicationContext(), e.toString(), Toast.LENGTH_LONG).show();
                    //Toast.makeText(getApplicationContext(), "Couldn't connect. Try again.", Toast.LENGTH_SHORT).show();
                    Intent returnIntent = new Intent(getApplicationContext(), MainActivity.class);
                    startActivity(returnIntent);
                }
                return null;
            }
        }

        clientConnection clConn = new clientConnection();
        clConn.execute();
        /*
        try {
            Toast.makeText(getApplicationContext(), "testt", Toast.LENGTH_SHORT).show();
            new Client(ip, port);
            Toast.makeText(getApplicationContext(), "Connected to " + ip + ":" + String.valueOf(port), Toast.LENGTH_SHORT).show();
            Intent forwardIntent = new Intent(getApplicationContext(), SendActivity.class);
            startActivity(forwardIntent);

        } catch(Exception e) {
            Toast.makeText(getApplicationContext(), e.toString(), Toast.LENGTH_LONG).show();
            //Toast.makeText(getApplicationContext(), "Couldn't connect. Try again.", Toast.LENGTH_SHORT).show();
            Intent returnIntent = new Intent(getApplicationContext(), MainActivity.class);
            startActivity(returnIntent);
        }
    } */

    }
}