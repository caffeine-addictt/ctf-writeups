# Bakery Sprint

This challenge is a bit special with 2 flags and 2 different attack vectors.

<!--toc:start-->
- [Bakery Sprint](#bakery-sprint)
  - [Context](#context)
  - [Flag 1](#flag-1)
    - [1a. You can manually change the recipe-id in the URL](#1a-you-can-manually-change-the-recipe-id-in-the-url)
    - [1b. Following RESTful API principals](#1b-following-restful-api-principals)
    - [2. Find the missing ID](#2-find-the-missing-id)
    - [3. Navigate to /recipes/43](#3-navigate-to-recipes43)
  - [Flag 2](#flag-2)
    - [1. Creating a new user](#1-creating-a-new-user)
    - [2. Identify user accounts not using JWT signing](#2-identify-user-accounts-not-using-jwt-signing)
    - [3. Find users endpoint](#3-find-users-endpoint)
    - [4. HTTP GET to `/api/v1/user`](#4-http-get-to-apiv1user)
    - [5. Edit user_id cookie](#5-edit-userid-cookie)
    - [6. Navigate to /profile](#6-navigate-to-profile)
<!--toc:end-->

## Context

Anne has 100 recipes posted on her website.

![recipes](assets/recipies.png)

Clicking on any one of the recipes, shows the steps to make it.

![recipe Steps](assets/recipie-steps.png)

There is also user logins

![Login Page](assets/login.png)

## Flag 1

Each recipe's page follows the syntax `/recipes/<recipie-id>`.
This is a simple `directory traversal attack`.

### 1a. You can manually change the recipe-id in the URL

Iterate the URL

```text
/recipe/1
/recipe/2
...
/recipe/100
```

This is slow however, because there is 100 recipies to iterate through.

### 1b. Following RESTful API principals

You can discover that the endpoint `/api/v1/recipe` exists.
Sending a GET request returns all the recipies.

![Recipes GET API](assets/recipes-get.png)

### 2. Find the missing ID

Looking at the IDs, you can discover that id 43 is skipped over.

![Missing ID](assets/missing-id.png)

### 3. Navigate to /recipes/43

The rendered page doesn't give us much, but looking at the HTML gives us the flag.

![Flag 1](assets/flag-1.png)

Flag: `NYP{hEymySEcr37ReCIpI35m@n}`

## Flag 2

This is part uses `session hijacking`.

### 1. Creating a new user

We create a user account ourselves to discover how session/authentication works.

### 2. Identify user accounts not using JWT signing

Notice that a cookie called `user_id` is used to identify which user is logged in.

![Bad cookie](assets/bad-cookie.png)

### 3. Find users endpoint

On the `/login` page, notice that there is a random HTTP PUT request to `/api/v1/user` which returns code `405`.

405 response means that the method is not allowed, and does not necessarily mean that the route is invalid.

![405](assets/405.png)

### 4. HTTP GET to `/api/v1/user`

The endpoint returns all the users, including their admin status. It's anne's Bakery so lets grep for `anne`.

![User GET API](assets/user-api.png)

### 5. Edit user_id cookie

Replace the user_id cookie with the value `8`.

### 6. Navigate to /profile

![Flag 2](assets/flag-2.png)

Flag: `NYP{nOWiOwn4L17heREC1P1E5}`
