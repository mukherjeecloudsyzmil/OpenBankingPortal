<?php
$servername = "localhost"; // Change this if your MySQL server is on a different host
$username = "bankuser"; // Replace with your MySQL username
$password = "bank@123"; // Replace with your MySQL password
$database = "bank"; // Replace with the name of your database

// Create connection
$conn = new mysqli($servername, $username, $password, $database);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}
?>
