import React from "react";

interface Person {
  image?: string;
  name?: string;
  description?: string;
  linkedin?: string;
  github?: string;
  portfolio?: string;
}

interface PersonCardProps {
  person: Person;
}

const PersonCard: React.FC<PersonCardProps> = ({ person }) => {
  if (!person || typeof person !== "object") {
    console.error("Invalid person data:", person);
    return null;
  }

  return (
    <div className="bg-white shadow-lg rounded-lg overflow-hidden flex flex-col h-full">
      <div className="relative pb-2/3 sm:pb-1/2 lg:pb-1/3">
        <img src={person.image} alt="" />
      </div>
      <div className="p-4 flex flex-col flex-grow">
        <h2 className="text-xl font-bold text-gray-900 mb-2">
          {person.name || "Unknown"}
        </h2>
        <p className="text-gray-600 text-sm flex-grow mb-4">
          {person.description || "No description available"}
        </p>
        <div className="flex flex-wrap gap-2 mt-auto">
          {person.linkedin && (
            <SocialLink href={person.linkedin} label="LinkedIn" />
          )}
          {person.github && <SocialLink href={person.github} label="GitHub" />}
          {person.portfolio && (
            <SocialLink href={person.portfolio} label="Portfolio" />
          )}
        </div>
      </div>
    </div>
  );
};

interface SocialLinkProps {
  href: string;
  label: string;
}

const SocialLink: React.FC<SocialLinkProps> = ({ href, label }) => (
  <a
    href={href}
    target="_blank"
    rel="noopener noreferrer"
    className="text-sm bg-indigo-100 text-indigo-700 px-3 py-1 rounded-full hover:bg-indigo-200 transition-colors"
  >
    {label}
  </a>
);

export default PersonCard;
