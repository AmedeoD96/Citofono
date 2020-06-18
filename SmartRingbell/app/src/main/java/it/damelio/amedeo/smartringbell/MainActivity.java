package it.damelio.amedeo.smartringbell;

import androidx.appcompat.app.AppCompatActivity;
import com.onesignal.OneSignal;
import android.os.Bundle;
import android.renderscript.ScriptIntrinsicBLAS;
import android.view.View;
import android.view.WindowManager;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;

public class MainActivity extends AppCompatActivity {

    private Button open, close;
    private NotificationOpenHandler notificationOpenHandler;
    private ImageView imageView;
    private TextView textView;

    final String imgURL = "http://192.168.1.20:5000/get-image/Dataset/sconosciuto.jpg";


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        getWindow().setFlags(WindowManager.LayoutParams.FLAG_SECURE, WindowManager.LayoutParams.FLAG_SECURE);
        setContentView(R.layout.activity_main);
        notificationOpenHandler = new NotificationOpenHandler();

        // OneSignal Init
        OneSignal.startInit(this)
                .setNotificationOpenedHandler(notificationOpenHandler)
                .inFocusDisplaying(OneSignal.OSInFocusDisplayOption.Notification)
                .unsubscribeWhenNotificationsAreDisabled(true)
                .init();

        initUI();

        open.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                flaskConnection("Apri la Porta");
                new SendMessage().execute("Apri la porta");
                imageView.setVisibility(View.INVISIBLE);
                textView.setText("Porta aperta");
                textView.setVisibility(View.VISIBLE);

            }
        });

        close.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                flaskConnection("Non aprire");
                new SendMessage().execute("Non aprire");
                imageView.setVisibility(View.INVISIBLE);
                textView.setText("Porta rimasta chiusa");
                textView.setVisibility(View.VISIBLE);
            }
        });


    }

    private void initUI() {
        open = findViewById(R.id.button);
        imageView = findViewById(R.id.imageView);
        close = findViewById(R.id.download);
        new DownloadImageTask(imageView).execute(imgURL);
        textView = findViewById(R.id.textView);
    }


    private void flaskConnection(final String value){
        new Thread(new Runnable() {
            @Override
            public void run() {
                OutputStream os = null;
                InputStream is = null;
                HttpURLConnection conn = null;
                try {
                    URL url = new URL("http://192.168.1.13:5000/");
                    JSONObject jsonObject = new JSONObject();
                    jsonObject.put("risposta", value);
                    String message = jsonObject.toString();

                    conn = (HttpURLConnection) url.openConnection();
                    conn.setReadTimeout(10000);
                    conn.setConnectTimeout(15000);
                    conn.setRequestMethod("POST");
                    conn.setDoInput(true);
                    conn.setDoOutput(true);
                    conn.setFixedLengthStreamingMode(message.getBytes().length);
                    conn.setRequestProperty("Content-Type", "application/json;charset=utf-8");
                    conn.setRequestProperty("X-Requested-Width", "XMLHttpRequest");
                    conn.connect();
                    os = new BufferedOutputStream(conn.getOutputStream());
                    os.write(message.getBytes());
                    os.flush();
                    is = conn.getInputStream();


                }catch (IOException | JSONException e){
                    e.printStackTrace();
                }finally {
                    conn.disconnect();
                }
            }
        }).start();
    }
}
