import React from "react";
import Header from "./components/Header";
import Footer from "./components/Footer";
import Items from './components/Items';
import Profile from './components/Profile';
import AboutUs from './pages/AboutUs';

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      currentPage: 'home', 
      items: [
        { id: 1, title: 'vip status', img: 'vip.png', desc: 'базовий мінімум...', category: 'status', price: '52' },
        { id: 2, title: 'admin', img: 'admin.png', desc: 'літай, твори...', category: 'status', price: '100' },
        { id: 3, title: 'console', img: 'console.png', desc: 'створюй або знищуй...', category: 'status', price: '200' }
      ]
    };
    this.setCurrentPage = this.setCurrentPage.bind(this);
  }

  setCurrentPage(page) {
    this.setState({ currentPage: page });
  }

  render() {
    return (
      <div className="wrapper">
        <Header setCurrentPage={this.setCurrentPage} />
        <main>
          {this.state.currentPage === 'home' && <Items items={this.state.items} />}
          {this.state.currentPage === 'profile' && <Profile />}
          {this.state.currentPage === 'about' && <AboutUs />}
        </main>
        <Footer />
      </div>
    );
  }
}

export default App;
