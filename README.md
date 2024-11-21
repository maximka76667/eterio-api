# Eterio ![image](https://github.com/user-attachments/assets/f96cf865-81c7-448e-84b9-5b57dac47945)

This project is a cocktails and drinks library, which i did as my final Superior Grade project.  
[**Demonstration**](https://maximka76667.github.io/eterio)



This repository is a **backend** part of the project.  
Written on **`Python`** + **`FastAPI`** + **`Google Firebase`**.  

Deployed using **`Docker`** container and **`Google Cloud Run`**.  
*Google Cloud URL*: (https://eterio-api-489286482375.europe-southwest1.run.app)

*Frontend repo*: https://github.com/maximka76667/eterio

## Usage (routes)

### `Users`

#### Models
- Default User: `User: { id: str, email: str, name: str, avatar: str }`  
- Creating User: `UserCreate { email: str, name: str, password: str }`  
- Updating user: `UserUpdate: { email: str, name: str, avatar: str }`  
- UserInDb: `UserInDb: { id: str, email: str, name: str, avatar: str, password: str }`  

#### Routes
###### GET `/users` : `User[]`  

Returns all users.

###### POST  `/users` : `User`  
`Body: UserCreate`  
Creates a new user. Returns the created user.

###### GET  `/users/me` : `UserInDb`  --requires auth  

Returns the current authenticated user.

###### PUT `(UserUpdate)` `/users/me` : `User`  --requires auth
`Body: UserUpdate`    
Updates the current authenticated user. Returns the updated user.

###### GET  `/users/{user_id}` : `User`  

Returns a user by their ID.

###### PUT `(UserUpdate)` `/users/{user_id}` : `User`  --requires auth
`Body: UserUpdate`  
Updates a user by their ID. Returns the updated user.

###### DELETE `/users/{user_id}` : `User`  --only for admin

Deletes a user by their ID. Returns the deleted user.

---

### `Drinks`

#### Models
- Default Drink: `Drink: { name: str, img: str, code: str, ingredients: Dict[str, int], extra: List[str], description: str, is_community: bool, favorites: List[str], author: str, date: str, category: str }`  
- DrinkInDb: `DrinkInDb: { id: str, name: str, img: str, code: str, ingredients: Dict[str, int], extra: List[str], description: str, is_community: bool, favorites: List[str], author: str, date: str, category: str }`  

#### Routes

###### POST `/drinks` : `DrinkInDb`
Creates a new drink.

###### GET `/drinks/{drink_id}` : `DrinkInDb`
Fetches a specific drink by its ID.

###### GET `/drinks` : `DrinkInDb[]`
Returns all drinks.

###### PUT `/drinks/{drink_id}` : `DrinkInDb`
Updates a drink by its ID.

###### DELETE `/drinks/{drink_id}` : `Message`
Deletes a drink by its ID.

###### PUT `/drinks/favs/{drink_id}` : `DrinkInDb`
Adds the current user to the favorites list of a specific drink.

###### DELETE `/drinks/favs/{drink_id}` : `DrinkInDb`
Removes the current user from the favorites list of a specific drink.

---

### `Auth`

#### Models:
- `UserLogin`: `{ email: str, password: str }`
- `Token`: `{ access_token: str, token_type: str }`

#### Routes

###### POST `/login` : `Token`
`Body: UserLogin`  
Logs in a user and returns a bearer token for authentication.


---

### `Categories`

#### Models:
- `Category`: `{ name: str }`
- `CategoryInDb`: `{ id: str, name: str }`

#### Routes

###### GET `/categories` : `CategoryInDb[]`
Returns a list of all categories.


---

### `Bottles`

#### Models:
- `Bottle`: `{ name: str, img: str }`
- `BottleInDb`: `{ id: str, name: str, img: str }`

#### Routes

###### GET `/bottles` : `BottleInDb[]`
Returns a list of all bottles.


---
