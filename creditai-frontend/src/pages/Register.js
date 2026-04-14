import React, { useState } from "react";
import axios from "axios";
import { useNavigate, Link } from "react-router-dom";
import { Container, TextField, Button, Typography, Card, CardContent } from "@mui/material";

function Register(){

const navigate = useNavigate()

const [name,setName] = useState("")
const [email,setEmail] = useState("")
const [password,setPassword] = useState("")

const handleRegister = async () => {

try{

await axios.post(
"http://localhost:5000/register",
{
name:name,
email:email,
password:password
}
)

alert("Registration Successful")

navigate("/")

}

catch(error){

alert("Email already exists")

}

}

return(

<Container maxWidth="sm" style={{marginTop:"100px"}}>

<Card>
<CardContent>

<Typography variant="h4" align="center">
Register
</Typography>

<br/>

<TextField
label="Name"
fullWidth
margin="normal"
onChange={(e)=>setName(e.target.value)}
/>

<TextField
label="Email"
fullWidth
margin="normal"
onChange={(e)=>setEmail(e.target.value)}
/>

<TextField
label="Password"
type="password"
fullWidth
margin="normal"
onChange={(e)=>setPassword(e.target.value)}
/>

<br/>

<Button
variant="contained"
color="primary"
fullWidth
onClick={handleRegister}
>
Register
</Button>

<br/><br/>

<Typography align="center">
Already have an account? <Link to="/">Login</Link>
</Typography>

</CardContent>
</Card>

</Container>

)

}

export default Register