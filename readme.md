## Introduction

This project is a final project for API Course in Coursera created with Django Rest Framework. 

## Little Lemon Restaurant API
This project provides a fully functioning API for the Little Lemon restaurant, allowing client application developers to use the APIs to develop web and mobile applications. With this API, users with different roles can browse, add, and edit menu items, place orders, browse orders, assign delivery crew to orders, and deliver the orders.

## Requirements
To run this project, you will need the following installed on your machine:

Python 3.8 or higher
Pipenv
Installation
Clone this repository.
Navigate to the root directory of the project.
Run the command pipenv install to install the required dependencies.


## Views
This project uses both function-based and class-based views. The proper API naming convention should be followed throughout the project.

## User groups
There are two user groups in this project: Manager and Delivery crew. You should create some random users and assign them to these groups from the Django admin panel. Users not assigned to a group will be considered customers.

## Error handling
This project handles errors by displaying appropriate HTTP status codes and error messages.

## Additional step

Implement proper filtering, pagination and sorting capabilities for /api/menu-items and /api/orders endpoints. Review the videos about [Filtering and searching](https://www.coursera.org/teach/apis/g98MzcdAEeyduw6ktL3Xvw/content/item/lecture/h7QUx/video-subtitles) and [Pagination](https://www.coursera.org/teach/apis/g98MzcdAEeyduw6ktL3Xvw/content/item/lecture/mEYFj/video-subtitles) as well as the reading [More on filtering and pagination](https://www.coursera.org/teach/apis/g98MzcdAEeyduw6ktL3Xvw/content/item/supplement/oCL3M).

## Throttling

Finally, apply some throttling for the authenticated users and anonymous or unauthenticated users. Review the video [Setting up API throttling](https://www.coursera.org/teach/apis/g98MzcdAEeyduw6ktL3Xvw/content/item/lecture/rPE4B/video-subtitles) and the reading [API throttling for class-based views](https://www.coursera.org/teach/apis/g98MzcdAEeyduw6ktL3Xvw/content/item/supplement/1h6WO) for guidance.

## Conclusion

Now that you have a better idea of the scope of this project with the essential API endpoints, it’s time to start coding. Good luck!