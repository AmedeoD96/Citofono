package it.damelio.amedeo.smartringbell;

import android.os.AsyncTask;
import android.util.Log;
import android.widget.Toast;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.net.Socket;

public class SendMessage extends AsyncTask<String, Void, Void> {
    private Exception exception;

    @Override
    protected Void doInBackground(String... strings) {
        try {
            try {
                Socket socket = new Socket("192.168.1.20", 8888);
                PrintWriter outToServer = new PrintWriter(
                        new OutputStreamWriter(
                                socket.getOutputStream()));
                outToServer.print(strings[0]);
                outToServer.flush();
                BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
                String response = in.readLine();
                Log.i("response", response);
            } catch (IOException e) {
                e.printStackTrace();
            }
        } catch (Exception e){
            this.exception = e;
            return null;
        }
        return null;
    }
}
