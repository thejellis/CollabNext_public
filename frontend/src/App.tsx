import React from 'react';
import {Route, Routes} from 'react-router-dom';

import {Box, ChakraProvider} from '@chakra-ui/react';

import Footer from './components/Footer';
import Navbar from './components/Navbar';
import NavbarMobile from './components/NavbarMobile';
import About from './pages/About';
import Technology from './pages/Technology';
import Acknowledgment from './pages/Acknowledgment';
import ContactUs from './pages/Contact';
import Feedback from './pages/Feedback';
import Help from './pages/Help';
import Home from './pages/Home';
import Search from './pages/Search';
import TopicSearch from './pages/TopicSearch';
import DataSources from './pages/DataSources';
import Terms from './pages/Terms';

function App() {
  return (
    <ChakraProvider>
      <Box display={{base: 'none', lg: 'block'}}>
        <Navbar />
      </Box>
      <Box display={{lg: 'none'}}>
        <NavbarMobile />
      </Box>
      <Box>
        <Routes>
          <Route path='/' element={<Home />} />
          <Route path='/about' element={<About />} />
          <Route path='/technology' element={<Technology />} />
          <Route path='/search' element={<Search />} />
          <Route path='/topic-search' element={<TopicSearch />} />
          <Route path='/contact' element={<ContactUs />} />
          <Route path='/team' element={<Acknowledgment />} />
          <Route path='/feedback' element={<Feedback />}/>
          <Route path='/data' element={<DataSources />} />
          <Route path='/terms' element={<Terms />} />
          <Route path='/help' element={<Help />} />
        </Routes>
      </Box>
      <Footer />
    </ChakraProvider>
  );
}

export default App;
