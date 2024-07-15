export interface ResearchDataInterface {
  cited_count: string;
  works_count: string;
  works: string[];
  institution_name: string;
  researcher_name: string;
  ror: string;
  author_count: string;
  url: string;
  worksAreTopics: boolean;
  worksAreAuthors: boolean;
  link: string;
  graph: {data: any}[];
}
