package com.example.dell.blind;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;


import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.StrictMode;
import android.preference.PreferenceManager;
import android.telephony.SmsManager;
import android.util.Log;
import android.widget.Toast;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

public class Emergency extends  BroadcastReceiver{
	//JSONParser jParser = new JSONParser();
	SharedPreferences sh;
	public static String ip,url="";
	public static ArrayList<String> contact ,message;
	@Override
	public void onReceive(Context context, Intent intent) {
		// TODO Auto-generated method stub
		sh=PreferenceManager.getDefaultSharedPreferences(context);
		ip=sh.getString("ip","");
		url="http://"+ip+":5000/emergency";
        Log.d("+++++++++++++++++","ok");


		try
	    {
	    	if(android.os.Build.VERSION.SDK_INT > 9)
	    	{
	    		StrictMode.ThreadPolicy policy=new StrictMode.ThreadPolicy.Builder().permitAll().build();
	    		StrictMode.setThreadPolicy(policy);
	    	}
	    }
	    catch(Exception e)
	    {
	    	
	    }
	    int volume = (Integer)intent.getExtras().get("android.media.EXTRA_VOLUME_STREAM_VALUE");
	    if(volume!=0)
	    {

			RequestQueue requestQueue = Volley.newRequestQueue(context);
			StringRequest postRequest = new StringRequest(Request.Method.POST, url,
					new Response.Listener<String>() {
						@Override
						public void onResponse(String response) {

							try {

								JSONObject js = new JSONObject(response);
								String status = js.getString("task");
								if (status.equalsIgnoreCase("invalid")) {






								} else {






								}

							} catch (Exception ex) {
							//	Toast.makeText(context(),"hii"+ ex.getMessage().toString(), Toast.LENGTH_SHORT).show();

							}


						}
					},
					new Response.ErrorListener() {
						@Override
						public void onErrorResponse(VolleyError error) {
							// error
							//Toast.makeText(context(), "err"+error.toString(), Toast.LENGTH_SHORT).show();
						}
					}
			) {
				@Override
				protected Map<String, String> getParams() {

					Map<String, String> params = new HashMap<String, String>();


					params.put("imei", "imei");



					return params;
				}
			};

			requestQueue.add(postRequest);





		}
	};



//	    	String ip=sp.getString("ip", "");
//	    	ur="http://"+ip+":8080/Pink_Police/Relative_number";
//	    	 List<NameValuePair> params = new ArrayList<NameValuePair>();
//	    	   params.add(new BasicNameValuePair("uid", sp.getString("lid", "")));
//	            JSONObject json = jParser.makeHttpRequest(ur, "GET", params);
//	            Log.d("Reultttttt=====---------",json+"");
//	            try
//	            {
//	                //int success = json.getInt(TAG_SUCCESS);
//	                JSONArray ar=new JSONArray();
//	                ar=json.getJSONArray("product");
//	               // Log.d("+++++++++++",ar+"");
//	                contact=new ArrayList<String>();
//
//
//
//
//	                for (int i = 0; i < ar.length(); i++) {
//	                        JSONObject c = ar.getJSONObject(i);
//
//	                       contact.add(c.getString("contact"));
//
//
//	                         Log.d("+++++++++++",c+"");
//
//
//	                    }
//	                for(int i=0;i<ar.length();i++)
//	                {
//	                String msg="http://maps.google.com/maps?q="+LocationService.lati+","+LocationService.logi;
//	                SmsManager sms = SmsManager.getDefault();
//		            sms.sendTextMessage(contact.get(i),null,"help me "+msg,null,null);
//	                }
//
//	            }
//	            catch(JSONException e)
//	            {
//	                 Log.d("err====",e.getMessage());
//	            }

//	    	SmsManager sms = SmsManager.getDefault();
//            sms.sendTextMessage("8281233725",null,"help me",null,null);
	            
	    }


