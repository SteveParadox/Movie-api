import React, { useState, useEffect, useContext } from "react";
import { MovieContext } from "../MovieContext";
import { Link, Redirect } from "react-router-dom";
import { FaArrowRight } from "react-icons/fa";
import { BsFillCameraVideoFill } from "react-icons/bs";
import "../styles/Signin.css";
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
  const [redirect, setRedirect] = useState(false);
  const [state, updateState] = useContext(MovieContext);

  useEffect(() => {
    const getStorage = () => {
      const logged_in = window.localStorage.getItem("logged_in");
      // console.log(logged_in);
      // console.log(state);
      if(logged_in === "true") {
        setRedirect(true);
        updateState(n => {
          return {
            ...n,
            logged_in: true,
          };
        })
      // console.log(state);
      }
    }
    getStorage();
  }, [redirect, state, updateState]);

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
    login(body);

    // Redirect the page
    setRedirect(true);
  }

  return (
    <div className="sign-body">
      {redirect ? <Redirect to="/" /> : null}
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
                <button onClick={() => setCount(count + 1)}><FaArrowRight size={24} color="var(--font-color)" /></button>
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
                  <input type="password" style={{ "fontSize": "18.5px" }} name="password" id="passwordLogin" placeholder="Password..." minLength={6} maxLength={16} value={password} onChange={updatePassword} />
                  <button style={{"fontSize": "22px", "color": "var(--font-color)" }} onClick={submit}>
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