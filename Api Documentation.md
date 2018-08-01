**Api Endponts**
----
**URL**
  ```
  /api/create_account
  ```
* **Method**
  `POST`

* **Data Params**
  ```
  username=[username]
  email=[emailId]
  password=[min 8 characters]
  first_name=[String]
  last_name=[String]
  ```

* **Success Response**
  * **Code:** 200
    **Content:** ```{"username":"foobar",
                     "email":"emailid",
                     "first_name":"foo",
                     "last_name":"bar"}```

* **Error Response**

  * **Code:** 400
    **Content** ```{
    "field": [
        "This field is required."
    ],}```

  * **Code:** 400
  **Content** ```{
    "username": [
        "A user with that username already exists."
    ],}```

  * **Code:** 400
  **Content** ```{
    "password": [
        "This password is too short. It must contain at least 8 characters."
    ]}```


  ----
  **URL**
    ```
    /api/login
    ```
  * **Method**
    `POST`

  * **Data Params**
    ```
    email=[email]
    password=[min 8 characters]
    ```

  * **Success Response**
    * **Code:** 200
      **Content:** ```{"login":True}```

  * **Error Response**

    * **Code:** 401
      **Content:** ```{"login":"False"}```

    * **Code:** 400 -- bad request
    **Content** ```{}```  

  ----
 **URL**
    ```
    /api/logout
    ```
  * **Method**
    `GET`


  * **Success Response**
    * **Code:** 200
      **Content:** ```{"logout":True}```

  * **Error Response**

    * **Code:** 403


  ----
  **URL**
    ```
    /api/change_password
    ```
  * **Method**
    `POST`

  * **Data Params**
    ```
    old_password=[old_password]
    new_password=[new_password]
    ```

  * **Success Response**
    * **Code:** 200
      **Content:** ```{"password":["changed"]}```

  * **Error Response**

    * **Code:** 400
      **Content:** ```{old_password": ["Wrong password."]}    ```

  * **Code:** 400
    **Content:** ```
    {
    "password": [
        "This password is too short. It must contain at least 8 characters.",
        "This password is too common."
    ]
}```


  ----
  **URL**
    ```
    /api/password_reset
    ```
  * **Method**
    `POST`

  * **Data Params**
    ```
    email=[email]
    ```

  * **Success Response**
    * **Code:** 200
      **Content:** ```"success"```

  * **Error Response**

    * **Code:** 400
      **Content:** ```"Email id is not registered"```


  ----
  **URL**
    ```
    /api/ask
    ```
  * **Method**
    `GET`


  * **Success Response**
    * **Code:** 200
      **Content:** ```
      {
    "level": 2,
    "source_hint": "Plata or Plomo?"
}```

  * **Error Response**

    * **Code:** 403
      **Content:** ```{"detail": "Authentication credentials were not provided."}```

  ----
  **URL**
    ```
    /api/answer
    ```
  * **Method**
    `POST`

  * **Data Params**
    ```
    answer=[answer]
    ```

  * **Success Response**
    * **Code:** 200
      **Content:** ```"{'answer': 'Correct'}" or {'answer': 'Wrong'}```

  * **Error Response**

    * **Code:** 403
      **Content:** ```{"detail": "Authentication credentials were not provided."}```
