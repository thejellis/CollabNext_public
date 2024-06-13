import React from 'react';

import {Flex, Text} from '@chakra-ui/react';

const Footer = () => {
  return (
    <Flex alignItems={'center'} mt={{base: '2.5rem', lg: '4rem'}}>
      <Flex mx='auto'>
        {['Contact Us', 'Help', 'Terms and Conditions', 'Provide Feedback'].map(
          (navTitle) => (
            <Text
              key={navTitle}
              fontSize={{base: '8px', lg: '16px'}}
              mr={{base: '1.3rem', lg: '2.5rem'}}
              color='#000000'
            >
              {navTitle}
            </Text>
          ),
        )}
      </Flex>
    </Flex>
  );
};

export default Footer;
