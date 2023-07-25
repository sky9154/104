## 系統環境

| 名稱      | 版本   |
| ------------- | ------ |
| Python | 3.10.9  |

## 安裝套件

| 名稱      | 版本   |
| ------------- | ------ |
| python-dotenv | 1.0.0  |
| requests      | 2.31.0 |
| pymssql       | 2.2.7  |

## 軟體設定

設定檔位置: `.env`

### CLIENT_ID

用戶端識別碼

### CLIENT_SECRET

用戶端密鑰

### DB_HOST

資料庫主機名稱

### DB_NAME

資料庫表格名稱

### SQL_PATH

SQL 檔檔案位置，預設位置為 `sql/select.sql`

### AUTO

是否開啟自動上傳


如需上傳指定的時間段，只需將選項改為`否`，以及設定開始及結束的時間，
啟動程式後將會上傳指定的時間段。

```
是: TRUE / True / true / t
否: FALSE / False / fasle / f
```

#### 範例

```
AUTO          = False
BEGIN_DATE    = '20230604 00:00:00.000'
END_DATE      = '20230604 23:59:59.999'
```

### BEGIN_DATE

開始時間

#### 格式

```
YYYY-MM-DD HH:MI:SS
```

#### 範例

```
'20230604 00:00:00.000'
```


### END_DATE

結束時間

#### 格式

```
YYYY-MM-DD HH:MI:SS
```

#### 範例

```
'20230604 23:59:59.999'
```

## 上傳紀錄

### 上傳結果

位置: `log/system/{date_time}.log`

[結果說明](https://pro.104.com.tw/hrmapi/docs/index.html#api-Send_card_data-transferCard)

### 上傳名單

位置: `log/user/{date_time}.log`