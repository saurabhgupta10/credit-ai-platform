import {BrowserRouter,Routes,Route} from "react-router-dom"

import Login from "./pages/Login"
import Register from "./pages/Register"
import UserDashboard from "./pages/UserDashboard"
import AdminDashboard from "./pages/AdminDashboard"

function App(){

return(

<BrowserRouter>

<Routes>

<Route path="/" element={<Login/>}/>

<Route path="/register" element={<Register/>}/>

<Route path="/user-dashboard" element={<UserDashboard/>}/>

<Route path="/admin-dashboard" element={<AdminDashboard/>}/>

</Routes>

</BrowserRouter>

)

}

export default App