import React, { useRef } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { Icosahedron, MeshDistortMaterial } from '@react-three/drei';

function CoreShape({ isThinking }) {
  const meshRef = useRef();
  
  // Rotate the shape
  useFrame((state, delta) => {
    if (meshRef.current) {
      meshRef.current.rotation.x += delta * (isThinking ? 2.5 : 0.2);
      meshRef.current.rotation.y += delta * (isThinking ? 3.0 : 0.3);
      
      // Add a slight floating effect
      meshRef.current.position.y = Math.sin(state.clock.elapsedTime) * 0.1;
    }
  });

  return (
    <Icosahedron ref={meshRef} args={[1, 1]} scale={1.5}>
      <MeshDistortMaterial 
        color={isThinking ? "#c084fc" : "#6366f1"}
        envMapIntensity={1}
        clearcoat={1}
        clearcoatRoughness={0.1}
        metalness={0.5}
        roughness={0.2}
        distort={isThinking ? 0.6 : 0.2}
        speed={isThinking ? 5 : 1}
        wireframe={true}
      />
    </Icosahedron>
  );
}

export default function AICore3D({ isThinking }) {
  return (
    <div style={{ width: '200px', height: '200px', margin: '0 auto', filter: isThinking ? 'drop-shadow(0 0 20px rgba(192, 132, 252, 0.8))' : 'drop-shadow(0 0 10px rgba(99, 102, 241, 0.4))', transition: 'filter 0.5s ease' }}>
      <Canvas camera={{ position: [0, 0, 4] }}>
        <ambientLight intensity={0.5} />
        <directionalLight position={[10, 10, 5]} intensity={1} color="#ffffff" />
        <directionalLight position={[-10, -10, -5]} intensity={0.5} color="#c084fc" />
        <CoreShape isThinking={isThinking} />
      </Canvas>
    </div>
  );
}
