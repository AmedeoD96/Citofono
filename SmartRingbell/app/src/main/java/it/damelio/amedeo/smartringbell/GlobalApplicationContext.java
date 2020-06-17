package it.damelio.amedeo.smartringbell;

import android.app.Application;
import android.content.Context;

import androidx.core.content.ContextCompat;


public class GlobalApplicationContext extends Application {
    private static Context appContext;

    @Override
    public void onCreate(){
        super.onCreate();
        appContext = getApplicationContext();
    }

    public static Context getAppContext(){
        return appContext;
    }
}
