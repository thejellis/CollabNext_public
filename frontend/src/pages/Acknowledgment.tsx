import React from "react";
import PersonCard from "../components/PersonCard";

const Acknowledgment = () => {
  const person = {
    image: "https://via.placeholder.com/150",
    name: "John Doe",
    description: "A passionate developer who loves to create web applications.",
    linkedin: "https://linkedin.com/in/johndoe",
    github: "https://github.com/johndoe",
    portfolio: "https://johndoe.com",
  };

  return (
    <div>
      <PersonCard person={person} />
      <PersonCard person={person} />
      <PersonCard person={person} />
      <PersonCard person={person} />
    </div>
  );
};

export default Acknowledgment;
