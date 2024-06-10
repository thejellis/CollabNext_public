import {BrowserRouter as Router, Route, Routes} from 'react-router-dom';

import {ChakraProvider} from '@chakra-ui/react';

import Footer from './components/Footer';
import Navbar from './components/Navbar';
import Home from './pages/Home';

function App() {
  return (
    <ChakraProvider>
      <Navbar />
      <Router>
        <Routes>
          <Route path='/' element={<Home />}></Route>
        </Routes>
      </Router>
      <Footer />
    </ChakraProvider>
  );
}

export default App;
