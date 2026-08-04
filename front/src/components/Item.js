import React, { Component } from 'react';

export class Item extends Component {
  
  handleBuy = async () => {
    const token = localStorage.getItem('token'); 
    if (!token) {
      alert("You need to log in first! Click 'Login' at the top");
      return;
    }

    try {

      const response = await fetch('http://localhost:8000/liqpay/params', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ item_id: this.props.item.id })
      });

      const { data, signature } = await response.json();

      const form = document.createElement('form');
      form.method = 'POST';
      form.action = 'https://www.liqpay.ua/api/3/checkout';
      form.acceptCharset = 'utf-8';

      const dataInput = document.createElement('input');
      dataInput.type = 'hidden';
      dataInput.name = 'data';
      dataInput.value = data;
      form.appendChild(dataInput);

      const sigInput = document.createElement('input');
      sigInput.type = 'hidden';
      sigInput.name = 'signature';
      sigInput.value = signature;
      form.appendChild(sigInput);

      document.body.appendChild(form);
      form.submit(); 
      document.body.removeChild(form);
    } catch (error) {
      console.error("error to pay:", error);
    }
  };

  render() {
    return (
      <div className='item'>
        <img 
          src={"./img/" + this.props.item.img} 
          alt={this.props.item.title} 
          className="item-img-btn"
          onClick={this.handleBuy} 
        />
        <h2>{this.props.item.title}</h2>
        <p>{this.props.item.desc}</p>
        <b>{this.props.item.price} UAH</b>
      </div>
    )
  }
}

export default Item;