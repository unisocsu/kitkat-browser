package org.kitkatbrowser;

import android.app.Activity;
import android.os.Bundle;
import android.view.KeyEvent;
import android.view.inputmethod.EditorInfo;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;
import org.mozilla.geckoview.GeckoRuntime;
import org.mozilla.geckoview.GeckoSession;
import org.mozilla.geckoview.GeckoView;

public class MainActivity extends Activity {
    private GeckoRuntime runtime;
    private GeckoSession session;
    private EditText address;

    @Override public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        address = findViewById(R.id.address);
        Button go = findViewById(R.id.go);
        GeckoView view = findViewById(R.id.geckoview);
        try {
            runtime = GeckoRuntime.create(this);
            session = new GeckoSession();
            session.open(runtime);
            view.setSession(session);
            go.setOnClickListener(v -> loadAddress());
            address.setOnEditorActionListener((v, actionId, event) -> {
                if (actionId == EditorInfo.IME_ACTION_GO || (event != null && event.getKeyCode() == KeyEvent.KEYCODE_ENTER)) {
                    loadAddress(); return true;
                }
                return false;
            });
            address.setText("https://example.com");
            loadAddress();
        } catch (Throwable t) {
            Toast.makeText(this, "GeckoView could not start: " + t.getClass().getSimpleName(), Toast.LENGTH_LONG).show();
        }
    }

    private void loadAddress() {
        if (session == null) return;
        String url = address.getText().toString().trim();
        if (url.isEmpty()) return;
        if (!url.contains("://")) {
            if (url.contains(" ")) url = "https://www.google.com/search?q=" + url.replace(" ", "+");
            else url = "https://" + url;
        }
        session.loadUri(url);
    }

    @Override public void onBackPressed() {
        if (session != null && session.getNavigationDelegate() != null) {
            // GeckoView 70 does not expose a synchronous canGoBack check here; Android back closes this first prototype.
        }
        super.onBackPressed();
    }

    @Override protected void onDestroy() {
        if (session != null) session.close();
        super.onDestroy();
    }
}
