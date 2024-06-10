import React from 'react';

import {Flex, Text} from '@chakra-ui/react';

const Footer = () => {
  return (
    <Flex alignItems={'center'}>
      <Flex mx='auto'>
        {['Contact Us', 'Help', 'Terms and Conditions', 'Provide Feedback'].map(
          (navTitle) => (
            <Text mr='2.5rem' color='#000000'>
              {navTitle}
            </Text>
          ),
        )}
      </Flex>
    </Flex>
  );
};

export default Footer;
