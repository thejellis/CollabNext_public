import React from 'react';

import {Flex, Text} from '@chakra-ui/react';

const Navbar = () => {
  return (
    <Flex
      px='3rem'
      py='1.9rem'
      justifyContent={'space-between'}
      alignItems={'center'}
    >
      <Text
        fontFamily='DM Sans'
        fontSize='20px'
        color='#000000'
        fontWeight={'700'}
      >
        CollabNext
      </Text>
      <Flex>
        {['Home', 'About Us', 'People', 'Technology', 'Data Sources'].map(
          (navTitle) => (
            <Text mr='2.5rem' color='#000000'>
              {navTitle}
            </Text>
          ),
        )}
      </Flex>
      <Text fontSize='20px' color='#000000'>
        Account
      </Text>
    </Flex>
  );
};

export default Navbar;
