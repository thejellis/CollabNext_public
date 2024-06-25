import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';

import { ChakraProvider} from '@chakra-ui/react';

import Footer from './components/Footer';
import Navbar from './components/Navbar';
// import NavbarMobile from './components/NavbarMobile';
import Home from './pages/Home';
import MainNavigation from './components/MainNavigation';
import ContactUs from './pages/ContactUs';

function App() {
  return (
    <ChakraProvider>
      <Navbar />
      <Router>
        <Routes>
          <Route path='/' element={<Home />}></Route>
          <Route path='/search' element={<MainNavigation />}></Route>
          <Route path='/aboutus' element={<ContactUs />}></Route>
        </Routes>
      </Router>
      <Footer />
    </ChakraProvider>
  );
}

export default App;
