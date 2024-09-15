export interface ResearchDataInterface {
  cited_count: string;
  works_count: string;
  institution_name: string;
  ror_link: string;
  author_count: string;
  institution_url: string;
  open_alex_link: string;
  graph?: {nodes: any[]; edges: any[]};
  is_hbcu: boolean;
  topics: string[][];
  organizations: string[][];
  topic_name: string;
  topic_clusters: string[];
  researcher_name: string;
  orcid_link: string;
  search?: 'topic' | 'researcher' | 'institution';
}
