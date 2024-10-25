import React from 'react';
import {Link} from 'react-router-dom';

import { Flex, Text } from '@chakra-ui/react';
import Terms from '../pages/Terms';

const Footer = () => {
  return (
    <Flex alignItems={'center'} my={{base: '2.5rem', lg: '4rem'}}>
      <Flex mx='auto'>
        {[
          {text: 'Contact Us', href: '/contact'},
          { text: 'Terms and Conditions', href: '/terms' },
          {text: 'Help', href: '/help'},
          {text: 'Provide Feedback', href: '/feedback'},
        ].map(({text, href}) => (
          <Text
            key={text}
            fontSize={{base: '8px', lg: '16px'}}
            mr={{base: '1.3rem', lg: '2.5rem'}}
            color='#000000'
          >
            <Link to={href}>{text}</Link>
          </Text>
        ))}
      </Flex>
    </Flex>
  );
};

export default Footer;
