import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import PhoneInput from "react-phone-input-2";
import "react-phone-input-2/lib/style.css";
import { BsFillCameraVideoFill } from "react-icons/bs";
import { FaArrowLeft, FaArrowRight } from "react-icons/fa";
import "../styles/Signin.css";
import { register } from "./Helper";
import axios from "axios";

// Date Picker
import { enGB } from 'date-fns/locale'
import { DatePicker } from 'react-nice-dates'
import 'react-nice-dates/build/style.css'

const Nav = () => {
  return (
    <nav>
      <div className="logo"><BsFillCameraVideoFill /> {" "}<Link to="/" className="name">Filba</Link></div>
      <div className="signBtn"><Link to="/signin"><button>Signin</button></Link></div>
    </nav>
  );
}

function Signup() {
  const [form, updateForm] = useState({
    firstName: "",
    lastName: "",
    userName: "",
    dob: "",
    email: "",
    password1: "",
    password2: "",
    number: "",
    country: ""
  });
  
  const [date, setDate] = useState(new Date(2020, 1, 24, 18, 15));
  

  // Helper functions
  const updateFirstName = (e) => updateForm(n => {
    return { ...n, [e.target.name]: e.target.value }
  });
  
  const updateLastName = (e) => updateForm(n => {
    return { ...n, [e.target.name]: e.target.value }
  });
  
  const updateUserName = (e) => updateForm(n => {
    return { ...n, [e.target.name]: e.target.value }
  });

  const updateEmail = (e) => updateForm(n => {
    return { ...n, [e.target.name]: e.target.value }
  });
  
  const updatePassword1 = (e) => updateForm(n => {
    return { ...n, [e.target.name]: e.target.value }
  });

  const updatePassword2 = (e) => updateForm(n => {
    return { ...n, [e.target.name]: e.target.value }
  });
  
  const updateNumber = (phone) => updateForm(n => {
    return { ...n, number: phone }
  });
  
  // const updateCountry = e => updateForm(n => {
  //   return { ...n, country: e.target.value };
  // });

  const [country, updateCountry] = useState("");
  const changeCountry = e => updateCountry(e.target.value);
  
  const SelectCountry = () => {
    const [countries, setCountries] = useState([]);
    useEffect(() => {
      // Note if you want to make this process/function async it's better to write a seperate async function else you get a cleanup warning from react.js
      // don't don this useEffect(async () => ...) but you can call an async function from inside it.
      let isCancelled = false;
      axios.get("https://trial.mobiscroll.com/content/countries.json")
      .then(res => {
        if(!isCancelled) {
          setCountries(res.data)
        }
      })
      .catch(err => {
        if(!isCancelled) {
          console.log("Sorry an error occured :(");
        }
      });
    }, []);
    return (
      <select name="country" className="select-css" id="countries" value={country} onChange={changeCountry}>
        {countries.map(i => <option key={i.text}>{i.text}</option>)}
      </select>
    );
  }
  
  
  useEffect(() => {
    form["dob"] = `${date.getDay()}-${date.getMonth()}-${date.getFullYear()}`;
    console.log(form);
  }, [date]);
  // Register function to submit the values
  const submit = e => {
    e.preventDefault();
    updateForm(n => {
      return { ...n, dob: toString(date.getDay() + "-" + date.getMonth() + "-" + date.getFullYear()) };
    });
    // console.log(form);
    const body = {
      name: form.firstName + " " + form.lastName,
      email: form.email,
      dob: form.dob,
      password: form.password1,
      country: form.country, // Please make sure to change this conditional statement later.
      phone_no: form.number,
    }

    console.log(body);
    let registeredSuccess = register(form); // register function should return an object
    if(registeredSuccess.success) {
      // then redirect to home
    } else if (registeredSuccess.customErr) {
      // State the problem message on top of the form
    } else {
      console.log("Sorry an error occurred :(");
      // Please use a good custom modal box to display this message.
    }
  }

  const [count, setCount] = useState(1);
  return (
    <div className="sign-body">
      <Nav />
      <div className="main">
        <form onSubmit={submit}>
          {count === 1 ? (
            <>
              <div className="firstname">
                <input type="text" value={form.firstName} onChange={updateFirstName} name="firstName" id="firstname" placeholder="First Name" />
              </div>
              <div className="lastname">
                <input type="text" value={form.lastName} onChange={updateLastName} name="lastName" id="lastname" placeholder="Last Name" />
              </div>
              <div className="username">
                <input type="text" value={form.userName} onChange={updateUserName} name="userName" id="username" placeholder="Username" />
              </div>
              <div className="dob">
                {/* <DateInput ev={updateDate} /> */}
                <DatePicker date={date} onDateChange={setDate} locale={enGB} format='dd-MM-yyyy'>
                  {({ inputProps, focused }) => <input className={'input' + (focused ? ' -focused' : '')} {...inputProps} />}
                </DatePicker>
              </div>
              <div className="country">
                <SelectCountry />
              </div>
            </>
          ) : null}
          
          {count === 2 ? (
            <>
              <div className="email">
                <input type="email" value={form.email} onChange={updateEmail} name="email" id="email" placeholder="Email" />
              </div>
              <div className="password">
                <input type="password" value={form.password1} onChange={updatePassword1} name="password1" id="password" placeholder="Password" minLength={6} maxLength={16} />
              </div>
              <div className="password">
                <input type="password" value={form.password2} onChange={updatePassword2} name="password2" id="password" placeholder="Confirm Password" minLength={6} maxLength={16} />
              </div>
              <div className="phonenumber">
                <PhoneInput counter="us" onChange={updateNumber} name="number" id="phone" style={{ "margin": "10px 0" }} />
              </div>
              <div className="submit">
                <button type="submit">Register</button>
              </div>
            </>
          ) : null}

          
        </form>
        <div className="btns">
          <button className="prev" hidden={count <= 1} onClick={() => setCount(count - 1)}><FaArrowLeft size={22} color="white" /></button>
          <button className="next" hidden={count > 1} onClick={() => setCount(count + 1)}><FaArrowRight size={22} color="white" /></button>
        </div>
      </div>
    </div>
  );
}

export default Signup;