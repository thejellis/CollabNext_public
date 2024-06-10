import React from 'react';

import {Flex, Text} from '@chakra-ui/react';

const Footer = () => {
  return (
    <Flex alignItems={'center'} mt='4rem'>
      <Flex mx='auto'>
        {['Contact Us', 'Help', 'Terms and Conditions', 'Provide Feedback'].map(
          (navTitle) => (
            <Text key={navTitle} mr='2.5rem' color='#000000'>
              {navTitle}
            </Text>
          ),
        )}
      </Flex>
    </Flex>
  );
};

export default Footer;
