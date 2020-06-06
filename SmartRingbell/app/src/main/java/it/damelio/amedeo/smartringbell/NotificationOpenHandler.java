package it.damelio.amedeo.smartringbell;

import android.util.Log;

import com.onesignal.OSNotificationAction;
import com.onesignal.OSNotificationOpenResult;
import com.onesignal.OneSignal;

import org.json.JSONObject;

public class NotificationOpenHandler implements OneSignal.NotificationOpenedHandler {
    String risposta;
    @Override
    public void notificationOpened(OSNotificationOpenResult result) {
        OSNotificationAction.ActionType actionType = result.action.type;
        JSONObject data = result.notification.payload.additionalData;
        String customKey;

        if (data != null) {
            customKey = data.optString("customkey", null);
            if (customKey != null) {
                Log.i("OneSignal", "customkey set with value: " + customKey);
            } else {
                Log.i("OneSignal", "la customkey è nulla");
            }
        }
        if (actionType == OSNotificationAction.ActionType.ActionTaken){
            Log.i("OneSignal", "Button pressed with id; " + result.action.actionID);
            risposta = result.action.actionID;
        }
    }

    public String getRisposta(){
        return risposta;
    }
}