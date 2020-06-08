package it.damelio.amedeo.smartringbell;

import androidx.appcompat.app.AppCompatActivity;

import com.onesignal.OSNotificationOpenResult;
import com.onesignal.OneSignal;

import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;

public class MainActivity extends AppCompatActivity {

    EditText editText;
    Button button;
    NotificationOpenHandler notificationOpenHandler;
    String risposta = "";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        notificationOpenHandler = new NotificationOpenHandler();

        // OneSignal Init
        OneSignal.startInit(this)
                .setNotificationOpenedHandler(notificationOpenHandler)
                .inFocusDisplaying(OneSignal.OSInFocusDisplayOption.Notification)
                .unsubscribeWhenNotificationsAreDisabled(true)
                .init();

        initUI();

        //risposta = notificationOpenHandler.getRisposta();

        button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                risposta = notificationOpenHandler.getRisposta();
                if (risposta != null && !risposta.equals("")) {
                    new SendMessage().execute(risposta);
                    editText.getText().clear();
                }else {
                    new SendMessage().execute("Porca troia non funziona");
                }
            }
        });


    }

    private void initUI() {
        editText = findViewById(R.id.editText);
        button = findViewById(R.id.button);
    }
}
