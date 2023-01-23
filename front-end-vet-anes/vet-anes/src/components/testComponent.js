import React from "react";

const Test = ({ drugList, loadDrugList }) => {
  const drugComponents = [];
  for (const drug of drugList) {
    drugComponents.push(
      <li key={drug.id}>
        {drug.name} {drug.concentration}
      </li>
    );
  }
  return (
    <div>
      <h3>Drugs</h3>
      <ul>{drugComponents}</ul>
    </div>
  );
};

export default Test;
