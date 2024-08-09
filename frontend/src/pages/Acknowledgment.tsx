import React, { useState, Suspense } from "react";
import team_members from "../assets/team_members.json";
const PersonCard = React.lazy(() => import("../components/PersonCard"));

const peopleData = team_members.members;

const AcknowledgementsPage: React.FC = () => {
  const [expandedCardIndex, setExpandedCardIndex] = useState<number | null>(
    null
  );

  const handleToggleExpand = (index: number) => {
    setExpandedCardIndex(expandedCardIndex === index ? null : index);
  };

  if (!Array.isArray(peopleData) || peopleData.length === 0) {
    console.error("peopleData is not an array or is empty:", peopleData);
    return <div>Error loading data</div>;
  }

  return (
    <div className="bg-gray-100 min-h-screen py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-4xl font-bold text-gray-900 text-center mb-12">
          Acknowledgements
        </h1>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8">
          {peopleData.map((person, index) => (
            <Suspense
              key={index}
              fallback={
                <div className="bg-white rounded-lg shadow-md p-4 h-96 animate-pulse">
                  <div className="bg-gray-300 h-48 rounded-md mb-4"></div>
                  <div className="bg-gray-300 h-4 rounded w-3/4 mb-2"></div>
                  <div className="bg-gray-300 h-4 rounded w-1/2 mb-4"></div>
                  <div className="bg-gray-300 h-20 rounded mb-4"></div>
                  <div className="flex space-x-2">
                    {[...Array(4)].map((_, i) => (
                      <div
                        key={i}
                        className="bg-gray-300 h-6 w-6 rounded-full"
                      ></div>
                    ))}
                  </div>
                </div>
              }
            >
              <PersonCard
                person={person}
                isExpanded={expandedCardIndex === index}
                onToggleExpand={() => handleToggleExpand(index)}
              />
            </Suspense>
          ))}
        </div>
      </div>
    </div>
  );
};

export default AcknowledgementsPage;
