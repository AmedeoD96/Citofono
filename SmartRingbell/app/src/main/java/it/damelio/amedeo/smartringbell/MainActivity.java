package it.damelio.amedeo.smartringbell;

import androidx.appcompat.app.AppCompatActivity;
import com.onesignal.OneSignal;
import android.os.Bundle;
import android.view.View;
import android.view.WindowManager;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;

public class MainActivity extends AppCompatActivity {

    private Button open, close;
    private NotificationOpenHandler notificationOpenHandler;
    private ImageView imageView;
    private TextView textView;

    final String imgURL = "http://192.168.1.13:5000/get-image/Dataset/sconosciuto.jpg";


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
                new SendMessage().execute("Apri la porta");
                imageView.setVisibility(View.INVISIBLE);
                textView.setText("Porta aperta");
                textView.setVisibility(View.VISIBLE);
            }
        });

        close.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
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
}
