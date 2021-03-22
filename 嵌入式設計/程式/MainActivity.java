package com.example.finalproject;

import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;

import android.app.DatePickerDialog;
import android.content.ContentValues;
import android.content.Context;
import android.content.DialogInterface;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuInflater;
import android.view.MenuItem;
import android.view.View;
import android.widget.AdapterView;
import android.widget.Button;
import android.widget.DatePicker;
import android.widget.EditText;
import android.widget.ListView;
import android.widget.SimpleCursorAdapter;
import android.widget.Spinner;
import android.widget.TextView;
import android.widget.Toast;

import java.util.Calendar;

public class MainActivity extends AppCompatActivity
        implements AdapterView.OnItemClickListener, AdapterView.OnItemSelectedListener,
                    DatePickerDialog.OnDateSetListener,DialogInterface.OnClickListener {

    static final String db_name = "db"; //資料庫名稱
    static final String tb_name = "tb"; //資料表名稱
    static final String[] FROM = new String[] {"date","type","name","price"};
    SQLiteDatabase db; //資料庫物件
    Cursor cur;
    SimpleCursorAdapter adapter;
    EditText  editName,editPrice;
    Spinner spinner;
    Button btnInsert,btnUpdate,btnDelete;
    ListView lv;
    String typeStr,search_type;

    Calendar c = Calendar.getInstance();
    TextView txvDate;
    int dateset=0;  //1表設定日期 2表查詢日期

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        editName = (EditText)findViewById(R.id.editName);
        editPrice = (EditText)findViewById(R.id.editPrice);
        spinner = (Spinner)findViewById(R.id.spinner);
        spinner.setOnItemSelectedListener(this);
        txvDate = (TextView)findViewById(R.id.txvDate);

        btnDelete = (Button)findViewById(R.id.btnDelete);
        btnInsert = (Button)findViewById(R.id.btnInsert);
        btnUpdate = (Button)findViewById(R.id.btnUpdate);


        db = openOrCreateDatabase(db_name, Context.MODE_PRIVATE,null);

        String createTable = "CREATE TABLE IF NOT EXISTS " +
                tb_name +
                "(_id INTEGER PRIMARY KEY AUTOINCREMENT, "+
                "date VARCHAR(32),"+
                "type VARCHAR(32),"+
                "name VARCHAR(32), "+
                "price INTEGER)";
        db.execSQL(createTable);

        cur = db.rawQuery("SELECT * FROM " + tb_name,null);
        adapter = new SimpleCursorAdapter(this,
                R.layout.item,cur,
                FROM,
                new int[]{R.id.date,R.id.type,R.id.name,R.id.price},0);

        lv = (ListView)findViewById(R.id.lv);
        lv.setAdapter(adapter);
        lv.setOnItemClickListener(this);
        requery();



    }
    //新增
    private void addData(String date ,String type ,String name , String price){
        ContentValues cv = new ContentValues(2);
        cv.put(FROM[0],date);
        cv.put(FROM[1],type);
        cv.put(FROM[2],name);
        cv.put(FROM[3],price);

        db.insert(tb_name,null,cv);
        editName.setText("");
        editPrice.setText("");
    }
    //更新
    private void update(String date ,String type ,String name , String price,int id){
        ContentValues cv = new ContentValues(2);
        cv.put(FROM[0],date);
        cv.put(FROM[1],type);
        cv.put(FROM[2],name);
        cv.put(FROM[3],price);

        db.update(tb_name,cv,"_id="+id,null);
        editName.setText("");
        editPrice.setText("");
    }
    private void requery(){
        cur = db.rawQuery("SELECT * FROM "+tb_name,null);
        adapter.changeCursor(cur);

        btnInsert.setEnabled(true);
        btnUpdate.setEnabled(false);
        btnDelete.setEnabled(false);
    }

    @Override
    public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
        cur.moveToPosition(position);

        txvDate.setText(cur.getString(cur.getColumnIndex(FROM[0])));
        editName.setText(cur.getString(cur.getColumnIndex(FROM[2])));
        editPrice.setText(cur.getString(cur.getColumnIndex(FROM[3])));

        btnUpdate.setEnabled(true);
        btnDelete.setEnabled(true);
    }

    public void onInsertUpdate(View v){
        String dateStr = txvDate.getText().toString().trim();
        String nameStr = editName.getText().toString().trim();
        String priceStr = editPrice.getText().toString().trim();
        if(dateStr.equals(getResources().getString(R.string.dateNotset))||nameStr.length()==0||priceStr.length()==0)
            return;
        if(v.getId()==R.id.btnUpdate)
            update(txvDate.getText().toString(),typeStr,nameStr,priceStr,cur.getInt(0));
        else
            addData(txvDate.getText().toString(),typeStr,nameStr,priceStr);
        requery();
    }
    public void onDelete(View v){
        db.delete(tb_name, "_id="+cur.getInt(0),null);
        editName.setText("");
        editPrice.setText("");
        requery();
    }

    @Override
    public void onItemSelected(AdapterView<?> parent, View view, int position, long id) {
        TextView txv = (TextView) view;
        typeStr = txv.getText().toString();
    }

    @Override
    public void onNothingSelected(AdapterView<?> parent) {

    }

    //設日期 查詢日期資訊
    @Override
    public void onDateSet(DatePicker view, int year, int month, int dayOfMonth) {
        int all = 0;
        int income = 0;
        if(dateset==1) {
            txvDate.setText(year + "/" + (month + 1) + "/" + dayOfMonth);
            //Toast.makeText(this, "日期已更正", Toast.LENGTH_LONG).show();
        }
        else{
            String searchResult="";
            String date = (year + "/" + (month + 1) + "/" + dayOfMonth);
            //Toast.makeText(this,date, Toast.LENGTH_LONG).show();
            Cursor searchdate = db.rawQuery("SELECT * FROM "+tb_name+" WHERE date = \'"+date+"\'",null);
            if(searchdate.moveToFirst()){
                searchResult+=date+"\n";
                do{
                    if(!searchdate.getString(2).equals(getResources().getString(R.string.income))) {
                        searchResult += "-----------------------\n";
                        searchResult += getResources().getString(R.string.type) + ":";
                        searchResult += searchdate.getString(2) + "\n";
                        searchResult += getResources().getString(R.string.name) + ":";
                        searchResult += searchdate.getString(3) + "\n";
                        searchResult += getResources().getString(R.string.price) + ":";
                        searchResult += searchdate.getString(4) + "\n";
                        all += searchdate.getInt(4);
                    }
                }while(searchdate.moveToNext());
                searchResult+="-----------------------\n";
                searchResult+=getResources().getString(R.string.outcome)+":";
                searchResult+=String.valueOf(all)+"\n\n";
                if(searchdate.moveToFirst()){
                    do{
                        if(searchdate.getString(2).equals(getResources().getString(R.string.income))) {
                            searchResult += "-----------------------\n";
                            searchResult += getResources().getString(R.string.type) + ":";
                            searchResult += searchdate.getString(2) + "\n";
                            searchResult += getResources().getString(R.string.name) + ":";
                            searchResult += searchdate.getString(3) + "\n";
                            searchResult += getResources().getString(R.string.price) + ":";
                            searchResult += searchdate.getString(4) + "\n";
                            income += searchdate.getInt(4);
                        }
                    }while(searchdate.moveToNext());
                    searchResult+="-----------------------\n";
                    searchResult+=getResources().getString(R.string.income)+":";
                    searchResult+=String.valueOf(income)+"\n";
                }
            }
            else{
                searchResult+=getResources().getString(R.string.Notfound);
            }
            new AlertDialog.Builder(this)
                    .setMessage(searchResult)
                    .setNeutralButton(getResources().getString(R.string.cancel),this)
                    .show();
        }
    }

    //menu
    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        MenuInflater inflater = getMenuInflater();
        inflater.inflate(R.menu.example_menu,menu);
        return true;
    }
    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        switch (item.getItemId()) {
            case R.id.menuDate:
                dateset=1;
                new DatePickerDialog(this,this,
                        c.get(Calendar.YEAR),
                        c.get(Calendar.MONTH),
                        c.get(Calendar.DAY_OF_MONTH)).show();
                return true;
            case R.id.menuSearch:
                new AlertDialog.Builder(this)
                        .setMessage(getResources().getString(R.string.DialogMessage))
                        .setNeutralButton(getResources().getString(R.string.cancel),this)
                        .setPositiveButton(getResources().getString(R.string.date),this)
                        .setNegativeButton(getResources().getString(R.string.type),this)
                        .show();
                return true;
            default:
                return super.onOptionsItemSelected(item);
        }
    }

    @Override
    public void onClick(DialogInterface dialog, int which) {
        if(which == DialogInterface.BUTTON_POSITIVE){
            dateset=2;
            new DatePickerDialog(this,this,
                    c.get(Calendar.YEAR),
                    c.get(Calendar.MONTH),
                    c.get(Calendar.DAY_OF_MONTH)).show();
        }
        else if(which == DialogInterface.BUTTON_NEGATIVE){
            new AlertDialog.Builder(this)
                    .setView(R.layout.search)
                    .setNeutralButton(getResources().getString(R.string.cancel),this)
                    .show();
        }
    }

    //查詢分類
    public void search_search(View v){
        int all = 0;
        switch (v.getId()){
            case R.id.search_diet:
                search_type = getResources().getString(R.string.diet);
                break;
            case R.id.search_traffic:
                search_type = getResources().getString(R.string.traffic);
                break;
            case R.id.search_entertainment:
                search_type = getResources().getString(R.string.entertainment);
                break;
            case R.id.search_clothing:
                search_type = getResources().getString(R.string.clothing);
                break;
            case R.id.search_others:
                search_type = getResources().getString(R.string.others);
                break;
            case R.id.search_income:
                search_type = getResources().getString(R.string.income);
                break;
        }
        String searchResult="";
        Cursor searchtype = db.rawQuery("SELECT * FROM "+tb_name+" WHERE type = \'"+search_type+"\'",null);
        if(searchtype.moveToFirst()){
            searchResult+=search_type+"\n";
            do{
                searchResult+="-----------------------\n";
                searchResult+=getResources().getString(R.string.date)+":";
                searchResult+=searchtype.getString(1)+"\n";
                searchResult+=getResources().getString(R.string.name)+":";
                searchResult+=searchtype.getString(3)+"\n";
                searchResult+=getResources().getString(R.string.price)+":";
                searchResult+=searchtype.getString(4)+"\n";
                all+=searchtype.getInt(4);
            }while(searchtype.moveToNext());
            searchResult+="-----------------------\n";
            searchResult+=getResources().getString(R.string.total)+":";
            searchResult+=String.valueOf(all);
        }
        else{
            searchResult+=getResources().getString(R.string.Notfound);
        }
        new AlertDialog.Builder(this)
                .setMessage(searchResult)
                .setNeutralButton(getResources().getString(R.string.cancel),this)
                .show();
    }
}