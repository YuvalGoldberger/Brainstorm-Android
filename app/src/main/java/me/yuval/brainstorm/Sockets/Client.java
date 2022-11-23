package me.yuval.brainstorm.Sockets;


import android.os.AsyncTask;

import java.io.IOException;
import java.net.Socket;

import me.yuval.brainstorm.MainActivity;
public class Client {
    public Client(String ip, int port) {
        //clientConnection clientCon = new clientConnection(ip, port);
        //clientCon.doInBackground();
    }
}
class clientConnection extends AsyncTask<Void, Void, Void> {

    private Socket client = MainActivity.getClient();
    private String ip;
    private int port;
/*
    public clientConnection(String ip, int port) {
        this.ip = ip;
        this.port = port;

    } */
    @Override
    protected Void doInBackground(Void... params) {
        try {
            client = new Socket("192.168.1.153", 12345);
        } catch (IOException e) {
            return null;
        }
        return null;
    }
}
