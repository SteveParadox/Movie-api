/* // This is an experimental component to implement slide show effect
import React, { Component, useEffect } from "react";
import ReactDOM from "react-dom";
// import Joker from "./joker_movie.jpg";

class ReactSlider extends Component {
  render() {
    return (
      <div>
        <button onClick={() => console.log(ReactDOM.findDOMNode(this.refs.textInput).value)}>Get Element</button>
        <input type="text" ref="textInput" />
      </div>
    );
  }
}

export default ReactSlider; */

import React, { useEffect, useState, useRef } from "react";
import { FaAngleRight, FaAngleLeft } from "react-icons/fa";
import "./ReactSlider.css";


// class ReactSlider extends Component {
//   constructor(props) {
//     super(props);

//     this.state = {

//     };
//   }

//   render() {
//     return (
//       <div className="slide-container">
//         <div className="slide-prop-arrow slide-prop-arrow-left">
//           <FaAngleLeft />
//         </div>

//         <div className="slide-container">
//           {this.props.children}
//         </div>

//         <div className="slide-prop-arrow slide-prop-arrow-right">
//           <FaAngleRight />
//         </div>

//       </div>
//     );
//   }
// }

function ReactSlider(props) {
  const showRef = useRef();
  const rightBtn = useRef();
  const leftBtn = useRef();
  const refPag = useRef();
  const [currentSlide, setCurrentSlide] = useState(0);
  const length = props.children.length;

  const angleStyle1 = currentSlide <= 0 ? {
    "opacity": "0.5"
  } : {
    "opacity": "1"
  };

  const angleStyle2 = currentSlide <= 0 ? {
    "opacity": "0.5"
  } : {
    "opacity": "1"
  };

  function handleBtns() {
    /* PLEASE 
      GIVE M
      ORE 
      ATTENTION 
      TO 
      THIS 
      */
     refPag.current.childNodes.forEach(i => {
      i.style.background = "nervousela !important";
      if(Number(i.getAttribute("key")) === currentSlide) {
        i.style.backgrounud = "white !important";
      }
    });
  }

  
  function slideRight() {
    // console.log(showRef.current.childNodes["length"]);
    // showRef.current.scrollBy(parseInt(getComputedStyle(showRef.current.firstChild).width), 0);
    leftBtn.current.disabled = false;
    if(currentSlide === length) {
      setCurrentSlide(0);
      return;
    } else if(currentSlide === length -1) {
        rightBtn.current.disabled = true;
    }
    else {
      setCurrentSlide(prevState => prevState + 1);
      rightBtn.current.disabled = false;
    }
    showRef.current.childNodes[currentSlide].scrollIntoView();
    handleBtns();
    // console.log(refPag.current.childNodes);
  }

  function slideLeft() {
    // console.log(showRef.current.childNodes["length"]);
    // showRef.current.scrollBy(parseInt(getComputedStyle(showRef.current.firstChild).width), 0);
    rightBtn.current.disabled = false;
    if(currentSlide === 0) {
      setCurrentSlide(1);
      return;
    } 
    // else if(currentSlide < 0) {
    //   leftBtn.current.disabled = true;
    // }
    else {
      setCurrentSlide(prevState => prevState - 1);
      leftBtn.current.disabled = false;
    }
    handleBtns();
    showRef.current.childNodes[currentSlide].scrollIntoView();
    // console.log(props.children);
  }

  // const activeStyle = {
  //   "background": "white !important"
  // };

  return (
    <div className="slide-container">
      <div className="slide-prop-arrow slide-prop-arrow-left">
        <button ref={leftBtn} onClick={slideLeft}>
          <FaAngleLeft 
            style={angleStyle1}
          />
        </button>
      </div>

      <div className="slide-container" ref={showRef}>
        {props.children}
      </div>

      <div className="slide-prop-arrow slide-prop-arrow-right">
        <button ref={rightBtn} onClick={slideRight}>
          <FaAngleRight style={angleStyle2}/>
        </button>
      </div>

      <div className="slide-prop-pagination" ref={refPag}>
        {props.children.map((i, idx) => (
          <div className="slide-prop-pagination-btn" key={idx} ></div>
        ))}        
      </div>

    </div>
  );
}

export default ReactSlider;