import React, { useState } from "react";
import { Link } from "react-router-dom";
import { FaArrowRight } from "react-icons/fa";
import { BsFillCameraVideoFill } from "react-icons/bs";
import "../styles/Signin.css";
import { set } from "date-fns/esm";
import { login } from "./Helper";

const Nav = () => {
  return (
    <nav>
      <div className="logo"><BsFillCameraVideoFill /> {" "}<Link to="/" className="name">Filba</Link></div>
      <div className="signBtn"><Link to="/signup"><button>Signup</button></Link></div>
    </nav>
  );
}

function Signin() {
  const [count, setCount] = useState(1);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const updateEmail = e => {
    setEmail(e.target.value);
  }

  const updatePassword = e => setPassword(e.target.value);

  const submit = () => {
    const body = {
      email,
      password
    };
    console.log(body);
    const result = login(body);
    if(result.success) {
      // Store the token in local storage and redirect to home page
      console.log(result);
    } else {
      // Else write an error message saying login failed
    }
  }

  return (
    <div className="sign-body">
      <Nav />
      <div className="main">
        {
          count === 1 ? (
            <>
              <div className="center">
                <p>Share that wonderful experience</p>
                <p>Anywhere & Anytime</p>
                <p className="red">Take the thrill with you.</p>
              </div>
              <div className="signin-form">
                <input type="email" name="email" id="emailLogin" placeholder="Email..." value={email} onChange={updateEmail} />
                <button onClick={() => setCount(count + 1)}><FaArrowRight size={24} color="white" /></button>
              </div>
            </>
          ) : null
        }
        

        {/* For the next */}
        {
          count === 2 ? (
            <>
              <div className="center">
                <p>Recommend a great show</p>
                <p>for your friends.</p>
                <p className="red">Let's see what your friends pick for you.</p>
              </div>
              <div className="signin-form">
                  <input type="password" style={{ "fontSize": "16px" }} name="password" id="passwordLogin" placeholder="Password..." minLength={6} maxLength={16} value={password} onChange={updatePassword} />
                  <button style={{"fontSize": "22px", "color": "white" }} onClick={submit}>
                    Login
                  </button>
              </div>
            </>
          ) : null
        }
      </div>
    </div>
  );
}

export default Signin;