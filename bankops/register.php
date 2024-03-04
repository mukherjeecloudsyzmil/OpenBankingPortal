<?php
include 'db_connection.php';

$username = $_POST['username'];
$email = $_POST['email'];
$password = password_hash($_POST['password'], PASSWORD_DEFAULT);
$phone = $_POST['phone']; // Assuming 'phone' is the name attribute of the phone number input field
$country = $_POST['country']; // Assuming 'country' is the name attribute of the country select field
$account_type = $_POST['account_type']; // Assuming 'account_type' is the name attribute of the account type select field

// Initialize ID details variables
$id_details = '';
$pan_card = '';
$national_id = '';
$ssn = '';

// Check selected country and assign appropriate ID details
if ($country === 'India') {
    $pan_card = $_POST['pan_card']; // Assuming 'pan_card' is the name attribute of the PAN Card input field
} elseif ($country === 'UK') {
    $national_id = $_POST['national_id']; // Assuming 'national_id' is the name attribute of the National ID input field
} elseif ($country === 'USA') {
    $ssn = $_POST['ssn']; // Assuming 'ssn' is the name attribute of the SSN input field
} else {
    $id_details = $_POST['id_details']; // Assuming 'id_details' is the name attribute of the generic ID details input field
}

$father_name = $_POST['father_name'];
$mother_name = $_POST['mother_name'];
$address = $_POST['address'];
$zip_code = $_POST['zip_code'];

$sql = "INSERT INTO users (username, email, password, phone, country, account_type, ID_details, pan_card, national_id, ssn, father_name, mother_name, address, zip_code) 
        VALUES ('$username', '$email', '$password', '$phone', '$country', '$account_type', '$id_details', '$pan_card', '$national_id', '$ssn', '$father_name', '$mother_name', '$address', '$zip_code')";

if ($conn->query($sql) === TRUE) {
    $user_id = $conn->insert_id;
    $unique_id = uniqid('user_');
    $sql_update = "UPDATE users SET unique_id = '$unique_id' WHERE id = '$user_id'";
    if ($conn->query($sql_update) === TRUE) {
        echo "Registration successful. Your unique ID is: $unique_id";
    } else {
        echo "Error updating user with unique ID: " . $conn->error;
    }
} else {
    echo "Error: " . $sql . "<br>" . $conn->error;
}

$conn->close();
?>
