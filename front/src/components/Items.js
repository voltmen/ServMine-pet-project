import React, { Component } from 'react';
import Item from './Item';

export class Items extends Component {
  render() {
    return (
      <main>
        {/* Ми проходимося циклом по всіх товарах, які ти додаси в App.js */}
        {this.props.items.map(el => (
          <Item key={el.id} item={el} />
        ))}
      </main>
    )
  }
}

export default Items;