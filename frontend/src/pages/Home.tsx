import React from 'react';

import {Box, Button, Flex, Input, SimpleGrid, Text} from '@chakra-ui/react';
import { useNavigate } from 'react-router-dom';

const Home = () => {

  const navigate = useNavigate();

  const handleSearch = () => {
    // Define the path you want to navigate to
    navigate('/search');
  };
  return (
    <Box w={{lg: '700px'}} mx='auto' mt='1.5rem'>
      <Text
        pl={{base: '1rem', lg: 0}}
        fontFamily='DM Sans'
        fontSize={{lg: '22px'}}
        color='#000000'
      >
        What are you searching for?
      </Text>
      <Box
        background='linear-gradient(180deg, #003057 0%, rgba(0, 0, 0, 0.5) 100%)'
        borderRadius={{lg: '6px'}}
        px={{base: '1.5rem', lg: '2.5rem'}}
        py={{base: '1.5rem', lg: '2rem'}}
        mt='1rem'
      >
        <SimpleGrid columns={{base: 1, lg: 2}} spacing={{base: 7, lg: '90px'}}>
          {[{text: 'Organization'}, {text: 'Institution Type'}].map(
            ({text}) => (
              <Box key={text}>
                <Input
                  variant={'flushed'}
                  focusBorderColor='white'
                  borderBottomWidth={'2px'}
                  color='white'
                  fontSize={{lg: '20px'}}
                  textAlign={'center'}
                />
                <Text
                  fontSize={{base: '12px', lg: '15px'}}
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
        <SimpleGrid
          mt={{base: '1.35rem', lg: '1rem'}}
          columns={{base: 1, lg: 2}}
          spacing={{base: 7, lg: '90px'}}
        >
          {[{text: 'Topic(s)'}, {text: 'Researcher Name'}].map(({text}) => (
            <Box key={text}>
              <Input
                variant={'flushed'}
                focusBorderColor='white'
                borderBottomWidth={'2px'}
                color='white'
                fontSize={{lg: '20px'}}
                textAlign={'center'}
              />
              <Text
                fontSize={{base: '12px', lg: '15px'}}
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
            width={{base: '165px', lg: '205px'}}
            height='41px'
            background='#000000'
            borderRadius={{base: '4px', lg: '6px'}}
            fontSize={{base: '13px', lg: '18px'}}
            color='#FFFFFF'
            fontWeight={'500'}
            onClick={handleSearch}
          >
            Search
          </Button>
        </Flex>
      </Box>
    </Box>
  );
};

export default Home;
