## Introduction

This project is a final project for API Course in Coursera created with Django Rest Framework. 

## Little Lemon Restaurant API
This project provides a fully functioning API for the Little Lemon restaurant, allowing client application developers to use the APIs to develop web and mobile applications. With this API, users with different roles can browse, add, and edit menu items, place orders, browse orders, assign delivery crew to orders, and deliver the orders.

## Requirements
To run this project, you will need the following installed on your machine:

Python 3.8 or higher
Pipenv


## Views
This project uses both function-based and class-based views.

## User groups
There are two user groups in this project: Manager and Delivery crew. 

## Error handling
This project handles errors by displaying appropriate HTTP status codes and error messages.

## Throttling

This project implement daily throttling at 10 request/day for anonymous user and 20 for registered user. Throttling setting can be change through settins.py found at root project.
<code>
'DEFAULT_THROTTLE_RATES': {
        'anon': '10/day',
        'user': '20/day'
    }
</code>
