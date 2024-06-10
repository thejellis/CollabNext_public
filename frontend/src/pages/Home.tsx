import React from 'react';

import {Box, Button, Flex, Input, SimpleGrid, Text} from '@chakra-ui/react';

const Home = () => {
  return (
    <Box w='700px' mx='auto' mt='1.5rem'>
      <Text fontFamily='DM Sans' fontSize='22px' color='#000000'>
        What are you searching for?
      </Text>
      <Box
        background='linear-gradient(180deg, #003057 0%, rgba(0, 0, 0, 0.5) 100%)'
        borderRadius='6px'
        px='2.5rem'
        py='2rem'
        mt='1rem'
      >
        <SimpleGrid columns={2} spacing={'90px'}>
          {[{text: 'Organization'}, {text: 'Institution Type'}].map(
            ({text}) => (
              <Box key={text}>
                <Input
                  variant={'flushed'}
                  focusBorderColor='white'
                  borderBottomWidth={'2px'}
                  color='white'
                  fontSize='20px'
                  textAlign={'center'}
                />
                <Text
                  fontSize='15px'
                  color='#FFFFFF'
                  textAlign={'center'}
                  mt='.7rem'
                >
                  {text}
                </Text>
              </Box>
            ),
          )}
        </SimpleGrid>
        <SimpleGrid mt='1rem' columns={2} spacing={'90px'}>
          {[{text: 'Topic(s)'}, {text: 'Researcher Name'}].map(({text}) => (
            <Box key={text}>
              <Input
                variant={'flushed'}
                focusBorderColor='white'
                borderBottomWidth={'2px'}
                color='white'
                fontSize='20px'
                textAlign={'center'}
              />
              <Text
                fontSize='15px'
                color='#FFFFFF'
                textAlign={'center'}
                mt='.7rem'
              >
                {text}
              </Text>
            </Box>
          ))}
        </SimpleGrid>
        <Flex justifyContent={'flex-end'} mt={'3rem'}>
          <Button
            width='205px'
            height='41px'
            background='#000000'
            borderRadius='6px'
            fontSize='18px'
            color='#FFFFFF'
            fontWeight={'500'}
          >
            Search
          </Button>
        </Flex>
      </Box>
    </Box>
  );
};

export default Home;
