import React, { useEffect, useRef } from 'react';
import { Orb } from '@memgraph/orb';

const GraphComponent = ({ graphData }) => {
  const graphContainerRef = useRef(null);
  const loaderOverlayRef = useRef(null);
  const detailsRef = useRef(null);

  useEffect(() => {
    if (!graphData) {
      return; // Exit early if no data is provided
    }

    const { nodes, edges } = graphData; // Destructure nodes and edges from graphData

    const container = graphContainerRef.current;
    const orb = new Orb(container);

    orb.view.setSettings({
      render: {
        backgroundColor: '#f4faff',
        padding: '0',
        margin: '0',
      },
    });

    orb.data.setDefaultStyle({
      getNodeStyle(node) {
        const basicStyle = {
          borderColor: '#1d1d1d',
          borderWidth: 0.6,
          color: '#DD2222',
          colorHover: '#e7644e',
          colorSelected: '#e7644e',
          fontSize: 3,
          label: node.data.label,
          size: 6,
        };

        if (node.data.type === 'AUTHOR') {
          return {
            ...basicStyle,
            size: 10,
            color: '#0df2c9',
            zIndex: 1,
          };
        }

        if (node.data.type === 'WORK') {
          return {
            ...basicStyle,
            size: 10,
            color: '#245cc3',
            zIndex: 1,
          };
        }

        if (node.data.type === 'TOPIC') {
          return {
            ...basicStyle,
            size: 10,
            color: '#f8ee35',
            zIndex: 1,
          };
        }

        return {
          ...basicStyle,
        };
      },
      getEdgeStyle(edge) {
        return {
          color: '#999999',
          colorHover: '#1d1d1d',
          colorSelected: '#1d1d1d',
          fontSize: 3,
          width: 0.3,
          widthHover: 0.9,
          widthSelected: 0.9,
          label: edge.data.label,
        };
      },
    });

    if (loaderOverlayRef.current) {
      loaderOverlayRef.current.style.display = 'flex';
    }

    orb.data.setup({ nodes, edges });

    orb.view.render(() => {
      if (loaderOverlayRef.current) {
        loaderOverlayRef.current.style.display = 'none';
      }
      if (detailsRef.current) {
        detailsRef.current.style.display = 'block';
      }
      orb.view.recenter();
    });
  }, [graphData]);

  return (
    <div>
      <div ref={loaderOverlayRef} id="loader-overlay" style={{ display: 'none' }}>
        Loading...
      </div>
      <div ref={graphContainerRef} id="graph" style={{ height: '500px', width: '100%' }} />
      <div ref={detailsRef} className="details" style={{ display: 'none' }}>
        {/* Any additional details to display */}
      </div>
    </div>
  );
};

export default GraphComponent;
