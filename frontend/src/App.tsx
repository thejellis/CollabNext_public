import {BrowserRouter as Router, Route, Routes} from 'react-router-dom';

import {Box, ChakraProvider} from '@chakra-ui/react';

import Footer from './components/Footer';
import Navbar from './components/Navbar';
import NavbarMobile from './components/NavbarMobile';
import About from './pages/About';
import Home from './pages/Home';

function App() {
  return (
    <Router>
      <ChakraProvider>
        <Box display={{base: 'none', lg: 'block'}}>
          <Navbar />
        </Box>
        <Box display={{lg: 'none'}}>
          <NavbarMobile />
        </Box>
        <Box>
          <Routes>
            <Route path='/' element={<Home />}></Route>
          </Routes>
          <Routes>
            <Route path='/about' element={<About />}></Route>
          </Routes>
        </Box>
        <Footer />
      </ChakraProvider>
    </Router>
  );
}

export default App;
