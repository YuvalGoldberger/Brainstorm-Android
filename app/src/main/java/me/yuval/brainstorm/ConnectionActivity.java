package me.yuval.brainstorm;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.widget.Toast;

import java.net.Socket;

public class ConnectionActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_connection);
        Intent getExtrasFromMainIntent = getIntent();
        String[] arr = getExtrasFromMainIntent.getStringArrayExtra("ip_port");
        String ip = arr[0].toString();
        String _port = arr[1];
        int port = Integer.parseInt(_port);

        Socket client = MainActivity.getSocket();

        try {
            client = new Socket(ip, port);
            Intent forwardIntent = new Intent(this, SendActivity.class);
            startActivity(forwardIntent);

        } catch(Exception e) {
            Toast.makeText(getApplicationContext(), e.toString(), Toast.LENGTH_LONG).show();
            //Toast.makeText(getApplicationContext(), "Couldn't connect. Try again.", Toast.LENGTH_SHORT).show();
            Intent returnIntent = new Intent(this, MainActivity.class);
            startActivity(returnIntent);
        }
    }
}