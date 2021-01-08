import React from 'react';
import "../styles/Footer.css";
import FooterNav from "./FooterNav";

const Footer = () => {
  return (
    <footer>
      <div className="logo">Filba</div>
      <FooterNav />
    <div className="copyrights">&copy; All rights reserved copyright {(new Date()).getFullYear()}</div>
    </footer>
  );
}

export default Footer;