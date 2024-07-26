import '../styles/Search.css';

import React, {useEffect, useState} from 'react';
import {Circles} from 'react-loader-spinner';
import {useSearchParams} from 'react-router-dom';

import {Box, Button, Text} from '@chakra-ui/react';

// import CytoscapeComponent from 'react-cytoscapejs';
import GraphComponent from '../components/GraphComponent';
// import NetworkMap from '../assets/NetworkMap.png';
import {baseUrl, initialValue} from '../utils/constants';
import {ResearchDataInterface} from '../utils/interfaces';

const Search = () => {
  // console.log(baseUrl);
  let [searchParams] = useSearchParams();
  // const cyRef = React.useRef<cytoscape.Core | undefined>();
  const institution = searchParams.get('institution');
  const type = searchParams.get('type');
  const topic = searchParams.get('topic');
  const researcher = searchParams.get('researcher');
  const [isNetworkMap, setIsNetworkMap] = useState(false);
  const [universityName, setUniversityName] = useState(institution || '');
  let [topicType, setTopicType] = useState(topic || '');
  const [institutionType, setInstitutionType] = useState(type || 'Education');
  const [researcherType, setResearcherType] = useState(researcher || '');
  const [data, setData] = useState<ResearchDataInterface>(initialValue);
  const [isLoading, setIsLoading] = useState(false);

  // const toast = useToast();

  const handleToggle = () => {
    setIsNetworkMap(!isNetworkMap);
  };

  useEffect(() => {
    handleSearch();
  }, []);

  const handleSearch = (topic?: string) => {
    // if (topicType && !researcherType) {
    //   setData(initialValue);
    //   return;
    // }
    if (researcherType || universityName || topicType) {
      setIsLoading(true);
      if (topic) {
        topicType = topic;
      }
      if (
        (!topicType && !researcherType) ||
        (!researcherType && !universityName) ||
        (!topicType && !universityName)
      ) {
        fetch(`${baseUrl}/initial-search`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            organization: universityName,
            type: institutionType,
            topic: topicType,
            researcher: researcherType,
          }),
        })
          .then((res) => res.json())
          .then((data) => {
            console.log(data);
            setData({
              cited_count:
                data?.metadata?.cited_count || data?.metadata?.cited_by_count,
              works_count:
                data?.metadata?.works_count || data?.metadata?.work_count,
              works: [],
              institution_name: researcherType
                ? data?.metadata?.current_institution
                : data?.metadata?.name,
              researcher_name: researcherType ? data?.metadata?.name : '',
              ror: data?.metadata?.ror,
              author_count: data?.metadata?.author_count,
              url: data?.metadata?.homepage || data?.metadata?.orcid,
              worksAreAuthors: false,
              worksAreTopics: false,
              link: data?.metadata?.oa_link,
              graph: data?.graph,
            });
            setIsLoading(false);
          })
          .catch((error) => {
            setIsLoading(false);
            setData(initialValue);
            console.log(error);
          });
        return;
      }
      fetch(`${baseUrl}/initial-search`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          // organization: 'Georgia Institute of Technology',
          // researcher: 'Didier Contis',
          // type: '',
          // topic: 'Network Intrusion Detection and Defense Mechanisms',
          organization: universityName,
          type: institutionType,
          topic: topicType,
          researcher: researcherType,
        }),
      })
        .then((res) => res.json())
        .then((data) => {
          console.log(data);
          setData({
            cited_count:
              data?.author_metadata?.cited_by_count ||
              data?.institution_metadata?.cited_count,
            works_count:
              data?.author_metadata?.work_count ||
              data?.institution_metadata?.works_count,
            works:
              (!topicType
                ? data?.topics?.names
                : !researcherType
                ? data?.authors?.names
                : data?.works?.titles) || [],
            worksAreTopics: !topicType ? true : false,
            worksAreAuthors: !researcherType ? true : false,
            institution_name: !universityName
              ? data?.author_metadata?.current_institution
              : data?.institution_metadata?.name,
            researcher_name: data?.author_metadata?.name || '',
            ror: data?.institution_metadata?.ror,
            author_count: '',
            url:
              data?.author_metadata?.orcid ||
              data?.institution_metadata?.homepage,
            link:
              data?.author_metadata?.oa_link ||
              data?.institution_metadata?.oa_link,
            graph: data?.graph,
          });
          setIsLoading(false);
        })
        .catch((error) => {
          setIsLoading(false);
          setData(initialValue);
          console.log(error);
        });
    } else {
      setIsLoading(true);
      fetch(`${baseUrl}/get-default-graph`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: null,
      })
        .then((res) => res.json())
        .then((data) => {
          console.log(data);
          setData({
            ...initialValue,
            graph: data?.graph,
          });
          setIsNetworkMap(true);
          setIsLoading(false);
        })
        .catch((error) => {
          setIsLoading(false);
          setData(initialValue);
          console.log(error);
        });
      // toast({
      //   title: 'Error',
      //   description: 'All 3 fields cannot be empty',
      //   status: 'error',
      //   duration: 8000,
      //   isClosable: true,
      //   position: 'top-right',
      // });
    }
  };

  return (
    <div className='main-content'>
      <div className='sidebar'>
        <input
          type='text'
          value={universityName}
          onChange={(e) => setUniversityName(e.target.value)}
          placeholder='University Name'
          className='textbox'
          disabled={isLoading}
        />
        <input
          type='text'
          value={topicType}
          onChange={(e) => setTopicType(e.target.value)}
          placeholder='Type Topic'
          className='textbox'
          disabled={isLoading}
        />
        <select
          value={institutionType}
          onChange={(e) => setInstitutionType(e.target.value)}
          className='dropdown'
        >
          <option value='Education'>Education</option>
        </select>
        {/* <FormControl isInvalid={topicType && !researcherType ? true : false}> */}
        <input
          type='text'
          value={researcherType}
          onChange={(e) => setResearcherType(e.target.value)}
          placeholder='Type Researcher'
          className='textbox'
          disabled={isLoading}
        />
        {/* <FormErrorMessage>
            Researcher must be provided when Topic is
          </FormErrorMessage>
        </FormControl> */}
        <Button
          width='100%'
          marginTop='10px'
          backgroundColor='transparent'
          color='white'
          border='2px solid white'
          isLoading={isLoading}
          onClick={() => handleSearch()}
        >
          Search
        </Button>
        <button className='button' onClick={handleToggle}>
          {isNetworkMap ? 'See List Map' : 'See Network Map'}
        </button>
      </div>
      <div className='content'>
        {isLoading ? (
          <Box
            w={{lg: '500px'}}
            justifyContent={'center'}
            height={{base: '190px', lg: '340px'}}
            display={'flex'}
            alignItems='center'
          >
            <Circles
              height='80'
              width='80'
              color='#003057'
              ariaLabel='circles-loading'
              wrapperStyle={{}}
              wrapperClass=''
              visible={true}
            />
          </Box>
        ) : !data?.graph ? (
          <Box fontSize={{lg: '20px'}} ml={{lg: '4rem'}} fontWeight={'bold'}>
            No result
          </Box>
        ) : isNetworkMap ? (
          <div className='network-map'>
            <button className='topButton'>Network Map</button>
            {/* <img src={NetworkMap} alt='Network Map' /> */}
            <GraphComponent graphData={data?.graph} />
          </div>
        ) : (
          <div>
            <button className='topButton'>List Map</button>
            <h2>{data?.institution_name}</h2>
            <h2 style={{marginTop: '.4rem'}}>{data?.researcher_name}</h2>
            <div className='list-map'>
              <div>
                {data?.ror && (
                  <a
                    target='_blank'
                    rel='noreferrer'
                    className='ror'
                    href={data?.ror}
                  >
                    RORID -{' '}
                    {data?.ror?.split('/')[data?.ror?.split('/')?.length - 1]}
                  </a>
                )}
                {data?.url && (
                  <a
                    target='_blank'
                    rel='noreferrer'
                    className='ror'
                    href={data?.url}
                  >
                    {data?.url}
                  </a>
                )}
                {data?.author_count && (
                  <p>Total {data?.author_count} authors</p>
                )}
                <p>Total {data?.works_count} works</p>
                <p>Total {data?.cited_count} citations</p>
                <a target='_blank' rel='noreferrer' href={data?.link}>
                  View on OpenAlex
                </a>
              </div>
              <div className='dep-content'>
                {data?.works?.map((eachWork) => (
                  <Text
                    onClick={() => {
                      if (data?.worksAreTopics) {
                        setTopicType(eachWork);
                        handleSearch(eachWork);
                      }
                      if (data?.worksAreAuthors) {
                        setResearcherType(eachWork);
                        handleSearch(eachWork);
                      }
                    }}
                    cursor={
                      data?.worksAreTopics || data?.worksAreAuthors
                        ? 'pointer'
                        : 'default'
                    }
                    key={eachWork}
                    textDecoration={
                      data?.worksAreTopics || data?.worksAreAuthors
                        ? 'underline'
                        : 'none'
                    }
                  >
                    {eachWork}
                  </Text>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Search;
