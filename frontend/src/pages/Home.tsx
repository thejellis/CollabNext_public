import { Field, Form, Formik } from 'formik';
import React from 'react';
import { useNavigate } from 'react-router-dom';
import * as Yup from 'yup';

import {
	Box,
	Button,
	Flex,
	FormControl,
	FormErrorMessage,
	Input,
	SimpleGrid,
	Text,
} from '@chakra-ui/react';

const validateSchema = Yup.object().shape({
  institution: Yup.string().required('This field is required'),
  type: Yup.string().notRequired(),
  topic: Yup.string().notRequired(),
  researcher: Yup.string().notRequired(),
});

const initialValues = {
  institution: '',
  type: '',
  topic: '',
  researcher: '',
};

const Home = () => {
  const navigate = useNavigate();
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
        <Formik
          initialValues={initialValues}
          enableReinitialize
          validationSchema={validateSchema}
          onSubmit={async ({institution, type, topic, researcher}) => {
            console.log(`institution: ${institution}`);
            console.log(`type: ${type}`);
            console.log(`topic: ${topic}`);
            console.log(`researcher: ${researcher}`);
            navigate(
              `?institution=${institution}&type=${type}&topic=${topic}&researcher=${researcher}`,
            );
          }}
        >
          {(props) => (
            <Form>
              <SimpleGrid
                columns={{base: 1, lg: 2}}
                spacing={{base: 7, lg: '90px'}}
              >
                {[
                  {text: 'Organization', key: 'institution'},
                  {text: 'Institution Type', key: 'type'},
                ].map(({text, key}) => (
                  <Box key={text}>
                    <Field name={key}>
                      {({field, form}: any) => (
                        <FormControl
                          isInvalid={form.errors[key] && form.touched[key]}
                        >
                          <Input
                            variant={'flushed'}
                            focusBorderColor='white'
                            borderBottomWidth={'2px'}
                            color='white'
                            fontSize={{lg: '20px'}}
                            textAlign={'center'}
                            {...field}
                          />
                          <FormErrorMessage>
                            {form.errors[key]}
                          </FormErrorMessage>
                        </FormControl>
                      )}
                    </Field>
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
              <SimpleGrid
                mt={{base: '1.35rem', lg: '1rem'}}
                columns={{base: 1, lg: 2}}
                spacing={{base: 7, lg: '90px'}}
              >
                {[
                  {text: 'Topic(s)', key: 'topic'},
                  {text: 'Researcher Name', key: 'researcher'},
                ].map(({text, key}) => (
                  <Box key={text}>
                    <Field name={key}>
                      {({field, form}: any) => (
                        <FormControl
                          isInvalid={form.errors[key] && form.touched[key]}
                        >
                          <Input
                            variant={'flushed'}
                            focusBorderColor='white'
                            borderBottomWidth={'2px'}
                            color='white'
                            fontSize={{lg: '20px'}}
                            textAlign={'center'}
                            {...field}
                          />
                          <FormErrorMessage>
                            {form.errors[key]}
                          </FormErrorMessage>
                        </FormControl>
                      )}
                    </Field>
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
                  type='submit'
                >
                  Search
                </Button>
              </Flex>
            </Form>
          )}
        </Formik>
      </Box>
    </Box>
  );
};

export default Home;
