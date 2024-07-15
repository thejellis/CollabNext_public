import React from 'react';
import { Link } from 'react-router-dom';

import { Flex, Image, Text } from '@chakra-ui/react';

const Navbar = () => {
  return (
    <Flex
      px='3rem'
      py='1.9rem'
      justifyContent={'space-between'}
      alignItems={'center'}
    >
      {/* <Text
        fontFamily='DM Sans'
        fontSize='20px'
        color='#000000'
        fontWeight={'700'}
      >
        CollabNext
      </Text> */}
      <Link to='/'>
        <Image src='/favicon.png' w='52px' h='77px' objectFit={'cover'}></Image>
      </Link>
      <Flex>
        {[
          {text: 'Home', href: '/'},
          {text: 'About Us', href: '/about'},
          {text: 'People', href: '/'},
          {text: 'Technology', href: '/'},
          {text: 'Data Sources', href: '/'},
        ].map(({text, href}) => (
          <Text key={text} mr='2.5rem' color='#000000'>
            <Link to={href}>{text}</Link>
          </Text>
        ))}
      </Flex>
      <Text fontSize='20px' color='#000000'>
        Account
      </Text>
    </Flex>
  );
};

export default Navbar;
