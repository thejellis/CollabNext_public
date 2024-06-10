import {BrowserRouter as Router, Route, Routes} from 'react-router-dom';

import {ChakraProvider} from '@chakra-ui/react';

import Home from './pages/Home';

function App() {
  return (
    <ChakraProvider>
      <Router>
        <Routes>
          <Route path='/' element={<Home />}></Route>
        </Routes>
      </Router>
    </ChakraProvider>
  );
}

export default App;
