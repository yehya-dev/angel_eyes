package com.example.dell.blind;

import android.content.Intent;
import android.content.SharedPreferences;
import android.preference.PreferenceManager;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONObject;

import java.util.HashMap;
import java.util.Map;

public class Signin extends AppCompatActivity {
    EditText e1;
    Button b1;
    String cnum;
    String ip="",url="";
    SharedPreferences sh;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_signin);
        e1=(EditText)findViewById(R.id.editText);
        b1=(Button)findViewById(R.id.button2);


        sh= PreferenceManager.getDefaultSharedPreferences(getApplicationContext());
        ip=sh.getString("ip","");
//        SharedPreferences.Editor ed= sh.edit();
//        ed.putString("ip",ip);
//        ed.commit();
        String ph=sh.getString("phno","na");
        if(!ph.equalsIgnoreCase("na"))
        {
            Intent a = new Intent(getApplicationContext(), Home.class);
            startActivity(a);

        }
        Log.d("+++++++++++++++++","ok");

        url="http://"+ip+":5000/bsign";

        b1.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                cnum = e1.getText().toString();
                if(cnum.equals(""))
                {
                    e1.setError("enter contactno");
                }
                else if(cnum.length()!=10)
                {
                    e1.setError("invalid no");
                }
                else {
                    RequestQueue requestQueue = Volley.newRequestQueue(getApplicationContext());
                    StringRequest postRequest = new StringRequest(Request.Method.POST, url,
                            new Response.Listener<String>() {
                                @Override
                                public void onResponse(String response) {

                                    try {

                                        JSONObject js = new JSONObject(response);
                                        String status = js.getString("task");
                                        if (status.equalsIgnoreCase("invalid")) {


                                            Toast.makeText(getApplicationContext(), " Signin failed!!.Inserted number is incorrect.", Toast.LENGTH_SHORT).show();
                                            Intent a = new Intent(getApplicationContext(), Signin.class);
                                            startActivity(a);

                                        } else {
                                            SharedPreferences.Editor ed = sh.edit();
                                            ed.putString("lid", status);
                                            ed.putString("phno", cnum);
                                            ed.commit();

                                            Toast.makeText(getApplicationContext(), "Signin successfull.", Toast.LENGTH_SHORT).show();
                                            Intent a = new Intent(getApplicationContext(), Home.class);
                                            startActivity(a);
//                                            Intent ik = new Intent(getApplicationContext(), LocationService.class);
//                                            startService(ik);


                                        }

                                    } catch (Exception ex) {
                                        Toast.makeText(getApplicationContext(), "hii" + ex.getMessage().toString(), Toast.LENGTH_SHORT).show();

                                    }


                                }
                            },
                            new Response.ErrorListener() {
                                @Override
                                public void onErrorResponse(VolleyError error) {
                                    // error
                                    Toast.makeText(getApplicationContext(), "err" + error.toString(), Toast.LENGTH_SHORT).show();
                                }
                            }
                    ) {
                        @Override
                        protected Map<String, String> getParams() {

                            Map<String, String> params = new HashMap<String, String>();

                            params.put("cnum", cnum);


                            return params;
                        }
                    };

                    requestQueue.add(postRequest);

                }
            }
        });
    }
}
