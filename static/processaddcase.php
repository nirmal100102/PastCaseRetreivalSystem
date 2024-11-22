<?php
$servername = "localhost";
$username = "root";
$password = "root";
$dbname = "past_cases_db";

$conn = new mysqli($servername, $username, $password, $dbname);

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

$id = $_POST['id'];
$case_description = $_POST['case_description'];
$keyword = $_POST['keyword'];
$date = $_POST['date'];
$status = $_POST['status'];
$created_at = $_POST['created_at'];
$criminal_name = $_POST['criminal_name'];
$officer_name = $_POST['officer_name'];

$sql = "INSERT INTO cases (ID, Case_Description, Keyword, Date, Status, Created_At, Criminal_Name, Officer_Name)
        VALUES ('$id', '$case_description', '$keyword', '$date', '$status', '$created_at', '$criminal_name', '$officer_name')";

if ($conn->query($sql) === TRUE) {
    echo "New case added successfully. <a href='/'>Go back to Home Page</a>";
} else {
    echo "Error: " . $sql . "<br>" . $conn->error;
}

$conn->close();
?>
